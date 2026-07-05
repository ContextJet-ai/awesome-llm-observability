---
name: trace-multi-agent-system
description: Use this to add observability to a multi-agent or agentic system (multiple agents, sub-agents, tool loops, handoffs). Trigger on "trace my agents", "my agent crew is a black box", "which agent failed", "debug my LangGraph/CrewAI/AutoGen/agent workflow", "the agents loop forever". Get a clear span tree across agents and tool calls so you can see who did what.
license: CC0-1.0
---

# Trace a multi-agent system

Multi-agent systems fail in ways single calls do not: an agent hands off bad state, a tool loop never terminates, a sub-agent silently fails and the orchestrator carries on. You cannot debug that from the final output. You need the full tree of who called whom.

## Get the structure right

Model the run as a nested span tree:

- **One root span** per user request or task.
- **One span per agent turn** (which agent, its role, its input state).
- **Child spans** for each tool call, retrieval, and LLM call inside that turn.
- **Handoff spans / events** when one agent passes control or state to another (record what was passed).

Most agent frameworks emit this if you turn on their tracing (LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, LlamaIndex) or add OpenTelemetry instrumentation (OpenLLMetry, OpenInference auto-instrument several agent frameworks). Prefer the framework's built-in tracing, then fill gaps with manual spans (see `instrument-llm-observability`).

## What to capture per agent

- **Identity + role** (`agent.name`, `agent.role`) so spans are attributable.
- **Input state and output** at each handoff (the #1 source of multi-agent bugs is corrupted or lost state between agents).
- **Tool calls** with args + results + errors.
- **Loop/iteration count** so runaway loops are visible.
- **Tokens + latency + cost per agent** (rolled up to the whole run) so you can see which agent is the expensive/slow one.

## Debug the common failures

| Symptom | Look at |
|---|---|
| Wrong final result | Walk the tree to the first agent whose output diverges from intent. Fix there. |
| Infinite / long loops | Iteration counts + repeated identical tool spans. Add a max-iterations guard. |
| One agent "did nothing" | A missing or errored subtree. A swallowed exception in a sub-agent. |
| Blows the budget | Per-agent token rollup. Usually one agent re-sending full context each turn. |
| Non-deterministic flakiness | Compare two traces of the same input side by side. |

## Verify

- Run one task and confirm the trace shows every agent turn, every tool call, and every handoff, nested correctly.
- Confirm per-agent cost + latency roll up to a run total.
- Break a sub-agent on purpose and confirm the failure is visible in the tree (not swallowed).

## Anti-patterns

- Logging only the orchestrator, so sub-agent behavior is invisible.
- No handoff/state capture, so you cannot tell where state got corrupted.
- No iteration count, so a runaway loop just looks like "it is slow and expensive."
- Treating a multi-agent bug as a prompt bug when it is really a state-passing bug between agents.
