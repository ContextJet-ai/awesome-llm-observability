---
name: add-llm-guardrails
description: Use this to add safety and security guardrails to an LLM/agent app - blocking prompt injection, PII leakage, jailbreaks, toxic output, off-topic responses, or invalid structured output. Trigger on "add guardrails", "prevent prompt injection", "stop PII leaks", "validate the model's output", "make this safe for production", especially for regulated/finance/enterprise use.
license: CC0-1.0
---

# Add guardrails to an LLM app

Guardrails are validation layers on the **input** (before the model) and **output** (before the user/downstream). They're mandatory for regulated and enterprise deployments. Treat them as tested code, and *observe* them (a guardrail that fires silently is useless).

## Two layers, distinct jobs

**Input guardrails** (run before the LLM):
- **Prompt-injection / jailbreak detection** - reject or sanitize inputs trying to override instructions.
- **PII detection** - flag/redact sensitive data before it reaches a third-party model (see the `redact-pii-for-tracing` skill for the tracing side).
- **Topic / policy** - reject off-scope requests.

**Output guardrails** (run before returning):
- **Structured-output validation** - enforce the schema (JSON/enum/type); repair or reject on failure.
- **Toxicity / safety** - block harmful content.
- **Groundedness / hallucination** - check the answer is supported by the retrieved context (for RAG).
- **Sensitive-data egress** - ensure the response isn't leaking secrets/PII.

## Implementation shape

1. **Pick a library** - [Guardrails AI](https://github.com/guardrails-ai/guardrails) (validators + structured output), [LLM Guard](https://github.com/protectai/llm-guard) (PII, injection, toxicity), or [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) (programmable rails). Don't hand-roll regexes for security.
2. **Wrap input** → validate/sanitize → call model → **wrap output** → validate → return or repair.
3. **Decide the failure mode per guardrail**: block (hard fail), redact (transform), or flag-and-log (soft). Regulated flows usually block; UX flows often redact.
4. **Fail closed for security-critical checks** - if the guardrail errors, treat as a failure, not a pass.

## Observe your guardrails (critical)

Emit a span/event every time a guardrail **fires** (which one, input hash, action taken). Without this you can't tell if injection attempts are rising, if PII redaction is over/under-triggering, or if a guardrail silently broke. Dashboard: guardrail-trigger rate over time + false-positive spot-checks.

## Verify

- Red-team it: feed known injection strings, PII samples, and malformed-output cases; confirm each is caught.
- Confirm guardrail firings show up in traces.
- Confirm the *failure mode* is right (block vs redact) for each check.

## Anti-patterns

- Output validation only, no input guardrails (injection walks right in).
- Guardrails that **fail open** on error (a crashing PII check that lets data through).
- Silent guardrails with no telemetry - you're blind to attacks and to your own false-positive rate.
- Regex-only "security" - brittle against adversarial inputs.
