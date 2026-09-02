#!/usr/bin/env python3
"""fill-prose-21-100.py -- one-shot: author the information fields for cards
L21..L100 into data/cards.js.

Each stub already carries photo / photoTag / photoCredit / locator /
locatorCredit / outline (from the imagery batches). This adds epoch, size,
depth (where it applies), bestDays, description, nameOrigin, facts[3], tips and
flips status stub -> draft, keeping the image fields intact.

bestDays is computed from the schema rule (age = 7.4 - lonE/12.2, 2-day window,
+15 for the sunset pass, clamp 27). diff is set per card below.
"""
import math, re, sys

ROOT  = __file__.rsplit("/tools/", 1)[0]
SPINE = ROOT + "/data/lunar100.js"
CARDS = ROOT + "/data/cards.js"

# ------------------------------------------------------------------ spine lon
def spine_lon():
    out = {}
    for m in re.finditer(r'\[\s*\d+\s*,\s*"(L\d+)"\s*,(.*?)\],\s*$', open(SPINE).read(), re.M):
        p = re.findall(r'"([^"]*)"', m.group(2).replace('\\"', ''))
        if len(p) >= 6 and p[5]:
            lon = p[5].strip()
            out[m.group(1)] = -float(lon[:-1]) if lon[-1] in "Ww" else float(lon[:-1])
    return out

def best_days(lonE):
    age = 7.4 - lonE / 12.2
    a = max(0, math.floor(age))
    w1 = [a, a + 2]
    w2 = [min(27, a + 15), min(27, a + 17)]
    return [w1, w2]

