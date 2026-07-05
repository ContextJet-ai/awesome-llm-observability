---
name: check-answer-consistency
description: Use this to get a cheap, reference-free signal that an LLM answer might be made up, by sampling the same prompt a few times and measuring agreement. Trigger on "is this answer reliable", "flag low-confidence answers", "cheap hallucination check", "confidence score without a ground truth", "self-consistency check". Ships a runnable, tested scorer you can put inline or on sampled traffic.
license: CC0-1.0
---

# Check answer consistency

A model that knows the answer repeats it across re-samples; a hallucinating model wanders. This skill ships a small consistency scorer that turns that idea into a number, with no reference answer required.

## Use the bundled script

[`scripts/self_consistency.py`](scripts/self_consistency.py) is pure Python, no install needed:

```python
from self_consistency import consistency_score, is_likely_hallucination

answers = [call_model(prompt, temperature=0.7) for _ in range(5)]
score = consistency_score(answers)              # 1.0 = all agree, ~0 = all differ
if is_likely_hallucination(answers, threshold=0.5):
    route_to_review()
```

Run it directly to see confident vs unsure examples: `python scripts/self_consistency.py`.

## How to apply it

1. **Sample with temperature > 0** (e.g. 5 samples). Consistency methods need diversity; a single deterministic answer tells you nothing.
2. **Score, then act:** flag/block/route-to-review when the score is below your threshold, or attach it to the trace as a reliability signal.
3. **Reserve it for high-stakes answers** if latency matters, sampling N times multiplies cost and latency by ~N.

This is a lightweight SelfCheckGPT-style check (normalized-string agreement). For meaning-level robustness (wording differs but the fact is the same), move to entailment clustering / semantic entropy, see the `detect-hallucinations` skill.

## Validation

Run the tests: `pytest skills/check-answer-consistency/tests/`. They confirm identical answers score 1.0 (ignoring case/punctuation/whitespace), all-different answers score low and flag, a 3-of-4 majority scores 0.75 and does not flag, and that fewer than two answers returns 0.0.

## Grounding

Consistency-based hallucination detection: SelfCheckGPT, Manakul et al. 2023 ([arXiv:2303.08896](https://arxiv.org/abs/2303.08896)). Meaning-level variant: semantic entropy, Farquhar et al., Nature 2024.

## Anti-patterns

- Running it at temperature 0 (no diversity, the score is meaningless).
- Treating a high consistency score as proof of correctness (a model can be confidently and consistently wrong).
- Sampling N times inline on every request when latency/cost matter (sample offline or only on risky answers).
