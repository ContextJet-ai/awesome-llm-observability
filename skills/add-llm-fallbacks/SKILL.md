---
name: add-llm-fallbacks
description: Use this to make an LLM app resilient to provider failures, rate limits, timeouts, and outages. Trigger on "handle LLM API errors", "add retries/fallbacks", "the app breaks when OpenAI is down", "rate limit errors", "make my LLM calls reliable", "timeout handling". Add retries, timeouts, and model/provider fallbacks, and observe them so failures are visible.
license: CC0-1.0
---

# Add LLM fallbacks and resilience

LLM providers rate-limit, time out, 500, and occasionally go down. A single unguarded call means your app goes down with them. Add layered resilience, and instrument it so you can see when it kicks in.

## The layers (add all of them)

1. **Timeouts.** Every call needs a sane timeout. An unbounded call can hang a request forever. Set it based on your p95 latency plus headroom.
2. **Retries with backoff.** Retry transient failures (429, 500, 503, timeouts) with *exponential backoff + jitter*. Cap the number of retries and cap the total wait, and honor `Retry-After` when present. A naive retry loop turns a rate limit into a retry storm (and a big bill, see `reduce-llm-cost`).
3. **Do not retry non-transient errors.** 400s (bad request), auth errors, and content-policy refusals will fail again. Retrying them wastes time and money.
4. **Model / provider fallback.** If the primary model errors or is down, fall back to a secondary (same provider different model, or a different provider). A gateway (LiteLLM, Portkey) gives you this with config instead of code.
5. **Graceful degradation.** When everything fails, return a sensible fallback (cached answer, a "try again shortly" message, a simpler non-LLM path) instead of a stack trace.

## Instrument it (so resilience is not invisible)

The failure mode of good resilience is that it hides problems. Emit telemetry so you still see them:

- A span/event when a **retry** happens (and how many).
- A span/event when a **fallback** fires (primary -> secondary).
- **Error rate per provider/model** and **fallback rate** on a dashboard, with alerts (see `set-up-drift-alerts`).

If your fallback rate silently climbs to 30%, you want to know, not find out from the bill or a user.

## Watch the cost/quality of fallbacks

A fallback model may be cheaper-but-worse or pricier. Track cost and (ideally) quality on the fallback path too, so a provider outage does not silently degrade your app for hours.

## Verify

- Kill the primary provider (bad key / block the host) and confirm the app fails over, not over.
- Simulate a 429 and confirm backoff + `Retry-After` are honored, with a capped total wait.
- Confirm retries and fallbacks show up in traces/metrics.

## Anti-patterns

- No timeout (one hung call ties up a worker).
- Retrying 4xx/auth/policy errors (they will not succeed; you just wait and pay).
- Fixed-delay retries with no cap (retry storm on a rate limit).
- Silent fallbacks with no telemetry (you are degraded and blind to it).
- A fallback model nobody evaluated (you fail over into worse answers).

## Grounding

Standard distributed-systems resilience patterns applied to LLM calls: exponential backoff with jitter (AWS Architecture guidance), retry/timeout/circuit-breaker (Nygard, *Release It!*). Gateways implement provider fallback: [LiteLLM](https://github.com/BerriAI/litellm), [Portkey](https://github.com/Portkey-AI/gateway).
