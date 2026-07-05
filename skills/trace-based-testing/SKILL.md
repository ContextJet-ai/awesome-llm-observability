---
name: trace-based-testing
description: Use this to turn real production traces into a regression test suite, so bugs you saw once never come back. Trigger on "turn traces into tests", "capture this bug as a test", "build tests from production data", "my eval set is out of date", or after debugging a production incident. This is the loop that connects observability to evaluation.
license: CC0-1.0
---

# Trace-based testing

Observability records what really happened; evaluation checks whether it was good. Trace-based testing is the bridge: promote real production traces into repeatable test cases. Done consistently, your eval set stays representative on its own and every incident makes the app more robust.

## The loop

1. **A trace shows a problem** (a bad answer, a hallucination, a tool misfire, a slow/expensive run). You find it via alerts (`set-up-drift-alerts`) or debugging (`debug-agent-from-traces`).
2. **Capture the trace's input as a test case.** The input, the retrieved context, the expected-correct output (write the gold answer, or a rubric). Redact PII first (`redact-pii-for-tracing`).
3. **Add it to the eval set** (`build-eval-dataset`), tagged with the incident so you know why it exists.
4. **Fix the bug**, confirm the new case passes.
5. **CI runs it forever** (`eval-driven-development`) so the bug cannot silently return.

## Make it systematic, not manual

- **Sample continuously**, not just on incidents. Periodically pull a stratified sample of production traces (by topic, difficulty, outcome) and fold them into the eval set so it tracks the real input distribution as it drifts.
- **Auto-flag candidates**: traces with low online-eval scores, thumbs-down feedback, errors, or high cost are prime candidates to promote to test cases.
- **Keep a "replay" path**: re-run a captured input through the current app and diff against the recorded/expected output. Most eval frameworks (promptfoo, DeepEval) support running a dataset of captured cases directly.

## What to capture per trace

Input, retrieved context / tool results, the model + prompt version at the time, the actual output, and the *expected* output (your judgment of what good looks like). The first four come from the trace; the last one is the human/label step.

## Verify

- A real production failure is now a test case that fails on the old code and passes on the fixed code.
- The eval set grows over time and reflects current production inputs.
- Feedback (thumbs-down) and low-score traces get triaged into candidate test cases regularly.

## Anti-patterns

- Fixing a production bug without capturing it as a test (you will debug it again).
- An eval set frozen at launch while production inputs drift away from it.
- Replaying raw traces with PII into a test suite or third-party judge (redact first).
- Capturing the input but not a clear expected output (then the "test" cannot pass or fail meaningfully).

## Grounding

This operationalizes the observability-to-eval feedback loop: online quality signals (LLM-as-a-judge, Zheng et al. 2023, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) and human feedback surface weak traces; those become evaluation cases (see [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/)). Ties together `debug-agent-from-traces`, `build-eval-dataset`, and `eval-driven-development`.
