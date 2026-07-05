---
name: measure-agent-task-success
description: Use this to measure whether an AI agent actually completed its task end to end, not just whether individual LLM calls looked fine. Trigger on "is my agent working", "measure agent success rate", "evaluate my agent", "how good is my agent", "agent completion rate", or evaluating a multi-step/tool-using agent. Score the outcome of the whole task, plus the path it took.
license: CC0-1.0
---

# Measure agent task success

A chatbot is judged per response; an *agent* is judged on whether it finished the job. An agent can produce great-looking individual steps and still fail the task (wrong final state, gave up, looped, took a destructive action). Measure at the task level.

## Score the outcome first, then the path

**Outcome (did it succeed?)** - the primary metric:
- **Task success rate:** did the agent reach the correct end state? Define "success" concretely per task type (the ticket was resolved, the code passed tests, the correct record was updated, the right answer with the right action taken).
- Prefer a **checkable** success signal where possible (tests pass, DB in expected state, API returned expected result) over a judged one. For open-ended tasks, use an LLM-as-judge against a rubric, calibrated.

**Path (how well did it get there?)** - the diagnostic metrics:
- **Steps / tool calls to completion** (efficiency; blowups mean loops or confusion).
- **Tool-call success rate** (did tools get called with valid args and succeed?).
- **Cost + latency per task** (rolled up across all the agent's calls).
- **Recovery:** did it recover from a tool error, or fail/loop?

## Build the eval

1. **A task dataset**, not a prompt dataset: each item is a full task with a defined success condition (see `build-eval-dataset`). Pull real tasks from production traces (`trace-based-testing`).
2. **Run the agent end to end** in a sandbox; score outcome (checkable or judged) + path metrics.
3. **Read failures via the trace** (`trace-multi-agent-system`, `debug-agent-from-traces`): find the step where it diverged. Success rate tells you *how often*; the trace tells you *why*.
4. **Gate in CI** on success rate, and monitor it online on real tasks (`set-up-drift-alerts`).

## Verify

- You can state a single number: task success rate on your task set.
- Failures are attributable to a step via the trace, not a mystery.
- Path metrics (steps, cost, tool success) are tracked, so a "successful but wildly inefficient" agent is visible.

## Anti-patterns

- Judging only the final text output, never the actual end state (the agent "said" it booked the flight but did not).
- Per-LLM-call quality as your only metric (each step fine, task still failed).
- No cap/measure on steps (a looping agent looks "busy," not broken).
- Judging success by vibes instead of a checkable condition where one exists.

## Grounding

Agentic evaluation emphasizes end-to-end task success and trajectory, as in agent benchmarks like SWE-bench (Jimenez et al., [arXiv:2310.06770](https://arxiv.org/abs/2310.06770)), WebArena ([arXiv:2307.13854](https://arxiv.org/abs/2307.13854)), and AgentBench ([arXiv:2308.03688](https://arxiv.org/abs/2308.03688)) - all score whether the task was completed, not just intermediate output.
