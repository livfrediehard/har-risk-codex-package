from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from har_engine.models import NormalizedEntry, VendorMatch


def load_vendors(path: str | Path) -> list[dict[str, Any]]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def classify_vendor(entry: NormalizedEntry, registry: list[dict[str, Any]]) -> VendorMatch | None:
    for record in registry:
        for domain in record.get("domains", []):
            if entry.host == domain or entry.host.endswith("." + domain):
                return VendorMatch(
                    vendor=str(record["vendor"]),
                    categories=list(record.get("categories", [])),
                    confidence=0.95 if entry.host == domain else 0.88,
                    matched_domain=domain,
                )
    return None
