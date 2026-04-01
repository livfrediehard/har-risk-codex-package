from __future__ import annotations

from har_engine.models import DataElement, NormalizedEntry


def infer_context(entry: NormalizedEntry, elements: list[DataElement]) -> set[str]:
    context: set[str] = set()
    url_lower = entry.url.lower()
    if any(token in url_lower for token in ["login", "account", "signin", "portal"]):
        context.add("authenticated_or_account")
    if any(token in url_lower for token in ["search", "query"]):
        context.add("search_page")
    if any(el.kind in {"email", "phone"} for el in elements):
        context.add("form_like")
    if any(el.kind == "health_term" for el in elements):
        context.add("health_related")
    return context
