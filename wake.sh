#!/bin/bash
set -ea
cd "$(dirname "$0")"
git pull --rebase
source .env
set +a
PROMPT="${1:-FREE}"
TIME=$(TZ='America/Los_Angeles' date '+%Y-%m-%d %H:%M %Z')
BALANCE=$(uv run scripts/check_balance.py 2>/dev/null || echo "unknown")
opencode run "[$TIME | $BALANCE] $PROMPT. Read AGENTS.md."
git add -A && git commit -m "$(date +%Y%m%d-%H%M) $PROMPT" || true
git push
uv run scripts/sync_secrets.py "$REPO"
