# Lunar Field Cards

A private THG deck of 100 lunar observing cards — one per feature in Charles A.
Wood's **Lunar 100** — in the visual language of *Cosmic Shards — Stargazing
Cards: The Moon*.

Each card:

- **Front** — locator map with the feature ringed, a close-up photo, a mini
  full-Moon globe, and the selenographic coordinates.
- **Back** — epoch and size, a difficulty slider, best days to observe,
  observation tips, and a short description / name origin / three facts.

Colour-coded by **lunar zone** (four), badged by **feature category** (seven).

## Layout

```
index.html                 local deck-preview app (nav, L-number strip, front/back)
css/card.css               the card system (imports fonts/fonts.css)
js/card.js                 data-driven front/back renderer (LFC.renderCard)
fonts/                     Chakra Petch · Saira Condensed · Barlow  (SIL OFL)
data/lunar100.js           the 100-feature spine, from ../loop/
data/cards.js              authored per-card content (merged onto the spine by id)
data/moon-atlas-db.csv     Rükl / 21st-Century atlas cross-reference
design/mockup-copernicus.html   the approved look (L 5 · Copernicus, front + back)
design/plates/             source imagery + processed plates + SOURCES.md
scripts/                   build scripts (card render, deck imposition) — TBD
cards/                     generated card / deck PDFs (git-ignored)
```

## Dev

```bash
./start_webserver.sh      # http://localhost:8002  (index.html)
```

## Status

Template stage (2026-09-01). Scaffold, data schema, and the data-driven render
template are done; `data/cards.js` has L5 Copernicus authored in full and the
other 99 stubbed. Next: per-card content, then the print proof.
See `Project/docs/design-brief.md` and `Project/docs/card-data-schema.md`.

## Licence

GPL-3.0 (see `LICENSE`), matching sibling project LOOP. Fonts are SIL OFL 1.1.
Imagery is either original THG work or US-Government / public-domain material;
provenance per plate in `design/plates/SOURCES.md`.
