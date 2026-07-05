---
name: eval-driven-development
description: Use this to build or change an LLM feature the reliable way, by writing evals first and iterating against them, instead of tweaking prompts by vibes. Trigger on "how do I improve this prompt", "my changes keep breaking other things", "how do I know if this is better", "iterate on my agent", or any prompt/model/RAG change. This is test-driven development for LLMs.
license: CC0-1.0
---

# Eval-driven development (TDD for LLMs)

Changing a prompt and eyeballing one output is how LLM apps quietly regress. Eval-driven development flips it: define what "good" means as a small test set, then iterate until you pass it. It is the single habit that separates apps that get more reliable over time from ones that drift.

## The loop

1. **Write the eval first.** Before touching the prompt, collect 10 to 30 real input cases and define what a good output looks like (a reference answer, or a rubric for LLM-as-a-judge). Include the failure cases you already know about.
2. **Run it against the current version.** This is your baseline score. Now you have a number, not a feeling.
3. **Make one change.** New prompt, different model, changed retrieval. One at a time so you know what moved the score.
4. **Re-run the evals.** Kept the score or improved it? Keep the change. Dropped it? Revert. No debate.
5. **Add every new bug as a case.** When something breaks in production, capture that input as a new eval case before you fix it. The suite grows into a regression net.

## Wire it into the workflow

- Keep the eval set in the repo (versioned), next to the prompts it tests.
- Run it in **CI on every PR** that touches prompts, models, or retrieval, with thresholds that fail the build on a regression.
- Pull real cases from **production traces** (this is where observability feeds evals) so the suite reflects reality, not toy inputs.

See the `add-llm-evals` skill for framework setup (promptfoo, DeepEval, Ragas) and how to calibrate an LLM judge.

## Why it works for "vibe coding"

You can move fast and change prompts freely precisely *because* the eval set catches regressions. Without it, every change is a gamble and confidence drops over time. With it, you get the speed of vibes plus a safety net.

## Anti-patterns

- Tuning a prompt against a single example (you overfit to that one case and break others).
- A dataset written after the fact to match current behavior (it can never catch a regression).
- Changing three things at once, then not knowing which helped.
- Evals that live on someone's laptop instead of in CI (they rot immediately).
