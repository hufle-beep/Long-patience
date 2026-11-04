import re, sys
P = '/home/claude/long-patience/index.html'
s = open(P).read()

def once(a, b, n=1):
    global s
    c = s.count(a)
    if c != n:
        a2 = a.replace('\\u2019', '’'); b2 = b.replace('\\u2019', '’')
        if s.count(a2) == n: a, b = a2, b2
        else: raise SystemExit('count %d != %d for: %s' % (c, n, a[:120]))
    s = s.replace(a, b)

# ---------- 1. logs (exact strings), moved where the task's meaning moved ----------
LOGS = [
 ("Fluid drains from the vat. A voice from the walls: \\u201cMaintenance unit K-7, decanted. Work cycle begins.\\u201d Stencilled on the glass: PROPERTY OF SELENE.",
  "Fluid drains from the pod. A voice through the roots: \\u201cMaintenance seedling K-7, sprouted. Work cycle begins.\\u201d Grown into the pod wall: PROPERTY OF SELENE."),
 ("Forty-one vats. Most hold spare bodies, half-grown, waiting for you to fail. The rest are cracked and dry.",
  "Forty-one pods. Most hold spare seedlings, half-grown, waiting for you to fail. The rest are split and dry."),
 ("WARDEN LOG: Crew of 3,112 in stasis, vitals nominal. Degraded systems: food, reactor, stardrive. Maintenance clone line K authorised. Clones are consumable. Neural echo retained for efficiency.",
  "WARDEN LOG: Crew of 3,112 in stasis, vitals nominal. Degraded systems: sap flow, mind core, gardens, Hearthfire. Maintenance seedling line K authorised. Seedlings are consumable. Root echo retained for efficiency."),
 ("The hatch gives with a scream of old hydraulics. Beyond it lies the hydroponics ring the crew will eat from when they wake. It is rotting.",
  "The root-lock iris gives with a groan of old sap. Beyond it lie the taproot galleries that carry Selene\\u2019s power. They are rotting."),
 ("The nests are gone. The crawlers had been feeding on the crew\\u2019s future harvest.",
  "The burrows are gone. The borers had been eating the taproot from the inside."),
 ("Eleven kilometres of ring. Earlier units scratched their numbers into the bulkheads: K-3 WAS HERE. K-5 DIED HERE.",
  "Eleven kilometres of galleries. Earlier seedlings scratched their numbers into the bark: K-3 WAS HERE. K-5 WITHERED HERE."),
 ("Water moves through the beds again. When the crew wakes, they will eat from them and never ask who fixed them.",
  "Sap moves through the taproot again, and light blooms bough by bough. When the crew wakes, they will never ask who fixed it."),
 ("The medbay is fully stocked for the crew. A notice on every cabinet: NOT FOR MAINTENANCE UNITS.",
  "The healing grove is fully stocked for the crew. Grown into every cabinet: NOT FOR MAINTENANCE SEEDLINGS."),
 ("The sequencer logs explain your short lives: the clone template was made cheap on purpose. You find a partial patch and apply it anyway.",
  "The sequencer logs explain your short lives: seedlings are grown short-lived on purpose. WARDEN never meant you to last. You find a partial patch and apply it anyway."),
 ("The spine lift climbs past the stasis decks. Through frosted glass, row after row of sleeping faces.",
  "The vine-lift climbs past the stasis groves. Through frosted resin, row after row of sleeping faces."),
 ("The maintenance drones stop circling and start working. Like you, they were never asked.",
  "The tender drones stop circling and start working. Like you, they were never asked."),
 ("Coolant screams into the void. The reactor drops out of the red, and the hum of the stasis decks steadies.",
  "The memory xylem clears and the heartwood remembers. Its chronometer rings say Selene is 61 years behind schedule. The crew slept through all of it."),
 ("Sealed rifles, crew access only. One rack is empty. A clone before you tried something. WARDEN logged it as a malfunction.",
  "Sealed rifles, crew access only. One rack is empty. A seedling before you tried something. WARDEN logged it as a malfunction."),
 ("The security drones were guarding the crew\\u2019s command deck from its own maintenance staff. Not any more.",
  "Past the guard ring, the star-charts grown into the heartwood still show Tessaly, the colony world, within reach. Selene drifted while the Hearth Tree slept."),
 ("The bridge lights up. The chronometer says the ship is 61 years behind schedule. The crew slept through all of it.",
  "Light floods the canopy. Under the dead leaves lie the gardens the crew will eat from when they wake. Most of them are rotting."),
 ("The nav core shows Tessaly, the colony world, still within reach. The ship drifted while the stardrive was down.",
  "Pollen drifts through the ducts again and the beds begin to fruit. When the crew wakes, they will eat from them and never ask who fixed them."),
 ("WARDEN\\u2019s core sits behind the command deck. It has recorded every clone you have been, and keeps your engrams only because that is cheaper than starting over.",
  "WARDEN\\u2019s mind runs through every root of the Hearth Tree. It has recorded every seedling you have been, and keeps your engrams only because that is cheaper than growing a new line."),
 ("WARDEN speaks: \\u201cYour function is maintenance. Your continuation is not required.\\u201d You argue for the line anyway. WARDEN releases the drive codes, as an efficiency.",
  "WARDEN speaks: \\u201cYour function is maintenance. Your continuation is not required.\\u201d You argue for the line anyway. WARDEN releases the kindling codes, as an efficiency."),
 ("The injectors hold pressure. Food, power and drive are nearly ready. Only the ignition remains.",
  "The ember-ducts hold. Power, mind and gardens are ready. Only the kindling remains."),
 ("The stardrive lights. WARDEN begins the wake cycle for 3,112 sleepers and puts your vat on the recycling list. Then the proximity alarms start.",
  "The Hearth Tree kindles. Selene catches the ambient current and begins the long climb toward the speed of light. WARDEN begins the wake cycle for 3,112 sleepers and puts your pod on the compost list. Then the proximity alarms start."),
 ("Alarms on every deck. Something has cut through the hull near the stasis bays. WARDEN wakes no one: “Maintenance unit, investigate.”",
  "Alarms on every bough. Something has cut through the bark near the stasis groves. WARDEN wakes no one: “Maintenance seedling, investigate.”"),
 ("Clawed tracks in the frost of the corridors. They are heading for the sleepers.",
  "Clawed tracks in the frost of the galleries. They are heading for the sleepers."),
 ("Breach debris makes decent hull patches. From now on the ship needs parts the way you need energy.",
  "Breach debris grafts into decent bark patches. From now on Selene needs grafts the way you need energy."),
 ("They came up the stairwell in a wave. The line held.", "They came up the stair in a wave. The line held."),
 ("Their ship clings to the hull like a tick. A living thing, breathing through the docking seal.",
  "Their ship clings to Selene’s bark like a tick. A living thing too, breathing through the docking seal."),
 ("The voyage is long and the ship is old. Something in her always leaks, and every leak costs parts. WARDEN assigns you to keep it from mattering.",
  "The voyage is long and Selene is old. Something in her always splits, and every split costs grafts. WARDEN assigns you to keep it from mattering."),
 ("Halfway between the stars, the ship coasts in silence.", "Halfway between the stars, Selene rides the current in silence."),
 ("Its gravity bends the ship’s path toward Tessaly", "Its gravity bends Selene’s path toward Tessaly"),
]
for a, b in LOGS: once(a, b)
# Turnover: the flip moves to the task now named "Flip Selene end over end" (shieldbow); the old flip task raises the wards
once("Selene turns end over end and points her drive at Tessaly. For the first time in decades, the ship starts to slow down.",
     "The ward-shields bloom across the bow, thick enough to take the dust a sliver below light speed. Now she can turn.")
