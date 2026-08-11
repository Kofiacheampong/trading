#!/usr/bin/env bash
# protect_config.sh — encrypted backup of the OpenClaw config (crons, tokens, pairing).
#   - Encrypts BEFORE anything touches disk, so the blob is safe even in a repo.
#   - Daily blobs stay local (rolling 30). Sundays: also stamp the "latest" copy,
#     which IS committed + pushed to GitHub for off-site disaster recovery.
#   - Passphrase lives at $PASSFILE (chmod 600, NOT in the repo). Kofi keeps a copy
#     in his password manager — without it the GitHub copy can't be decrypted.
#   - Restore: gpg -d backup.tar.gpg | tar xzf - -> copy contents back into ~/.openclaw/
set -euo pipefail
cd /home/kofi/clawd

PASSFILE="/home/kofi/.config/openclaw-backup-pass"
OUTDIR="backups"
SRC="$HOME/.openclaw"

if [ ! -f "$PASSFILE" ]; then
  echo "CONFIG_BACKUP_FAILED: no passphrase file at $PASSFILE"
  exit 1
fi

STAMP="$(date +%Y%m%d)"
TARBALL="/tmp/openclaw-config-$STAMP.tar.gz"
BLOB="$OUTDIR/openclaw-config-$STAMP.tar.gpg"

# Snapshot the rebuild-critical pieces (DB + WAL together = consistent snapshot;
# shm is transient and excluded). agents/, media/, memory index are derived/regenerable.
tar czf "$TARBALL" -C "$SRC" \
  openclaw.json openclaw.json.bak* clawdbot.json clawdbot.json.bak* \
  cron credentials devices identity \
  state/openclaw.sqlite state/openclaw.sqlite-wal 2>/dev/null || true

gpg -c --batch --yes --quiet --cipher-algo AES256 \
  --passphrase-file "$PASSFILE" -o "$BLOB" "$TARBALL"
rm -f "$TARBALL"

# Rolling: keep the 30 newest local blobs
ls -1t "$OUTDIR"/openclaw-config-*.tar.gpg 2>/dev/null | grep -v latest | tail -n +31 | xargs -r rm -f

# Sundays: stamp the "latest" copy (committed + pushed by protect.sh)
if [ "$(date +%u)" = "7" ]; then
  cp "$BLOB" "$OUTDIR/openclaw-config-latest.tar.gpg"
fi
echo "CONFIG_OK"
