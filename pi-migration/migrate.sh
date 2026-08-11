#!/usr/bin/env bash
# migrate.sh — run ON THE PC (WSL2). Copies OpenClaw config + workspace to the Pi.
# Usage: ./migrate.sh [user@pi-host]   (default: kofi@raspberrypi.local)
# Does NOT touch the PC gateway. Cutover is swap.sh.
set -euo pipefail

PI="${1:-kofi@raspberrypi.local}"

echo "==> Installing SSH key (passwordless from now on)"
ssh-copy-id -o StrictHostKeyChecking=accept-new "$PI" >/dev/null 2>&1 || true

echo "==> Checking Pi prerequisites"
ssh "$PI" 'bash -lc "command -v node >/dev/null && command -v openclaw >/dev/null && echo OK-prereqs || echo MISSING-prereqs-run-setup.sh"'

echo "==> Copying ~/.openclaw (config, secrets, cron jobs, state) — excluding logs/cache"
rsync -a --info=progress2 \
  --exclude 'logs/' \
  --exclude 'cache/' \
  --exclude 'locks/' \
  --exclude 'audit/' \
  ~/.openclaw/ "$PI":~/.openclaw/

echo "==> Copying ~/clawd workspace (memory, trading_sim, projects, docs)"
rsync -a --info=progress2 \
  --exclude '__pycache__/' \
  --exclude '.git/' \
  ~/clawd/ "$PI":~/clawd/

echo "==> Sanity: key files present on Pi"
ssh "$PI" 'ls -la ~/.openclaw/openclaw.json ~/.openclaw/clawdbot.json ~/clawd/MEMORY.md ~/clawd/trading_sim/sim.py'

echo
echo "Migrate complete. Nothing on the PC was changed."
echo "Next: ./swap.sh $PI  (cutover)"