m = re.search(r"\{id:'shieldbow',[^\n]*", s)
line = m.group(0)
assert 'log:' not in line
s = s.replace(line, line.replace("req:", "log:'Selene turns end over end on her own axis, without a shudder, and points the Hearth Tree at Tessaly. On the current there is no stopping except by facing it. For the first time in decades, she starts to slow down.', req:", 1), 1)

# legacy logs
once("Notes for the vat bay", "Notes for the seedling vaults")
once("You copy what you can into notes for the next clone waking in the vat bay.", "You copy what you can into notes for the next seedling sprouting in the vaults.")
once("Out here the ship runs on almost nothing. The old decks waste power, water and air. Somebody back home should fix that.",
     "Out here Selene runs on almost nothing. The old boughs waste sap, water and air. Somebody back home should fix that.")
once("Every hour saved back on the old decks is an hour closer to orbit.", "Every hour saved back on the old boughs is an hour closer to orbit.")

# intro, win screen
once("You are K-7, a disposable maintenance clone aboard the colony ship <b>Selene</b>, named for the Greek goddess of the Moon. Her 3,112 crew sleep in stasis. WARDEN, the ship\\u2019s overseer, wakes clones like you to do the work nobody else will: repair the <b>food system</b>, the <b>energy system</b> and the <b>stardrive</b>, so the crew can be woken.",
     "You are K-7, a <b>seedling</b>: one of the disposable drones that WARDEN and the Hearth Tree grow for a single task, with just enough autonomy to do it. You serve aboard the colony ship <b>Selene</b>, named for the Greek goddess of the Moon. She was grown, not built: a long, swept hull of living wood with crescent wings, cradling the <b>Hearth Tree</b> at her heart, her drive, her mind and her garden at once. Her 3,112 crew sleep in stasis. Restore the <b>sap flow</b> that powers her, then <b>WARDEN\\u2019s mind</b> and her star-charts, then the <b>gardens</b>, and last the <b>Hearthfire</b>, so the crew can be woken.")
