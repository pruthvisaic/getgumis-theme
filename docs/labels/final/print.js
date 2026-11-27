// Exports each label as a 175 x 70 mm PDF (Suplify spec): 2075 x 830 px layout (2.5:1), scaled to the page.
const { chromium } = require('playwright');
const fs = require('fs');
const CSS = `html,body{background:#fff!important}
.label{width:2075px!important;grid-template-columns:630px 815px 630px!important}
@page{size:175mm 70mm;margin:0}
.left,.right{border:0!important}`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 2075, height: 830 }, deviceScaleFactor: 2 });
  for (const k of ['sleep', 'glow', 'power']) {
    await p.goto('file://' + process.cwd() + '/get-B-' + k + '.html');
    await p.addStyleTag({ content: CSS });
    await p.waitForTimeout(600);
    const o = await p.evaluate(() => [...document.querySelectorAll('.side')].map((s) => s.scrollHeight - s.clientHeight));
    console.log(k, 'overflow', JSON.stringify(o));
    await p.screenshot({ path: 'print-' + k + '.png', clip: { x: 0, y: 0, width: 2075, height: 830 } });
    await p.pdf({ path: 'getgumis-' + k + '-label-175x70mm.pdf', width: '175mm', height: '70mm', printBackground: true, pageRanges: '1', scale: (175 / 25.4 * 96) / 2075 });
  }
  await b.close();
})();
