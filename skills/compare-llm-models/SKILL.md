---
name: compare-llm-models
description: Use this to pick or switch the LLM behind a feature, based on evidence instead of hype or the newest release. Trigger on "which model should I use", "is GPT/Claude/Gemini/Llama better for this", "should I switch models", "can a cheaper model do this", "compare models for my use case". Evaluate on YOUR task, not on leaderboards alone.
license: CC0-1.0
---

# Compare LLM models for your task

The best model on a public leaderboard is often not the best model for *your* task at *your* cost and latency. Public benchmarks narrow the field; your own eval set makes the call.

## Use benchmarks to shortlist, not to decide

- **General leaderboards** (Chatbot Arena / LMArena for human preference, HELM for multi-metric, MMLU/GPQA for reasoning) tell you the rough tier a model is in. Use them to pick 2-4 candidates, not to declare a winner for your app.
- **Watch for contamination and overfitting** to popular benchmarks. A high MMLU score does not mean the model is good at your specific extraction/RAG/agent task.
- **Task-relevant benchmarks** beat general ones: if you do code, look at code evals; if RAG, look at long-context/faithfulness; if tools, look at agent/tool-use benchmarks.

## Then evaluate the shortlist on YOUR eval set

This is the part that actually decides it. Run each candidate model through your own eval suite (see `build-eval-dataset` and `add-llm-evals`) and compare on the axes that matter:

| Axis | How to measure |
|---|---|
| **Quality** | Your eval scores on your dataset (not a leaderboard) |
| **Cost** | Tokens x price on your real prompts (see `reduce-llm-cost`) |
| **Latency** | p50/p95 on your prompt sizes |
| **Reliability** | Structured-output adherence, refusal rate, error rate |
| **Context/limits** | Context window, rate limits, region/availability |
| **Fit** | Tool-calling quality, multilingual, safety, data-residency terms |

Run it as an apples-to-apples eval: same inputs, same rubric, same judge. Report a small table, not a vibe.

## Decide

- Pick the cheapest/fastest model that clears your quality bar, not the highest absolute quality. Most tasks do not need the frontier model.
- Consider **routing**: cheap model for easy calls, frontier model for hard ones (a gateway makes this easy).
- Re-run this when a provider ships a new model, but gate switches behind the eval, model upgrades sometimes regress *your* task even when the leaderboard goes up.

## Verify

- You have a table comparing candidates on quality + cost + latency for your task.
- The decision is defensible from that table, not from "it is the newest."
- Switching is behind an eval gate so a regression is caught before shipping.

## Anti-patterns

- Choosing by leaderboard rank alone (leaderboards are not your task).
- Switching to the newest model without re-running evals (silent regressions).
- Comparing quality while ignoring the 5x cost/latency difference.
- One-off manual spot-check instead of a repeatable eval.

## Grounding

Human-preference evaluation: Chatbot Arena, Zheng et al. 2023 ([arXiv:2306.05685](https://arxiv.org/abs/2306.05685)). Multi-metric holistic evaluation: HELM, Liang et al. ([arXiv:2211.09110](https://arxiv.org/abs/2211.09110)). Benchmark harness: [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness).
