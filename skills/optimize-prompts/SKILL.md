---
name: optimize-prompts
description: Use this to improve a prompt systematically instead of hand-tweaking it by feel. Trigger on "optimize my prompt", "make this prompt better", "the prompt isn't working well", "auto-tune my prompt", "few-shot example selection", or when prompt quality has plateaued. Optimize against an eval set with a method, and let the numbers pick the winner.
license: CC0-1.0
---

# Optimize prompts (with a method, not vibes)

Hand-tuning a prompt and eyeballing one output tops out fast and quietly overfits to the last example you looked at. Systematic prompt optimization treats the prompt as something you search over, scored by an eval set.

## Prerequisite: you need an eval set

You cannot optimize what you cannot measure. Build an eval set first (`build-eval-dataset`) and wire up scoring (`add-llm-evals`). The optimization loop is: propose a prompt variant, score it on the eval set, keep the winner. Everything below is a smarter way to propose variants.

## The levers, cheapest first

1. **Instructions.** Clarify the task, add constraints, specify the output format. The highest-leverage and cheapest change.
2. **Few-shot examples.** Adding 2-5 good examples often beats a longer instruction. *Which* examples matters a lot; select them from your eval/production data, and measure (more examples is not always better, and they cost input tokens).
3. **Output structure.** Ask for structured output (JSON/enum) when you need reliability; add a short reasoning step before the answer when quality needs it.
4. **Decomposition.** Split one overloaded prompt into a small pipeline of focused steps (each independently evaluable).

## Automate the search (when hand-tuning plateaus)

Once you have an eval metric, use an optimizer instead of manual trial-and-error:

- **Auto instruction search (APE-style):** have an LLM propose many instruction candidates, score each on the eval set, keep the best.
- **Few-shot / demonstration optimization:** algorithmically select which examples to include (this is often a bigger win than instruction wording).
- **Frameworks:** [DSPy](https://github.com/stanfordnlp/dspy) compiles and optimizes prompt pipelines against a metric (bootstrap few-shot, MIPRO); [promptfoo](https://github.com/promptfoo/promptfoo) and several eval platforms support prompt experiments/comparison. Let the optimizer + metric pick, not your intuition.

## Guardrails on optimization

- **Hold out a test split** so you optimize on one set and validate on another, otherwise you overfit the prompt to your eval examples.
- **Change one lever at a time** when doing it by hand, so you know what moved the score.
- **Watch cost too:** a prompt that adds 6 few-shot examples for +2% quality may not be worth the token cost. Optimize quality *per token* where cost matters.
- **Re-optimize on model change:** a prompt tuned for one model can underperform on another.

## Verify

- The chosen prompt beats the baseline on a held-out split, not just the training examples.
- You have the scores to show it (a table, not "it feels better").
- Cost/latency did not quietly blow up for a small quality gain.

## Anti-patterns

- Tuning against a handful of examples with no held-out validation (overfitting).
- Piling on few-shot examples without measuring (token cost balloons, quality may not).
- Optimizing prompt wording when the real fix is retrieval or decomposition.
- Declaring a winner from one side-by-side output instead of an eval run.

## Grounding

Automatic instruction optimization: APE, Zhou et al. 2022 ([arXiv:2211.01910](https://arxiv.org/abs/2211.01910)). Programmatic prompt/pipeline optimization: DSPy, Khattab et al. ([arXiv:2310.03714](https://arxiv.org/abs/2310.03714)); MIPRO, Opsahl-Ong et al. ([arXiv:2406.11695](https://arxiv.org/abs/2406.11695)). All optimization is scored against an eval set (see `build-eval-dataset`).
