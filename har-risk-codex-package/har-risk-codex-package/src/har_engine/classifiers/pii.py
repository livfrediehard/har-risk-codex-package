from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from har_engine.models import DataElement, NormalizedEntry


def load_patterns(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _flatten_entry_text(entry: NormalizedEntry) -> list[tuple[str, str]]:
    parts: list[tuple[str, str]] = []
    for key, value in entry.query_params.items():
        parts.append((f"query:{key}", value))
    for key, value in entry.headers.items():
        parts.append((f"header:{key}", value))
    for key, value in entry.cookies.items():
        parts.append((f"cookie:{key}", value))
    if entry.body_text:
        parts.append(("body", entry.body_text))
    return parts


def extract_data_elements(entry: NormalizedEntry, patterns: dict[str, Any]) -> list[DataElement]:
    findings: list[DataElement] = []
    flattened = _flatten_entry_text(entry)

    for source, value in flattened:
        for match in _find_matches("email", value, patterns):
            findings.append(DataElement(kind="email", value=match, source=source))
        for match in _find_matches("phone", value, patterns):
            findings.append(DataElement(kind="phone", value=match, source=source))
        for match in _find_matches("account_id", value, patterns):
            findings.append(DataElement(kind="account_id", value=match, source=source))
        for match in _find_matches("user_id", value, patterns):
            findings.append(DataElement(kind="user_id", value=match, source=source))

        lowered = value.lower()
        for kw in patterns.get("health_terms", {}).get("keywords", []):
            if kw in lowered:
                findings.append(DataElement(kind="health_term", value=kw, source=source))

    for key in patterns.get("search_term_keys", {}).get("keys", []):
        if key in entry.query_params and entry.query_params[key]:
            findings.append(DataElement(kind="search_term", value=entry.query_params[key], source=f"query:{key}"))

    deduped: dict[tuple[str, str, str], DataElement] = {}
    for item in findings:
        deduped[(item.kind, item.value, item.source)] = item
    return list(deduped.values())


def _find_matches(name: str, value: str, patterns: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for regex in patterns.get(name, {}).get("regexes", []):
        out.extend(re.findall(regex, value))
    return [str(x) for x in out if str(x)]
