// Garnsh pitch deck builder — one content source, two outputs.
//   node build.js            -> garnsh-pitch-deck.pptx + deck.html
// Colors + type come from garnsh.vercel.app CSS custom properties:
//   --garnsh-mango #ffbf1f  --garnsh-carbon #151515  --garnsh-cloud #fffdf8
//   --garnsh-paper #f6f2e7  --garnsh-green #22c878   --garnsh-tomato #ff644b
//   --garnsh-brown #2e2118  --garnsh-muted #5e5e5a  --garnsh-line #d9d7d0
// Fonts: Manrope (200-800) body/UI, Fraunces (display serif).
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

const C = {
  mango: 'FFBF1F',
  carbon: '151515',
  cloud: 'FFFDF8',
  paper: 'F6F2E7',
  green: '22C878',
  tomato: 'FF644B',
  brown: '2E2118',
  muted: '5E5E5A',
  line: 'D9D7D0',
};
const SANS = 'Manrope';
const SERIF = 'Fraunces';

const W = 13.333, H = 7.5, M = 0.85;

// ---------------------------------------------------------------- content
const SLIDES = [
  {
    type: 'title',
    kicker: 'MENU PUBLISHING LAYER FOR TOAST',
    title: 'Garnsh',
    subtitle: 'Your menu, everywhere.',
    body: 'We publish the menu a restaurant already runs in Toast to every guest-facing surface it has — website, QR, screens — per location, with preview, rollback, and a menu that never goes dark.',
    foot: '2027 · Confidential',
  },
  {
    type: 'content',
    kicker: 'THE PROBLEM',
    title: 'One menu. Five versions.\nNone of them agree.',
    lead: 'The menu a guest sees is never the menu the kitchen runs. It is a copy of a copy, edited by whoever had the login.',
    bullets: [
      { label: 'Fragmentation', text: 'The POS holds the real menu. The website holds a PDF from March. The QR code points at a third copy. The boards run off a USB stick.' },
      { label: 'Multi-location', text: 'Groups multiply it — airport, stadium and flagship pricing on the same item, each with its own stale copy.' },
      { label: 'Cost', text: 'The guest reads $16 and gets charged $18. That is a comp, a bad review, and in some jurisdictions a consumer-protection exposure.' },
      { label: 'Turnover', text: 'Someone retypes the menu into Canva every time a price changes. Then that person quits.' },
    ],
    stats: [
      { value: '3', label: 'guest surfaces per location, minimum' },
      { value: '0', label: 'rollbacks available when a bad menu ships' },
      { value: '1', label: 'person who knows how to update it' },
    ],
  },
  {
    type: 'content',
    kicker: 'WHY NOW',
    title: 'The menu became the product listing.',
    bullets: [
      { label: 'Machine-readable', text: 'AI answer engines and search summaries reward current, structured menus. A PDF is invisible to them.' },
      { label: 'Hardware collapsed', text: 'A 43" commercial display is a few hundred dollars. The bottleneck is software and content, not screens.' },
      { label: 'Labor churn', text: '"The person who knew how" is now a recurring annual failure mode in every restaurant.' },
      { label: 'Compounding base', text: 'Toast adds ~8,500 net locations a quarter. Our addressable market grows without us spending a dollar.' },
    ],
  },
  {
    type: 'cards',
    kicker: 'WHAT IT IS',
    title: 'Four surfaces. One source of truth.',
    cards: [
      { head: 'Hosted page', text: 'A public menu page per location, server-rendered, phone-first, in the restaurant\'s own brand.' },
      { head: 'Website embed', text: 'Drops the same menu into the site they already have. No rebuild, no migration.' },
      { head: 'QR menu', text: 'A phone view behind a printed code, one per location — tables, patios, counters.' },
      { head: 'Menu board', text: 'A designed display for screens they already own. 16:9 and 3-panel landscape.' },
    ],
    foot: 'The operator keeps running the menu in Toast. We handle what guests see, where, and for which location.',
  },
  {
    type: 'content',
    kicker: 'THE DIFFERENCE',
    title: 'We ship menus like software.',
    lead: 'Nobody in restaurant tech treats a menu like a release. That is the entire product.',
    bullets: [
      { label: 'Preview → publish → rollback', text: 'Draft v15 is never visible while v14 is live. Every published version is retained and restorable.' },
      { label: 'Last-known-good', text: 'If the upstream feed breaks, surfaces keep serving the most recent version that published correctly. No blank boards at the counter.' },
      { label: 'Location mapping', text: 'Each surface is bound to one location. The airport price never appears on the flagship board.' },
      { label: 'Freshness, honestly', text: '"Source last read 6 minutes ago" — an operational readout, not a fake real-time claim.' },
    ],
  },
  {
    type: 'content',
    kicker: 'SCOPE',
    title: 'What we refuse to build — and why.',
    lead: 'No ordering. No payments. No cart. No delivery. No 86 status.',
    bullets: [
      { label: 'Off Toast\'s revenue path', text: 'We never touch orders or money, so we are never competing with the platform we depend on.' },
      { label: 'Out of PCI scope', text: 'No card data, no chargebacks, no tax and tip logic. A different company, with different risk, is what we are deliberately not.' },
      { label: 'No conflict for the operator', text: 'We do not threaten their ordering vendor, so saying yes costs them nothing politically.' },
      { label: 'Focus', text: 'Every engineering hour goes to the hard part: correct, versioned, per-location rendering.' },
    ],
  },
  {
    type: 'stats',
    kicker: 'MARKET',
    title: 'Bottom-up, not top-down.',
    stats: [
      { value: '189K', label: 'Toast locations, +21% YoY' },
      { value: '8.5K', label: 'net locations added per quarter' },
      { value: '15–23K', label: 'locations in groups of 10+' },
      { value: '$8–17M', label: 'SAM, Toast 10+ segment' },
    ],
    bullets: [
      { label: 'Expansion axis', text: 'More POS platforms, not bigger accounts. Square, then Clover, takes the addressable market to $250–400M.' },
      { label: 'Why 10+ first', text: 'Longer contracts, real budgets, rational buyers, and location mapping is an acute pain at that scale — not a nice-to-have.' },
    ],
  },
  {
    type: 'content',
    kicker: 'CUSTOMER',
    title: 'Operators with 10+ locations.',
    lead: 'Not single-unit independents. That market is owned by bundles we cannot beat on price or features.',
    bullets: [
      { label: 'Who', text: 'Franchisee groups, local chains, hospitality groups, airport and stadium concessionaires.' },
      { label: 'Who signs', text: 'Director of Operations or Marketing. Not IT — which means a 20-minute demo, not a procurement cycle.' },
      { label: 'Why they say yes', text: 'Pricing integrity per location, brand consistency, and a new opening that does not require rebuilding a website.' },
      { label: 'Why they stay', text: 'Switching means re-mapping every location. It becomes part of the opening procedure.' },
    ],
    stats: [
      { value: '1.2%', label: 'monthly churn, multi-unit' },
      { value: '4.0%', label: 'monthly churn, single-unit' },
    ],
  },
  {
    type: 'table',
    kicker: 'BUSINESS MODEL',
    title: 'Priced per location, because that is how they think.',
    table: {
      head: ['Plan', 'Price', 'Includes'],
      rows: [
        ['Solo', '$39 / location / mo', 'Hosted page, embed, QR, one board screen'],
        ['Growth', '$69 / location / mo', 'Unlimited boards, custom domain, brand kit'],
        ['Multi', '$45 / location / mo', 'Min. 3 locations. Location mapping, per-location overrides'],
        ['Group', '$35 / location / mo', '26+ locations, annual, onboarding, priority support'],
        ['Setup', '$199 one-time', 'Brand import, first location live, QR assets'],
      ],
      colW: [2.0, 3.3, 6.3],
    },
    bullets: [
      { label: 'Rule one', text: 'Never discount the per-location price. Per-location price is the entire revenue model.' },
      { label: 'Rule two', text: 'Charge per location, not per surface. Surface pricing invites the operator to turn things off.' },
    ],
  },
  {
    type: 'stats',
    kicker: 'UNIT ECONOMICS',
    title: '88% gross margin. 4–6x LTV to CAC.',
    stats: [
      { value: '$52', label: 'blended ARPU / location / mo' },
      { value: '88%', label: 'gross margin' },
      { value: '$3,800', label: 'LTV, multi-unit' },
      { value: '4.2–6.3x', label: 'LTV : CAC' },
    ],
    bullets: [
      { label: 'Payback', text: '13–20 months on multi-unit, 6–8 on single-unit. Single-unit pays back faster; multi-unit is 4x the lifetime value.' },
      { label: 'The margin risk', text: 'Onboarding, not infrastructure. Two to four hours of human time per location is why setup fees are not discounted casually.' },
    ],
  },
  {
    type: 'table',
    kicker: 'COMPETITION',
    title: 'Everyone solves a different part of this.',
    table: {
      head: ['Player', 'What they do', 'Price', 'Why we differ'],
      rows: [
        ['Toast (native)', 'POS, marketing suite, Delphi boards', 'Bundled / hardware', 'Brand-first, versioned, any screen they own'],
        ['Owner.com', 'Website + ordering + marketing', '$249/mo + 5% of orders', 'We layer on top; no site migration'],
        ['Popmenu', 'Website + menu + marketing', '~$500/mo + ~$1,300 setup', 'Cheap, narrow, removable'],
        ['Marqii', 'Menu sync to Google, Yelp, Apple', 'Mid-market', 'Rendering, not distribution'],
        ['Signage vendors', 'Screens + CMS', 'Signage pricing', 'Menu-first; also page and embed'],
      ],
      colW: [2.1, 3.5, 3.0, 3.0],
    },
  },
  {
    type: 'content',
    kicker: 'HONESTLY',
    title: 'Where we win. Where we lose.',
    bullets: [
      { label: 'Win', text: 'Multi-location pricing integrity, release discipline, last-known-good reliability — and no requirement to change POS, website or ordering vendor.' },
      { label: 'Win', text: 'Design quality in a category where the incumbents look like 2014.' },
      { label: 'Lose', text: 'Anyone who wants one vendor for everything. Anyone who wants ordering. Anyone who has decided to live with the problem.' },
      { label: 'No technical moat', text: 'This is a well-made CRUD app with taste. The durable advantages are switching cost, distribution and brand — all of which compound, none of which exist on day one.' },
    ],
  },
  {
    type: 'cards',
    kicker: 'ROADMAP',
    title: 'Gen 1.0 is the company.\nGen 2.0 is the risk.',
    cards: [
      { head: 'Gen 1.0 · 2027', text: 'Custom menus, order-ready menu boards, location picker. This is the entire company for eighteen months.' },
      { head: 'Gen 2.0 · 2028', text: 'Branded ordering experience that submits into the operator\'s existing Toast Online Ordering. Not our own checkout.' },
      { head: 'Gen 3.0 · 2029', text: 'Branded mobile app and commerce. Funded from revenue, only after the base case is proven.' },
    ],
    foot: 'Owning checkout means PCI scope, chargebacks, and direct competition with the platform that controls our API access. We take the front-end, not the rails — until there is a signed partnership that makes the rest safe.',
  },
  {
    type: 'content',
    kicker: '2027 PLAN',
    title: 'Ten locations, six of them paying.',
    bullets: [
      { label: 'January', text: 'Entity formed, operating agreement signed, $10K per partner in. Toast partner application filed in week one — it is the longest pole in the company.' },
      { label: 'Jan–March', text: 'Product vision, pricing and pitch finalized. Pricing published publicly — it filters customers and shortens every cycle.' },
      { label: 'March–June', text: 'Ten locations onboarded. At least six paying, even $50/month. A free showcase is a favour, not validation.' },
      { label: 'July–September', text: 'Cash-positive gate. If we are not revenue-positive by September, we stop and reassess instead of spending the buffer.' },
    ],
    stats: [
      { value: '$20K', label: 'initial paid-in capital' },
      { value: 'Day 120', label: 'Toast approval go / no-go' },
    ],
  },
  {
    type: 'split',
    kicker: 'TEAM & ASK',
    title: 'Two founders. $20,000.\nA deliberately narrow wedge.',
    colA: {
      head: 'The team',
      bullets: [
        'Two partners, $10,000 each, equal vesting — four years with a one-year cliff.',
        'Founder-led product and engineering; contract design, because design is the differentiator.',
        'Advisors wanted: multi-unit restaurant operations, and POS channel sales.',
      ],
    },
    colB: {
      head: 'The ask',
      bullets: [
        'Three design partners at 10+ locations, on a 30-day pilot, two locations each.',
        'One advisor with restaurant-group operations experience.',
        'Not raising yet — deliberately. We raise after 50 paid locations, measured churn, known Toast status, and one 20+ location group signed.',
      ],
    },
    foot: 'Bootstrap budget: legal and trademark $1.5K · insurance $2K · design $6K · infrastructure $3.6K · buffer $6.9K.',
  },
  {
    type: 'end',
    kicker: 'GARNSH',
    title: 'Change it in Toast.\nShow it with Garnsh.',
    body: 'garnsh.vercel.app',
    foot: 'Kofi · 2027',
  },
];

