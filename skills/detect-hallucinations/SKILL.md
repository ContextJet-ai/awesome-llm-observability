---
name: detect-hallucinations
description: Use this to detect when an LLM is making things up, so you can flag or block confident-but-wrong answers before users see them. Trigger on "detect hallucinations", "is the model making this up", "flag unreliable answers", "hallucination check", "confidence scoring for LLM output", or hardening a RAG/QA system. Pick a method that matches whether you have reference context or not.
license: CC0-1.0
---

# Detect LLM hallucinations

Hallucination detection scores how likely an answer is fabricated, so you can flag, block, or ask-for-review before it reaches a user. There is no single detector; pick by whether you have a ground-truth/context to check against.

## Choose a method by what you have

**You have retrieved context (RAG / QA):** check **faithfulness / groundedness** - is every claim in the answer supported by the retrieved context?
- NLI/entailment: run each answer sentence against the context with an entailment model; unsupported sentences are suspect.
- LLM-as-a-judge: ask a strong model "is this answer fully supported by the context? list any unsupported claims." Cheap, effective, calibrate it (see `add-llm-evals`).

**You have no reference (open-ended generation):** use **consistency across samples** - a model that knows the answer says the same thing across re-samples; a hallucinating model varies.
- **Self-consistency (SelfCheckGPT-style):** sample the answer N times; measure agreement. High disagreement = likely hallucination.
- **Semantic entropy:** cluster the N samples by *meaning* (bidirectional entailment), then compute entropy over the semantic clusters. High semantic entropy = the model is uncertain about the *fact*, not just the wording. This is the current state of the art for reference-free detection.

**Cheap signals to combine:** token log-probs / low confidence, and "I don't know"-style hedging. Weak alone, useful as features.

See [`references/methods.md`](references/methods.md) for how each method works, cost/latency tradeoffs, and which libraries implement them.

## Wire it into production

1. Run the detector **inline** on high-stakes answers (block/route to human on high hallucination score) or **sampled** on traffic (dashboard + alert).
2. Emit the score as a span attribute so hallucination rate is trackable over time (see `instrument-llm-observability`).
3. For RAG, log which claims were unsupported so failures are diagnosable (ties to `monitor-rag-quality`).

## Calibrate (do not skip)

Any detector has false positives/negatives. Label ~50 answers (hallucinated vs not) and tune the threshold to your tolerance - blocking flow favors recall (catch more), UX flow favors precision (fewer false blocks). Re-check after model changes.

## Anti-patterns

- Trusting a single LLM-as-judge call as ground truth without calibration.
- Using consistency methods on deterministic (temperature 0) output - you need sampling diversity for them to work.
- Checking only the final answer in RAG, never which retrieved claim was (un)supported.
- Treating low token-probability as proof of hallucination - it is a weak signal, not a verdict.

## Grounding

Self-consistency: SelfCheckGPT, Manakul et al. 2023 ([arXiv:2303.08896](https://arxiv.org/abs/2303.08896)). Semantic entropy: Farquhar et al., *Detecting hallucinations in large language models using semantic entropy*, Nature 2024 ([paper](https://www.nature.com/articles/s41586-024-07421-0)); cheaper variant, Semantic Entropy Probes ([arXiv:2406.15927](https://arxiv.org/abs/2406.15927)). LLM-as-a-judge: Zheng et al. 2023 ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)).
