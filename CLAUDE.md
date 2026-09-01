# CLAUDE.md — Lunar Field Cards

## What This Is

Lunar Field Cards is a private THG deck of **100 lunar observing cards**, one
per feature in **Charles A. Wood's "Lunar 100"**, modelled closely on the
commercial *Cosmic Shards — Stargazing Cards: The Moon* set: landscape
laminated card, burnt-orange-on-black system, a **front** that helps you find
the feature (locator map + close-up photo + mini globe + coordinates) and a
**back** that briefs it (specs, difficulty, best days, observation tips,
description, name origin, three facts).

What makes it ours rather than a reprint: the data spine is the Lunar 100 (fed
from **LOOP**'s `lunar100.js`), and the feature photos are meant to be Aaron's
own Seestar / processed captures out of the `astro.thgnetworks` pipeline, with
NASA / LRO imagery only as the fallback where a capture doesn't exist yet.

**Domain:** personal astronomy — lunar observing, card/print design, the Lunar 100
**Working directory:** `/Users/wahender/My_Library/Tech/git_repos/astronomy/lunar-cards/`
**Parent:** Standing directives from the THG Media CLAUDE.md carry forward.
**Siblings:** `../loop/` (Lunar 100 web log — the data spine), `../luna/` & `../luna2/` (Moon atlases), `../astro/` (astronomy hub), `../images/` (astrophotography gallery), `../mmol/`.

---

## Mission

> Put the Lunar 100 in your coat pocket: 100 durable cards that tell you where
> a feature is, what it looks like up close, and what to know about it — in the
> Cosmic Shards visual language, on THG's own imagery.

---

## Team

Load current profiles from `~/.claude/team/staff/` at session start — do not
copy them here (they go stale).

| Name | Role on Lunar Field Cards | Profile |
|------|--------------------------|---------|
| Astrid Star | Imaging lead — feature photos, plate selection, LRO fallbacks, provenance | `~/.claude/team/staff/astrid.md` |
| Lila | Technical lead — card template, print/PDF pipeline, build scripts | `~/.claude/team/staff/lila.md` |
| Kate | Web / card design — the Cosmic Shards visual language, badge icons, typography | `~/.claude/team/staff/kate.md` |
| Terry | Development, QA | `~/.claude/team/staff/terry.md` |
| Pam | Coordination, change log | `~/.claude/team/staff/pam.md` |
| Sara | Document registry & update gate | `~/.claude/team/staff/sara.md` |

---

## Technical Stack

- **No framework.** Plain HTML / CSS / JS.
- **Card system:** `css/card.css` (+ `fonts/fonts.css`), extracted from the
  approved mockup at `design/mockup-copernicus.html`. Every internal size is in
  `cqw`, so one `.lfc-card` renders at any width.
- **Data spine:** `data/lunar100.js` (`const DATA = [...]`, 11-field rows),
  copied from `../loop/`. Card-specific fields (zone, epoch, difficulty, best
  days, prose, plate) are layered on top — schema TBD (Step 2).
- **Atlas cross-reference:** `data/moon-atlas-db.csv` (Rükl / 21st-Century / Aristarchus codes).
- **Print pipeline:** card HTML → PDF via WeasyPrint (`thg-media/tools/generate_pdf.py`
  pattern), fixed 6.1 × 4.4 in + bleed, with cut guides. Output to `cards/`.
- **Local dev:** `./start_webserver.sh` (port 8002) — plain `python3 -m http.server`.
- **Web viewer:** a possible sibling to LOOP later; candidate domain `cards.thgnetworks.com` (not decided).

---

## Fonts (all SIL OFL 1.1)

Vendored in `fonts/` with their `OFL-*.txt`. Free stand-ins for the deck's
proprietary faces:

| Family | Role |
|--------|------|
| Chakra Petch | display — card title, section headers, badges |
| Saira Condensed | utility labels — coordinates, epoch, difficulty, map pins |
| Barlow | body — description, tips, facts |

---

## Design System

**Palette**

| Token | Hex | Usage |
|-------|-----|-------|
| ground | `#0C0B0A` | card background |
| panel | `#151310` | inset panels |
| accent | `#E36A1E` | burnt orange — the one bold colour |
| ink | `#EDE9E3` | primary text |
| muted | `#928C83` | secondary text |

**Four lunar zones** (colour-coded tab, top-right of the front):
Eastern Rim `#6D8299` · Eastern Heartland `#8B8F98` · Western Heartland `#9C7F6A` · Western Rim `#6F6862`

**Seven feature categories** (badge, top-right of the back):
Maria & Plains · Craters · Valleys & Rilles · Special Phenomena · Ridges & Scarps · Mountains · Volcanoes & Domes

---

## Data & Licensing

- **Lunar 100** text (names, significance, coords, charts) — from Wood's
  S&T article, via LOOP. Prose on the cards is written fresh, not copied.
- **Imagery** — Aaron's own captures, or US-Government / public-domain LRO /
  LROC / Lunar Orbiter / Apollo material. Every plate records its exact
  source, credit line, and retrieval URL in `design/plates/SOURCES.md`.
  Nothing goes on a card without its provenance line.
- Repo licence: GPL-3.0 (matches sibling LOOP).

---

## Working Norms

- **Document Registry & Update Gate** (Sara): `Project/docs/document-index.md`
  is the living registry. On "update docs", Sara scans, lists proposed changes
  one line each (plus PDF companions), and waits for Aaron's approval.
- **PDF with Every MD**: every `.md` gets a branded PDF via
  `thg-media/tools/generate_pdf.py`, except `Project/notes/change-log.md` and
  any `Project/*/notes.md`. Batch the builds — only when Aaron says ready.
- **Change log** (Pam): `Project/notes/change-log.md`.
- **Never commit until told.** Verify locally, Aaron confirms, then commit.
- Card template / pipeline changes go through Lila; imagery and plate calls go through Astrid.

---

*Started 2026-09-01 in the Ready Room (Aaron, Astrid, Lila, Sara), off the*
*approved Copernicus mockup. Working title "Lunar Field Cards" — not final.*
