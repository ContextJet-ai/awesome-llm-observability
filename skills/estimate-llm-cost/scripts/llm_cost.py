"""
llm_cost - estimate and project LLM API cost from token counts.

Pure-Python, zero dependencies. Prices are approximate USD per 1M tokens and
change often; pass explicit prices (or edit PRICES) for accuracy. The math is
what's tested, not the price table.

    from llm_cost import estimate_cost, project_monthly

    estimate_cost(1500, 300, model="gpt-4o")          # one call
    project_monthly(1500, 300, calls_per_day=5000, model="gpt-4o-mini")

CC0 - ContextJet.ai.
"""

from __future__ import annotations

# USD per 1M tokens: (input, output). Approximate - override for accuracy.
PRICES = {
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "claude-opus-4": (15.00, 75.00),
    "claude-sonnet-4": (3.00, 15.00),
    "claude-haiku-4": (0.80, 4.00),
    "gemini-2.5-pro": (1.25, 10.00),
    "gemini-2.5-flash": (0.30, 2.50),
}


def _prices(model, input_price, output_price):
    if input_price is not None and output_price is not None:
        return input_price, output_price
    if model not in PRICES:
        raise KeyError(f"Unknown model {model!r}; pass input_price/output_price or add it to PRICES.")
    ip, op = PRICES[model]
    return (input_price if input_price is not None else ip,
            output_price if output_price is not None else op)


def estimate_cost(input_tokens, output_tokens, *, model=None,
                  input_price=None, output_price=None, cached_input_tokens=0,
                  cached_discount=0.9):
    """Cost of a single call in USD.

    cached_input_tokens are billed at (1 - cached_discount) of the input price
    (prompt caching). Set cached_discount=0 to disable.
    """
    ip, op = _prices(model, input_price, output_price)
    fresh_input = max(0, input_tokens - cached_input_tokens)
    cost = fresh_input * ip
    cost += cached_input_tokens * ip * (1 - cached_discount)
    cost += output_tokens * op
    return cost / 1_000_000


def project_monthly(input_tokens, output_tokens, *, calls_per_day, days=30, **kw):
    """Projected monthly cost in USD for a repeated call."""
    return estimate_cost(input_tokens, output_tokens, **kw) * calls_per_day * days


if __name__ == "__main__":
    per_call = estimate_cost(1500, 300, model="gpt-4o")
    monthly = project_monthly(1500, 300, calls_per_day=5000, model="gpt-4o")
    print(f"gpt-4o: ${per_call:.5f}/call, ~${monthly:,.0f}/month at 5k calls/day")
    cheaper = project_monthly(1500, 300, calls_per_day=5000, model="gpt-4o-mini")
    print(f"gpt-4o-mini: ~${cheaper:,.0f}/month  (save ~${monthly - cheaper:,.0f})")
