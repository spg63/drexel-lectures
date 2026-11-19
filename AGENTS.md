# Working in drexel-lectures

Lecture decks for Sean Grimes's Drexel CS courses, built with Slidev and one shared theme. This file is for any agent (Claude, Codex, others) writing or editing decks here.

## Layout

```
packages/slidev-theme-drexel/   the theme: styles/base.css (tokens), layouts/, components/, example.md (style guide)
courses/<course>/<slug>/        one lecture per folder: slides.md, public/img/, annotations/
tools/lecture.mjs               the CLI behind every npm script
tools/convert.py, prep_pptx.py  PPTX -> Slidev conversion
tools/fit.py, measure.mjs       overflow measurement -> per-slide zoom
docs/STYLE.md                   the style spec. Read it before writing slides.
```

Decks are addressed by prefix: `cs510/w06` matches `courses/cs510/w06-constraint-reasoning`.

## Commands

```
npm run list
npm run new cs510/w07-mdps "Markov Decision Processes" "CS 510 · Week 7"
npm run dev cs510/w07          # live preview
npm run render cs510/w07       # PNG per slide -> renders/cs510/w07-mdps/
npm run fit cs510/w07          # measure and set zoom where content overflows
npm run convert path/to.pptx cs510/w07-mdps "Title" "CS 510 · Week 7"
```

Set `CHROME_PATH` if Playwright's bundled browser isn't installed.

## Writing slides

Follow `docs/STYLE.md`. The rules that get broken most:

- Every content slide ends with speaker notes in `<!-- ... -->`.
- About six top-level bullets, two levels deep. Too much content means split the slide; it does not mean shrink it.
- Layouts: default, `split`, `figure`, `statement`, `section`, `cover`. Do not position things absolutely; do not invent per-slide CSS.
- Colors only via `dx-red|blue|green|purple`. Never `c-*` or `text-*` (UnoCSS owns them).
- Math in KaTeX with `\text{}` for names. MDC is off; leave it off.
- Builds (`v-click`, `<v-clicks>`) only where the order teaches something.
- Never move, delete, hide or unhide slides in a deck that has ink in `annotations/live/`. Ink is keyed by slide number.

## Verify before handing back

1. `npm run render <deck>` and look at every slide you touched. Check for overflow, collisions, empty space, unreadable figures.
2. `npm run fit <deck>` if anything overflowed. A zoom below 0.75 means the slide needs splitting.
3. Report what you changed by slide number and title, not as a diff dump.

## Converting PowerPoint

- `npm run convert` strips ink, renders a reference copy with LibreOffice, converts, then runs fit. Needs `soffice` and `pdftoppm`.
- Runs of near-identical slides become one slide with click steps. Drawn diagrams are cropped from the reference render. OMML equations are cropped and flagged.
- While iterating a conversion, fix individual slides with `courses/<course>/<slug>/overrides/sNN.md` (NN = source PPTX slide), so re-running keeps them. Override-only images go in `overrides/img/`.
- After the first hand edit to `slides.md`, the deck is source, not output. `convert` refuses to overwrite it without `FORCE=1`.
- Slides built from PowerPoint animations render with every state stacked. Rebuild those as click steps; don't ship the crop.

## Git

Personal repo, one author. Commit straight to `main`; no feature branches or PRs unless Sean asks for one.

## Don't

- Don't commit `handouts/`, `renders/`, `dist/`, `.cache/` or `annotations/live/` (all git-ignored).
- Don't change the theme to fix one deck. If a deck needs something new, add it to the theme and to `example.md`, then use it.
- Don't put exam answers in decks that will be posted before the exam. Hidden slides are still in the source.