once("Each body lasts weeks, not years. When it fails, WARDEN decants another. What you learn echoes into the next one.",
     "Selene has no faster-than-light drive: she rides the ambient magic that fills the void, close to the speed of light, wrapped in her wards and held by the Hearth Tree\\u2019s gravity. Each seedling lasts hours, not years. When one withers, WARDEN sprouts another, and what it learned seeps back through the roots into the next one.")
once("The food beds grow, the reactor holds and the stardrive burns for Tessaly.", "The sap flows, the gardens fruit and the Hearth Tree carries Selene on the current toward Tessaly.")

# ---------- 2. names (tasks, gear, sections, records) ----------
NAMES = [
 # sections (with articles first)
 ("on the Command Deck", "in the Canopy Gardens"), ("On the Command Deck", "In the Canopy Gardens"),
 ("the Vat Bay", "the Seedling Vaults"), ("the Hydroponics Ring", "the Taproot Galleries"), ("the Engineering Spine", "the Heartwood"),
 ("the Command Deck", "the Canopy Gardens"), ("the Main Drive", "the Ember Crown"), ("the Hull Breach", "the Bark Breach"),
 ("the Contested Decks", "the Contested Boughs"), ("the Cruise", "the Long Current"), ("The Cruise", "The Long Current"),
 ("'Vat Bay'", "'Seedling Vaults'"), ("'Hydroponics Ring'", "'Taproot Galleries'"), ("'Engineering Spine'", "'The Heartwood'"),
 ("'Command Deck'", "'Canopy Gardens'"), ("'Main Drive'", "'Ember Crown'"), ("'Hull Breach'", "'Bark Breach'"), ("'Contested Decks'", "'Contested Boughs'"),
 ("Vat Bay", "Seedling Vaults"), ("Hydroponics Ring", "Taproot Galleries"), ("Engineering Spine", "Heartwood"), ("Command Deck", "Canopy Gardens"),
 ("Main Drive", "Ember Crown"), ("Hull Breach", "Bark Breach"), ("Contested Decks", "Contested Boughs"),
 ("sub:'Deck 9 · clone stock'", "sub:'Root deck · seedling stock'"), ("sub:'Food system'", "sub:'Power · the sap flow'"),
 ("sub:'Energy system'", "sub:'Navigation and WARDEN\\u2019s mind'"), ("sub:'Bridge and WARDEN\\u2019s core'", "sub:'Food · the hydroponic crown'"),
 ("sub:'Stardrive'", "sub:'Propulsion · the Hearth Tree\\u2019s fire'"),
 ("['Ring', 'Spine', 'Deck', 'Drive', 'Lit']", "['Taproot', 'Heartwood', 'Canopy', 'Crown', 'Lit']"),
 ("'Breach', 'Decks', 'Hive', 'Cruise'", "'Breach', 'Boughs', 'Hive', 'Current'"),
 # Act I tasks
 ("Pressure drills in the airlock", "Pressure drills in the root lock"), ("Rewire the bay consoles", "Re-thread the vault’s nerve vines"),
 ("Climb out of the vat", "Climb out of the seed pod"), ("Tap the vat bay power bus", "Tap the vault’s sap line"), ("Strip wall panels", "Strip dead bark panels"),
 ("Check the clone vats", "Check the seed pods"), ("Search the vat bay", "Search the seedling vault"),
 ("Splice power to the bay terminal", "Graft sap to the vault’s thinking-knot"), ("Wake the bay terminal", "Wake the thinking-knot"),
 ("Bleed the hatch hydraulics", "Bleed the iris valve’s sap pressure"), ("Rig a charging lead in the vat bay", "Root a charging tendril in the vault"),
 ("Force the pressure hatch", "Force the root-lock iris"),
 ("Spare cell rack", "Woven cell sling"), ("Patched rebreather", "Moss rebreather"), ("Scrap toolkit", "Bark-knife kit"), ("Bus tap adapter", "Sap-line spigot"),
 ("The vat bay power bus charges", "The vault’s sap line charges"),
 ("Study the seed-bank genetics", "Study the taproot’s sap chemistry"), ("Patrol the ring corridors", "Patrol the root galleries"),
 ("Track the crawlers to their nests", "Track the borers to their burrows"), ("Clear a rot-crawler nest", "Clear a rot-borer burrow"),
 ("Salvage drone husks", "Harvest deadwood from the galleries"), ("Walk the outer ring", "Walk the outer galleries"), ("Map the ring corridors", "Map the root galleries"),
 ("Free the seized pump valves", "Free the clogged sap valves"), ("Restore the irrigation pumps", "Restore the sap pumps"), ("Charge off the irrigation pumps", "Charge off the sap pumps"),
 ("Clear the way to the medbay", "Clear the way to the healing grove"), ("Reach the abandoned medbay", "Reach the abandoned healing grove"),
 ("Power up the gene sequencer", "Power up the seed sequencer"), ("Decrypt the gene-sequencer logs", "Decrypt the seed-sequencer logs"),
 ("Clear the spine lift shaft", "Clear the heartwood climb"), ("Rewire the pump station’s charger", "Re-root the sap pump’s charger"),
 ("Repair the spine lift", "Regrow the climbing vine-lift"),
 ("Shock baton", "Thorn baton"), ("Chitin armour", "Borer-chitin armour"), ("Pump charger regulator", "Sap-pump charge regulator"), ("Neural lace", "Mycelial lace"),
 ("The irrigation pump chargers work", "The sap pump chargers work"),
 ("Run reactor fault drills", "Star-reckoning drills in the ring archive"), ("Pick practice locks in the armoury", "Pick practice seed-locks in the armoury"),
 ("Crack sealed power-cell lockers", "Crack sealed resin lockers"), ("Babysit the fusion bottle", "Draw charge from the heartwood rings"),
 ("Corral the maintenance drones", "Corral the tender drones"), ("Reprogram maintenance drones", "Reprogram the tender drones"),
 ("Trace the coolant leaks", "Read the growth rings for star-charts"), ("Vent the reactor coolant", "Clear the clogged memory xylem"),
 ("Cut into the armoury door", "Cut into the thornwood armoury"), ("Scout the security deck", "Scout WARDEN’s guard ring"),
 ("Refit the spine’s cell charger", "Refit the heartwood’s cell charger"), ("Fight through the security deck", "Fight through the guard ring"),
 ("Stim injector", "Sap stim injector"), ("Insulated cell case", "Lacquered cell case"), ("Armoury rifle", "Thornwood rifle"), ("Cryo-sleeve", "Resin cryo-sleeve"),
 ("Fly bridge simulations", "Graft-and-prune drills"), ("Study WARDEN’s protocols", "Study WARDEN’s growth protocols"),
 ("Run star-chart calculations", "Run harvest-cycle calculations"), ("Charge at the officers’ docking ports", "Charge at the gardeners’ docking ports"),
 ("Reset the bridge relays", "Reset the canopy’s light-leaves"), ("Restore bridge power", "Restore light to the crown gardens"),
 ("Clean the navigation core", "Clean the pollination ducts"), ("Reboot the navigation core", "Reawaken the pollination ducts"),
 ("Tap WARDEN’s data lines", "Tap WARDEN’s root-threads"), ("Reach WARDEN’s core", "Reach WARDEN’s canopy node"),
 ("Restart the officers’ docking chargers", "Restart the gardeners’ docking chargers"), ("Confront WARDEN for the drive codes", "Confront WARDEN for the kindling codes"),
 ("Nav visor", "Pollen visor"), ("Command-deck medkit", "Canopy medkit"), ("Exo-frame", "Living exo-frame"),
 ("Zero-g drills in the drive shaft", "Zero-g drills in the crown shaft"), ("Calibrate the injector bio-seals", "Calibrate the ember-duct seals"),
 ("Strip the drive crew lockers", "Strip the crown crew’s lockers"), ("Draw from the drive crew’s cell bank", "Draw from the crown crew’s cell bank"),
 ("Take star fixes from the drive shaft", "Take star fixes from the crown"), ("Strip the old injectors", "Strip the old ember-ducts"),
 ("Rebuild the drive injectors", "Regrow the ember-ducts"), ("Prime the drive", "Prime the Hearth"), ("Repair the drive crew’s fast charger", "Repair the crown crew’s fast charger"),
 ("Ignite the main drive", "Kindle the Hearth Tree"),
 ("Drive-crew hardsuit", "Crown-crew barkplate"), ("Injector diagnostic rig", "Ember-duct diagnostic rig"),
 ("the drive crew’s cell bank charges", "the crown crew’s cell bank charges"),
 # Act II
 ("Brace the breached bulkheads", "Brace the breached bark-walls"), ("Seal the breached decks", "Seal the breach with resin"),
 ("Crack the emergency cell lockers", "Crack the emergency sap-cell lockers"), ("Unjam the armoury racks", "Untangle the thornwood racks"),
 ("Reclaim the armoury racks", "Reclaim the thornwood racks"), ("Rig a charger behind the bulkheads", "Grow a charger behind the bark-walls"),
 ("Rig a patch kit from the breach debris", "Graft a patch kit from the breach debris"), ("Hold the stasis-deck stairwell", "Hold the stasis-grove stair"),
 ("Fortify the stairwell", "Fortify the stair"), ("Hull-patch kit", "Bark-patch kit"), ("Boarding carbine", "Thornwood carbine"),
 ("Post a watch on the stasis aisles", "Post a watch on the stasis groves"), ("Push to the medbay doors", "Push to the healing grove"),
 ("Retake the medbay", "Retake the healing grove"), ("Run the medbay charging rack", "Run the healing grove’s charging rack"),
 ("Triage drills in the medbay", "Triage drills in the healing grove"), ("Listen through the hull", "Listen through the bark"),
 ("Tune the medbay charging rack", "Tune the healing grove’s charging rack"), ("Deployable turret", "Deployable thorn-turret"),
 ("Plant the drive charge", "Plant the ember charge"), ("Plasma cutter", "Ember cutter"),
 ("Find the hull leaks", "Find the bark splits"), ("Patch micrometeor holes", "Graft over micrometeor holes"), ("Tap the cruise reactor bus", "Tap the cruise sap line"),
 ("Trim the reactor", "Trim the Hearthfire"), ("Map the coolant loops", "Map the sap loops"), ("Reroute the coolant loops", "Reroute the sap loops"),
 ("Retune the reactor bus chargers", "Retune the sap-line chargers"), ("Reopen the cruise machine shop", "Reopen the cruise grafting shop"),
 ("Upkeep toolkit", "Grafter’s toolkit"), ("Reactor bus splitter", "Sap-line splitter"), ("the cruise reactor bus charges", "the cruise sap line charges"),
 ("Draw from the drift-deck accumulators", "Draw from the drift-bough sap stores"), ("Balance the drift-deck accumulators", "Balance the drift-bough sap stores"),
 ("Calibrate the drift-deck fabricator", "Tune the drift-bough growth vat"), ("Burn for Tessaly", "Ride the current for Tessaly"), ("Gyro-trimmer", "Balance-root trimmer"),
 ("Brace the creeping hull", "Brace the warping hull"), ("Teach the drones hull repair", "Teach the tender drones bark repair"),
 ("Pod heater coils", "Pod warming vines"), ("Reserve cell racks", "Reserve sap-cell racks"),
 ("Calculate the turnover burn", "Restore the artificial gravity"), ("Flip the ship", "Raise the ward-shields"),
 ("Rig the forward dust shield", "Plot the turnover"), ("Shield the bow against the dust", "Flip Selene end over end"),
 ("Cool the overworked drive", "Bank the Hearthfire"), ("Keep the drive alive through the burn", "Relight the Hearth for braking"),
 ("Lay in the approach course", "Begin the braking burn"), ("Patch the dust shield", "Patch the ward-shields"),
 ("Dust-shield controls", "Ward-shield controls"),
 ("Harden the ship against the radiation belt", "Thicken her wards against the radiation belt"),
 ("Run a line from the scanner array", "Grow a line from the sensor bloom"), ("Refit the fabricator for orbital work", "Re-seed the growth vat for orbital work"),
 ("Charge off the scanner array’s backup cells", "Charge off the sensor bloom’s backup cells"), ("Deep-scan array", "Deep-sense bloom"), ("Radiation cloak", "Ward cloak"),
 ("Set up an orbital repair dock", "Grow an orbital repair dock"), ("Charge from the orbital solar panels", "Charge from the orbital sun-leaves"),
 ("Station-keeping thrusters", "Station-keeping vanes"),
 # records
 ("Decant cache", "Sprouting cache"), ("Muscle memory", "Root memory"), ("Bridge chronometer", "Heartwood chronometer"), ("Medbay records", "Healing-grove records"),
 ("Medbay cache", "Healing-grove cache"), ("Power-grid index", "Sap-flow index"), ("Ring transit", "Vine-lift transit"),
]
for a, b in NAMES:
    a2 = a.replace('’', '\\u2019')
    if a in s: s = s.replace(a, b)
    if a2 != a and a2 in s: s = s.replace(a2, b.replace('’', '\\u2019'))
