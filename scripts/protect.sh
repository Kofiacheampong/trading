#!/usr/bin/env bash
# protect.sh — daily snapshot of Kofi's workspace.
#  1) Rolling archive of the trading sim state (60 days, belt & suspenders)
#  2) git commit of everything changed (full version history of every file)
#  3) Daily git tag = clean restore point
# Run daily via cron at 5 PM ET (after the 4:15 PM sim step).
set -euo pipefail
cd /home/kofi/clawd

# 1) Rolling archive of the sim state
mkdir -p backups
cp trading_sim/state.json "backups/state-$(date +%Y%m%d).json"
ls -1t backups/state-*.json 2>/dev/null | tail -n +61 | xargs -r rm -f

# 2) Git snapshot
git add -A
if git diff --cached --quiet; then
  echo "NO_CHANGES"
  exit 0
fi
git commit -q -m "auto-backup $(date '+%Y-%m-%d %H:%M %Z')"

# 3) Daily tag = clean restore point
TAG="v$(date +%Y-%m-%d)"
if ! git tag | grep -q "^${TAG}$"; then
  git tag "$TAG"
fi
echo "BACKUP_OK"
