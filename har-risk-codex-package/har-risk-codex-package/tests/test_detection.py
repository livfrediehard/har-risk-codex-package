from har_engine.classifiers.context import infer_context
from har_engine.classifiers.pii import extract_data_elements, load_patterns
from har_engine.classifiers.vendors import classify_vendor, load_vendors
from har_engine.models import NormalizedEntry
from har_engine.rules.engine import evaluate_rules
from har_engine.rules.registry import load_rules


def test_vendor_and_rule_match() -> None:
    entry = NormalizedEntry(
        entry_id="entry-1",
        started_datetime=None,
        method="POST",
        url="https://api.mixpanel.com/track?query=therapy",
        host="api.mixpanel.com",
        path="/track",
        query_params={"query": "therapy"},
        headers={"x-test": "person@example.com"},
        cookies={},
        body_text='{"email":"person@example.com"}',
        body_json={"email": "person@example.com"},
        is_third_party=True,
    )
    vendors = load_vendors("config/vendors.yaml")
    patterns = load_patterns("config/patterns.yaml")
    rules = load_rules("config/rules.yaml")

    vendor = classify_vendor(entry, vendors)
    assert vendor is not None
    assert vendor.vendor == "mixpanel"

    elements = extract_data_elements(entry, patterns)
    kinds = {e.kind for e in elements}
    assert "email" in kinds
    assert "search_term" in kinds
    assert "health_term" in kinds

    context = infer_context(entry, elements)
    findings = evaluate_rules(entry, vendor, elements, context, rules)
    assert findings
    assert any(f.rule_id == "THIRD_PARTY_ANALYTICS_EMAIL" for f in findings)
