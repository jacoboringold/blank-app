import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';

const html = await readFile(new URL('./index.html', import.meta.url));
const server = createServer((req, res) => { res.writeHead(200, {'content-type':'text/html; charset=utf-8'}); res.end(html); });
await new Promise(resolve => server.listen(4173, '127.0.0.1', resolve));
let browser;
try {
  browser = await chromium.launch({headless:true});
  const context = await browser.newContext({viewport:{width:390,height:844}, isMobile:true, hasTouch:true});
  const page = await context.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto('http://127.0.0.1:4173/');
  await page.locator('#deploy').tap();
  await page.waitForTimeout(250);
  if (!(await page.locator('#overlay').evaluate(el => el.classList.contains('hidden')))) throw new Error('Deploy button did not dismiss launch screen');
  await page.locator('button[onclick*="sonar"]').tap();
  if (!(await page.locator('#toast').evaluate(el => el.classList.contains('show')))) throw new Error('Sonar button did not trigger feedback');
  const joy = page.locator('#joy');
  const rect = await joy.boundingBox();
  await page.mouse.move(rect.x + rect.width/2, rect.y + rect.height/2);
  await page.mouse.down();
  await page.mouse.move(rect.x + rect.width*.8, rect.y + rect.height*.55, {steps:5});
  await page.mouse.up();
  if ((await page.locator('#knob').getAttribute('style') || '').includes('translate(0,0)')) throw new Error('Joystick did not move');
  if (errors.length) throw new Error('Browser JavaScript errors: ' + errors.join('; '));
  console.log('PASS: mobile viewport loaded; deploy tap dismissed overlay; sonar responded; joystick moved; no page errors.');
} finally {
  if (browser) await browser.close();
  server.close();
}
