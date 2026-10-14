from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class Config:
    permission_set: int = 0o644

    problematic_symbols: list[str] = field(
        default_factory=lambda: [
            ":",
            '"',
            ";",
            "*",
            "?",
            "$",
            "#",
            "'",
            "|",
            "\\",
        ]
    )

    substitute_symbol: str = "_"

    temporary: list[str] = field(
        default_factory=lambda: ["*.tmp", "*~", "*.temp"]
    )

    @classmethod
    def from_file(cls, filename: Path | str) -> "Config":
        """Load configuration from a JSON file."""
        filename = Path(filename)

        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return cls(
            permission_set=int(data.get("permission_set", "644"), 8),
            problematic_symbols=data.get(
                "problematic_symbols",
                cls().problematic_symbols,
            ),
            substitute_symbol=data.get("substitute_symbol", "_"),
            temporary=data.get(
                "temporary",
                cls().temporary,
            ),
        )
