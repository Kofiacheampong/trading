#!/usr/bin/env bash
# setup.sh — run ON THE PI as user kofi (Raspberry Pi OS Lite 64-bit, fresh boot)
# Installs: Node 24, OpenClaw, Python sim deps, Ollama + nomic-embed-text,
#           systemd user service for the gateway (mirrors the PC's unit).
set -euo pipefail

echo "==> System update"
sudo apt update && sudo apt upgrade -y

echo "==> Node.js 24 (ARM64 via NodeSource)"
if ! command -v node >/dev/null; then
  curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
  sudo apt install -y nodejs
fi
node --version

echo "==> OpenClaw"
sudo npm install -g openclaw
NODE_BIN="$(command -v node)"
OPENCLAW_ENTRY="$(npm root -g)/openclaw/dist/index.js"
echo "    node: $NODE_BIN"
echo "    entry: $OPENCLAW_ENTRY"

echo "==> Python deps for trading sims (Debian packages — no pip/PEP668 pain)"
sudo apt install -y python3-yfinance python3-pandas python3-numpy python3-requests python3-pip
python3 -c "import yfinance, pandas, numpy, requests; print('    yfinance', yfinance.__version__, '| pandas', pandas.__version__, '| numpy', numpy.__version__)"

echo "==> Ollama + nomic-embed-text (local memory embeddings)"
if ! command -v ollama >/dev/null; then
  curl -fsSL https://ollama.com/install.sh | sh
fi
ollama pull nomic-embed-text
ollama list | grep nomic-embed-text

echo "==> systemd user service (mirror of the PC unit)"
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/openclaw-gateway.service <<EOF
[Unit]
Description=OpenClaw Gateway (Pi)
After=network-online.target
Wants=network-online.target
StartLimitBurst=5
StartLimitIntervalSec=60

[Service]
ExecStart=$NODE_BIN $OPENCLAW_ENTRY gateway --port 18789
Restart=always
RestartSec=5
RestartPreventExitStatus=78
TimeoutStopSec=30
TimeoutStartSec=30
SuccessExitStatus=0 143
KillMode=control-group
Environment=HOME=/home/kofi
Environment=TMPDIR=/tmp
Environment=NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
Environment=PATH=/usr/local/bin:/usr/bin:/bin
Environment=OPENCLAW_GATEWAY_PORT=18789
Environment=OPENCLAW_SYSTEMD_UNIT=openclaw-gateway.service
Environment=OPENCLAW_SERVICE_KIND=gateway

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload

echo "==> Keep user services alive after logout"
sudo loginctl enable-linger kofi

echo
echo "DONE. Next steps:"
echo "  1. On the PC: cd ~/clawd/pi-migration && ./migrate.sh kofi@<pi-ip-or-hostname>"
echo "  2. Then: ./swap.sh kofi@<pi-ip-or-hostname>   (stops PC gateway, starts Pi)"
