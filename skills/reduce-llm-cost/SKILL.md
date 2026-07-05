---
name: reduce-llm-cost
description: Use this to cut the cost of an LLM app using observability data. Trigger on "my OpenAI/Anthropic bill is too high", "reduce token usage", "the app is expensive", "optimize LLM cost", "why am I spending so much on the API". Find the expensive spans first (measure), then apply the cheapest wins. Don't guess - the trace tells you where the money goes.
license: CC0-1.0
---

# Reduce LLM cost (measure first)

Most LLM bills are dominated by a few patterns you can *see* in traces. Measure before optimizing - the biggest cost is rarely where people assume.

## Step 1 - find where the money goes

From your observability tool, sort spans by cost (or `input_tokens`). You're looking for:

- **The highest-token spans** - usually bloated context or a whole chat history re-sent every turn.
- **Retry storms** - the same call repeated N times (rate limits / transient errors) multiplying cost.
- **The most-frequent call** × its per-call cost - a cheap call made 10,000×/day beats one expensive call.
- **Model overkill** - using a frontier model for a task a small/cheap model handles fine.

If you have no cost data yet, add tracing first (see `instrument-llm-observability`) - you can't optimize what you can't see.

## Step 2 - apply wins, cheapest-effort first

1. **Right-size the model.** Route easy calls (classification, extraction, routing) to a small/cheap model; reserve the frontier model for hard reasoning. Biggest lever for most apps.
2. **Trim the context.** Stop re-sending the full history/system prompt every turn. Send only what's needed; summarize old turns. For RAG, retrieve fewer/better chunks, not more.
3. **Cache.** Enable prompt caching (Anthropic/OpenAI) for stable prefixes; cache identical requests (a gateway like Helicone/Portkey/LiteLLM does this for free).
4. **Cap `max_tokens`.** Unbounded outputs cost unbounded money; set a sane ceiling.
5. **Fix retry storms.** Cap retries + honor `Retry-After`; a backoff bug can 10× cost silently.
6. **Batch / async** where the API supports it (batch endpoints are often ~50% cheaper).
7. **Shorten prompts.** Few-shot examples and verbose instructions are pure input-token cost - trim to what actually changes behavior (measure with an eval so quality holds).

## Step 3 - protect quality while cutting

Every cost cut is a potential quality regression. Gate changes with an **eval suite** (see `add-llm-evals`): make the cheap change, run evals, keep it only if quality holds. Then **watch cost + quality together** on a dashboard so a future change doesn't silently trade one for the other.

## Quick math to prioritize

`monthly_cost_of_a_span = per_call_tokens × price × calls_per_month`. Optimize the span with the biggest product, not the one that *looks* expensive per call.

## Anti-patterns

- Optimizing the model choice while ignoring a 20k-token context that's the real cost.
- Cutting cost with no eval → shipping a cheaper, worse app you find out about from users.
- Turning off logging "to save money" (observability cost is tiny vs the model bill it helps you cut).
