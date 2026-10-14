# File Organizer
## Author: Kornelia Błaszczuk

## Project Description

**File Organizer** is a Python application designed to help organize files in selected directories. It detects common file management issues, such as duplicate files, temporary files, empty files, problematic filenames, and incorrect file permissions.

The application allows users to analyze a main directory and additional directories, identify files that may require attention, and perform operations to help keep files organized.

## Features

The application supports the following features:

- **Duplicate content detection** – identifies files with identical contents and determines which file is the oldest.
- **Duplicate filename detection** – finds files with the same name.
- **Problematic filename detection** – identifies filenames containing characters considered problematic.
- **Temporary file detection** – finds files with extensions specified in the configuration.
- **Empty file detection** – identifies files with a size of zero bytes.
- **File permission checking** – detects files whose permissions differ from the configured value.
- **File organization** – supports moving files into a selected directory and performing available file management operations.
- **Configuration** – allows users to define default file permissions, problematic characters, a replacement character, and temporary file extensions.

## Requirements

- Python 3.10 or newer.
- Python standard library modules used by the project.
- `pytest`, if you want to run the automated tests.

## Configuration

The application settings are defined in `config.py`. The following parameters can be configured:

- `permission_set` – the default file permissions.
- `problematic_symbols` – a list of characters considered problematic in filenames.
- `substitute_symbol` – the character used to replace problematic characters.
- `temporary` – a list of extensions used to identify temporary files.

## Running the Application

Pass the directories to be analyzed using the command-line arguments supported by the application. To display the available arguments, run:

```bash
python3 cli.py --help
```

## Manual Testing

The application can be tested manually using sample directories containing files with different properties. This allows you to verify that each operating mode detects the expected issues and suggests appropriate actions.

### Test Directory Structure

For manual testing, use three directories:

- `tests/X` – the main directory.
- `tests/Y1` – the first additional directory.
- `tests/Y2` – the second additional directory.

The application analyzes the specified directories, using the first directory (`X`) as the main directory.

Make sure the test directories contain sample files representing the scenarios you want to verify. For example, include duplicate files, files with identical names but different contents, empty files, temporary files, filenames containing problematic characters, and files with different permissions.

### Available Operating Modes

Run the application using one of the following modes:

| Mode | Description |
|---|---|
| `duplicate-content` | Detects files with identical contents and identifies the oldest file. |
| `duplicate-name` | Detects files with the same filename. |
| `problematic-name` | Detects filenames containing configured problematic characters and suggests normalizing them. |
| `temporary` | Detects temporary files based on the extensions specified in the configuration. |
| `empty` | Detects files with a size of zero bytes. |
| `permissions` | Detects files whose permissions differ from the configured default. |
| `move` | Moves files from additional directories into the main directory, according to the implemented rules. |

### Manual Test Commands

Run the following commands from the project root directory.

**1. Detect files with identical contents**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode duplicate-content
```

Verify that files with identical contents are detected and that the oldest file can be identified.

**2. Detect files with duplicate names**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode duplicate-name
```

Verify that files with the same name are detected. When the implementation supports it, check that the application suggests keeping the newer file.

**3. Normalize problematic filenames**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode problematic-name
```

Verify that filenames containing configured problematic characters are identified and that replacement with the configured substitute character is suggested.

**4. Detect temporary files**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode temporary
```

Verify that files with extensions listed in the configuration, such as `.tmp` and `.temp`, are detected.

**5. Detect empty files**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode empty
```

Verify that files with a size of zero bytes are detected and that the application asks for confirmation before removing them when interactive mode is enabled.

**6. Normalize file permissions**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode permissions
```

Verify that files with permissions different from the configured value are identified and that the application suggests normalizing their permissions.

For example, the permission value `644` corresponds to `rw-r--r--` on Unix-like systems.

**7. Move files to the main directory**

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 -i --mode move
```

Verify that eligible files from the additional directories are moved into the main directory, according to the application's implementation.

### Interactive Mode and Dry Run

The `-i` or `--interactive` option enables confirmation prompts before operations are performed.

To preview planned operations without modifying files, use `--dry-run`. For example:

```bash
python3 cli.py tests/X tests/Y1 tests/Y2 --dry-run --mode problematic-name
```

The dry-run mode should report the planned actions without actually changing, deleting, or moving files.

### Configuration Checks

Before testing, verify that the configuration contains the expected values for:

- `permission_set` – the default file permission value, for example `0o644`.
- `problematic_symbols` – characters to be replaced in filenames.
- `substitute_symbol` – the replacement character, for example `_`.
- `temporary` – temporary file extensions, for example `.tmp` and `.temp`.

## Running Tests

To run the automated tests, execute:

```bash
python3 -m pytest -v
```

## Safety

Before performing operations such as deleting, replacing, or moving files, make sure that the correct directories have been selected. During development and testing, it is recommended to use test directories containing sample files to prevent accidental data loss.