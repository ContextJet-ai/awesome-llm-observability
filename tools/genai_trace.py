"""
genai_trace - a minimal, vendor-neutral OpenTelemetry GenAI tracer.

Drop-in tracing for LLM calls using the OpenTelemetry GenAI semantic conventions
(``gen_ai.*``), so spans export to *any* OTel backend (Langfuse, Phoenix, Opik,
Datadog, Grafana, …). Includes an optional redaction hook so prompts/completions
can be masked before they leave the process - important for finance / regulated
data. No hard dependency: if OpenTelemetry isn't installed, it degrades to a no-op.

Original work by ContextJet.ai - CC0.

Usage
-----
    from genai_trace import trace_llm

    with trace_llm(system="openai", model="gpt-4o", messages=msgs) as span:
        resp = client.chat.completions.create(model="gpt-4o", messages=msgs)
        span.record_response(
            output_text=resp.choices[0].message.content,
            input_tokens=resp.usage.prompt_tokens,
            output_tokens=resp.usage.completion_tokens,
        )

    # redact PII before it hits the backend:
    with trace_llm("openai", "gpt-4o", msgs, redact=my_redactor) as span:
        ...
"""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Any, Callable, Iterator, Optional, Sequence

try:  # optional dependency
    from opentelemetry import trace as _otel_trace

    _TRACER = _otel_trace.get_tracer("genai_trace")
except Exception:  # pragma: no cover - OTel not installed
    _TRACER = None

Redactor = Callable[[str], str]


class _LLMSpan:
    """Thin wrapper that records GenAI attributes on an OTel span (or nothing)."""

    def __init__(self, span: Any, redact: Optional[Redactor]) -> None:
        self._span = span
        self._redact = redact or (lambda s: s)

    def set(self, key: str, value: Any) -> None:
        if self._span is not None and value is not None:
            self._span.set_attribute(key, value)

    def record_response(
        self,
        output_text: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        response_model: Optional[str] = None,
        finish_reason: Optional[str] = None,
    ) -> None:
        self.set("gen_ai.usage.input_tokens", input_tokens)
        self.set("gen_ai.usage.output_tokens", output_tokens)
        self.set("gen_ai.response.model", response_model)
        self.set("gen_ai.response.finish_reason", finish_reason)
        if output_text is not None:
            self.set("gen_ai.completion", self._redact(output_text))


@contextmanager
def trace_llm(
    system: str,
    model: str,
    messages: Optional[Sequence[dict]] = None,
    *,
    operation: str = "chat",
    temperature: Optional[float] = None,
    redact: Optional[Redactor] = None,
    capture_content: bool = True,
) -> Iterator[_LLMSpan]:
    """Trace one LLM call as a ``gen_ai.*`` span.

    :param system: provider, e.g. "openai", "anthropic".
    :param model: requested model id.
    :param messages: chat messages (recorded only if ``capture_content``).
    :param redact: optional ``str -> str`` applied to any captured content
        before it is set on the span (mask PII before export).
    :param capture_content: set False to record metadata only (no prompt/output).
    """
    if _TRACER is None:  # no-op fast path
        yield _LLMSpan(None, redact)
        return

    _redact = redact or (lambda s: s)
    with _TRACER.start_as_current_span(f"{operation} {model}") as raw:
        llm = _LLMSpan(raw, redact)
        llm.set("gen_ai.system", system)
        llm.set("gen_ai.operation.name", operation)
        llm.set("gen_ai.request.model", model)
        llm.set("gen_ai.request.temperature", temperature)
        if capture_content and messages:
            text = "\n".join(f"{m.get('role','')}: {m.get('content','')}" for m in messages)
            llm.set("gen_ai.prompt", _redact(text))
        started = time.time()
        try:
            yield llm
        except Exception as exc:  # record and re-raise - never swallow
            raw.record_exception(exc)
            raise
        finally:
            llm.set("gen_ai.latency_ms", int((time.time() - started) * 1000))


def mask_common_pii(text: str) -> str:
    """A conservative example redactor (emails, cards, SSN-like, long digit runs).

    For production / finance, use a real detector (Presidio, LLM Guard) plus a
    domain ruleset - this is a safe default, not a complete solution.
    """
    import re

    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "<email>", text)
    text = re.sub(r"\b(?:\d[ -]?){13,16}\b", "<card>", text)          # card-ish
    text = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "<ssn>", text)            # US SSN
    text = re.sub(r"\b\d{9,}\b", "<acct>", text)                       # long digit run
    return text


if __name__ == "__main__":  # tiny demo (runs with or without OTel installed)
    with trace_llm("openai", "gpt-4o", [{"role": "user", "content": "hi, my card is 4111 1111 1111 1111"}],
                   redact=mask_common_pii) as span:
        span.record_response(output_text="Your card ****", input_tokens=12, output_tokens=3)
    print("mask_common_pii demo:", mask_common_pii("email a@b.com card 4111111111111111 ssn 123-45-6789"))
