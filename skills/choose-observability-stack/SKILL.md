---
name: choose-observability-stack
description: Use this to recommend an LLM observability / evaluation tool or stack for a specific situation. Trigger on "which observability tool should I use", "compare Langfuse vs Phoenix vs LangSmith", "what's the best LLM monitoring for us", or picking an eval/tracing/gateway tool given constraints (self-hosting, budget, compliance, existing stack). Ask about constraints, then recommend from the curated list — don't just name the most popular tool.
license: CC0-1.0
---

# Choose an LLM observability stack

There's no single best tool — the right choice depends on constraints. Gather them, then map to a recommendation. Base recommendations on this repo's curated list (verified tools + licenses), not on hype.

## Ask these constraints first

1. **Deployment**: SaaS OK, or must self-host / on-prem (data residency, regulated industry)?
2. **Primary need**: tracing/cost, *evaluation* (quality testing), or both? Prompt management too?
3. **Existing stack**: already on Datadog/Grafana/OTel? On LangChain? Using a gateway?
4. **Budget/licensing**: need a permissive OSS license (MIT/Apache), or is a commercial tier fine? (Note AGPL/Elastic-license implications for embedding.)
5. **Code-change tolerance**: want zero-code (proxy) or fine to add an SDK?
6. **Team**: engineers, or also non-technical PMs who need a UI?

## Map constraints → recommendation

- **Must self-host, permissive license, want everything** → **Langfuse** (MIT core: tracing + evals + prompts) or **Comet Opik** (Apache-2.0). For eval-heavy local work, **Arize Phoenix**.
- **Zero code changes, just want cost + logs** → a **gateway/proxy**: **Helicone** (change base URL), **LiteLLM** or **Portkey** (also routing).
- **Already on OTel / want vendor-neutral, future-proof** → emit **OpenTelemetry GenAI semantic conventions** via **OpenLLMetry** or **OpenInference**; export to your existing backend.
- **Deep in the LangChain ecosystem** → **LangSmith** (tightest integration; SDK OSS, backend commercial).
- **Enterprise APM already (Datadog/New Relic)** → use their **LLM Observability** product to keep one pane of glass.
- **Primary need is *evaluation*/testing, not dashboards** → **promptfoo** (prompt/RAG + CI), **DeepEval** (pytest-style), **Ragas** (RAG metrics). Pair with a tracing tool for online scoring.
- **Regulated / finance / must audit + guardrail** → self-hosted tracing (Langfuse/Phoenix) + **guardrails** (Guardrails AI, LLM Guard for PII/prompt-injection) + strict prompt/PII redaction.

## Common production shape

A gateway (cost + routing) **+** an evaluation framework (quality) **+** an OTel-native tracing backbone. This keeps cost, quality, and traces decoupled and swappable.

## Deliver the recommendation

- Name a **primary** tool + a **runner-up**, each with a one-line *why it fits these constraints*.
- Call out license/self-hosting implications explicitly (especially AGPL / Elastic-license for embedding, and SaaS data-egress for regulated data).
- Link to the tool's row in this repo's README so they can compare stars/license.

## Anti-pattern

Recommending the highest-star tool by default. LiteLLM has the most stars but is a *gateway* — it's the wrong answer for someone who asked for an *evaluation* framework. Match the tool category to the stated need.
