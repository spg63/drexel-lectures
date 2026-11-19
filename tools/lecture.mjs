#!/usr/bin/env node
// One entry point for every deck. Decks are named by course/slug prefix, e.g. "cs510/w06".
//
//   npm run list
//   npm run dev      cs510/w06
//   npm run handout  cs510/w06 [label]   after lecture: PDF with ink -> handouts/, ink archived
//   npm run export   cs510/w06           PDF of the current state (no archiving)
//   npm run render   cs510/w06           PNG per slide -> renders/cs510/<slug>/ (layout check)
//   npm run build    cs510/w06           static site -> dist/cs510/<slug>/
//   npm run fit      cs510/w06           re-measure every slide, set zoom only where it overflows
//   npm run new      cs510/w07-mdps "Markov Decision Processes" ["CS 510 · Week 7"]
//   npm run convert  path/to/deck.pptx cs510/w07-mdps "Markov Decision Processes" ["CS 510 · Week 7"]
//
// Env: CHROME_PATH=/path/to/chrome  use a specific browser for export/fit instead of Playwright's.

import { execFileSync, spawnSync } from 'node:child_process'
import { existsSync, mkdirSync, readdirSync, renameSync, statSync, writeFileSync } from 'node:fs'
import { join, relative, resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..')
const COURSES = join(ROOT, 'courses')
const [cmd, ...args] = process.argv.slice(2)
const chrome = process.env.CHROME_PATH ? ['--executable-path', process.env.CHROME_PATH] : []

const die = (msg) => { console.error(msg); process.exit(1) }
const run = (bin, argv, cwd = ROOT) => {
  const r = spawnSync(bin, argv, { cwd, stdio: 'inherit' })
  if (r.status !== 0) die(`${bin} ${argv.join(' ')} failed`)
}
const slidev = (argv) => run('npx', ['slidev', ...argv])

function decks() {
  if (!existsSync(COURSES)) return []
  return readdirSync(COURSES).flatMap(course => {
    const cdir = join(COURSES, course)
    if (!statSync(cdir).isDirectory()) return []
    return readdirSync(cdir)
      .filter(d => existsSync(join(cdir, d, 'slides.md')))
      .map(d => ({ id: `${course}/${d}`, course, slug: d, dir: join(cdir, d) }))
  })
}

function deck(name) {
  if (!name) die('Which deck? e.g. "cs510/w06". Run `npm run list`.')
  const all = decks()
  const hits = all.filter(d => d.id === name || d.id.startsWith(name))
  if (hits.length === 1) return hits[0]
  if (!hits.length) die(`No deck matches "${name}". Run \`npm run list\`.`)
  die(`"${name}" is ambiguous: ${hits.map(h => h.id).join(', ')}`)
}

const today = () => new Date().toLocaleDateString('en-CA') // YYYY-MM-DD, local time

function exportPdf(d, out) {
  mkdirSync(dirname(out), { recursive: true })
  slidev(['export', relative(ROOT, join(d.dir, 'slides.md')), '--output', out, '--timeout', '60000',
    '--per-slide', // whole-document print shrinks slides when layouts carry page numbers
    ...chrome])
}

const commands = {
  list() {
    const all = decks()
    if (!all.length) return console.log('No decks yet. `npm run new cs510/w01-intro "Title"`')
    for (const d of all) console.log(d.id)
  },

  dev([name]) {
    slidev([relative(ROOT, join(deck(name).dir, 'slides.md')), '--open'])
  },

  export([name]) {
    const d = deck(name)
    exportPdf(d, join(ROOT, 'handouts', d.course, `${d.slug}.pdf`))
  },

  handout([name, label = today()]) {
    const d = deck(name)
    const live = join(d.dir, 'annotations', 'live')
    const inked = existsSync(live) ? readdirSync(live).filter(f => f.endsWith('.svg')).length : 0
    if (!inked) console.warn('No ink in annotations/live; exporting a clean PDF.')
    const out = join(ROOT, 'handouts', d.course, `${d.slug}-${label}.pdf`)
    exportPdf(d, out)
    if (inked) {
      let dest = join(d.dir, 'annotations', label)
      for (let i = 2; existsSync(dest); i++) dest = join(d.dir, 'annotations', `${label}-${i}`)
      renameSync(live, dest)
      console.log(`Ink from ${inked} slide(s) archived to ${relative(ROOT, dest)}/ (deck is clean for next time).`)
    }
    console.log(`Handout: ${relative(ROOT, out)}`)
  },

  render([name]) {
    // one PNG per visible slide, builds fully revealed: how an agent (or you) checks layout
    const d = deck(name)
    const out = join(ROOT, 'renders', d.course, d.slug)
    slidev(['export', relative(ROOT, join(d.dir, 'slides.md')), '--format', 'png', '--output', out, '--timeout', '60000', ...chrome])
    console.log(`Renders: ${relative(ROOT, out)}/`)
  },

  build([name]) {
    const d = deck(name)
    slidev(['build', relative(ROOT, join(d.dir, 'slides.md')), '--base', './', '--out', join(ROOT, 'dist', d.course, d.slug)])
  },

  fit([name]) {
    run('python3', [join(ROOT, 'tools', 'fit.py'), deck(name).dir])
  },

  new([id, title, kicker]) {
    if (!id || !id.includes('/') || !title) die('usage: npm run new cs510/w07-mdps "Markov Decision Processes" ["CS 510 · Week 7"]')
    const dir = join(COURSES, id)
    if (existsSync(join(dir, 'slides.md'))) die(`${id} already exists`)
    mkdirSync(join(dir, 'public', 'img'), { recursive: true })
    const course = id.split('/')[0].toUpperCase().replace(/^([A-Z]+)(\d+)/, '$1 $2')
    writeFileSync(join(dir, 'slides.md'), `---
theme: drexel
title: "${course} · ${title}"
aspectRatio: 16/9
canvasWidth: 980
layout: cover
kicker: ${kicker || course}
---

# ${title}

Sean Grimes

---

# First content slide

- Point one
- Point two

<!--
Speaker notes for this slide.
-->
`)
    console.log(`Created courses/${id}/slides.md  ->  npm run dev ${id}`)
  },

  convert([pptx, id, title, kicker]) {
    if (!pptx || !id || !title) die('usage: npm run convert path/to/deck.pptx cs510/w07-mdps "Title" ["CS 510 · Week 7"]')
    const dir = join(COURSES, id)
    if (existsSync(join(dir, 'slides.md')) && !process.env.FORCE)
      die(`courses/${id}/slides.md exists. Converting again would overwrite hand edits. FORCE=1 to do it anyway.`)
    mkdirSync(dir, { recursive: true })
    const cache = join(dir, '.cache')
    run('python3', [join(ROOT, 'tools', 'prep_pptx.py'), resolve(pptx), cache])
    const course = id.split('/')[0].toUpperCase().replace(/^([A-Z]+)(\d+)/, '$1 $2')
    run('python3', [join(ROOT, 'tools', 'convert.py'), join(cache, 'clean.pptx'), join(cache, 'ref'), dir,
      '--title', `${course} · ${title}`, '--kicker', kicker || course])
    run('python3', [join(ROOT, 'tools', 'fit.py'), dir])
    console.log(`Converted -> courses/${id}/slides.md. Review with: npm run dev ${id}`)
  },
}

if (!commands[cmd]) die(`Commands: ${Object.keys(commands).join(', ')}`)
commands[cmd](args)
