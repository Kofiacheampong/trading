# Pi Migration Kit — move Jambot to an always-on Raspberry Pi

Goal: OpenClaw gateway + trading sims + memory embeddings run 24/7 on a Pi 5,
so Jambot never dies when the Windows PC is off.

## Shopping list (Aug 2026 prices)

| Item | Est. price | Notes |
|---|---|---|
| Raspberry Pi 5 8GB | ~$125 | Official price after memory hikes; street $100–175 |
| Official 27W USB-C PSU | ~$12 | Required — Pi 5 won't run off phone chargers |
| NVMe Base HAT+ (Pimoroni/official) | ~$15–30 | Mounts M.2 SSD under the board |
| 256GB M.2 NVMe SSD (2230/2280) | ~$20–25 | **NVMe, not microSD** — SD corrupts under 24/7 writes |
| Official case | ~$10 | Pairs with the NVMe Base sandwich |
| Ethernet cable | $5 | Optional; Pi 5 WiFi works but wired = stable |

**Total ≈ $180–200.** Budget alt: high-endurance 32GB microSD instead of NVMe
(~$150 total) — acceptable but expect SD wear over a year+ of always-on.
Buy from pishop.us, Adafruit, Amazon, or any official reseller.

## Pi 4 option (Kofi has a spare — chosen Aug 7, 2026)

Pi 4 is **plenty** for this workload (Node gateway + Python sims + Ollama
embeddings). Changes vs the Pi 5 list:

| Item | Pi 5 route | Pi 4 route |
|---|---|---|
| Board | Pi 5 8GB ~$125 | **free (spare)** |
| Storage attach | NVMe Base HAT $19 | USB 3.0 → NVMe enclosure ~$13 |
| SSD | 256GB NVMe ~$22 | same 256GB NVMe ~$22 |
| PSU | 27W official ~$12 | any 15W+ USB-C (original Pi 4 PSU fine) |
| Case | official ~$10 | Pi 4 case w/ fan ~$10 if missing |
| **Total** | **~$188** | **~$35** |

Notes:
- NVMe Base / any Pi 5 PCIe HAT **does not fit Pi 4** (no PCIe connector).
- Pi 4 boots from USB SSD fine (Imager → boot from USB; EEPROM updates
  automatically on modern Raspberry Pi OS).
- RAM: 4GB or 8GB comfortable; 2GB tight (gateway + Ollama + OS ≈ 1.5GB).
- Migration kit scripts are identical for both boards. Pi 5 upgrade later is
  drop-in (same SSD/OS).

## Build & boot

1. **Flash Raspberry Pi OS Lite (64-bit)** with Raspberry Pi Imager.
   Pi 4 route: write the image straight to the USB SSD (Imager sees it as a
   drive); keep the microSD out — Pi 4 will USB-boot after the first EEPROM
   update (Imager images handle this).
   - In Imager advanced options: set user `kofi`, enable SSH (password or key),
     set WiFi (or plan ethernet).
2. Assemble: NVMe Base HAT + SSD under the Pi, case, PSU, network.
3. Boot, then from the PC: `ssh kofi@raspberrypi.local` (or the Pi's IP).

## Install (one command, run ON the Pi)

```bash
cd ~ && curl -fsSL https://raw...  # or copy pi-migration/setup.sh over
bash setup.sh
```

Installs: Node 24, OpenClaw (global npm), Python sim deps (apt packages),
Ollama + nomic-embed-text. Ends with a ready check.

## Migrate (run ON the PC, from ~/clawd)

```bash
cd ~/clawd/pi-migration
./migrate.sh kofi@raspberrypi.local
```

Copies `~/.openclaw` (config, secrets, cron jobs, state) and `~/clawd`
(workspace, memory, trading_sim) to the Pi. **Does NOT touch the PC gateway yet.**

## Cutover (the swap — the only risky step)

```bash
cd ~/clawd/pi-migration
./swap.sh kofi@raspberrypi.local
```

1. Stops + disables the PC gateway (`systemctl --user stop/disable openclaw-gateway`)
2. Starts + enables the Pi gateway (systemd user service, auto-start on boot)
3. Rebuilds the memory index on the Pi (`openclaw memory index --force`)

**Verify:** send Jambot a Telegram message — it should answer from the Pi.
Check `openclaw status` on the Pi shows the gateway up.

**⚠️ Never run both gateways at once** — duplicate Telegram replies and
DOUBLE-FIRED crons (duplicate trade reports, sim steps, alerts). Pi on → PC off.

## Rollback (if the Pi fails to come up)

```bash
# On the PC (WSL2):
systemctl --user enable --now openclaw-gateway
# On the Pi: disable the service so it stops fighting:
ssh kofi@raspberrypi.local "systemctl --user disable --now openclaw-gateway"
```

PC copy stays intact as a full backup — nothing is deleted during migration.

## Gotchas (learned from the existing setup)

- **Memory index:** after copying, the index on the Pi can report "index
  metadata is missing" — that's the known fix: `openclaw memory index --force --agent main`
  then `systemctl --user restart openclaw-gateway` (swap.sh does this).
- **Device pairing:** `identity/` and `devices/` regenerate on the new host.
  Telegram credentials (`clawdbot.json`) carry over, so the bot keeps working.
- **Python versions:** PC has pandas 3.0 / numpy 2.5; Pi apt ships pandas 2.x /
  numpy 1.26. The sim scripts use standard calls and should be fine — but verify
  one daily sim step runs before trusting the Saturday report.
- **Power blips:** Pi draws ~5W. For true uptime through outages, a small USB
  UPS/power-bank with pass-through charging is a ~$20 add-on. Optional.
- **gpt-oss:20b (13GB) won't run on 8GB RAM** — the Pi only needs
  nomic-embed-text for memory search. llama3.2 (2GB) fits if you want a local
  fallback model.

## Files

- `setup.sh` — run on the Pi (installs everything)
- `migrate.sh` — run on the PC (copies config + workspace)
- `swap.sh` — run on the PC (cutover + rollback-safe)
