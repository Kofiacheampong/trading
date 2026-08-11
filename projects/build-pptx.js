const pptxgen = require('pptxgenjs');

const p = new pptxgen();
p.defineLayout({ name: 'WIDE', width: 13.333, height: 7.5 });
p.layout = 'WIDE';

const colors = {
  bg: '0A0A0A',
  gold: 'F59E0B',
  green: '10B981',
  blue: '3B82F6',
  purple: '8B5CF6',
  red: 'EF4444',
  white: 'FFFFFF',
  gray: '666666',
  ltGray: '999999',
};

function addSlideNum(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 11.8, y: 6.9, w: 1.2, h: 0.4,
    fontSize: 11, color: '333333', align: 'right', fontFace: 'Inter',
  });
}

function addTag(slide, text, x, y) {
  slide.addShape(p.ShapeType.roundRect, {
    x, y, w: text.length * 7.5 + 24, h: 0.35,
    fill: { color: 'F59E0B', transparency: 85 },
    rectRadius: 0.175,
  });
  slide.addText(text.toUpperCase(), {
    x, y, w: text.length * 7.5 + 24, h: 0.35,
    fontSize: 9, color: colors.gold, align: 'center', fontFace: 'Inter', bold: true,
    letterSpacing: 1,
  });
}

// =========== SLIDE 1: TITLE ===========
const s1 = p.addSlide();
s1.background = { fill: colors.bg };
addSlideNum(s1, 1, 13);
addTag(s1, 'Franchise Pitch Deck', 0.8, 1.0);
s1.addText('Afro Deli', {
  x: 0.8, y: 1.6, w: 8, h: 1.2,
  fontSize: 56, fontFace: 'Inter', bold: true, color: colors.white,
});
s1.addText('Woodbury, MN', {
  x: 0.8, y: 2.7, w: 8, h: 0.9,
  fontSize: 56, fontFace: 'Inter', bold: true,
  color: 'F59E0B',
});
s1.addText('African-Mediterranean Fusion — East Metro Expansion', {
  x: 0.8, y: 3.7, w: 7, h: 0.5,
  fontSize: 18, fontFace: 'Inter', color: '888888',
});
s1.addText('A fast-casual franchise opportunity in an affluent, fast-growing suburb with zero direct competition. Projections calibrated against actual operational data from 3 existing locations.', {
  x: 0.8, y: 4.3, w: 7, h: 0.7,
  fontSize: 13, fontFace: 'Inter', color: '777777',
});
s1.addShape(p.ShapeType.line, { x: 0.8, y: 5.3, w: 3, h: 0, line: { color: '333333', width: 1 } });
const info1 = [
  ['FRANCHISE', 'Afro Deli'],
  ['OWNER-OPERATOR', 'Koo Ok'],
  ['TOTAL INVESTMENT', '$600,000'],
  ['DATE', 'June 2026'],
];
info1.forEach((r, i) => {
  s1.addText(r[0], { x: 0.8 + i * 2.3, y: 5.6, w: 2.2, h: 0.3, fontSize: 10, color: '555555', fontFace: 'Inter' });
  s1.addText(r[1], { x: 0.8 + i * 2.3, y: 5.9, w: 2.2, h: 0.3, fontSize: 14, color: colors.white, fontFace: 'Inter', bold: true });
});

// =========== SLIDE 2: CONCEPT ===========
const s2 = p.addSlide();
s2.background = { fill: colors.bg };
addSlideNum(s2, 2, 13);
s2.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 0.4, w: 0.3, h: 0.3,
  fill: { color: colors.gold },
  rectRadius: 0.15,
});
s2.addText('Concept Overview', { x: 1.3, y: 0.4, w: 6, h: 0.4, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });
s2.addText('Afro Deli is a fast-casual fusion restaurant weaving African, Mediterranean, and American cuisine in a fast, fun, family-friendly environment.\n\nAll dishes made fresh, prepared Halal, rooted in a social enterprise mission. 3 locations operating 12+ years in the Twin Cities.', {
  x: 0.8, y: 1.2, w: 5.5, h: 2.0, fontSize: 13, fontFace: 'Inter', color: 'AAAAAA', lineSpacing: 18,
});
// KPIs
const kpis2 = [
  { v: '3', l: 'Existing Locations', c: colors.gold },
  { v: '$1.37M', l: 'Combined Annual Net Sales', c: colors.green },
  { v: '25.7%', l: 'Catering Share (actual)', c: colors.green },
];
kpis2.forEach((k, i) => {
  s2.addShape(p.ShapeType.roundRect, {
    x: 0.8 + i * 2.2, y: 3.5, w: 2.0, h: 1.3,
    fill: { color: colors.white, transparency: 96 },
    rectRadius: 0.12,
    line: { color: '222222', width: 1 },
  });
  s2.addText(k.v, { x: 0.8 + i * 2.2, y: 3.6, w: 2.0, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: k.c, align: 'center' });
  s2.addText(k.l, { x: 0.8 + i * 2.2, y: 4.2, w: 2.0, h: 0.4, fontSize: 11, fontFace: 'Inter', color: '777777', align: 'center' });
});
// Menu card
s2.addShape(p.ShapeType.roundRect, {
  x: 7.0, y: 1.0, w: 5.5, h: 3.8,
  fill: { color: 'F59E0B', transparency: 94 },
  rectRadius: 0.16,
  line: { color: 'F59E0B', transparency: 85, width: 1 },
});
s2.addText('Menu Highlights', { x: 7.4, y: 1.2, w: 4, h: 0.5, fontSize: 15, fontFace: 'Inter', bold: true, color: colors.white });
const menuItems = [
  '✦ Chicken Fantastic — Somali rice, creole sauce',
  '✦ Sambusas (beef, chicken, veggie) — fan favorite',
  '✦ Lamb & Chicken Gyros — spiced rotisserie',
  '✦ Spiced Bowls — proteins over Somali rice',
  '✦ Falafel / Hummus — strong vegan options',
];
menuItems.forEach((t, i) => {
  s2.addText(t, { x: 7.4, y: 1.9 + i * 0.45, w: 4.8, h: 0.4, fontSize: 12, fontFace: 'Inter', color: 'BBBBBB' });
});
s2.addShape(p.ShapeType.roundRect, {
  x: 7.0, y: 5.1, w: 5.5, h: 1.0,
  fill: { color: '10B981', transparency: 94 },
  rectRadius: 0.12,
  line: { color: '10B981', transparency: 88, width: 1 },
});
s2.addText('📊 Actual Avg Ticket: $15.89 | Turn Time: 17.8 min | 17.1% from 3rd-party delivery', {
  x: 7.4, y: 5.3, w: 4.8, h: 0.6, fontSize: 11, fontFace: 'Inter', color: '999999',
});

