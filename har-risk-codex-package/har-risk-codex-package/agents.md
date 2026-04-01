# AGENTS.md

## Project purpose
This project analyzes HAR files and produces deterministic, evidence-first litigation risk signals for attorney review.

## Non-goals
- Do not output legal conclusions.
- Do not say "violation", "liable", or "illegal" as a final determination.
- Do not use an LLM to infer facts not present in the HAR.
- Do not silently change scoring weights or rule thresholds.

## Required behavior
- Prefer deterministic parsing and rules over heuristics when possible.
- Every finding must cite the exact HAR entry or normalized event that triggered it.
- Preserve reproducibility: same HAR + same config = same output.
- Add or update tests with every code change.
- Keep rules/config externalized in YAML or JSON when possible.
- Separate parser, extractor, scoring, and reporting layers.

## Output contract
Each finding must include:
- finding_id
- theory_family
- score
- confidence
- summary
- observed_elements
- missing_elements
- defenses_or_caveats
- evidence_refs

## Coding standards
- Python 3.11+
- typed code
- pytest required
- small focused modules
- avoid hidden global state
