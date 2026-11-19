# Lecture style: slidev-theme-drexel v1

Drexel blue and gold, minus the letterhead. This is the spec; `packages/slidev-theme-drexel/example.md` is the same spec rendered (`npm run style-guide`). Change both together.

## Principles

1. **Readable from the back row.** Body text is ~21px on a 980×551 canvas. If a slide doesn't fit, cut or split it before shrinking it.
2. **Drexel colors, not Drexel letterhead.** No logo, no footer band, no diagonal stripes. Blue grounds are for covers and section breaks only.
3. **One idea per slide.** The title says what the slide is about; a statement slide says what it *means*.
4. **The handout matters as much as the projection.** Students get the PDF after class with your ink on it, so slides must read well without you talking over them.

## Tokens

| Token | Value | Use |
|---|---|---|
| `--dx-blue` | `#07294d` | Titles, bold text, cover/section ground |
| `--dx-blue-2` | `#1d4f86` | Links, second-level list markers |
| `--dx-gold` | `#ffc600` | Title rule, highlighter, accents on blue |
| `--dx-gold-deep` | `#d9a200` | Gold on paper (bullets, aside border) |
| `--paper` | `#fbf9f4` | Slide ground |
| `--paper-2` | `#f2eee4` | Code blocks, inline code, asides |
| `--ink` | `#1a2433` | Body text |
| `--muted` | `#6b7280` | Captions, slide numbers |
| `--tx-red / blue / green / purple` | `#c0162f` `#1f5fcf` `#1d8a4a` `#6b3fa0` | Semantic text color (see below) |

**Type.** Headings: Bricolage Grotesque (700). Body: Source Sans 3. Code and small labels: JetBrains Mono. All fonts ship with the theme (no network needed to present).

**Sizes.** Body `1.34rem` (~21px) · H1 `2.3rem` · H2 `1.45rem` · level-2 bullets 88% of their parent · code 16px · captions 82%.

## Layouts

| Layout | When | Frontmatter |
|---|---|---|
| `cover` | First slide only | `kicker` (e.g. `CS 510 · Week 6`) |
| `section` | Part breaks in a long lecture | `kicker` (e.g. `Part 2`) |
| default | Text-led slides | none |
| `split` | Text with one supporting figure | `flip: true` (figure left), `ratio: 1.2fr 1fr` (text column first) |
| `figure` | The picture is the point | `caption` |
| `statement` | Discussion prompt, definition, punchline | `kicker` (e.g. `Discuss`, `Quick check`) |

Slots in `split`: content before `::left::` is the title; `::left::` holds text; `::right::` holds the figure and an optional `<div class="caption">`.

Slide numbers appear bottom right on default, split and figure slides, so students can say "slide 23."

## Text

- **Bullets:** about six top-level items at most. Two levels is normal; a third is rare.
- **Bold** marks a term being defined. *Italic* is for stress. `<span class="mark">…</span>` is the highlighter: one per slide at most.
- **Semantic color** only where color carries meaning (variables vs. domains vs. constraints, wrong answers): `dx-red`, `dx-blue`, `dx-green`, `dx-purple`.
  - Never `c-*` or `text-*` classes. UnoCSS owns those prefixes and silently overrides them.
  - Purple is legacy; avoid it in new material.
- **Asides:** `<Aside>…</Aside>` or `<Aside label="Exam tip">…</Aside>` for instructor notes the students should also see. One per slide.
- **Speaker notes:** every content slide ends with an HTML comment `<!-- … -->` holding what you'll say.

## Figures

- Default layout: `<div class="figs"><img src="/img/x.png" class="fig" style="max-height:300px" /></div>`.
- `.fig` uses `mix-blend-mode: multiply`, so white image backgrounds disappear into the paper. Transparent PNG or SVG is still better.
- Put images in the deck's `public/img/` and reference them as `/img/...`.
- Prefer a real diagram (Mermaid, SVG, a clean PNG) over a screenshot of someone else's slide.

## Math and code

- KaTeX: `$…$` inline, `$$…$$` display. Variable names inside math use `\text{}`: `$\text{SA} \neq \text{WA}$`.
- Braces are literal: MDC syntax is off, so `{1,2,…,9}` is safe in text.
- Code blocks: fenced with a language. Step through lines on click with `{2-3|5-8|all}`.

## Builds

- `<v-clicks>` around a list reveals one item per click. `<div v-click>` reveals a block.
- Use builds when the order of revelation teaches something (search fringes, derivations), not for every list.
- The PDF handout shows every build fully revealed.

## Fit

- Run `npm run fit <deck>` after big edits. It measures every slide in a browser and sets `zoom` only where content overflows.
- `zoom` under ~0.75 means the slide has too much on it: split it.

## Ink and handouts

- Ink saves to `annotations/live/<slide>.svg` as you draw (requires presenting via `npm run dev`).
- `npm run handout <deck>` after class: a PDF with your ink, then the ink moves to `annotations/<date>/`.
- **Export before you edit.** Ink is keyed by visible slide number; adding, removing, hiding or unhiding a slide misaligns every later annotation.
