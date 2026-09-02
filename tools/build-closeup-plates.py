#!/usr/bin/env python3
"""build-closeup-plates.py -- generate the RIGHT (overhead close-up) panel for a
range of Lunar Field Cards from the LRO LROC WAC global mosaic (100 m/px),
served as a WMTS pyramid by NASA Solar System Treks.

  layer : LRO_WAC_Mosaic_Global_303ppd_v02   (equirectangular, z0..z8)
  tile  : .../default028mm/{z}/{y}/{x}.jpg    256 px, origin lon -180 / lat +90

For each card: pick a zoom so the feature's field of view is ~1500 px, fetch and
stitch the covering tiles, crop exactly (longitude widened by 1/cos(lat) so the
feature reads round in the 4:3 panel), resize to 1400x1050, write
design/plates/plate-L<n>-photo.jpg, and add photo / photoTag / photoCredit to
data/cards.js.

Tiles are cached under design/plates/.trekcache/ (git-ignored). Re-runs skip
plates that already exist unless --force.

Usage:  tools/build-closeup-plates.py 16 100 [--force] [--dry-run] [--only 16,42,88]
"""
import math, os, re, sys, time, urllib.request

ROOT   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATES = os.path.join(ROOT, "design/plates")
CACHE  = os.path.join(PLATES, ".trekcache")
SPINE  = os.path.join(ROOT, "data/lunar100.js")
CARDS  = os.path.join(ROOT, "data/cards.js")
MAGICK = "/opt/homebrew/bin/magick"

TILE   = 256
ZMAX   = 8
PPD_MAX = TILE * (2 ** ZMAX) / 360.0        # 364.089 px/deg at z8
KM_PER_DEG = 10917.0 / 360.0
BASEURL = ("https://trek.nasa.gov/tiles/Moon/EQ/LRO_WAC_Mosaic_Global_303ppd_v02"
           "/1.0.0/default/default028mm")
UA = "LunarFieldCards/0.1 (THG Media; hikerdad@gmail.com)"
OUT_W, OUT_H = 1400, 1050
TARGET_PX = 1500
CREDIT = "LROC WAC global mosaic (100 m/px). NASA / GSFC / Arizona State University."

def parse_spine():
    rows = {}
    txt = open(SPINE).read()
    for m in re.finditer(r'\[\s*\d+\s*,\s*"(L\d+)"\s*,((?:[^\[\]]|"[^"]*")*)\]', txt):
        p = re.findall(r'"([^"]*)"', m.group(2))
        if len(p) < 6:
            continue
        rows[m.group(1)] = dict(name=p[1], diam=p[3].strip(), lat=p[4].strip(), lon=p[5].strip())
    return rows

def signed(v):
    if not v:
        return None
    s = v[-1].upper()
    n = float(v[:-1])
    return -n if s in ("S", "W") else n

def fetch_tile(z, x, y):
    d = os.path.join(CACHE, str(z))
    os.makedirs(d, exist_ok=True)
    fn = os.path.join(d, f"{x}_{y}.jpg")
    if os.path.exists(fn) and os.path.getsize(fn) > 0:
        return fn
    url = f"{BASEURL}/{z}/{y}/{x}.jpg"
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
            if len(data) < 100:
                raise IOError("short tile")
            open(fn, "wb").write(data)
            time.sleep(0.06)
            return fn
        except Exception as e:
            if attempt == 3:
                print(f"    tile {z}/{y}/{x} failed: {e}")
                return None
            time.sleep(0.5 * (attempt + 1))
    return None