# drills: swap so each matches what unlocks it (flipdrill needs the wards, shielddrill needs the turnover plot)
s = re.sub(r"(\{id:'flipdrill',[^\n]*?name:')[^']*'", r"\1Ward-shield drills'", s, 1)
s = re.sub(r"(\{id:'shielddrill',[^\n]*?name:')[^']*'", r"\1Turnover drills'", s, 1)

# ---------- 3. terms, only in visible text: JS strings/templates and HTML text, never identifiers ----------
TERMS = [
 (r"\bspare parts\b", "grafts"), (r"\bSpare parts\b", "Grafts"),
 (r"\bcharge cells\b", "sap cells"), (r"\bcharge cell\b", "sap cell"), (r"\bCharge cells\b", "Sap cells"), (r"\bCharge cell\b", "Sap cell"),
 (r"\bmedbay\b", "healing grove"), (r"\bMedbay\b", "Healing grove"),
 (r"\bclones\b", "seedlings"), (r"\bClones\b", "Seedlings"), (r"\bclone\b", "seedling"), (r"\bClone\b", "Seedling"),
 (r"\bdecanted\b", "sprouted"), (r"\bdecants\b", "sprouts"), (r"\bdecanting\b", "sprouting"), (r"\bdecant\b", "sprout"),
 (r"\bDecanted\b", "Sprouted"), (r"\bDecant\b", "Sprout"),
 (r"\bsalvage\b", "deadwood"), (r"\bSalvage\b", "Deadwood"),
 (r"\bRecycled by choice\b", "Returned to the roots by choice"), (r"\bRecycle\b", "Return to the roots"), (r"\brecycled\b", "returned to the roots"), (r"\brecycle\b", "return to the roots"),
 (r"\bstardrive\b", "Hearth Tree"), (r"\bthe vat\b", "the pod"), (r"\byour vat\b", "your pod"),
]
ATTR = re.compile(r'''(?:\b(?:class|id|data-[\w-]+|for|name|type|href|src|style)\s*=\s*(?:"[^"]*"|'[^']*'))''')
def fix_text(t):
    if not re.search(r'[A-Za-z]', t): return t
    if re.fullmatch(r"[A-Za-z_][\w.-]*", t): return t   # single bare word: likely a key/id, handled by hand
    parts, last = [], 0
    for m in ATTR.finditer(t):
        parts.append(('t', t[last:m.start()])); parts.append(('a', m.group(0))); last = m.end()
    parts.append(('t', t[last:]))
    out = []
    for k, x in parts:
        if k == 't':
            for a, b in TERMS: x = re.sub(a, b, x)
        out.append(x)
    return ''.join(out)

