# Plate sources & provenance

Every image used on a card records its source, credit line and licence here.
`src-*` files are the originals (git-ignored, re-fetchable from the URL);
`plate-*` files are the processed crops that go on the card.

Unless noted otherwise, every image below is a work of the U.S. Government
(NASA) or a NASA / university partner (LROC is NASA / GSFC / Arizona State
University) and is in the public domain, Wikimedia Commons tag
`PD-USGov-NASA`. Batch-1 plates were retrieved 2026-09-01 from Wikimedia
Commons via `Special:FilePath/<file name>`.

Processing tool: ImageMagick 7. Common steps: `-colorspace sRGB -strip
-quality 82`.

---

## L1 · Moon

**plate-L1-scene.jpg** (left / scene panel) ← `src-l1-scene-moon-mountains.jpg`
- Full Moon rising over a snow-lit mountain ridge at sunset. A concept card, so
  the left panel carries an evocative scene instead of a locator map.
- Supplied by Aaron from `/Volumes/Starfish_Backup/moon-field-card/`
  (filename marked "no-copyright"). **Attribution / licence not yet verified —
  confirm origin before the deck ships.**
- Processing: resized to 1000 px wide, EXIF stripped, JPEG q82.

**plate-L1-photo.jpg** (right / close-up panel) ← `src-moon-nearside-lro.jpg`
- LROC Wide Angle Camera near-side mosaic. Credit: NASA / GSFC / Arizona State University.
- Commons: `File:Moon nearside LRO.jpg`
- Processing: resized to 1200 px.

## L2 · Earthshine

Batch-1 Apollo 12 plate replaced 2026-09-01 with two Aaron-supplied images.

**plate-L2-scene.jpg** (left / scene panel) ← `src-l2-scene-crescent-trees.jpeg`
- Twilight crescent Moon low over a tree-line horizon, orange-to-blue sky.
- Supplied by Aaron from `/Volumes/Starfish_Backup/moon-field-card/`.
  **Attribution / licence not verified** (same open question as L1).
- **Low resolution: source is only 276 × 478 px.** Upscaled for the panel; fine
  for screen preview, not for the print PDF. Needs a larger version.
- Processing: resized to 1000 px wide, EXIF stripped, JPEG q82.

**plate-L2-photo.jpg** (right / close-up panel) ← `src-l2-earthshine-crescent.png`
- Telescopic crescent Moon with strong earthshine, whole disc visible in ashen
  light, bright sunlit limb. 1110 × 1043 source.
- Supplied by Aaron from `/Volumes/Starfish_Backup/moon-field-card/`.
  **Attribution / licence not verified.**
- Processing: resized to 1400 px wide, JPEG q82.

## L3 · Mare / highland dichotomy

Panels reversed 2026-09-01 (Aaron): the annotated scope view is the left panel,
the near/far two-up the right.

**plate-L3-annotated.jpg** (left panel) ← `src-l3-dichotomy-annotated.jpg`
- Telescopic waning-gibbous Moon with two rings drawn on it: one over a smooth
  mare, one over the cratered southern highlands, showing the dichotomy in a
  single scope view. 700 × 887 source.
- Supplied by Aaron from `/Volumes/Starfish_Backup/moon-field-card/`.
  **Attribution / licence not verified** (same open question as L1).
- Processing: resized to 1200 px wide, JPEG q82.

**plate-L3-nearfar.jpg** (right panel) ← `src-moon-nearside-lro.jpg` + `src-moon-farside-lro.jpg`
- Two-up: near side (left), far side (right), LROC WAC mosaics. The far side is almost all highland. Credit: NASA / GSFC / ASU.
- Commons: `File:Moon nearside LRO.jpg`, `File:Moon Farside LRO.jpg`
- Processing: each resized to 700 px, joined with a 14 px gutter (`magick +smush 14`).

## L4 · Apennines

**plate-L4-scene.jpg** (left / scene panel) ← `src-l4-scene-apennines.png`
- Telescopic view of the Apennine range along the terminator, Mare Imbrium to
  the west. 626 × 872 source.
- Supplied by Aaron from `/Volumes/Starfish_Backup/moon-field-card/`.
  **Attribution / licence not verified.** A burned-in caption
  ("Raleigh - Stagecoach · April 10, 2008") points to a Raleigh, NC amateur
  capture; origin to confirm.
