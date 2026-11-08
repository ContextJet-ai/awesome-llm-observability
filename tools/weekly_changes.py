"""Write release notes for what changed in README.md since a git ref.

Usage: python tools/weekly_changes.py <since-ref>   (prints markdown, empty if nothing changed)
"""
import re
import subprocess
import sys

ROW = re.compile(r"^\|\s*(?:\S+\s+)?\[([^\]]+)\]\((https?://[^)]+)\)\s*\|(.*)$")
STARS = re.compile(r"^\s*([\d.]+)(k?)\s*$")


def stars(cell):
    m = STARS.match(cell)
    if not m:
        return None
    n = float(m.group(1))
    return int(n * 1000) if m.group(2) else int(n)


def rows(text):
    out = {}
    for line in text.splitlines():
        m = ROW.match(line)
        if m:
            name, url, rest = m.groups()
            cells = rest.split("|")
            out.setdefault(url, (name, stars(cells[0]) if cells else None))
    return out


def readme_at(ref):
    return subprocess.run(["git", "show", f"{ref}:README.md"], capture_output=True, text=True, check=True).stdout


def notes(old, new):
    before, after = rows(old), rows(new)
    added = [after[u][0] + f" ({u})" for u in after if u not in before]
    removed = [before[u][0] for u in before if u not in after]
    moves = []
    for u in after.keys() & before.keys():
        a, b = before[u][1], after[u][1]
        if a and b and b != a:
            moves.append((b - a, after[u][0], a, b))
    moves.sort(reverse=True)
    parts = []
    if added:
        parts.append("### Added\n" + "\n".join(f"- {x}" for x in added))
    if removed:
        parts.append("### Removed\n" + "\n".join(f"- {x}" for x in removed))
    if moves[:5] and moves[0][0] > 0:
        parts.append("### Fastest growing\n" + "\n".join(
            f"- {name}: {a:,} → {b:,} (+{d:,})" for d, name, a, b in moves[:5] if d > 0))
    return "\n\n".join(parts)


if __name__ == "__main__":
    print(notes(readme_at(sys.argv[1]), open("README.md").read()))
