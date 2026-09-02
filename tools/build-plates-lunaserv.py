#!/usr/bin/env python3
"""build-plates-lunaserv.py -- (re)build card panels as the EARTH / TELESCOPE
view from LROC QuickMap's engine.

These are observing cards; the Moon is never seen from directly overhead. So we
render the LROC WAC global mosaic (`luna_wac_global`, served by the LunaServ WMS
at wms.im-ldi.com -- the engine behind quickmap.lroc.im-ldi.com) in an
ORTHOGRAPHIC projection centred on a sub-observer point, with a little
favourable libration toward the feature, off-disc sky forced black.

  SRS   = AUTO:42003,9001,<lon0>,<lat0>     (orthographic)
  sphere= 6 378 137 m  (PROJ's default -- NOT the Moon's radius; a quirk we ride)
  bbox  = projection metres, cropped to the feature's projected (x,y)

Left (locator): 44 deg field, crop pulled ~40% back toward disc centre so the
feature sits in context with the limb often in view; a small orange dot marks
it (written to `outline.cx/cy`). Right (close-up): per-feature field, centred
on the feature.

Usage:  tools/build-plates-lunaserv.py --only L11,L12 [--panel both|left|right] [--dry-run]
"""
import math, os, re, subprocess, sys, urllib.parse

ROOT   = __file__.rsplit("/tools/", 1)[0]
PLATES = ROOT + "/design/plates"
CARDS  = ROOT + "/data/cards.js"
MAGICK = "/opt/homebrew/bin/magick"
WMS    = "https://wms.im-ldi.com/"
LAYER  = "luna_wac_global"
UA     = "LunarFieldCards/0.1 (THG Media; hikerdad@gmail.com)"
CREDIT = "LROC WAC (LROC QuickMap / LunaServ), rendered as the Earth view. NASA / GSFC / ASU."

R      = 6378137.0                 # PROJ default sphere for AUTO:42003
U_PER_DEG = R * math.pi / 180.0    # ~111 320 projection units per degree at disc centre
LOC_FOV   = 44.0                   # locator field, degrees
LOC_PULL  = 0.85                   # locator crop centre = feature xy * this (gentle pull toward disc centre)