- Processing: chopped 34 px off the top to remove the caption, resized to 1000 px
  wide, EXIF stripped, JPEG q82.

**plate-L4-photo.jpg** (right / close-up panel) ← `src-apenninus-lro.png`
- LRO mosaic of the Montes Apenninus along the southeast rim of Mare Imbrium. Credit: NASA / GSFC / ASU.
- Commons: `File:Montes Apenninus (LRO).png`
- Processing: resized to 1500 px wide.

## L5 · Copernicus

**plate-L5-photo.jpg** (front photo panel) ← `src-copernicus-lro-wac.png`
- LROC Wide Angle Camera mosaic, 150 km across, north up. Credit: NASA / GSFC / Arizona State University.
- Commons: `File:Copernicus (LRO) 2.png` (1264 × 1264, `PD-USGov-NASA`)
- Processing: resized to 1400 × 1400.
- Added 2026-09-01 as the straight-on primary view, replacing the Lunar Orbiter 2 oblique.

**plate-L5-photo2.jpg** ("Another view" inset) ← `src-lunarorbiter2-copernicus.jpg`
- Lunar Orbiter 2, 1966, the "Picture of the Century" oblique. Credit: NASA / JPL / USGS.
- Retrieved earlier from `https://science.nasa.gov/resource/copernicus-from-lunar-orbiter/`
  (asset `assets.science.nasa.gov/.../lunarorb_copernicus.jpg`).
- Processing: trimmed ~70 px of top sky, 1400 px wide.
- Was the front photo panel on the approved mockup; moved to the inset 2026-09-01.

**plate-L5-locator.jpg** (front locator panel) ← `src-lroc-wac-copernicus.png`
- LROC WAC colour mosaic of Copernicus and its ray system ("Absolute Time", LROC featured image 480). Credit: NASA / GSFC / ASU.
- Commons: `File:Absolute Time (LROC480 - copern lwac731a).png`, via
  `https://commons.wikimedia.org/wiki/Special:FilePath/Absolute%20Time%20(LROC480%20-%20copern%20lwac731a).png`
- Processing: cropped off the burned caption strip, desaturated to ~24 %, 700 px wide, q84.

**src-lroc238-copernicus-context.png / src-lroc473-copernicus-floor.png** (not used)
- LROC WAC context mosaic (annotated) and LROC NAC floor-detail mosaic. NASA / GSFC / ASU.
- Kept as candidates for a wider production locator.

## L6 · Tycho

Right panel changed 2026-09-01 (Aaron): the dramatic LRO NAC sunrise oblique is
a spacecraft-only angle; replaced with a near-vertical view that matches what a
telescope shows from Earth.

**plate-L6-scene.jpg** (left / scene panel) ← `src-l6-scene-tycho-wide.png`
- Wide telescopic view of the southern highlands with Tycho and its rays.
  411 × 495 source (low resolution; fine for screen, soft for print).
- Supplied by Aaron from `/Volumes/Starfish_Backup/moon-field-card/`.
  **Attribution / licence not verified.**
- Processing: resized to 1000 px wide, EXIF stripped, JPEG q82.

**plate-L6-photo.jpg** (right / close-up panel) ← `src-l6-tycho-lro-wac.png`
- LROC Wide Angle Camera mosaic of Tycho, 120 km across, north up, near-vertical.
  Credit: NASA / GSFC / Arizona State University.
- Commons: `File:Tycho LRO.png` (1058 × 1058, `PD-USGov-NASA`)
- Processing: resized to 1400 × 1400, JPEG q82.

**src-tycho-lro-centralpeak.jpg** (not used) — `File:LRO Tycho Central Peak.jpg`,
the LRO NAC sunrise oblique. Kept as a candidate for an "Another view" inset.

## L7 · Altai Scarp

**plate-L7-scene.jpg** (left / zoomed-out panel) ← `src-l7-scene-nectaris-lro.png`
- The whole Mare Nectaris basin; Rupes Altai is its southwestern ring. LROC WAC.
  Credit: NASA / GSFC / ASU.
- Commons: `File:Mare Nectaris (LRO).png` (2750 × 2750, `PD-USGov-NASA` family)
- Processing: resized to 1400 × 1400, JPEG q82.

