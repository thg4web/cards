#!/usr/bin/env python3
"""build-locator-plates.py -- generate the LEFT (locator) panel for a range of
Lunar Field Cards by cropping the Virtual Moon Atlas near-side base map.

For each target card:
  * centre a crop on the feature's spine lat/lon
  * field of view scales with feature size
  * longitude is widened by 1/cos(lat) then squeezed back on export, so craters
    read round instead of smearing sideways near the poles
  * write design/plates/plate-L<n>-scene.jpg
  * rewrite the card's stub line in data/cards.js with locator / locatorCredit /
    outline (the orange ring the renderer draws)

Usage:  tools/build-locator-plates.py 16 100
        tools/build-locator-plates.py 16 100 --dry-run
"""
import math, os, re, subprocess, sys

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE   = os.path.join(ROOT, "design/plates/src-moonbase-wac.jpg")
PLATES = os.path.join(ROOT, "design/plates")
SPINE  = os.path.join(ROOT, "data/lunar100.js")
CARDS  = os.path.join(ROOT, "data/cards.js")
MAGICK = "/opt/homebrew/bin/magick"

W, H       = 10000, 5000          # base map, equirectangular, lon -180..+180 W->E
PXDEG      = W / 360.0
KM_PER_DEG = 10917.0 / 360.0      # ~30.3 km per degree of arc on the Moon
OUT_W, OUT_H = 1100, 1038         # ~1.06:1, matches the locator pane
ASPECT     = OUT_W / OUT_H
CREDIT     = "LROC WAC low-sun mosaic (Virtual Moon Atlas). NASA / ASU."

def parse_spine():
    rows = {}
    txt = open(SPINE).read()
    for m in re.finditer(r'\[\s*\d+\s*,\s*"(L\d+)"\s*,((?:[^\[\]]|"[^"]*")*)\]', txt):
        cid, rest = m.group(1), m.group(2)
        parts = re.findall(r'"([^"]*)"', rest)
        # rest fields after id: type, name, significance, diam, lat, lon, rukl, atlas, notes
        if len(parts) < 6:
            continue
        _type, name, _sig, diam, lat, lon = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5]
        rows[cid] = dict(name=name, diam=diam.strip(), lat=lat.strip(), lon=lon.strip())
    return rows

def signed(v):
    if not v:
        return None
    s = v[-1].upper(); n = float(v[:-1])
    if s in ("S", "W"):
        n = -n
    return n

def plan(row):
    lat = signed(row["lat"]); lon = signed(row["lon"])
    if lat is None or lon is None:
        return None
    try:
        diam_km = float(row["diam"])
    except ValueError:
        diam_km = 40.0
    feat_deg = diam_km / KM_PER_DEG

    fov_lat = max(36.0, min(64.0, feat_deg * 3.0 + 30.0))
    coslat  = max(0.30, math.cos(math.radians(lat)))
    fov_lon = (fov_lat / ASPECT) / coslat

    cx = (lon + 180.0) * PXDEG
    cy = (90.0 - lat) * (H / 180.0)
    cw = fov_lon * PXDEG
    ch = fov_lat * (H / 180.0)
    x0 = cx - cw / 2.0
    y0 = cy - ch / 2.0
    # keep the window on the map; if we shove it, the ring follows the feature
    x0 = max(0.0, min(x0, W - cw))
    y0 = max(0.0, min(y0, H - ch))
    cw = min(cw, W); ch = min(ch, H)

    ring = max(4.0, min(16.0, (feat_deg / fov_lat) * 50.0))
    ring_cx = round((cx - x0) / cw * 100.0, 1)
    ring_cy = round((cy - y0) / ch * 100.0, 1)
    off = abs(ring_cx - 50) > 6 or abs(ring_cy - 50) > 6

    return dict(x0=int(round(x0)), y0=int(round(y0)), cw=int(round(cw)),
                ch=int(round(ch)), ring=round(ring, 1),
                rcx=ring_cx, rcy=ring_cy, lat=lat, lon=lon,
                edge=off or abs(lat) > 60 or abs(lon) > 75)

def make_plate(cid, p, dry):
    out = os.path.join(PLATES, f"plate-{cid}-scene.jpg")
    cmd = [MAGICK, BASE, "-crop", f"{p['cw']}x{p['ch']}+{p['x0']}+{p['y0']}",
           "+repage", "-resize", f"{OUT_W}x{OUT_H}!", "-colorspace", "sRGB",
           "-brightness-contrast", "3x5", "-strip", "-quality", "88", out]
    if dry:
        return
    subprocess.run(cmd, check=True)

STUB_RE = re.compile(r'^(?P<pre>\s*\{ id:"(?P<id>L\d+)",.*?status:"stub")(?P<gap> )\}(?P<post>,.*)?$')

def rewrite_cards(plans, dry):
    lines = open(CARDS).read().split("\n")
    done = []
    for i, ln in enumerate(lines):
        m = STUB_RE.match(ln)
        if not m:
            continue
        cid = m.group("id")
        if cid not in plans:
            continue
        p = plans[cid]
        indent = re.match(r'\s*', ln).group(0)
        post = m.group("post") or ","
        block = (
            f'{m.group("pre")},\n'
            f'{indent}  locator:"plate-{cid}-scene.jpg",\n'
            f'{indent}  locatorCredit:"{CREDIT}",\n'
            f'{indent}  outline:{{ shape:"ellipse", cx:{p["rcx"]}, cy:{p["rcy"]}, '
            f'rx:{p["ring"]}, ry:{p["ring"]} }} }}{post}'
        )
        lines[i] = block
        done.append(cid)
    if not dry:
        open(CARDS, "w").write("\n".join(lines))
    return done

def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    dry = "--dry-run" in sys.argv
    spine = parse_spine()
    plans, skipped, edge = {}, [], []
    for n in range(lo, hi + 1):
        cid = f"L{n}"
        row = spine.get(cid)
        if not row:
            skipped.append((cid, "no spine row")); continue
        p = plan(row)
        if p is None:
            skipped.append((cid, "no lat/lon")); continue
        plans[cid] = p
        make_plate(cid, p, dry)
        if p["edge"]:
            edge.append(cid)
    done = rewrite_cards(plans, dry)
    print(f"{'DRY ' if dry else ''}plates generated : {len(plans)}  ({lo}..{hi})")
    print(f"cards.js stubs rewritten : {len(done)}")
    miss = sorted(set(plans) - set(done), key=lambda s: int(s[1:]))
    if miss:
        print(f"  plate made but stub NOT found (already expanded?): {', '.join(miss)}")
    if skipped:
        print("skipped:")
        for cid, why in skipped:
            print(f"  {cid}: {why}")
    if edge:
        print(f"edge/polar (locator will be rougher on the equirect base): {', '.join(edge)}")

if __name__ == "__main__":
    main()
