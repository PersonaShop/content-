// Скачать публичный Instagram-рилс для покадрового разбора референса.
// Instagram отдаёт 429 на прямые запросы, а embed-плеер в headless Chromium отдаёт mp4.
//
//   node ai-page/tools/reel_grab.js <ссылка на рилс> <папка>
//   → <папка>/reel.mp4, <папка>/meta.json (подпись, автор), <папка>/sheet_*.jpg (кадры 2 к/с с таймкодом)
//
// Папку брать вне репо: чужие ролики не коммитим.
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const PW = ['/opt/node-tools/node_modules/playwright', 'playwright'].find(p => { try { require.resolve(p); return true; } catch { return false; } });
const { chromium } = require(PW);

(async () => {
  const [url, outDir] = process.argv.slice(2);
  if (!url || !outDir) { console.error('usage: reel_grab.js <reel url> <out dir>'); process.exit(1); }
  const code = (url.match(/\/(?:reel|p)\/([^/?]+)/) || [])[1];
  if (!code) { console.error('не нашёл код рилса в ссылке'); process.exit(1); }
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--autoplay-policy=no-user-gesture-required'] });
  const ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36';
  const page = await (await browser.newContext({ userAgent: ua })).newPage();

  // 1. Подпись и автор: со страницы рилса (meta og:*), там без логина.
  await page.goto(`https://www.instagram.com/reel/${code}/`, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(4000);
  const meta = Object.fromEntries(await page.$$eval('meta[property^="og:"]', m => m.map(x => [x.getAttribute('property'), x.getAttribute('content')])));

  // 2. Видео: из embed-плеера.
  await page.goto(`https://www.instagram.com/reel/${code}/embed/`, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  await page.waitForTimeout(3000);
  const src = (await page.$$eval('video', v => v.map(x => x.currentSrc || x.src)))[0];
  await browser.close();
  if (!src) { console.error('видео не найдено: рилс приватный или embed отключён'); process.exit(2); }

  const mp4 = path.join(outDir, 'reel.mp4');
  execFileSync('curl', ['-sS', '-A', ua, '-o', mp4, src]);
  fs.writeFileSync(path.join(outDir, 'meta.json'), JSON.stringify({ url, ...meta }, null, 2));

  // 3. Контактные листы: 2 кадра/с, 12 кадров на лист, таймкод в углу.
  execFileSync('ffmpeg', ['-v', 'error', '-y', '-i', mp4, '-vf',
    "fps=2,scale=270:-1,drawtext=text='%{pts\\:hms}':x=5:y=5:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x2",
    path.join(outDir, 'sheet_%02d.jpg')]);
  console.log(`ok: ${mp4}`);
})();