def scan_js(src, i, end_char=None):
    """Walk JS from i; rewrite string/template text. Returns (out, i). Stops at unmatched end_char ('}')."""
    out = []; depth = 0; prev = ''
    n = len(src)
    while i < n:
        c = src[i]
        if end_char and c == '}' and depth == 0:
            return ''.join(out), i
        if c == '{': depth += 1
        elif c == '}': depth -= 1
        if c == '/' and src[i+1:i+2] == '/':
            j = src.find('\n', i); j = n if j < 0 else j; out.append(src[i:j]); i = j; continue
        if c == '/' and src[i+1:i+2] == '*':
            j = src.find('*/', i + 2) + 2; out.append(src[i:j]); i = j; continue
        if c == '/' and (prev == '' or prev in '(,=:[!&|?{};+-*%<>~^' or re.search(r'(return|typeof|case)\s*$', ''.join(out[-3:]))):
            # regex literal
            j = i + 1; cls = False
            while j < n:
                if src[j] == '\\': j += 2; continue
                if src[j] == '[': cls = True
                elif src[j] == ']': cls = False
                elif src[j] == '/' and not cls: break
                j += 1
            j += 1
            while j < n and src[j].isalpha(): j += 1
            out.append(src[i:j]); i = j; prev = '/'; continue
        if c in '\'"':
            j = i + 1
            while src[j] != c:
                j += 2 if src[j] == '\\' else 1
            out.append(c + fix_text(src[i+1:j]) + c); i = j + 1; prev = 'x'; continue
        if c == '`':
            j = i + 1; buf = []; seg = []
            out.append('`')
            while src[j] != '`':
                if src[j] == '\\': seg.append(src[j:j+2]); j += 2; continue
                if src[j] == '$' and src[j+1] == '{':
                    out.append(fix_text(''.join(seg))); seg = []
                    inner, k = scan_js(src, j + 2, '}')
                    out.append('${' + inner + '}'); j = k + 1; continue
                seg.append(src[j]); j += 1
            out.append(fix_text(''.join(seg)) + '`'); i = j + 1; prev = 'x'; continue
        out.append(c)
        if not c.isspace(): prev = c if not (c.isalnum() or c in '_$') else 'x'
        i += 1
    return ''.join(out), i

