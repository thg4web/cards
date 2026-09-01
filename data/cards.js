// Lunar Field Cards -- authored card content.
//
// Merged onto data/lunar100.js by `id` at load time. Spine fields
// (name, significance, diamKm, lat, lon, rukl, stAtlas) are NOT repeated here.
//
// Full record -- see Project/docs/card-data-schema.md:
//   id       "L5"                        spine key
//   zone     "ER"|"EH"|"WH"|"WR"|""      lunar zone tab            (schema section 3)
//   cat      maria|crater|valley|special|ridge|mtn|volc            (schema section 4)
//   alt      "Rupes Recta"               header alt/Latin name, "" if none
//   dSeed    1..5                        first-pass difficulty     (schema section 5)
//   status   stub|draft|review|final     per-card workflow state
//   -- authored in Step 3/4, added to each object as it is written:
//   epoch, size[], depth, diff, bestDays[], outline, neighbours[], pins[],
//   photo, photoCredit, photoCaption, locator, locatorCredit,
//   description, nameOrigin, facts[3], tips
//
// flag comments: C concept   S spans boundary   B near 45-deg cutoff
//                R region/judgement   L limb/libration   H hypothesised

const CARDS = [
  { id:"L1",   zone:"",   cat:"special", alt:"",                    dSeed:1, status:"stub" }, // C
  { id:"L2",   zone:"",   cat:"special", alt:"",                    dSeed:1, status:"stub" }, // C
  { id:"L3",   zone:"",   cat:"special", alt:"",                    dSeed:1, status:"stub" }, // C
  { id:"L4",   zone:"WH", cat:"mtn",     alt:"Montes Apenninus",    dSeed:1, status:"stub" },
  { id:"L5",   zone:"WH", cat:"crater",  alt:"",                    dSeed:1, status:"draft",
    epoch:"Copernican",
    size:[{ label:"Diameter", value:"93 km (58 mi)" }],
    depth:"~3.8 km (12,500 ft)",
    diff:1,
    bestDays:[[9,11],[14,16]],
    outline:{ shape:"ellipse", cx:47, cy:52, rx:18, ry:12 },
    neighbours:[
      { label:"Copernicus",          x:22, y:36, o:true },
      { label:"Eratosthenes",        x:57, y:14, o:true },
      { label:"Oceanus Procellarum", x:5,  y:62 }
    ],
    pins:[{ label:"Apollo 12", x:30, y:83, kind:"apollo" }],
    photo:"plate-L5-photo.jpg",
    photoTag:"NASA · Lunar Orbiter 2",
    photoCredit:"Lunar Orbiter 2, 1966. The “Picture of the Century.” NASA / JPL / USGS. Stand-in until a Seestar capture takes this panel.",
    locator:"plate-L5-locator.jpg",
    locatorCredit:"LROC WAC · NASA/GSFC/ASU",
    description:"The archetypal large complex crater: about 93 km across and close to 4 km deep, with broad terraced walls slumped in concentric benches, a cluster of central mountains on a rough floor, and a blanket of bright rays and secondary craters flung across the surrounding mare. It stands alone on Mare Insularum, south of the Carpathian Mountains, so it reads sharply even at low power.",
    nameOrigin:"Named for Nicolaus Copernicus by Giovanni Battista Riccioli in his 1651 nomenclature. Riccioli did not accept a moving Earth, and by tradition is said to have flung Copernicus into the Ocean of Storms, grouping the crater with Kepler and Aristarchus out in Oceanus Procellarum.",
    facts:[
      "Lunar Orbiter 2’s 1966 oblique view down its terraced walls was hailed in the press as the picture of the century.",
      "The ray system reaches more than 800 km; the rays are young unweathered ejecta, marking the crater at roughly 800 million years old.",
      "The Copernican period, the Moon’s most recent geologic era, is named after this one crater."
    ],
    tips:"Easy in binoculars as a bright spot in the Moon’s western half. A small scope a night or two after first quarter shows the terraced rim and central peaks in raking light; near full Moon the crater flattens but its splash of rays becomes the brightest feature on that side." },
  { id:"L6",   zone:"WH", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L7",   zone:"EH", cat:"ridge",   alt:"Rupes Altai",         dSeed:1, status:"stub" },
  { id:"L8",   zone:"EH", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L9",   zone:"WH", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L10",  zone:"ER", cat:"maria",   alt:"",                    dSeed:1, status:"stub" },
  { id:"L11",  zone:"WR", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L12",  zone:"ER", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L13",  zone:"WH", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L14",  zone:"WH", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L15",  zone:"WH", cat:"ridge",   alt:"Rupes Recta",         dSeed:1, status:"stub" },
  { id:"L16",  zone:"ER", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L17",  zone:"WR", cat:"valley",  alt:"Vallis Schröteri",    dSeed:1, status:"stub" },
  { id:"L18",  zone:"EH", cat:"maria",   alt:"",                    dSeed:1, status:"stub" },
  { id:"L19",  zone:"EH", cat:"valley",  alt:"Vallis Alpes",        dSeed:1, status:"stub" },
  { id:"L20",  zone:"EH", cat:"crater",  alt:"",                    dSeed:1, status:"stub" },
  { id:"L21",  zone:"EH", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L22",  zone:"WR", cat:"volc",    alt:"",                    dSeed:2, status:"stub" },
  { id:"L23",  zone:"WH", cat:"mtn",     alt:"Mons Pico",           dSeed:2, status:"stub" },
  { id:"L24",  zone:"EH", cat:"valley",  alt:"Rima Hyginus",        dSeed:2, status:"stub" },
  { id:"L25",  zone:"ER", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L26",  zone:"EH", cat:"maria",   alt:"",                    dSeed:2, status:"stub" }, // S
  { id:"L27",  zone:"WH", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L28",  zone:"EH", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L29",  zone:"EH", cat:"valley",  alt:"Rima Ariadaeus",      dSeed:2, status:"stub" },
  { id:"L30",  zone:"WH", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L31",  zone:"ER", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L32",  zone:"EH", cat:"volc",    alt:"",                    dSeed:2, status:"stub" },
  { id:"L33",  zone:"EH", cat:"ridge",   alt:"Dorsa Smirnov",       dSeed:2, status:"stub" },
  { id:"L34",  zone:"EH", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L35",  zone:"EH", cat:"valley",  alt:"Rimae Triesnecker",   dSeed:2, status:"stub" },
  { id:"L36",  zone:"WR", cat:"maria",   alt:"",                    dSeed:2, status:"stub" },
  { id:"L37",  zone:"WR", cat:"maria",   alt:"",                    dSeed:2, status:"stub" },
  { id:"L38",  zone:"EH", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L39",  zone:"WR", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L40",  zone:"EH", cat:"valley",  alt:"Rimae Janssen",       dSeed:2, status:"stub" },
  { id:"L41",  zone:"EH", cat:"special", alt:"",                    dSeed:2, status:"stub" },
  { id:"L42",  zone:"WR", cat:"volc",    alt:"",                    dSeed:2, status:"stub" },
  { id:"L43",  zone:"WR", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L44",  zone:"WR", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L45",  zone:"EH", cat:"crater",  alt:"",                    dSeed:2, status:"stub" },
  { id:"L46",  zone:"WH", cat:"crater",  alt:"",                    dSeed:3, status:"stub" },
  { id:"L47",  zone:"WH", cat:"volc",    alt:"",                    dSeed:3, status:"stub" },
  { id:"L48",  zone:"EH", cat:"valley",  alt:"",                    dSeed:3, status:"stub" }, // R
  { id:"L49",  zone:"WH", cat:"volc",    alt:"",                    dSeed:3, status:"stub" },
  { id:"L50",  zone:"EH", cat:"maria",   alt:"",                    dSeed:3, status:"stub" },
  { id:"L51",  zone:"WH", cat:"crater",  alt:"Catena Davy",         dSeed:3, status:"stub" },
  { id:"L52",  zone:"WR", cat:"crater",  alt:"",                    dSeed:3, status:"stub" },
  { id:"L53",  zone:"EH", cat:"maria",   alt:"",                    dSeed:3, status:"stub" },
  { id:"L54",  zone:"WH", cat:"valley",  alt:"Rimae Hippalus",      dSeed:3, status:"stub" },
  { id:"L55",  zone:"EH", cat:"crater",  alt:"",                    dSeed:3, status:"stub" },
  { id:"L56",  zone:"ER", cat:"maria",   alt:"",                    dSeed:3, status:"stub" },
  { id:"L57",  zone:"WR", cat:"special", alt:"",                    dSeed:3, status:"stub" },
  { id:"L58",  zone:"ER", cat:"valley",  alt:"Vallis Rheita",       dSeed:3, status:"stub" },
  { id:"L59",  zone:"WR", cat:"maria",   alt:"",                    dSeed:3, status:"stub" }, // B
  { id:"L60",  zone:"WH", cat:"volc",    alt:"Kies π",         dSeed:3, status:"stub" },
  { id:"L61",  zone:"WH", cat:"crater",  alt:"",                    dSeed:3, status:"stub" },
  { id:"L62",  zone:"WR", cat:"volc",    alt:"Mons Rümker",         dSeed:3, status:"stub" },
  { id:"L63",  zone:"EH", cat:"special", alt:"",                    dSeed:3, status:"stub" },
  { id:"L64",  zone:"EH", cat:"crater",  alt:"",                    dSeed:3, status:"stub" },
  { id:"L65",  zone:"WH", cat:"volc",    alt:"",                    dSeed:3, status:"stub" },
  { id:"L66",  zone:"EH", cat:"valley",  alt:"Rima Hadley",         dSeed:4, status:"stub" },
  { id:"L67",  zone:"WH", cat:"special", alt:"",                    dSeed:4, status:"stub" },
  { id:"L68",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" }, // B
  { id:"L69",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L70",  zone:"ER", cat:"maria",   alt:"",                    dSeed:4, status:"stub" },
  { id:"L71",  zone:"EH", cat:"volc",    alt:"",                    dSeed:4, status:"stub" },
  { id:"L72",  zone:"EH", cat:"volc",    alt:"",                    dSeed:4, status:"stub" }, // B
  { id:"L73",  zone:"ER", cat:"maria",   alt:"",                    dSeed:4, status:"stub" }, // L
  { id:"L74",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L75",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L76",  zone:"EH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L77",  zone:"WR", cat:"valley",  alt:"Rima Sirsalis",       dSeed:4, status:"stub" },
  { id:"L78",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L79",  zone:"WH", cat:"volc",    alt:"",                    dSeed:4, status:"stub" },
  { id:"L80",  zone:"WR", cat:"maria",   alt:"",                    dSeed:4, status:"stub" }, // L
  { id:"L81",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L82",  zone:"EH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L83",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L84",  zone:"WH", cat:"crater",  alt:"",                    dSeed:4, status:"stub" },
  { id:"L85",  zone:"ER", cat:"special", alt:"",                    dSeed:4, status:"stub" },
  { id:"L86",  zone:"WH", cat:"valley",  alt:"Rimae Prinz",         dSeed:5, status:"stub" }, // B
  { id:"L87",  zone:"ER", cat:"crater",  alt:"",                    dSeed:5, status:"stub" },
  { id:"L88",  zone:"EH", cat:"crater",  alt:"",                    dSeed:5, status:"stub" }, // L
  { id:"L89",  zone:"EH", cat:"volc",    alt:"",                    dSeed:5, status:"stub" },
  { id:"L90",  zone:"EH", cat:"crater",  alt:"",                    dSeed:5, status:"stub" },
  { id:"L91",  zone:"WR", cat:"valley",  alt:"Rimae de Gasparis",   dSeed:5, status:"stub" },
  { id:"L92",  zone:"EH", cat:"valley",  alt:"Vallis Gyldén",       dSeed:5, status:"stub" },
  { id:"L93",  zone:"EH", cat:"special", alt:"",                    dSeed:5, status:"stub" },
  { id:"L94",  zone:"WR", cat:"crater",  alt:"",                    dSeed:5, status:"stub" }, // L
  { id:"L95",  zone:"WH", cat:"maria",   alt:"",                    dSeed:5, status:"stub" }, // S, H
  { id:"L96",  zone:"EH", cat:"mtn",     alt:"",                    dSeed:5, status:"stub" }, // L, H
  { id:"L97",  zone:"WR", cat:"valley",  alt:"Vallis Inghirami",    dSeed:5, status:"stub" },
  { id:"L98",  zone:"WH", cat:"maria",   alt:"",                    dSeed:5, status:"stub" },
  { id:"L99",  zone:"EH", cat:"volc",    alt:"Ina (D-caldera)",     dSeed:5, status:"stub" },
  { id:"L100", zone:"ER", cat:"special", alt:"",                    dSeed:5, status:"stub" }, // L
];

if (typeof module !== 'undefined') { module.exports = CARDS; }