// =========== SLIDE 3: MARKET SELECTION ===========
const s3 = p.addSlide();
s3.background = { fill: colors.bg };
addSlideNum(s3, 3, 13);
s2.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 0.4, w: 0.3, h: 0.3,
  fill: { color: colors.gold },
  rectRadius: 0.15,
});
s3.addText('Market Selection', { x: 1.3, y: 0.4, w: 6, h: 0.4, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });
s3.addText('Three Twin Cities suburbs evaluated. One clear winner.', { x: 0.8, y: 0.9, w: 8, h: 0.4, fontSize: 14, fontFace: 'Inter', color: '888888' });

// Table
const tableRows = [
  [{ text: 'Factor', options: { bold: true, color: colors.gold, fontSize: 11, fontFace: 'Inter' } },
   { text: '📍 Woodbury', options: { bold: true, color: colors.gold, fontSize: 11, fontFace: 'Inter' } },
   { text: 'Minnetonka', options: { bold: true, color: '888888', fontSize: 11, fontFace: 'Inter' } },
   { text: 'Edina', options: { bold: true, color: '888888', fontSize: 11, fontFace: 'Inter' } }],
  [{ text: 'Population', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '~75,000', options: { bold: true, color: colors.white, fontSize: 11, fontFace: 'Inter' } },
   { text: '~55,000', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '~54,000', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } }],
  [{ text: 'Growth (2020–25)', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '+12%', options: { bold: true, color: colors.green, fontSize: 11, fontFace: 'Inter' } },
   { text: '+4%', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '+3%', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } }],
  [{ text: 'Median Income', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '$117,000', options: { bold: true, color: colors.white, fontSize: 11, fontFace: 'Inter' } },
   { text: '$105,000', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '$120,000', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } }],
  [{ text: 'Daytime Surge', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: 'Strong (medical+retail)', options: { bold: true, color: colors.white, fontSize: 11, fontFace: 'Inter' } },
   { text: 'Moderate', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: 'Moderate', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } }],
  [{ text: 'Med Competition', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: 'None (gap)', options: { bold: true, color: colors.green, fontSize: 11, fontFace: 'Inter' } },
   { text: 'None', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: 'None', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } }],
  [{ text: 'Lease ($/sq ft)', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '$20–$25', options: { bold: true, color: colors.white, fontSize: 11, fontFace: 'Inter' } },
   { text: '$22–$28', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '$28–$35', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } }],
  [{ text: 'Permitting', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '4–6 weeks', options: { bold: true, color: colors.white, fontSize: 11, fontFace: 'Inter' } },
   { text: '6–10 weeks', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } },
   { text: '8–12 weeks', options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } }],
];
s3.addTable(tableRows, {
  x: 0.8, y: 1.5, w: 11.7,
  colW: [2.5, 3.5, 2.5, 2.5],
  rowH: [0.45, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35, 0.35],
  border: { type: 'solid', pt: 0.5, color: '222222' },
  autoPage: false,
});

// Ranking cards
const ranks = [
  { v: '#1', l: 'Woodbury — Primary', c: colors.green },
  { v: '#2', l: 'Minnetonka — Year 3–5', c: colors.gold },
  { v: '#3', l: 'Edina — Future', c: '666666' },
];
ranks.forEach((r, i) => {
  s3.addShape(p.ShapeType.roundRect, {
    x: 0.8 + i * 4.0, y: 5.2, w: 3.6, h: 1.2,
    fill: { color: colors.white, transparency: 96 },
    rectRadius: 0.12,
    line: { color: '222222', width: 1 },
  });
  s3.addText(r.v, { x: 0.8 + i * 4.0, y: 5.3, w: 3.6, h: 0.5, fontSize: 24, fontFace: 'Inter', bold: true, color: r.c, align: 'center' });
  s3.addText(r.l, { x: 0.8 + i * 4.0, y: 5.8, w: 3.6, h: 0.4, fontSize: 13, fontFace: 'Inter', color: '888888', align: 'center' });
});

