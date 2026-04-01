from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_rules(path: str | Path) -> list[dict[str, Any]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))
