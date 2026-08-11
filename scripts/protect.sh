#!/usr/bin/env bash
# protect.sh — daily snapshot of Kofi's workspace.
#  1) Rolling archive of the trading sim state (60 days, belt & suspenders)
#  2) git commit of everything changed (full version history of every file)
#  3) Daily git tag = clean restore point
#  4) Push to GitHub (off-site copy)
# Run daily via cron at 5 PM ET (after the 4:15 PM sim step).
set -euo pipefail
cd /home/kofi/clawd

# 0) Encrypted OpenClaw config snapshot (daily local, Sunday "latest" goes off-site)
bash scripts/protect_config.sh

# 1) Rolling archive of the sim state
mkdir -p backups
cp trading_sim/state.json "backups/state-$(date +%Y%m%d).json"
ls -1t backups/state-*.json 2>/dev/null | tail -n +61 | xargs -r rm -f

# 2) Git snapshot
git add -A
if ! git diff --cached --quiet; then
  git commit -q -m "auto-backup $(date '+%Y-%m-%d %H:%M %Z')"
fi

# 3) Daily tag = clean restore point
TAG="v$(date +%Y-%m-%d)"
if ! git tag | grep -q "^${TAG}$"; then
  git tag "$TAG"
fi

# 4) Off-site: keep the GitHub copy current (self-healing if a push failed)
if ! git push -q origin main --tags; then
  echo "PUSH_FAILED"
  exit 1
fi
echo "BACKUP_OK"
