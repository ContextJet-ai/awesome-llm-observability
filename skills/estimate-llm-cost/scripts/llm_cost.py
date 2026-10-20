"""
llm_cost - estimate and project LLM API cost from token counts.

Pure-Python, zero dependencies. Prices are approximate USD per 1M tokens and
change often; pass explicit prices (or edit PRICES) for accuracy. The math is
what's tested, not the price table.

    from llm_cost import estimate_cost, project_monthly

    estimate_cost(1500, 300, model="gpt-6.1-sol")      # one call
    project_monthly(1500, 300, calls_per_day=5000, model="gpt-6-luna")

CC0 - ContextJet.ai.
"""

from __future__ import annotations

# USD per 1M tokens: (input, output), standard tier, short context, no caching.
# Read from each provider's pricing page on PRICES_AS_OF. Override for accuracy.
PRICES_AS_OF = "2026-10-19"
PRICES = {
    # OpenAI (developers.openai.com/api/docs/pricing)
    "gpt-6-astra": (10.00, 50.00),
    "gpt-6.1-sol": (2.00, 10.00),
    "gpt-6-luna": (0.10, 0.50),
    # Anthropic (docs.anthropic.com pricing)
    "claude-opus-5-5": (4.00, 20.00),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-haiku-5-5": (0.10, 0.50),    # prompts up to 100K tokens; 0.50/2.50 beyond
    # Google (ai.google.dev/gemini-api/docs/pricing)
    "gemini-4-argon": (2.00, 10.00),     # promo through 2026-11-30, then 4.00/20.00
    "gemini-3.8-flash": (0.75, 3.75),    # promo through 2026-12-31, then 1.50/7.50
    "gemini-3.5-flash-lite": (0.30, 2.50),
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
    per_call = estimate_cost(1500, 300, model="gpt-6.1-sol")
    monthly = project_monthly(1500, 300, calls_per_day=5000, model="gpt-6.1-sol")
    print(f"gpt-6.1-sol: ${per_call:.5f}/call, ~${monthly:,.0f}/month at 5k calls/day")
    cheaper = project_monthly(1500, 300, calls_per_day=5000, model="gpt-6-luna")
    print(f"gpt-6-luna: ~${cheaper:,.0f}/month  (save ~${monthly - cheaper:,.0f})")
    print(f"(prices as of {PRICES_AS_OF}; pass input_price/output_price for anything newer)")
