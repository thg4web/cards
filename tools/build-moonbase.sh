#!/usr/bin/env bash
# build-moonbase.sh -- assemble a near-side equirectangular Moon base map from
# Virtual Moon Atlas level-2 texture tiles (10 cols x 5 rows, 1000px active +
# 12px border per 1024 tile => 10000 x 5000 full sphere, lon -180..+180 W->E,
# lat +90..-90 N->S). Output is the master every card's locator panel is cropped
# from. Git-ignored (src- prefix); only the per-card crops are tracked.
#
# Usage: tools/build-moonbase.sh [change|wac]
set -euo pipefail

SET="${1:-wac}"
case "$SET" in
  wac)    SUB="WAC_LOWSUN" ;;
  change) SUB="Change" ;;
  *) echo "usage: $0 [change|wac]" >&2; exit 2 ;;
esac

VMA="/Users/wahender/My_Library/Tech/git_repos/virtmoonatlas/data-extracted/usr/share/virtualmoon/Textures/$SUB/L2"
MAGICK="/opt/homebrew/bin/magick"
OUTDIR="$(cd "$(dirname "$0")/.." && pwd)/design/plates"
OUT="$OUTDIR/src-moonbase-${SET}.jpg"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

[ -d "$VMA" ] || { echo "missing tiles: $VMA" >&2; exit 1; }

echo "assembling $SUB L2 -> $OUT"
for r in 0 1 2 3 4; do
  cols=()
  for c in 0 1 2 3 4 5 6 7 8 9; do
    n=$((r*10+c))
    "$MAGICK" "$VMA/$n.jpg" -crop 1000x1000+12+12 +repage "$TMP/t_${r}_${c}.mpc"
    cols+=("$TMP/t_${r}_${c}.mpc")
  done
  "$MAGICK" "${cols[@]}" +append "$TMP/row_${r}.mpc"
done
"$MAGICK" "$TMP/row_0.mpc" "$TMP/row_1.mpc" "$TMP/row_2.mpc" "$TMP/row_3.mpc" "$TMP/row_4.mpc" \
  -append -colorspace sRGB -strip -quality 90 "$OUT"

"$MAGICK" identify "$OUT"
