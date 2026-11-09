import docx
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn

d = docx.Document('garnsh-v2-source.docx')
body = d.element.body
out = []

def para_to_md(p):
    text = ''.join(n.text or '' for n in p._p.iter(qn('w:t')))
    style = (p.style.name or '') if p.style is not None else ''
    if not text.strip():
        return ''
    if style.lower().startswith('heading'):
        lvl = ''.join(ch for ch in style if ch.isdigit()) or '1'
        return '#' * int(lvl) + ' ' + text.strip()
    if style.lower() == 'title':
        return '# ' + text.strip()
    return text.strip()

def table_to_md(tbl):
    rows = []
    for r in tbl.rows:
        cells = []
        for c in r.cells:
            cells.append(' '.join(p.text.strip() for p in c.paragraphs if p.text.strip()).replace('|','\\|'))
        rows.append(cells)
    if not rows: return ''
    width = max(len(r) for r in rows)
    rows = [r + ['']*(width-len(r)) for r in rows]
    md = ['| ' + ' | '.join(rows[0]) + ' |', '|' + '---|'*width]
    for r in rows[1:]:
        md.append('| ' + ' | '.join(r) + ' |')
    return '\n'.join(md)

for child in body.iterchildren():
    if child.tag == qn('w:p'):
        md = para_to_md(Paragraph(child, d))
        if md: out.append(md)
    elif child.tag == qn('w:tbl'):
        out.append(table_to_md(Table(child, d)))
        out.append('')

open('v2-extracted.md','w').write('\n\n'.join(out) + '\n')
print('lines', len('\n'.join(out).splitlines()))
