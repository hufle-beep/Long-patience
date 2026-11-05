// Queue tools and forecast hints (builds "forecast hints and icons", "preset rows and filters").
const test = require('node:test'), assert = require('node:assert');
const {logicSrc} = require('./_game');
const G = new Function(logicSrc() + `
  const fresh = () => { S = defaultState(); M = mods(); S.life.hp = M.maxHp; S.set.autoFood = true; S.set.autoEat = true; S.set.foodPct = 40; };
  const acts1 = () => TASKS.filter(t => t.z === 1 && t.kind === 'act' && !t.cross).map(t => t.id);
  const realRun = () => { const L = S.life; let n = 0; while (!L.dead && n++ < 400000) { if (step(2) === false) break; } return {dead:L.dead, day:L.day, cause:L.cause}; };
  return {get S(){ return S; }, fresh, acts1, realRun, forecast, fcTries, fcMakeTry, fcRun, fcGain, qCurEntry, step, T};`)();

test('forecast hint: a starving setting is found, and its copy matches the real run with it on', () => {
  G.fresh(); const S = G.S; S.set.autoEat = false; S.life.queue = G.acts1();
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
