---
name: validate-genai-spans
description: Use this to check that your LLM tracing actually emits complete, spec-compliant spans, so cost/latency/model dashboards downstream are not full of holes. Trigger on "are my traces complete", "validate my instrumentation", "my spans are missing fields", "lint my OTel GenAI spans", "test my tracing". Ships a runnable, tested validator you can drop into your instrumentation tests.
license: CC0-1.0
---

# Validate GenAI spans

Broken instrumentation fails silently: the app works, the dashboards just quietly miss the model, the tokens, or the cost. This skill ships a validator that asserts your spans carry the required OpenTelemetry `gen_ai.*` fields, so you catch gaps in a test instead of in a half-empty dashboard.

## Use the bundled script

[`scripts/validate_span.py`](scripts/validate_span.py) is pure Python, no install needed:

```python
from validate_span import validate_gen_ai_span, is_valid_gen_ai_span

problems = validate_gen_ai_span(span_attributes)          # [] means valid
validate_gen_ai_span(span_attributes, strict=True)        # also flag recommended fields
assert is_valid_gen_ai_span(span_attributes)              # use in an instrumentation test
```

It checks the required fields (`gen_ai.system`, `gen_ai.operation.name`, `gen_ai.request.model`) and, in strict mode, the recommended usage fields (`gen_ai.usage.input_tokens`/`output_tokens`, `gen_ai.response.model`) that cost analysis depends on.

## How to apply it

1. **Add an instrumentation test:** capture the span your app emits for a sample call (most SDKs have an in-memory span exporter for tests) and assert `is_valid_gen_ai_span(attrs)`.
2. **Run it in CI** so a change that breaks instrumentation fails the build, not production.
3. **Use strict mode** once basic spans pass, to push toward full cost/usage coverage.

Pairs with `instrument-llm-observability` (which gets the spans emitted in the first place).

## Validation

Run the tests: `pytest skills/validate-genai-spans/tests/`. They cover a valid span, each missing required field, empty/wrong-typed values, strict-mode recommended checks, and non-dict input.

## Anti-patterns

- Assuming "traces show up" means they are complete (missing token fields break cost dashboards).
- Only checking spans by eye once, instead of asserting them in CI.
- Ignoring the response model id (you cannot break cost down by served model without it).
