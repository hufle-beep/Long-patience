// The queue forecast must match what really happens: same death tick and cause, on a fresh game over
// many lives and on the Act I/II fixture saves. Also: running a forecast must not change the real state.
const test = require('node:test'), assert = require('node:assert'), fs = require('fs'), path = require('path');
const {logicSrc, TOOLS} = require('./_game');
const G = new Function('fs', 'path', 'TOOLS', logicSrc() + `
  const realRun = () => { const L = S.life, d0 = L.day; let n = 0; while (!L.dead && n++ < 400000) { if (step(2) === false) break; } return {dead:L.dead, day:L.day, cause:L.cause}; };
  const fresh = () => { S = defaultState(); M = mods(); S.life.hp = M.maxHp; S.set.autoFood = true; S.set.autoEat = true; S.set.foodPct = 55; };
  const fillQueue = () => { const L = S.life; L.queue = TASKS.filter(t => t.kind !== 'job' && t.z === (L.sec || 1) && !complete(t) && legacyOpen(t)).map(t => t.id); };
  // like a real load (mergeState): queue entries for tasks that no longer exist are dropped
  const okQ = q => typeof q === 'string' && (isCQ(q) ? cSteps(q).length > 0 : isGQ(q) ? !!IT[q.slice(2)] : !!T[q]);
  const load = f => { S = JSON.parse(fs.readFileSync(path.join(TOOLS, 'fixtures', f), 'utf8')); ['queue', 'qdone'].forEach(k => { if (Array.isArray(S.life[k])) S.life[k] = S.life[k].filter(okQ); }); M = mods(); };
  return {get S(){ return S; }, forecast, realRun, fresh, fillQueue, load, decant};`)(fs, path, TOOLS);
test('forecast matches the real run, fresh game, 12 lives', () => {
  G.fresh();
  for (let life = 0; life < 12; life++) {
    G.fillQueue();
    const before = JSON.stringify(G.S), f = G.forecast();
    assert.strictEqual(JSON.stringify(G.S), before, 'forecast changed the real state');
    const r = G.realRun();
    assert.strictEqual(f.end === 'dead', r.dead, 'life ' + (life + 1) + ': dies?');
    assert.ok(Math.abs(f.endDay - r.day) < 1e-6, `life ${life + 1}: forecast ${f.endDay} vs real ${r.day}`);
    if (r.dead) assert.strictEqual(f.cause, r.cause); else break;
    G.decant();
  }
});
for (const fx of ['snap4old.json', 'snap7.json', 'snap12.json', 'snap16.json']) test('forecast matches the real run: ' + fx, () => {
  G.load(fx); if (!G.S.life.queue.length) G.fillQueue();
  const f = G.forecast(), r = G.realRun();
  assert.strictEqual(f.end === 'dead', r.dead); assert.ok(Math.abs(f.endDay - r.day) < 1e-6, `forecast ${f.endDay} vs real ${r.day}`); assert.strictEqual(f.cause, r.cause);
});
