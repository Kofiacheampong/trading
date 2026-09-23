# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Document → PDF pipeline (this box: Oracle ARM64)

**Use WeasyPrint, not puppeteer.** `projects/generate-pdf.js` (puppeteer) is unreliable here: Chrome for Testing has no linux-arm64 build, so puppeteer downloads an **x86-64** binary that cannot execute on this host.

Working pipeline (installed 2026-09-23):

```bash
cd ~/clawd/projects
node md2html.js <input.md> <output.html>      # dependency-free Markdown → styled HTML
weasyprint <output.html> <output.pdf>          # WeasyPrint 61.1 via apt
```

- `projects/md2html.js` handles headings, GFM tables, lists, blockquotes, fenced code (org charts), hr, and inline `**bold**` `*italic*` `` `code` `` `[links](url)`. Class names for bold are spelled out so it doesn't collide with the `strong` CSS rule.
- Installed for this: `weasyprint`, `unzip`, `poppler-utils` (pdfinfo / pdftotext / pdftoppm for verifying output).
- Don't `@import` web fonts in the CSS — WeasyPrint has no network font fetch; use the local font stack ('Inter', 'DejaVu Sans', Arial).
- Verify every generated PDF: `pdfinfo out.pdf` (page count) + `pdftotext -layout out.pdf - | grep -nE '\*\*|\| *---'` (should return nothing — that would mean raw markdown leaked through).
- Same HTML also renders in a browser if Kofi wants to preview it (`projects/*.html`).

## Reports / reference docs
- Afro Deli Woodbury plan lives in `projects/` (`.md` source, `.html`, `.pdf`). Keep the Markdown as source of truth; regenerate HTML+PDF after edits.
