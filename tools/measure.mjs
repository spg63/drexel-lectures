// usage: node measure.mjs http://localhost:3031/# <count>  -> JSON [{n, height, width}] in canvas px
import { chromium } from 'playwright-chromium'

const [base, count] = [process.argv[2], Number(process.argv[3])]
const browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {})
const page = await browser.newPage({ viewport: { width: 1960, height: 1104 } })
const out = []
for (let n = 1; n <= count; n++) {
  await page.goto(`${base}/${n}?clicks=99`, { waitUntil: 'networkidle' })
  await page.waitForTimeout(250)
  await page.evaluate(() => document.fonts.ready)
  const r = await page.evaluate(() => {
    const layouts = [...document.querySelectorAll('.slidev-layout')].filter(e => e.offsetParent !== null)
    const L = layouts.sort((a, b) => b.getBoundingClientRect().width - a.getBoundingClientRect().width)[0]
    if (!L) return null
    const lr = L.getBoundingClientRect()
    const scale = lr.height / L.offsetHeight
    let bottom = 0, right = 0
    for (const el of L.querySelectorAll('*')) {
      const cs = getComputedStyle(el)
      if (cs.position === 'absolute' || cs.display === 'contents') continue
      const b = el.getBoundingClientRect()
      if (!b.width || !b.height) continue
      bottom = Math.max(bottom, b.bottom)
      right = Math.max(right, b.right)
    }
    const pb = parseFloat(getComputedStyle(L).paddingBottom)
    return {
      height: (bottom - lr.top) / scale + pb,
      width: (right - lr.left) / scale,
      canvasH: L.offsetHeight,
      canvasW: L.offsetWidth,
      title: (L.querySelector('h1') || {}).textContent || '',
    }
  })
  out.push({ n, ...r })
}
console.log(JSON.stringify(out))
await browser.close()
