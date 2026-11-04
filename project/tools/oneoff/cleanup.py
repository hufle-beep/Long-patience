import re
P = '/home/claude/long-patience/index.html'
s = open(P).read()
def once(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:100])
    s = s.replace(a, b)

# ---- 1. patch ('rest') tasks: definitions, the startup splice, and every branch that handled them
s, k = re.subn(r"\n  \{id:'[a-z]+', z:\d+, kind:'rest',[^\n]*", "", s)
assert k == 14, k
once("for (let i = TASKS.length - 1; i >= 0; i--) if (TASKS[i].kind === 'rest') TASKS.splice(i, 1);   // the fault is gone, and with it the patches\n", "")
once("t.kind === 'train' ? TRAIN_CAP : t.kind === 'rest' ? 1 : (t.reps || 1); }", "t.kind === 'train' ? TRAIN_CAP : (t.reps || 1); }")
once("if (t.cross || t.kind === 'rest' || !isAuto(t)", "if (t.cross || !isAuto(t)")
once(": (t.kind === 'rest' || complete(t))) continue;", ": complete(t)) continue;")
once("      else if (t.kind === 'rest') { rank = 3; run = () => t; }   // rests are worth more later in a life\n", "")
once("!['job', 'rest'].includes(T[x].kind)", "T[x].kind !== 'job'")
once("t.kind === 'train' ? TRAIN_CAP : t.kind === 'rest' ? 1 : (t.reps || 1); if ((P[t.id]", "t.kind === 'train' ? TRAIN_CAP : (t.reps || 1); if ((P[t.id]")
once("    const rests = zt.filter(t => t.kind === 'rest' && vis.includes(t.id));\n", "")
once("!acts.length && !rests.length && !trains.length", "!acts.length && !trains.length")
once("const left = t.kind === 'rest' ? (t.days - (L.prog[t.id] || 0)) / sp : (t.days * (t.reps", "const left = (t.days * (t.reps")
once("<g class=\"mn${t.kind === 'rest' ? ' rest' : t.kind === 'train' ? ' train' : ''}\"", "<g class=\"mn${t.kind === 'train' ? ' train' : ''}\"")
once("!av ? 'locked' : t.kind === 'rest' ? 'rest · ' + fmtDays((t.days - (L.prog[t.id] || 0)) / sp)\n      : (t.reps", "!av ? 'locked'\n      : (t.reps")
once("['job','act','train','rest'].forEach(k =>", "['job','act','train'].forEach(k =>")
once("const KIND_LABEL = {job:'Job', act:'Action', train:'Training', rest:'Patch'};", "const KIND_LABEL = {job:'Job', act:'Action', train:'Training'};")
assert "'rest'" not in s, [m.start() for m in re.finditer("'rest'", s)]

# ---- 2. unused functions and styles
once("const ngpFree = () => Math.max(0, ngpPts() - ngpSpent());\n", "")
once("const lifeDays = () => Infinity;   // no lifespan limit\n", "")
once("function checkKit(){ const pr = S.pr || {}; if (!pr.kit && S.won) { pr.kit = true; HOOK.kit(); } }   // Quartermaster's cache: from the first lit drive\n", "")
s = re.sub(r"function fmtSecs\(s\)\{\n[\s\S]*?\n\}\n", "", s, count=1)
s = re.sub(r"function twoStep\(b, key, label\)\{\n[\s\S]*?\n\}\n", "", s, count=1)
once("const armed = {};\n", "")
i = s.index("function masteryTxt(t){"); j = s.index("\n}\n", i) + 3; s = s[:i] + s[j:]
for rule in [r"\.chip\{[^}]*\}\n", r"\.tp\{[^}]*\}\n", r"\.tp\.open\{[^}]*\}\n", r"\.aprio\{[^}]*\}\n", r"\.aprio\.note\{[^}]*\}\n", r"\.aprio button\{[^}]*\}\n", r"\.aprio button\.on\{[^}]*\}\n", r"\.arow:not\(\.on\) \.aprio button\.on\{[^}]*\}\n"]:
    s, k = re.subn(rule, "", s, count=1); assert k == 1, rule