def build_plate(cid, row, force, dry):
    out = os.path.join(PLATES, f"plate-{cid}-photo.jpg")
    if os.path.exists(out) and not force:
        return "exists"
    lat = signed(row["lat"]); lon = signed(row["lon"])
    if lat is None or lon is None:
        return "no lat/lon"
    try:
        diam_km = float(row["diam"])
    except ValueError:
        diam_km = 40.0
    feat_deg = max(0.3, diam_km / KM_PER_DEG)

    fov = min(9.0, max(1.3, feat_deg / 0.62))          # latitude span, deg
    coslat = max(0.09, math.cos(math.radians(lat)))
    fov_lon = min(60.0, fov * (OUT_W / OUT_H) / coslat)  # longitude span, deg

    # zoom so the wider axis is ~TARGET_PX
    want_ppd = TARGET_PX / max(fov, fov_lon * OUT_H / OUT_W)
    z = ZMAX - max(0, min(5, round(math.log2(max(1e-6, PPD_MAX / want_ppd)))))
    ppd = TILE * (2 ** z) / 360.0
    world = int(round(ppd * 360))

    cxp = (lon + 180.0) * ppd
    cyp = (90.0 - lat) * ppd
    cw = fov_lon * ppd
    ch = fov * ppd
    x0 = cxp - cw / 2.0
    y0 = cyp - ch / 2.0
    y0 = max(0.0, min(y0, world / 2.0 - ch))            # lat clamp (no wrap)

    tx0 = int(math.floor(x0 / TILE)); tx1 = int(math.floor((x0 + cw) / TILE))
    ty0 = int(math.floor(y0 / TILE)); ty1 = int(math.floor((y0 + ch) / TILE))
    ncols = tx1 - tx0 + 1; nrows = ty1 - ty0 + 1
    ntiles = ncols * nrows
    edge = abs(lat) > 78 or abs(lon) > 80
    print(f"  {cid} {row['name'][:26]:26s} lat{lat:+6.1f} lon{lon:+6.1f} "
          f"fov{fov:4.1f} z{z} {ncols}x{nrows}={ntiles}t" + ("  EDGE" if edge else ""))
    if dry:
        return "dry"

    tiles = []
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            txm = tx % (world // TILE)                  # longitude wrap
            f = fetch_tile(z, txm, ty)
            tiles.append((tx, ty, f))
    if any(f is None for _, _, f in tiles):
        return "tile fetch failed"

    rows_img = []
    for ty in range(ty0, ty1 + 1):
        rowf = [f for (tx, tyy, f) in tiles if tyy == ty]
        rp = os.path.join(CACHE, f"_row_{cid}_{ty}.mpc")
        os.system(f'{MAGICK} ' + " ".join(f'"{f}"' for f in rowf) + f' +append "{rp}"')
        rows_img.append(rp)
    mosaic = os.path.join(CACHE, f"_mos_{cid}.mpc")
    os.system(f'{MAGICK} ' + " ".join(f'"{r}"' for r in rows_img) + f' -append "{mosaic}"')

    ox = x0 - tx0 * TILE
    oy = y0 - ty0 * TILE
    cmd = (f'{MAGICK} "{mosaic}" -crop {int(round(cw))}x{int(round(ch))}+'
           f'{int(round(ox))}+{int(round(oy))} +repage -resize {OUT_W}x{OUT_H}! '
           f'-colorspace sRGB -normalize -sigmoidal-contrast 3.5x46% '
           f'-strip -quality 88 "{out}"')
    os.system(cmd)
    for f in rows_img + [mosaic]:
        try: os.remove(f)
        except OSError: pass
    return "edge" if edge else "ok"

CARD_RE = re.compile(r'(\n\s*\{ id:"(L\d+)",[^\n]*\n(?:\s*[^\n]*\n)*?)(\s*)(locator:"plate-)')

def wire_cards(ids, dry):
    txt = open(CARDS).read()
    done = []
    def repl(m):
        cid = m.group(2)
        if cid not in ids:
            return m.group(0)
        if f'photo:"plate-{cid}-photo.jpg"' in m.group(1):
            return m.group(0)
        ind = m.group(3)
        add = (f'{ind}photo:"plate-{cid}-photo.jpg",\n'
               f'{ind}photoTag:"NASA · LROC WAC",\n'
               f'{ind}photoCredit:"{CREDIT}",\n')
        done.append(cid)
        return m.group(1) + add + m.group(3) + m.group(4)
    txt2 = CARD_RE.sub(repl, txt)
    if not dry:
        open(CARDS, "w").write(txt2)
    return done

def main():
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    force = "--force" in sys.argv
    dry = "--dry-run" in sys.argv
    only = None
    if "--only" in sys.argv:
        only = set("L" + s for s in sys.argv[sys.argv.index("--only") + 1].split(","))
    spine = parse_spine()
    tally = {}
    targets = []
    for n in range(lo, hi + 1):
        cid = f"L{n}"
        if only and cid not in only:
            continue
        if cid not in spine:
            tally.setdefault("no spine row", []).append(cid); continue
        r = build_plate(cid, spine[cid], force, dry)
        tally.setdefault(r, []).append(cid)
        if r in ("ok", "edge", "exists", "dry"):
            targets.append(cid)
    wired = wire_cards(set(targets), dry) if not dry else []
    print("\n--- summary ---")
    for k, v in tally.items():
        print(f"{k:20s}: {len(v)}  {' '.join(v) if len(v) <= 20 else ''}")
    print(f"cards.js photo wired : {len(wired)}")

if __name__ == "__main__":
    main()
