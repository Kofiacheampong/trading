// Generate PDFs for the Afro Deli package: node generate-pdf.js <input.html> <output.pdf> [--deck]
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const input = path.resolve(__dirname, process.argv[2]);
  const output = path.resolve(__dirname, process.argv[3] || input.replace(/\.\w+$/, '.pdf'));
  const isDeck = process.argv[4] === '--deck';

  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto('file://' + input, { waitUntil: 'networkidle0', timeout: 60000 });

  if (isDeck) {
    // Convert the scroll-snap slide layout into one-slide-per-page printing.
    await page.addStyleTag({ content: `
      html, body { overflow: visible !important; height: auto !important; background: #0a0a0a !important; }
      .slides { overflow: visible !important; height: auto !important; scroll-snap-type: none !important; }
      .slide { min-height: 100vh !important; height: auto !important; width: 100vw !important;
               page-break-after: always !important; break-inside: avoid !important;
               overflow: hidden !important; padding: 48px 64px !important; }
      .slide-number { display: none !important; }
    `});
  }

  await page.pdf({
    path: output,
    format: isDeck ? 'A4' : 'Letter',
    landscape: isDeck,
    printBackground: true,
    preferCSSPageSize: !isDeck,
  });

  await browser.close();
  console.log('PDF created:', output);
})();
