<div align="center">

# Awesome LLM Observability [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

**A current, hand-checked list of 60+ LLM observability tools, plus 26 [agent skills](#-skills-batteries-included) you install in one command.**

Star counts refresh themselves. The skills get validated in CI. More on both further down.

[![26 Agent Skills](https://img.shields.io/badge/🧰_Agent_Skills-26-1f6feb)](#-skills-batteries-included)
[![Install](https://img.shields.io/badge/install-1_command-brightgreen)](#-skills-batteries-included)
[![tests](https://github.com/ContextJet-ai/awesome-llm-observability/actions/workflows/tests.yml/badge.svg)](https://github.com/ContextJet-ai/awesome-llm-observability/actions/workflows/tests.yml)
[![skills validated](https://github.com/ContextJet-ai/awesome-llm-observability/actions/workflows/skill-validation.yml/badge.svg)](https://github.com/ContextJet-ai/awesome-llm-observability/actions/workflows/skill-validation.yml)
[![Awesome](https://img.shields.io/badge/Awesome-list-blueviolet)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: CC0](https://img.shields.io/badge/License-CC0_1.0-lightgrey.svg)](LICENSE)
[![By ContextJet.ai](https://img.shields.io/badge/by-ContextJet.ai-1f6feb)](https://www.contextjetai.com)

</div>

The tooling for watching LLM apps in production is a fast-moving mess of overlapping projects, and every list I found had stars from 2023 on it. So I kept my own, verified the entries, and wired up a job to keep the numbers honest. Use it to find the right tool without re-researching the whole space.

**Legend:** 🟢 open-source · 🔵 open-core / hybrid · 🟠 commercial (public repo is an SDK/client only - low star counts don't reflect the product). Star counts are pulled live from the GitHub API and **auto-refreshed weekly by CI** ([tools/refresh_stars.py](tools/refresh_stars.py)), so they stay current instead of rotting.

## Contents

- [What is LLM Observability?](#what-is-llm-observability)
- [🧰 Skills (Batteries Included)](#-skills-batteries-included)
- [Platform Comparison (At a Glance)](#platform-comparison-at-a-glance)
- [Tracing & Observability Platforms](#tracing--observability-platforms)
- [Evaluation Frameworks](#evaluation-frameworks)
- [Prompt Management & Experimentation](#prompt-management--experimentation)
- [LLM Gateways & Proxies](#llm-gateways--proxies)
- [Instrumentation & Standards](#instrumentation--standards-opentelemetry-genai)
- [Guardrails & Safety Monitoring](#guardrails--safety-monitoring)
- [Self-Hosted / Open-Source First](#self-hosted--open-source-first)
- [Research & Benchmarks](#research--benchmarks)
- [Learning Resources](#learning-resources)
- [Guides & Tools (Original)](#guides--tools-original)
- [How to Choose](#how-to-choose)
- [Contributing](#contributing)

## What is LLM Observability?

Regular observability assumes your system is deterministic. LLM apps aren't. They make things up, drift as inputs change, quietly burn tokens, and fail without ever throwing an error. So you end up watching different things:

- tracing: every step of a run, with tokens, latency, and cost per span
- evals: whether the output is actually any good, both offline and on live traffic
- monitoring: alerts when quality, cost, latency, or error rate move
- prompt and dataset management: version your prompts, and pull real production cases back into your tests

People call this LLMOps observability, AI observability, or just LLM monitoring. Same idea.

## 🧰 Skills (Batteries Included)

Most lists stop at links. This one also ships 26 [agent skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), the `SKILL.md` kind, so your coding agent knows how to actually do this stuff instead of just knowing where the tools live. They fire on plain requests like "add tracing" or "reduce my LLM bill".

A handful (marked ⚙️) are backed by real Python with unit tests that run in CI. The rest ship trigger cases and get checked by [skillvitals](https://github.com/ContextJet-ai/skillvitals), a small tool I built to measure whether a skill actually fires when it should. A free heuristic runs on every push as a regression gate.

Graded on a cheap model (llama-3.1-8b via NVIDIA NIM), the 26 skills average a trigger F1 of 0.99 (98.7% recall, 0% false-fire), and that holds even against adjacent negatives, prompts about a *different* LLM task the skill should refuse to fire on. It's not a clean sweep though. `choose-observability-stack` came in at 0.80 because the model kept confusing a "compare Langfuse vs Phoenix" prompt with the model-comparison skill. That's exactly the kind of overlap this is meant to catch. Run it yourself:

```bash
skillvitals trigger skills/reduce-llm-cost/SKILL.md \
  --cases validation/cases/reduce-llm-cost.yaml \
  --model meta/llama-3.1-8b-instruct --base-url https://integrate.api.nvidia.com/v1
```

### Install (about 10 seconds)

**As a Claude Code plugin (easiest):**
```
/plugin marketplace add ContextJet-ai/awesome-llm-observability
/plugin install llm-observability@contextjet
```

**Or copy the skills into any agent's skills folder:**
```bash
npx degit ContextJet-ai/awesome-llm-observability/skills ~/.claude/skills
```

**Or clone and run the installer:**
```bash
git clone https://github.com/ContextJet-ai/awesome-llm-observability
./awesome-llm-observability/install.sh          # installs into ~/.claude/skills
```

### The skills

| Skill | Use it to… |
|---|---|
| [`instrument-llm-observability`](skills/instrument-llm-observability/SKILL.md) | Add production tracing (OpenTelemetry GenAI or a platform SDK) to an LLM/agent app. |
| ⚙️ [`validate-genai-spans`](skills/validate-genai-spans/SKILL.md) | Lint your spans against the OTel GenAI spec so cost/latency dashboards aren't full of holes. |
| [`add-llm-evals`](skills/add-llm-evals/SKILL.md) | Add an offline (CI) + online (LLM-as-a-judge) evaluation suite, with calibration. |
| [`eval-driven-development`](skills/eval-driven-development/SKILL.md) | Improve a prompt/agent the reliable way: write evals first, iterate against them (TDD for LLMs). |
| [`build-eval-dataset`](skills/build-eval-dataset/SKILL.md) | Build an eval set that actually reflects production (the part everyone underestimates). |
| [`optimize-prompts`](skills/optimize-prompts/SKILL.md) | Improve a prompt systematically against an eval set (few-shot selection, DSPy/APE), not by feel. |
| [`debug-agent-from-traces`](skills/debug-agent-from-traces/SKILL.md) | Diagnose *why* an agent gave a wrong / empty / slow / expensive result, from its trace. |
| [`trace-based-testing`](skills/trace-based-testing/SKILL.md) | Turn real production traces into a regression suite so bugs never come back. |
| [`collect-user-feedback`](skills/collect-user-feedback/SKILL.md) | Capture thumbs/edits/implicit signals, attach to traces, feed back into evals. |
| [`annotate-traces-for-review`](skills/annotate-traces-for-review/SKILL.md) | Human review + error analysis of traces to build golden data and calibrate judges. |
| [`reduce-llm-cost`](skills/reduce-llm-cost/SKILL.md) | Cut your LLM bill using observability data (find the expensive spans first). |
| ⚙️ [`estimate-llm-cost`](skills/estimate-llm-cost/SKILL.md) | Price a call, project a monthly bill, and compare models with a real calculator. |
| [`add-llm-fallbacks`](skills/add-llm-fallbacks/SKILL.md) | Make LLM calls resilient: timeouts, backoff, provider fallback, all observed. |
| [`monitor-rag-quality`](skills/monitor-rag-quality/SKILL.md) | Measure + fix RAG quality, telling retrieval bugs from generation bugs. |
| [`detect-hallucinations`](skills/detect-hallucinations/SKILL.md) | Detect when the model is making things up (self-consistency, semantic entropy, faithfulness). |
| ⚙️ [`check-answer-consistency`](skills/check-answer-consistency/SKILL.md) | Cheap reference-free hallucination signal: sample N times, score the agreement. |
| [`trace-multi-agent-system`](skills/trace-multi-agent-system/SKILL.md) | Add observability to a multi-agent / agentic system (who did what, handoffs, loops). |
| [`measure-agent-task-success`](skills/measure-agent-task-success/SKILL.md) | Measure whether an agent actually completed the task end to end, not just per-call quality. |
| [`set-up-drift-alerts`](skills/set-up-drift-alerts/SKILL.md) | Catch quality / cost / latency / input drift in production before your users do. |
| [`set-up-ab-testing`](skills/set-up-ab-testing/SKILL.md) | Test a prompt/model change on real traffic (canary/A-B) before rolling it out to everyone. |
| [`add-llm-guardrails`](skills/add-llm-guardrails/SKILL.md) | Add input/output guardrails (injection, PII, schema, safety) and observe them. |
| [`red-team-llm-app`](skills/red-team-llm-app/SKILL.md) | Adversarially test for prompt injection, jailbreaks & tool misuse (OWASP LLM Top 10). |
| [`compare-llm-models`](skills/compare-llm-models/SKILL.md) | Pick or switch the model on evidence (your eval set), not leaderboards or hype. |
| [`redact-pii-for-tracing`](skills/redact-pii-for-tracing/SKILL.md) | Add **compliant** tracing for finance/regulated apps without leaking PII. |
| ⚙️ [`scrub-pii-from-text`](skills/scrub-pii-from-text/SKILL.md) | Mask emails/cards/SSNs/IBANs before they hit the backend (Luhn-checked). |
| [`choose-observability-stack`](skills/choose-observability-stack/SKILL.md) | Recommend the right tool/stack for given constraints (self-hosting, budget, compliance). |

**Also original in this repo:**
- 📖 Guide - [**LLM Observability for Finance & Regulated Industries**](guides/llm-observability-for-finance.md)
- 🛠️ Tool - [**`genai_trace.py`**](tools/genai_trace.py): a minimal, vendor-neutral OpenTelemetry GenAI tracer with a built-in PII-redaction hook (no-op if OTel isn't installed).

→ Browse [`skills/`](skills/), [`guides/`](guides/), [`tools/`](tools/). Contributions welcome.

## Platform Comparison (At a Glance)

The question everyone asks first is _"Langfuse or Phoenix or LangSmith or Opik or Helicone?"_ Pick by the constraints you can't bend (self-hosting, license), then worry about features. Double-check specifics against the docs, this table moves.

| Platform | Self-host | License | Tracing | Evals | Prompt Mgmt | OTel-native |
|---|:--:|---|:--:|:--:|:--:|:--:|
| [Langfuse](https://github.com/langfuse/langfuse) | ✅ | MIT | ✅ | ✅ | ✅ | ✅ |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | ✅ | Elastic v2 | ✅ | ✅ | ➖ | ✅ |
| [Comet Opik](https://github.com/comet-ml/opik) | ✅ | Apache-2.0 | ✅ | ✅ | ✅ | ➖ |
| [LangSmith](https://github.com/langchain-ai/langsmith-sdk) | ➖ SaaS | Commercial | ✅ | ✅ | ✅ | ➖ |
| [Helicone](https://github.com/Helicone/helicone) | ✅ | Apache-2.0 | ✅ | ➖ | ✅ | ➖ |
| [Latitude](https://github.com/latitude-dev/latitude-llm) | ✅ | MIT | ✅ | ✅ | ✅ | ➖ |
| [Laminar](https://github.com/lmnr-ai/lmnr) | ✅ | Apache-2.0 | ✅ | ✅ | ➖ | ✅ |
| [MLflow](https://github.com/mlflow/mlflow) | ✅ | Apache-2.0 | ✅ | ✅ | ➖ | ✅ |
| [OpenLIT](https://github.com/openlit/openlit) | ✅ | Apache-2.0 | ✅ | ✅ | ➖ | ✅ |

✅ first-class · ➖ limited/not the focus. Need help deciding? Use the [`choose-observability-stack`](skills/choose-observability-stack/SKILL.md) skill.

## Tracing & Observability Platforms

End-to-end tracing + dashboards for LLM/RAG/agent apps.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🔵 [Langfuse](https://github.com/langfuse/langfuse) | 31.5k | MIT (open-core) | AI engineering platform: tracing, evals, prompt mgmt, playground. The most widely adopted OSS LLM-obs platform. |
| 🟢 [MLflow](https://github.com/mlflow/mlflow) | 27.1k | Apache-2.0 | The ML platform, now with first-class LLM/agent **tracing & evaluation**. |
| 🟢 [Comet Opik](https://github.com/comet-ml/opik) | 20.7k | Apache-2.0 | Trace, evaluate & monitor LLM/RAG/agent apps; automated prompt optimization. |
| 🟢 [Microsoft PromptFlow](https://github.com/microsoft/promptflow) | 11.2k | MIT | Build, test, deploy & monitor LLM apps end-to-end. |
| 🟢 [Arize Phoenix](https://github.com/Arize-ai/phoenix) | 10.6k | Elastic v2 | OpenTelemetry-native AI observability & evaluation; runs locally or self-hosted. |
| 🟢 [Helicone](https://github.com/Helicone/helicone) | 6.0k | Apache-2.0 | One-line **proxy** observability - change the base URL, log every request/cost/error. |
| 🟢 [Latitude](https://github.com/latitude-dev/latitude-llm) | 4.5k | MIT | Open-source LLM monitoring + prompt-engineering platform. |
| 🟢 [Laminar](https://github.com/lmnr-ai/lmnr) | 3.1k | Apache-2.0 | Open-source observability + evals, purpose-built for AI agents. |
| 🟢 [LangWatch](https://github.com/langwatch/langwatch) | 3.4k | Apache-2.0 | Evals + agent testing + observability platform. |
| 🟢 [OpenLIT](https://github.com/openlit/openlit) | 2.6k | Apache-2.0 | OTel-native LLM observability with GPU monitoring, guardrails & evals. |
| 🟢 [Langtrace](https://github.com/Scale3-Labs/langtrace) | 1.2k | AGPL-3.0 | OpenTelemetry-based end-to-end LLM app observability. |
| 🟢 [W&B Weave](https://github.com/wandb/weave) | 1.1k | Apache-2.0 | Weights & Biases toolkit for tracing/eval of LLM apps (SaaS backend). |
| 🟠 [LangSmith](https://github.com/langchain-ai/langsmith-sdk) | 973 (SDK) | MIT (SDK) | Tracing/eval platform from LangChain; SDK is OSS, backend commercial. |
| 🟠 [Datadog LLM Observability](https://github.com/DataDog/dd-trace-py) | 647 (tracer) | BSD-3 | LLM Observability product on top of Datadog APM. |
| 🟠 [New Relic AI Monitoring](https://github.com/newrelic/newrelic-python-agent) | 209 (agent) | Apache-2.0 | AI monitoring integrated into New Relic's agent. |
| 🟠 [Azure Monitor / App Insights](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable) | SDK | MIT (SDK) | OpenTelemetry-native APM with GenAI + agent-trace visualization; the observability backend under Azure AI Foundry. |
| 🟠 [Literal AI](https://github.com/Chainlit/literalai-python) | SDK | Apache-2.0 | Observability/eval platform from the Chainlit team. |
| 🟠 [Lunary](https://github.com/lunary-ai/lunary-py) | SDK | Apache-2.0 | Analytics, monitoring & evals for GenAI apps (open-core). |
| 🟠 [Parea AI](https://github.com/parea-ai/parea-sdk-py) | SDK | Apache-2.0 | Experiment, test, evaluate & monitor LLM apps (YC S23). |
| 🟠 [HoneyHive](https://honeyhive.ai) | - | commercial | Evaluation & observability platform (no primary OSS repo). |
| 🟢 [AgentOps](https://github.com/AgentOps-AI/agentops) | 5.7k | MIT | Agent monitoring with session replays, cost + latency tracking, across agent frameworks. |
| 🟢 [Pydantic Logfire](https://github.com/pydantic/logfire) | 4.4k | MIT | OpenTelemetry-based observability for LLM and agent apps, from the Pydantic team. |

## Evaluation Frameworks

Test and score LLM/agent output. One thing to sort out before you pick a tool: are you doing **offline/batch** evals (run over a dataset in CI to optimize a prompt) or **inline** evals (score a response live, to gate or block it before it reaches the user)? They're pretty different jobs. Most of the frameworks below are built for the offline case. Live gating usually lands in the [guardrails](#guardrails--safety-monitoring) tools or a platform's online-scoring feature.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [promptfoo](https://github.com/promptfoo/promptfoo) | 23.4k | MIT | Test/eval prompts, agents & RAG; red-teaming and CI/CD. |
| 🟢 [OpenAI Evals](https://github.com/openai/evals) | 18.9k | MIT | Framework + registry of benchmarks for evaluating LLMs. |
| 🟢 [DeepEval](https://github.com/confident-ai/deepeval) | 17.0k | Apache-2.0 | "Pytest for LLMs" - 40+ metrics for LLM output evaluation. |
| 🟢 [Ragas](https://github.com/vibrantlabsai/ragas) | 14.9k | Apache-2.0 | Evaluation toolkit for LLM/RAG applications. |
| 🟢 [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) | 13.3k | MIT | Few-shot benchmark evaluation of language models (EleutherAI). |
| 🟢 [Evidently](https://github.com/evidentlyai/evidently) | 7.7k | Apache-2.0 | ML + LLM observability/eval with 100+ metrics. |
| 🟢 [Giskard](https://github.com/Giskard-AI/giskard-oss) | 5.7k | Apache-2.0 | Open-source eval & testing for LLM agents. |
| 🟢 [Deepchecks](https://github.com/deepchecks/deepchecks) | 4.0k | AGPL-3.0 | Continuous validation/testing for ML & LLM. |
| 🟢 [TruLens](https://github.com/truera/trulens) | 3.4k | MIT | Evaluation & tracking for LLM experiments and agents. |
| 🟢 [UpTrain](https://github.com/uptrain-ai/uptrain) | 2.4k | Apache-2.0 | Evaluate & improve GenAI apps with 20+ checks. |
| 🟢 [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) | 2.4k | MIT | LLM evaluation framework from the UK AI Safety Institute. |
| 🟢 [DeepTeam](https://github.com/confident-ai/deepteam) | 2.3k | Apache-2.0 | Red-teaming framework for LLMs & agents (by the DeepEval team). |
| 🟢 [OpenEvals](https://github.com/langchain-ai/openevals) | 1.1k | MIT | Ready-made evaluators for LLM apps. |
| 🟠 [Braintrust](https://github.com/braintrustdata/braintrust-sdk-python) | SDK | Apache-2.0 | Tracing + prompt-centric evals; SDK OSS, platform commercial. |
| 🟠 [Azure AI Evaluation (Foundry)](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation) | SDK | MIT | Microsoft Foundry's evaluation SDK: built-in quality + safety/risk evaluators; runs locally or in Foundry. |
| 🟠 [Athina](https://github.com/athina-ai/athina-evals) | 301 | - | Python SDK for running evals on LLM responses. |
| 🟢 [HELM](https://github.com/stanford-crfm/helm) | 2.9k | Apache-2.0 | Stanford's Holistic Evaluation of Language Models: broad, multi-metric benchmarking. |
| 🟢 [RAGChecker](https://github.com/amazon-science/RAGChecker) | 1.1k | Apache-2.0 | Fine-grained framework for diagnosing RAG failures (retriever vs generator). |
| 🟢 [continuous-eval](https://github.com/relari-ai/continuous-eval) | 516 | Apache-2.0 | Data-driven, modular evaluation for LLM/RAG pipelines. |
| 🟠 [Galileo](https://github.com/rungalileo/galileo-python) | SDK | Apache-2.0 | Eval + observability platform; SDK OSS, platform commercial. |
| 🟠 [Openlayer](https://github.com/openlayer-ai/openlayer-python) | SDK | Apache-2.0 | Testing, eval & monitoring platform; SDK OSS, platform commercial. |
| 🟢 [whatbroke](https://github.com/arthi-arumugam-git/whatbroke) | 1 | MIT | CLI that diffs two agent runs: tool calls, args, cost, latency, outcome flips, flake detection. |

## Prompt Management & Experimentation

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [Agenta](https://github.com/Agenta-AI/agenta) | 4.3k | MIT | LLMOps platform: prompt playground, versioning, eval & observability. |
| 🟢 [Pezzo](https://github.com/pezzolabs/pezzo) | 3.3k | Apache-2.0 | Developer-first prompt design, versioning & observability. |
| 🟠 [PromptLayer](https://github.com/MagnivOrg/prompt-layer-library) | 779 | Apache-2.0 | Log, track, debug & replay prompts and LLM requests. |

> Langfuse and Agenta also provide strong prompt management - listed once under their best-fit category.

## LLM Gateways & Proxies

Route to many providers through one endpoint; get logging, cost tracking & caching for free.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [LiteLLM](https://github.com/BerriAI/litellm) | 54.1k | MIT | Python SDK + proxy calling 100+ LLMs with unified cost tracking & logging. |
| 🟢 [Portkey Gateway](https://github.com/Portkey-AI/gateway) | 12.5k | MIT | Fast AI gateway routing to 1,600+ LLMs with built-in guardrails & observability. |
| 🟢 [Helicone](https://github.com/Helicone/helicone) | 6.0k | Apache-2.0 | Proxy-first observability (also listed under Tracing). |
| 🟠 Cloudflare AI Gateway | - | commercial | Managed AI gateway with analytics/logging/caching (no OSS repo). |
| 🟠 OpenRouter | - | commercial | Unified API/marketplace routing to many LLMs with usage analytics. |
| 🟢 [Bifrost](https://github.com/maximhq/bifrost) | 6.6k | Apache-2.0 | Fast AI gateway routing to 1,000+ models with logging, cost tracking & governance. |

## Instrumentation & Standards (OpenTelemetry GenAI)

The observability layer is standardizing on **OpenTelemetry** - emit these and your traces export to *any* OTel backend.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [OpenLLMetry](https://github.com/traceloop/openllmetry) | 7.3k | Apache-2.0 | OTel-based open-source observability for GenAI/LLM apps (Traceloop). |
| 🟢 [OpenInference](https://github.com/Arize-ai/openinference) | 1.1k | Apache-2.0 | OpenTelemetry instrumentation for AI observability (Arize). |
| 🟢 [OTel Python Contrib](https://github.com/open-telemetry/opentelemetry-python-contrib) | 1.1k | Apache-2.0 | OTel instrumentation modules, including GenAI. |
| 🟢 [Noveum Trace](https://github.com/Noveum/noveum-trace) | 12 | Apache-2.0 | OpenTelemetry-compliant tracing SDK built specifically for LLM/agent apps. |
| 🟢 [OTel Semantic Conventions](https://github.com/open-telemetry/semantic-conventions) | 614 | Apache-2.0 | Home of the **GenAI semantic conventions** spec (`gen_ai.*`). |
| 🟢 [WhyLabs LangKit](https://github.com/whylabs/langkit) | 992 | Apache-2.0 | Extract telemetry/metrics (quality, sentiment, injection signals) from prompts & responses. |

## Guardrails & Safety Monitoring

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [Guardrails AI](https://github.com/guardrails-ai/guardrails) | 7.2k | Apache-2.0 | Add input/output guardrails and structured validation to LLMs. |
| 🟢 [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | 6.7k | Apache-2.0 | Programmable guardrails for LLM conversational systems (NVIDIA). |
| 🟢 [LLM Guard](https://github.com/protectai/llm-guard) | 3.2k | MIT | Security toolkit: PII redaction, prompt-injection & toxicity detection. |
| 🟢 [Presidio](https://github.com/data-privacy-stack/presidio) | 10.1k | MIT | PII detection, redaction & anonymization; the standard for scrubbing prompts and traces. |
| 🟢 [garak](https://github.com/NVIDIA/garak) | 8.5k | Apache-2.0 | LLM vulnerability scanner: probes for prompt injection, jailbreaks & data leakage (NVIDIA). |

## Self-Hosted / Open-Source First

Need data residency / on-prem? These ship a genuinely self-hostable OSS core:
[Langfuse](https://github.com/langfuse/langfuse) (MIT) · [Arize Phoenix](https://github.com/Arize-ai/phoenix) · [Comet Opik](https://github.com/comet-ml/opik) (Apache-2.0) · [Helicone](https://github.com/Helicone/helicone) (Apache-2.0) · [OpenLIT](https://github.com/openlit/openlit) (Apache-2.0) · [Langtrace](https://github.com/Scale3-Labs/langtrace) (AGPL) · [LangWatch](https://github.com/langwatch/langwatch) (Apache-2.0) · [MLflow](https://github.com/mlflow/mlflow) (Apache-2.0) · [Evidently](https://github.com/evidentlyai/evidently) (Apache-2.0) · [SigNoz](https://github.com/SigNoz/signoz) (open-core, OTel-native).

## Research & Benchmarks

The tooling above is grounded in a fast-moving literature. Key anchors:

- **LLM-as-a-Judge** - Zheng et al., 2023, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) - the basis for scalable, model-graded evaluation used by most eval tools.
- **HELM** - Liang et al., *Holistic Evaluation of Language Models* ([arXiv:2211.09110](https://arxiv.org/abs/2211.09110)) - canonical multi-metric evaluation.
- **SelfCheckGPT** - Manakul et al., 2023 ([arXiv:2303.08896](https://arxiv.org/abs/2303.08896)) - reference-free hallucination detection.
- **Agent hallucination** - *MIRAGE-Bench* ([arXiv:2507.21017](https://arxiv.org/abs/2507.21017)); paper list: [EdinburghNLP/awesome-hallucination-detection](https://github.com/EdinburghNLP/awesome-hallucination-detection).
- **OTel GenAI semantic conventions** - the observability standard (see [Instrumentation & Standards](#instrumentation--standards-opentelemetry-genai)).

## Learning Resources

- [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) - the emerging standard for LLM telemetry.
- [Arize Phoenix docs](https://docs.arize.com/phoenix) & [Langfuse docs](https://langfuse.com/docs) - practical tracing/eval concepts.
- Hamel Husain - [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/).
- Chip Huyen - [*Building LLM applications for production*](https://huyenchip.com/2023/04/11/llm-engineering.html).
- Loop & Retry - [*Measuring agent failure in production*](https://loopandretry.github.io/posts/measuring-agent-failure-in-production/) - which signals actually surface a broken agent in prod, and why request-level success rates hide the failures that matter.

## Guides & Tools (Original)

Original work in this repo, not just curated links:

- 🧰 **[Agent Skills](skills/)** - 26 ready-to-run workflows (instrument, evals, debug-from-traces, guardrails, PII-safe tracing, tool selection).
- 📖 **[LLM Observability for Finance & Regulated Industries](guides/llm-observability-for-finance.md)** - a guide for teams where observability is a *compliance control*, not a dashboard.
- 🛠️ **[](tools/genai_trace.py)** - a minimal vendor-neutral OpenTelemetry GenAI tracer with a PII-redaction hook.

## How to Choose

- **Just need traces + cost, minimal code?** Start with a **gateway/proxy** (change base URL, zero SDK) or a tracing platform with OTel auto-instrumentation.
- **Need to *test* quality, not just watch it?** Add an **evaluation framework** (offline eval in CI + online LLM-as-a-judge).
- **Data residency / on-prem required?** Pick from [Self-Hosted](#self-hosted--open-source-first).
- **Want vendor-neutral, future-proof traces?** Emit **OTel GenAI semantic conventions** so you can swap backends.

A common production setup pairs a **gateway** (cost + routing) with an **evaluation tool** (quality) on top of an **OTel-native tracing** backbone.

## Contributing

Contributions welcome - see [`CONTRIBUTING.md`](CONTRIBUTING.md). Add a tool via PR with: name, link, one-line **neutral** description, correct category, and the OSS/commercial marker. Keep it factual and non-promotional - a wrong entry or dead link discredits the whole list.

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](LICENSE)

To the extent possible under law, the contributors have waived all copyright and related rights to this work.
