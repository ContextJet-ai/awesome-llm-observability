import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from refresh_stars import (  # noqa: E402
    format_stars, parse_star_rows, plan_updates, apply_updates, fetch_repo,
)

SAMPLE = """\
## Tracing

| Tool | ⭐ | License | Description |
|---|---|---|---|
| 🔵 [Langfuse](https://github.com/langfuse/langfuse) | 30.4k | MIT | tracing platform |
| 🟠 [LangSmith](https://github.com/langchain-ai/langsmith-sdk) | SDK | MIT | not numeric, skip |
| 🟢 [Langtrace](https://github.com/Scale3-Labs/langtrace) | 1.2k | AGPL | otel tracing |
| 🟠 [Datadog](https://github.com/DataDog/dd-trace-py) | 0.6k (tracer) | BSD-3 | apm |

Not a table row with https://github.com/foo/bar in prose should be ignored.
"""


def test_format_stars():
    assert format_stars(30412) == "30.4k"
    assert format_stars(979) == "979"
    assert format_stars(1000) == "1.0k"


def test_parse_only_numeric_github_rows():
    rows = parse_star_rows(SAMPLE)
    repos = {(r["owner"], r["repo"]) for r in rows}
    assert ("langfuse", "langfuse") in repos
    assert ("Scale3-Labs", "langtrace") in repos
    assert ("DataDog", "dd-trace-py") in repos
    # the SDK (non-numeric) row and the prose link are skipped
    assert ("langchain-ai", "langsmith-sdk") not in repos
    assert ("foo", "bar") not in repos
    # suffix is preserved for the tracer row
    dd = next(r for r in rows if r["repo"] == "dd-trace-py")
    assert dd["suffix"] == "(tracer)" and dd["star_text"] == "0.6k"


def test_plan_updates_and_flags():
    rows = parse_star_rows(SAMPLE)
    data = {
        ("langfuse", "langfuse"): {"stars": 31200, "archived": False},   # drifted 30.4k -> 31.2k
        ("Scale3-Labs", "langtrace"): {"stars": 1200, "archived": True},  # same count, but archived
        ("DataDog", "dd-trace-py"): None,                                  # dead / moved
    }
    updates, flags = plan_updates(rows, data)
    changed = {u["repo"]: u["new_text"] for u in updates}
    assert changed["langfuse"] == "31.2k"
    assert "langtrace" not in changed  # count unchanged
    issues = {f["repo"]: f["issue"] for f in flags}
    assert "archived" in issues["Scale3-Labs/langtrace"]
    assert "not found" in issues["DataDog/dd-trace-py"]


def test_apply_updates_rewrites_cell_and_keeps_suffix():
    rows = parse_star_rows(SAMPLE)
    data = {
        ("langfuse", "langfuse"): {"stars": 31200, "archived": False},
        ("DataDog", "dd-trace-py"): {"stars": 5900, "archived": False},   # 0.6k -> 5.9k, keep (tracer)
    }
    updates, _ = plan_updates(rows, data)
    out = apply_updates(SAMPLE, updates)
    assert "| 31.2k |" in out and "| 30.4k |" not in out
    assert "| 5.9k (tracer) |" in out and "| 0.6k (tracer) |" not in out


def test_fetch_repo_uses_injected_fetcher():
    got = fetch_repo("a", "b", fetcher=lambda o, r: {"stars": 42, "archived": False})
    assert got["stars"] == 42


def test_stale_flag_uses_last_commit():
    import datetime as dt
    from refresh_stars import is_stale
    now = dt.datetime(2026, 11, 8, tzinfo=dt.timezone.utc)
    assert is_stale("2026-04-14T15:29:57Z", now)        # ~208 days
    assert not is_stale("2026-10-01T00:00:00Z", now)
    assert not is_stale(None, now)                       # unknown date isn't flagged
    rows = parse_star_rows(SAMPLE)
    data = {
        ("langfuse", "langfuse"): {"stars": 30400, "archived": False, "last_commit": "2026-11-07T00:00:00Z"},
        ("Scale3-Labs", "langtrace"): {"stars": 1200, "archived": False, "last_commit": "2025-11-24T11:36:18Z"},
        ("DataDog", "dd-trace-py"): {"stars": 600, "archived": False},
    }
    _, flags = plan_updates(rows, data, now)
    issues = {f["repo"]: f["issue"] for f in flags}
    assert issues == {"Scale3-Labs/langtrace": "no commit since 2025-11-24"}
    # without a clock the freshness check is off, matching the old behavior
    assert plan_updates(rows, data)[1] == []
