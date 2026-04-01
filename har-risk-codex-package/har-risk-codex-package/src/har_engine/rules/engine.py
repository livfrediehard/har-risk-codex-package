from __future__ import annotations

from typing import Any

from har_engine.models import DataElement, Evidence, Finding, NormalizedEntry, VendorMatch


def evaluate_rules(
    entry: NormalizedEntry,
    vendor: VendorMatch | None,
    elements: list[DataElement],
    context: set[str],
    rules: list[dict[str, Any]],
) -> list[Finding]:
    findings: list[Finding] = []
    element_kinds = {item.kind for item in elements}
    vendor_categories = set(vendor.categories) if vendor else set()
    matched_vendor_name = vendor.vendor if vendor else None

    for index, rule in enumerate(rules, start=1):
        when = rule.get("when", {})
        if not _matches_vendor_category(when, vendor_categories):
            continue
        if not _matches_data_elements(when, element_kinds):
            continue
        if not _matches_third_party(when, entry.is_third_party):
            continue
        if not _matches_url_contains(when, entry.url.lower()):
            continue
        if not _matches_context(when, context):
            continue

        relevant_elements = sorted(element_kinds.intersection(set(when.get("data_elements_any", element_kinds))))
        evidence = [
            Evidence(
                entry_id=entry.entry_id,
                url=entry.url,
                method=entry.method,
                vendor=matched_vendor_name,
                excerpt=_build_excerpt(elements),
                matched_on=_matched_on(when),
            )
        ]
        findings.append(
            Finding(
                finding_id=f"{entry.entry_id}-finding-{index}",
                rule_id=str(rule["id"]),
                theory_family=str(rule["family"]),
                confidence=float(rule.get("score", 0.5)),
                summary=str(rule["summary_template"]),
                caveat=str(rule.get("caveat", "Human review required.")),
                vendor=matched_vendor_name,
                endpoint=entry.url,
                observed_data_elements=relevant_elements,
                evidence=evidence,
            )
        )

    return findings


def _matches_vendor_category(when: dict[str, Any], vendor_categories: set[str]) -> bool:
    required = set(when.get("vendor_category_in", []))
    return not required or bool(required.intersection(vendor_categories))


def _matches_data_elements(when: dict[str, Any], element_kinds: set[str]) -> bool:
    required = set(when.get("data_elements_any", []))
    return not required or bool(required.intersection(element_kinds))


def _matches_third_party(when: dict[str, Any], is_third_party: bool) -> bool:
    if "third_party" not in when:
        return True
    return bool(when["third_party"]) is is_third_party


def _matches_url_contains(when: dict[str, Any], url: str) -> bool:
    required = [str(x).lower() for x in when.get("url_contains_any", [])]
    return not required or any(token in url for token in required)


def _matches_context(when: dict[str, Any], context: set[str]) -> bool:
    required = set(when.get("context_in", []))
    return not required or bool(required.intersection(context))


def _build_excerpt(elements: list[DataElement], limit: int = 3) -> str:
    preview = [f"{item.kind}:{item.value}" for item in elements[:limit]]
    return "; ".join(preview)


def _matched_on(when: dict[str, Any]) -> list[str]:
    matched: list[str] = []
    for key, value in when.items():
        matched.append(f"{key}={value}")
    return matched
