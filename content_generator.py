
import random
import string


class ContentGenerator:
    """Generates content for File Organizer test files."""

    def __init__(self) -> None:
        self._unique_counter = 0

    def duplicate(self) -> str:
        """Return identical content for duplicate-file tests."""
        return "Duplicated text."

    def random(self) -> str:
        """Return random content."""
        return self._create_random_word()

    def empty(self) -> str:
        """Return empty content."""
        return ""

    def unique(self) -> str:
        """Return content that differs between calls."""
        self._unique_counter += 1
        return f"UQ{self._unique_counter}{self._create_random_word()}"

    @staticmethod
    def _create_random_word() -> str:
        return "".join(random.choices(string.ascii_lowercase, k=10))
