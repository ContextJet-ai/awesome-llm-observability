---
name: instrument-llm-observability
description: Use this when adding tracing/observability to an LLM or AI-agent application — capturing prompts, tool calls, token usage, latency, and cost per step. Trigger whenever someone wants to "add tracing", "instrument", "monitor", "see what my agent is doing", or debug an LLM app in production. Prefer vendor-neutral OpenTelemetry unless a specific platform is already in use.
license: CC0-1.0
---

# Instrument an LLM app for observability

Add production-grade tracing to an LLM/agent app so every run is inspectable: prompts, tool calls, retrievals, token usage, latency, and cost per span.

## Decide the approach first (2 questions)

1. **Is a backend already chosen?** (Langfuse, Arize Phoenix, Comet Opik, Datadog, Grafana…). If yes, use its SDK/auto-instrumentation. If no, default to **OpenTelemetry GenAI semantic conventions** so traces export to *any* OTel backend and you avoid lock-in.
2. **Lowest-friction path available?** If the app calls LLMs through a **gateway/proxy** (LiteLLM, Helicone, Portkey), you may get tracing + cost with *zero code* by changing the base URL. Check that before adding an SDK.

## Vendor-neutral path (recommended default): OpenTelemetry

Emit `gen_ai.*` spans via an OTel instrumentation library, then point at any collector.

- Use **OpenLLMetry** (`traceloop-sdk`) or **OpenInference** (Arize) — both emit OTel-compatible LLM spans.
- Minimal shape:
  1. Install the instrumentation lib + an OTLP exporter.
  2. Initialize once at startup (set service name + OTLP endpoint via `OTEL_EXPORTER_OTLP_ENDPOINT`).
  3. Auto-instrument the LLM SDK (OpenAI/Anthropic/etc.); wrap custom agent steps in manual spans (`gen_ai.operation.name`, tool spans).
- Result: spans carry model, prompt/completion, token counts, latency; cost is derived downstream.

See `references/opentelemetry.md` for the exact span attributes to set and a copy-paste init.

## Platform SDK path (if a backend is already picked)

Wrap the LLM client with the platform's tracer (e.g. `track_openai(...)`, `@observe`, an OTel exporter to that backend). Prefer their **auto-instrumentation** over hand-rolled spans; add manual spans only for custom tool/retrieval steps the SDK can't see.

## Instrument the right things (checklist)

- [ ] Each LLM call: model, input messages, output, `prompt_tokens`/`completion_tokens`, latency.
- [ ] Tool/function calls: name, args, result, error.
- [ ] Retrieval steps (RAG): query, retrieved doc IDs/scores.
- [ ] Agent/chain boundaries: one parent span per user request, child spans per step.
- [ ] Errors: record exceptions on the span (don't swallow them — a silent `except` that returns empty output hides the failure).
- [ ] Cost: derive from token counts × model price (most platforms do this for you).

## Verify

Run one representative request and confirm the trace tree shows the full chain (parent → LLM/tool/retrieval children) with tokens + latency populated. If spans are missing, the instrumentation isn't wrapping that code path — instrument it manually.

## Anti-patterns

- Logging raw prints instead of structured spans (no trace tree, no cost rollup).
- Instrumenting only the top-level call, missing tool/retrieval steps (the interesting failures hide there).
- Hard-coding a vendor SDK when OTel would keep you portable.
- Sending full prompts/PII to a third-party backend without redaction — mask sensitive fields first.

## Tool picker

Not sure which backend? See the sibling `choose-observability-stack` skill, or the curated list in this repo's README.