# id: (lat, lon E+, close-up field of view in degrees)
JOBS = {
 "L7":  ( -23.5,  24.5, 13.0),  # Rupes Altai
 "L10": (  18.0,  59.0, 15.0),  # Mare Crisium
 "L11": (  23.7, -47.4,  3.5),  # Aristarchus
 "L12": (  16.1,  46.8,  3.0),  # Proclus
 "L13": ( -17.6, -40.1,  7.0),  # Gassendi
 "L14": (  45.0, -32.0, 15.0),  # Sinus Iridum
 "L15": ( -21.8,  -7.8,  6.0),  # Straight Wall
 "L16": ( -25.1,  60.4,  8.0),  # Petavius
 "L17": (  26.2, -50.8,  8.0),  # Schroter's Valley
 "L18": (  17.8,  23.0, 20.0),  # Mare Serenitatis dark edges
 "L19": (  49.0,   3.0,  8.0),  # Alpine Valley
 "L20": (  31.8,  29.9,  5.5),  # Posidonius
 "L21": ( -21.5,  33.2,  6.5),  # Fracastorius
 "L22": (  26.0, -51.0,  5.5),  # Aristarchus Plateau
 "L23": (  45.7,  -8.9,  2.4),  # Pico
 "L24": (   7.4,   7.8,  7.5),  # Hyginus Rille
 "L25": (  -1.9,  47.6,  2.4),  # Messier & Messier A
 "L26": (  56.0,   1.4, 20.0),  # Mare Frigoris (arcuate; representative stretch)
 "L27": (  29.7,  -4.0,  6.0),  # Archimedes
 "L28": (  -5.5,   4.8,  8.0),  # Hipparchus
 "L29": (   6.4,  14.0,  7.0),  # Ariadaeus Rille
 "L30": ( -51.9, -39.0,  7.0),  # Schiller
 "L31": (   5.6,  46.5,  4.0),  # Taruntius
 "L32": (   6.2,  21.4,  4.0),  # Arago Alpha & Beta (domes)
 "L33": (  27.3,  25.3,  8.0),  # Serpentine Ridge / Dorsa Smirnov
 "L34": (  45.0,  27.2,  7.0),  # Lacus Mortis
 "L35": (   4.3,   4.6,  5.0),  # Triesnecker Rilles
 "L36": (  -5.5, -68.3,  9.0),  # Grimaldi basin
 "L37": ( -66.5, -69.1,  9.0),  # Bailly
 "L38": (   1.7,  19.7,  4.0),  # Sabine & Ritter
 "L39": ( -44.3, -55.3, 10.0),  # Schickard
 "L40": ( -45.4,  39.3,  8.0),  # Janssen Rille
 "L41": (  21.8,  17.9, 15.0),  # Bessel ray (across Serenitatis)
 "L42": (  12.5, -54.0,  6.0),  # Marius Hills
 "L43": ( -49.6, -60.2,  5.0),  # Wargentin
 "L44": ( -21.5, -49.2,  6.0),  # Mersenius
 "L45": ( -42.0,  14.0,  7.0),  # Maurolycus
 "L46": ( -28.0,  -0.6,  6.0),  # Regiomontanus central peak
 "L47": ( -13.7,  -3.2,  7.0),  # Alphonsus dark spots
 "L48": (  10.5,  38.0,  4.0),  # Cauchy region
 "L49": (  36.3, -40.0,  3.5),  # Gruithuisen Delta & Gamma (domes)
 "L50": (   4.0,  15.1,  4.0),  # Cayley Plains
 "L51": ( -11.1,  -6.6,  4.0),  # Davy crater chain
 "L52": ( -16.7, -66.8,  4.0),  # Cruger (dark-floored crater, W limb)
 "L53": (   4.4,  23.7,  8.0),  # Lamont (ghost ring, S Tranquillitatis)
 "L54": ( -24.5, -29.0,  8.0),  # Hippalus Rilles
 "L55": ( -51.0,  19.1,  6.0),  # Baco
 "L56": ( -49.8,  84.5, 16.0),  # Australe basin (SE limb)
 "L57": (   7.7, -59.2,  4.0),  # Reiner Gamma (swirl)
 "L58": ( -42.5,  51.5,  9.0),  # Rheita Valley
 "L59": ( -56.0, -45.0, 10.0),  # Schiller-Zucchius basin
 "L60": ( -26.9, -24.2,  3.5),  # Kies Pi (dome)
 "L61": (  -3.2,  -5.2,  3.0),  # Mosting A
 "L62": (  40.8, -58.1,  4.0),  # Rumker (dome plateau)
 "L63": (  11.0,  12.0,  8.0),  # Imbrium sculpture
 "L64": ( -11.7,  15.7,  5.0),  # Descartes (Apollo 16)
 "L65": (   7.6, -27.9,  3.5),  # Hortensius domes
 "L66": (  25.0,   3.0,  4.0),  # Hadley Rille
 "L67": (  -3.6, -17.5,  7.0),  # Fra Mauro formation
 "L68": (  -3.0, -44.0,  6.0),  # Flamsteed P (ghost ring)
 "L69": (  19.6, -19.1,  5.0),  # Copernicus secondary craters (near Pytheas)
 "L70": (  57.0,  80.0, 12.0),  # Humboldtianum basin (NE limb)
 "L71": (  19.6,  11.6,  4.0),  # Sulpicius Gallus dark mantle
 "L72": (  46.7,  44.4,  5.0),  # Atlas dark-halo craters
 "L73": (  -2.0,  87.0, 14.0),  # Smythii basin (E limb)
 "L74": (   6.9, -18.3,  3.0),  # Copernicus H (dark-halo)
 "L75": (  -8.0,  -0.8,  5.0),  # Ptolemaeus B (saucer on the floor)
 "L76": (  65.3,   3.7,  8.0),  # W. Bond (far N)
 "L77": ( -15.7, -61.7, 10.0),  # Sirsalis Rille
 "L78": (  23.8, -20.6,  5.0),  # Lambert R (ghost)
 "L79": (  12.0,  -3.5,  6.0),  # Sinus Aestuum (dark mantle)
 "L80": ( -19.0, -95.0, 14.0),  # Orientale basin (W limb arcs)
 "L81": ( -30.1, -17.0,  3.5),  # Hesiodus A (concentric crater)
 "L82": (  27.7,  11.8,  3.0),  # Linne
 "L83": (  51.6,  -9.4,  5.0),  # Plato craterlets
 "L84": ( -29.8, -13.5,  5.0),  # Pitatus
 "L85": (  -8.9,  60.9,  8.0),  # Langrenus rays (E limb-ish)
 "L86": (  27.0, -43.0,  4.0),  # Prinz Rilles
 "L87": ( -27.0,  80.9,  9.0),  # Humboldt (SE limb FFC)
 "L88": (  88.6,  33.0,  5.0),  # Peary (north polar sliver)
 "L89": (  30.5,  10.1,  4.0),  # Valentine Dome
 "L90": (   1.3,  23.7,  3.0),  # Armstrong, Aldrin & Collins (Apollo 11 site)
 "L91": ( -25.9, -50.7,  4.0),  # De Gasparis Rilles
 "L92": (  -5.1,   0.7,  4.0),  # Gylden Valley
 "L93": (   2.8,  17.3,  4.0),  # Dionysius rays
 "L94": ( -79.3, -84.9,  7.0),  # Drygalski (SW polar-ish)
 "L95": (  23.0, -15.0, 38.0),  # Procellarum basin (whole western sweep)
 "L96": ( -85.0,  30.0,  8.0),  # Leibnitz Mountains (S limb peaks)
 "L97": ( -44.0, -73.0,  7.0),  # Inghirami Valley
 "L98": (  32.8, -22.0,  8.0),  # Imbrium lava flows
 "L99": (  18.6,   5.3,  3.0),  # Ina (D-caldera)
 "L100":(  18.5,  88.0,  6.0),  # Mare Marginis swirls (E limb)
}