// ---------------------------------------------------------------- pptx
function buildPptx(outFile) {
  const p = new pptxgen();
  p.defineLayout({ name: 'WIDE', width: W, height: H });
  p.layout = 'WIDE';
  p.author = 'Kofi';
  p.company = 'Garnsh';
  p.title = 'Garnsh — Pitch Deck';
  p.subject = 'Menu publishing layer for Toast';

  const total = SLIDES.length;

  const kicker = (s, text, dark) => {
    if (!text) return;
    s.addShape(p.ShapeType.rect, { x: M, y: 0.72, w: 0.28, h: 0.055, fill: { color: C.mango }, line: { color: C.mango, width: 0 } });
    s.addText(text, {
      x: M + 0.42, y: 0.58, w: 9.5, h: 0.3,
      fontFace: SANS, fontSize: 11, bold: true, charSpacing: 2.2,
      color: dark ? C.mango : C.brown, valign: 'middle',
    });
  };

  const num = (s, i, dark) => {
    s.addText(String(i + 1).padStart(2, '0'), {
      x: W - M - 0.8, y: H - 0.62, w: 0.8, h: 0.3,
      fontFace: SANS, fontSize: 10, color: dark ? '7A7368' : C.muted, align: 'right',
    });
    s.addText('GARNSH', {
      x: M, y: H - 0.62, w: 3, h: 0.3,
      fontFace: SANS, fontSize: 10, bold: true, charSpacing: 1.6, color: dark ? '7A7368' : C.muted,
    });
  };

  const headline = (s, text, opts = {}) => {
    s.addText(text, {
      x: M, y: opts.y || 1.02, w: opts.w || (W - 2 * M), h: opts.h || 1.55,
      fontFace: SERIF, fontSize: opts.size || 34, bold: true,
      color: opts.color || C.carbon, valign: 'top', lineSpacingMultiple: 1.0,
    });
  };

  const bulletList = (s, bullets, y, opts = {}) => {
    const size = opts.size || 12.5;
    // Rich text must be a FLAT array of runs. A paragraph = runs joined until one
    // sets breakLine; the bullet belongs on the paragraph's FIRST run.
    const items = [];
    bullets.forEach((b) => {
      if (typeof b === 'string') {
        items.push({ text: b, options: { bullet: { code: '25AA' }, breakLine: true, paraSpaceAfter: 8 } });
      } else {
        items.push({ text: b.label + '  ', options: { bold: true, color: opts.labelColor || C.brown, bullet: { code: '25AA' } } });
        items.push({ text: b.text, options: { color: opts.textColor || C.muted, breakLine: true, paraSpaceAfter: 9 } });
      }
    });
    s.addText(items, {
      x: opts.x || M, y, w: opts.w || (W - 2 * M - 0.2), h: opts.h || 2.6,
      fontFace: SANS, fontSize: size, valign: 'top', lineSpacingMultiple: 1.16, fit: 'shrink',
    });
  };

  const statRow = (s, stats, y, dark) => {
    const n = stats.length;
    const gap = 0.3;
    const cw = (W - 2 * M - gap * (n - 1)) / n;
    stats.forEach((st, i) => {
      const x = M + i * (cw + gap);
      s.addText(st.value, {
        x, y, w: cw, h: 0.75,
        fontFace: SERIF, fontSize: 34, bold: true, color: dark ? C.mango : C.carbon, valign: 'bottom',
      });
      s.addText(st.label, {
        x, y: y + 0.78, w: cw, h: 0.55,
        fontFace: SANS, fontSize: 10.5, color: dark ? 'C9C4B8' : C.muted, valign: 'top',
      });
    });
    return y + 1.55;
  };

  SLIDES.forEach((sl, i) => {
    const s = p.addSlide();
    const dark = sl.type === 'stats' || sl.type === 'title' || sl.type === 'end';

    if (sl.type === 'table') {
      s.background = { color: C.cloud };
    } else if (dark) {
      s.background = { color: C.carbon };
    } else if (sl.type === 'split') {
      s.background = { color: C.paper };
    } else {
      s.background = { color: C.cloud };
    }

    kicker(s, sl.kicker, dark);
    num(s, i, dark);

    if (sl.type === 'title') {
      s.addText(sl.title, {
        x: M, y: 1.35, w: W - 2 * M, h: 1.35,
        fontFace: SERIF, fontSize: 76, bold: true, color: C.cloud, valign: 'bottom',
      });
      s.addText(sl.subtitle, {
        x: M, y: 2.62, w: W - 2 * M, h: 0.6,
        fontFace: SANS, fontSize: 25, bold: true, color: C.mango, valign: 'middle',
      });
      s.addText(sl.body, {
        x: M, y: 3.5, w: W - 2 * M - 1.4, h: 1.3,
        fontFace: SANS, fontSize: 14, color: 'C9C4B8', valign: 'top', lineSpacingMultiple: 1.26,
      });
      s.addShape(p.ShapeType.rect, { x: M, y: 3.25, w: 1.6, h: 0.035, fill: { color: C.mango }, line: { color: C.mango, width: 0 } });
      s.addText(sl.foot, {
        x: W - M - 2.6, y: H - 1.35, w: 2.6, h: 0.3,
        fontFace: SANS, fontSize: 10, color: '7A7368', align: 'right',
      });
      return;
    }

    if (sl.type === 'end') {
      s.addText(sl.title, {
        x: M, y: 2.1, w: W - 2 * M, h: 2.0,
        fontFace: SERIF, fontSize: 46, bold: true, color: C.cloud, valign: 'middle', lineSpacingMultiple: 1.05,
      });
      s.addText(sl.body, {
        x: M, y: 4.35, w: W - 2 * M, h: 0.4,
        fontFace: SANS, fontSize: 16, bold: true, color: C.mango,
      });
      s.addText(sl.foot, {
        x: M, y: 4.85, w: W - 2 * M, h: 0.35,
        fontFace: SANS, fontSize: 11, color: '7A7368',
      });
      return;
    }

    headline(s, sl.title);

    let y = sl.title.includes('\n') ? 2.62 : 2.3;

    if (sl.lead) {
      s.addText(sl.lead, {
        x: M, y: y - 0.1, w: W - 2 * M - 0.6, h: 0.75,
        fontFace: SANS, fontSize: 14.5, color: C.brown, valign: 'top', lineSpacingMultiple: 1.2,
      });
      y += 0.78;
    }

    if (sl.type === 'content') {
      bulletList(s, sl.bullets, y, {
        labelColor: dark ? C.mango : C.brown,
        textColor: dark ? 'C9C4B8' : C.muted,
        h: sl.stats ? 2.4 : 3.3,
      });
      if (sl.stats) statRow(s, sl.stats, 5.15, dark);
    }

    if (sl.type === 'stats') {
      const ny = statRow(s, sl.stats, y + 0.1, dark);
      bulletList(s, sl.bullets, ny + 0.25, {
        labelColor: C.mango, textColor: 'C9C4B8', size: 12, h: 1.7,
      });
    }

    if (sl.type === 'cards') {
      const n = sl.cards.length;
      const gap = 0.32;
      const cw = (W - 2 * M - gap * (n - 1)) / n;
      sl.cards.forEach((c, j) => {
        const x = M + j * (cw + gap);
        const h = 2.5;
        s.addShape(p.ShapeType.roundRect, {
          x, y, w: cw, h, fill: { color: C.paper }, line: { color: C.line, width: 1 }, rectRadius: 0.06,
        });
        s.addShape(p.ShapeType.rect, { x, y, w: cw, h: 0.055, fill: { color: C.mango }, line: { color: C.mango, width: 0 } });
        s.addText(c.head, {
          x: x + 0.28, y: y + 0.3, w: cw - 0.56, h: 0.45,
          fontFace: SANS, fontSize: 14, bold: true, color: C.carbon, valign: 'top',
        });
        s.addText(c.text, {
          x: x + 0.28, y: y + 0.85, w: cw - 0.56, h: h - 1.1,
          fontFace: SANS, fontSize: 11.5, color: C.muted, valign: 'top', lineSpacingMultiple: 1.22, fit: 'shrink',
        });
      });
      if (sl.foot) {
        s.addText(sl.foot, {
          x: M, y: y + 2.75, w: W - 2 * M, h: 0.7,
          fontFace: SANS, fontSize: 11.5, italic: true, color: C.brown, valign: 'top', lineSpacingMultiple: 1.2,
        });
      }
    }

    if (sl.type === 'table') {
      const t = sl.table;
      const rows = [
        t.head.map(h => ({
          text: h,
          options: { bold: true, color: C.cloud, fill: { color: C.carbon }, fontSize: 11, fontFace: SANS },
        })),
        ...t.rows.map((r, ri) => r.map((cell, ci) => ({
          text: cell,
          options: {
            color: ci === 0 ? C.carbon : C.muted,
            bold: ci === 0,
            fontSize: 10.5,
            fontFace: SANS,
            fill: { color: ri % 2 === 0 ? C.cloud : C.paper },
          },
        }))),
      ];
      s.addTable(rows, {
        x: M, y, w: W - 2 * M, colW: t.colW,
        border: { type: 'solid', color: C.line, pt: 0.75 },
        rowH: 0.42, valign: 'middle', margin: 0.09,
      });
      const tblH = 0.42 * (t.rows.length + 1);
      if (sl.bullets) {
        bulletList(s, sl.bullets, y + tblH + 0.35, {
          labelColor: C.brown, textColor: C.muted, size: 11.5, h: 1.2,
        });
      }
    }

    if (sl.type === 'split') {
      const cw = (W - 2 * M - 0.45) / 2;
      [sl.colA, sl.colB].forEach((col, j) => {
        const x = M + j * (cw + 0.45);
        s.addShape(p.ShapeType.rect, { x, y: y + 0.05, w: cw, h: 0.035, fill: { color: j === 0 ? C.brown : C.mango }, line: { color: j === 0 ? C.brown : C.mango, width: 0 } });
        s.addText(col.head, {
          x, y: y + 0.22, w: cw, h: 0.35,
          fontFace: SANS, fontSize: 11, bold: true, charSpacing: 1.6, color: C.carbon,
        });
        s.addText(col.bullets.map(b => ({
          text: b, options: { bullet: { code: '25AA' }, breakLine: true, paraSpaceAfter: 8 },
        })), {
          x, y: y + 0.68, w: cw, h: 2.1,
          fontFace: SANS, fontSize: 11.5, color: C.muted, valign: 'top', lineSpacingMultiple: 1.22, fit: 'shrink',
        });
      });
      if (sl.foot) {
        s.addText(sl.foot, {
          x: M, y: 5.55, w: W - 2 * M, h: 0.8,
          fontFace: SANS, fontSize: 11.5, italic: true, color: C.brown, valign: 'top', lineSpacingMultiple: 1.2,
        });
      }
    }
  });

  return p.writeFile({ fileName: outFile });
}

