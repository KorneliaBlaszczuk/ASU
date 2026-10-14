
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from test_creator import TestCreator


if __name__ == "__main__":
    data_root = PROJECT_ROOT / "tests"
    data_root.mkdir(parents=True, exist_ok=True)

    config_file = data_root / "test_files.json"

    creator = TestCreator(data_root)
    creator.create(str(config_file))

    print(f"Test data created in: {data_root}")
    print(f"Main directory: {data_root / 'X'}")
    print(f"Additional directory: {data_root / 'Y1'}")
    print(f"Additional directory: {data_root / 'Y2'}")
