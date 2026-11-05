// Runs (build "runs"): the lean whole-game bot (as sim16c.js AB) plays the full voyage RUNS times on one save,
// starting each new run with the game's own newRun(), and prints in-game hours per run (Act I / Act II, at x1,
// overclock included like sim16c's REAL line) and seedlings used. Usage: RUNS=3 node simruns.js
const fs = require('fs');
const html = fs.readFileSync(process.env.F || '/home/claude/long-patience/index.html', 'utf8');
const logic = html.match(/<script id="logic">([\s\S]*?)<\/script>/)[1];
const RUNS = +(process.env.RUNS || 3);
eval(logic + `
S = defaultState(); M = mods(); S.life.hp = M.maxHp; S.perks.survival = true; S.set.foodPct = 55; S.set.autoFood = true; S.set.autoEat = true;
let rt = 0, r0 = 0, rWon = null, g0 = 1; const out = [];
for (let run = 1; run <= RUNS; run++) {
  let done = false;
  for (let life = 0; life < 600 && !done; life++) {
    const L = S.life;
    while (!L.dead && !done) {
      if (S.actEnd === 1) moveOnToAct2();   // the Act I choice: move on
      const acts = TASKS.filter(t => t.kind === 'act' && available(t) && !complete(t)).sort((a, b) => a.days / speedOf(a) - b.days / speedOf(b));
      const safe = acts.filter(t => !t.haz || Math.min(hazDmg(t), MAX_DRAIN) * t.days * t.reps / speedOf(t) < L.hp * 0.8);
      const nonCross = safe.filter(t => !t.cross && !t.finale && !t.win), cross = safe.filter(t => t.cross || t.finale || t.win);
      L.queue = (nonCross.length ? nonCross : cross.length ? cross : safe.length ? safe : acts).map(t => t.id);
      let bj = null, bs = 0; TASKS.forEach(t => { if (t.kind === 'job' && t.prod && t.prod.salvage && available(t) && !jobFull(t)) { const r = t.prod.salvage * speedOf(t); if (r > bs) { bs = r; bj = t; } } });
      if (!bj) bj = pickFood(); L.job = bj ? bj.id : null;
      ITEMS.forEach(i => buyItem(i.id, false));
      const d0 = L.day; advance(20); rt += (L.day - d0) / (DPS * ngpSpeed());
      if (S.won && rWon == null) rWon = rt;
      if (S.a2run.done.C) done = true;
    }
    if (done) break; decant();
  }
  out.push('run ' + run + (done ? '' : ' (unfinished)') + ': Act I h ' + ((rWon - r0) / 3600).toFixed(2) + ' Act II h ' + ((rt - rWon) / 3600).toFixed(2) + ' seedlings ' + (S.gen - g0 + 1) + ' legacy levels ' + ['growth', 'drain', 'hp', 'speed', 'wear'].map(k => ngpLv(k).toFixed(2)).join('/'));
  if (!done) break;
  newRun(); S.life.hp = M.maxHp; r0 = rt; rWon = null; g0 = S.gen;
}
console.log(out.join('\\n'));
`);