// ---------------------------------------------------------------- html
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

function buildHtml(outFile) {
  const slideHtml = SLIDES.map((sl, i) => {
    const dark = ['stats', 'title', 'end'].includes(sl.type);
    const bg = sl.type === 'split' ? 'var(--paper)' : dark ? 'var(--carbon)' : 'var(--cloud)';
    const num = `<div class="num">${String(i + 1).padStart(2, '0')}</div><div class="brandmark">GARNSH</div>`;
    const kick = sl.kicker ? `<div class="kicker"><span></span>${esc(sl.kicker)}</div>` : '';

    if (sl.type === 'title') {
      return `<section class="slide dark" style="background:${bg}">
        ${kick}
        <h1 class="mega">${esc(sl.title)}</h1>
        <div class="sub">${esc(sl.subtitle)}</div>
        <div class="rule"></div>
        <p class="lede">${esc(sl.body)}</p>
        <div class="foot-r">${esc(sl.foot)}</div>${num}</section>`;
    }
    if (sl.type === 'end') {
      return `<section class="slide dark" style="background:${bg}">${kick}
        <h1 class="mega2">${sl.title.split('\n').map(esc).join('<br>')}</h1>
        <div class="sub">${esc(sl.body)}</div><div class="foot-l">${esc(sl.foot)}</div>${num}</section>`;
    }

    const stats = sl.stats ? `<div class="stats">${sl.stats.map(s =>
      `<div><div class="sv">${esc(s.value)}</div><div class="sl">${esc(s.label)}</div></div>`).join('')}</div>` : '';

    const bullets = (arr, cls) => `<ul class="${cls}">${arr.map(b => typeof b === 'string'
      ? `<li>${esc(b)}</li>`
      : `<li><b>${esc(b.label)}</b> ${esc(b.text)}</li>`).join('')}</ul>`;

    if (sl.type === 'cards') {
      return `<section class="slide" style="background:${bg}">${kick}
        <h2 class="head">${sl.title.split('\n').map(esc).join('<br>')}</h2>
        <div class="cards">${sl.cards.map(c => `<div class="card"><h3>${esc(c.head)}</h3><p>${esc(c.text)}</p></div>`).join('')}</div>
        ${sl.foot ? `<p class="note">${esc(sl.foot)}</p>` : ''}${num}</section>`;
    }
    if (sl.type === 'table') {
      const t = sl.table;
      return `<section class="slide" style="background:${bg}">${kick}
        <h2 class="head">${sl.title}</h2>
        <table><thead><tr>${t.head.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead>
        <tbody>${t.rows.map(r => `<tr>${r.map((c, j) => `<td${j === 0 ? ' class="k"' : ''}>${esc(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>
        ${sl.bullets ? bullets(sl.bullets, 'bul') : ''}${num}</section>`;
    }
    if (sl.type === 'split') {
      return `<section class="slide" style="background:${bg}">${kick}
        <h2 class="head">${sl.title.split('\n').map(esc).join('<br>')}</h2>
        <div class="cols">
          <div><div class="colh">${esc(sl.colA.head)}</div>${bullets(sl.colA.bullets, 'bul sm')}</div>
          <div><div class="colh amber">${esc(sl.colB.head)}</div>${bullets(sl.colB.bullets, 'bul sm')}</div>
        </div>
        ${sl.foot ? `<p class="note">${esc(sl.foot)}</p>` : ''}${num}</section>`;
    }
    return `<section class="slide${dark ? ' dark' : ''}" style="background:${bg}">${kick}
      <h2 class="head">${sl.title.split('\n').map(esc).join('<br>')}</h2>
      ${sl.lead ? `<p class="lead">${esc(sl.lead)}</p>` : ''}
      ${bullets(sl.bullets, 'bul')}${stats}${num}</section>`;
  }).join('\n');

  const html = `<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<title>Garnsh — Pitch Deck</title>
<style>
@font-face{font-family:Manrope;font-weight:400;src:url(fonts/Manrope-400.ttf)}
@font-face{font-family:Manrope;font-weight:500;src:url(fonts/Manrope-500.ttf)}
@font-face{font-family:Manrope;font-weight:700;src:url(fonts/Manrope-700.ttf)}
@font-face{font-family:Manrope;font-weight:800;src:url(fonts/Manrope-800.ttf)}
@font-face{font-family:Fraunces;font-weight:400;src:url(fonts/Fraunces-400.ttf)}
@font-face{font-family:Fraunces;font-weight:600;src:url(fonts/Fraunces-600.ttf)}
@font-face{font-family:Fraunces;font-weight:700;src:url(fonts/Fraunces-700.ttf)}
:root{--mango:#FFBF1F;--carbon:#151515;--cloud:#FFFDF8;--paper:#F6F2E7;--green:#22C878;
--tomato:#FF644B;--brown:#2E2118;--muted:#5E5E5A;--line:#D9D7D0}
@page{size:13.333in 7.5in;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Manrope,sans-serif;-webkit-font-smoothing:antialiased}
.slide{width:13.333in;height:7.5in;padding:0.72in 0.85in 0.6in;position:relative;
page-break-after:always;overflow:hidden;display:block}
.slide:last-child{page-break-after:auto}
.kicker{display:flex;align-items:center;font-size:10.5pt;font-weight:700;
letter-spacing:.14em;color:var(--brown);margin-bottom:.42in}
.kicker span{display:inline-block;width:.28in;height:3px;background:var(--mango);margin-right:.16in}
.dark .kicker{color:var(--mango)}
.head{font-family:Fraunces,serif;font-weight:700;font-size:27pt;line-height:1.08;
color:var(--carbon);margin-bottom:.2in;max-width:11.2in}
.dark .head{color:var(--cloud)}
.mega{font-family:Fraunces,serif;font-weight:700;font-size:64pt;line-height:1;color:var(--cloud);margin-top:.35in}
.mega2{font-family:Fraunces,serif;font-weight:700;font-size:38pt;line-height:1.12;color:var(--cloud);margin-top:1.1in}
.sub{font-family:Manrope,sans-serif;font-weight:700;font-size:19pt;color:var(--mango);margin-top:.12in}
.rule{width:1.6in;height:3px;background:var(--mango);margin:.3in 0}
.lede{font-size:11pt;line-height:1.5;color:#C9C4B8;max-width:10.4in}
.lead{font-size:11.5pt;line-height:1.45;color:var(--brown);max-width:10.8in;margin-bottom:.24in;font-weight:500}
.bul{list-style:none;max-width:11.3in}
.bul li{position:relative;padding-left:.26in;margin-bottom:.15in;font-size:10.5pt;line-height:1.42;color:var(--muted)}
.bul li:before{content:"";position:absolute;left:0;top:.045in;width:5px;height:5px;background:var(--mango)}
.bul li b{color:var(--brown);font-weight:700}
.dark .bul li{color:#C9C4B8}
.dark .bul li b{color:var(--mango)}
.bul.sm li{font-size:9.8pt}
.stats{display:flex;margin-top:.42in}
.stats>div{flex:1;border-top:3px solid var(--mango);padding-top:.14in}
.stats>div:not(:last-child){margin-right:.3in}
.sv{font-family:Fraunces,serif;font-weight:700;font-size:26pt;color:var(--carbon);line-height:1.05}
.dark .sv{color:var(--mango)}
.sl{font-size:9pt;color:var(--muted);margin-top:.06in;line-height:1.3}
.dark .sl{color:#C9C4B8}
.cards{display:flex;margin-top:.3in}
.card{flex:1;background:var(--paper);border:1px solid var(--line);border-radius:4px;
border-top:3px solid var(--mango);padding:.26in .24in}
.card:not(:last-child){margin-right:.3in}
.card h3{font-family:Manrope;font-size:12pt;font-weight:700;color:var(--carbon);margin-bottom:.1in}
.card p{font-size:9.6pt;line-height:1.45;color:var(--muted)}
table{width:100%;border-collapse:collapse;margin-top:.16in}
th{background:var(--carbon);color:var(--cloud);font-size:9.2pt;font-weight:700;text-align:left;
padding:.11in .1in;letter-spacing:.03em}
td{font-size:9.2pt;padding:.1in;border-bottom:1px solid var(--line);color:var(--muted);background:var(--cloud)}
tr:nth-child(even) td{background:var(--paper)}
td.k{color:var(--carbon);font-weight:700}
.cols{display:flex;margin-top:.28in}
.cols>div{flex:1}
.cols>div:not(:last-child){margin-right:.45in}
.colh{font-size:10pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
color:var(--carbon);border-top:3px solid var(--brown);padding-top:.1in;margin-bottom:.16in}
.colh.amber{border-top-color:var(--mango)}
.note{font-size:9.6pt;font-style:italic;line-height:1.4;color:var(--brown);margin-top:.3in;max-width:11.3in}
.num{position:absolute;right:.85in;bottom:.3in;font-size:9pt;color:var(--muted)}
.dark .num{color:#7A7368}
.brandmark{position:absolute;left:.85in;bottom:.3in;font-size:9pt;font-weight:700;
letter-spacing:.16em;color:var(--muted)}
.dark .brandmark{color:#7A7368}
.foot-r{position:absolute;right:.85in;bottom:1.05in;font-size:9pt;color:#7A7368}
.foot-l{position:absolute;left:.85in;bottom:1.2in;font-size:10pt;color:#7A7368}
</style></head><body>
${slideHtml}
</body></html>`;
  fs.writeFileSync(outFile, html);
  console.log('HTML written:', outFile, `(${SLIDES.length} slides)`);
}

const dir = __dirname;
buildPptx(path.join(dir, 'garnsh-pitch-deck.pptx'))
  .then(() => console.log('PPTX written:', path.join(dir, 'garnsh-pitch-deck.pptx')))
  .catch(e => { console.error('pptx failed:', e); process.exit(1); });
buildHtml(path.join(dir, 'deck.html'));
