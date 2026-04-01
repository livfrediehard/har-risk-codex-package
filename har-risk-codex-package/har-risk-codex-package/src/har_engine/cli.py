from __future__ import annotations

import argparse
from pathlib import Path

from har_engine.classifiers.context import infer_context
from har_engine.classifiers.pii import extract_data_elements, load_patterns
from har_engine.classifiers.vendors import classify_vendor, load_vendors
from har_engine.parser import parse_har
from har_engine.reports.json_report import write_json_report
from har_engine.reports.markdown_report import write_markdown_report
from har_engine.rules.engine import evaluate_rules
from har_engine.rules.registry import load_rules


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan a HAR file for potential risk signals.")
    parser.add_argument("har_path")
    parser.add_argument("--first-party-host", action="append", default=[])
    parser.add_argument("--vendors", default="config/vendors.yaml")
    parser.add_argument("--patterns", default="config/patterns.yaml")
    parser.add_argument("--rules", default="config/rules.yaml")
    parser.add_argument("--json-out", default="out/findings.json")
    parser.add_argument("--md-out", default="out/summary.md")
    return parser


def main() -> None:
    args = build_arg_parser().parse_args()
    Path("out").mkdir(exist_ok=True)

    entries = parse_har(args.har_path, first_party_hosts=set(args.first_party_host))
    vendors = load_vendors(args.vendors)
    patterns = load_patterns(args.patterns)
    rules = load_rules(args.rules)

    all_findings = []
    for entry in entries:
        vendor = classify_vendor(entry, vendors)
        elements = extract_data_elements(entry, patterns)
        context = infer_context(entry, elements)
        all_findings.extend(evaluate_rules(entry, vendor, elements, context, rules))

    write_json_report(all_findings, args.json_out)
    write_markdown_report(all_findings, args.md_out)


if __name__ == "__main__":
    main()
