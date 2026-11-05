// Queue tools and forecast hints (builds "forecast hints and icons", "preset rows and filters").
const test = require('node:test'), assert = require('node:assert');
const {logicSrc} = require('./_game');
const G = new Function(logicSrc() + `
  const fresh = () => { S = defaultState(); M = mods(); S.life.hp = M.maxHp; S.set.autoFood = true; S.set.autoEat = true; S.set.foodPct = 40; };
  const acts1 = () => TASKS.filter(t => t.z === 1 && t.kind === 'act' && !t.cross).map(t => t.id);
  const realRun = () => { const L = S.life; let n = 0; while (!L.dead && n++ < 400000) { if (step(2) === false) break; } return {dead:L.dead, day:L.day, cause:L.cause}; };
  return {get S(){ return S; }, fresh, acts1, realRun, forecast, fcTries, fcMakeTry, fcRun, fcGain, qCurEntry, step, T, complete, qPresetFire};`)();

test('forecast hint: a starving setting is found, and its copy matches the real run with it on', () => {
  G.fresh(); const S = G.S; S.set.autoEat = false; S.life.queue = G.acts1().slice(0, 3);   // a short queue: charging runs after the work (rule D2)
  const before = JSON.stringify(S), base = G.forecast();
  assert.strictEqual(base.end, 'dead');
  const tries = G.fcTries(base); assert.ok(tries.some(x => x.k === 'autoEat'), 'Auto-recharge is tried');
  const x = tries.find(y => y.k === 'autoEat'), f = G.fcMakeTry(x); G.fcRun(Infinity, f);
  assert.strictEqual(JSON.stringify(S), before, 'tries changed the real state');
  assert.ok(G.fcGain(base, f) > 0, 'Auto-recharge adds life');
  S.set.autoEat = true; const r = G.realRun();
  assert.ok(Math.abs(f.endDay - r.day) < 1e-6, `tried ${f.endDay} vs real ${r.day}`);
});
test('forecast hint: nothing to suggest on a fresh game with the usual settings', () => {
  G.fresh(); G.S.life.queue = G.acts1();
  const base = G.forecast(), tries = G.fcTries(base);
  assert.ok(tries.every(x => { const f = G.fcMakeTry(x); G.fcRun(Infinity, f); return G.fcGain(base, f) === 0; }));
});
test('clear queue keeps the row being worked on', () => {
  G.fresh(); const L = G.S.life, q = G.acts1(); L.queue = q.slice(0, 3);
  for (let i = 0; i < 5; i++) G.step(2);
  const cur = L.cur; assert.ok(L.queue.includes(cur), 'working on a queued row'); assert.strictEqual(G.qCurEntry(), cur);
  L.queue = L.queue.filter(x => x !== cur); assert.strictEqual(G.qCurEntry(), null, 'nothing kept when the current task is not queued');
});

test('preset row: fires once the rows above are done, replaces itself and the rows below', () => {
  G.fresh(); const S = G.S, L = S.life, q = G.acts1();
  S.qpresets[1] = [q[3], q[4]]; L.queue = [q[0], 'p:1', q[1], q[2]];
  G.qPresetFire(); assert.deepStrictEqual(L.queue, [q[0], 'p:1', q[1], q[2]], 'waits while a row above is left');
  let n = 0; while (!L.dead && !G.complete(G.T[q[0]]) && n++ < 20000) G.step(2);
  G.qPresetFire();
  assert.deepStrictEqual(L.queue.filter(x => x !== q[0]), [q[3], q[4]].filter(x => !G.complete(G.T[x])));
  assert.ok((L.qdone || []).includes('p:1'), 'the row is used up');
});
test('preset row: skipped rows above do not block; each preset loads once per seedling', () => {
  G.fresh(); const S = G.S, L = S.life, q = G.acts1();
  S.qpresets[0] = [q[2], 'p:0']; L.queue = [q[1], 'p:0']; L.qskip = {[q[1]]:1};
  G.qPresetFire();
  assert.deepStrictEqual(L.queue, [q[1], q[2], 'p:0'], 'fired past the skipped row');
  L.queue = ['p:0', q[3]]; G.qPresetFire();
  assert.deepStrictEqual(L.queue, [q[3]], 'a second load of the same preset is just used up');
});
test('preset row: the forecast matches the real run', () => {
  G.fresh(); const S = G.S, L = S.life, q = G.acts1();
  S.qpresets[2] = q.slice(2); L.queue = [q[0], q[1], 'p:2'];
  const f = G.forecast(), r = G.realRun();
  assert.ok(Math.abs(f.endDay - r.day) < 1e-6, `forecast ${f.endDay} vs real ${r.day}`); assert.strictEqual(f.cause, r.cause);
  assert.strictEqual(f.rows[2].st, 'done', 'the preset row is marked done in the forecast');
});
