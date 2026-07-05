---
name: build-eval-dataset
description: Use this to build a good evaluation dataset for an LLM app, the part everyone underestimates. Trigger on "make an eval set", "what should I test my LLM on", "I don't have test data for my prompt", "build a golden dataset", or before setting up evals. A great eval set beats a great metric; garbage-in means your evals lie to you.
license: CC0-1.0
---

# Build an eval dataset

Evals are only as good as the dataset behind them. A metric run over toy inputs gives you confident, wrong signal. This is how to build a set that actually reflects your app and catches real regressions.

## What makes a dataset good

- **Representative** of real usage, not made-up easy cases. The distribution should match production.
- **Covers the hard cases** you already know about: edge cases, ambiguous inputs, adversarial ones, the bug reports.
- **Has a clear success definition** per item: a reference answer, or a rubric a judge can apply consistently.
- **Small enough to iterate, big enough to trust.** Start at 20-50 items; grow toward a few hundred as the app matures. You do not need thousands to start.
- **Versioned** in the repo next to the code it tests.

## Where to get the data (best to worst)

1. **Real production traffic** (best). Pull real inputs from your traces (this is the payoff of having observability). Sample across the distribution, and deliberately include failures you saw.
2. **Beta / internal usage.** Dogfood inputs before you have prod traffic.
3. **Domain experts writing cases.** For regulated/specialized apps, have an expert write inputs + gold answers.
4. **LLM-generated cases** (last resort, use with care). Have a model generate candidate inputs, then a human curates. Never ship purely synthetic gold answers unverified.

## Build it in layers

1. **Smoke set (5-10):** obvious cases that must always pass. Run these on every change.
2. **Core set (20-100):** the representative distribution + known hard cases. Your main gate.
3. **Regression set (grows forever):** every production bug becomes a case here before it is fixed. This is how the app gets more reliable over time.

## Label quality

- For reference answers: have a human write/verify them. If using a rubric, make it concrete enough that two people would grade the same way.
- **Measure inter-annotator agreement** on a sample if multiple people label. Low agreement means the rubric is ambiguous, fix the rubric before trusting the scores.
- Stratify by category (topic, difficulty, language) so you can see *where* the app is weak, not just an average.

## Verify

- Run your current app over the set; the scores should feel right (known-good cases pass, known-bad fail).
- Introduce a deliberate regression; the set should catch it.
- The set lives in the repo and CI runs it (see `add-llm-evals` and `eval-driven-development`).

## Anti-patterns

- Ten cherry-picked easy examples that always pass (feels good, catches nothing).
- Purely synthetic data with unverified gold answers (you evaluate against the model's own mistakes).
- One flat list with no categories (you can't tell which part regressed).
- A frozen set that never grows (real inputs drift; add production cases continuously).

## Grounding

Eval-first practice: Hamel Husain, [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/). Multi-metric, stratified evaluation: HELM, Liang et al. ([arXiv:2211.09110](https://arxiv.org/abs/2211.09110)). Human-alignment of judges: Zheng et al. 2023 ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)).
