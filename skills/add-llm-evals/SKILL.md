---
name: add-llm-evals
description: Use this when adding evaluation to an LLM/agent app - measuring output quality (correctness, faithfulness, relevance, safety) rather than just watching traces. Trigger on "add evals", "test my prompt", "is my RAG accurate", "catch regressions", "score outputs", or setting up an eval suite in CI. Covers offline (CI) and online (production LLM-as-a-judge) evaluation.
license: CC0-1.0
---

# Add evaluations to an LLM app

Observability tells you *what happened*; evaluation tells you *whether it was good*. Add both an offline suite (runs in CI on a fixed dataset) and, optionally, online scoring (grades production traffic).

## Pick the eval type per metric

Two families, use both where relevant:

- **Reference-based** (you have a ground-truth answer): exact/fuzzy match, semantic similarity, ROUGE/BLEU - cheap, deterministic. Good for classification, extraction, closed QA.
- **Reference-free / LLM-as-a-judge** (open-ended output): a strong model scores the output against a rubric (faithfulness, relevance, coherence, safety). Scalable proxy for human judgment - but calibrate it (see caveats).

For RAG specifically, use the standard quartet: **faithfulness, answer relevance, context precision, context recall** (Ragas implements these).

## Build the offline suite (do this first)

1. **Curate a dataset** - 20-100 representative inputs with expected outputs or rubrics. Pull real cases from production traces (this is where observability + eval connect). Version it in the repo.
2. **Choose a framework** - `promptfoo` (YAML, great for prompt/RAG + CI), `DeepEval` (pytest-style, 40+ metrics), or `Ragas` (RAG metrics). Pick one; don't hand-roll.
3. **Define pass criteria** - per-metric thresholds (e.g. faithfulness ≥ 0.8). Fail the build if a threshold regresses.
4. **Wire into CI** - run on every PR that touches prompts/models/retrieval. Store scores so you can see trends, not just pass/fail.

See `references/frameworks.md` for a minimal promptfoo config and a DeepEval test example.

## Add online evaluation (optional, higher value)

Sample production traffic and score it with LLM-as-a-judge (most observability platforms - Langfuse, Phoenix, Opik, Braintrust - run these on live traces). Alert when a quality score drops. This catches drift the offline suite can't (real inputs shift over time).

## Calibrate LLM-as-a-judge (don't skip)

- **Anchor to humans**: label ~30 examples yourself, then check the judge agrees. Iterate the rubric until agreement is high.
- **Watch known biases**: position bias, verbosity bias, self-preference. Randomize order; keep rubrics concrete.
- **Use a strong judge model** and a low temperature; a weak judge produces noisy scores.

## Verify

- Offline suite runs green in CI and *fails* when you intentionally break a prompt.
- Scores are stored/trended, not just printed.
- (If online) a dashboard shows quality over time with an alert threshold.

## Anti-patterns

- Only "vibe-checking" outputs manually - doesn't scale, doesn't catch regressions.
- A dataset of toy inputs that don't resemble production.
- Trusting an uncalibrated LLM judge as ground truth.
- Evals that never fail the build (then they're decoration, not a gate).

## Research grounding

LLM-as-a-judge: Zheng et al. 2023 (MT-Bench/Chatbot Arena). Reference-free hallucination detection: SelfCheckGPT (Manakul et al. 2023). See this repo's README → *Research & Benchmarks*.
