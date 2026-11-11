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
    kicker: 'MENU PUBLISHING AND CONTROL FOR MULTI-LOCATION RESTAURANT GROUPS',
    title: 'Garnsh',
    subtitle: 'One menu. Every location. Published on purpose.',
    body: 'A controlled publishing layer for restaurant groups on Toast: prepare the menu once, preview every surface, publish per location, and roll back if something is wrong.',
    foot: 'Investor Deck v3.1 · November 2026 · Pre-revenue',
  },
  {
    type: 'content',
    kicker: 'THE PROBLEM',
    title: 'One menu. Four surfaces.\nNone guaranteed to agree.',
    lead: 'A 10-location group maintains one menu in Toast and presents it on the website, a hosted page, QR codes and in-store boards — usually by hand.',
    bullets: [
      { label: 'Price drift', text: 'Toast says $16.25; the website says $14.50.' },
      { label: 'Dead items', text: 'Discontinued items and last season’s menu linger for weeks.' },
      { label: 'Wrong location', text: 'One location’s prices or items appear at another.' },
      { label: 'No safety net', text: 'A bad publish leaves a blank board during service.' },
    ],
    foot: 'This is a described problem from founder research. No customer has been signed and no live location exists.',
  },
  {
    type: 'content',
    kicker: 'TARGET CUSTOMER',
    title: '10–50 location Toast groups\nwith a brand to protect.',
    bullets: [
      { label: 'ICP', text: 'Regional fast-casual and casual-dining groups, all on Toast, with a named owner for menu presentation.' },
      { label: 'Buyer', text: 'VP of Marketing, Director of Operations, or the founder-operator.' },
      { label: 'Trigger', text: 'A price change, rebrand, new location, menu cycle or agency handover.' },
      { label: 'Why now', text: 'Menu data is a discovery asset, signage is cheap, and labor turnover keeps recreating the manual updater.' },
    ],
    foot: 'Below 10 locations the budget is small. Above 50 the security review exceeds a two-person team.',
  },
  {
    type: 'cards',
    kicker: 'SOLUTION',
    title: 'Publish once. Preview everything.\nRoll back if wrong.',
    cards: [
      { head: 'One menu document', text: 'Ingest from Toast or CSV/Sheets. Normalize items, modifiers, prices and location variants.' },
      { head: 'Per-location control', text: 'Map every surface to the right location, with overrides and a group dashboard.' },
      { head: 'Publishing safety', text: 'Preview, deliberate publish, version history, rollback and last-known-good serving.' },
    ],
    foot: 'Gen 1 is menu publishing: not ordering, payments, live inventory or real-time sync.',
  },
  {
    type: 'content',
    kicker: 'PRODUCT',
    title: 'Four surfaces. One source of truth.',
    lead: 'Ingest → normalize → map → preview → publish → serve.',
    bullets: [
      { label: 'Website embed', text: 'The group’s own site, styled to the brand.' },
      { label: 'Hosted page', text: 'A Garnsh-hosted menu per location.' },
      { label: 'QR menu', text: 'A phone view opened by a printed code.' },
      { label: 'Menu boards', text: 'In-store screens fed from the same published version.' },
    ],
    foot: 'Demo today: per-location rendering, preview/publish, version history, rollback. Production build: 10–12 weeks. No customer screenshots are presented as live.',
  },
  {
    type: 'content',
    kicker: 'DIFFERENTIATION',
    title: 'The wedge is publishing discipline,\nnot menu rendering.',
    bullets: [
      { label: 'Version history', text: 'Every publish is recorded; one click rolls back.' },
      { label: 'Last-known-good', text: 'A broken upstream source serves the last good menu, not a blank board.' },
      { label: 'Per-location mapping', text: 'Prices, items and overrides follow the location, not the template.' },
      { label: 'Keep the stack', text: 'No change to POS, website or ordering vendor.' },
    ],
    foot: 'Marqii owns distribution, Popmenu and BentoBox own the website, Owner.com and ChowNow own ordering. None sells publishing control as the product.',
  },
  {
    type: 'stats',
    kicker: 'MARKET',
    title: '$14–28M Gen 1 market.\n3–6% share is a real business.',
    stats: [
      { value: '189K', label: 'Toast locations, Q3 2026' },
      { value: '19–38K', label: 'in 10+ location groups (modeled)' },
      { value: '$14–28M', label: 'Gen 1 market at $61/location' },
      { value: '1,182', label: 'locations in the 2029 plan' },
    ],
    bullets: [
      { label: 'Bottom-up', text: '189,000 locations × 10–20% in 10+ groups × $61/month.' },
      { label: 'Excluded', text: 'Ordering, apps and payments are upside, not the base case.' },
      { label: 'Honest limit', text: 'The 10–20% band is a management estimate; Toast does not publish the breakdown.' },
    ],
  },
  {
    type: 'table',
    kicker: 'BUSINESS MODEL',
    title: '$59 per location. $40 for boards.\nSetup at cost.',
    table: {
      head: ['Item', 'Price', 'Basis'],
      rows: [
        ['Core publishing', '$59 / location / month', 'Per location'],
        ['Menu boards', '+$40 / location / month', 'Locations with screens'],
        ['Onboarding', '$120 / location, $1,500 min', '2h at $60/h — cost recovery'],
        ['Gen 2 ordering', '+$99 / location / month', 'Conditional on certification'],
        ['Gen 3 app', '$5,000 build + $149 / location / month', 'Conditional; 25+ locations'],
      ],
      colW: [3.2, 4.6, 3.8],
    },
    bullets: [
      { label: '14-location group', text: '$826/month core; $1,386 with boards at every location; $1,680 onboarding.' },
      { label: 'v3.1 change', text: 'The flat $1,500 fee lost $180 at 14 locations and $3,300 at 40. The fee now scales with the work.' },
    ],
  },
  {
    type: 'stats',
    kicker: 'VALIDATION',
    title: 'Pre-revenue. Zero signed.\nThe next 90 days are the test.',
    stats: [
      { value: '0', label: 'signed design partners' },
      { value: '0', label: 'live locations' },
      { value: '0', label: 'paying customers' },
      { value: '15', label: 'target groups in 2027' },
    ],
    bullets: [
      { label: 'Plan', text: '60 qualified conversations → 24 paid pilots → 15 groups: 4 free for 90 days, 6 at 20% for six months, 5 at list.' },
      { label: 'Integrity', text: 'No logos, testimonials or pilot results are claimed. Reference rights are contractual, not assumed.' },
      { label: 'Purpose', text: 'The first ten groups replace founder assumptions with cohort data.' },
    ],
  },
  {
    type: 'content',
    kicker: 'GO-TO-MARKET',
    title: 'Founder-led. Agency-assisted.\nNo paid acquisition.',
    bullets: [
      { label: 'Funnel', text: '60 conversations → 24 pilots → 15 gross groups at a 25% close rate.' },
      { label: 'Pilot', text: '30 days, 3 locations, $59/location; setup charged on conversion.' },
      { label: 'Design partners', text: 'Four groups free for 90 days; six at 20% off for six months. Program cost $30.6K, not $91.3K.' },
      { label: 'Agencies', text: '25% recurring revenue share. They already handle menu updates and dislike it.' },
    ],
    foot: 'A paid channel at $10–15K per group cannot be funded from $20,000 — the constraint is cash, not LTV.',
  },
  {
    type: 'stats',
    kicker: 'UNIT ECONOMICS',
    title: 'One 14-location group:\n1.3-month payback.',
    stats: [
      { value: '$1,372', label: 'monthly revenue' },
      { value: '$1,221', label: 'recurring gross profit' },
      { value: '$1,590', label: 'CAC, fully loaded' },
      { value: '1.3 mo', label: 'payback on upfront investment' },
    ],
    bullets: [
      { label: 'Definitions', text: 'Upfront investment = CAC + unrecovered onboarding ($0 at cost-recovery pricing).' },
      { label: 'LTV', text: '38.4x CAC at 2.0% monthly churn; 21.9x at 3.5%. Modeled, with no cohort to test it.' },
      { label: 'Caution', text: 'A 38x ratio is an assumption set, not a benchmark. The binding constraint is founder time and cash.' },
    ],
  },
  {
    type: 'table',
    kicker: 'FINANCIAL PLAN',
    title: 'Cash-positive in 2027 only because\nfounders work unpaid.',
    table: {
      head: ['', '2027', '2028', '2029'],
      rows: [
        ['Revenue', '$46K', '$361K', '$919K'],
        ['Economic result', '−$17K', '+$82K', '+$233K'],
        ['Cash from operations', '+$26K', '+$143K', '+$326K'],
        ['Year-end cash', '$46K', '$188K', '$514K'],
        ['Net groups', '14', '46', '90'],
        ['Exit ARR', '$130K', '$577K', '$1.18M'],
      ],
      colW: [4.2, 2.4, 2.4, 2.6],
    },
    bullets: [
      { label: 'Cash floor', text: '$6,750 at the April trough, $1,750 above the $5,000 reserve — with $25,200 of founder onboarding imputed at $60/hour.' },
      { label: 'Gen 1 only', text: 'No ordering or app revenue. Paid 2027 onboarding breaches the reserve by about $6.9K; the combined stress needs a $25–30K bridge.' },
    ],
  },
  {
    type: 'table',
    kicker: 'COMPETITION',
    title: 'Everyone solves a different part.\nNobody sells publishing control.',
    table: {
      head: ['Player', 'What they sell', 'Price signal', 'Basis'],
      rows: [
        ['Toast native', 'Website, ordering, boards', 'Bundled / not disclosed', 'Per location'],
        ['Marqii', 'Menu + listings distribution', '$90–$250/mo', 'Per location, annual'],
        ['Popmenu', 'Website, menu, marketing', '$179–$499/mo', 'Per location'],
        ['BentoBox', 'Website and ordering', '$119–$479/mo', 'Per location'],
        ['Owner.com / ChowNow', 'Ordering and websites', '$249–$499/mo; from $229', 'Per restaurant'],
        ['Agencies', 'Custom sites, manual updates', 'Quote-based', 'Project + retainer'],
      ],
      colW: [2.3, 3.4, 3.2, 2.7],
      cellSize: 9.5,
      rowH: 0.44,
    },
    bullets: [
      { label: 'The opening', text: 'Versioned, per-location publishing on the site the group already owns — without changing POS, website or ordering vendor.' },
      { label: 'The incumbent', text: 'The agency, not another SaaS product. Prices captured 11 Nov 2026 from vendor pricing pages.' },
    ],
  },
  {
    type: 'cards',
    kicker: 'ROADMAP & RISKS',
    title: 'Gen 1 is the company.\nGen 2 is an option.',
    cards: [
      { head: 'Gen 1 · 2027', text: 'Menu publishing. The only product in the base case. 14 net groups, 192 locations, $46K revenue.' },
      { head: 'Gen 2 · 2028', text: 'Ordering on the group’s own site. Gated on Toast certification. Costs $65K before it earns a dollar.' },
      { head: 'Gen 3 · 2029', text: 'Branded app and commerce. Optional, funded from revenue, only after proof.' },
    ],
    foot: 'Critical path: the day-120 Toast gate. Fail means import-first and a re-plan. The combined stress is insolvent by May without a cost response.',
  },
  {
    type: 'split',
    kicker: 'TEAM & ASK',
    title: 'Two founders. $20,000.\nA deliberately narrow wedge.',
    colA: {
      head: 'THE TEAM',
      bullets: [
        'Two partners, $10,000 each, equal vesting.',
        'Build lead and sales lead; each owns two of four functions.',
        'Founder names, backgrounds and time commitment: to be completed before external circulation.',
      ],
    },
    colB: {
      head: 'THE ASK',
      bullets: [
        'Not raising now.',
        'Raise after 10 paying groups, ~140 locations, six months of churn data and a clear Toast status.',
        'If the founders cannot perform 2027 onboarding, the bridge is about $7K — a note, not a round.',
      ],
    },
    foot: 'The $20,000 works only if the founders perform 2027 onboarding. That is the plan’s binding constraint.',
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
          options: { bold: true, color: C.cloud, fill: { color: C.carbon }, fontSize: sl.cellSize ? sl.cellSize + 0.5 : 11, fontFace: SANS },
        })),
        ...t.rows.map((r, ri) => r.map((cell, ci) => ({
          text: cell,
          options: {
            color: ci === 0 ? C.carbon : C.muted,
            bold: ci === 0,
            fontSize: sl.cellSize || 10.5,
            fontFace: SANS,
            fill: { color: ri % 2 === 0 ? C.cloud : C.paper },
          },
        }))),
      ];
      s.addTable(rows, {
        x: M, y, w: W - 2 * M, colW: t.colW,
        border: { type: 'solid', color: C.line, pt: 0.75 },
        rowH: sl.rowH || 0.42, valign: 'middle', margin: 0.09,
      });
      const tblH = (sl.rowH || 0.42) * (t.rows.length + 1);
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

    if (sl.foot && ['content','stats','table'].includes(sl.type)) {
      s.addText(sl.foot, {
        x: M, y: H - 1.08, w: W - 2 * M, h: 0.5,
        fontFace: SANS, fontSize: 10.5, italic: true, color: C.brown,
        valign: 'bottom', fit: 'shrink', lineSpacingMultiple: 1.1,
      });
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
        ${sl.bullets ? bullets(sl.bullets, 'bul') : ''}${sl.foot ? `<p class="note">${esc(sl.foot)}</p>` : ''}${num}</section>`;
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
      ${bullets(sl.bullets, 'bul')}${stats}${sl.foot ? `<p class="note">${esc(sl.foot)}</p>` : ''}${num}</section>`;
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
