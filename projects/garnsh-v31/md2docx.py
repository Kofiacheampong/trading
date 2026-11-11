#!/usr/bin/env python3
"""Markdown -> DOCX for the Garnsh plan. Handles headings, paragraphs,
bullet/numbered lists, GFM tables and **bold** / *italic* inline runs."""
import re, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

CARBON = RGBColor(0x15, 0x15, 0x15)
BROWN = RGBColor(0x2E, 0x21, 0x18)
MUTED = RGBColor(0x5E, 0x5E, 0x5A)
SERIF, BODY = 'Georgia', 'Calibri'

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)

def inline(p, text, size=10.5, color=None, bold_all=False):
    text = text.replace('\\|', '|')
    for part in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)', text):
        if not part:
            continue
        b = bold_all
        i = False
        if part.startswith('**') and part.endswith('**'):
            part, b = part[2:-2], True
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            part, i = part[1:-1], True
        elif part.startswith('`') and part.endswith('`'):
            part = part[1:-1]
        r = p.add_run(part)
        r.font.name = BODY; r.font.size = Pt(size)
        r.bold = b; r.italic = i
        if color: r.font.color.rgb = color

def add_table(doc, rows):
    head, body = rows[0], rows[1:]
    t = doc.add_table(rows=len(rows), cols=len(head))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, cell_text in enumerate(head):
        c = t.cell(0, j)
        c.text = ''
        p = c.paragraphs[0]
        inline(p, cell_text, size=9.5, color=RGBColor(0xFF, 0xFD, 0xF8), bold_all=True)
        shade(c, '151515')
    for i, row in enumerate(body, start=1):
        for j in range(len(head)):
            val = row[j] if j < len(row) else ''
            c = t.cell(i, j)
            c.text = ''
            p = c.paragraphs[0]
            inline(p, val, size=9.5, color=CARBON if j == 0 else MUTED, bold_all=(j == 0))
            if i % 2 == 0:
                shade(c, 'F6F2E7')
    doc.add_paragraph()

def main(src, out):
    lines = open(src).read().splitlines()
    doc = Document()
    for s in doc.sections:
        s.top_margin = Inches(0.9); s.bottom_margin = Inches(0.9)
        s.left_margin = Inches(0.9); s.right_margin = Inches(0.9)
    doc.styles['Normal'].font.name = BODY
    doc.styles['Normal'].font.size = Pt(10.5)

    i, n = 0, len(lines)
    while i < n:
        line = lines[i].rstrip()
        if not line.strip():
            i += 1; continue
        # table block
        if line.lstrip().startswith('|'):
            block = []
            while i < n and lines[i].lstrip().startswith('|'):
                block.append(lines[i].strip()); i += 1
            rows = []
            for r in block:
                if re.match(r'^\|[\s:\-|]+\|$', r):
                    continue
                cells = [c.strip() for c in r.strip('|').split('|')]
                rows.append(cells)
            if rows: add_table(doc, rows)
            continue
        # headings
        m = re.match(r'^(#{1,4})\s+(.*)$', line)
        if m:
            level, text = len(m.group(1)), m.group(2)
            if level == 1:
                p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(text); r.font.name = SERIF; r.font.size = Pt(24); r.bold = True; r.font.color.rgb = CARBON
                p.paragraph_format.space_after = Pt(4)
            else:
                p = doc.add_paragraph()
                r = p.add_run(text); r.font.name = SERIF
                r.font.size = Pt(15 if level == 2 else 11.5)
                r.bold = True; r.font.color.rgb = BROWN if level == 2 else CARBON
                p.paragraph_format.space_before = Pt(16 if level == 2 else 10)
                p.paragraph_format.space_after = Pt(5)
                if level == 2:
                    pPr = p._p.get_or_add_pPr()
                    pbdr = OxmlElement('w:pBdr'); bottom = OxmlElement('w:bottom')
                    bottom.set(qn('w:val'), 'single'); bottom.set(qn('w:sz'), '8')
                    bottom.set(qn('w:space'), '4'); bottom.set(qn('w:color'), 'FFBF1F')
                    pbdr.append(bottom); pPr.append(pbdr)
            i += 1; continue
        # bullet
        m = re.match(r'^[-*]\s+(.*)$', line)
        if m:
            p = doc.add_paragraph(style='List Bullet')
            inline(p, m.group(1)); p.paragraph_format.space_after = Pt(3)
            i += 1; continue
        # numbered
        m = re.match(r'^(\d+)\.\s+(.*)$', line)
        if m:
            p = doc.add_paragraph(style='List Number')
            inline(p, m.group(2)); p.paragraph_format.space_after = Pt(4)
            i += 1; continue
        # hr
        if set(line.strip()) <= {'-', '*', '_'} and len(line.strip()) >= 3:
            i += 1; continue
        # paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.12
        txt = line.strip()
        if txt.startswith('*') and txt.endswith('*') and not txt.startswith('**'):
            r = p.add_run(txt[1:-1]); r.italic = True; r.font.name = BODY; r.font.size = Pt(10)
            r.font.color.rgb = MUTED
        else:
            inline(p, txt)
        i += 1
    doc.save(out)
    print('docx written:', out)

main(sys.argv[1], sys.argv[2])
