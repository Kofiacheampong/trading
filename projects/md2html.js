// Minimal Markdown -> styled HTML converter for the Afro Deli document set.
// Usage: node md2html.js <input.md> <output.html>
const fs = require('fs');
const path = require('path');

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function inline(s) {
  s = esc(s);
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
  s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  s = s.replace(/(^|[^*])\*([^*\n]+)\*/g, '$1<em>$2</em>');
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  return s;
}

function render(md) {
  const lines = md.replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let i = 0;
  const listStack = [];
  const closeLists = () => { while (listStack.length) out.push(`</${listStack.pop()}>`); };

  while (i < lines.length) {
    const line = lines[i];

    // fenced code
    if (/^```/.test(line)) {
      closeLists(); i++;
      const buf = [];
      while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
      i++;
      out.push('<pre><code>' + esc(buf.join('\n')) + '</code></pre>');
      continue;
    }

    // table
    if (/^\s*\|/.test(line) && i + 1 < lines.length && /^\s*\|[\s:|-]+\|\s*$/.test(lines[i + 1])) {
      closeLists();
      const rows = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) { rows.push(lines[i]); i++; }
      const cells = r => r.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
      const head = cells(rows[0]);
      let html = '<table><thead><tr>' + head.map(c => `<th>${inline(c)}</th>`).join('') + '</tr></thead><tbody>';
      for (let r = 2; r < rows.length; r++) {
        html += '<tr>' + cells(rows[r]).map(c => `<td>${inline(c)}</td>`).join('') + '</tr>';
      }
      out.push(html + '</tbody></table>');
      continue;
    }

    // headings
    const h = line.match(/^(#{1,6})\s+(.*)$/);
    if (h) { closeLists(); out.push(`<h${h[1].length}>${inline(h[2])}</h${h[1].length}>`); i++; continue; }

    // hr
    if (/^\s*---+\s*$/.test(line)) { closeLists(); out.push('<hr>'); i++; continue; }

    // blockquote
    if (/^\s*>\s?/.test(line)) {
      closeLists();
      const buf = [];
      while (i < lines.length && /^\s*>\s?/.test(lines[i])) { buf.push(lines[i].replace(/^\s*>\s?/, '')); i++; }
      out.push('<blockquote>' + buf.map(b => `<p>${inline(b)}</p>`).join('') + '</blockquote>');
      continue;
    }

    // lists
    const ul = line.match(/^\s*[-*]\s+(.*)$/);
    const ol = line.match(/^\s*\d+\.\s+(.*)$/);
    if (ul || ol) {
      const tag = ul ? 'ul' : 'ol';
      if (!listStack.length || listStack[listStack.length - 1] !== tag) {
        closeLists(); listStack.push(tag); out.push(`<${tag}>`);
      }
      out.push(`<li>${inline((ul || ol)[1])}</li>`);
      i++; continue;
    }

    // blank
    if (/^\s*$/.test(line)) { closeLists(); i++; continue; }

    // paragraph
    closeLists();
    out.push(`<p>${inline(line)}</p>`);
    i++;
  }
  closeLists();
  return out.join('\n');
}

const input = path.resolve(process.argv[2]);
const output = path.resolve(process.argv[3] || input.replace(/\.\w+$/, '.html'));
const body = render(fs.readFileSync(input, 'utf8'));

const css = `
  * { box-sizing: border-box; }
  body { font-family: 'Inter', 'Segoe UI', 'DejaVu Sans', Arial, sans-serif; color: #1a1a1a; line-height: 1.5; font-size: 9.5pt; }
  h1 { font-size: 22pt; font-weight: 800; color: #111; border-bottom: 3px solid #d97706; padding-bottom: 6px; margin: 0 0 4px; }
  h1 + h2 { border-bottom: none; color: #6b7280; font-size: 13pt; margin-top: 0; }
  h2 { font-size: 15pt; font-weight: 700; color: #b45309; border-bottom: 1px solid #e5e7eb; padding-bottom: 4px; margin: 1.4em 0 0.6em; page-break-after: avoid; }
  h3 { font-size: 12pt; font-weight: 700; color: #333; margin: 1.1em 0 0.4em; page-break-after: avoid; }
  h4 { font-size: 11pt; font-weight: 700; margin: 1em 0 0.3em; }
  p { margin: 0.45em 0; }
  table { width: 100%; border-collapse: collapse; margin: 0.7em 0; font-size: 8.8pt; page-break-inside: avoid; }
  th { background: #fef3c7; border: 1px solid #f0d9a0; padding: 5px 7px; text-align: left; font-weight: 700; }
  td { border: 1px solid #e5e7eb; padding: 4px 7px; vertical-align: top; }
  tbody tr:nth-child(even) td { background: #fafafa; }
  ul, ol { margin: 0.4em 0 0.6em; padding-left: 20px; }
  li { margin: 0.15em 0; }
  blockquote { border-left: 3px solid #d97706; background: #fffbeb; margin: 0.7em 0; padding: 8px 14px; color: #3f3f46; font-size: 9.8pt; page-break-inside: avoid; }
  blockquote p { margin: 0.25em 0; }
  code { background: #f4f4f5; padding: 1px 4px; border-radius: 3px; font-family: ui-monospace, Menlo, monospace; font-size: 9pt; }
  pre { background: #f8f8f7; border: 1px solid #e5e7eb; border-radius: 4px; padding: 10px 12px; font-size: 8.8pt; page-break-inside: avoid; }
  pre code { background: none; padding: 0; }
  hr { border: none; border-top: 1px solid #e5e7eb; margin: 1.2em 0; }
  strong { color: #000; }
  a { color: #b45309; text-decoration: none; }
  @page { size: letter; margin: 15mm 14mm; }
`;

fs.writeFileSync(output, `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><title>Afro Deli — Woodbury Business Plan</title>
<style>${css}</style></head>
<body>${body}</body></html>`);
console.log('HTML written:', output);