def libration(lat, lon):
    return (max(-8.0, min(8.0, round(lon * 0.13))),
            max(-7.0, min(7.0, round(lat * 0.13))))

def project(lon, lat, lon0, lat0):
    dl = math.radians(lon - lon0); la = math.radians(lat); la0 = math.radians(lat0)
    x = R * math.cos(la) * math.sin(dl)
    y = R * (math.cos(la0) * math.sin(la) - math.sin(la0) * math.cos(la) * math.cos(dl))
    return x, y

def getmap(lon0, lat0, cx, cy, hw, hh, W, H, out):
    bbox = "%.1f,%.1f,%.1f,%.1f" % (cx - hw, cy - hh, cx + hw, cy + hh)
    q = urllib.parse.urlencode({
        "SERVICE": "WMS", "VERSION": "1.1.1", "REQUEST": "GetMap", "LAYERS": LAYER,
        "STYLES": "", "SRS": "AUTO:42003,9001,%s,%s" % (lon0, lat0),
        "BBOX": bbox, "WIDTH": W, "HEIGHT": H, "FORMAT": "image/jpeg", "BGCOLOR": "0x000000",
    })
    subprocess.run(["curl", "-sL", "--max-time", "150", "-A", UA, "-o", out, WMS + "?" + q], check=True)
    if os.path.getsize(out) < 2000:
        raise SystemExit("tiny response for %s: %s" % (out, open(out).read()[:200]))

