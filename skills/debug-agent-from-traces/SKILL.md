---
name: debug-agent-from-traces
description: Use this to diagnose WHY an LLM agent or chain produced a wrong, empty, slow, or expensive result, by reading its observability trace. Trigger on "my agent gave the wrong answer", "the chain returned nothing", "why is this so slow/expensive", "debug this trace/run", or when a trace tree is available. Walk the span tree systematically instead of guessing.
license: CC0-1.0
---

# Debug an agent from its trace

A trace is a tree of spans (parent request → LLM/tool/retrieval children). Most agent failures are visible in it if you read it in the right order. Don't guess from the final output - walk the tree.

## Triage by symptom

| Symptom | Look here first |
|---|---|
| **Wrong answer** | The LLM span *just before* the bad output: was the prompt/context correct? Then the retrieval span that fed it. |
| **Empty / truncated output** | `finish_reason` (length? content_filter?), `max_tokens`, and any span that raised an exception then got swallowed. |
| **Hallucinated facts** | Retrieval spans - were the right docs retrieved (check scores/IDs)? If not, it's a retrieval bug, not an LLM bug. |
| **Too slow** | Span durations - find the critical path. Usually one slow retrieval, a serial loop that should be parallel, or a huge context. |
| **Too expensive** | Token counts per LLM span - find the span with the largest `input_tokens` (usually bloated context or a retry storm). |
| **Silent failure** | A span with an error/exception that was caught and returned empty. A missing subtree = a step that never ran. |

## The systematic walk

1. **Start at the root**, confirm the user input is what you expect.
2. **Follow to the first LLM call.** Read the *actual* rendered prompt + context (not the template). Most "model is dumb" bugs are actually "we fed it the wrong context".
3. **Check each tool/retrieval span** in order: inputs correct? output sane? error?
4. **Find the divergence point** - the first span where reality differs from intent. Fix *there*, not at the output.
5. **Check token + latency** on every LLM span to catch cost/perf issues even when the answer is right.

## Common root causes (in order of frequency)

- **Wrong/empty retrieved context** → the LLM was set up to fail. (Retrieval bug.)
- **Prompt/template rendering bug** → a variable didn't interpolate; context is blank or duplicated.
- **Swallowed exception** → a `try/except` that logs and returns empty, dropping context or output silently. Grep for these.
- **Retry storm** → the same call repeated N times (rate limit / transient error) inflating cost + latency.
- **Context bloat** → the whole history re-sent each turn; `input_tokens` grows every step.

## Turn the fix into a regression test

Once you find the divergence, capture that input as an **eval case** (see the `add-llm-evals` skill) so the bug can't come back. Debugging a trace and *not* adding a test means you'll debug it again next month.

## Anti-patterns

- Re-prompting the model when the real bug is upstream retrieval/rendering.
- Reading only the final output and inferring the cause.
- Fixing the symptom without adding a regression test.
