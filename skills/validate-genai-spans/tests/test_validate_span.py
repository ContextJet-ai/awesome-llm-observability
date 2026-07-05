import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from validate_span import is_valid_gen_ai_span, validate_gen_ai_span  # noqa: E402

VALID = {
    "gen_ai.system": "openai",
    "gen_ai.operation.name": "chat",
    "gen_ai.request.model": "gpt-4o",
}


def test_valid_span_has_no_problems():
    assert validate_gen_ai_span(VALID) == []
    assert is_valid_gen_ai_span(VALID)


def test_missing_required_field_is_reported():
    span = {k: v for k, v in VALID.items() if k != "gen_ai.request.model"}
    problems = validate_gen_ai_span(span)
    assert "missing gen_ai.request.model" in problems


def test_empty_string_is_invalid():
    span = dict(VALID, **{"gen_ai.system": "  "})
    assert any("gen_ai.system" in p for p in validate_gen_ai_span(span))


def test_wrong_type_is_invalid():
    span = dict(VALID, **{"gen_ai.request.model": 123})
    assert any("gen_ai.request.model" in p for p in validate_gen_ai_span(span))


def test_strict_flags_missing_recommended():
    assert any("input_tokens" in p for p in validate_gen_ai_span(VALID, strict=True))
    # but non-strict treats a required-only span as valid
    assert validate_gen_ai_span(VALID) == []


def test_non_dict_input():
    assert validate_gen_ai_span("not a dict") == ["span attributes must be a dict"]
