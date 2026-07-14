#!/usr/bin/env bash
#
# devarm installer — symlinks the devarm skills into the directories that Cursor, Codex, and
# Claude Code scan, so one source of truth (this repo) works across every tool.
#
# Because it uses symlinks, editing a skill here updates it everywhere instantly.
#
# Usage:
#   ./install.sh                      # global install (all your projects) -> ~/.agents/skills
#   ./install.sh --project /path/repo # install into one project -> <repo>/.agents/skills
#   ./install.sh --uninstall          # remove global symlinks
#   ./install.sh --project /path/repo --uninstall
#
# Notes:
#   - .agents/skills is read natively by Cursor and Codex. We also mirror into .claude/skills
#     and .codex/skills so tools that only scan their own dir still see the skills.
#   - Idempotent: re-running refreshes the links.

set -euo pipefail

DEVARM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$DEVARM_ROOT/skills"

MODE="global"
PROJECT=""
UNINSTALL="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) MODE="project"; PROJECT="${2:-}"; shift 2 ;;
    --uninstall) UNINSTALL="true"; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

if [[ ! -d "$SKILLS_SRC" ]]; then
  echo "error: skills dir not found at $SKILLS_SRC" >&2
  exit 1
fi

# Resolve the base skill directories to (un)install into.
declare -a TARGET_BASES
if [[ "$MODE" == "global" ]]; then
  TARGET_BASES=("$HOME/.agents/skills" "$HOME/.claude/skills" "$HOME/.codex/skills")
else
  if [[ -z "$PROJECT" ]]; then echo "error: --project needs a path" >&2; exit 1; fi
  PROJECT="$(cd "$PROJECT" && pwd)"
  TARGET_BASES=("$PROJECT/.agents/skills" "$PROJECT/.claude/skills" "$PROJECT/.codex/skills")
fi

link_one() {
  local base="$1" name="$2" src="$3"
  mkdir -p "$base"
  local dest="$base/$name"
  # Refresh: only remove if it's our symlink or missing; never clobber a real dir.
  if [[ -L "$dest" ]]; then rm -f "$dest"; fi
  if [[ -e "$dest" && ! -L "$dest" ]]; then
    echo "  skip (real dir exists, not a symlink): $dest" >&2
    return 0
  fi
  ln -s "$src" "$dest"
  echo "  linked $dest -> $src"
}

for base in "${TARGET_BASES[@]}"; do
  echo "${UNINSTALL:+un}installing in: $base"
  for skill_dir in "$SKILLS_SRC"/devarm-*; do
    [[ -d "$skill_dir" ]] || continue
    name="$(basename "$skill_dir")"
    if [[ "$UNINSTALL" == "true" ]]; then
      dest="$base/$name"
      if [[ -L "$dest" ]]; then rm -f "$dest" && echo "  removed $dest"; fi
    else
      link_one "$base" "$name" "$skill_dir"
    fi
  done
done

if [[ "$UNINSTALL" == "true" ]]; then
  echo "devarm uninstalled."
  exit 0
fi

# For project installs, wire Claude Code to read devarm's AGENTS.md brain (import, don't clobber).
if [[ "$MODE" == "project" ]]; then
  claude_md="$PROJECT/CLAUDE.md"
  if [[ ! -e "$claude_md" ]]; then
    printf '@AGENTS.md\n' > "$claude_md"
    echo "  created $claude_md (imports AGENTS.md for Claude Code)"
  fi
fi

echo
echo "devarm installed. Skills available: $(ls -1 "$SKILLS_SRC" | tr '\n' ' ')"
echo "Restart your agent tool (or reopen the project) so it re-scans skill directories."
