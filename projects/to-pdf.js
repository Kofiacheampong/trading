const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const input = path.resolve(__dirname, process.argv[2]);
  const output = path.resolve(__dirname, process.argv[3] || input.replace(/\.\w+$/, '.pdf'));
  
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.goto('file://' + input, { waitUntil: 'networkidle0' });
  
  await page.pdf({
    path: output,
    format: 'A4',
    margin: { top: '0.75in', bottom: '0.75in', left: '0.75in', right: '0.75in' },
    printBackground: true,
  });
  
  await browser.close();
  console.log('PDF created:', output);
})();
