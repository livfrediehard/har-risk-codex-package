from __future__ import annotations

from pathlib import Path

from har_engine.models import Finding


def write_markdown_report(findings: list[Finding], path: str | Path) -> None:
    lines = ["# HAR Risk Findings", ""]
    if not findings:
        lines.append("No findings generated.")
    for finding in findings:
        lines.extend(
            [
                f"## {finding.rule_id}",
                f"- Theory family: {finding.theory_family}",
                f"- Confidence: {finding.confidence}",
                f"- Vendor: {finding.vendor or 'unknown'}",
                f"- Endpoint: {finding.endpoint}",
                f"- Summary: {finding.summary}",
                f"- Caveat: {finding.caveat}",
                f"- Data elements: {', '.join(finding.observed_data_elements) or 'none'}",
                "- Evidence:",
            ]
        )
        for evidence in finding.evidence:
            lines.append(
                f"  - {evidence.entry_id} | {evidence.method} | {evidence.url} | {evidence.excerpt}"
            )
        lines.append("")
    Path(path).write_text("\n".join(lines), encoding="utf-8")