// =========== SLIDE 4: DEMOGRAPHICS ===========
const s4 = p.addSlide();
s4.background = { fill: colors.bg };
addSlideNum(s4, 4, 13);
s4.addText('Woodbury Demographics', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });
s4.addText('Affluent, fast-growing — the perfect launchpad.', { x: 0.8, y: 1.0, w: 8, h: 0.4, fontSize: 14, fontFace: 'Inter', color: '888888' });

const demos = [
  { v: '75K', l: 'Population', n: '+12% since 2020', c: colors.green },
  { v: '$117K', l: 'Median Income', n: 'Well above metro', c: colors.gold },
  { v: '38%', l: 'Families w/ Kids', n: 'Primary dinner target', c: colors.blue },
  { v: '30–40%', l: 'Daytime Surge', n: 'Medical+retail+office', c: colors.purple },
];
demos.forEach((d, i) => {
  const x = 0.8 + i * 3.1;
  s4.addShape(p.ShapeType.roundRect, {
    x, y: 1.6, w: 2.8, h: 1.8,
    fill: { color: colors.white, transparency: 96 },
    rectRadius: 0.16,
    line: { color: '222222', width: 1 },
  });
  s4.addText(d.v, { x, y: 1.7, w: 2.8, h: 0.6, fontSize: 32, fontFace: 'Inter', bold: true, color: d.c, align: 'center' });
  s4.addText(d.l, { x, y: 2.3, w: 2.8, h: 0.4, fontSize: 14, fontFace: 'Inter', bold: true, color: colors.white, align: 'center' });
  s4.addText(d.n, { x, y: 2.65, w: 2.8, h: 0.4, fontSize: 10, fontFace: 'Inter', color: '888888', align: 'center' });
});

// Target segments card
s4.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 3.7, w: 5.8, h: 2.8,
  fill: { color: colors.white, transparency: 96 },
  rectRadius: 0.16,
  line: { color: '222222', width: 1 },
});
s4.addText('Target Segments', { x: 1.2, y: 3.9, w: 5, h: 0.4, fontSize: 16, fontFace: 'Inter', bold: true, color: colors.white });
const segs = [
  'Primary (50%) — Families with kids 6–17',
  'Catering (25%) — Corporate, medical, schools (25.7% actual)',
  'Professionals (15%) — Affluent couples, global seekers',
  'Daytime + Delivery (10%) — Lunch workforce + 17.1% delivery',
];
segs.forEach((s, i) => s4.addText('✦ ' + s, { x: 1.2, y: 4.4 + i * 0.45, w: 5, h: 0.4, fontSize: 12, fontFace: 'Inter', color: 'AAAAAA' }));

// Site criteria card
s4.addShape(p.ShapeType.roundRect, {
  x: 7.0, y: 3.7, w: 5.5, h: 2.8,
  fill: { color: colors.white, transparency: 96 },
  rectRadius: 0.16,
  line: { color: '222222', width: 1 },
});
s4.addText('Ideal Site Criteria', { x: 7.4, y: 3.9, w: 4.5, h: 0.4, fontSize: 16, fontFace: 'Inter', bold: true, color: colors.white });
const sites = [
  '1,500–1,800 sq ft endcap/inline',
  'Power center near grocery anchor',
  '25,000+ VPD, street-facing signage',
  'Lease: $18–$25/sq ft NNN (~$4,200/mo)',
];
sites.forEach((s, i) => s4.addText('✦ ' + s, { x: 7.4, y: 4.4 + i * 0.45, w: 4.5, h: 0.4, fontSize: 12, fontFace: 'Inter', color: 'AAAAAA' }));

// =========== SLIDE 5: COMPETITOR LANDSCAPE ===========
const s5 = p.addSlide();
s5.background = { fill: colors.bg };
addSlideNum(s5, 5, 13);
s5.addText('Competitor Landscape', { x: 0.8, y: 0.4, w: 8, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });
s5.addText('Woodbury has a clear gap — Afro Deli fills it.', { x: 0.8, y: 1.0, w: 8, h: 0.4, fontSize: 14, fontFace: 'Inter', color: '888888' });

