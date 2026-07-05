---
name: set-up-ab-testing
description: Use this to test an LLM change (new prompt, new model, new retrieval) on real traffic before rolling it out to everyone. Trigger on "A/B test my prompt", "roll out a new model safely", "compare two prompts in production", "canary this change", "does this actually improve things for real users". Measure impact on real users, gated, before a full switch.
license: CC0-1.0
---

# A/B test LLM changes in production

Offline evals tell you a change *should* be better; a production experiment tells you it *is*, on real users and real traffic. For anything user-facing, run a controlled rollout instead of flipping the switch for everyone.

## When to use this vs offline evals

- **Offline evals** (`add-llm-evals`): fast, cheap, run in CI, catch regressions before deploy. Do these first, always.
- **A/B / online experiment:** use when the change is user-facing and the offline metric does not fully capture success (helpfulness, engagement, task completion, downstream conversion). Offline says "passes"; A/B says "users actually do better."

## Set it up

1. **Pick one variable.** New prompt OR new model OR new retrieval, not all at once, or you cannot attribute the result.
2. **Define the metric up front.** The primary success metric (task completion, thumbs-up rate, downstream action) plus guardrail metrics (cost, latency, error rate) that must not regress. Decide the win condition before you start.
3. **Split traffic** deterministically by user/session (a feature-flag / experiment tool: LaunchDarkly, GrowthBook, or your platform's built-in). Keep a user on one variant for consistency.
4. **Instrument both arms** with the same tracing + online evals + feedback capture (`instrument-llm-observability`, `collect-user-feedback`), tagged with the variant, so every metric is comparable across arms.
5. **Run until it is significant**, not until it looks good. Small differences need enough traffic; stopping early on a favorable blip is how you ship noise.

## Read the result honestly

- Compare the primary metric across arms **and** the guardrails (a +2% quality win that doubles cost or latency may not be worth it).
- Watch for novelty effects and segment differences (a change can help new users and hurt power users).
- If it is flat or worse, keep the control. "No worse and cheaper" is still a win.

## Safer rollout patterns

- **Canary:** send 5% to the new variant, watch the dashboards, ramp up if healthy. Good for risky changes.
- **Shadow / offline replay:** run the new variant on copied traffic without showing users, compare outputs. Zero user risk, no live metric though.

## Verify

- Traffic is actually split and each user stays on one arm.
- Both arms emit the same metrics, tagged by variant.
- The decision cites the primary metric + guardrails with enough sample size, not a first-hour blip.

## Anti-patterns

- Changing several things at once (you cannot attribute the effect).
- Peeking and stopping the moment it looks good (false positives).
- Measuring only quality, ignoring cost/latency guardrails.
- A/B testing something an offline eval would have caught for free (do offline first).

## Grounding

Online controlled experimentation methodology: Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments* (2020), and Kohavi et al., *Controlled experiments on the web* (2009). Applied here with LLM-specific metrics (online LLM-as-judge, Zheng et al. 2023, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) and user feedback (`collect-user-feedback`).
