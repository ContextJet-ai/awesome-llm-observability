<div align="center">

# Awesome LLM Observability [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

**A curated list of tools, frameworks, standards, and research for tracing, evaluating, and monitoring LLM & AI-agent applications in production.**

_...plus original, ready-to-use [Agent Skills](#-skills-batteries-included) to put them to work._

[![Awesome](https://img.shields.io/badge/Awesome-list-blueviolet)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: CC0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![Maintained by ContextJet.ai](https://img.shields.io/badge/curated_by-ContextJet.ai-1f6feb)](https://www.contextjetai.com)

</div>

> [!NOTE]
> LLM observability is one of the fastest-growing layers of the AI stack — an estimated **~$2.7B market in 2026, projected to ~$9.3B by 2030 (≈36% CAGR)**. Gartner projects LLM-observability investment will rise from ~15% of GenAI deployments in early 2026 to **50% by 2028**, yet **73% of enterprises need AI-agent monitoring in production while 63% cite a lack of adequate tooling**. This list maps the landscape so you can find the right tool fast.

**Legend:** 🟢 open-source · 🔵 open-core / hybrid · 🟠 commercial (public repo is an SDK/client only — low star counts don't reflect the product). Star counts are approximate (July 2026) and refreshed periodically.

## Contents

- [What is LLM Observability?](#what-is-llm-observability)
- [🧰 Skills (Batteries Included)](#-skills-batteries-included)
- [Tracing & Observability Platforms](#tracing--observability-platforms)
- [Evaluation Frameworks](#evaluation-frameworks)
- [Prompt Management & Experimentation](#prompt-management--experimentation)
- [LLM Gateways & Proxies](#llm-gateways--proxies)
- [Instrumentation & Standards](#instrumentation--standards-opentelemetry-genai)
- [Guardrails & Safety Monitoring](#guardrails--safety-monitoring)
- [Self-Hosted / Open-Source First](#self-hosted--open-source-first)
- [Research & Benchmarks](#research--benchmarks)
- [Learning Resources](#learning-resources)
- [How to Choose](#how-to-choose)
- [Contributing](#contributing)

## What is LLM Observability?

Traditional observability assumes deterministic systems. LLM apps are **non-deterministic, token-metered, and failure-rich** — they hallucinate, drift, run up cost, and fail silently. LLM observability adds the missing pillars:

- **Tracing** — capture every step of a chain/agent run (prompts, tool calls, retrievals, sub-agent spans) with token + latency + cost per span.
- **Evaluation** — score output quality (correctness, faithfulness, relevance, safety), offline and online, often via **LLM-as-a-judge** and reference-based metrics.
- **Monitoring** — dashboards + alerts on latency, cost, error rate, hallucination/quality scores, and drift over time.
- **Prompt & dataset management** — version prompts, curate eval datasets, and close the feedback loop from production back into tests.

## 🧰 Skills (Batteries Included)

Most lists stop at links. This one ships **original [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)** (by [ContextJet.ai](https://www.contextjetai.com)) that turn the tools below into working setups — drop a folder into your coding agent's skills directory (e.g. `.claude/skills/`) and it gains the workflow. Authored to Anthropic's skill best-practices (focused `SKILL.md`, progressive disclosure, actionable checklists).

| Skill | Use it to… |
|---|---|
| [`instrument-llm-observability`](skills/instrument-llm-observability/SKILL.md) | Add production tracing (OpenTelemetry GenAI or a platform SDK) to an LLM/agent app. |
| [`add-llm-evals`](skills/add-llm-evals/SKILL.md) | Add an offline (CI) + online (LLM-as-a-judge) evaluation suite, with calibration. |
| [`choose-observability-stack`](skills/choose-observability-stack/SKILL.md) | Recommend the right tool/stack for a given set of constraints (self-hosting, budget, compliance). |

→ Browse the [`skills/`](skills/) directory. Contributions of new skills welcome.

## Tracing & Observability Platforms

End-to-end tracing + dashboards for LLM/RAG/agent apps.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🔵 [Langfuse](https://github.com/langfuse/langfuse) | 30.4k | MIT (open-core) | AI engineering platform: tracing, evals, prompt mgmt, playground. The most widely adopted OSS LLM-obs platform. |
| 🟢 [MLflow](https://github.com/mlflow/mlflow) | 26.9k | Apache-2.0 | The ML platform, now with first-class LLM/agent **tracing & evaluation**. |
| 🟢 [Comet Opik](https://github.com/comet-ml/opik) | 20.3k | Apache-2.0 | Trace, evaluate & monitor LLM/RAG/agent apps; automated prompt optimization. |
| 🟢 [Microsoft PromptFlow](https://github.com/microsoft/promptflow) | 11.2k | MIT | Build, test, deploy & monitor LLM apps end-to-end. |
| 🟢 [Arize Phoenix](https://github.com/Arize-ai/phoenix) | 10.4k | Elastic v2 | OpenTelemetry-native AI observability & evaluation; runs locally or self-hosted. |
| 🟢 [Helicone](https://github.com/Helicone/helicone) | 5.9k | Apache-2.0 | One-line **proxy** observability — change the base URL, log every request/cost/error. |
| 🟢 [LangWatch](https://github.com/langwatch/langwatch) | 3.3k | Apache-2.0 | Evals + agent testing + observability platform. |
| 🟢 [OpenLIT](https://github.com/openlit/openlit) | 2.6k | Apache-2.0 | OTel-native LLM observability with GPU monitoring, guardrails & evals. |
| 🟢 [Langtrace](https://github.com/Scale3-Labs/langtrace) | 1.2k | AGPL-3.0 | OpenTelemetry-based end-to-end LLM app observability. |
| 🟢 [W&B Weave](https://github.com/wandb/weave) | 1.1k | Apache-2.0 | Weights & Biases toolkit for tracing/eval of LLM apps (SaaS backend). |
| 🟠 [LangSmith](https://github.com/langchain-ai/langsmith-sdk) | 0.9k (SDK) | MIT (SDK) | Tracing/eval platform from LangChain; SDK is OSS, backend commercial. |
| 🟠 [Datadog LLM Observability](https://github.com/DataDog/dd-trace-py) | 0.6k (tracer) | BSD-3 | LLM Observability product on top of Datadog APM. |
| 🟠 [New Relic AI Monitoring](https://github.com/newrelic/newrelic-python-agent) | 0.2k (agent) | Apache-2.0 | AI monitoring integrated into New Relic's agent. |
| 🟠 [Literal AI](https://github.com/Chainlit/literalai-python) | SDK | Apache-2.0 | Observability/eval platform from the Chainlit team. |
| 🟠 [Lunary](https://github.com/lunary-ai/lunary-py) | SDK | Apache-2.0 | Analytics, monitoring & evals for GenAI apps (open-core). |
| 🟠 [Parea AI](https://github.com/parea-ai/parea-sdk-py) | SDK | Apache-2.0 | Experiment, test, evaluate & monitor LLM apps (YC S23). |
| 🟠 [HoneyHive](https://honeyhive.ai) | — | commercial | Evaluation & observability platform (no primary OSS repo). |

## Evaluation Frameworks

Test and score LLM/agent output — in CI (offline) and in production (online).

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [promptfoo](https://github.com/promptfoo/promptfoo) | 22.9k | MIT | Test/eval prompts, agents & RAG; red-teaming and CI/CD. |
| 🟢 [OpenAI Evals](https://github.com/openai/evals) | 18.8k | MIT | Framework + registry of benchmarks for evaluating LLMs. |
| 🟢 [DeepEval](https://github.com/confident-ai/deepeval) | 16.6k | Apache-2.0 | "Pytest for LLMs" — 40+ metrics for LLM output evaluation. |
| 🟢 [Ragas](https://github.com/vibrantlabsai/ragas) | 14.7k | Apache-2.0 | Evaluation toolkit for LLM/RAG applications. |
| 🟢 [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) | 13.2k | MIT | Few-shot benchmark evaluation of language models (EleutherAI). |
| 🟢 [Evidently](https://github.com/evidentlyai/evidently) | 7.7k | Apache-2.0 | ML + LLM observability/eval with 100+ metrics. |
| 🟢 [Giskard](https://github.com/Giskard-AI/giskard-oss) | 5.5k | Apache-2.0 | Open-source eval & testing for LLM agents. |
| 🟢 [Deepchecks](https://github.com/deepchecks/deepchecks) | 4.0k | AGPL-3.0 | Continuous validation/testing for ML & LLM. |
| 🟢 [TruLens](https://github.com/truera/trulens) | 3.4k | MIT | Evaluation & tracking for LLM experiments and agents. |
| 🟢 [UpTrain](https://github.com/uptrain-ai/uptrain) | 2.4k | Apache-2.0 | Evaluate & improve GenAI apps with 20+ checks. |
| 🟢 [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) | 2.3k | MIT | LLM evaluation framework from the UK AI Safety Institute. |
| 🟢 [DeepTeam](https://github.com/confident-ai/deepteam) | 1.9k | Apache-2.0 | Red-teaming framework for LLMs & agents (by the DeepEval team). |
| 🟢 [OpenEvals](https://github.com/langchain-ai/openevals) | 1.1k | MIT | Ready-made evaluators for LLM apps. |
| 🟠 [Braintrust](https://github.com/braintrustdata/braintrust-sdk-python) | SDK | Apache-2.0 | Tracing + prompt-centric evals; SDK OSS, platform commercial. |
| 🟠 [Athina](https://github.com/athina-ai/athina-evals) | 0.3k | — | Python SDK for running evals on LLM responses. |

## Prompt Management & Experimentation

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [Agenta](https://github.com/Agenta-AI/agenta) | 4.3k | MIT | LLMOps platform: prompt playground, versioning, eval & observability. |
| 🟢 [Pezzo](https://github.com/pezzolabs/pezzo) | 3.3k | Apache-2.0 | Developer-first prompt design, versioning & observability. |
| 🟠 [PromptLayer](https://github.com/MagnivOrg/prompt-layer-library) | 0.8k | Apache-2.0 | Log, track, debug & replay prompts and LLM requests. |

> Langfuse and Agenta also provide strong prompt management — listed once under their best-fit category.

## LLM Gateways & Proxies

Route to many providers through one endpoint; get logging, cost tracking & caching for free.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [LiteLLM](https://github.com/BerriAI/litellm) | 52.6k | MIT | Python SDK + proxy calling 100+ LLMs with unified cost tracking & logging. |
| 🟢 [Portkey Gateway](https://github.com/Portkey-AI/gateway) | 12.3k | MIT | Fast AI gateway routing to 1,600+ LLMs with built-in guardrails & observability. |
| 🟢 [Helicone](https://github.com/Helicone/helicone) | 5.9k | Apache-2.0 | Proxy-first observability (also listed under Tracing). |
| 🟠 Cloudflare AI Gateway | — | commercial | Managed AI gateway with analytics/logging/caching (no OSS repo). |
| 🟠 OpenRouter | — | commercial | Unified API/marketplace routing to many LLMs with usage analytics. |

## Instrumentation & Standards (OpenTelemetry GenAI)

The observability layer is standardizing on **OpenTelemetry** — emit these and your traces export to *any* OTel backend.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [OpenLLMetry](https://github.com/traceloop/openllmetry) | 7.3k | Apache-2.0 | OTel-based open-source observability for GenAI/LLM apps (Traceloop). |
| 🟢 [OpenInference](https://github.com/Arize-ai/openinference) | 1.1k | Apache-2.0 | OpenTelemetry instrumentation for AI observability (Arize). |
| 🟢 [OTel Python Contrib](https://github.com/open-telemetry/opentelemetry-python-contrib) | 1.1k | Apache-2.0 | OTel instrumentation modules, including GenAI. |
| 🟢 [OTel Semantic Conventions](https://github.com/open-telemetry/semantic-conventions) | 0.6k | Apache-2.0 | Home of the **GenAI semantic conventions** spec (`gen_ai.*`). |

## Guardrails & Safety Monitoring

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [Guardrails AI](https://github.com/guardrails-ai/guardrails) | 7.1k | Apache-2.0 | Add input/output guardrails and structured validation to LLMs. |
| 🟢 [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | 6.6k | Apache-2.0 | Programmable guardrails for LLM conversational systems (NVIDIA). |
| 🟢 [LLM Guard](https://github.com/protectai/llm-guard) | 3.1k | MIT | Security toolkit: PII redaction, prompt-injection & toxicity detection. |

## Self-Hosted / Open-Source First

Need data residency / on-prem? These ship a genuinely self-hostable OSS core:
[Langfuse](https://github.com/langfuse/langfuse) (MIT) · [Arize Phoenix](https://github.com/Arize-ai/phoenix) · [Comet Opik](https://github.com/comet-ml/opik) (Apache-2.0) · [Helicone](https://github.com/Helicone/helicone) (Apache-2.0) · [OpenLIT](https://github.com/openlit/openlit) (Apache-2.0) · [Langtrace](https://github.com/Scale3-Labs/langtrace) (AGPL) · [LangWatch](https://github.com/langwatch/langwatch) (Apache-2.0) · [MLflow](https://github.com/mlflow/mlflow) (Apache-2.0) · [Evidently](https://github.com/evidentlyai/evidently) (Apache-2.0).

## Research & Benchmarks

The tooling above is grounded in a fast-moving literature. Key anchors:

- **LLM-as-a-Judge** — Zheng et al., 2023, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) — the basis for scalable, model-graded evaluation used by most eval tools.
- **HELM** — Liang et al., *Holistic Evaluation of Language Models* ([arXiv:2211.09110](https://arxiv.org/abs/2211.09110)) — canonical multi-metric evaluation.
- **SelfCheckGPT** — Manakul et al., 2023 ([arXiv:2303.08896](https://arxiv.org/abs/2303.08896)) — reference-free hallucination detection.
- **Agent hallucination** — *MIRAGE-Bench* ([arXiv:2507.21017](https://arxiv.org/abs/2507.21017)); paper list: [EdinburghNLP/awesome-hallucination-detection](https://github.com/EdinburghNLP/awesome-hallucination-detection).
- **OTel GenAI semantic conventions** — the observability standard (see [Instrumentation & Standards](#instrumentation--standards-opentelemetry-genai)).

## Learning Resources

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) — the emerging standard for LLM telemetry.
- [Arize Phoenix docs](https://docs.arize.com/phoenix) & [Langfuse docs](https://langfuse.com/docs) — practical tracing/eval concepts.
- Hamel Husain — [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/).
- Chip Huyen — [*Building LLM applications for production*](https://huyenchip.com/2023/04/11/llm-engineering.html).

## How to Choose

- **Just need traces + cost, minimal code?** Start with a **gateway/proxy** (change base URL, zero SDK) or a tracing platform with OTel auto-instrumentation.
- **Need to *test* quality, not just watch it?** Add an **evaluation framework** (offline eval in CI + online LLM-as-a-judge).
- **Data residency / on-prem required?** Pick from [Self-Hosted](#self-hosted--open-source-first).
- **Want vendor-neutral, future-proof traces?** Emit **OTel GenAI semantic conventions** so you can swap backends.

A common production setup pairs a **gateway** (cost + routing) with an **evaluation tool** (quality) on top of an **OTel-native tracing** backbone.

## Contributing

Contributions welcome — see [`CONTRIBUTING.md`](CONTRIBUTING.md). Add a tool via PR with: name, link, one-line **neutral** description, correct category, and the OSS/commercial marker. Keep it factual and non-promotional — a wrong entry or dead link discredits the whole list.

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](LICENSE)

To the extent possible under law, the contributors have waived all copyright and related rights to this work.
