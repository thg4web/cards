/* ============================================================
   Lunar Field Cards -- card search (Bug 1, 2026-11-20).

   Load after js/card.js. Builds a folded index (lower case, accents
   dropped, curly quotes straightened) over each card's spine and
   authored text, then ranks the cards for a query.

   Searched, highest weight first:
     name, alt/Latin name, Wood's significance line, zone, category,
     epoch, then the card back: description, name origin, facts, tips.

   Rules:
     - apostrophes drop out, so "schroters valley" finds Schröter's Valley
     - every word in the query must start a word somewhere on the card
       ("ray" finds "rays", not "gray"); accents never matter
       ("schroter" finds "Schröteri")
     - a query that is just a number, or L + number ("28", "L28"),
       lists that card first, then the L numbers that start with it
     - a query shorter than two letters returns null (keep typing)

   Public API (global `LFCSearch`):
     LFCSearch.query(text) -> null | [ result, ... ]  best first
       result = { id, i, lNum, name, alt, zone, cat, score,
                  nameRanges, altRanges,        // [start,end) to highlight
                  hit }                         // null when the name matched,
                                                // else { label, text, ranges }
     LFCSearch.fold(text)  -> { s, t, map }    // original, folded, t->s index
   ============================================================ */

(function (global) {
  "use strict";

  var MARKS = /[̀-ͯ]/g;
  var WORDCH = /[\p{L}\p{N}]/u;
  var SPLIT = /[^\p{L}\p{N}]+/u;
  var SNIP = 110;                        // snippet length, in characters
  var LEAD = 30;                         // context kept before the first match

  // fold one string, keeping a map from each folded char back to the original
  function fold(s) {
    s = String(s == null ? "" : s);
    var t = "", map = [];
    for (var k = 0; k < s.length; k++) {
      var f = s[k].normalize("NFD").replace(MARKS, "").toLowerCase()
        .replace(/['‘’ʼ]/g, "")
        .replace(/[“”]/g, '"')
        .replace(/[–—]/g, "-");
      for (var j = 0; j < f.length; j++) { t += f[j]; map.push(k); }
    }
    return { s: s, t: t, map: map };
  }

  // positions where `tok` starts a word in folded text `t`
  function wordStarts(t, tok, firstOnly) {
    var out = [], p = t.indexOf(tok);
    while (p >= 0) {
      if (p === 0 || !WORDCH.test(t[p - 1])) {
        out.push(p);
        if (firstOnly) break;
      }
      p = t.indexOf(tok, p + 1);
    }
    return out;
  }
  function has(en, tok) { return wordStarts(en.f.t, tok, true).length > 0; }

  // every match of every token, as merged [start,end) ranges in the ORIGINAL text
  function ranges(f, toks) {
    var rs = [];
    toks.forEach(function (tok) {
      wordStarts(f.t, tok, false).forEach(function (p) {
        rs.push([f.map[p], f.map[p + tok.length - 1] + 1]);
      });
    });
    rs.sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; });
    var out = [];
    rs.forEach(function (r) {
      var last = out[out.length - 1];
      if (last && r[0] <= last[1]) last[1] = Math.max(last[1], r[1]);
      else out.push(r.slice());
    });
    return out;
  }

  // a short window of `en` around its first match, with highlight ranges
  function snippet(en, toks) {
    var s = en.f.s, rs = ranges(en.f, toks);
    if (s.length <= SNIP || !rs.length) return { label: en.label, text: s, ranges: rs };
    var first = rs[0][0];
    var a = Math.max(0, first - LEAD), b = Math.min(s.length, a + SNIP);
    if (b === s.length) a = Math.max(0, b - SNIP);
    if (a > 0) {                          // start on a word
      var sp = s.indexOf(" ", a);
      if (sp >= 0 && sp < first) a = sp + 1;
    }
    if (b < s.length) {                   // end on a word
      var sp2 = s.lastIndexOf(" ", b);
      if (sp2 > first) b = sp2;
    }
    var pre = a > 0 ? "…" : "", off = pre.length - a;
    return {
      label: en.label,
      text: pre + s.slice(a, b) + (b < s.length ? "…" : ""),
      ranges: rs.filter(function (r) { return r[0] >= a && r[1] <= b; })
                .map(function (r) { return [r[0] + off, r[1] + off]; })
    };
  }

  var INDEX = null;
  function build() {
    var LFC = global.LFC;
    INDEX = LFC.ids().map(function (id, i) {
      var g = LFC.get(id), sp = g.spine, cd = g.card, e = [];
      function add(key, label, w, text) {
        if (text && text !== "—") e.push({ key: key, label: label, w: w, f: fold(text) });
      }
      var zl = LFC.ZONE_LABEL[cd.zone];
      add("name",   "Name",        100, sp[3]);
      add("alt",    "Name",         90, cd.alt);
      add("sig",    "Lunar 100",    50, sp[4]);
      add("zone",   "Zone",         35, zl ? zl.join(" ") : "");
      add("cat",    "Category",     35, LFC.CAT_LABEL[cd.cat]);
      add("epoch",  "Epoch",        30, cd.epoch);
      add("desc",   "Description",  12, cd.description);
      add("origin", "Name origin",  12, cd.nameOrigin);
      (cd.facts || []).forEach(function (f) { add("fact", "Fact", 10, f); });
      add("tips",   "Tips",         10, cd.tips);
      add("notes",  "Notes",        10, sp[10]);
      return { id: id, i: i, lNum: sp[0], name: sp[3], alt: cd.alt || "",
               zone: cd.zone, cat: cd.cat, e: e,
               nameEn: e[0], altEn: e[1] && e[1].key === "alt" ? e[1] : null };
    });
  }

  function result(c, score, toks, hit) {
    return {
      id: c.id, i: c.i, lNum: c.lNum, name: c.name, alt: c.alt,
      zone: c.zone, cat: c.cat, score: score, hit: hit,
      nameRanges: toks.length ? ranges(c.nameEn.f, toks) : [],
      altRanges: toks.length && c.altEn ? ranges(c.altEn.f, toks) : []
    };
  }

  function query(text) {
    if (!INDEX) build();
    var q = fold(text).t.trim();

    // "28" / "L28" / "l 28" -> by L number
    var m = /^l?\s*(\d{1,3})$/.exec(q);
    if (m) {
      var n = m[1];
      return INDEX
        .filter(function (c) { return String(c.lNum).indexOf(n) === 0; })
        .sort(function (a, b) {
          return (String(b.lNum) === n) - (String(a.lNum) === n) || a.lNum - b.lNum;
        })
        .map(function (c) { return result(c, 0, [], null); });
    }

    var toks = q.split(SPLIT).filter(Boolean);
    var phrase = toks.join(" ");
    if (!toks.length || toks.join("").length < 2) return null;

    var out = [];
    INDEX.forEach(function (c) {
      var score = 0, inName = 0, k, j;
      for (k = 0; k < toks.length; k++) {
        var best = 0, named = false;
        for (j = 0; j < c.e.length; j++) {
          var en = c.e[j], p = wordStarts(en.f.t, toks[k], true);
          if (!p.length) continue;
          var isName = en.key === "name" || en.key === "alt";
          var w = en.w + (isName && p[0] === 0 ? 40 : 0);
          if (isName) named = true;
          if (w > best) best = w;
        }
        if (!best) return;                // every word has to land somewhere
        score += best;
        if (named) inName++;
      }
      if (toks.length > 1) {              // the words together, in order
        var inNm = has(c.nameEn, phrase) || (c.altEn && has(c.altEn, phrase));
        if (inNm) score += 60;
        else if (c.e.some(function (en) { return has(en, phrase); })) score += 50;
      }

      // name covered every word -> no snippet; else show the best text field
      var hit = null;
      if (inName < toks.length) {
        var pick = null, pickN = 0;
        c.e.forEach(function (en) {
          if (en.key === "name" || en.key === "alt") return;
          var nHit = toks.filter(function (t) { return has(en, t); }).length +
                     (toks.length > 1 && has(en, phrase) ? 1 : 0);
          if (nHit > pickN || (nHit === pickN && nHit && en.w > pick.w)) { pick = en; pickN = nHit; }
        });
        if (pick) hit = snippet(pick, toks);
      }
      out.push(result(c, score, toks, hit));
    });

    out.sort(function (a, b) { return b.score - a.score || a.lNum - b.lNum; });
    return out;
  }

  global.LFCSearch = { query: query, fold: fold };
})(typeof window !== "undefined" ? window : this);

if (typeof module !== "undefined") module.exports = (typeof window !== "undefined" ? window : this).LFCSearch;
