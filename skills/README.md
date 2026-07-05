# Skills - by [ContextJet.ai](https://www.contextjetai.com)

22 original, batteries-included [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) for putting the tools in this list to work. They auto-trigger when you ask your coding agent to add tracing, cut cost, debug an agent, and so on.

## Install (about 10 seconds)

```
# Claude Code plugin (easiest)
/plugin marketplace add ContextJet-ai/awesome-llm-observability
/plugin install llm-observability@contextjet
```
```bash
# or copy the skills into any agent's skills folder
npx degit ContextJet-ai/awesome-llm-observability/skills ~/.claude/skills
# or: git clone the repo and run ./install.sh
```

## The skills

| Skill | Use it to… |
|---|---|
| [`instrument-llm-observability`](instrument-llm-observability/SKILL.md) | Add production tracing (OTel GenAI or a platform SDK) to an LLM/agent app. |
| [`add-llm-evals`](add-llm-evals/SKILL.md) | Add an offline (CI) + online (LLM-as-a-judge) evaluation suite, with calibration. |
| [`eval-driven-development`](eval-driven-development/SKILL.md) | Write evals first and iterate against them (TDD for LLMs). |
| [`build-eval-dataset`](build-eval-dataset/SKILL.md) | Build an eval set that reflects production. |
| [`optimize-prompts`](optimize-prompts/SKILL.md) | Improve a prompt systematically against an eval set. |
| [`debug-agent-from-traces`](debug-agent-from-traces/SKILL.md) | Diagnose *why* an agent gave a wrong/empty/slow/expensive result, from its trace. |
| [`trace-based-testing`](trace-based-testing/SKILL.md) | Turn production traces into a regression suite. |
| [`collect-user-feedback`](collect-user-feedback/SKILL.md) | Capture feedback, attach to traces, feed back into evals. |
| [`annotate-traces-for-review`](annotate-traces-for-review/SKILL.md) | Human review + error analysis of traces. |
| [`reduce-llm-cost`](reduce-llm-cost/SKILL.md) | Cut your LLM bill using observability data. |
| [`add-llm-fallbacks`](add-llm-fallbacks/SKILL.md) | Timeouts, backoff, provider fallback, all observed. |
| [`monitor-rag-quality`](monitor-rag-quality/SKILL.md) | Measure + fix RAG quality (retrieval vs generation). |
| [`detect-hallucinations`](detect-hallucinations/SKILL.md) | Detect fabricated answers (self-consistency, semantic entropy, faithfulness). |
| [`trace-multi-agent-system`](trace-multi-agent-system/SKILL.md) | Add observability to a multi-agent / agentic system. |
| [`measure-agent-task-success`](measure-agent-task-success/SKILL.md) | Measure whether an agent completed the task end to end. |
| [`set-up-drift-alerts`](set-up-drift-alerts/SKILL.md) | Catch quality/cost/latency/input drift in production. |
| [`set-up-ab-testing`](set-up-ab-testing/SKILL.md) | Canary/A-B a prompt/model change on real traffic. |
| [`add-llm-guardrails`](add-llm-guardrails/SKILL.md) | Add input/output guardrails (injection, PII, schema, safety) and observe them. |
| [`red-team-llm-app`](red-team-llm-app/SKILL.md) | Adversarially test for injection, jailbreaks & tool misuse (OWASP LLM Top 10). |
| [`compare-llm-models`](compare-llm-models/SKILL.md) | Pick/switch models on evidence (your eval set), not leaderboards. |
| [`redact-pii-for-tracing`](redact-pii-for-tracing/SKILL.md) | Compliant tracing for finance/regulated apps without leaking PII. |
| [`choose-observability-stack`](choose-observability-stack/SKILL.md) | Recommend the right tool for a given set of constraints. |

Each skill follows Anthropic's authoring best practices (a focused `SKILL.md`, progressive disclosure via `references/`, actionable checklists). New-skill contributions welcome; see [`../CONTRIBUTING.md`](../CONTRIBUTING.md).
