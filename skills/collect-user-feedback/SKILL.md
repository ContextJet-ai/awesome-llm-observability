---
name: collect-user-feedback
description: Use this to capture user feedback on LLM outputs (thumbs up/down, edits, corrections, implicit signals) and feed it back into observability and evals. Trigger on "add thumbs up/down", "collect feedback on responses", "how do I know if users like the answers", "improve from real usage", "human feedback loop". Turn real user signal into your best source of eval data.
license: CC0-1.0
---

# Collect user feedback

Your users are running the best eval you have, for free, every day. Capturing their reactions and attaching them to the trace turns production into a continuous source of labeled data. Most teams either skip this or collect it and never use it.

## Capture both explicit and implicit signals

**Explicit** (ask directly):
- Thumbs up/down on a response (the simplest, highest-signal control).
- A short reason on thumbs-down (dropdown: wrong / unhelpful / unsafe / other).
- Accept / edit / reject on a suggested output (great for copilot-style apps).

**Implicit** (infer from behavior, no extra UI):
- Did the user retry, rephrase, or immediately give up? (dissatisfaction).
- Did they copy/use the output, or continue the task? (satisfaction).
- Did a downstream action succeed (the code ran, the ticket resolved)?

Implicit signals are noisier but you get them on 100% of traffic instead of the small % who click thumbs.

## Wire it to the trace (this is the key step)

Attach every feedback signal to the **trace/span it is about** (by trace ID), with the user, timestamp, and the reason. Most observability platforms (Langfuse, Phoenix, Opik, LangSmith) have a feedback/scores API for exactly this. Without the trace link, feedback is a number with no context; with it, a thumbs-down is a fully debuggable example.

## Use it (do not just collect it)

1. **Monitor** feedback rate + thumbs-down rate over time; alert on spikes (see `set-up-drift-alerts`).
2. **Triage** thumbs-down traces into candidate test cases (see `trace-based-testing`) and your eval set (`build-eval-dataset`).
3. **Correlate** feedback with your automated eval scores to check your judge actually agrees with humans (calibration).
4. **Close the loop:** the corrections/edits users make are gold-standard reference outputs, use them.

## Handle it responsibly

- **PII / privacy:** feedback text can contain sensitive data, redact before it hits a third-party backend (`redact-pii-for-tracing`).
- **Bias:** thumbs are a biased sample (angry and delighted users click most). Do not treat thumbs-up rate as ground-truth quality; use it as signal, validate with evals.

## Verify

- A thumbs-down in the UI shows up attached to the right trace in your backend.
- Thumbs-down traces are being triaged into the eval/regression set, not just counted.
- A dashboard shows feedback trends with an alert on a drop.

## Anti-patterns

- Collecting feedback that never links to a trace (a number you cannot act on).
- Collecting it and never feeding it back into evals or fixes.
- Treating thumbs-up rate as objective quality (selection bias).
- Logging raw feedback with PII to a SaaS backend without redaction.

## Grounding

Human feedback as the signal for LLM quality underpins RLHF and preference modeling (Ouyang et al., InstructGPT, [arXiv:2203.02155](https://arxiv.org/abs/2203.02155)) and human-aligned evaluation (Zheng et al. 2023, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)). Here it feeds the lighter-weight eval + observability loop (`trace-based-testing`, `build-eval-dataset`).
