"""
refresh_stars - keep the star counts in README.md honest.

Parses the tool tables, fetches live star counts from the GitHub API, and either
reports drift (--check, a CI gate) or rewrites the counts in place (--write, run
on a schedule to open a refresh PR). Also flags repos that went archived or dead.

The parsing, formatting, and diff logic are pure functions with no network, so
they are unit-tested; only fetch_repo touches GitHub. CC0, ContextJet.ai.

    python tools/refresh_stars.py --check           # report drift, exit 1 if any
    python tools/refresh_stars.py --write            # rewrite README star cells
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request

_GH_LINK = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
# a star cell is a number, optionally with a k suffix and a trailing note like "(SDK)"
_STAR_CELL = re.compile(r"^(\d+(?:\.\d+)?k?)(\s*\([^)]*\))?$")


def format_stars(n: int) -> str:
    """Render a raw count in the list's convention: 30412 -> '30.4k', 979 -> '979'."""
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)


def parse_star_rows(text: str):
    """Find table rows that link a GitHub repo and carry a numeric star cell.

    Returns a list of dicts: owner, repo, line_index, star_text, suffix.
    Non-numeric star cells (SDK, -, etc.) are skipped, not touched.
    """
    rows = []
    for i, line in enumerate(text.splitlines()):
        if not line.lstrip().startswith("|"):
            continue
        link = _GH_LINK.search(line)
        if not link:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        name_idx = next((j for j, c in enumerate(cells) if "github.com" in c), None)
        if name_idx is None or name_idx + 1 >= len(cells):
            continue
        star = _STAR_CELL.match(cells[name_idx + 1])
        if not star:
            continue
        rows.append({
            "owner": link.group(1),
            "repo": link.group(2).rstrip("/"),
            "line_index": i,
            "star_text": star.group(1),
            "suffix": (star.group(2) or "").strip(),
        })
    return rows


def plan_updates(rows, repo_data: dict):
    """Compare claimed vs live. repo_data maps (owner, repo) -> {stars, archived}.

    Returns (updates, flags): updates change a star cell, flags note dead/archived repos.
    """
    updates, flags = [], []
    for r in rows:
        data = repo_data.get((r["owner"], r["repo"]))
        key = f"{r['owner']}/{r['repo']}"
        if data is None:
            flags.append({"repo": key, "issue": "not found (moved or deleted)"})
            continue
        if data.get("archived"):
            flags.append({"repo": key, "issue": "archived upstream"})
        new = format_stars(data["stars"])
        if new != r["star_text"]:
            updates.append({**r, "new_text": new})
    return updates, flags


def apply_updates(text: str, updates) -> str:
    lines = text.splitlines(keepends=True)
    for u in updates:
        old = f"| {u['star_text']}{(' ' + u['suffix']) if u['suffix'] else ''} |"
        new = f"| {u['new_text']}{(' ' + u['suffix']) if u['suffix'] else ''} |"
        lines[u["line_index"]] = lines[u["line_index"]].replace(old, new, 1)
    return "".join(lines)


def fetch_repo(owner: str, repo: str, fetcher=None):
    """Return {'stars': int, 'archived': bool} or None. Injectable for tests."""
    if fetcher is not None:
        return fetcher(owner, repo)
    req = urllib.request.Request(f"https://api.github.com/repos/{owner}/{repo}")
    req.add_header("Accept", "application/vnd.github+json")
    tok = os.getenv("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"Bearer {tok}")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            d = json.load(resp)
        return {"stars": d["stargazers_count"], "archived": bool(d.get("archived"))}
    except Exception:
        return None


def _main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Keep README star counts current.")
    p.add_argument("--readme", default="README.md")
    p.add_argument("--check", action="store_true", help="report drift, exit 1 if any")
    p.add_argument("--write", action="store_true", help="rewrite the star cells in place")
    args = p.parse_args(argv)

    path = pathlib.Path(args.readme)
    text = path.read_text()
    rows = parse_star_rows(text)
    repo_data = {(r["owner"], r["repo"]): fetch_repo(r["owner"], r["repo"]) for r in rows}
    updates, flags = plan_updates(rows, repo_data)

    for u in updates:
        print(f"  {u['owner']}/{u['repo']}: {u['star_text']} -> {u['new_text']}")
    for f in flags:
        print(f"  FLAG {f['repo']}: {f['issue']}")
    print(f"{len(updates)} star updates, {len(flags)} flags, {len(rows)} repos scanned")

    if args.write and updates:
        path.write_text(apply_updates(text, updates))
        print(f"wrote {args.readme}")
    if args.check and (updates or flags):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(_main())