for n in ['ngpFree', 'lifeDays', 'checkKit', 'fmtSecs', 'twoStep', 'masteryTxt', 'armed[']:
    assert n not in s, n

# ---- 3. the old fault (strain): out of the drain formula and the forecast
once("function drainNow(strain, haz, wear, z){ const k = danger(z); return Math.min((HUNGER * strain + (haz || 0)) * k,", "function drainNow(haz, wear, z){ const k = danger(z); return Math.min((HUNGER + (haz || 0)) * k,")
once("drainNow(L.strain || 1, cur && cur.haz ? hazDmg(cur) : 0, L.wear, L.sec || 1)", "drainNow(cur && cur.haz ? hazDmg(cur) : 0, L.wear, L.sec || 1)")
once("drainNow(L.strain || 1, 0, L.wear, L.sec || 1)", "drainNow(0, L.wear, L.sec || 1)")
once("drainNow(L.strain, h1, L.wear, L.sec || 1)", "drainNow(h1, L.wear, L.sec || 1)")
once("let hp = L.hp, strain = L.strain || 1, t = 0, why = '';", "let hp = L.hp, t = 0, why = '';")
once("hp -= drainNow(strain, haz, (L.wear || 0) + t, L.sec || 1) * dt;", "hp -= drainNow(haz, (L.wear || 0) + t, L.sec || 1) * dt;")
once(" stationRes:1, strainMul:1,", " stationRes:1,")
once(" if (e.strainMul) m.strainMul *= e.strainMul;", "")
once("meal:0, strain:1, sec:1,", "meal:0, sec:1,")
once("  $('#s-strain').hidden = true;   // (the fault is gone)\n", "")
s, k = re.subn(r'<[a-z]+[^>]*id="s-strain"[^>]*>[^<]*</[a-z]+>', '', s); assert k <= 1
assert 'drainNow(L.strain' not in s and 's-strain' not in s and 'strainMul' not in s

# ---- 4. remnants of removed systems: stasis boost, background pause, banked time, new game plus labels
once(",'boostX']", "]") if ",'boostX']" in s else None
s = s.replace("'deathPause','startPaused','pauseCross','pauseRunEnd','pauseDone','replay','fillCross','autoFeed','boostX'", "'deathPause','startPaused','pauseCross','pauseRunEnd','pauseDone','replay','fillCross','autoFeed'")
once(", autoFeed:false, boost:false, boostX:2}", ", autoFeed:false}")
once("  S.bank = 0; S.set.boost = false;   // the stasis boost is gone\n", "  delete S.bank; delete S.set.boost; delete S.set.boostX; delete S.set.bgPause;   // removed: banked time, the stasis boost, background pause\n")
once(" + !!S.set.bgPause + ", " + ")
once("(raw.pr && raw.pr.n ? ' \\u00b7 NG+' + raw.pr.n : '') + ", "")
once("(S.pr && (S.pr.n || ngpLv('speed')) ? ' <span class=\"hng\">' + [S.pr.n ? 'NG+' + S.pr.n : '', ngpLv('speed') ? '\\u00d7' + ngpSpeed().toFixed(1) : ''].filter(Boolean).join(' \\u00b7 ') + '</span>' : '')",
     "(ngpLv('speed') ? ' <span class=\"hng\">\\u00d7' + ngpSpeed().toFixed(1) + '</span>' : '')")
i = s.index("  // Play time: the whole save across new game plus"); j = s.index("  h += `<tr class=\"pttot\">", i)
s = s[:i] + """  // Play time: real time the clock has run in this save
  const tot = S.stats.played || 0;
  let h = statsGrid() + `<div class="panel"><span class="h2">Play time</span><p class="note">Real time the clock has run in this save.</p><div class="rtab"><table class="dt"><tbody>`;
  h += `<tr><td>This run</td><td>${S.gen} seedling${S.gen === 1 ? '' : 's'} so far</td><td>${fmtHours(tot)}</td></tr>`;
""" + s[j:]
s = s.replace("${S.bestAll.ng ? ' NG+' + S.bestAll.ng : ''}", "")
open(P, 'w').write(s)
print('cleanup ok')
