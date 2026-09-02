# Lunar Field Cards

A deck of 100 lunar observing cards — one for each feature in Charles A. Wood's
**Lunar 100** — in the visual language of *Cosmic Shards — Stargazing Cards:
The Moon*.

Each card:

- **Front** — a locator map with the feature marked, a close-up image, a mini
  full-Moon globe, and the selenographic coordinates.
- **Back** — epoch and size, a difficulty rating, the best days to observe,
  observing tips, and a short description with name origin and three facts.

Cards are colour-coded by **lunar zone** (four) and badged by **feature
category** (seven).

## Viewer

`index.html` is a self-contained browser app for paging through the deck. It
runs from any static web server:

```bash
python3 -m http.server 8002      # then open http://localhost:8002
```

The header has previous / next controls, a jump-to-number box, and a
Both / Front / Back toggle. Below it, a grouping strip with a
`Num · Colour · Phase` switch:

- **Num** — ten pills of ten (`1–10` … `91–100`), tinted along a difficulty
  ramp (Wood's numbering runs roughly easiest to hardest).
- **Colour** — one pill per lunar zone, in that zone's colour, filtering the
  strip to that zone.
- **Phase** — seven Moon-phase pills built from each card's best-observing
  windows, with a caption and a **Tonight** switch that highlights the phase
  for the current date.

Click any card image to view it full size. Keyboard: `←` / `→` to move,
`F` / `B` / `D` for front / back / both, `Esc` to close an enlarged image.
The URL tracks the current card (`index.html#L42`), so links are shareable.

**[docs/users-guide.md](docs/users-guide.md)** is the full walkthrough of the
viewer (also as `docs/users-guide.pdf`).

## Layout

```
index.html            the viewer app
docs/users-guide.md    full walkthrough of the viewer  (+ users-guide.pdf)
css/card.css           the card styling (imports fonts/fonts.css)
js/card.js             the front / back card renderer
fonts/                 Chakra Petch · Saira Condensed · Barlow  (SIL OFL 1.1)
data/lunar100.js       the 100-feature list (numbering, names, coordinates, sizes)
data/cards.js          the written content for each card
design/plates/         the card imagery, plus SOURCES.md crediting each plate
```

## Imagery

The locator and close-up panels are rendered as the Moon is actually seen from
the ground: LROC Wide Angle Camera imagery (via LROC QuickMap's LunaServ
service) in an orthographic projection centred on a favourable sub-observer
point, with the sky off the disc left black. Limb and polar features appear as
the foreshortened slivers a telescope shows.

## Licence

Code and text are GPL-3.0 (see `LICENSE`). The bundled fonts are under the SIL
Open Font License 1.1. Imagery is original work or US-Government / public-domain
material; the source and credit for every plate are listed in
`design/plates/SOURCES.md`.