# ------------------------------------------------------------------ content
# C[id] = (diff, epoch, [(label,value)...], depth-or-None, desc, origin, [f1,f2,f3], tips)
C = {
"L21": (2, "Nectarian", [("Diameter", "124 km (77 mi)")], "shallow, ~1.5 km; the floor sits near mare level",
 "A floor-fractured crater forming a bay on the south rim of Mare Nectaris. Its north wall is gone, breached and drowned by the mare, and its floor has been lifted and cracked from below into low domes and rilles. Under a low sun the broken northern side and the floor cracks stand out; under a high sun it nearly melts into the mare.",
 "Named for Girolamo Fracastoro, a sixteenth-century Italian physician, poet and astronomer who wrote on contagion and on the motions of the sky.",
 ["It is a close cousin of Gassendi and Posidonius, another crater whose floor was pushed up and split by magma at a basin edge.",
  "The missing north wall makes Fracastorius read as a bay of Nectaris rather than a closed ring.",
  "A fine rille and a scatter of low hills cross the flooded floor."],
 "Day 5, with Mare Nectaris on the terminator. A 100 mm scope shows the open north side and the main floor cracks; 150 mm adds the domes."),

"L22": (2, "Imbrian volcanism", [("Extent", "~200 x 150 km")], None,
 "A raised, tilted block of crust at the eastern edge of Oceanus Procellarum, mantled in dark volcanic ash and packed with volcanic landforms. It carries Aristarchus and Herodotus, Schroter's Valley, dozens of sinuous rilles and cones, and is the densest volcanic complex on the near side. The plateau stands one to two kilometres above the surrounding mare.",
 "The plateau takes its name from the brilliant crater Aristarchus on its southeast corner.",
 ["It holds the largest concentration of sinuous rilles anywhere on the Moon.",
  "The whole surface is coated in pyroclastic glass from fire-fountain eruptions, which is why it looks dark.",
  "Orbiters have detected radon gas leaking from the plateau, a sign it is not entirely dead."],
 "Day 11 to 13, western Procellarum on the terminator. Binoculars show the bright wedge of the plateau; a telescope adds Herodotus, the Cobra's Head and the rille field."),

"L23": (2, "Imbrian (basin ring)", [("Height", "~2.4 km (7,900 ft)"), ("Base", "~25 km (16 mi)")], None,
 "An isolated mountain rising sharply from the flat floor of Mare Imbrium, south of the crater Plato. It is a surviving fragment of an inner ring of the Imbrium basin, left standing when lava flooded around it. Though it looks like a spire, it is a broad, gentle pile; the drama is all in its shadow.",
 "From the Spanish and Portuguese word for a peak, applied by early mapmakers after a mountain in the Azores.",
 ["At sunrise and sunset Pico throws a long spike of shadow across the smooth mare, often easier to see than the mountain itself.",
  "It is one of several Imbrium ring fragments in the area, along with the Montes Teneriffe and Pico Beta.",
  "Despite the sharp look, its slopes are shallow, a rubble heap rather than a peak."],
 "Day 9, when the shadow is longest. Almost any scope shows the bright speck and its dark spire on the mare."),

"L24": (2, "Imbrian", [("Length", "~220 km (137 mi)")], None,
 "A rille near the centre of the disc that bends sharply where it meets the rimless crater Hyginus. Much of its length is not a smooth trench but a chain of round collapse pits with no raised rims, which points to the ground dropping into a fracture as gas or lava withdrew beneath it. It forms a rough Y with the Ariadaeus Rille to the east.",
 "From the crater Hyginus, for Gaius Julius Hyginus, a Roman writer on astronomy and myth of the first century BC.",
 ["Hyginus is one of the few sizeable lunar craters with no raised rim, itself probably a collapse or volcanic pit.",
  "The pit chain is aligned along a single fracture, suggesting a volcanic or drainage origin rather than a simple fault.",
  "It sits in a showcase strip of rilles with the Ariadaeus and Triesnecker systems nearby."],
 "Day 7, near first quarter, with the central highlands on the terminator. An 80 mm scope shows the rille and the kink at Hyginus; 150 mm resolves the pit chain."),

"L25": (2, "Copernican", [("Each", "~9 x 11 km (6 x 7 mi)")], None,
 "A pair of small craters in Mare Fecunditatis with two long bright rays sweeping west like a comet tail. Messier is an elongated oval, Messier A a double crater just west of it. The elongation and the twin one-sided rays are the signature of an impactor that came in at a very low angle from the east and almost skipped off the surface.",
 "For Charles Messier, the eighteenth-century French comet hunter whose catalogue of fuzzy objects is still in daily use.",
 ["The blank ground and the twin western rays point back along the path of a nearly grazing impact.",
  "In the nineteenth century the pair were at the centre of a long argument over whether they had changed shape; they had not.",
  "Their rays cross the dark mare and lighten it, making the comet shape easy to trace."],
 "Day 4 or 5 in Mare Fecunditatis. An 80 mm scope splits the two craters; the double western rays show better under higher sun toward full Moon."),

"L26": (1, "Imbrian fill", [("Length", "~1,600 km (990 mi)")], None,
 "A long, narrow, curving mare that runs along the northern edge of the near side, wrapping the top of Mare Imbrium. Unlike the round maria it is a ribbon, not a basin fill, roughly following the Imbrium basin rim, and its origin is still debated. Its floor is crossed by wrinkle ridges and dotted with flooded craters.",
 "Latin for the Sea of Cold, one of Riccioli's 1651 names, chosen for its far-northern place on the disc.",
 ["Mare Frigoris has no clear basin of its own, which sets it apart from every other named sea.",
  "It stretches through more than a thousand kilometres of longitude, the most elongated mare on the Moon.",
  "The crater Plato sits on its southern shore and makes a ready landmark."],
 "Any time the northern limb is lit. Sweep along the top of the Moon with low power; the ribbon of grey against the highlands is unmistakable."),

"L27": (1, "Upper Imbrian, later flooded", [("Diameter", "83 km (52 mi)")], "~2.1 km (6,900 ft)",
 "A large, sharp-rimmed crater on eastern Mare Imbrium whose floor is flooded smooth with mare lava, so it has no central peak, just a flat grey plain inside terraced walls. The flooding came after the crater formed, showing that Imbrium's lavas kept erupting long after the basin itself.",
 "For Archimedes of Syracuse, the Greek mathematician and engineer of the third century BC.",
 ["The lava-filled floor is one of the clearest cases of a crater drowned by later mare eruptions.",
  "A set of rilles, the Rimae Archimedes, runs across the mare to the southeast.",
  "With Aristillus and Autolycus it forms a distinctive triangle of craters on the plain."],
 "Day 8, near first quarter. The flat floor against the shadowed walls is striking, and a low sun brings out faint ridges on the fill."),

"L28": (2, "pre-Nectarian", [("Diameter", "~150 km (93 mi)")], None,
 "A large, very worn walled plain just southeast of the disc centre, its rim broken and low, its floor pocked by later craters and partly filled. It is old enough that within a day or two of the terminator passing, the whole ring nearly vanishes under higher light.",
 "For Hipparchus of Nicaea, the Greek astronomer of the second century BC who compiled the first star catalogue.",
 ["Hipparchus was the subject of one of the first drawings devoted to a single lunar crater rather than the whole face.",
  "The sharp young crater Horrocks sits inside it, a bright bowl on a faded floor.",
  "With its neighbour Albategnius it makes a classic first-quarter pairing."],
 "Day 7 or 8 only. Under a low sun the ghostly rim stands out; a few days later the crater is hard to find at all."),

"L29": (1, "Imbrian", [("Length", "~250 km (155 mi)")], None,
 "A long, remarkably straight trench running east to west between Mare Tranquillitatis and the central highlands. It is a graben, a strip of crust dropped between two parallel faults, and a textbook example of the type. It cuts craters and ridges without swerving, which shows it is tectonic, not carved by lava.",
 "From the small crater Ariadaeus, named for Philip Arrhidaeus, half-brother of Alexander the Great.",
 ["The rille is nearly dead straight for its full length, the mark of two clean parallel faults.",
  "It runs close to the Hyginus Rille and the two are usually observed together.",
  "It is one of the easiest rilles on the Moon, within reach of a 60 mm scope."],
 "Day 6 or 7, near first quarter. A small scope shows it as a fine straight line reaching out of the highlands into the mare."),

"L30": (3, "Nectarian", [("Length", "~180 km (112 mi)"), ("Width", "~70 km (43 mi)")], None,
 "A strange elongated crater in the southwest, shaped like a footprint or two merged craters, with a smooth floor and a low ridge but no central peak. A very oblique impact is the usual explanation, though a chance overlap of two craters is also argued.",
 "For Julius Schiller, a seventeenth-century German astronomer who tried, without lasting success, to rename the constellations after Biblical figures.",
 ["Schiller's outline is unlike any other large crater on the Moon.",
  "The smooth floor and missing peak fit a low-angle strike that ploughed rather than punched.",
  "It lies near the buried Schiller-Zucchius basin in the crowded southwest."],
 "Day 10 to 12 in the southwest, when libration tips the region into view. Low power shows the odd shape, which is the whole point of the card."),

"L31": (2, "Eratosthenian", [("Diameter", "56 km (35 mi)")], None,
 "A young floor-fractured crater on the northwest shore of Mare Fecunditatis. A low central rise is ringed by a delicate concentric crack, and a fresh-looking ejecta apron surrounds the sharp rim. Because it is one of the youngest craters of its kind, the cracks and inner ring are crisp rather than softened.",
 "For Lucius Tarutius Firmanus, a Roman scholar and astrologer of the first century BC.",
 ["Its floor was domed upward by magma pushing beneath a thin crater floor near the mare edge.",
  "A faint ray system still surrounds it, another sign of its youth.",
  "It is a compact, bright object that stands out against the darker mare."],
 "Day 4 or 5 in Mare Fecunditatis. A 100 mm scope under low light shows the central rise and the concentric rille around it."),

"L32": (3, "Imbrian volcanism", [("Field", "~26 km (16 mi) across")], None,
 "Two of the largest and best-studied volcanic domes on the Moon, low swellings near the crater Arago in western Mare Tranquillitatis. Each rises only a few hundred metres over tens of kilometres, a very gentle bulge built by thick, slow lava, and each carries a small summit pit where the last lava drained back.",
 "From the crater Arago, for Francois Arago, the nineteenth-century French physicist and astronomer.",
 ["Arago Alpha is about 30 km across but rises only some 300 m, so it is nearly invisible except at sunrise.",
  "The domes were built by lava too stiff to spread far, piling up over a vent instead.",
  "Summit craterlets on both mark the vents."],
 "Day 6, first quarter, with Tranquillitatis on the terminator. The domes show only when the sun is within a few degrees of rising on them; otherwise they disappear."),

"L33": (1, "post-dates the Imbrian mare fill", [("Length", "~150 km (93 mi)")], None,
 "A prominent, snaking wrinkle ridge running up the eastern floor of Mare Serenitatis, one of the finest ridge systems visible from Earth. It marks a buried inner ring of the Serenitatis basin. Wrinkle ridges form where cooling mare lava is squeezed and buckles as the basin settles.",
 "An old descriptive name; the formal designation is Dorsa Smirnov, for the Russian geologist Sergey Smirnov.",
 ["The ridge traces a ring of the buried basin structure beneath the smooth lava.",
  "It stands only tens to a couple of hundred metres high, yet casts a clear shadow at low sun.",
  "Within two days of the terminator passing, it flattens almost to invisibility."],
 "Day 6, near first quarter. The ridge stands out sharply against the smooth mare; catch it before the sun climbs and erases it."),

"L34": (2, "Nectarian crater, Imbrian fill", [("Span", "~150 km (93 mi)")], None,
 "A large, roughly hexagonal flooded crater or plain in the north, the Lake of Death, with the crater Burg on its floor, a branching rille system and a wrinkle ridge. The angular outline hints that old fractures controlled its shape.",
 "Latin for the Lake of Death, one of Riccioli's darker names, paired with the nearby Lacus Somniorum, the Lake of Dreams.",
 ["Burg sits off-centre with a bright interior and a small central peak.",
  "The Rimae Burg fan across the floor and are a good medium-aperture target.",
  "Straight sections of the surrounding wall give the plain its odd, boxy look."],
 "Day 6, northern near side. A 100 mm scope shows Burg and the main rille; low sun sharpens the straight walls."),

"L35": (3, "Imbrian", [("Extent", "~215 km (134 mi)")], None,
 "A dense, braided network of narrow rilles near the crater Triesnecker, just east of the disc centre, one of the most intricate rille fields a telescope can show. The rilles cross at angles, unusual for a graben set, and their origin is still argued between faulting and volcanism.",
 "From the crater Triesnecker, for Franz von Paula Triesnecker, an eighteenth-century Austrian Jesuit astronomer.",
 ["The mesh runs close to the Hyginus and Ariadaeus rilles, making this strip of the Moon a rille showcase.",
  "The main channels show in a 100 mm scope; the finest threads need 200 mm and excellent seeing.",
  "The pattern is tighter and more tangled than a typical parallel graben set."],
 "Day 7 or 8, near first quarter, with the central meridian on the terminator. Steady air matters as much as aperture."),

"L36": (2, "pre-Nectarian basin", [("Diameter", "~430 km (267 mi)"), ("Dark floor", "~220 km (137 mi)")], None,
 "A small two-ring impact basin near the western limb whose inner ring is filled with very dark mare lava, making Grimaldi one of the darkest spots on the near side. The low reflectivity makes it visible to the naked eye near full Moon as a small dark patch on the western edge.",
 "For Francesco Maria Grimaldi, the seventeenth-century Italian Jesuit who, with Riccioli, produced the 1651 map and the naming system still in use.",
 ["The dark floor is ringed by a broken mountainous rim about 430 km across.",
  "Libration in longitude strongly changes how foreshortened the basin looks.",
  "Grimaldi also co-discovered the diffraction of light, unrelated to his lunar work but from the same restless mind."],
 "Day 13 or 14, or just after full Moon. The dark floor is obvious; the outer ring is subtle and shows best at favourable western libration."),

"L37": (4, "pre-Nectarian", [("Diameter", "~300 km (186 mi)")], None,
 "The largest crater on the near side, so old and broken that it reads as a rough field of hills and smaller craters rather than a crater. It is sometimes called a field of ruins. It sits near the southwest limb and is only worth chasing when southern libration is favourable.",
 "For Jean Sylvain Bailly, the eighteenth-century French astronomer and historian who was briefly mayor of Paris and was guillotined in the Revolution.",
 ["Bailly is large enough that some classify it as an impact basin rather than a crater.",
  "Its rim rises to around 4 km but is deeply gullied and hard to trace.",
  "Foreshortening near the limb makes detail fleeting even on a good night."],
 "Day 13 to 15, deep in the southwest, only when southern libration is favourable. Low power shows the broken ring; expect a jumble, not a bowl."),

"L38": (2, "Imbrian", [("Each", "~30 km (19 mi)")], None,
 "A near-identical pair of craters on the western shore of Mare Tranquillitatis, long cited as possible twin impacts. Both have flat, fractured floors, from their position at the mare edge. Apollo 11 came in over them, and they were landmarks on the approach to the landing site just to the southeast.",
 "For Sir Edward Sabine, the Irish astronomer and geophysicist, and Karl Ritter, the German geographer.",
 ["The two are so alike in size and form that a shared origin was once assumed; a chance pairing now seems more likely.",
  "Both floors are cracked like small floor-fractured craters.",
  "The Apollo 11 landing point lies a short way southeast, on smooth mare with no crater to mark it."],
 "Day 6, first quarter. An 80 mm scope splits the pair; the low-relief floors show their fractures only under very low sun."),

"L39": (3, "Nectarian", [("Diameter", "~227 km (141 mi)")], None,
 "A huge walled plain in the southwest whose darker, mare-flooded floor is crossed by a broad lighter stripe of debris flung from the Orientale basin far to the west. The result is a floor in three tone bands. The low, worn rim makes Schickard look more like a bay than a crater under a high sun.",
 "For Wilhelm Schickard, the seventeenth-century German polymath who built one of the first mechanical calculating machines.",
 ["The pale central band is an ejecta sheet from the Orientale impact, laid across the older floor.",
  "The darker patches on either side are later mare lava.",
  "At about 230 km across it is one of the largest craters on the near side."],
 "Day 12 in the southwest, libration permitting. Low power shows the size and the banded floor, which is the feature's signature."),

"L40": (3, "Nectarian terrain, later faulting", [("Length", "~190 km (118 mi)")], None,
 "A rare highland rille, a broad valley-like graben crossing the floor of the ancient crater Janssen in the rugged southeast. Rilles are mostly a mare feature, so one running through old highland crust is unusual and harder to explain.",
 "From the crater Janssen, for Jules Janssen, the nineteenth-century French astronomer and pioneer of solar spectroscopy.",
 ["Most rilles sit in young mare basalt; this one runs through some of the oldest crust on the Moon.",
  "The crater Janssen that holds it is about 190 km across and barely holds together.",
  "The sharp crater Fabricius cuts its northeastern floor and makes a good pointer to it."],
 "Day 5, deep southeast under a low sun. A 150 mm scope shows the rille as a wide shallow trough; good libration and seeing help."),

"L41": (2, "Copernican (ray)", [("Length", "~300 km (186 mi)")], None,
 "A single bright ray crossing Mare Serenitatis from south to north in a nearly straight line, passing near the crater Bessel. Its source crater is uncertain; Menelaus to the south and distant Tycho are the usual suspects, but tracing it back is a classic puzzle.",
 "From the crater Bessel, for Friedrich Bessel, the nineteenth-century German astronomer who made the first reliable measurement of a stellar parallax.",
 ["It is one of the few prominent rays that crosses an entire mare on its own.",
  "It does not clearly begin at Bessel, despite the name.",
  "Like all rays it fades under low sun and brightens toward full Moon."],
 "High sun, day 9 onward toward full Moon. The ray is easy in binoculars once Serenitatis is well lit."),

"L42": (3, "Imbrian volcanism", [("Field", "~125 km (78 mi) across")], None,
 "The largest field of volcanic domes and cones on the Moon, dozens of low mounds packed into a stretch of Oceanus Procellarum near the crater Marius, with sinuous rilles winding among them. The domes here are steeper and blockier than the gentle Arago or Hortensius domes, built from stickier lava.",
 "From the crater Marius, for Simon Marius, the seventeenth-century German astronomer who observed Jupiter's moons independently of Galileo.",
 ["It holds the densest concentration of lunar volcanic landforms, domes, cones and rilles together.",
  "A deep pit found among the hills from orbit may be the collapsed roof of a lava tube.",
  "The domes range from a few kilometres to over ten across."],
 "Day 11 to 13, western Procellarum on the terminator. A 150 mm scope at low sun shows the mottled, lumpy ground; the individual domes are subtle."),

"L43": (3, "Nectarian crater, Imbrian fill", [("Diameter", "84 km (52 mi)")], None,
 "A crater in the southwest that filled to the brim with lava or ejecta before it could drain, leaving a raised plateau instead of a hollow. It is the best example on the Moon of a crater filled flush with its rim, so it stands proud of the surrounding land.",
 "For Pehr Wargentin, the eighteenth-century Swedish astronomer who was long-serving secretary of the Swedish Academy of Sciences.",
 ["Low ridges on its raised floor may be lava that squeezed up along cooling cracks.",
  "It sits against the larger crater pair Nasmyth and Phocylides.",
  "Observers nickname it the cheese, or the thin cheese, for its flat raised disc."],
 "Day 12 or 13 in the southwest, at favourable libration. A low sun catches the rim so the whole table stands up from the terrain."),

"L44": (3, "Nectarian", [("Diameter", "84 km (52 mi)")], None,
 "An 84 km crater on the west rim of Mare Humorum with a distinctly domed, bulging floor, later peppered by a line of small secondary craters. Rilles run in the mare just to its east. The convex floor was pushed up by magma under the Humorum basin edge, like Gassendi across the mare.",
 "For Marin Mersenne, the seventeenth-century French friar and mathematician who was the hub of scientific correspondence in Europe.",
 ["Its bulged floor makes it a floor-fractured crater, one of a ring of them around Mare Humorum.",
  "The chain of small craters across the floor are secondaries from a later impact elsewhere.",
  "The Rimae Mersenius run north to south in the mare to the east."],
 "Day 12, on the western Humorum shore under a low sun. A 100 mm scope shows the bulged floor and the secondary chain; 150 mm the rilles."),

"L45": (2, "Nectarian", [("Diameter", "114 km (71 mi)")], None,
 "A large, deep crater in the crowded southern highlands, a good place to see saturation cratering, ground so old that a new crater can only form by destroying older ones. Maurolycus has a cluster of central peaks and heavily terraced walls, partly overlapping older craters.",
 "For Francesco Maurolico, the sixteenth-century Sicilian mathematician and astronomer.",
 ["The highlands around it are saturated, so the crater count has stopped rising with time.",
  "Its walls cut into older craters, showing it is younger than the terrain it sits in.",
  "It is a striking sight when the first-quarter terminator runs through it."],
 "Day 7, southern highlands on the terminator. Almost any scope shows the deep interior and peaks; the saturated ground around it is the thing to notice."),

"L46": (3, "Nectarian", [("Crater", "124 km (77 mi)")], None,
 "The off-centre peak on the floor of the distorted crater Regiomontanus carries a small summit pit. That pit once raised the idea, now doubted, that it might be a volcanic vent atop a crater's central mountain. It is almost certainly a small impact.",
 "From the crater Regiomontanus, the Latin name of Johannes Muller of Konigsberg, the fifteenth-century German astronomer.",
 ["The summit craterlet is tiny, and resolving it is the observing challenge.",
  "Regiomontanus is squeezed into a rough rectangle by the older crater Purbach to its north.",
  "The Walter, Regiomontanus and Purbach column is a classic first-quarter chain."],
 "Day 8, near the central meridian on the terminator. A 150 mm scope and steady air show the pit on the peak."),

"L47": (3, "Imbrian volcanism on a Nectarian crater", [("Crater", "119 km (74 mi)")], None,
 "Several dark-haloed pits on the floor of the crater Alphonsus, small explosive volcanic vents that erupted ash along the floor's rilles. Unlike bright young craters, these are ringed by darker, not lighter, material.",
 "From the crater Alphonsus, for Alfonso X of Castile, the thirteenth-century king who sponsored the Alfonsine astronomical tables.",
 ["The dark halos are ash rings around vents where gas-charged magma reached the surface.",
  "In 1958 Nikolai Kozyrev reported a spectrum of gas over Alphonsus, one of the better-documented transient events.",
  "Ranger 9 crashed into the floor in 1965, sending back close-up pictures to the last second."],
 "Day 8, just west of centre. Any scope shows the crater and its central peak; the dark spots need 150 mm and a low-to-moderate sun."),

"L48": (2, "Imbrian", [("Region", "~130 km (81 mi) across")], None,
 "A compact showcase in Mare Tranquillitatis: the sharp crater Cauchy, the straight Cauchy Fault, the parallel Cauchy Rille, and two domes, all in one low-power field. The fault and the rille run on opposite sides of the crater, a scarp on one side and a graben on the other, recording a stretch of the mare crust.",
 "From the crater Cauchy, for Augustin-Louis Cauchy, the nineteenth-century French mathematician.",
 ["The fault shows as a bright or a dark line depending on the sun angle.",
  "Two domes nearby, Cauchy Omega and Tau, sit within the same field, one with a summit pit.",
  "The whole set fits inside about a 40 km span."],
 "Day 5, eastern Tranquillitatis on the terminator. A 100 mm scope shows the fault, the rille and the crater together."),

"L49": (3, "Imbrian, possibly evolved volcanism", [("Domes", "~20 km (12 mi) across the pair")], None,
 "Two steep, dome-like mountains on the Imbrium shore near the crater Gruithuisen, built from unusually thick, silica-rich lava, so they bulge one to two kilometres high instead of the usual few hundred metres. They are prime targets for future landers looking for non-basaltic lunar magma.",
 "From the crater Gruithuisen, for Franz von Paula Gruithuisen, the nineteenth-century Bavarian astronomer who once claimed to see a lunar city.",
 ["Their steep slopes mark eruptions of viscous, evolved lava, rare on a Moon dominated by runny basalt.",
  "Small summit craters cap both domes.",
  "They stand on the boundary between the Jura Mountains and northern Mare Imbrium."],
 "Day 10 or 11, northwest Imbrium shore under a low sun. A 100 mm scope shows the two rounded humps above the mare; higher power their steep profiles."),

"L50": (2, "Imbrian (Cayley Formation)", [("Patch", "~14 km (9 mi)")], None,
 "Patches of smooth, light-toned plains filling low ground in the central highlands near the crater Cayley. They look like old lava, flat and pale, but Apollo 16 sampled them and found only impact breccia, which rewrote how such light plains everywhere on the Moon are read.",
 "From the crater Cayley, for Arthur Cayley, the nineteenth-century British mathematician.",
 ["The plains fill valleys and crater floors across the highlands, wherever there was a low spot to catch debris.",
  "Before Apollo 16 they were widely taken for highland volcanism.",
  "The samples turned out to be debris sheets flung from large basin impacts."],
 "Day 7, central highlands on the terminator. Any scope shows the smooth pale floors between the rugged hills near Cayley and Whewell."),

"L51": (4, "Copernican", [("Length", "~50 km (31 mi)")], None,
 "A straight string of a dozen or so tiny craters, each a kilometre or two across, laid across the floor of the ruined crater Davy Y just west of centre. It is thought to record the impact of a train of fragments from a body pulled apart by tides before it hit, like Shoemaker-Levy 9 at Jupiter.",
 "From the crater Davy, for Sir Humphry Davy, the English chemist of the early nineteenth century.",
 ["The chain is beautifully straight, the signature of a tidally disrupted impactor.",
  "The individual pits shrink steadily toward one end of the line.",
  "It takes 150 mm and good seeing to resolve the craterlets."],
 "Day 8, near the central meridian. Find the crater Davy first, then look for the fine dotted line on the neighbouring floor at high power."),

"L52": (3, "Nectarian crater, later lava", [("Diameter", "45 km (28 mi)")], None,
 "A 45 km crater near the western limb whose floor is filled with very dark, smooth lava with no central peak, giving it the look of a small volcanic caldera, though it is an impact crater. Its floor is one of the darkest on the near side.",
 "For Peter Cruger, the seventeenth-century German mathematician and astronomer who taught Hevelius.",
 ["Late lava from Oceanus Procellarum seeped in and flooded the floor black.",
  "The flat dark floor and missing peak are what gave rise to the caldera idea.",
  "Foreshortening near the limb makes the crater look distinctly oval."],
 "Day 13, southwest limb, at favourable libration. Low power shows the dark floor as an inky spot; there is little internal detail to chase."),

"L53": (3, "buried Nectarian, Imbrian fill", [("Ring", "~106 km (66 mi)")], None,
 "A ghostly ring of wrinkle ridges in southern Mare Tranquillitatis marking a crater or small basin buried under the mare. There is almost nothing to see except the ridge pattern, concentric and radial, where the lava draped and settled over a buried structure.",
 "From the crater Lamont, for Johann von Lamont, the nineteenth-century Scottish-born Bavarian astronomer.",
 ["Whether Lamont is a buried crater or a small basin is still uncertain.",
  "It shows only as low ridges, a test of how faint a feature you can pull out of a flat mare.",
  "The ridges stand for a night or two around the terminator, then vanish."],
 "Day 6, southern Tranquillitatis right on the terminator. A 100 mm scope at low power and a patient eye are what it takes."),

"L54": (3, "Imbrian", [("Extent", "~240 km (149 mi)")], None,
 "A set of long, gently curved rilles on the east side of Mare Humorum, running concentric with the basin rim. They formed as the basin edge stretched and dropped along rings of faults after the lava filled in.",
 "From the crater Hippalus, for the Greek navigator who described the monsoon winds of the Indian Ocean.",
 ["The rilles arc parallel to the Humorum shore, tracing rings of faulting around the settling basin.",
  "The crater Hippalus itself is a half-drowned ring that the rilles cut across.",
  "The Campanus and Mercator craters sit at the southern end of the system."],
 "Day 10, on the eastern Humorum shore under a low sun. A 100 mm scope shows two or three of the arcs; more aperture shows more."),

"L55": (3, "Nectarian", [("Diameter", "69 km (43 mi)")], None,
 "A deep crater in the far southern highlands surrounded, unusually for that region, by a broad apron of smooth, light plains, so it sits in a patch of calm amid the roughest terrain on the near side. The origin of the plains is debated between old lava and impact debris.",
 "For Roger Bacon, the thirteenth-century English friar and early advocate of experiment, latinised as Baco.",
 ["The smooth plains around Baco stand out sharply against the saturated highlands.",
  "Baco itself has a flat floor and sharp walls, younger-looking than its surroundings.",
  "It lies deep enough south that libration matters for seeing it well."],
 "Day 6, deep south on the terminator, with favourable libration. Low power shows the crater and the surprising smoothness around it."),

"L56": (4, "pre-Nectarian", [("Basin", "~600 km (370 mi)")], None,
 "A very old impact basin straddling the southeast limb, its floor a scatter of separate dark mare patches inside and between craters rather than one continuous sheet. The rim is almost erased, and even at favourable libration the whole thing is foreshortened to a thin strip.",
 "Latin for the Southern Sea, named for its position; the basin name follows the mare.",
 ["The mare here is a patchwork, lava that welled up into many crater floors over a wide area.",
  "Only strong eastern libration brings the basin into view at all.",
  "It is one of the least conspicuous named basins from Earth."],
 "Around the crescent phases for the sunrise view, better after full Moon, always with strong eastern libration. Low power shows dark blotches along the limb."),

"L57": (2, "surface marking, age uncertain", [("Extent", "~70 km (43 mi)")], None,
 "A bright, tadpole-shaped swirl in Oceanus Procellarum with no relief at all, just a pale marking on the mare, tied to one of the strongest magnetic anomalies on the Moon. Swirls are flat, so they are not deposits or flows but a change in how the top soil has weathered.",
 "From the nearby crater Reiner, for Vincenzo Reinieri, a seventeenth-century Italian astronomer and correspondent of Galileo.",
 ["The local magnetic field seems to shield the surface from the solar wind, keeping it bright.",
  "Reiner Gamma is the type example of a lunar swirl and a target for a dedicated orbiter.",
  "It shows no detail at low sun because it is pure tone, not shape."],
 "High sun, day 12 onward toward full Moon. An 80 mm scope shows the bright comma shape west of the crater Reiner."),

"L58": (3, "Nectarian", [("Length", "~450 km (280 mi)")], None,
 "A long, straight trench in the rugged southeast made of overlapping elongated craters, a chain of secondary impacts flung out along a line from the Nectaris basin. It is one of the best secondary-crater chains a telescope can show.",
 "From the crater Rheita, for Anton Maria Schyrleus of Rheita, a seventeenth-century Bohemian friar and optician.",
 ["The gouges are all radial to Nectaris, dug by debris thrown from that impact.",
  "The crater Rheita sits at the northwestern end of the chain.",
  "Under a low sun the beads-on-a-string structure is clear at higher power."],
 "Day 4, southeast under a low sun with decent libration. Low power shows the whole gash; higher power the individual craters."),

"L59": (4, "pre-Nectarian", [("Basin", "~335 km (208 mi)")], None,
 "A badly worn impact basin in the southwest, overlooked for years because its rim is so degraded. The elongated crater Schiller lies on its northern rim. Its inner ring survives only as an arc of low peaks, and parts of its floor carry dark mare patches.",
 "Named for the craters Schiller and Zucchius on its rim; Zucchius honours Niccolo Zucchi, a seventeenth-century Italian Jesuit astronomer.",
 ["Recognising the basin at all took careful mapping of subtle, broken rings.",
  "It is one of the oldest identifiable basins on the near side.",
  "The region needs favourable libration to be seen well."],
 "Day 11 or 12 in the southwest, with favourable libration. Low power and a low sun show the ring of hills; this is a know-what-you-are-looking-for object."),

"L60": (3, "Imbrian volcanism", [("Dome", "~12 km (7 mi)")], None,
 "A classic isolated volcanic dome in Mare Nubium just west of the flooded crater Kies, a low circular swelling with a small summit pit. It rises only about 150 m over its 12 km width, a very gentle bulge typical of fluid lava, and sits alone on smooth mare, which makes it a favourite first dome for observers.",
 "From the crater Kies, for Johann Kies, an eighteenth-century German astronomer; Pi is the old label for the dome.",
 ["A tiny craterlet marks the vent at the dome's summit.",
  "Its shallow slope means it shows only when the sun is within a few degrees of local sunrise.",
  "It is a textbook mare dome, useful for learning what to look for elsewhere."],
 "Day 10, Mare Nubium on the terminator. A 100 mm scope and a very low sun show the dome and its pit; it fades under higher light."),

"L61": (2, "Copernican", [("Diameter", "13 km (8 mi)")], None,
 "A small, sharp, bright bowl crater near the centre of the near side, historically used as the reference point for the Moon's coordinate grid. It is a textbook fresh simple crater, a clean bowl with a bright rim and no terraces.",
 "From the crater Mosting, for Johan Sigismund von Mosting, a Danish statesman and patron of astronomy in the early nineteenth century.",
 ["Its precise position was long the origin for selenographic longitude and latitude.",
  "Its size and central location make it a handy yardstick on the disc.",
  "It is bright enough to serve as a landmark for finding fainter nearby features."],
 "Day 8, just southwest of the exact centre. Any scope shows it as a brilliant little point."),

"L62": (3, "Imbrian volcanism", [("Diameter", "~70 km (43 mi)")], None,
 "A large volcanic construct in northern Oceanus Procellarum, a broad raised platform carrying about thirty coalesced domes, the biggest volcanic pile on the near side. It rises several hundred metres above the mare and looks like a wrinkled blister under a low sun.",
 "From Mons Rumker, for Karl Rumker, a nineteenth-century German astronomer.",
 ["It is a cluster of domes merged into a single plateau, not one smooth shield.",
  "China's Chang'e 5 landed just south of it in 2020 and returned some of the Moon's youngest basalts.",
  "The dome tops on its surface show only at grazing sun."],
 "Day 12 or 13, far northwest Procellarum, with libration helping. A 100 mm scope shows the raised patch; larger scopes the lumpy tops."),

"L63": (3, "Lower Imbrian", [("Pattern", "radial to Mare Imbrium")], None,
 "A set of parallel gouges and ridges in the highlands southeast of Mare Imbrium, all aligned radial to the basin. They are scars ploughed by low-flying debris from the Imbrium impact, a landscape-scale ejecta texture rather than a single feature.",
 "A descriptive term coined by Grove Karl Gilbert in 1893, who recognised the pattern and used it to locate the Imbrium impact.",
 ["Gilbert took the sculpture as evidence that Mare Imbrium fills an impact basin, not a volcanic one.",
  "The flooded craters Julius Caesar and Boscovich show the grooved grain clearly.",
  "Every valley and ridge in the set points back toward the centre of Imbrium."],
 "Day 7, first quarter, with the ground southeast of Imbrium on the terminator. Low power and a low sun bring out the combed texture."),

"L64": (3, "Nectarian crater", [("Diameter", "48 km (30 mi)")], None,
 "A worn crater in the central highlands whose hilly, furrowed surroundings were the target of Apollo 16. From Earth they looked like highland lava domes and flows, so the mission was sent to sample lunar volcanism. The crew found only impact breccia, and the volcanic reading collapsed.",
 "From the crater Descartes, for Rene Descartes, the seventeenth-century French philosopher and mathematician.",
 ["The Descartes and Cayley terrain is now read as basin debris, not volcanism.",
  "One of the Moon's strongest patches of crustal magnetism lies nearby.",
  "Apollo 16 was the only mission to land in the lunar highlands."],
 "Day 7, central highlands. A 100 mm scope shows the low crater and the rough ground around the landing site."),

"L65": (3, "Imbrian volcanism", [("Field", "~10 km (6 mi) across")], None,
 "A tight group of about six low volcanic domes just north of the crater Hortensius in Mare Insularum, each a few kilometres across and only one or two hundred metres high, and nearly all with a clear summit pit. It is one of the cleanest dome fields to observe.",
 "From the crater Hortensius, for Martinus Hortensius, a seventeenth-century Dutch astronomer.",
 ["The domes sit close together on smooth mare, which makes them easier to pick out than scattered ones.",
  "Almost every dome shows a central craterlet, the vent.",
  "The group is a natural test of seeing and low-sun timing."],
 "Day 10, between Copernicus and Kepler on the terminator. A 100 mm scope at low sun shows the blisters; higher power the summit pits."),

"L66": (3, "Imbrian volcanism", [("Length", "~80 km (50 mi)"), ("Width", "~1.5 km (1 mi)")], "~300 m (1,000 ft)",
 "A sinuous lava channel winding along the foot of the Montes Apenninus, visited on the ground by Apollo 15, whose crew drove to its edge. It is a collapsed or roofed lava channel that carried flows along the mountain front, and one of the few rilles a telescope user can connect to a place humans have stood.",
 "From Mons Hadley, the Apennine peak, for John Hadley, the English inventor of the reflecting octant in the early eighteenth century.",
 ["Apollo 15 landed beside it in 1971 and photographed rock layering in its far wall.",
  "The rille is about 1.5 km wide and 300 m deep, meandering like a river channel.",
  "It runs for roughly 80 km along the base of the Apennines."],
 "Day 8, with the Apennine front on the terminator. A 150 mm scope and steady air show the rille as a thread against the mountains."),

"L67": (3, "Lower Imbrian", [("Feature", "Imbrium ejecta blanket")], None,
 "A broad blanket of hummocky, ridged material draped over the highlands south of Copernicus, debris thrown from the Imbrium basin. Apollo 14 landed on it in 1971 to sample that ejecta and to reach Cone Crater, which had punched through to deeper layers.",
 "From the crater Fra Mauro, for the fifteenth-century Venetian monk and mapmaker.",
 ["The formation is the Imbrium impact's ejecta sheet, ridged and grooved across a wide area.",
  "The ghost crater Fra Mauro that names it is nearly buried by the same debris.",
  "The crew hauled a cart of tools uphill toward Cone Crater but ran out of time short of the rim."],
 "Day 9, south of Copernicus. A low sun shows the rolling, grooved ground; the craters Fra Mauro, Bonpland and Parry frame the site."),

"L68": (3, "buried pre-Imbrian, Imbrian fill", [("Ring", "~110 km (68 mi)")], None,
 "A nearly complete ring of low hills in Oceanus Procellarum, the rim of a large crater almost entirely buried by mare lava. Only the tops of the old wall stand above the flood. Surveyor 1 soft-landed just inside it in 1966, the first fully successful US landing on the Moon.",
 "From the small crater Flamsteed on the ring, for John Flamsteed, the first Astronomer Royal of England in the late seventeenth century.",
 ["The buried crater is about 110 km across; the lava filled it almost to the brim.",
  "The sharp little crater Flamsteed sits on the southern part of the ring.",
  "It shows how deep the Procellarum lavas ran, enough to drown a crater this size."],
 "Day 11 or 12, western Procellarum under a low sun. A 100 mm scope shows the broken ring of hummocks; a high sun erases it."),

"L69": (3, "Copernican", [("Craterlets", "~4 km (2 mi) and smaller")], None,
 "The field of small gouges, loops and V-shaped pairs scattered north of Copernicus around the crater Pytheas, dug by chunks of rock thrown out when Copernicus formed. Secondaries form in clusters and chains, often as herringbone pairs pointing back toward the primary.",
 "The craterlets take their name from their parent crater, Copernicus.",
 ["They show how far Copernicus ejecta travelled, tens to over a hundred kilometres.",
  "A surface peppered by them is younger than nothing and older than Copernicus, a dating tool.",
  "They look ragged and paired, unlike the clean bowls of primary impacts."],
 "Day 9 or 10, the mare north of Copernicus on the terminator. A 100 mm scope shows the irregular pits and chains around Pytheas."),

"L70": (4, "Nectarian", [("Basin", "~600 km (370 mi)"), ("Mare", "~270 km (170 mi)")], None,
 "A multi-ring impact basin on the northeast limb, with a dark inner sea of lava. It is heavily foreshortened and only well seen at favourable libration, when at least three rings can be traced with the dark mare filling the centre.",
 "For Alexander von Humboldt, the German naturalist and explorer of the early nineteenth century; the mare and basin follow the name.",
 ["Its position right at the limb means libration can add or subtract a lot of what is visible.",
  "The large crater Belkovich sits on its rim.",
  "The dark central mare is what catches the eye first."],
 "Just after full Moon, or the crescent phases for the sunrise view, always with strong northeast libration. Low power shows the dark oval and a partial ring."),

"L71": (3, "Imbrian volcanism", [("Deposit", "tens of km across")], None,
 "A dark, smooth deposit of volcanic ash coating the mare and low hills northwest of the crater Sulpicius Gallus, on the southwest edge of Mare Serenitatis. It is fire-fountain ash, glass beads flung out and settled as a dark blanket.",
 "From the crater Sulpicius Gallus, for a Roman consul and astronomer who predicted an eclipse in 168 BC.",
 ["It is the same kind of material Apollo 17 sampled as orange soil across the basin.",
  "The deposit darkens an area tens of kilometres across along the mare shore.",
  "The nearby Serpentine Ridge makes a good pointer to it."],
 "A moderate to high sun, day 7 onward, since this is a tone feature. A 100 mm scope shows the dusky smudge on the mare edge."),

"L72": (3, "Imbrian volcanism on an older crater", [("Crater", "87 km (54 mi)")], None,
 "Small pits on the floor of the large crater Atlas ringed by dark ash, volcanic vents that opened along the crater's floor fractures. Unlike bright young craters these are ringed by darker, not lighter, material.",
 "From the crater Atlas, for the Titan of Greek myth who holds up the sky.",
 ["Atlas is a floor-fractured crater, and gas-charged magma reached the surface through its cracks.",
  "It pairs with the lava-flooded crater Hercules just to its west.",
  "The dark spots lie along the rilles that web the crater floor."],
 "Day 4, northeast quadrant on the terminator. A 100 mm scope shows Atlas's fractured floor; 150 mm the dark-haloed pits."),

"L73": (4, "pre-Nectarian", [("Basin", "~500 km (310 mi)")], None,
 "An ancient basin sitting right on the eastern limb, with a smooth dark mare floor and a partial scarp for a rim. It lies on the equator, so from Earth it is seen almost edge-on and needs strong libration to show at all.",
 "For William Henry Smyth, the nineteenth-century British naval officer and astronomer, author of a famous observing handbook.",
 ["Mare Smythii was one of the last named maria to be mapped well, because it lies flat against the limb.",
  "Its floor is unusually dark and level for a limb mare.",
  "Libration in longitude can swing it fully into view or hide it completely."],
 "Only at strong eastern libration, near full Moon. Low power shows a dark strip along the equatorial limb, seen nearly sideways."),

"L74": (3, "Copernican", [("Diameter", "5 km (3 mi)")], None,
 "A small crater southeast of Copernicus with a dark halo, an impact that punched through bright surface rays into darker material below and spread it around the rim. Most fresh small craters have bright halos; this one has a dark one because it dug up buried mare basalt.",
 "A lettered satellite crater of Copernicus.",
 ["It became a standard example of using a small crater as a drill core into the layers beneath.",
  "The dark halo shows best under a high sun, the opposite of most low-relief targets.",
  "It sits within the pale ejecta apron of Copernicus, which makes the contrast sharp."],
 "Day 9, southeast of Copernicus. A 150 mm scope and a moderate-to-high sun show the dark ring around the tiny pit."),

"L75": (4, "degraded; floor is Imbrian fill", [("Diameter", "16 km (10 mi)")], None,
 "A broad, shallow, saucer-like hollow on the floor of the great crater Ptolemaeus, so subtle it shows only when the sun is very low, when it appears as a faint dish in the otherwise smooth floor. It is a ghost crater, its rim nearly level with the lava-smoothed floor.",
 "A lettered satellite of Ptolemaeus, which honours Claudius Ptolemy, the second-century astronomer.",
 ["Catching it is a classic low-sun challenge, a matter of hours around local sunrise on Ptolemaeus.",
  "The floor of Ptolemaeus is also freckled with tiny craterlets that test aperture.",
  "As the sun rises the saucer fills with light and disappears."],
 "Day 8, near the central meridian, within a few hours of local sunrise on Ptolemaeus. A 150 mm scope shows the shallow dish."),

"L76": (4, "pre-Nectarian", [("Diameter", "158 km (98 mi)")], None,
 "A very large but shallow, broken crater in the far north, its rim and floor heavily overrun by Imbrium ejecta and later craters, so it barely holds its shape. At over 150 km across it is one of the larger near-side craters, yet it is easy to miss.",
 "For William Cranch Bond, the first director of Harvard College Observatory in the nineteenth century.",
 ["A rille crosses its worn floor.",
  "It sits just north of the crater Barrow, near the shore of Mare Frigoris.",
  "Its degraded state makes it nearly invisible under a high sun."],
 "Day 8, far north on the terminator, with favourable libration. A low sun shows the low ring and the floor rille."),

"L77": (3, "Imbrian or later faulting", [("Length", "~400 km (250 mi)")], None,
 "One of the longest rilles on the Moon, a graben running north to south near the west limb, cutting straight across highlands and mare alike. It stays straight over craters and ridges, the mark of a deep fault, and is radial to the debated buried Procellarum basin.",
 "From the crater Sirsalis, for Girolamo Sersale, a seventeenth-century Italian Jesuit astronomer.",
 ["It ignores the terrain it crosses, which is why it is read as a fracture rather than a channel.",
  "A magnetic anomaly runs along part of its length.",
  "Its radial trend is cited by some as evidence for a giant buried basin under Procellarum."],
 "Day 13, southwest near the limb, with favourable libration. A 100 mm scope shows the long straight cleft, best under a low sun."),

"L78": (3, "buried pre-fill crater", [("Ring", "~55 km (34 mi)")], None,
 "A ghost crater in Mare Imbrium just south of the crater Lambert, a ring of low ridges where an old crater rim pokes through the lava that buried it. Its interior is flooded to the same level as the surrounding mare.",
 "A lettered satellite of Lambert, for Johann Heinrich Lambert, the eighteenth-century Swiss polymath.",
 ["The ring is a near-perfect circle of subdued ridges, drowned to the brim.",
  "It shows how deep the Imbrium lavas ran, enough to bury a crater this size.",
  "Only the sun angle makes it appear or vanish."],
 "Day 10, Mare Imbrium south of Lambert on the terminator. A 100 mm scope at low sun shows the faint ring; it flattens out within a day or two."),

"L79": (2, "Imbrian volcanism", [("Deposit", "~90 km (56 mi)")], None,
 "The dark, nearly crater-free plain between Copernicus and the Apennines, coated on its eastern side by one of the largest dark-mantle volcanic ash deposits on the near side. The deposit is so low in reflectivity it stands out even at full Moon.",
 "Latin for the Bay of Billows, from Riccioli's 1651 map.",
 ["The dark patch is fine pyroclastic ash, not ordinary mare basalt.",
  "The region is almost untouched by later cratering.",
  "It sits in a gap in the ring of bright highlands around Copernicus."],
 "Any time the bay is lit. The dark eastern patch shows in binoculars near full Moon; a scope adds the contrast with the brighter mare to the west."),

"L80": (5, "Lower Imbrian", [("Diameter", "~930 km (580 mi)")], None,
 "The youngest and best-preserved large impact basin on the Moon, a bullseye of three mountain rings on the western limb with a small central sea. Most of it lies on the far side; from Earth its eastern rings are just glimpsed edge-on at favourable libration.",
 "Latin for the Eastern Sea, named before the 1961 convention flipped lunar east and west, so it now sits on the western limb under an eastern name.",
 ["Its rings, the Montes Rook and Montes Cordillera, are the least eroded on the Moon, a template for how all basins once looked.",
  "Lunar Orbiter 4 returned the classic overhead view of the bullseye in 1967.",
  "It is the standard against which basin structure everywhere else is measured."],
 "Day 15 or just after full Moon, with strong western libration. Low power shows the arcs of the Cordillera as a bright curved range on the limb."),

"L81": (4, "uncertain", [("Diameter", "15 km (9 mi)")], None,
 "A rare concentric crater on the southern edge of Mare Nubium, a normal-looking bowl with a smaller complete crater ring inside it, sharing the same centre. Only a few dozen concentric craters are known on the Moon, and this is the showpiece.",
 "A lettered satellite of Hesiodus, for the Greek poet Hesiod.",
 ["The inner ring may be a low lava ridge or a second impact; the cause is still argued.",
  "It sits near the Hesiodus and Pitatus craters and the Rima Hesiodus.",
  "Too low a sun fills the ring with shadow and hides the effect."],
 "Day 9, southern Nubium. A 150 mm scope and steady seeing at a moderate sun show the ring within the ring."),

"L82": (3, "Copernican", [("Diameter", "2.4 km (1.5 mi)")], None,
 "A tiny, very bright crater in western Mare Serenitatis, famous for a nineteenth-century claim that it had changed from a crater into a white spot. It had not. Spacecraft images show an ordinary small, fresh bowl inside a wide pale ejecta patch that makes it look larger.",
 "For Carl Linnaeus, the eighteenth-century Swedish botanist who founded modern biological naming.",
 ["In 1866 Johann Schmidt reported the crater had vanished, setting off decades of debate.",
  "At about 2.4 km across it is near the limit of what a small scope can resolve as a crater.",
  "The bright halo around it is the easy part; the crater itself needs aperture."],
 "A high sun, day 8 onward toward full Moon. A 100 mm scope shows it as a bright dot; 200 mm as a real crater."),

"L83": (4, "Plato is Imbrian; the floor lava is younger", [("Craterlets", "~2 km (1 mi) and smaller")], None,
 "The handful of tiny pits scattered across the smooth dark floor of the crater Plato, a traditional test of aperture and atmosphere. Plato's lava floor is one of the flattest, darkest surfaces on the near side, which is the only reason the craterlets show at all.",
 "The craterlets take their name from Plato, the crater, named for the Greek philosopher.",
 ["Four craterlets are within reach of a good 150 mm scope; more appear with aperture and seeing.",
  "The number seen on a given night is a rough measure of the seeing.",
  "The floor darkens noticeably from rim to centre, an illusion of contrast with the bright walls."],
 "Day 9, near first quarter, with the sun moderately high so Plato's floor is fully lit. Steady air matters more than aperture; try 150 to 250 mm."),

"L84": (2, "Nectarian crater, Imbrian fill", [("Diameter", "97 km (60 mi)")], None,
 "A large crater on the south shore of Mare Nubium with a lava-flooded floor, an off-centre peak, and a set of rilles running around the inside of its wall. The floor rilles formed as the flooded floor sagged and pulled away from the rim.",
 "For Pietro Pitati, a sixteenth-century Italian astronomer and calendar reformer.",
 ["Pitatus connects to the neighbouring crater Hesiodus through a break in its wall.",
  "The perimeter rilles trace a rough circle just inside the rampart.",
  "A low sun turns the floor cracks into fine dark lines."],
 "Day 9, southern Nubium on the terminator. A 100 mm scope shows the peak and the wall break to Hesiodus; 150 mm the rilles."),

"L85": (2, "Eratosthenian to early Copernican", [("Crater", "132 km (82 mi)")], None,
 "The faint, stubby ray system around the large crater Langrenus on the eastern shore of Mare Fecunditatis. Old and subdued compared with Tycho's or Copernicus's rays, it is a sign of an older bright crater, since ray brightness fades with age as the soil darkens.",
 "From the crater Langrenus, for Michael van Langren, the seventeenth-century Flemish astronomer who made the first named map of the Moon.",
 ["Langrenus itself is a fresh-looking 130 km crater with terraced walls and bright central peaks.",
  "Its rays have faded to short, patchy streaks rather than long spokes.",
  "Van Langren's 1645 map named features for royalty and saints, and almost none of his names survived."],
 "Near full Moon for the rays, day 3 or 4 for the crater under a low sun. An 80 mm scope shows the terraces and peaks."),

"L86": (4, "Imbrian volcanism", [("Extent", "~46 km (29 mi)")], None,
 "A fan of curved sinuous rilles rising from the half-buried crater Prinz on the northern edge of the Aristarchus volcanic province. Several start at small pit craters and curve north across the mare, a compact fire-fountain and lava-channel system.",
 "From the crater Prinz, for Wilhelm Prinz, a nineteenth-century Belgian selenographer.",
 ["Prinz itself is a crater open to the north, drowned by the same lavas that fed the rilles.",
  "The channels begin at vents and meander like rivers, the signature of flowing lava.",
  "The area links to the Harbinger Mountains and the wider Aristarchus Plateau."],
 "Day 11, northwest under a low sun. A 150 mm scope and good seeing show two or three of the curving channels; a hard but rewarding target."),

"L87": (4, "Nectarian", [("Diameter", "207 km (129 mi)")], None,
 "A giant crater near the southeast limb with a cluster of central peaks, a floor cut by long radial and concentric rilles, and dark pyroclastic patches near the wall. It is a floor-fractured crater on a grand scale.",
 "For Wilhelm von Humboldt, the Prussian scholar and linguist, brother of Alexander; not to be confused with Mare Humboldtianum, named for Alexander.",
 ["The floor rilles form a rough spoke-and-ring pattern from magma lifting the floor.",
  "Small dark spots near the southwest wall are volcanic ash.",
  "At about 200 km across it is one of the largest craters with such a well-developed fractured floor."],
 "Just after full Moon, with strong southeast libration. Low power shows the ring and central peaks; larger scopes hint at the floor rilles when the limb tips our way."),

"L88": (5, "pre-Nectarian", [("Diameter", "74 km (46 mi)")], None,
 "A crater sitting almost exactly at the Moon's north pole, so sunlight only ever grazes it and parts of its floor never see the sun at all. From Earth it is seen practically edge-on, at the very top of the disc.",
 "For Robert Peary, the American Arctic explorer of the early twentieth century.",
 ["Its rim holds spots of near-permanent sunlight and its floor spots of permanent shadow, both of interest for future bases.",
  "It can only be studied when libration in latitude tips the north pole toward us.",
  "The permanently shadowed floor is a candidate cold trap for ice."],
 "Only at strong northern libration. Find the polar glare on the terminator and look for the last crater before the edge; expect a thin, shadowed arc."),

"L89": (4, "Imbrian volcanism", [("Dome", "~30 km (19 mi)")], None,
 "A large, very low volcanic dome on the western edge of Mare Serenitatis, roughly heart-shaped, which is where the informal name comes from. At about 30 km across it is one of the largest domes on the near side, but so shallow it needs a knife-edge sun.",
 "An informal observers' name for its heart-like outline; it lies near the crater Linne on the west shore of Serenitatis.",
 ["A small rille runs across its top from a vent.",
  "Wrinkle ridges of the mare border it on more than one side.",
  "It is broad but only tens of metres high, so it disappears under any real light."],
 "Day 6 or 7, west Serenitatis right on the terminator. A 150 mm scope and a sun within a couple of degrees of local sunrise show the broad swelling."),

"L90": (4, "Copernican to Eratosthenian", [("Each", "~3 to 5 km (2 to 3 mi)")], None,
 "Three small craters in southern Mare Tranquillitatis named for the Apollo 11 crew, lying a few kilometres southwest of the landing site. The landing point itself, Statio Tranquillitatis, is on smooth mare with no crater to mark it.",
 "For Neil Armstrong, Buzz Aldrin and Michael Collins; the IAU named the trio in 1970.",
 ["Armstrong is about 5 km across, Aldrin and Collins about 3 km each.",
  "They sit just southwest of where the lunar module Eagle landed on 20 July 1969.",
  "Observers use the three pits to point toward a landing site that has no telescopic marker."],
 "Day 6, southern Tranquillitatis. A 150 mm scope shows the three pits in a rough line."),

"L91": (4, "Imbrian", [("Extent", "~90 km (56 mi)")], None,
 "A dense knot of intersecting rilles around the crater de Gasparis, between Mare Humorum and the southwest limb. The rilles cross at sharp angles, a sign of more than one episode of faulting in the stretched crust.",
 "From the crater de Gasparis, for Annibale de Gasparis, a nineteenth-century Italian astronomer and prolific discoverer of asteroids.",
 ["The crossing pattern is unusual for a graben set, which normally runs parallel.",
  "The system lies in the strained crust between the Humorum basin and the limb.",
  "The whole tangle fits within about 90 km."],
 "Day 12, southwest of Mare Humorum under a low sun. A 150 mm scope and steady air show two or three of the clefts and their crossings."),

"L92": (4, "Lower Imbrian", [("Length", "~47 km (29 mi)")], None,
 "A shallow, ragged valley just southeast of the disc centre near the crater Gylden, one strand of the Imbrium radial sculpture reaching almost to the middle of the Moon. It is more a linear low than a sharp trench.",
 "From the crater Gylden, for Hugo Gylden, a nineteenth-century Swedish astronomer.",
 ["It runs radial to Mare Imbrium, ploughed by debris from that basin's impact.",
  "It lies in the jumbled ground east of Ptolemaeus and Albategnius.",
  "Other Imbrium-radial grooves nearby help confirm the alignment."],
 "Day 8, near the central meridian under a low sun. A 100 mm scope shows it as a shallow gash lined up with its neighbours."),

"L93": (3, "Copernican", [("Rays", "~18 km (11 mi) crater")], None,
 "The crater Dionysius on the western edge of Mare Tranquillitatis has a rare set of dark rays, streaks that are darker than the surroundings, mixed with bright ones. Dark rays form when an impact throws dark mare material out over brighter ground.",
 "From the crater Dionysius, for Dionysius Exiguus, the sixth-century monk who devised the AD year count.",
 ["Only a few craters on the Moon show dark rays clearly.",
  "Dionysius has both light and dark rays, which makes it a natural comparison.",
  "The effect needs a high sun, like all ray systems."],
 "A high sun, day 7 onward toward full Moon. A 100 mm scope shows the crater on the Tranquillitatis shore with its odd mix of pale and dusky streaks."),

"L94": (5, "pre-Nectarian", [("Diameter", "162 km (101 mi)")], None,
 "A large crater very close to the south pole on the far southwest limb, seen almost edge-on, its interior in near-permanent deep shadow. At over 160 km across it is one of the larger south polar craters, but from Earth it is a foreshortened crescent on the limb.",
 "For Erich von Drygalski, the German geographer and polar explorer of the early twentieth century.",
 ["Its floor gets so little sun that it is a candidate cold trap for ice.",
  "Only strong southern libration brings it into view at all.",
  "Position is the achievement here; detail is minimal."],
 "Only at favourable southern libration, near full Moon. Look for the last big shadow-filled ring before the southwest edge."),

"L95": (3, "pre-Nectarian, if it is an impact at all", [("Proposed diameter", "~3,000 km (1,900 mi)")], None,
 "The proposed giant impact basin that would underlie Oceanus Procellarum and much of the near side. Its existence is debated, since no clear rings survive, and gravity data may explain the region better as cooling and cracking than as a single colossal impact.",
 "From Oceanus Procellarum, Latin for the Ocean of Storms, the largest of the dark plains.",
 ["The near side's thin crust and its concentration of maria have been offered as evidence for an early impact here.",
  "GRAIL gravity mapping revealed a rectangular pattern of buried rifts, which argues against an impact basin.",
  "If real, it would be the largest impact structure on the Moon."],
 "Nothing to see directly. Instead take in the whole sweep of Oceanus Procellarum with the naked eye or binoculars, the dark expanse the debate is about."),

"L96": (5, "pre-Nectarian", [("Feature", "south-limb rim peaks")], None,
 "The old name for the rugged peaks along the Moon's south limb, now understood as part of the rim of the vast South Pole-Aitken basin on the far side. Seen in profile at favourable libration, the highest of them jut above the smooth curve of the limb as tiny teeth.",
 "Named by nineteenth-century observers for Gottfried Wilhelm Leibniz; the IAU has retired the label, but observers still use it for the limb range.",
 ["These peaks are the near-side edge of the largest and deepest impact basin in the solar system.",
  "Most of South Pole-Aitken faces away from Earth and was only mapped from orbit.",
  "Early observers wrongly credited the range with Himalayan heights."],
 "Strong southern libration near full Moon. Watch the south limb for irregular bumps standing off the edge against black sky."),

"L97": (4, "Lower Imbrian", [("Length", "~140 km (87 mi)")], None,
 "A broad valley gouged into the southwest highlands, radial to the Orientale basin and part of that basin's ejecta sculpture. It points straight back at Orientale, cut by debris ploughing outward from that impact.",
 "From the crater Inghirami, for Giovanni Inghirami, a nineteenth-century Italian Jesuit astronomer.",
 ["It is one of several Orientale-radial valleys, with the Bouvard Valley nearby.",
  "The crater Inghirami sits at its southeastern end.",
  "Its alignment toward the limb is the clue to its origin."],
 "Day 13 or 14, southwest under a low sun with good libration. Low power shows the wide trough lined up with the Orientale rings on the limb."),

"L98": (4, "Eratosthenian (young mare)", [("Fronts", "tens of km long, only metres high")], None,
 "The low, lobed scarps in southwestern Mare Imbrium that mark the edges of separate lava flows, some of the few flow fronts on the Moon visible from Earth. They stand only ten to sixty metres high, so they show only when the sun is within a degree or two of grazing them.",
 "A descriptive term; the flows spread across Imbrium from vents to the southwest and are among the youngest mare surfaces.",
 ["They record at least three great eruptions that spread hundreds of kilometres across the basin.",
  "Because the surface is so young, little has buried the fronts.",
  "They lie near the craters Euler and La Hire."],
 "Day 9 or 10, southwest Imbrium exactly on the terminator. A 150 mm scope and the lowest possible sun show the flows as faint ribbon-edged steps; a timing-critical target."),

"L99": (5, "very young, possibly tens of millions of years", [("Diameter", "~3 km (2 mi)"), ("Depth", "~60 m (200 ft)")], None,
 "A tiny, D-shaped depression in Lacus Felicitatis with a bright, blocky floor and sharp edges, so young-looking it may be one of the most recent volcanic features on the Moon. Its floor looks almost uncratered, hinting at an age far younger than the billions-of-years-old mare around it.",
 "Ina is a given name assigned by the IAU; the feature is often called the Ina caldera, or the D-caldera.",
 ["Ideas for it range from a late small eruption to slow outgassing collapsing the surface.",
  "It was first noticed on Apollo 15 orbital photographs.",
  "It sits near the Triesnecker and Hyginus rille fields."],
 "Effectively impossible for a visual telescope at 3 km on the floor of a small lake. Included as a know-it-is-there object near the central rille country."),

"L100": (5, "surface marking", [("Swirls", "tens of km across")], None,
 "Pale, looping albedo markings on Mare Marginis, right on the eastern limb. Like Reiner Gamma, these are flat swirls tied to a magnetic anomaly, and this one lies roughly opposite the young Orientale basin.",
 "From Mare Marginis, Latin for the Sea of the Edge, named for its position on the limb.",
 ["The swirls sit near a magnetic anomaly that is roughly antipodal to Orientale, supporting the idea that big impacts focus effects at their antipodes.",
  "Mare Marginis lies almost exactly on the limb, so the swirls are foreshortened to near nothing.",
  "The mare itself is patchy and thin, not a deep flood."],
 "Strong eastern libration near full Moon. Even then the swirls are at the threshold; low power shows Mare Marginis as a grey patch on the edge, and the swirls need photographs."),
}

