from __future__ import annotations

import json
from pathlib import Path

from har_engine.models import Finding


def write_json_report(findings: list[Finding], path: str | Path) -> None:
    payload = []
    for finding in findings:
        payload.append(
            {
                "finding_id": finding.finding_id,
                "rule_id": finding.rule_id,
                "theory_family": finding.theory_family,
                "confidence": finding.confidence,
                "summary": finding.summary,
                "caveat": finding.caveat,
                "vendor": finding.vendor,
                "endpoint": finding.endpoint,
                "observed_data_elements": finding.observed_data_elements,
                "evidence": [e.__dict__ for e in finding.evidence],
            }
        )
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