const compRows = [
  [{ text: 'Competitor', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter' } },
   { text: 'Category', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter' } },
   { text: 'Location', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter' } },
   { text: 'Afro Deli Advantage', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter' } }],
  ['Naf Naf Grill', 'Mediterranean', 'Tamarack Village', 'African spicing, sambusas, halal, brand story'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Chipotle', 'Mexican Grill', 'Woodbury Lakes', 'Unique flavor — Somali rice, spice blends'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Panera Bread', 'Bakery-Café', 'Valley Creek', 'Dinner-centric, bolder flavors, community mission'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Noodles & Co.', 'Global-Inspired', 'Woodbury Lakes', 'Authentic cuisine, halal commitment'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Crisp & Green', 'Health Fast-Casual', 'Woodbury Lakes', 'Warm bowls + gyros = comfort + nutrition'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
];
s5.addTable(compRows, {
  x: 0.8, y: 1.6, w: 11.7,
  colW: [2.2, 2.0, 2.5, 5.0],
  rowH: [0.4, 0.35, 0.35, 0.35, 0.35, 0.35],
  border: { type: 'solid', pt: 0.5, color: '222222' },
  autoPage: false,
});

// Key insight card
s5.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 4.5, w: 11.7, h: 1.2,
  fill: { color: 'F59E0B', transparency: 94 },
  rectRadius: 0.12,
  line: { color: 'F59E0B', transparency: 88, width: 1 },
});
s5.addText('💡 Key Insight: No competitor offers African-Med fusion, halal-first, or cultural storytelling. And none does 25.7% of revenue from catering.', {
  x: 1.2, y: 4.8, w: 11, h: 0.6, fontSize: 14, fontFace: 'Inter', color: 'BBBBBB',
});

// =========== SLIDE 6: SWOT ===========
const s6 = p.addSlide();
s6.background = { fill: colors.bg };
addSlideNum(s6, 6, 13);
s6.addText('SWOT Analysis', { x: 0.8, y: 0.4, w: 6, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });

const swotData = [
  { title: 'Strengths', color: colors.green, items: [
    'Proven model (3 locations, 12+ years)',
    '25.7% catering revenue — proven institutional',
    'Unique cuisine = zero direct competition',
    'All-halal = growing demand driver',
    '17.1% 3rd-party delivery (DoorDash, Uber, Grubhub)',
    'Strong community/social enterprise mission',
  ]},
  { title: 'Weaknesses', color: colors.red, items: [
    'First suburban expansion — new territory',
    'Limited Woodbury brand awareness vs nationals',
    'Royalty + marketing (8%) compresses margins',
    'No drive-thru (vs Panera, Chipotle)',
    'Owner-operator learning curve',
  ]},
  { title: 'Opportunities', color: colors.gold, items: [
    'Woodbury 12% growth = rising dining demand',
    'No African-Med fusion competitor',
    'Catering proven at 25.7% — larger Woodbury market',
    'Dinner only 16.1% → huge growth runway',
    'Growing halal demand across Metro',
    'Second location or Minnetonka Yr 3–5',
  ]},
  { title: 'Threats', color: colors.purple, items: [
    'Economic downturn reduces discretionary dining',
    'Halal protein cost inflation',
    'Labor market wage pressure',
    'Potential Cava entry into Woodbury',
    'Lease escalation at Yr 5–10 renewal',
  ]},
];

swotData.forEach((q, qi) => {
  const col = qi % 2;
  const row = Math.floor(qi / 2);
  const x = 0.8 + col * 6.3;
  const y = 1.2 + row * 3.0;

  s6.addShape(p.ShapeType.roundRect, {
    x, y, w: 5.9, h: 2.7,
    fill: { color: colors.white, transparency: 96 },
    rectRadius: 0.14,
    line: { color: q.color, transparency: 70, width: 1.5 },
  });
  s6.addShape(p.ShapeType.roundRect, {
    x, y, w: 0.06, h: 2.7,
    fill: { color: q.color },
    rectRadius: 0,
  });
  s6.addText(q.title, { x: x + 0.3, y: y + 0.1, w: 4, h: 0.4, fontSize: 15, fontFace: 'Inter', bold: true, color: q.color });
  q.items.forEach((item, i) => {
    s6.addText(item, { x: x + 0.3, y: y + 0.55 + i * 0.38, w: 5.2, h: 0.35, fontSize: 10.5, fontFace: 'Inter', color: 'AAAAAA' });
  });
});

// =========== SLIDE 7: FUNDING ===========
const s7 = p.addSlide();
s7.background = { fill: colors.bg };
addSlideNum(s7, 7, 13);
s7.addText('Funding Structure', { x: 0.8, y: 0.4, w: 6, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });

// Total cost card
s7.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 1.2, w: 5.8, h: 1.0,
  fill: { color: 'F59E0B', transparency: 94 },
  rectRadius: 0.14,
  line: { color: 'F59E0B', transparency: 85, width: 1 },
});
s7.addText('Total Project Cost:', { x: 1.2, y: 1.25, w: 4, h: 0.4, fontSize: 14, fontFace: 'Inter', color: 'AAAAAA' });
s7.addText('$600,000', { x: 1.2, y: 1.55, w: 3, h: 0.5, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.gold });

// Cost breakdown table
const costRows = [
  [{ text: 'Cost Category', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter' } },
   { text: 'Amount', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter', align: 'right' } }],
  ['Franchise Fee', '$35,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Leasehold Improvements (1,600 sq ft)', '$250,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['FF&E (Kitchen, POS, Seating)', '$135,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Permits, Licenses & Legal', '$15,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Technology & POS', '$10,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Initial Inventory & Smallwares', '$20,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Pre-Opening Marketing', '$25,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Professional Fees', '$15,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Insurance (Yr 1)', '$8,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Working Capital Reserve (6 mo)', '$87,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Contingency (5%)', '$30,000'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  [{ text: 'Total', options: { bold: true, color: colors.gold, fontSize: 11, fontFace: 'Inter' } },
   { text: '$600,000', options: { bold: true, color: colors.gold, fontSize: 11, fontFace: 'Inter', align: 'right' } }],
];
s7.addTable(costRows, {
  x: 0.8, y: 2.5, w: 5.8,
  colW: [4.0, 1.8],
  rowH: [0.35, ...Array(11).fill(0.28), 0.35],
  border: { type: 'solid', pt: 0.5, color: '222222' },
  autoPage: false,
});

// Capital stack
s7.addShape(p.ShapeType.roundRect, {
  x: 7.0, y: 1.2, w: 5.5, h: 5.2,
  fill: { color: colors.white, transparency: 96 },
  rectRadius: 0.14,
  line: { color: '222222', width: 1 },
});
s7.addText('Capital Stack', { x: 7.4, y: 1.3, w: 4, h: 0.4, fontSize: 16, fontFace: 'Inter', bold: true, color: colors.white });

// Equity box
s7.addShape(p.ShapeType.roundRect, {
  x: 7.4, y: 1.9, w: 2.2, h: 1.5,
  fill: { color: '10B981', transparency: 90 },
  rectRadius: 0.12,
});
s7.addText('$200K', { x: 7.4, y: 1.95, w: 2.2, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.green, align: 'center' });
s7.addText('Owner Equity', { x: 7.4, y: 2.45, w: 2.2, h: 0.3, fontSize: 10, fontFace: 'Inter', color: '888888', align: 'center' });
s7.addText('33% of total', { x: 7.4, y: 2.7, w: 2.2, h: 0.3, fontSize: 9, fontFace: 'Inter', color: '666666', align: 'center' });

// SBA box
s7.addShape(p.ShapeType.roundRect, {
  x: 9.8, y: 1.9, w: 2.3, h: 1.5,
  fill: { color: '3B82F6', transparency: 90 },
  rectRadius: 0.12,
});
s7.addText('$400K', { x: 9.8, y: 1.95, w: 2.3, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.blue, align: 'center' });
s7.addText('SBA 7(a) Loan', { x: 9.8, y: 2.45, w: 2.3, h: 0.3, fontSize: 10, fontFace: 'Inter', color: '888888', align: 'center' });
s7.addText('10 yr @ 9% | $5,075/mo', { x: 9.8, y: 2.7, w: 2.3, h: 0.3, fontSize: 9, fontFace: 'Inter', color: '666666', align: 'center' });

// Key assumptions
s7.addText('Key Assumptions', { x: 7.4, y: 3.7, w: 4, h: 0.4, fontSize: 14, fontFace: 'Inter', bold: true, color: colors.white });
const assumptions = [
  'Avg Ticket: $15.00 (actual: $15.89 → conservative)',
  'COGS: 29% of revenue',
  'Labor: 30% inclusive of $60K owner salary',
  'Catering (Yr 1): 15–20% (actual: 25.7%)',
  'Royalty: 6% standard',
  'Rent: ~$4,200/mo ($24/sq ft NNN)',
];
assumptions.forEach((a, i) => {
  s7.addText(a, { x: 7.4, y: 4.2 + i * 0.35, w: 4.8, h: 0.3, fontSize: 11, fontFace: 'Inter', color: 'AAAAAA' });
});

// =========== SLIDE 8: P&L ===========
const s8 = p.addSlide();
s8.background = { fill: colors.bg };
addSlideNum(s8, 8, 13);
s8.addText('12-Month P&L Projection', { x: 0.8, y: 0.2, w: 8, h: 0.5, fontSize: 24, fontFace: 'Inter', bold: true, color: colors.white });
s8.addText('Ramp from 60 to 200 daily covers. Calibrated against actual location data.', { x: 0.8, y: 0.7, w: 10, h: 0.3, fontSize: 12, fontFace: 'Inter', color: '888888' });

const months = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12'];
const covers = [60,85,120,140,155,170,175,180,185,190,195,200];
const rev = [23400,33150,46800,54600,60450,66300,68250,70200,72150,74100,76050,78000];
const ebitda = [-978,2240,6244,7768,9399,11529,11723,11966,13210,14053,14197,14640];
const netCF = [-6053,-2835,1169,2693,4324,6454,6648,6891,8135,8978,9122,9565];
const cml = [-6053,-8888,-7719,-5026,-702,5752,12400,19291,27426,36404,45526,55091];

const fmt = (n) => (n < 0 ? '(' : '') + '$' + Math.abs(n).toLocaleString() + (n < 0 ? ')' : '');

const plRows = [
  [{ text: 'Item', options: { bold: true, color: colors.gold, fontSize: 8, fontFace: 'Inter' } },
   ...months.map(m => ({ text: m, options: { bold: true, color: colors.gold, fontSize: 8, fontFace: 'Inter', align: 'right' } }))],
  [{ text: 'Daily Covers', options: { color: 'AAAAAA', fontSize: 8, fontFace: 'Inter' } },
   ...covers.map(c => ({ text: String(c), options: { color: 'AAAAAA', fontSize: 8, fontFace: 'Inter', align: 'right' } }))],
  [{ text: 'Revenue', options: { color: 'AAAAAA', fontSize: 8, fontFace: 'Inter' } },
   ...rev.map(r => ({ text: fmt(r), options: { color: 'AAAAAA', fontSize: 8, fontFace: 'Inter', align: 'right' } }))],
  [{ text: 'EBITDA', options: { bold: true, color: colors.green, fontSize: 8, fontFace: 'Inter' } },
   ...ebitda.map(e => ({ text: fmt(e), options: { bold: true, color: e >= 0 ? colors.green : colors.red, fontSize: 8, fontFace: 'Inter', align: 'right' } }))],
  [{ text: 'Net Cash Flow', options: { bold: true, color: colors.gold, fontSize: 8, fontFace: 'Inter' } },
   ...netCF.map(n => ({ text: fmt(n), options: { bold: true, color: n >= 0 ? colors.green : colors.red, fontSize: 8, fontFace: 'Inter', align: 'right' } }))],
  [{ text: 'Cumulative', options: { color: '666666', fontSize: 8, fontFace: 'Inter' } },
   ...cml.map(c => ({ text: fmt(c), options: { color: c >= 0 ? colors.green : colors.red, fontSize: 8, fontFace: 'Inter', align: 'right' } }))],
];
s8.addTable(plRows, {
  x: 0.3, y: 1.2, w: 12.7,
  colW: [1.6, ...Array(12).fill(0.925)],
  rowH: [0.3, 0.25, 0.25, 0.25, 0.25, 0.25],
  border: { type: 'solid', pt: 0.5, color: '222222' },
  autoPage: false,
});

// ==== SLIDES 9–13: Continue building with high-level summaries for the rest ====
// SLIDE 9: Year 1 Highlights
const s9 = p.addSlide();
s9.background = { fill: colors.bg };
addSlideNum(s9, 9, 13);
s9.addText('Year 1 Highlights', { x: 0.8, y: 0.4, w: 6, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });

const kpis9 = [
  { v: '$673K', l: 'Total Revenue', c: colors.gold },
  { v: '$86K', l: 'EBITDA', c: colors.green },
  { v: '$55K', l: 'Net Cash Flow', c: colors.green },
  { v: '$60K', l: 'Owner Salary', c: colors.gold },
  { v: 'Month 3', l: 'Cash Flow Positive', c: colors.green },
  { v: '85–90', l: 'Daily Break-Even Covers', c: colors.gold },
];
kpis9.forEach((k, i) => {
  s9.addShape(p.ShapeType.roundRect, {
    x: 0.8 + (i % 3) * 3.2, y: 1.2 + Math.floor(i / 3) * 1.6, w: 2.9, h: 1.3,
    fill: { color: colors.white, transparency: 96 },
    rectRadius: 0.12,
    line: { color: '222222', width: 1 },
  });
  s9.addText(k.v, { x: 0.8 + (i % 3) * 3.2, y: 1.25 + Math.floor(i / 3) * 1.6, w: 2.9, h: 0.6, fontSize: 26, fontFace: 'Inter', bold: true, color: k.c, align: 'center' });
  s9.addText(k.l, { x: 0.8 + (i % 3) * 3.2, y: 1.8 + Math.floor(i / 3) * 1.6, w: 2.9, h: 0.4, fontSize: 11, fontFace: 'Inter', color: '888888', align: 'center' });
});

// Unit economics card
s9.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 4.3, w: 11.7, h: 2.2,
  fill: { color: 'F59E0B', transparency: 94 },
  rectRadius: 0.14,
  line: { color: 'F59E0B', transparency: 88, width: 1 },
});
s9.addText('Unit Economics vs Actual Data', { x: 1.2, y: 4.4, w: 6, h: 0.4, fontSize: 15, fontFace: 'Inter', bold: true, color: colors.white });
const unitEcon = [
  'Avg Ticket $15.00 (actual: $15.89 — conservative)',
  'Catering 15–20% Yr 1 (actual: 25.7% — building toward parity)',
  'Dinner ~25% (actual: 16.1% — growth thesis)',
  '3rd-party delivery: modeled within covers (actual: 17.1%)',
];
unitEcon.forEach((u, i) => {
  s9.addText(u, { x: 1.2, y: 4.9 + i * 0.35, w: 10, h: 0.3, fontSize: 11, fontFace: 'Inter', color: 'AAAAAA' });
});

// =========== SLIDE 10: REAL-WORLD VALIDATION ===========
const s10 = p.addSlide();
s10.background = { fill: colors.bg };
addSlideNum(s10, 10, 13);
s10.addText('Real-World Validation', { x: 0.8, y: 0.3, w: 8, h: 0.5, fontSize: 26, fontFace: 'Inter', bold: true, color: colors.white });
s10.addText('Actual POS data from 3 existing Afro Deli locations (June 2025 – June 2026)', { x: 0.8, y: 0.8, w: 10, h: 0.3, fontSize: 12, fontFace: 'Inter', color: '888888' });

const valRows = [
  [{ text: 'Metric', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter' } },
   { text: 'Actual (3-Loc Avg)', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter', align: 'right' } },
   { text: 'Woodbury Projection', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter', align: 'right' } },
   { text: 'Notes', options: { bold: true, color: colors.gold, fontSize: 10, fontFace: 'Inter' } }],
  ['Annual Revenue', '~$456K/location', '~$673K', '+47% — higher income, no competition'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Average Ticket', '$15.89', '$15.00', 'Conservative — Woodbury can support $16+'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Catering %', '25.7%', '15–20% (Yr 1)', 'Conservative ramp; targeting 25% by Yr 3'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['3rd-Party Delivery', '17.1%', 'Incl. in covers', 'DoorDash 12.7%, Uber 3.1%, Grubhub 1.3%'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
  ['Lunch / Dinner Split', '55.7% / 16.1%', '~50% / ~25%', 'Key thesis: dinner is underpenetrated'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 10, fontFace: 'Inter' } })),
];
s10.addTable(valRows, {
  x: 0.8, y: 1.3, w: 11.7,
  colW: [2.5, 2.5, 2.5, 4.2],
  rowH: [0.35, 0.3, 0.3, 0.3, 0.3, 0.3],
  border: { type: 'solid', pt: 0.5, color: '222222' },
  autoPage: false,
});

s10.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 3.5, w: 11.7, h: 1.4,
  fill: { color: '10B981', transparency: 94 },
  rectRadius: 0.12,
  line: { color: '10B981', transparency: 85, width: 1.5 },
});
s10.addText('✅ Verdict: The real data validates the model. The biggest Woodbury-specific upsides are catering (25.7% proven — Woodbury institutional market is larger) and dinner (only 16.1% today — significant growth runway).', {
  x: 1.2, y: 3.8, w: 10.5, h: 0.8, fontSize: 13, fontFace: 'Inter', color: 'BBBBBB',
});
s10.addText('Source: Afro Deli POS system (Toast) — combined data from Minneapolis Marquette, Downtown St. Paul, and Riverside/West Bank locations.', {
  x: 0.8, y: 5.1, w: 10, h: 0.3, fontSize: 9, fontFace: 'Inter', color: '555555',
});

// =========== SLIDE 11: SENSITIVITY ===========
const s11 = p.addSlide();
s11.background = { fill: colors.bg };
addSlideNum(s11, 11, 13);
s11.addText('Sensitivity Analysis', { x: 0.8, y: 0.4, w: 6, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });
s11.addText('The business holds up well even with a 10% revenue headwind.', { x: 0.8, y: 1.0, w: 8, h: 0.4, fontSize: 14, fontFace: 'Inter', color: '888888' });

const sensRows = [
  [{ text: 'Metric', options: { bold: true, color: colors.gold, fontSize: 11, fontFace: 'Inter' } },
   { text: 'Base Case', options: { bold: true, color: colors.gold, fontSize: 11, fontFace: 'Inter', align: 'right' } },
   { text: '–10% Scenario', options: { bold: true, color: colors.gold, fontSize: 11, fontFace: 'Inter', align: 'right' } }],
  ['Year 1 Revenue', '$673,350', '$606,015'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } })),
  ['Year 1 EBITDA', '$85,917', '$40,110'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } })),
  ['Year 1 Net Cash Flow', '$55,091', '($20,790)'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } })),
  ['Break-Even Month', 'Month 3', 'Month 7'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } })),
  ['Yr-End Cumulative Cash', '$55,091', '($20,790)'].map(t => ({ text: t, options: { color: 'AAAAAA', fontSize: 11, fontFace: 'Inter' } })),
];
s11.addTable(sensRows, {
  x: 0.8, y: 1.6, w: 6.0,
  colW: [2.5, 1.8, 1.7],
  rowH: [0.35, 0.3, 0.3, 0.3, 0.3, 0.3],
  border: { type: 'solid', pt: 0.5, color: '222222' },
  autoPage: false,
});

