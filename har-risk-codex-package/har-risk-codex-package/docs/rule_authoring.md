# Rule Authoring

Rules are stored in `config/rules.yaml`.

## Required fields

- `id`
- `family`
- `summary_template`
- `when`
- `score`
- `caveat`

## Supported conditions

- `vendor_category_in`
- `data_elements_any`
- `third_party`
- `url_contains_any`
- `context_in`

## Guidance

- Keep rules narrow and explainable
- Prefer multiple targeted rules over one broad rule
- Every rule should have at least one test fixture or synthetic test case
- Never state that a rule proves a legal violation
