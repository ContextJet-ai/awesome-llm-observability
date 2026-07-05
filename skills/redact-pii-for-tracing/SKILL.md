---
name: redact-pii-for-tracing
description: Use this when adding LLM observability to an app that handles sensitive data (finance, healthcare, PII) and you must NOT ship raw prompts/PII to a third-party tracing backend. Trigger on "redact traces", "PII in observability", "can we self-host tracing for compliance", "GDPR/HIPAA/SOC2 and LLM logging", or instrumenting a regulated app. Get observability without creating a data-leak.
license: CC0-1.0
---

# PII-safe / compliant LLM tracing

Observability captures prompts and completions - which, for a finance or healthcare app, means you may be shipping account numbers, SSNs, or PHI to a third-party SaaS. That's a compliance incident waiting to happen. This skill adds tracing **without** the leak.

## Decision order (most-compliant first)

1. **Self-host the backend.** For regulated data, prefer an OSS platform you host: [Langfuse](https://github.com/langfuse/langfuse) (MIT), [Arize Phoenix](https://github.com/Arize-ai/phoenix), [Comet Opik](https://github.com/comet-ml/opik), [Helicone](https://github.com/Helicone/helicone). Data never leaves your VPC.
2. **If using a SaaS backend, redact before export.** Strip/mask PII in the span-processor pipeline so raw values never leave the process.
3. **Or don't capture content at all.** Many SDKs let you record *metadata only* (tokens, latency, model, span structure) and omit prompt/completion text. You lose content-level debugging but keep full cost/perf/shape observability.

## Redaction pipeline (SaaS path)

Insert redaction **between span creation and export** so it always runs:

1. **Detect** PII with a real detector - [Microsoft Presidio](https://github.com/microsoft/presidio), [LLM Guard](https://github.com/protectai/llm-guard), or a domain ruleset (account/card/IBAN/SSN patterns for finance). Don't rely on ad-hoc regex alone.
2. **Transform** - mask (`****1234`), hash (for join-ability without exposure), or drop the field. Choose per field: costs need amounts, but not the account holder.
3. **Apply on the OTel span processor / SDK hook** (e.g. an `on_end` span processor, or the platform's masking callback) so no code path bypasses it.
4. **Redact both directions** - user input *and* model output (models echo PII back).

## Governance to layer on

- **Retention** - set TTLs on trace storage; regulated data shouldn't live forever.
- **Access control** - restrict who can read traces; content view separate from metrics view.
- **Audit** - log who accessed traces (observability of your observability).
- **Data-processing agreements** - if any content leaves your boundary, ensure the vendor DPA covers it.

## Verify

- Feed a request containing synthetic PII (fake SSN/card/account). Confirm the exported trace shows **masked** values, not raw ones - check the backend, not just local logs.
- Confirm redaction runs on the *export* path (disable the backend and it should still redact, proving it's not backend-side).
- Confirm output/echoed PII is also masked.

## Anti-patterns

- Turning on "log full prompts" in a finance app and pointing it at a SaaS backend. (Direct leak.)
- Redacting only inputs, not model outputs.
- Regex-only PII detection for high-stakes data (misses formats, context-dependent PII).
- Redacting client-side *after* the SDK already sent the span - redact **before** export.

_Authored by [ContextJet.ai](https://www.contextjetai.com) - we build secure, observable AI for finance and regulated industries._
