
from pathlib import Path
from types import SimpleNamespace

from file_organizer import FileOrganizer


def make_organizer(temporary=None, problematic_symbols=None):
    """Create an organizer for testing its helper methods."""
    organizer = object.__new__(FileOrganizer)
    organizer._config = SimpleNamespace(
        temporary=temporary or [".tmp", ".temp"],
        problematic_symbols=problematic_symbols or [":", "*", "?"],
    )
    return organizer


def test_tmp_file_is_temporary():
    organizer = make_organizer()

    assert organizer._is_temporary(Path("example.tmp")) is True


def test_temp_file_is_temporary():
    organizer = make_organizer()

    assert organizer._is_temporary(Path("example.temp")) is True


def test_regular_file_is_not_temporary():
    organizer = make_organizer()

    assert organizer._is_temporary(Path("document.txt")) is False


def test_temporary_extension_is_read_from_config():
    organizer = make_organizer(temporary=[".bak"])

    assert organizer._is_temporary(Path("backup.bak")) is True
    assert organizer._is_temporary(Path("backup.tmp")) is False


def test_problematic_filename_is_detected():
    organizer = make_organizer()

    assert organizer._is_name_problematic(Path("report?.txt")) is True


def test_normal_filename_is_not_problematic():
    organizer = make_organizer()

    assert organizer._is_name_problematic(Path("report.txt")) is False
