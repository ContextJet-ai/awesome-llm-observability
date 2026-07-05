#!/usr/bin/env bash
# Install the ContextJet LLM-observability skills into a Claude Code skills dir.
# Usage:  ./install.sh [target-skills-dir]   (default: ~/.claude/skills)
set -euo pipefail
DEST="${1:-$HOME/.claude/skills}"
SRC="$(cd "$(dirname "$0")" && pwd)/skills"
mkdir -p "$DEST"
count=0
for d in "$SRC"/*/; do
  [ -f "${d}SKILL.md" ] || continue
  name="$(basename "$d")"
  rm -rf "$DEST/$name"
  cp -R "$d" "$DEST/$name"
  echo "  ✓ installed: $name"
  count=$((count+1))
done
echo "Done — $count skills installed into $DEST"
echo "Restart Claude Code (or your agent) to pick them up."