// Working capital cushion card
s11.addShape(p.ShapeType.roundRect, {
  x: 7.2, y: 1.6, w: 5.3, h: 2.5,
  fill: { color: '10B981', transparency: 93 },
  rectRadius: 0.14,
  line: { color: '10B981', transparency: 88, width: 1.5 },
});
s11.addText('Working Capital Cushion', { x: 7.6, y: 1.7, w: 4.5, h: 0.4, fontSize: 15, fontFace: 'Inter', bold: true, color: colors.green });
s11.addText('$87K reserve covers the –10% scenario gap for 4+ months before additional capital is needed.', { x: 7.6, y: 2.2, w: 4.5, h: 0.8, fontSize: 12, fontFace: 'Inter', color: 'AAAAAA' });
s11.addText('Revenue would need to underperform by 20%+ before a capital infusion is required.', { x: 7.6, y: 3.0, w: 4.5, h: 0.6, fontSize: 12, fontFace: 'Inter', color: 'AAAAAA' });

// Breakeven card
s11.addShape(p.ShapeType.roundRect, {
  x: 0.8, y: 4.5, w: 5.5, h: 2.2,
  fill: { color: 'F59E0B', transparency: 94 },
  rectRadius: 0.14,
  line: { color: 'F59E0B', transparency: 88, width: 1 },
});
s11.addText('Break-Even Analysis', { x: 1.2, y: 4.6, w: 4, h: 0.4, fontSize: 14, fontFace: 'Inter', bold: true, color: colors.white });
const beItems = [
  ['Fixed Monthly Costs', '~$22,500'],
  ['Variable Cost Ratio', '40–42% of revenue'],
  ['Break-Even Revenue', '~$32.5K–$34K/mo'],
  ['Break-Even Daily Covers', '85–90/day'],
];
beItems.forEach((b, i) => {
  s11.addText(b[0], { x: 1.2, y: 5.1 + i * 0.35, w: 3.0, h: 0.3, fontSize: 11, fontFace: 'Inter', color: 'AAAAAA' });
  s11.addText(b[1], { x: 4.0, y: 5.1 + i * 0.35, w: 2.0, h: 0.3, fontSize: 11, fontFace: 'Inter', bold: true, color: i === 3 ? colors.green : colors.white, align: 'right' });
});

