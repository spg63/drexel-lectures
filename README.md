# drexel-lectures

Lecture decks for Drexel CS courses, in [Slidev](https://sli.dev) with one shared theme.

## Setup (once per machine)

```bash
npm install
npx playwright install chromium   # for PDF/PNG export
```

Converting PowerPoint decks also needs LibreOffice and poppler: `brew install --cask libreoffice && brew install poppler`.

## Teaching a lecture

```bash
npm run dev cs510/w06       # present; `o` for presenter mode
# ... ink as you go; every stroke saves to the deck's annotations/live/
npm run handout cs510/w06   # after class: handouts/cs510/w06-...-YYYY-MM-DD.pdf, ink archived
```

Post the PDF. Two sections in one day: `npm run handout cs510/w06 2026-11-19-s2`.

**Export before you edit.** Ink is keyed by slide number; adding, removing, hiding or unhiding a slide shifts every later annotation.

## Everything else

| Command | Does |
|---|---|
| `npm run list` | List decks |
| `npm run new cs510/w07-mdps "Title" "CS 510 · Week 7"` | Start a deck |
| `npm run render cs510/w07` | PNG per slide, for checking layout |
| `npm run fit cs510/w07` | Shrink only the slides that overflow |
| `npm run export cs510/w07` | PDF without archiving ink |
| `npm run build cs510/w07` | Static site in `dist/` |
| `npm run convert deck.pptx cs510/w07-mdps "Title" "CS 510 · Week 7"` | PowerPoint to Slidev |
| `npm run style-guide` | The theme's style guide deck |

Style rules: [docs/STYLE.md](docs/STYLE.md). Agent conventions: [AGENTS.md](AGENTS.md).

Decks are named by prefix: `cs510/w06` finds `courses/cs510/w06-constraint-reasoning`.