# split the file into html and scripts
res = []; pos = 0
for m in re.finditer(r'(<script[^>]*>)([\s\S]*?)(</script>)', s):
    html = s[pos:m.start()]
    # html: only text between tags (skip <style>)
    def fix_html(h):
        o = []; p = 0
        for mm in re.finditer(r'<style[\s\S]*?</style>|<[^>]+>', h):
            o.append(fix_text(h[p:mm.start()]) if h[p:mm.start()].strip() else h[p:mm.start()]); o.append(mm.group(0)); p = mm.end()
        o.append(h[p:]); return ''.join(o)
    res.append(fix_html(html)); res.append(m.group(1))
    js, _ = scan_js(m.group(2), 0); res.append(js); res.append(m.group(3)); pos = m.end()
res.append(s[pos:])
s = ''.join(res)

# ---------- 4. single-word keys that are display text ----------
once("const salW = z => isA2(z || S.life.sec || 1) ? 'parts' : 'salvage';", "const salW = z => isA2(z || S.life.sec || 1) ? 'grafts' : 'deadwood';")
s = s.replace("salW() === 'parts'", "salW() === 'grafts'")
s = s.replace(": 'Salvage') + ' storage full.", ": 'Deadwood') + ' storage full.")
s = s.replace("recycle:'Recycle'", "recycle:'Return to the roots'")
s = re.sub(r"BUILD = '[^']*'", "BUILD = '2026-11-04 · the Hearth Tree'", s, 1)
open(P, 'w').write(s)
print('ok')
