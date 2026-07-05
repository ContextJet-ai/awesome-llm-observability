# Tools

Small, original, dependency-light utilities. CC0.

## `genai_trace.py`

A minimal, **vendor-neutral OpenTelemetry GenAI tracer** — trace any LLM call as a `gen_ai.*` span so it exports to any OTel backend (Langfuse, Phoenix, Opik, Datadog, …). Built-in **PII-redaction hook** so prompts/completions can be masked before they leave the process (finance/regulated use). Degrades to a **no-op** if OpenTelemetry isn't installed.

```python
from genai_trace import trace_llm, mask_common_pii

with trace_llm("openai", "gpt-4o", messages, redact=mask_common_pii) as span:
    resp = client.chat.completions.create(model="gpt-4o", messages=messages)
    span.record_response(
        output_text=resp.choices[0].message.content,
        input_tokens=resp.usage.prompt_tokens,
        output_tokens=resp.usage.completion_tokens,
    )
```

Run the demo: `python tools/genai_trace.py`
