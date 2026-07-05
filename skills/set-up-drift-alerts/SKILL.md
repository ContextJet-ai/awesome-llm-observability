---
name: set-up-drift-alerts
description: Use this to catch an LLM app silently getting worse in production - quality dropping, cost creeping up, inputs shifting away from what you tested. Trigger on "monitor my LLM in production", "alert me when quality drops", "detect drift", "my app got worse and I didn't notice", "set up monitoring/alerting for my AI app". Alert on the signals that actually move, not vanity metrics.
license: CC0-1.0
---

# Set up drift alerts

An LLM app that worked at launch degrades quietly: a model provider updates weights, users start asking different questions, a prompt change trades quality for cost. Drift alerting turns "we found out from an angry customer" into "we got paged when the metric moved."

## The four drifts worth alerting on

1. **Quality drift** - your online eval scores (faithfulness, relevance, hallucination rate) trend down. The one that matters most and the one people forget to watch. Requires online evals (see `add-llm-evals`).
2. **Cost drift** - tokens/request or spend/day creeps up (context bloat, a retry bug, a prompt that grew). Cheap to track, common, expensive to ignore.
3. **Latency / error drift** - p95 latency or error rate rises (provider slowdown, rate limits, a slow retrieval).
4. **Input drift** - production inputs move away from your eval set (new topics, new languages, longer inputs). Your evals stop being representative, so quality can drop *without* your quality metric catching it. Detect via input length/embedding-distribution shift.

## How to set it up

1. **Emit the signals** as span attributes / metrics (see `instrument-llm-observability`): per-request tokens, cost, latency, error, and online eval score.
2. **Baseline them** over a stable window (e.g. last 7-14 days) to know "normal."
3. **Alert on deviation, not absolute values** - page when a metric moves meaningfully vs its own baseline (e.g. quality score down >X%, cost/request up >Y%, error rate over threshold). Absolute thresholds age badly; relative-to-baseline survives growth.
4. **Route alerts** where the team actually looks (Slack/PagerDuty), with the trace/dashboard link attached so triage is one click.
5. **Sample, don't score everything** - online eval on a % of traffic is enough to see a trend and keeps cost sane.

Most observability platforms (Langfuse, Phoenix, Opik, Datadog LLM Obs) have built-in dashboards + alerting for these - wire the signals in and set the thresholds rather than building from scratch.

## Verify

- Deliberately regress a prompt in staging and confirm the quality alert fires.
- Confirm cost/latency/error alerts fire against a baseline, not a hard-coded number.
- Confirm the alert lands where the team sees it, with a link to the offending traces.

## Anti-patterns

- Alerting on cost/latency but never on *quality* (the app silently gets dumber while staying cheap and fast).
- Absolute thresholds that either page constantly or never (tie alerts to a rolling baseline).
- Scoring 100% of traffic with LLM-as-judge (expensive; sample instead).
- Alerts nobody sees, or with no link to the trace (they get muted, then ignored).

## Grounding

Drift/monitoring for ML has a long lineage (data & concept drift); the LLM-specific additions are online LLM-as-a-judge quality scoring (Zheng et al. 2023, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) and token/cost/latency telemetry via the [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/). Open-source drift/eval monitoring: [Evidently](https://github.com/evidentlyai/evidently).