// Mitigation card
s11.addShape(p.ShapeType.roundRect, {
  x: 6.7, y: 4.5, w: 5.8, h: 2.2,
  fill: { color: colors.white, transparency: 96 },
  rectRadius: 0.14,
  line: { color: '222222', width: 1 },
});
s11.addText('Mitigation Levers', { x: 7.1, y: 4.6, w: 4, h: 0.4, fontSize: 14, fontFace: 'Inter', bold: true, color: colors.white });
const levers = [
  'Reduce labor % to ~27% (owner takes lower draw)',
  'Tighten COGS through portion control',
  'Defer non-essential maintenance & marketing',
  'Accelerate catering outreach (higher margin)',
];
levers.forEach((l, i) => s11.addText(l, { x: 7.1, y: 5.1 + i * 0.35, w: 5, h: 0.3, fontSize: 11, fontFace: 'Inter', color: 'AAAAAA' }));

// =========== SLIDE 12: NEXT ACTIONS ===========
const s12 = p.addSlide();
s12.background = { fill: colors.bg };
addSlideNum(s12, 12, 13);
s12.addText('Next Actions', { x: 0.8, y: 0.4, w: 6, h: 0.6, fontSize: 28, fontFace: 'Inter', bold: true, color: colors.white });

const phases = [
  { title: 'Immediate (Week 1–4)', color: colors.gold, items: [
    '📄 Request FDD from Afro Deli franchisor',
    '⚖️ Engage franchise attorney for FDD review',
    '🔍 Validate Item 19 financial performance reps',
    '🏗️ Site scouting — Tamarack, Woodbury Lakes, Valley Creek',
  ]},
  { title: 'Short-Term (Month 1–3)', color: colors.blue, items: [
    '💰 Begin SBA 7(a) loan application',
    '🤝 Schedule Discovery Day with franchisor',
    '📋 Finalize entity structure (LLC)',
    '🔑 Negotiate lease letter of intent',
  ]},
  { title: 'Key Contacts Needed', color: colors.green, items: [
    'Franchisor: Afro Deli corporate',
    'Lender: SBA-preferred bank',
    'Attorney: Franchise + lease specialist',
    'Broker: Woodbury commercial RE',
    'Contractor: Restaurant build-out',
  ]},
  { title: 'Timeline', color: colors.purple, items: [
    'Month 0–2: FDD, lease LOI, loan approval',
    'Month 2–5: Build-out, equipment, training',
    'Month 5–6: Soft opening → grand opening',
  ]},
];

