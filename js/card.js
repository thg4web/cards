/* ============================================================
   Lunar Field Cards -- data-driven card renderer.

   Consumes the two globals loaded before this file:
     DATA   -- the spine  (data/lunar100.js)   array of 11-field rows
     CARDS  -- authored    (data/cards.js)      array of per-card objects

   Public API (global `LFC`):
     LFC.ids()               -> ["L1", ... "L100"] in CARDS order
     LFC.get(id)             -> { spine:[...], card:{...} } or null
     LFC.renderCard(id,side) -> HTML string for one .lfc-card
                                side = "front" | "back"
     LFC.zoneClass / catClass / CAT_LABEL / ZONE_LABEL  -- lookup tables

   Markup matches css/card.css (all block classes are `.lfc-*`;
   descendant helpers -- .lu .nm .plate .lbl .mk etc -- stay bare).
   ============================================================ */

(function (global) {
  "use strict";

  var S = { lNum: 0, id: 1, type: 2, name: 3, significance: 4, diamKm: 5,
            lat: 6, lon: 7, rukl: 8, stAtlas: 9, notes: 10 };

  var ZONE_LABEL = {
    ER: ["Eastern", "Rim"], EH: ["Eastern", "Heartland"],
    WH: ["Western", "Heartland"], WR: ["Western", "Rim"]
  };
  var ZONE_CLASS = { ER: "zone-er", EH: "zone-eh", WH: "zone-wh", WR: "zone-wr" };

  var CAT_LABEL = {
    maria: "Maria & Plains", crater: "Craters", valley: "Valleys & Rilles",
    special: "Special Phenomena", ridge: "Ridges & Scarps",
    mtn: "Mountains", volc: "Volcanoes & Domes"
  };
  var CAT_CLASS = {
    maria: "cat-maria", crater: "cat-crater", valley: "cat-valley",
    special: "cat-special", ridge: "cat-ridge", mtn: "cat-mtn", volc: "cat-volc"
  };
  // 24x24 viewBox glyphs; stroke colour comes from card.css (.lfc-cat .badge svg)
  var CAT_ICON = {
    maria:   '<path d="M3 14c3-2 5-2 8 0s5 2 8 0"/><path d="M3 9c3-2 5-2 8 0s5 2 8 0"/>',
    crater:  '<circle cx="10" cy="11" r="6"/><circle cx="17.5" cy="16" r="3.5"/><circle cx="16" cy="6.5" r="2.5"/>',
    valley:  '<path d="M6 3l3 9-2 9"/><path d="M15 3l3 9-2 9"/>',
    special: '<circle cx="12" cy="12" r="3.6"/><path d="M12 2.5v3.4M12 18.1v3.4M2.5 12h3.4M18.1 12h3.4M5.2 5.2l2.4 2.4M16.4 16.4l2.4 2.4M18.8 5.2l-2.4 2.4M7.6 16.4l-2.4 2.4"/>',
    ridge:   '<path d="M2 18l6-9 4 5 3-3 7 7"/>',
    mtn:     '<path d="M2 20l7-14 4.5 8 3-4.5 5.5 10.5z"/>',
    volc:    '<path d="M8 20l3-7h2l3 7z"/><path d="M11 5.5c0-2 2-2 2-3.5M13.2 6c1-1 3-1 3-2.6"/>'
  };

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }
  function num(v) {                       // "20.1W" -> -20.1 ; "9.7N" -> 9.7
    if (!v) return null;
    var m = /^(-?[\d.]+)\s*([NSEW])?$/.exec(String(v).trim());
    if (!m) return null;
    var n = parseFloat(m[1]);
    if (m[2] === "S" || m[2] === "W") n = -n;
    return n;
  }

  var _byId = null;
  function spine(id) {
    if (!_byId) { _byId = {}; for (var i = 0; i < DATA.length; i++) _byId[DATA[i][S.id]] = DATA[i]; }
    return _byId[id] || null;
  }
  function ids() { return CARDS.map(function (c) { return c.id; }); }
  function get(id) {
    var sp = spine(id), cd = null;
    for (var i = 0; i < CARDS.length; i++) if (CARDS[i].id === id) { cd = CARDS[i]; break; }
    return (sp && cd) ? { spine: sp, card: cd } : null;
  }

  function coordText(sp) {
    var la = sp[S.lat], lo = sp[S.lon];
    if (!la && !lo) return "";
    var f = function (v) { return v ? v.replace(/([NSEW])$/, "°$1") : "—"; };
    return "Coordinates: " + f(la) + " | " + f(lo);
  }
  function atlasText(sp) {
    var out = [];
    if (sp[S.rukl]) out.push("Rükl " + sp[S.rukl]);
    if (sp[S.stAtlas]) {
      var nums = sp[S.stAtlas].split(",").map(function (x) { return x.trim(); })
                 .filter(function (x) { return /^\d+$/.test(x); });
      if (nums.length) out.push("21stC " + nums.join(","));
    }
    return out.join(" · ");
  }
  function sizeRows(cd, sp) {
    if (cd.size && cd.size.length) return cd.size;
    var km = sp[S.diamKm];
    return [{ label: "Diameter", value: km ? km + " km" : "—" }];
  }
  function diffPct(d) { return Math.max(2, Math.min(98, (((d || 1) - 0.5) / 5) * 100)); }

  function shell(inner, zone, cat) {
    var z = ZONE_CLASS[zone] || "";
    var c = CAT_CLASS[cat] || "cat-crater";
    return '<div class="lfc-card ' + z + " " + c + '">' +
      '<div class="lfc-bleed top"><i class="w"></i><i class="z"></i></div>' +
      '<div class="lfc-bleed bot"><i class="w"></i><i class="z"></i></div>' +
      '<div class="lfc-frame"><i class="tl"></i><i class="tr"></i><i class="bl"></i><i class="br"></i></div>' +
      '<div class="lfc-face">' + inner + '</div></div>';
  }
  function header(sp, cd, tail) {
    var alt = cd.alt ? '<span class="alt">| ' + esc(cd.alt) + '</span>' : '';
    return '<div class="lfc-hd">' +
      '<span class="lu">L ' + sp[S.lNum] + '</span>' +
      '<span class="gem"></span>' +
      '<span class="nm">' + esc(sp[S.name]) + alt + '</span>' +
      '<span class="rule"></span>' + tail + '</div>';
  }
  function zoneTail(zone) {
    var L = ZONE_LABEL[zone];
    if (!L) return '';
    return '<span class="lfc-zone"><span class="phase"></span>' +
      '<span class="zt">' + L[0] + '<br>' + L[1] + '</span></span>';
  }
  function catTail(cat) {
    return '<span class="lfc-cat"><span class="badge" aria-hidden="true">' +
      '<svg viewBox="0 0 24 24">' + (CAT_ICON[cat] || CAT_ICON.crater) + '</svg></span>' +
      '<span class="ct">' + esc(CAT_LABEL[cat] || cat) + '</span></span>';
  }

  function outlineSVG(o) {
    if (!o) return '';
    var st = ' fill="none" stroke="#e36a1e" stroke-width="1.1" style="filter:drop-shadow(0 0 2px rgba(227,106,30,.9))"';
    var body;
    if (o.shape === "ellipse") {
      body = '<ellipse cx="' + o.cx + '" cy="' + o.cy + '" rx="' + o.rx + '" ry="' + o.ry + '"' +
             (o.rot ? ' transform="rotate(' + o.rot + ' ' + o.cx + ' ' + o.cy + ')"' : '') + st + '/>';
    } else if (o.shape === "path") {
      body = '<path d="' + esc(o.d) + '"' + st + '/>';
    } else {
      body = '<circle cx="' + o.cx + '" cy="' + o.cy + '" r="' + (o.r || 2.5) + '"' + st + '/>';
    }
    return '<svg class="outline" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">' + body + '</svg>';
  }
  function labels(list) {
    return (list || []).map(function (n) {
      return '<span class="lbl' + (n.o ? ' o' : '') + '" style="left:' + n.x + '%;top:' + n.y + '%">' + esc(n.label) + '</span>';
    }).join('');
  }
  function pins(list) {
    return (list || []).map(function (p) {
      return '<span class="pin" style="left:' + p.x + '%;top:' + p.y + '%"></span>' +
        '<span class="lbl" style="left:' + (p.x + 3) + '%;top:' + p.y + '%">' + esc(p.label) + '</span>';
    }).join('');
  }

  function renderFront(id) {
    var g = get(id); if (!g) return '';
    var sp = g.spine, cd = g.card;
    var la = num(sp[S.lat]) || 0, lo = num(sp[S.lon]) || 0;
    var gx = 50 + (lo / 90) * 45, gy = 50 - (la / 90) * 45;

    var locImg = cd.locator
      ? '<img class="plate" src="design/plates/' + esc(cd.locator) + '" alt="Locator map for ' + esc(sp[S.name]) + '">'
      : '';
    var mapCredit = cd.locatorCredit ? '<span class="lfc-map-credit">' + esc(cd.locatorCredit) + '</span>' : '';
    var coords = coordText(sp);
    var coordEl = coords ? '<span class="lfc-coords">' + esc(coords) + '</span>' : '';
    var globeEl = (sp[S.lat] || sp[S.lon])
      ? '<div class="lfc-globe"><span class="mk" style="left:' + gx.toFixed(1) + '%;top:' + gy.toFixed(1) + '%"></span></div>'
      : '';

    var phImg = cd.photo
      ? '<img class="plate" src="design/plates/' + esc(cd.photo) + '" alt="' + esc(sp[S.name]) + ' close-up">'
      : '';
    var phTag = cd.photoTag ? '<span class="lfc-ph-tag">' + esc(cd.photoTag) + '</span>' : '';
    var credit = cd.photoCredit ? '<p class="lfc-credit">' + esc(cd.photoCredit) + '</p>' : '';

    var inner = header(sp, cd, zoneTail(cd.zone)) +
      '<div class="lfc-front-body">' +
        '<div class="lfc-pane lfc-locator">' +
          locImg + outlineSVG(cd.outline) + labels(cd.neighbours) + pins(cd.pins) +
          mapCredit + coordEl + globeEl +
        '</div>' +
        '<div class="lfc-pane">' + phImg + phTag + credit + '</div>' +
      '</div>';
    return shell(inner, cd.zone, cd.cat);
  }

  function renderBack(id) {
    var g = get(id); if (!g) return '';
    var sp = g.spine, cd = g.card;
    var dash = "—";

    var kv = '';
    kv += '<div class="lfc-kv"><b>Epoch</b><span>' + esc(cd.epoch || dash) + '</span></div>';
    sizeRows(cd, sp).forEach(function (r) {
      kv += '<div class="lfc-kv"><b>' + esc(r.label) + '</b><span>' + esc(r.value) + '</span></div>';
    });
    if (cd.depth) kv += '<div class="lfc-kv"><b>Depth</b><span>' + esc(cd.depth) + '</span></div>';
    var atlas = atlasText(sp);
    if (atlas) kv += '<div class="lfc-kv"><b>Atlas</b><span>' + esc(atlas) + '</span></div>';

    var best = '';
    if (cd.bestDays && cd.bestDays.length) {
      best = '<p class="lfc-mini-h">Best days to observe</p><div class="lfc-chips">' +
        cd.bestDays.map(function (w) {
          return '<b>' + w[0] + "–" + w[1] + '</b>';
        }).join('') + '</div>';
    }
    var facts = (cd.facts && cd.facts.length ? cd.facts : [dash]).map(function (f) {
      return '<li>' + esc(f) + '</li>';
    }).join('');

    var inner = header(sp, cd, catTail(cd.cat)) +
      '<div class="lfc-back-body">' +
        '<div class="lfc-col">' +
          kv +
          '<p class="lfc-mini-h">Difficulty level</p>' +
          '<div class="lfc-diff"><span class="mk" style="left:' + diffPct(cd.diff || cd.dSeed).toFixed(1) + '%"></span></div>' +
          '<div class="lfc-diff-scale"><span>Easy</span><span>Moderate</span><span>Hard</span></div>' +
          best +
          '<span class="lfc-pill">Observation tips</span>' +
          '<p class="lfc-tips">' + esc(cd.tips || dash) + '</p>' +
        '</div>' +
        '<div class="lfc-col">' +
          '<div class="lfc-block"><h4>Description</h4><p>' + esc(cd.description || dash) + '</p></div>' +
          '<div class="lfc-block"><h4>Name origin</h4><p>' + esc(cd.nameOrigin || dash) + '</p></div>' +
          '<div class="lfc-block"><h4>Interesting facts</h4><ul class="lfc-facts">' + facts + '</ul></div>' +
        '</div>' +
      '</div>';
    return shell(inner, cd.zone, cd.cat);
  }

  function renderCard(id, side) {
    return side === "back" ? renderBack(id) : renderFront(id);
  }

  global.LFC = {
    ids: ids, get: get, renderCard: renderCard,
    renderFront: renderFront, renderBack: renderBack,
    ZONE_LABEL: ZONE_LABEL, ZONE_CLASS: ZONE_CLASS,
    CAT_LABEL: CAT_LABEL, CAT_CLASS: CAT_CLASS
  };
})(typeof window !== "undefined" ? window : this);

if (typeof module !== "undefined") module.exports = (typeof window !== "undefined" ? window : this).LFC;
