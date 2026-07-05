import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from llm_cost import PRICES, estimate_cost, project_monthly  # noqa: E402


def test_explicit_prices_are_exact():
    # 1M input tokens at $2.50/1M = $2.50, plus 0 output.
    assert estimate_cost(1_000_000, 0, input_price=2.50, output_price=10.0) == 2.50
    assert estimate_cost(1000, 1000, input_price=2.50, output_price=10.0) == (2500 + 10000) / 1_000_000


def test_model_lookup_matches_table():
    # Stays correct even if PRICES change, because it reads the table.
    ip, op = PRICES["gpt-4o"]
    assert estimate_cost(1000, 500, model="gpt-4o") == (1000 * ip + 500 * op) / 1_000_000


def test_unknown_model_raises():
    try:
        estimate_cost(10, 10, model="does-not-exist")
    except KeyError:
        return
    raise AssertionError("expected KeyError for unknown model")


def test_prompt_caching_discounts_cached_input():
    # 1000 input tokens, all cached, 90% cheaper -> 10% of input price billed.
    full = estimate_cost(1000, 0, input_price=10.0, output_price=0.0)
    cached = estimate_cost(1000, 0, input_price=10.0, output_price=0.0,
                           cached_input_tokens=1000, cached_discount=0.9)
    assert abs(cached - full * 0.1) < 1e-12


def test_project_monthly_scales():
    one = estimate_cost(1500, 300, model="gpt-4o")
    assert project_monthly(1500, 300, calls_per_day=5000, model="gpt-4o") == one * 5000 * 30
