from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import parse_qsl, urlparse

from har_engine.models import NormalizedEntry


def _lower_dict(items: list[dict[str, str]]) -> dict[str, str]:
    return {item.get("name", "").lower(): item.get("value", "") for item in items if item.get("name")}


def parse_har(path: str | Path, first_party_hosts: set[str] | None = None) -> list[NormalizedEntry]:
    har = json.loads(Path(path).read_text(encoding="utf-8"))
    entries = har.get("log", {}).get("entries", [])
    normalized: list[NormalizedEntry] = []

    for idx, entry in enumerate(entries, start=1):
        request = entry.get("request", {})
        url = request.get("url", "")
        parsed = urlparse(url)
        headers = _lower_dict(request.get("headers", []))
        cookies = _lower_dict(request.get("cookies", []))
        body_text = request.get("postData", {}).get("text", "")
        body_json = None
        if body_text:
            try:
                body_json = json.loads(body_text)
            except json.JSONDecodeError:
                body_json = None
        query_params = dict(parse_qsl(parsed.query, keep_blank_values=True))
        host = parsed.netloc.lower()
        is_third_party = True
        if first_party_hosts and host in first_party_hosts:
            is_third_party = False

        normalized.append(
            NormalizedEntry(
                entry_id=f"entry-{idx}",
                started_datetime=entry.get("startedDateTime"),
                method=request.get("method", "GET"),
                url=url,
                host=host,
                path=parsed.path,
                query_params=query_params,
                headers=headers,
                cookies=cookies,
                body_text=body_text,
                body_json=body_json,
                is_third_party=is_third_party,
            )
        )

    return normalized
