"""
self_consistency - a cheap reference-free hallucination signal.

Pure-Python, zero dependencies. Given several sampled answers to the same
prompt, it measures how much they agree. A model that knows the answer repeats
it across samples; a hallucinating model varies. Low consistency == treat the
answer as unreliable (flag, block, or route to review).

This is a lightweight SelfCheckGPT-style consistency check (normalized-string
agreement). For meaning-level robustness, cluster by entailment (semantic
entropy) instead - see the detect-hallucinations skill.

    from self_consistency import consistency_score, is_likely_hallucination

    answers = [call_model(prompt) for _ in range(5)]
    if is_likely_hallucination(answers):
        ...

CC0 - ContextJet.ai.
"""

from __future__ import annotations

import re
from collections import Counter


def _normalize(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", s.lower())).strip()


def consistency_score(answers) -> float:
    """Fraction of answers that match the most common (normalized) answer.

    1.0 == all identical, near 0 == all different. Returns 0.0 for <2 answers.
    """
    normed = [_normalize(a) for a in answers if a and a.strip()]
    if len(normed) < 2:
        return 0.0
    most_common = Counter(normed).most_common(1)[0][1]
    return most_common / len(normed)


def is_likely_hallucination(answers, threshold: float = 0.5) -> bool:
    """True when agreement across samples is below threshold."""
    return consistency_score(answers) < threshold


if __name__ == "__main__":
    confident = ["Paris", "Paris.", "paris"]
    unsure = ["Paris", "Lyon", "It's Berlin", "Madrid"]
    print("confident:", consistency_score(confident), "-> hallucination?",
          is_likely_hallucination(confident))
    print("unsure:", round(consistency_score(unsure), 2), "-> hallucination?",
          is_likely_hallucination(unsure))
