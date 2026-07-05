"""
validate_span - lint an LLM span against the OpenTelemetry GenAI conventions.

Pure-Python, zero dependencies. Checks that a span's attributes carry the
required `gen_ai.*` fields (and sane types) so your traces are complete enough
to compute cost, latency, and per-model breakdowns downstream.

    from validate_span import validate_gen_ai_span

    problems = validate_gen_ai_span(span_attributes_dict)
    if problems:
        raise ValueError(problems)   # fail your instrumentation test

CC0 - ContextJet.ai. Based on the OTel GenAI semantic conventions.
"""

from __future__ import annotations

REQUIRED = {
    "gen_ai.system": str,            # e.g. "openai", "anthropic"
    "gen_ai.operation.name": str,    # e.g. "chat", "embeddings"
    "gen_ai.request.model": str,     # requested model id
}

# Recommended for cost/usage analysis; missing -> warnings, not errors.
RECOMMENDED = {
    "gen_ai.usage.input_tokens": int,
    "gen_ai.usage.output_tokens": int,
    "gen_ai.response.model": str,
}


def _check(attrs, spec):
    problems = []
    for key, typ in spec.items():
        if key not in attrs or attrs[key] is None:
            problems.append(f"missing {key}")
        elif not isinstance(attrs[key], typ) or (typ is str and not attrs[key].strip()):
            problems.append(f"{key} should be a non-empty {typ.__name__}, got {attrs[key]!r}")
    return problems


def validate_gen_ai_span(attrs, *, strict=False):
    """Return a list of problems with a span's attributes (empty == valid).

    Errors: missing/invalid required gen_ai.* fields.
    With strict=True, missing recommended fields are reported too.
    """
    if not isinstance(attrs, dict):
        return ["span attributes must be a dict"]
    problems = _check(attrs, REQUIRED)
    if strict:
        problems += [f"(recommended) {p}" for p in _check(attrs, RECOMMENDED)]
    return problems


def is_valid_gen_ai_span(attrs, **kw):
    return not validate_gen_ai_span(attrs, **kw)


if __name__ == "__main__":
    good = {
        "gen_ai.system": "openai",
        "gen_ai.operation.name": "chat",
        "gen_ai.request.model": "gpt-4o",
        "gen_ai.usage.input_tokens": 42,
        "gen_ai.usage.output_tokens": 7,
    }
    print("good span ->", validate_gen_ai_span(good, strict=True) or "valid")
    print("missing model ->", validate_gen_ai_span({"gen_ai.system": "openai", "gen_ai.operation.name": "chat"}))
