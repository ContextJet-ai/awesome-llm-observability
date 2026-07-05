---
name: estimate-llm-cost
description: Use this to estimate what an LLM call or feature will cost, and to compare models on price, before or after shipping. Trigger on "how much will this cost", "estimate my OpenAI/Anthropic bill", "is a cheaper model worth it", "cost of this prompt", "project my LLM spend". Ships a runnable, tested calculator so the numbers are real, not hand-waved.
license: CC0-1.0
---

# Estimate LLM cost

Cost surprises come from not doing the arithmetic. This skill ships a small, dependency-free calculator so you can price a call, project a monthly bill, and compare models with actual numbers.

## Use the bundled script

[`scripts/llm_cost.py`](scripts/llm_cost.py) is pure Python, no install needed:

```python
from llm_cost import estimate_cost, project_monthly

estimate_cost(1500, 300, model="gpt-4o")                       # one call, USD
project_monthly(1500, 300, calls_per_day=5000, model="gpt-4o") # monthly projection
estimate_cost(2000, 200, model="gpt-4o", cached_input_tokens=1800)  # with prompt caching
```

Run it directly to see a worked example: `python scripts/llm_cost.py`.

Prices in the `PRICES` table are approximate and change often, so pass `input_price`/`output_price` explicitly when you need exact figures, or edit the table. The arithmetic (not the price table) is what the tests pin down.

## How to apply it

1. **Price the call** with realistic token counts (measure them from a trace, see `instrument-llm-observability`).
2. **Project the bill** with your real call volume. A cheap call at 10k/day beats an expensive one at 10/day.
3. **Compare models** by running the same tokens through two model ids. Pick the cheapest that still passes your evals (see `compare-llm-models`).
4. **Feed it into cost cutting** (see `reduce-llm-cost`).

## Validation

Run the tests: `pytest skills/estimate-llm-cost/tests/`. They check the math is exact for explicit prices, that model lookups match the table, that prompt-cache discounting is correct, and that monthly projection scales linearly.

## Anti-patterns

- Trusting the built-in price table as current (verify against provider pricing).
- Pricing one call and forgetting to multiply by real volume.
- Comparing models on price without checking quality holds on your eval set.
