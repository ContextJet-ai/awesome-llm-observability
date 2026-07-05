import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from self_consistency import consistency_score, is_likely_hallucination  # noqa: E402


def test_identical_answers_score_one():
    # Same answer with punctuation/case/space differences still counts as agreement.
    assert consistency_score(["Paris", "paris.", " PARIS "]) == 1.0
    assert not is_likely_hallucination(["Paris", "paris.", "PARIS"])


def test_all_different_answers_score_low():
    score = consistency_score(["Paris", "Lyon", "Berlin", "Madrid"])
    assert score == 0.25
    assert is_likely_hallucination(["Paris", "Lyon", "Berlin", "Madrid"])


def test_majority_agreement():
    # 3 of 4 agree -> 0.75, above the default 0.5 threshold.
    score = consistency_score(["yes", "yes", "yes", "no"])
    assert score == 0.75
    assert not is_likely_hallucination(["yes", "yes", "yes", "no"])


def test_too_few_answers_returns_zero():
    assert consistency_score(["only one"]) == 0.0
    assert consistency_score([]) == 0.0


def test_blank_answers_ignored():
    assert consistency_score(["Paris", "  ", "Paris"]) == 1.0
