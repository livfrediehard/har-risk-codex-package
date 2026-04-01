# Methodology

## Goal

This project detects technically observable patterns in HAR files and maps them to attorney-reviewable risk signals.

## Analysis stages

1. Parse HAR into normalized entries
2. Identify vendor and endpoint category
3. Extract data elements from requests
4. Infer coarse page or request context
5. Apply deterministic rules
6. Generate evidence-backed findings

## Confidence

Confidence is heuristic and bounded. It reflects observable support for a finding, not legal sufficiency.

## Key limitation patterns

- Encrypted or compressed application payloads that cannot be decoded
- Browser activity not captured in the HAR
- Missing authentication state context
- Ambiguous vendor domains that require manual review

## Review expectations

Every finding should be reviewed by a human before it is used in legal analysis or drafting.
