import argparse
import json
import os
import random
import string
from datetime import datetime
from pathlib import Path


class ContentGenerator:
    def __init__(self) -> None:
        self._unique_counter = 0

    def duplicate(self) -> str:
        return "Duplicated text."

    def random(self) -> str:
        return self._create_random_word()

    def _create_random_word(seld) -> str:
        return "".join(random.choices(string.ascii_lowercase, k=10))

    def empty(self) -> str:
        return ""

    def unique(self) -> str:
        self._unique_counter += 1
        return "UQ" + str(self._unique_counter) + self._create_random_word()


class TestCreator:
    """
    Adjusted to file structure described in `README.md`.
    """

    DEFAULT_PERMISSIONS = "644"

    def __init__(self, root: Path) -> None:
        self._root = root
        self._content = ContentGenerator()

    def create(self, config_file: str) -> None:
        tests_dir = self._create_dir("tests", self._root)
        data = self._read_from_json(config_file)
        self._create_file_structure(data, tests_dir)

    def _read_from_json(self, filename: str) -> dict:
        with open(filename) as f:
            data = json.load(f)
        return data

    def _create_file_structure(self, structure: dict, parent: Path) -> None:
        for name, specification in structure.items():
            if self._is_directory(name):
                new_dir = self._create_dir(name, parent)
                self._create_file_structure(specification, new_dir)
            else:
                self._create_file(name, parent, specification)

    def _is_directory(self, name: str) -> bool:
        # In current version directiories are named with uppercase
        return name.isupper()

    def _create_dir(self, name: str, parent: Path) -> Path:
        new_dir = parent / name
        new_dir.mkdir()
        return new_dir

    def _create_file(
        self,
        name: str,
        parent: Path,
        specification: dict,
    ) -> None:
        generators = {
            "duplicate": self._content.duplicate,
            "random": self._content.random,
            "empty": self._content.empty,
            "unique": self._content.unique,
        }
        new_file = parent / name
        new_file.touch()

        if not (content_generator := generators.get(specification.get("generator"))):
            raise ValueError("Missing 'generator' field in file specification")

        new_file.write_text(content_generator())

        if mtime := specification.get("mtime"):
            self._set_mtime(new_file, mtime)

        if not (permissions := specification.get("permissions")):
            permissions = TestCreator.DEFAULT_PERMISSIONS
        self._set_permissions(new_file, permissions)

    def _set_mtime(self, path: Path, mtime: str) -> None:
        dt = datetime.fromisoformat(mtime)
        timestamp = dt.timestamp()
        os.utime(path, (timestamp, timestamp))

    def _set_permissions(self, path: Path, permissions: str) -> None:
        os.chmod(path, int(permissions, 8))

    def _delete_dir(self, name: str) -> None:
        path = self._get_path(name)
        for child in path.iterdir():
            if child.is_file():
                child.unlink()
            else:
                self._delete_dir(child)
        path.rmdir()

    def _get_path(self, name: str) -> Path:
        return self._root.joinpath(name)


def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--create", action="store_true", help="Create test folder"
    )
    parser.add_argument(
        "-d", "--delete", action="store_true", help="Delete test folder"
    )
    parser.add_argument(
        "-r", "--recreate", action="store_true", help="Recreate test folder"
    )
    return parser


if __name__ == "__main__":
    creator = TestCreator(Path.cwd())
    parser = setup_parser()
    args = parser.parse_args()

    if args.create:
        creator.create("test_files.json")
    if args.delete:
        creator._delete_dir("tests")
    if args.recreate:
        creator._delete_dir("tests")
        creator.create("test_files.json")