phases.forEach((ph, i) => {
  const col = i % 2;
  const row = Math.floor(i / 2);
  const x = 0.8 + col * 6.3;
  const y = 1.2 + row * 3.0;

  s12.addShape(p.ShapeType.roundRect, {
    x, y, w: 5.9, h: 2.6,
    fill: { color: colors.white, transparency: 96 },
    rectRadius: 0.14,
    line: { color: ph.color, transparency: 85, width: 1.5 },
  });
  s12.addText(ph.title, { x: x + 0.3, y: y + 0.15, w: 5, h: 0.4, fontSize: 14, fontFace: 'Inter', bold: true, color: ph.color });
  ph.items.forEach((item, j) => {
    s12.addText(item, { x: x + 0.3, y: y + 0.65 + j * 0.4, w: 5.2, h: 0.35, fontSize: 11.5, fontFace: 'Inter', color: 'AAAAAA' });
  });
});

// =========== SLIDE 13: CLOSE ===========
const s13 = p.addSlide();
s13.background = { fill: colors.bg };
addSlideNum(s13, 13, 13);

s13.addText("Let's", { x: 0, y: 1.0, w: 13.333, h: 1.0, fontSize: 52, fontFace: 'Inter', bold: true, color: colors.white, align: 'center' });
s13.addText('Build This.', { x: 0, y: 1.9, w: 13.333, h: 1.2, fontSize: 60, fontFace: 'Inter', bold: true, color: colors.gold, align: 'center' });

