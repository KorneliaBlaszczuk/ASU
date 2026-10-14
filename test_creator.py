
import json
import os
from datetime import datetime
from pathlib import Path

from content_generator import ContentGenerator


class TestCreator:
    DEFAULT_PERMISSIONS = "644"

    def __init__(self, root: Path) -> None:
        self._root = root
        self._content = ContentGenerator()

    def create(self, config_file: str) -> None:
        with open(config_file, encoding="utf-8") as file:
            structure = json.load(file)

        self._create_file_structure(structure, self._root)

    def _create_file_structure(self, structure: dict, parent: Path) -> None:
        for name, specification in structure.items():
            path = parent / name

            if isinstance(specification, dict) and "generator" not in specification:
                path.mkdir(parents=True, exist_ok=True)
                self._create_file_structure(specification, path)
            else:
                self._create_file(name, parent, specification)

    def _create_file(self, name: str, parent: Path, specification: dict) -> None:
        generators = {
            "duplicate": self._content.duplicate,
            "random": self._content.random,
            "empty": self._content.empty,
            "unique": self._content.unique,
        }

        generator_name = specification.get("generator")
        if generator_name not in generators:
            raise ValueError(f"Unknown generator: {generator_name}")

        path = parent / name
        path.write_text(generators[generator_name](), encoding="utf-8")

        if mtime := specification.get("mtime"):
            timestamp = datetime.fromisoformat(mtime).timestamp()
            os.utime(path, (timestamp, timestamp))

        permissions = specification.get("permissions", self.DEFAULT_PERMISSIONS)
        os.chmod(path, int(permissions, 8))