**plate-L7-photo.jpg** (right / close-up panel) ← `src-altai-lroc-wac.jpg`
- LROC Wide Angle Camera view of the full arc of Rupes Altai. Credit: NASA / GSFC / ASU.
- Commons: `File:Rupes Altai - LROC - WAC.JPG`
- Processing: resized to 1200 px wide, centre-cropped to 1200 × 1350.
- ⚠️ **Has burned-in white labels** (Catharina, Fermat, Pons, Polybius, Rupes
  Altai, etc). The `- LROC - WAC.JPG` Commons set is an annotated atlas. No clean
  dedicated Altai view found yet; replace this panel with an unlabelled crop.

## L8 · Theophilus, Cyrillus, Catharina

**plate-L8-scene.jpg** (left / zoomed-out panel) ← `src-l8-scene-nectaris-lro.png`
- The trio sits on the northwest rim of Mare Nectaris; this is a NW crop of the
  same LROC WAC basin mosaic used on L7. Credit: NASA / GSFC / ASU.
- Commons: `File:Mare Nectaris (LRO).png` (2750 × 2750, `PD-USGov-NASA` family)
- Processing: cropped to the NW quadrant (`-gravity northwest -crop 1950x2300+100+100`),
  resized to 1150 px wide, JPEG q82.

**plate-L8-photo.jpg** (right / overhead panel) ← `src-l8-scene-nectaris-lro.png`
- All three craters from directly overhead: Theophilus (sharp, terraced, central
  peak) at top, Cyrillus (degraded) centre, Catharina (worn) bottom, the
  degradation sequence in one view. Cropped from the same LROC WAC basin mosaic
  as the left panel. Credit: NASA / GSFC / ASU.
- Commons: `File:Mare Nectaris (LRO).png` (2750 × 2750, `PD-USGov-NASA` family)
- Processing: cropped to the trio (`-crop 1120x1050+210+700`), resized to 1300 px
  wide, JPEG q82. Crop centring checked by eye against the rendered image.
- Changed 2026-09-01 (Aaron): Apollo 16 oblique → overhead of the trio. An
  interim single-Theophilus WAC frame (`File:Central Peak Bedrock (LROC428 -
  Theophilus WAC).png`) was rejected for not showing all three.

**Both L8 panels now derive from `File:Mare Nectaris (LRO).png`** (different
crops). Flag: find a distinct overhead if we want them from separate sources.

**src-theophilus-as16.jpg** (not used) — `File:Theophilus crater AS16-113-18295HR.jpg`,
Apollo 16 oblique on Orion's approach. Kept as an "Another view" candidate.

## L9 · Clavius

**plate-L9-photo.jpg** ← `src-clavius-lo4.png`
- Lunar Orbiter 4 frame of Clavius and its curving chain of floor craters, 1967. Credit: NASA.
- Commons: `File:Lunar Orbiter 4 FRAME 4107 M p13.png`
- Processing: reduced to 8-bit, resized to 1300 px wide, centre-cropped to 1300 × 1300.

## L10 · Mare Crisium

**plate-L10-scene.jpg** (left / scene panel) ← `src-l10-scene-crisium.png`
- Telescopic near-limb view of a large circular basin with a raised highland
  ring, the lunar edge running down the right side. 397 × 525 source
  (low resolution; fine for screen, soft for print).
- Supplied by Aaron from `/Volumes/Starfish_Backup/moon-field-card/`.
  **Attribution / licence not verified.**
- **Identification to confirm:** the floor reads lighter and greyer than a
  classic dark mare, so this may not be Mare Crisium (could be Mare
  Humboldtianum or another limb basin). The isolated circular form at the limb
  does fit Crisium under low sun / high libration.
- Processing: resized to 1000 px wide, EXIF stripped, JPEG q82.

**plate-L10-photo.jpg** (right / close-up panel) ← `src-crisium-as17.jpg`
- Mare Crisium, Apollo 17 mapping-camera mosaic, 1972. Credit: NASA.
- Commons: `File:Mare Crisium AS17-M-0913-0919-0924.jpg`
- Processing: resized to 1500 px wide.
- Still flagged: the source is a wide, short mosaic strip (1768 × 543) and
  letterboxes in the panel. Needs a squarer frame or an original capture.

---

# Batch 2 (L11–L20)

LEFT panel = wide finder field; RIGHT panel = narrow eyepiece detail. All
public-domain (NASA / LROC / Lunar Orbiter / Apollo). The Commons
`… - LROC - WAC.JPG` atlas set was avoided where possible: it carries burned-in
labels. Prose for these cards is not yet written.

