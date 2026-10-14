import hashlib
import shutil
from collections import defaultdict
from collections.abc import Callable, Iterable
from enum import Enum
from pathlib import Path

from config import Config

class Mode(Enum):
    REMOVE_CONTENT_DUPLICATES = "duplicate-content"
    REMOVE_NAME_DUPLICATES = "duplicate-name"
    NORMALIZE_NAME = "problematic-name"
    REMOVE_TEMPORARY = "temporary"
    REMOVE_EMPTY = "empty"
    NORMALIZE_PERMISSIONS = "permissions"
    MOVE_TO_MAIN = "move"


class Message(Enum):
    REMOVE_CONTENT_DUPLICATES = (
        "Remove duplicate-content files and keep the oldest version"
    )
    REMOVE_NAME_DUPLICATES = (
        "Remove duplicate-name files and keep the newest version"
    )
    NORMALIZE_NAME = "Normalize the name of"
    REMOVE_TEMPORARY = "Remove temporary file"
    REMOVE_EMPTY = "Remove empty file"
    NORMALIZE_PERMISSIONS = "Normalize permissions for"
    MOVE_TO_MAIN = "Move file to the main directory"


class FileOrganizer:
    def __init__(
        self,
        config: Config,
        main_dir: Path,
        directories: list[Path],
        mode: Mode | str,
        is_interactive: bool = False,
        dry_run: bool = False,
    ) -> None:
        self._config = config
        self._main_dir = main_dir.resolve()
        self._directories = [directory.resolve() for directory in directories]
        self._mode = mode if isinstance(mode, Mode) else Mode(mode)
        self._is_interactive = is_interactive
        self._dry_run = dry_run

        self._actions: dict[Mode, Callable[[], None]] = {
            Mode.REMOVE_CONTENT_DUPLICATES: self._remove_content_duplicates,
            Mode.REMOVE_NAME_DUPLICATES: self._remove_name_duplicates,
            Mode.NORMALIZE_NAME: self._normalize_problematic_names,
            Mode.REMOVE_TEMPORARY: self._remove_temporary,
            Mode.REMOVE_EMPTY: self._remove_empty,
            Mode.NORMALIZE_PERMISSIONS: self._normalize_permissions,
            Mode.MOVE_TO_MAIN: self._move_to_main,
        }

        self._messages: dict[Mode, Message] = {
            Mode.REMOVE_CONTENT_DUPLICATES: Message.REMOVE_CONTENT_DUPLICATES,
            Mode.REMOVE_NAME_DUPLICATES: Message.REMOVE_NAME_DUPLICATES,
            Mode.NORMALIZE_NAME: Message.NORMALIZE_NAME,
            Mode.REMOVE_TEMPORARY: Message.REMOVE_TEMPORARY,
            Mode.REMOVE_EMPTY: Message.REMOVE_EMPTY,
            Mode.NORMALIZE_PERMISSIONS: Message.NORMALIZE_PERMISSIONS,
            Mode.MOVE_TO_MAIN: Message.MOVE_TO_MAIN,
        }

    # PUBLIC API

    def run(self) -> None:
        """Execute the selected organization operation."""
        self._actions[self._mode]()

    # FILE DISCOVERY

    def _iter_files(
        self,
        directories: Iterable[Path],
    ) -> Iterable[Path]:
        """Yield unique, resolved file paths from the given directories."""
        seen: set[Path] = set()

        for directory in directories:
            if not directory.is_dir():
                continue

            for item in directory.rglob("*"):
                try:
                    if not item.is_file():
                        continue

                    path = item.resolve()

                    if path not in seen:
                        seen.add(path)
                        yield path

                except OSError:
                    print("Could not inspect path: %s", item)

    def _find_files(
        self,
        directories: Iterable[Path],
        condition: Callable[[Path], bool],
    ) -> list[Path]:
        """Find files satisfying a condition."""
        selected_files: list[Path] = []

        for path in self._iter_files(directories):
            try:
                if condition(path):
                    selected_files.append(path)
            except OSError:
                print("Could not check file: %s", path)

        return selected_files

    def _group_files_by_name(
        self,
        directories: Iterable[Path],
    ) -> dict[str, list[Path]]:
        """Group files by their exact filename."""
        groups: dict[str, list[Path]] = defaultdict(list)

        for path in self._iter_files(directories):
            groups[path.name].append(path)

        return dict(groups)

    def _group_files_by_size(
        self,
        directories: Iterable[Path],
    ) -> dict[int, list[Path]]:
        """Group files by size."""
        groups: dict[int, list[Path]] = defaultdict(list)

        for path in self._iter_files(directories):
            try:
                groups[path.stat().st_size].append(path)
            except OSError:
                print("Could not get file size: %s", path)

        return dict(groups)

    def _find_name_duplicates(
        self,
        directories: Iterable[Path],
    ) -> list[list[Path]]:
        """Find groups of files with the same filename."""
        return [
            files
            for files in self._group_files_by_name(directories).values()
            if len(files) > 1
        ]

    def _find_content_duplicates(
        self,
        directories: Iterable[Path],
    ) -> list[list[Path]]:
        """Find groups of files with identical contents."""
        files_by_size = self._group_files_by_size(directories)
        files_by_hash: dict[tuple[int, str], list[Path]] = defaultdict(list)

        for size, files in files_by_size.items():
            if len(files) < 2:
                continue

            for path in files:
                try:
                    file_hash = self._hash_file(path)
                    files_by_hash[(size, file_hash)].append(path)
                except OSError:
                    print("Could not hash file: %s", path)

        return [files for files in files_by_hash.values() if len(files) > 1]

    def _find_unique_files(
        self,
        directories: Iterable[Path],
    ) -> list[Path]:
        """Find files whose filenames occur only once across
        the directories."""
        return [
            files[0]
            for files in self._group_files_by_name(directories).values()
            if len(files) == 1
        ]

    # FILE METADATA

    def _hash_file(self, path: Path) -> str:
        """Calculate a SHA-256 hash without loading the whole file
         into memory."""
        digest = hashlib.sha256()

        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def _find_oldest(paths: list[Path]) -> Path:
        """Select the file with the oldest modification time."""
        return min(paths, key=lambda path: path.stat().st_mtime)

    @staticmethod
    def _find_newest(paths: list[Path]) -> Path:
        """Select the file with the newest modification time."""
        return max(paths, key=lambda path: path.stat().st_mtime)

    # CONDITIONS

    def _is_temporary(self, path: Path) -> bool:
        return path.suffix in self._config.temporary

    @staticmethod
    def _is_empty(path: Path) -> bool:
        return path.stat().st_size == 0

    def _is_name_problematic(self, path: Path) -> bool:
        return any(
            symbol in path.name
            for symbol in self._config.problematic_symbols
        )   

    def _is_permission_set_unusual(self, path: Path) -> bool:
        return (path.stat().st_mode & 0o777) != self._config.permission_set

    # CONFIRMATION

    def _confirm(
        self,
        message: str,
        paths: list[Path],
    ) -> bool:
        """Ask for confirmation, unless running non-interactively."""
        if self._dry_run:
            return False

        if not self._is_interactive:
            return True

        print(f"\n{message}")
        for path in paths:
            print(f"  {path}")

        while True:
            answer = input("Proceed? [Y/N] ").strip().upper()

            if answer in {"Y", "N"}:
                return answer == "Y"

            print("Please enter Y or N.")

    # ACTION DISPATCH HELPERS

    def _remove_duplicates(
        self,
        find_files: Callable[[Iterable[Path]], list[list[Path]]],
        criterion: Callable[[list[Path]], Path],
    ) -> None:
        for paths in find_files(self._directories):
            try:
                keep = criterion(paths)
            except OSError:
                print("Could not select a file to keep")
                continue

            to_remove = [path for path in paths if path != keep]

            if not to_remove:
                continue

            if self._confirm(
                f"Keep {keep} and remove duplicate files?",
                [keep, *to_remove],
            ):
                self._remove_files(to_remove)

    def _do_action(
        self,
        condition: Callable[[Path], bool],
        operation: Callable[[Path], None],
        message: Message,
    ) -> None:
        files = self._find_files(self._directories, condition)

        for path in files:
            if self._confirm(f"{message.value} {path}?", [path]):
                try:
                    operation(path)
                except OSError:
                    print("Operation failed for file: %s", path)

    # ACTIONS

    def _remove_content_duplicates(self) -> None:
        self._remove_duplicates(
            self._find_content_duplicates,
            self._find_oldest,
        )

    def _remove_name_duplicates(self) -> None:
        self._remove_duplicates(
            self._find_name_duplicates,
            self._find_newest,
        )

    def _normalize_problematic_names(self) -> None:
        self._do_action(
            self._is_name_problematic,
            self.normalize_name,
            Message.NORMALIZE_NAME,
        )

    def _remove_temporary(self) -> None:
        self._do_action(
            self._is_temporary,
            self._remove,
            Message.REMOVE_TEMPORARY,
        )

    def _remove_empty(self) -> None:
        self._do_action(
            self._is_empty,
            self._remove,
            Message.REMOVE_EMPTY,
        )

    def _normalize_permissions(self) -> None:
        self._do_action(
            self._is_permission_set_unusual,
            self.normalize_permission_set,
            Message.NORMALIZE_PERMISSIONS,
        )

    def _move_to_main(self) -> None:
        self._main_dir.mkdir(parents=True, exist_ok=True)

        for path in self._find_unique_files(self._directories):
            # Files already directly inside the main directory need no move.
            if path.parent == self._main_dir:
                continue

            destination = self._main_dir / path.name

            if destination.exists():
                continue

            if self._confirm(
                f"{Message.MOVE_TO_MAIN.value} {path}?",
                [path],
            ):
                try:
                    self._move_file(path, destination)
                except OSError:
                    print("Could not move file: %s", path)

    # FILE OPERATIONS

    def _move_file(self, source: Path, destination: Path) -> None:
        """Move a file without intentionally overwriting an existing target."""
        if destination.exists():
            raise FileExistsError(f"Destination already exists: {destination}")

        old_source = source

        # shutil.move supports cross-filesystem moves.
        shutil.move(str(source), str(destination))

    def _remove_files(
        self,
        paths: list[Path],
        remain: Path | None = None,
    ) -> None:
        for path in paths:
            if path == remain:
                continue

            try:
                self._remove(path)
            except OSError:
                print("Could not remove file: %s", path)

    @staticmethod
    def _remove(path: Path) -> None:
        path.unlink(missing_ok=False)

    def normalize_permission_set(self, path: Path) -> None:
        path.chmod(self._config.permission_set)

    def normalize_name(self, path: Path) -> None:
        """Replace problematic characters in a filename while
        preserving its suffix."""
        stem = path.stem
        suffix = path.suffix

        for symbol in self._config.problematic_symbols:
            stem = stem.replace(
                symbol,
                self._config.substitute_symbol,
            )

        new_path = path.with_name(stem + suffix)

        if new_path == path:
            return

        if new_path.exists():
            raise FileExistsError(
                f"Cannot rename {path}: destination already exists: {new_path}"
            )

        path.rename(new_path)