def proc_locator(src, dst):
    subprocess.run([MAGICK, src, "-colorspace", "sRGB", "-gamma", "1.5",
                    "-sigmoidal-contrast", "1.4x38%", "-strip", "-quality", "88", dst], check=True)

def proc_closeup(src, dst):
    subprocess.run([MAGICK, src, "-colorspace", "sRGB", "-normalize",
                    "-level", "0%,100%,1.35", "-sigmoidal-contrast", "2x42%",
                    "-strip", "-quality", "88", dst], check=True)

def patch_cards(marks, panel):
    txt = open(CARDS).read()
    for cid, (dotx, doty) in marks.items():
        m = re.search(r'(\{ id:"' + cid + r'",.*?\n\s*tips:"[^"]*" \},)', txt, re.S)
        if not m:
            print("  ! card block not found:", cid); continue
        b = m.group(1); b2 = b
        if panel in ("both", "right"):
            b2 = re.sub(r'photoCredit:"[^"]*"', 'photoCredit:"' + CREDIT + '"', b2)
            b2 = re.sub(r'photoTag:"[^"]*"', 'photoTag:"NASA · LROC WAC"', b2)
        if panel in ("both", "left"):
            b2 = re.sub(r'locatorCredit:"[^"]*"', 'locatorCredit:"' + CREDIT + '"', b2)
            dot = 'outline:{ shape:"dot", cx:%s, cy:%s }' % (dotx, doty)
            if 'outline:{' in b2:
                b2 = re.sub(r'outline:\{[^}]*\}', dot, b2)
            else:
                b2 = re.sub(r'(\n(\s*)locatorCredit:"[^"]*",)', r'\1\n\2' + dot + ',', b2)
        txt = txt.replace(b, b2)
    open(CARDS, "w").write(txt)

def main():
    dry = "--dry-run" in sys.argv
    panel = sys.argv[sys.argv.index("--panel") + 1] if "--panel" in sys.argv else "both"
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else set(JOBS)
    marks = {}
    for cid in sorted(only, key=lambda s: int(s[1:])):
        if cid not in JOBS:
            print("  ? no JOBS entry:", cid); continue
        lat, lon, cf = JOBS[cid]
        lon0, lat0 = libration(lat, lon)
        fx, fy = project(lon, lat, lon0, lat0)
        # locator
        lcx, lcy = fx * LOC_PULL, fy * LOC_PULL
        lhh = LOC_FOV / 2 * U_PER_DEG
        lhw = lhh * 1100 / 1040
        dotx = round(50 + (fx - lcx) / lhw * 50, 1)
        doty = round(50 - (fy - lcy) / lhh * 50, 1)
        marks[cid] = (dotx, doty)
        # close-up
        chh = cf / 2 * U_PER_DEG
        chw = chh * 1400 / 1050
        print("%-4s lat%+6.1f lon%+6.1f  libr(%+d,%+d)  close %.1f deg  dot(%.0f,%.0f)  [%s]"
              % (cid, lat, lon, lon0, lat0, cf, dotx, doty, panel))
        if dry:
            continue
        if panel in ("both", "left"):
            raw = "%s/src-%s-scene-lunaserv.jpg" % (PLATES, cid.lower())
            getmap(lon0, lat0, lcx, lcy, lhw, lhh, 1100, 1040, raw)
            proc_locator(raw, "%s/plate-%s-scene.jpg" % (PLATES, cid))
        if panel in ("both", "right"):
            raw = "%s/src-%s-photo-lunaserv.jpg" % (PLATES, cid.lower())
            getmap(lon0, lat0, fx, fy, chw, chh, 1400, 1050, raw)
            proc_closeup(raw, "%s/plate-%s-photo.jpg" % (PLATES, cid))
    if not dry:
        patch_cards(marks, panel)
    print(("DRY " if dry else "") + "done: " + ", ".join(sorted(marks, key=lambda s: int(s[1:]))))

if __name__ == "__main__":
    main()
