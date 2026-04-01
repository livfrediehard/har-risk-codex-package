from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DataElement:
    kind: str
    value: str
    source: str


@dataclass(slots=True)
class VendorMatch:
    vendor: str
    categories: list[str]
    confidence: float
    matched_domain: str


@dataclass(slots=True)
class NormalizedEntry:
    entry_id: str
    started_datetime: str | None
    method: str
    url: str
    host: str
    path: str
    query_params: dict[str, str]
    headers: dict[str, str]
    cookies: dict[str, str]
    body_text: str
    body_json: dict[str, Any] | None
    is_third_party: bool


@dataclass(slots=True)
class Evidence:
    entry_id: str
    url: str
    method: str
    vendor: str | None
    excerpt: str
    matched_on: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Finding:
    finding_id: str
    rule_id: str
    theory_family: str
    confidence: float
    summary: str
    caveat: str
    vendor: str | None
    endpoint: str
    observed_data_elements: list[str]
    evidence: list[Evidence]
