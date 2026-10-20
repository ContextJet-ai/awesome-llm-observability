import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from validate_span import is_valid_gen_ai_span, validate_gen_ai_span  # noqa: E402

VALID = {
    "gen_ai.provider.name": "openai",
    "gen_ai.operation.name": "chat",
    "gen_ai.request.model": "gpt-6.1-sol",
}


def test_valid_span_has_no_problems():
    assert validate_gen_ai_span(VALID) == []
    assert is_valid_gen_ai_span(VALID)


def test_missing_required_field_is_reported():
    span = {k: v for k, v in VALID.items() if k != "gen_ai.request.model"}
    problems = validate_gen_ai_span(span)
    assert "missing gen_ai.request.model" in problems


def test_empty_string_is_invalid():
    span = dict(VALID, **{"gen_ai.provider.name": "  "})
    assert any("gen_ai.provider.name" in p for p in validate_gen_ai_span(span))


def test_legacy_gen_ai_system_is_accepted_but_flagged():
    legacy = {k: v for k, v in VALID.items() if k != "gen_ai.provider.name"}
    legacy["gen_ai.system"] = "openai"
    problems = validate_gen_ai_span(legacy)
    assert problems == ["(deprecated) gen_ai.system is now gen_ai.provider.name"]
    assert not any("missing gen_ai.provider.name" in p for p in problems)


def test_wrong_type_is_invalid():
    span = dict(VALID, **{"gen_ai.request.model": 123})
    assert any("gen_ai.request.model" in p for p in validate_gen_ai_span(span))


def test_strict_flags_missing_recommended():
    assert any("input_tokens" in p for p in validate_gen_ai_span(VALID, strict=True))
    # but non-strict treats a required-only span as valid
    assert validate_gen_ai_span(VALID) == []


def test_non_dict_input():
    assert validate_gen_ai_span("not a dict") == ["span attributes must be a dict"]