## L9 · Clavius  (left panel = VMA locator, 2026-09-01)

**plate-L9-scene.jpg** (left, locator map) ← `src-moonbase-wac.jpg`
- ~50°-wide field centred on Clavius (58.8°S, 14.1°W), cropped from the
  project's Virtual Moon Atlas near-side base map. Maginus upper-left, the
  south-polar terrain along the bottom edge. The orange ring is drawn by the
  renderer from the card's `outline` field, not baked into the plate.
- Source: **VMA `WAC_LOWSUN` level-2 tiles** (LROC WAC low-sun-angle mosaic,
  NASA / Arizona State University), assembled by `tools/build-moonbase.sh` into
  a 10000×5000 equirectangular map (`src-moonbase-wac.jpg`, git-ignored).
- Processing: crop `2529×1389+3344+3439` from the base (longitude widened by
  1/cos lat, then squeezed to `1100×1038` so craters read round), `-colorspace
  sRGB -brightness-contrast 3x5`, quality 88. Native grayscale kept.
- This is the first card on the new plan: one VMA base map, every locator panel
  a crop of it. Supersedes the first-quarter telescopic crop
  (`File:First quarter moon.jpg`, Astrobond, CC BY-SA 4.0) which was itself a
  fix for the earlier Lunar Orbiter 4 frame. Both earlier `src-l9-*` files
  stay on disk (git-ignored), unused.

**plate-L9-photo.jpg** (right) ← `src-l9-narrow-clavius-lroc.jpg`
- Clavius floor and its curving crater arc, LROC. NASA / GSFC / ASU.
- Commons: `File:Clavius LROC.jpg` (707 × 758 — low resolution, soft for print).
- Processing: resized to 1000 px wide.

## L11 · Aristarchus

**plate-L11-scene.jpg** (left) ← `src-l11-wide-aristarchus-plateau-lro.png`
- The Aristarchus Plateau with Vallis Schröteri; Aristarchus bright at lower
  right, Herodotus lava-flooded beside it. LROC WAC. NASA / GSFC / ASU.
- Commons: `File:Aristarchus Plateau (LRO).png` (2706 × 2706, clean/unlabelled)
- Processing: resized to 1300 px wide.

**plate-L11-photo.jpg** (right) ← `src-l11-narrow-aristarchus-as15.jpg`
- Aristarchus, oblique close-up from Apollo 15. NASA.
- Commons: `File:Aristarchus crater hrp162.jpg` (1437 × 1066)
- Processing: resized to 1400 px wide.

## L12 · Proclus

**plate-L12-scene.jpg** (left) ← `src-l12-wide-proclus-as17.jpg`
- Proclus and the western shore of Mare Crisium, Apollo 17. NASA.
- Commons: `File:Proclus crater AS17-150-23046.jpg` (1136 × 1136)
- Processing: resized to 1200 px wide.

**plate-L12-photo.jpg** (right) ← `src-l12-narrow-proclus-as17.jpg`
- Proclus interior, oblique from Apollo 17. NASA.
- Commons: `File:Proclus crater hrp147.jpg` (800 × 1675)
- Processing: centre-cropped to ~square, resized to 1200 px wide.

## L13 · Gassendi

**plate-L13-scene.jpg** (left) ← `src-l13-wide-humorum-lro.png`
- Mare Humorum, with Gassendi cut into its north rim. LROC WAC. NASA / GSFC / ASU.
- Commons: `File:Mare Humorum (LRO).png` (2744 × 2744, clean/unlabelled)
- Processing: resized to 1300 px wide.

**plate-L13-photo.jpg** (right) ← `src-l13-narrow-gassendi-lro.png`
- Gassendi, LROC Wide Angle Camera. NASA / GSFC / ASU.
- Commons: `File:Gassendi (LRO).png` (1520 × 1520)
- Processing: resized to 1400 px wide.

## L14 · Sinus Iridum

Both panels are crops of one NASA image (a public-domain LRO perspective view);
flag for a distinct narrow view later.

**plate-L14-scene.jpg** (left) ← `src-l14-sinus-iridum-nasa.jpg`
- Sinus Iridum and the Jura Mountains arc, LRO perspective view. NASA (`PD-USGov`).
- Commons: `File:Sinus Iridum.jpg` (1428 × 788)
- Processing: centre-cropped, resized to 1200 px wide.

