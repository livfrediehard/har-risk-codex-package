# HAR Risk Engine

An evidence-first HAR analysis engine that detects technically observable patterns associated with privacy and consumer-protection class action theories, then outputs reviewable findings rather than legal conclusions.

## What this repo does

- Parses HAR files into a normalized event schema
- Identifies vendors and endpoint categories
- Extracts data elements from URLs, headers, cookies, and bodies
- Applies deterministic rules to create findings
- Produces JSON and Markdown reports

## What this repo does not do

- It does not determine liability
- It does not replace attorney review
- It does not infer facts that are not observable in the HAR
- It does not make a final legal conclusion

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest
python -m har_engine.cli sample.har --json-out out/findings.json --md-out out/summary.md
```

## Example output finding

Each finding includes:

- finding_id
- rule_id
- theory_family
- confidence
- summary
- vendor
- endpoint
- observed_data_elements
- caveats
- evidence references

## Repository guide

- `src/har_engine/parser.py`: HAR parsing and normalization
- `src/har_engine/classifiers/`: vendor, PII, and context classification
- `src/har_engine/rules/`: rule loading and evaluation
- `src/har_engine/reports/`: JSON and Markdown report generation
- `config/vendors.yaml`: vendor signatures and categories
- `config/patterns.yaml`: regex and keyword extractors
- `config/rules.yaml`: theory mapping rules
- `.codex/`: prompts and project instructions for Codex
- `docs/`: methodology and rule-authoring docs

## Design principles

1. Deterministic first
2. Evidence attached to every finding
3. Config-driven legal theory mapping
4. Human review is required
5. Tests for every parser or rule change
