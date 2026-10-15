<div align="center">

# Awesome LLM Observability [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

**A current, hand-checked list of 75+ LLM observability tools, plus 26 [agent skills](#-skills-batteries-included) you install in one command.**

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
- 🛠️ Tool - [**`genai_trace.py`**](tools/genai_trace.py): a minimal, vendor-neutral OpenTelemetry GenAI tracer (current attribute names: `gen_ai.provider.name`, `gen_ai.input.messages`) with a built-in PII-redaction hook (no-op if OTel isn't installed).

→ Browse [`skills/`](skills/), [`guides/`](guides/), [`tools/`](tools/). Contributions welcome.

## Platform Comparison (At a Glance)

The question everyone asks first is _"Langfuse or Phoenix or LangSmith or Opik or Helicone?"_ Pick by the constraints you can't bend (self-hosting, license), then worry about features. Double-check specifics against the docs, this table moves.

| Platform | Self-host | License | Tracing | Evals | Prompt Mgmt | OTel-native |
|---|:--:|---|:--:|:--:|:--:|:--:|
| [Langfuse](https://github.com/langfuse/langfuse) | ✅ | MIT | ✅ | ✅ | ✅ | ✅ |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | ✅ | Elastic v2 | ✅ | ✅ | ✅ | ✅ |
| [Comet Opik](https://github.com/comet-ml/opik) | ✅ | Apache-2.0 | ✅ | ✅ | ✅ | ✅ |
| [LangSmith](https://github.com/langchain-ai/langsmith-sdk) | ➖ SaaS | Commercial | ✅ | ✅ | ✅ | ✅ |
| [Helicone](https://github.com/Helicone/helicone) | ✅ | Apache-2.0 | ✅ | ✅ | ✅ | ➖ |
| [Latitude](https://github.com/latitude-dev/latitude-llm) | ✅ | MIT | ✅ | ✅ | ✅ | ✅ |
| [Laminar](https://github.com/lmnr-ai/lmnr) | ✅ | Apache-2.0 | ✅ | ✅ | ➖ | ✅ |
| [MLflow](https://github.com/mlflow/mlflow) | ✅ | Apache-2.0 | ✅ | ✅ | ➖ | ✅ |
| [OpenLIT](https://github.com/openlit/openlit) | ✅ | Apache-2.0 | ✅ | ✅ | ➖ | ✅ |

✅ first-class · ➖ limited/not the focus. OTel-native means the backend ingests OTLP directly (Opik, LangSmith and Latitude all added OTLP endpoints; checked October 2026). Need help deciding? Use the [`choose-observability-stack`](skills/choose-observability-stack/SKILL.md) skill.

## Tracing & Observability Platforms

End-to-end tracing + dashboards for LLM/RAG/agent apps.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🔵 [Langfuse](https://github.com/langfuse/langfuse) | 35.9k | MIT (open-core) | AI engineering platform: tracing, evals, prompt mgmt, playground. The most widely adopted OSS LLM-obs platform. |
| 🔵 [PostHog](https://github.com/PostHog/posthog) | 40.3k | MIT (open-core) | LLM analytics inside the product-analytics platform: traces, generations, cost and latency tied to the user and session that produced them; self-hostable. |
| 🔵 [SigNoz](https://github.com/SigNoz/signoz) | 32.4k | MIT (open-core) | OpenTelemetry-native APM that accepts GenAI spans from any OTel instrumentation; logs, metrics and traces in one backend, ClickHouse underneath. |
| 🟢 [MLflow](https://github.com/mlflow/mlflow) | 28.4k | Apache-2.0 | The ML platform, now with first-class LLM/agent **tracing & evaluation**. |
| 🟢 [Comet Opik](https://github.com/comet-ml/opik) | 22.6k | Apache-2.0 | Trace, evaluate & monitor LLM/RAG/agent apps; automated prompt optimization. |
| 🟢 [Microsoft PromptFlow](https://github.com/microsoft/promptflow) | 11.3k | MIT | Build, test, deploy & monitor LLM apps end-to-end. |
| 🟢 [Arize Phoenix](https://github.com/Arize-ai/phoenix) | 11.9k | Elastic v2 | OpenTelemetry-native AI observability & evaluation; runs locally or self-hosted. |
| 🟢 [Helicone](https://github.com/Helicone/helicone) | 6.2k | Apache-2.0 | One-line **proxy** observability - change the base URL, log every request/cost/error. |
| 🟢 [Latitude](https://github.com/latitude-dev/latitude-llm) | 4.7k | MIT | Open-source LLM monitoring + prompt-engineering platform. |
| 🟢 [Laminar](https://github.com/lmnr-ai/lmnr) | 3.4k | Apache-2.0 | Open-source observability + evals, purpose-built for AI agents. |
| 🟢 [LangWatch](https://github.com/langwatch/langwatch) | 5.0k | Apache-2.0 | Evals + agent testing + observability platform. |
| 🟢 [OpenLIT](https://github.com/openlit/openlit) | 2.9k | Apache-2.0 | OTel-native LLM observability with GPU monitoring, guardrails & evals. |
| 🟢 [W&B Weave](https://github.com/wandb/weave) | 1.1k | Apache-2.0 | Weights & Biases toolkit for tracing/eval of LLM apps (SaaS backend). |
| 🟠 [LangSmith](https://github.com/langchain-ai/langsmith-sdk) | 1.1k (SDK) | MIT (SDK) | Tracing/eval platform from LangChain; SDK is OSS, backend commercial. |
| 🟠 [Datadog LLM Observability](https://github.com/DataDog/dd-trace-py) | 652 (tracer) | BSD-3 | LLM Observability product on top of Datadog APM. |
| 🟠 [New Relic AI Monitoring](https://github.com/newrelic/newrelic-python-agent) | 220 (agent) | Apache-2.0 | AI monitoring integrated into New Relic's agent. |
| 🟠 [Azure Monitor / App Insights](https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-enable) | SDK | MIT (SDK) | OpenTelemetry-native APM with GenAI + agent-trace visualization; the observability backend under Azure AI Foundry. |
| 🟠 [Lunary](https://lunary.ai) | - | commercial | Analytics, monitoring & evals for GenAI apps; the Python SDK repo was archived in 2025, the hosted product continues. |
| 🟠 [HoneyHive](https://honeyhive.ai) | - | commercial | Evaluation & observability platform (no primary OSS repo). |
| 🟢 [AgentOps](https://github.com/AgentOps-AI/agentops) | 5.9k | MIT | Agent monitoring with session replays, cost + latency tracking, across agent frameworks. |
| 🟢 [Pydantic Logfire](https://github.com/pydantic/logfire) | 4.5k | MIT | OpenTelemetry-based observability for LLM and agent apps, from the Pydantic team. |
| 🔵 [ClawMetry](https://github.com/vivekchand/clawmetry) | 427 | MIT (open-core) | Reads coding-agent session logs from disk rather than proxying calls; sessions, tool calls, tokens and cost for Claude Code, Codex, Cursor, Aider and others. |
| 🟠 [telemetry.dev](https://telemetry.dev) | - | commercial | OpenTelemetry-native tracing for LLM/agent apps: per-span tokens, cost, latency and errors; TypeScript SDKs or any OTLP exporter (no primary OSS repo). |
| 🟢 [Overmind](https://github.com/overmind-core/overmind) | 659 | AGPL-3.0 (MIT SDK) | OpenTelemetry-native tracing and evals whose traces feed dataset curation, LoRA fine-tuning and serving of small open-weight models; self-hostable. |
| 🟢 [OrcaReplay](https://github.com/Continuum-AI-Corp/OrcaReplay) | 285 | Apache-2.0 | Records a coding-agent run below the harness and replays it offline from the recorded bytes with no model called; a run can be forked at any step onto a different model. |
| 🟠 [The Context Company](https://github.com/The-Context-Company/observatory) | 124 (SDK) | MIT (SDK) | Agent observability and customer analytics: recurring patterns and account-level insights from production conversations and traces; SDK is OSS, platform commercial. |
| 🟠 [Apica AI & LLM Observability](https://www.apica.io/ai-llm-observability/) | - | commercial | OpenTelemetry-native AI agent and LLM observability; token cost attribution, multi-agent trace visualization, and telemetry pipeline governance. |
| 🟠 [Flowlines](https://flowlines.ai/) | - | commercial | Behavioral observability for production AI agents; analyzes traces for drift, repeated failures, context loss, and claim/tool-result mismatches. |
| 🟠 [Infere](https://infere.com) | - | commercial | OpenAI-compatible gateway plus LLMOps control plane: capability-based model routing, multi-provider fallback, Git-backed prompt repositories, evaluation with regression gates, and per-request traces (no primary OSS repo). |

## Evaluation Frameworks

Test and score LLM/agent output. One thing to sort out before you pick a tool: are you doing **offline/batch** evals (run over a dataset in CI to optimize a prompt) or **inline** evals (score a response live, to gate or block it before it reaches the user)? They're pretty different jobs. Most of the frameworks below are built for the offline case. Live gating usually lands in the [guardrails](#guardrails--safety-monitoring) tools or a platform's online-scoring feature.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [promptfoo](https://github.com/promptfoo/promptfoo) | 26.0k | MIT | Test/eval prompts, agents & RAG; red-teaming and CI/CD. |
| 🟢 [OpenAI Evals](https://github.com/openai/evals) | 19.6k | MIT | Framework + registry of benchmarks for evaluating LLMs. |
| 🟢 [DeepEval](https://github.com/confident-ai/deepeval) | 18.9k | Apache-2.0 | "Pytest for LLMs" - 40+ metrics for LLM output evaluation. |
| 🟢 [Ragas](https://github.com/vibrantlabsai/ragas) | 16.0k | Apache-2.0 | Evaluation toolkit for LLM/RAG applications. |
| 🟢 [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) | 14.2k | MIT | Few-shot benchmark evaluation of language models (EleutherAI). |
| 🟢 [Evidently](https://github.com/evidentlyai/evidently) | 8.0k | Apache-2.0 | ML + LLM observability/eval with 100+ metrics. |
| 🟢 [Giskard](https://github.com/Giskard-AI/giskard-oss) | 5.9k | Apache-2.0 | Open-source eval & testing for LLM agents. |
| 🟢 [Deepchecks](https://github.com/deepchecks/deepchecks) | 4.1k | AGPL-3.0 | Continuous validation/testing for ML & LLM. |
| 🟢 [TruLens](https://github.com/truera/trulens) | 3.6k | MIT | Evaluation & tracking for LLM experiments and agents. |
| 🟢 [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) | 3.0k | MIT | LLM evaluation framework from the UK AI Safety Institute. |
| 🟢 [DeepTeam](https://github.com/confident-ai/deepteam) | 3.0k | Apache-2.0 | Red-teaming framework for LLMs & agents (by the DeepEval team). |
| 🟢 [EvalScope](https://github.com/modelscope/evalscope) | 3.5k | Apache-2.0 | Benchmark and custom evaluation for LLM, VLM and embedding models with a built-in stress-test mode for serving endpoints (ModelScope). |
| 🟢 [lighteval](https://github.com/huggingface/lighteval) | 2.6k | MIT | Hugging Face's evaluation toolkit: runs standard and custom benchmarks across transformers, vLLM and API backends. |
| 🟢 [OpenEvals](https://github.com/langchain-ai/openevals) | 1.2k | MIT | Ready-made evaluators for LLM apps. |
| 🟢 [AutoEvals](https://github.com/braintrustdata/autoevals) | 1.1k | MIT | Library of model-graded and heuristic scorers (factuality, JSON validity, embedding similarity) usable without the Braintrust platform. |
| 🟢 [AgentEvals](https://github.com/langchain-ai/agentevals) | 750 | MIT | Evaluators for agent trajectories: did the agent take the expected tool-call path, with strict or LLM-judged matching. |
| 🟠 [Braintrust](https://github.com/braintrustdata/braintrust-sdk-python) | SDK | Apache-2.0 | Tracing + prompt-centric evals; SDK OSS, platform commercial. |
| 🟠 [Azure AI Evaluation (Foundry)](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/evaluation/azure-ai-evaluation) | SDK | MIT | Microsoft Foundry's evaluation SDK: built-in quality + safety/risk evaluators; runs locally or in Foundry. |
| 🟢 [HELM](https://github.com/stanford-crfm/helm) | 2.9k | Apache-2.0 | Stanford's Holistic Evaluation of Language Models: broad, multi-metric benchmarking. |
| 🟢 [ClawBench](https://github.com/TIGER-AI-Lab/ClawBench) | 1.0k | Apache-2.0 | Live-web benchmark for browser and computer-use agents: isolated runs, request interception and replayable execution traces. |
| 🔵 [agent-qa](https://github.com/vostride/agent-qa) | 906 | FSL-1.1-ALv2 | Natural-language web and mobile regression testing with persistent memory and self-healing execution. |
| 🟢 [continuous-eval](https://github.com/relari-ai/continuous-eval) | 519 | Apache-2.0 | Data-driven, modular evaluation for LLM/RAG pipelines. |
| 🟠 [Galileo](https://github.com/rungalileo/galileo-python) | SDK | Apache-2.0 | Eval + observability platform; SDK OSS, platform commercial. |
| 🟠 [Openlayer](https://github.com/openlayer-ai/openlayer-python) | SDK | Apache-2.0 | Testing, eval & monitoring platform; SDK OSS, platform commercial. |
| 🟠 [TestMu AI Agent Testing](https://www.testmuai.com/agent-testing/) | - | commercial | Tests chat, voice and phone agents with simulated conversations and real phone calls; validates tool calls from Vapi, Retell, ElevenLabs and Agentforce. |

## Prompt Management & Experimentation

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [Agenta](https://github.com/Agenta-AI/agenta) | 4.8k | MIT | LLMOps platform: prompt playground, versioning, eval & observability. |
| 🟢 [Pezzo](https://github.com/pezzolabs/pezzo) | 3.3k | Apache-2.0 | Developer-first prompt design, versioning & observability. |
| 🟠 [PromptLayer](https://github.com/MagnivOrg/prompt-layer-library) | 784 | Apache-2.0 | Log, track, debug & replay prompts and LLM requests. |

> Langfuse and Agenta also provide strong prompt management - listed once under their best-fit category.

## LLM Gateways & Proxies

Route to many providers through one endpoint; get logging, cost tracking & caching for free.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [LiteLLM](https://github.com/BerriAI/litellm) | 61.3k | MIT | Python SDK + proxy calling 100+ LLMs with unified cost tracking & logging. |
| 🟢 [Portkey Gateway](https://github.com/Portkey-AI/gateway) | 13.2k | MIT | Fast AI gateway routing to 1,600+ LLMs with built-in guardrails & observability. |
| 🟢 [Helicone](https://github.com/Helicone/helicone) | 6.2k | Apache-2.0 | Proxy-first observability (also listed under Tracing). |
| 🟠 Cloudflare AI Gateway | - | commercial | Managed AI gateway with analytics/logging/caching (no OSS repo). |
| 🟠 OpenRouter | - | commercial | Unified API/marketplace routing to many LLMs with usage analytics. |
| 🟢 [Bifrost](https://github.com/maximhq/bifrost) | 8.8k | Apache-2.0 | Fast AI gateway routing to 1,000+ models with logging, cost tracking & governance. |
| 🟢 [Kong AI Gateway](https://github.com/Kong/kong) | 44.3k | Apache-2.0 | AI plugins for the Kong API gateway: multi-provider proxying, token-based rate limiting, prompt guards and request/response logging. |
| 🟢 [Higress](https://github.com/higress-group/higress) | 9.6k | Apache-2.0 | Envoy-based AI-native API gateway from Alibaba: provider routing, token rate limits, caching and OTel tracing for LLM traffic. |
| 🟢 [Agent Router (Envoy AI Gateway)](https://github.com/theagentrouter/agent-router) | 2.2k | Apache-2.0 | Envoy Gateway extension for unified access to LLM providers with token-aware rate limiting and usage metrics. |

## Instrumentation & Standards (OpenTelemetry GenAI)

The observability layer is standardizing on **OpenTelemetry** - emit these and your traces export to *any* OTel backend.

Two things changed in 2025-26 that older tutorials miss: the GenAI conventions moved out of the main semconv repo into their own, and `gen_ai.system` was renamed `gen_ai.provider.name`, with prompt/completion content moving from span events to the opt-in `gen_ai.input.messages` / `gen_ai.output.messages` attributes. The spec also now covers agent spans, tool calls and MCP.

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [OpenLLMetry](https://github.com/traceloop/openllmetry) | 7.5k | Apache-2.0 | OTel-based open-source observability for GenAI/LLM apps (Traceloop). |
| 🟢 [OpenInference](https://github.com/Arize-ai/openinference) | 1.3k | Apache-2.0 | OpenTelemetry instrumentation for AI observability (Arize). |
| 🟢 [OTel Python Contrib](https://github.com/open-telemetry/opentelemetry-python-contrib) | 1.1k | Apache-2.0 | OTel instrumentation modules, including GenAI. |
| 🟢 [OTel GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai) | 449 | Apache-2.0 | The **GenAI semantic conventions** spec (`gen_ai.*` spans, metrics, events, agent and MCP conventions), now in its own repo with a Python reference implementation. |
| 🟢 [OpenLLMetry-JS](https://github.com/traceloop/openllmetry-js) | 412 | Apache-2.0 | The TypeScript sibling of OpenLLMetry: OTel instrumentations for the OpenAI, Anthropic, Bedrock, LangChain and LlamaIndex Node SDKs. |

## Guardrails & Safety Monitoring

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🟢 [Guardrails AI](https://github.com/guardrails-ai/guardrails) | 7.5k | Apache-2.0 | Add input/output guardrails and structured validation to LLMs. |
| 🟢 [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) | 7.3k | Apache-2.0 | Programmable guardrails for LLM conversational systems (NVIDIA). |
| 🟢 [Presidio](https://github.com/data-privacy-stack/presidio) | 11.3k | MIT | PII detection, redaction & anonymization; the standard for scrubbing prompts and traces. |
| 🟢 [garak](https://github.com/NVIDIA/garak) | 9.6k | Apache-2.0 | LLM vulnerability scanner: probes for prompt injection, jailbreaks & data leakage (NVIDIA). |
| 🔵 [Failproof](https://github.com/FailproofAI/failproofai) | 5.5k | MIT (open-core) | Learns failure modes from agent traces and turns them into enforceable policies. |
| 🟢 [PyRIT](https://github.com/microsoft/PyRIT) | 4.6k | MIT | Microsoft's risk-identification toolkit: automated multi-turn red-teaming of GenAI systems with pluggable attack strategies and scorers. |
| 🟢 [Purple Llama](https://github.com/meta-llama/PurpleLlama) | 4.4k | mixed (Llama / MIT) | Meta's LLM security toolset: Llama Guard input/output classifiers, Prompt Guard for injection, and the CyberSecEval benchmarks. |

## Self-Hosted / Open-Source First

Need data residency / on-prem? These ship a genuinely self-hostable OSS core:
[Langfuse](https://github.com/langfuse/langfuse) (MIT) · [Arize Phoenix](https://github.com/Arize-ai/phoenix) · [Comet Opik](https://github.com/comet-ml/opik) (Apache-2.0) · [Helicone](https://github.com/Helicone/helicone) (Apache-2.0) · [OpenLIT](https://github.com/openlit/openlit) (Apache-2.0) · [PostHog](https://github.com/PostHog/posthog) (MIT, open-core) · [LangWatch](https://github.com/langwatch/langwatch) (Apache-2.0) · [MLflow](https://github.com/mlflow/mlflow) (Apache-2.0) · [Evidently](https://github.com/evidentlyai/evidently) (Apache-2.0) · [SigNoz](https://github.com/SigNoz/signoz) (open-core, OTel-native).

## Research & Benchmarks

The tooling above is grounded in a fast-moving literature. Key anchors:

- **LLM-as-a-Judge** - Zheng et al., 2023, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena* ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)) - the basis for scalable, model-graded evaluation used by most eval tools.
- **HELM** - Liang et al., *Holistic Evaluation of Language Models* ([arXiv:2211.09110](https://arxiv.org/abs/2211.09110)) - canonical multi-metric evaluation.
- **SelfCheckGPT** - Manakul et al., 2023 ([arXiv:2303.08896](https://arxiv.org/abs/2303.08896)) - reference-free hallucination detection.
- **G-Eval** - Liu et al., 2023 ([arXiv:2303.16634](https://arxiv.org/abs/2303.16634)) - chain-of-thought, form-filling judge prompts; the template most "LLM-as-a-judge" metrics in the eval tools above are built on.
- **Ragas** - Es et al., 2023 ([arXiv:2309.15217](https://arxiv.org/abs/2309.15217)) - reference-free faithfulness / answer relevance / context precision for RAG, the metric set that became the Ragas library.
- **Prometheus 2** - Kim et al., 2024 ([arXiv:2405.01535](https://arxiv.org/abs/2405.01535)) - an open-weight judge model, for when sending evaluation traffic to a closed API is not an option.
- **τ-bench** - Yao et al., 2024 ([arXiv:2406.12045](https://arxiv.org/abs/2406.12045)) - tool-agent-user benchmark whose pass^k metric exposes how unreliable agents are across repeated runs of the same task.
- **Agent hallucination** - *MIRAGE-Bench* ([arXiv:2507.21017](https://arxiv.org/abs/2507.21017)); paper list: [EdinburghNLP/awesome-hallucination-detection](https://github.com/EdinburghNLP/awesome-hallucination-detection).
- **OTel GenAI semantic conventions** - the observability standard (see [Instrumentation & Standards](#instrumentation--standards-opentelemetry-genai)).

## Learning Resources

- [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md) - the standard for LLM telemetry; the old opentelemetry.io pages now just redirect here.
- [Arize Phoenix docs](https://docs.arize.com/phoenix) & [Langfuse docs](https://langfuse.com/docs) - practical tracing/eval concepts.
- Hamel Husain - [*Your AI Product Needs Evals*](https://hamel.dev/blog/posts/evals/).
- Hamel Husain & Shreya Shankar - [*Frequently Asked Questions (And Answers) About AI Evals*](https://hamel.dev/blog/posts/evals-faq/) - error analysis before metrics, binary over Likert, calibrate judges on human labels.
- Eugene Yan - [*Patterns for Building LLM-based Systems & Products*](https://eugeneyan.com/writing/llm-patterns/) - evals, RAG, guardrails, caching and monitoring as one connected design.
- Applied LLMs - [*What We've Learned From A Year of Building with LLMs*](https://applied-llms.org/) - six practitioners' operational lessons, including why evals and tracing are where most teams under-invest.
- Chip Huyen - [*Building LLM applications for production*](https://huyenchip.com/2023/04/11/llm-engineering.html).
- Loop & Retry - [*Measuring agent failure in production*](https://loopandretry.github.io/posts/measuring-agent-failure-in-production/) - which signals actually surface a broken agent in prod, and why request-level success rates hide the failures that matter.

## Guides & Tools (Original)

Original work in this repo, not just curated links:

- 🧰 **[Agent Skills](skills/)** - 26 ready-to-run workflows (instrument, evals, debug-from-traces, guardrails, PII-safe tracing, tool selection).
- 📖 **[LLM Observability for Finance & Regulated Industries](guides/llm-observability-for-finance.md)** - a guide for teams where observability is a *compliance control*, not a dashboard.
- 🛠️ **[`genai_trace.py`](tools/genai_trace.py)** - a minimal vendor-neutral OpenTelemetry GenAI tracer with a PII-redaction hook.

## How to Choose

- **Just need traces + cost, minimal code?** Start with a **gateway/proxy** (change base URL, zero SDK) or a tracing platform with OTel auto-instrumentation.
- **Need to *test* quality, not just watch it?** Add an **evaluation framework** (offline eval in CI + online LLM-as-a-judge).
- **Data residency / on-prem required?** Pick from [Self-Hosted](#self-hosted--open-source-first).
- **Want vendor-neutral, future-proof traces?** Emit **OTel GenAI semantic conventions** so you can swap backends.

A common production setup pairs a **gateway** (cost + routing) with an **evaluation tool** (quality) on top of an **OTel-native tracing** backbone.

### What it actually costs to run (self-hosted)

The feature tables above don't tell you what you're signing up to operate, and that's usually the
thing that decides it. Roughly three tiers:

| Tier | Backing services | Notes |
|---|---|---|
| **Single process** | SQLite or one Postgres | Phoenix, MLflow. One container, no OLAP store. Easiest to run. |
| **Postgres-class** | Postgres (+ object storage for artifacts) | MLflow with a tracking server, Latitude. Ordinary web-app operations. |
| **OLAP-class** | ClickHouse + Postgres + Redis/Valkey + S3-compatible blob storage | Langfuse v3/v4, Opik, Helicone, SigNoz. Four moving parts, not one. |

**Why ClickHouse keeps showing up:** high-volume span ingest with analytical queries over it is a
column-store workload, and Postgres degrades on it. It's driven by *tracing* throughput, not by
evals - if you don't need tracing, the whole tier is avoidable. ClickHouse is a hard requirement
for self-hosted Langfuse; there's no Postgres-only mode.

**Is a single, non-replicated ClickHouse enough?** For development and low-volume production,
yes - it runs fine on one node, and that's what the docker-compose quickstarts give you
(`CLICKHOUSE_CLUSTER_ENABLED=false`). Understand what you're trading: a single node has no
redundancy, so node loss means trace loss, which is why Langfuse labels single-container Docker
development-only rather than slow. For production they suggest 3 ClickHouse replicas plus 3
Keeper nodes, ~2 CPU / 8-16 GiB each. Disk is the thing that bites - observability data grows
fast, so set a retention policy on day one and use a volume you can expand.

**If that's more than you want to operate:** stay in the single-process tier (Phoenix for
tracing + evals, MLflow if you're already on it), or run evals in CI with a framework that keeps
no server at all and reach for a hosted backend only when you actually need trace history.

Versions move - check the self-hosting docs before you size anything.

## Contributing

Contributions welcome - see [`CONTRIBUTING.md`](CONTRIBUTING.md). Add a tool via PR with: name, link, one-line **neutral** description, correct category, and the OSS/commercial marker. Keep it factual and non-promotional - a wrong entry or dead link discredits the whole list.

## License

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](LICENSE)

To the extent possible under law, the contributors have waived all copyright and related rights to this work.
