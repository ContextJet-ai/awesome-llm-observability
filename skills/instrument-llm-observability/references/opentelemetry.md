# OpenTelemetry GenAI - span attributes & init

## Key `gen_ai.*` semantic-convention attributes

Set these on LLM spans so any OTel backend understands them:

| Attribute | Example | Meaning |
|---|---|---|
| `gen_ai.provider.name` | `openai`, `anthropic`, `aws.bedrock` | Provider (was `gen_ai.system` before the 2025 rename) |
| `gen_ai.operation.name` | `chat`, `embeddings` | Operation |
| `gen_ai.request.model` | `gpt-4o` | Requested model |
| `gen_ai.response.model` | `gpt-4o-2024-…` | Actual model |
| `gen_ai.usage.input_tokens` | `812` | Prompt tokens |
| `gen_ai.usage.output_tokens` | `126` | Completion tokens |
| `gen_ai.request.temperature` | `0.2` | Sampling params |

Prompts/completions are opt-in span attributes (`gen_ai.input.messages` / `gen_ai.output.messages`, JSON arrays of `{role, parts}`); the older `gen_ai.content.*` events are deprecated. Gate content capture behind a flag and redact PII before enabling it in production.

## Minimal init (OpenLLMetry / Traceloop)

```python
from traceloop.sdk import Traceloop
# OTEL_EXPORTER_OTLP_ENDPOINT points at your collector/backend
Traceloop.init(app_name="my-agent", disable_batch=False)
# LLM SDK calls (OpenAI/Anthropic/…) are now auto-instrumented as gen_ai.* spans.
```

## Wrap a custom step (manual span)

```python
from opentelemetry import trace
tracer = trace.get_tracer("my-agent")
with tracer.start_as_current_span("retrieve") as span:
    span.set_attribute("retrieval.query", query)
    docs = retriever.search(query)
    span.set_attribute("retrieval.doc_count", len(docs))
```

Reference: OpenTelemetry GenAI semantic conventions (moved out of the main semconv repo in 2026) - https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md
