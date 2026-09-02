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
index.html                 local deck-preview app (grouping strip, front/back, enlarge)
users-guide.md             how to drive the preview app  (+ users-guide.pdf)
css/card.css               the card system (imports fonts/fonts.css)
js/card.js                 data-driven front/back renderer (LFC.renderCard)
fonts/                     Chakra Petch · Saira Condensed · Barlow  (SIL OFL)
data/lunar100.js           the 100-feature spine, from ../loop/
data/cards.js              authored per-card content (merged onto the spine by id)
data/moon-atlas-db.csv     Rükl / 21st-Century atlas cross-reference
design/mockup-copernicus.html   the approved look (L 5 · Copernicus, front + back)
design/plates/             processed plates (plate-L*-{scene,photo}.jpg) + SOURCES.md
                           src-* originals and .trekcache/ are git-ignored
tools/                     build-plates-lunaserv.py  (the Earth-view panel builder) ·
                           fill-prose-21-100.py  (one-shot prose) ·
                           build-moonbase.sh / build-locator-plates.py /
                           build-closeup-plates.py  (earlier nadir pipeline, kept)
cards/                     generated card / deck PDFs (git-ignored)
```

## Dev

```bash
./start_webserver.sh      # http://localhost:8002  (index.html)
```

## Preview app

`index.html` is a local browser tool for reviewing the deck. Header: prev/next
and a number box (both scoped to the selected pill), and a Both/Front/Back
toggle. Below it a grouping strip with a `Num · Color · Phase` switch —

- **Num** — ten decade pills (`1–10` … `91–100`), tinted along the difficulty
  ramp (Wood's L-order is his difficulty order).
- **Color** — four pills, one per lunar zone in that zone's colour
  (ER steel blue, EH forest green, WH light red, WR light yellow), filtering
  the strip to that zone.
- **Phase** — seven Moon-phase glyph pills (🌒 → 🌘) built from each card's
  best-days windows by lunar age, a caption naming the selected phase, and a
  **Tonight** switch that isolates the current phase from today's date.

Click any card image — locator, close-up, or the "Another view" inset — to see
it full size. Full walkthrough in `users-guide.md`.

## Status

Content draft (2026-09-02). Scaffold, data schema, and the data-driven renderer
are done. **All 100 cards are `status:"draft"`** — full prose (epoch, size,
best days, description, name origin, facts, tips) and per-card difficulty.

**Imagery — the Earth / telescope view.** These are observing cards, so both
panels are rendered as the Moon is actually seen from the ground: LROC WAC
imagery (via LROC QuickMap's LunaServ engine) in an orthographic projection
centred on a favourable-libration sub-observer point, off-disc sky black, the
feature marked on the locator with a small orange dot
(`tools/build-plates-lunaserv.py`). Limb and polar features come out as the
foreshortened slivers you'd really see. All of L7 and L10–L100 are on this
pipeline; L1–L6, L8 use bespoke scenes and L9 is the last nadir straggler.
Where Aaron has an original capture it goes in the "Another view" inset (L5, L7).

Open: an accuracy / ephemeris review of the prose, then the print proof.
See `Project/docs/design-brief.md` and `Project/docs/card-data-schema.md`.

## Licence

GPL-3.0 (see `LICENSE`), matching sibling project LOOP. Fonts are SIL OFL 1.1.
Imagery is either original THG work or US-Government / public-domain material;
provenance per plate in `design/plates/SOURCES.md`.
