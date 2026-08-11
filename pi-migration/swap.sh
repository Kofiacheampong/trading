#!/usr/bin/env bash
# swap.sh — CUTOVER. Run ON THE PC after migrate.sh succeeded.
#  1. Stops + disables the PC gateway (no more double-fires)
#  2. Starts + enables the Pi gateway
#  3. Rebuilds memory index on the Pi
# Rollback: on PC run `systemctl --user enable --now openclaw-gateway`
#           on Pi run `systemctl --user disable --now openclaw-gateway`
set -euo pipefail

PI="${1:-kofi@raspberrypi.local}"

echo "==> STEP 1/3 — stopping PC gateway (this machine goes quiet now)"
systemctl --user stop openclaw-gateway
systemctl --user disable openclaw-gateway
echo "    PC gateway stopped + disabled. Rollback: systemctl --user enable --now openclaw-gateway"

echo "==> STEP 2/3 — starting Pi gateway"
ssh "$PI" 'bash -lc "
  systemctl --user daemon-reload
  systemctl --user enable --now openclaw-gateway
  sleep 4
  systemctl --user is-active openclaw-gateway
  openclaw status | head -20
"'

echo "==> STEP 3/3 — rebuilding memory index on Pi"
ssh "$PI" 'bash -lc "openclaw memory index --force --agent main && systemctl --user restart openclaw-gateway && echo INDEX-OK"'

echo
echo "SWAP DONE. Verify: send Jambot a Telegram message — it must reply (from the Pi)."
echo "Check no duplicate replies. If the Pi is silent, roll back:"
echo "  PC:  systemctl --user enable --now openclaw-gateway"
echo "  Pi:  ssh $PI \"systemctl --user disable --now openclaw-gateway\""
