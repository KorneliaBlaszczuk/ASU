import argparse
from pathlib import Path

from config import Config
from file_organizer import FileOrganizer, Mode

class CommandLineInterface:
    def __init__(
        self,
        parser: argparse.ArgumentParser,
        config: Config,
    ) -> None:
        self._parser = parser
        self._config = config

        self._setup()
        self._args = self._parser.parse_args()

    def _setup(self) -> None:
        """Configure the command-line arguments."""
        self._parser.add_argument(
            "directories",
            type=Path,
            nargs="+",
            metavar="DIRECTORY",
            help="Directories to process; the first is the main directory",
        )

        self._parser.add_argument(
            "-i",
            "--interactive",
            action="store_true",
            help="Ask for confirmation before each operation",
        )

        self._parser.add_argument(
            "--mode",
            type=Mode,
            choices=list(Mode),
            required=True,
            help="File organization operation to perform",
        )

        self._parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview planned operations without modifying files",
        )

        self._parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Enable debug-level logging",
        )

    def _parse_directories(
        self,
        directories: list[Path],
    ) -> list[Path]:
        """Validate, resolve, and deduplicate directory paths."""
        resolved_directories: list[Path] = []

        for directory in directories:
            try:
                resolved = directory.resolve(strict=True)
            except OSError as error:
                self._parser.error(
                    f"Cannot access directory '{directory}': {error}"
                )

            if not resolved.is_dir():
                self._parser.error(f"'{directory}' is not a directory")

            # Skip duplicate paths and directories already covered
            # by an existing parent directory.
            if any(
                resolved == parent or resolved.is_relative_to(parent)
                for parent in resolved_directories
            ):
                continue

            # Remove previously added directories nested inside this one.
            resolved_directories = [
                existing
                for existing in resolved_directories
                if not existing.is_relative_to(resolved)
            ]

            resolved_directories.append(resolved)

        if not resolved_directories:
            self._parser.error("At least one valid directory is required")

        return resolved_directories

    def _create_file_organizer(self) -> FileOrganizer:
        """Create the organizer using validated CLI arguments."""
        directories = self._parse_directories(self._args.directories)

        return FileOrganizer(
            config=self._config,
            main_dir=directories[0],
            directories=directories,
            mode=self._args.mode,
            is_interactive=self._args.interactive,
            dry_run=self._args.dry_run,
        )

    def run(self) -> None:
        """Execute the requested operation."""
        organizer = self._create_file_organizer()
        organizer.run()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Organize files by detecting duplicates and normalizing files."
    )

    config_path = Path.home() / ".clean_files"

    if config_path.exists():
        config = Config.from_file(config_path)
    else:
        config = Config()

    cli = CommandLineInterface(parser, config)
    cli.run()


if __name__ == "__main__":
    main()