**plate-L14-photo.jpg** (right) ← same source
- Processing: tighter centre crop of the bay, resized to 1200 px wide.

## L15 · Straight Wall  (Rupes Recta)

**plate-L15-scene.jpg** (left) ← `src-l15-wide-thebit-lro.png`
- The Straight Wall (thin dark line, centre) with Birt to its west and Thebit to
  its east, in eastern Mare Nubium. LRO. NASA / GSFC / ASU.
- Commons: `File:Ancient Thebit (LRO).png` (2116 × 2116, clean/unlabelled)
- Processing: resized to 1300 px wide.

**plate-L15-photo.jpg** (right) ← `src-l15-narrow-rupesrecta-as16.jpg`
- Rupes Recta, Birt and Rima Birt, oblique from Apollo 16. NASA / GSFC / ASU.
- Commons: `File:Rupes Recta Birt crater AS16-M-2486 ASU.jpg` (1600 × 1000)
- Processing: resized to 1400 px wide.

## L16–L100 · left (locator) panels — VMA base map, batch 2026-09-01

`plate-L16-scene.jpg` … `plate-L100-scene.jpg` (85 files) generated by
`tools/build-locator-plates.py 16 100`, each a crop of `src-moonbase-wac.jpg`
(the assembled Virtual Moon Atlas `WAC_LOWSUN` near-side map — see the L9 entry).

- Centred on the feature's spine lat/lon; field of view scales with feature
  size (~36–64° of latitude); longitude widened by 1/cos(lat) then squeezed on
  export so craters read round. Output 1100 × 1038 (locator-pane aspect).
- `data/cards.js` for each of these got `locator`, `locatorCredit`
  ("LROC WAC low-sun mosaic (Virtual Moon Atlas). NASA / ASU.") and an
  `outline` ring sized from the feature's angular diameter.
- **Rougher on the equirectangular base (flagged, revisit):** L37, L56, L70,
  L73, L76, L80, L87, L88, L94, L96, L100 — high latitude or extreme limb, where
  the base map smears. L88 (Peary, 88.6°N) is the worst; its crop runs into the
  polar-cap tile edge.
## L16–L100 · right (close-up) panels — LROC WAC mosaic, batch 2026-09-01

`plate-L16-photo.jpg` … `plate-L100-photo.jpg` (85 files) generated by
`tools/build-closeup-plates.py 16 100`.

- Source: **LRO LROC WAC Global Mosaic, 100 m/px** (`LRO_WAC_Mosaic_Global_303ppd_v02`),
  the equirectangular WMTS pyramid served by **NASA Solar System Treks**
  (`trek.nasa.gov/tiles/Moon/EQ/...`, z0–z8). NASA / GSFC / Arizona State
  University; public domain.
- Per feature: zoom chosen so the field of view is ~1500 px; covering tiles
  fetched (cached under `.trekcache/`, git-ignored), stitched, cropped
  (longitude widened by 1/cos lat so the feature reads round), resized to
  1400 × 1050, `-normalize -sigmoidal-contrast 3.5x46%`, quality 88.
- `data/cards.js` for each got `photo`, `photoTag:"NASA · LROC WAC"`,
  `photoCredit:"LROC WAC global mosaic (100 m/px). NASA / GSFC / Arizona State University."`
- **Poor — need a polar-stereographic source (equirect mosaic smears to
  streaks here):** **L88 Peary** (88.6°N), **L94 Drygalski** (79.3°S),
  **L96 Leibnitz Mountains** (85°S). Currently placeholder-grade.
- **Acceptable but wide / limb-distorted:** L56, L73, L80, L87, L100 — big
  basins or far-limb; framed as a representative chunk, not the whole feature.
- Big basins (L80 Orientale 930 km, L95 Procellarum ~2500 km, L54/L73/L77) are
  capped at a 9° field, so the close-up shows the centre, not the full ring
  system.

---

## Production note

The mockup and batch-1 plates are public-domain stand-ins. The finished deck
uses Aaron's own Seestar / processed captures in the close-up panel wherever one
exists, with LRO / LROC / Lunar Orbiter / Apollo public-domain imagery as the
fallback. The "Another view" inset is an optional second image per card; on L5 it
carries the historic Lunar Orbiter 2 oblique.

The Copernicus locator labels and orange ring are placed by eye, not projected
from coordinates; a production locator should use a wider projected mosaic.