# ------------------------------------------------------------------ rewrite
def js_size(rows):
    return "[" + ", ".join('{ label:"%s", value:"%s" }' % (l, v) for l, v in rows) + "]"

def js_facts(fs):
    return "[\n" + ",\n".join('      "%s"' % f for f in fs) + "\n    ]"

HEAD_RE = re.compile(r'^\s*\{ id:"(L\d+)",\s*zone:"([^"]*)",\s*cat:"([^"]*)",\s*alt:"([^"]*)",\s*dSeed:(\d+),\s*status:"stub",\s*$')

def main():
    dry = "--dry-run" in sys.argv
    lon = spine_lon()
    lines = open(CARDS).read().split("\n")
    out, i, done = [], 0, []
    while i < len(lines):
        m = HEAD_RE.match(lines[i])
        if not m or m.group(1) not in C:
            out.append(lines[i]); i += 1; continue
        cid, zone, cat, alt, dseed = m.groups()
        # gather block image fields until the outline-closing line
        blk = [lines[i]]; j = i + 1
        while j < len(lines) and not re.match(r'^\s*outline:\{.*\}\s*\},(\s*//.*)?\s*$', lines[j]):
            blk.append(lines[j]); j += 1
        blk.append(lines[j])           # outline line
        text = "\n".join(blk)
        def grab(key):
            mm = re.search(r'\b%s:("(?:[^"\\]|\\.)*")' % key, text)
            return mm.group(1) if mm else '""'
        photo, ptag, pcred = grab("photo"), grab("photoTag"), grab("photoCredit")
        loc, lcred = grab("locator"), grab("locatorCredit")
        om = re.search(r'outline:\{[^}]*\}', text)
        outline = om.group(0) if om else 'outline:{ shape:"ellipse", cx:50, cy:50, rx:6, ry:6 }'
        diff, epoch, size, depth, desc, origin, facts, tips = C[cid]
        bd = best_days(lon[cid])
        nb = []
        nb.append('  { id:"%s", zone:"%s", cat:"%s", alt:"%s", dSeed:%s, diff:%d, status:"draft",'
                  % (cid, zone, cat, alt, dseed, diff))
        nb.append('    epoch:"%s",' % epoch)
        nb.append('    size:%s,' % js_size(size))
        if depth:
            nb.append('    depth:"%s",' % depth)
        nb.append('    bestDays:[[%d,%d],[%d,%d]],' % (bd[0][0], bd[0][1], bd[1][0], bd[1][1]))
        nb.append('    %s,' % photo_kv("photo", photo))
        nb.append('    %s,' % photo_kv("photoTag", ptag))
        nb.append('    %s,' % photo_kv("photoCredit", pcred))
        nb.append('    %s,' % photo_kv("locator", loc))
        nb.append('    %s,' % photo_kv("locatorCredit", lcred))
        nb.append('    %s,' % outline)
        nb.append('    description:"%s",' % desc)
        nb.append('    nameOrigin:"%s",' % origin)
        nb.append('    facts:%s,' % js_facts(facts))
        nb.append('    tips:"%s" },' % tips)
        out.extend(nb)
        done.append(cid)
        i = j + 1
    if not dry:
        open(CARDS, "w").write("\n".join(out))
    print(("DRY " if dry else "") + "rewrote %d cards: %s .. %s"
          % (len(done), done[0] if done else "-", done[-1] if done else "-"))
    miss = [k for k in C if k not in done]
    if miss:
        print("NOT FOUND:", ", ".join(sorted(miss, key=lambda s: int(s[1:]))))

def photo_kv(key, quoted):
    return '%s:%s' % (key, quoted)

if __name__ == "__main__":
    main()
