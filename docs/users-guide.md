---
title: "Lunar Field Cards — User's Guide"
date: 2026-11-20
status: active
description: How to use the Lunar Field Cards site.
---

# User's Guide

The Lunar Field Cards site shows all 100 cards in the browser — front and back —
with tools to search them, page through them, group them by decade, lunar zone
or Moon phase, and enlarge the imagery.

## The header bar

| Control | What it does |
|---------|--------------|
| **◀ / ▶** | Previous / next card **within the selected pill** (see the grouping strip below). Wraps at the ends of that pill's list. |
| **number box** | Jump to a card by its L-number. It is scoped to the selected pill: its min/max track the pill, and a number outside the pill snaps to the nearest L that is in it. |
| **L n · Name** | The current card's L-number and feature name. |
| **meta** | The current card's lunar zone and feature category ("no zone" for the concept cards L1–L3). |
| **Search cards** | Find a card by name or by anything written on it. See [Search](#search) below. Press `/` to jump to it. |
| **Both / Front / Back** | Show both faces side by side, or just one. Also `D` / `F` / `B` on the keyboard. |

## Search

Type in the **Search cards** box in the header bar, or press `/` from anywhere
on the page to jump to it. A list of matching cards opens under the box as you
type.

**What it searches:**

- the feature name and its Latin name (Rupes Recta, Vallis Schröteri…)
- Wood's one-line note for the feature
- its lunar zone, category and epoch
- the text on the back of the card: description, name origin, facts and tips

Matches in a name come first. Accents and apostrophes don't matter, so
`schroters valley` finds Schröter's Valley. Each word you type has to start a
word on the card, so `ray` finds "rays" but not "gray". Type at least two
letters.

**Searching by number:** type `28` or `L28` to go to L28. A single digit lists
the cards that start with it: `2` gives L2, then L20 to L29.

**Reading the results:** each row shows the L-number, the name and Latin name,
and a dot in the card's zone colour. The second line is the zone and category
when the name matched, or else the bit of the card where the match is, labelled
by where it came from (**Fact**, **Tips**, **Epoch**…). Every match is
highlighted in orange.

**Opening a card:** click a result, or move with **↑** / **↓** and press
**Enter**. **Esc** closes the list, and a second **Esc** clears the box. If the
card you open isn't in tonight's phase, the Tonight switch turns off.

## The grouping strip

Under the header is a row of **pills** and a `Num · Color · Phase` toggle that
chooses what the pills mean. Whatever pill is active defines the list the
◀ ▶ arrows, the arrow keys and the number box walk. Click a pill to jump to
its first card. The current card's pill is always the highlighted (orange) one;
below the pills, a second row of small buttons is the **card strip** for that
pill, each with a small status dot (stub / draft / review / final) — click one
to go straight to that card.

### Num — by decade

Ten pills, `1–10` … `91–100`. Wood ordered the Lunar 100 by roughly increasing
difficulty, so each decade is a difficulty band; the pills are tinted along the
same green → amber → rust ramp as the difficulty slider on the back of a card.

### Color — by lunar zone

Four pills, one per zone, each in that zone's own colour:

| Zone | Colour |
|------|--------|
| Eastern Limb | steel blue |
| Eastern Interior | forest green |
| Western Interior | light red |
| Western Limb | light yellow |

The two **Limb** zones are the foreshortened, libration-dependent edges of the
disc; the two **Interior** zones are the central maria. Selecting a zone pill
filters the strip to that zone's cards. The three concept cards (L1–L3) have no
zone; in Color mode they fall back to the Eastern Limb strip.

### Phase — by Moon phase

Seven pills labelled with the Moon-phase glyphs:

| Glyph | Phase | Lunar age (days) |
|-------|-------|------------------|
| 🌒 | Waxing Crescent | 0–7 |
| 🌓 | First Quarter | 7–11 |
| 🌔 | Waxing Gibbous | 11–15 |
| 🌕 | Full | 15–18 |
| 🌖 | Waning Gibbous | 18–22 |
| 🌗 | Last Quarter | 22–26 |
| 🌘 | Waning Crescent | 26–30 |

Each card is placed by its **best-days** windows (lunar age), so a card with a
sunrise window and a sunset window shows up under two pills and the pill counts
add up to more than 100. New Moon is dropped — there is nothing to observe — and
those days fold into the 🌒 pill.

A **caption** between the pills and the strip names the selected phase and its
day range, e.g. `WAXING GIBBOUS · DAY 11–15`.

#### The Tonight switch

In Phase mode a `Tonight 🌖` button sits after the glyph pills. It works out
tonight's Moon age from the current date and, when toggled on:

- greys out every phase pill except tonight's,
- gives tonight's pill an accent ring and jumps the strip to it,
- adds `· TONIGHT` to the caption.

Toggle it off, click any other phase pill, or leave Phase mode to return to the
normal view. It is a quick "what's well placed for me right now" filter.

## Enlarging an image

Click any card image — the locator panel, the close-up, or the small "Another
view" inset — to open it full size in a lightbox. Click the image again to
toggle 1:1 (actual pixels) versus fit-to-window. Click the backdrop, the ✕, or
press **Esc** to close.

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| **/** | Jump to the search box |
| **←** / **→** | Previous / next card in the selected pill |
| **F** | Front only |
| **B** | Back only |
| **D** | Both faces |
| **Esc** | Close the lightbox |

In the search box, **↑** / **↓** move through the results, **Enter** opens one,
and **Esc** closes the list (press it again to clear the box). The page
shortcuts don't fire while you're typing in the search box, or when Cmd, Ctrl
or Alt is held, so browser shortcuts like Cmd-F work as usual.

## Deep links

The URL hash tracks the current card: adding `#L42` to the site's address opens
straight to L42, and the address updates as you move, so a copied link always
points at the card you were on.
