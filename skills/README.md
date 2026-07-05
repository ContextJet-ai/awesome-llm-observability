# Skills — by [ContextJet.ai](https://www.contextjetai.com)

Original, batteries-included [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) for putting the tools in this list to work. Drop a folder into your agent's skills directory (e.g. `.claude/skills/`) and your coding agent gains the workflow.

| Skill | Use it to… |
|---|---|
| [`instrument-llm-observability`](instrument-llm-observability/SKILL.md) | Add production tracing (OTel GenAI or a platform SDK) to an LLM/agent app. |
| [`add-llm-evals`](add-llm-evals/SKILL.md) | Add an offline (CI) + online (LLM-as-a-judge) evaluation suite, with calibration. |
| [`debug-agent-from-traces`](debug-agent-from-traces/SKILL.md) | Diagnose *why* an agent gave a wrong/empty/slow/expensive result, from its trace. |
| [`add-llm-guardrails`](add-llm-guardrails/SKILL.md) | Add input/output guardrails (injection, PII, schema, safety) — and observe them. |
| [`redact-pii-for-tracing`](redact-pii-for-tracing/SKILL.md) | Add compliant tracing for finance/regulated apps without leaking PII. |
| [`choose-observability-stack`](choose-observability-stack/SKILL.md) | Recommend the right observability/eval tool for a given set of constraints. |

Each skill follows Anthropic's authoring best practices — a focused `SKILL.md`, progressive disclosure via `references/`, and actionable checklists. New-skill contributions welcome; see [`../CONTRIBUTING.md`](../CONTRIBUTING.md).
