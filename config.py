from dataclasses import dataclass


@dataclass
class Config:
    permission_set = 0o644  # "rw-r--r--"
    problematic_symbols = [
        ":",
        '"',
        ".",
        ";",
        "*",
        "?",
        "$",
        "#",
        "'",
        "|",
        "\\",
    ]
    substitute_symbol = "_"
    temporary = [".temp"]
