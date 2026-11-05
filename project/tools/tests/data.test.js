// Data integrity (round 5, R6) and static softlock checks (R38): every reference points at something that exists,
// every section can be finished from what it and earlier sections hold, and every section has its pieces
// (end task, danger, crossing cost, store, length, year, target, icon). Fast: no bots.
const test = require('node:test'), assert = require('node:assert'), fs = require('fs');
const {logicSrc, GAME} = require('./_game');
const G = new Function(logicSrc() + `
  return {TASKS, ZONES, ROUTE, ACT1, ACT2R, ACT_ENDS, PERKS, ITEMS, T, DANGER, STORE_CAP, ZDAYS, TARGETS, nextZone};`)();
const html = fs.readFileSync(GAME, 'utf8'), ui = html.match(/<script id="ui">([\s\S]*?)<\/script>/)[1];
const routeIdx = z => G.ROUTE.indexOf(z), zoneIds = new Set(G.ZONES.map(z => z.id));
const ends = z => G.TASKS.filter(t => t.z === z && (t.cross || t.finale || t.win));

test('ids are unique and every task points at known things', () => {
  const ids = G.TASKS.map(t => t.id), dup = ids.filter((x, i) => ids.indexOf(x) !== i);
  assert.deepStrictEqual(dup, [], 'duplicate task ids');
  const iids = G.ITEMS.map(i => i.id); assert.deepStrictEqual(iids.filter((x, i) => iids.indexOf(x) !== i), [], 'duplicate gear ids');
  const pids = G.PERKS.map(p => p.id); assert.deepStrictEqual(pids.filter((x, i) => pids.indexOf(x) !== i), [], 'duplicate record ids');
  const bad = [];
  for (const t of G.TASKS) {
    if (!zoneIds.has(t.z)) bad.push(t.id + ': unknown section ' + t.z);
    if (!['act', 'job', 'train'].includes(t.kind)) bad.push(t.id + ': unknown kind ' + t.kind);
    for (const r of t.req || []) if (!G.T[r]) bad.push(t.id + ': requirement ' + r + ' does not exist');
    if (t.perk && !pids.includes(t.perk)) bad.push(t.id + ': record ' + t.perk + ' does not exist');
    if (t.to != null && !zoneIds.has(t.to)) bad.push(t.id + ': leads to unknown section ' + t.to);
    if (!t.name || !String(t.name).trim()) bad.push(t.id + ': no name');
    if (!(t.days > 0) && t.kind !== 'job') bad.push(t.id + ': no length');
  }
  for (const it of G.ITEMS) {
    if (it.req && !G.T[it.req]) bad.push('gear ' + it.id + ': opened by ' + it.req + ', which does not exist');
    if (!(it.cost >= 0)) bad.push('gear ' + it.id + ': no cost');
  }
  assert.deepStrictEqual(bad, []);
});

test('requirements never point at a later section, and have no loops', () => {
  const bad = [];
  for (const t of G.TASKS) for (const r of t.req || []) {
    const rt = G.T[r]; if (rt && routeIdx(rt.z) > routeIdx(t.z)) bad.push(t.id + ' (' + t.z + ') needs ' + r + ' from a later section (' + rt.z + ')');
  }
  const state = {}, loop = [];
  const visit = (id, path) => {
    if (state[id] === 2) return; if (state[id] === 1) { loop.push(path.concat(id).join(' > ')); return; }
    state[id] = 1; for (const r of (G.T[id].req || [])) if (G.T[r]) visit(r, path.concat(id)); state[id] = 2;
  };
  G.TASKS.forEach(t => visit(t.id, []));
  assert.deepStrictEqual(bad.concat(loop), []);
});

test('every section can be finished: its end task is reachable from its own and earlier tasks (no softlock by data)', () => {
  // Same-life reachability: a task can be done once all its requirements can (legacy finals count as unrevealed).
  const can = new Set(), stuck = [];
  for (const z of G.ROUTE) {
    const here = G.TASKS.filter(t => t.z === z);
    let grew = true;
    while (grew) { grew = false; for (const t of here) if (!can.has(t.id) && (t.req || []).every(r => can.has(r) || G.T[r].legacy)) { can.add(t.id); grew = true; } }
    for (const t of here) if (!can.has(t.id) && !t.legacy) stuck.push(z + ': ' + t.id + ' (needs ' + (t.req || []).filter(r => !can.has(r)).join(', ') + ')');
    const e = ends(z); if (!e.length) stuck.push(z + ': no crossing or finale');
  }
  assert.deepStrictEqual(stuck, []);
});

test('the route is whole: each end task leads to the next section, every section has its tables', () => {
  const bad = [];
  assert.strictEqual(new Set(G.ROUTE).size, G.ROUTE.length, 'a section appears twice in the route');
  for (const z of zoneIds) if (!G.ROUTE.includes(z)) bad.push('section ' + z + ' is not on the route');
  G.ROUTE.forEach((z, i) => {
    const e = ends(z);
    for (const t of e.filter(t => t.cross)) { const to = t.to != null ? t.to : G.nextZone(z); if (to !== G.ROUTE[i + 1]) bad.push(t.id + ' leads to ' + to + ', not ' + G.ROUTE[i + 1]); }
    for (const [name, tb] of [['DANGER', G.DANGER], ['STORE_CAP', G.STORE_CAP], ['ZDAYS', G.ZDAYS], ['TARGETS', G.TARGETS]]) if (!(tb[z] > 0)) bad.push(name + ' has no value for section ' + z);
    const zo = G.ZONES.find(x => x.id === z); if (!(zo.yr > 0)) bad.push('section ' + z + ' has no voyage year');
    if (!new RegExp('\\bz' + z + '\\s*:').test(ui)) bad.push('section ' + z + ' has no route icon (GI.z' + z + ')');
    if (i && G.DANGER[z] < G.DANGER[G.ROUTE[i - 1]]) bad.push('danger drops at section ' + z);
  });
  for (const z of G.ACT_ENDS) if (!G.ROUTE.includes(z)) bad.push('act end ' + z + ' not on the route');
  assert.deepStrictEqual(bad, []);
});

test('every record is found by some task, and every non-legacy task can be seen', () => {
  const found = new Set(G.TASKS.filter(t => t.perk).map(t => t.perk)), bad = [];
  for (const p of G.PERKS) if (!found.has(p.id) && !(p.by && G.T[p.by])) bad.push('record ' + p.id + ' is found by no task');
  for (const p of G.PERKS) if (p.by && !G.T[p.by]) bad.push('record ' + p.id + ': its task ' + p.by + ' does not exist');
  assert.deepStrictEqual(bad, []);
});

test('every gear design fits the deadwood storage its section can reach', () => {
  // build "gear built when paid" raised costs: a design costing more than the most storage a seedling can have in its
  // section (every record, everything done up to and in it, all gear owned) could never be built
  const R = new Function(logicSrc() + `
    const cap = {};
    ROUTE.forEach((z, k) => { S = defaultState(); S.won = k >= ACT1.length; S.life.sec = z; PERKS.forEach(p => S.perks[p.id] = true);
      const upto = ROUTE.slice(0, k + 1); TASKS.forEach(t => { if (upto.includes(t.z)) S.life.done[t.id] = t.reps || 1; });
      ITEMS.forEach(i => { if (upto.includes(gearZone(i))) S.life.owned[i.id] = true; }); M = mods(); cap[z] = M.salCap; });
    return ITEMS.filter(i => i.cost > cap[gearZone(i)]).map(i => i.id + ' costs ' + i.cost + ', storage reaches ' + cap[gearZone(i)]);`)();
  assert.deepStrictEqual(R, []);
});
