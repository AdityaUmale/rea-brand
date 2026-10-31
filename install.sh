#!/usr/bin/env sh
# Installs the rea-brand skill into ~/.claude/skills so every Claude Code project can use it.
set -e
REPO="https://github.com/AdityaUmale/rea-brand"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
git clone --quiet --depth 1 "$REPO" "$TMP/repo"
mkdir -p "$DEST"
rm -rf "$DEST/rea-brand"
cp -R "$TMP/repo/skills/rea-brand" "$DEST/"
echo "Installed rea-brand into $DEST"
if ! command -v treg >/dev/null 2>&1; then
  echo "Next: install treg for the data: curl -fsSL https://treg.to/install.sh | sh && treg login"
fi
echo "Then open Claude Code and type: /rea-brand how did <person> grow?"