s13.addText('A proven franchise concept validated by real operational data\nin a growing, affluent market with no direct competition.', {
  x: 2, y: 3.2, w: 9.333, h: 0.8, fontSize: 16, fontFace: 'Inter', color: '888888', align: 'center',
});

// Final KPIs
const finalKpis = [
  { v: '$600K', l: 'Total Investment', c: colors.gold },
  { v: 'Month 3', l: 'Cash Flow Positive', c: colors.green },
  { v: '$86K', l: 'Year 1 EBITDA', c: colors.blue },
];
finalKpis.forEach((k, i) => {
  s13.addText(k.v, { x: 2 + i * 3.5, y: 4.3, w: 2.5, h: 0.7, fontSize: 40, fontFace: 'Inter', bold: true, color: k.c, align: 'center' });
  s13.addText(k.l, { x: 2 + i * 3.5, y: 5.0, w: 2.5, h: 0.4, fontSize: 13, fontFace: 'Inter', color: '777777', align: 'center' });
});

// Footer
s13.addShape(p.ShapeType.line, { x: 2, y: 5.7, w: 9.333, h: 0, line: { color: '222222', width: 1 } });
s13.addText('Projections calibrated against actual POS data from 3 existing Afro Deli locations (June 2025–June 2026):\nCombined net sales $1.37M | Avg ticket $15.89 | 86,170 annual guests | Catering 25.7% | 17.1% delivery\nAll Woodbury projections are estimates pending FDD review, site selection, and lease negotiation.', {
  x: 1.5, y: 5.85, w: 10.333, h: 1.2, fontSize: 9, fontFace: 'Inter', color: '555555', align: 'center',
});

// Save
p.writeFile({ fileName: '/home/kofi/clawd/projects/afrodeli-woodbury-pitch-deck.pptx' })
  .then(() => console.log('DONE'));
