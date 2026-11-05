// Act totals from the lean bots (playtest-notes.md). Update the expected values whenever balance changes on purpose.
const test = require('node:test'), assert = require('node:assert');
const {bot} = require('./_game');
let a1Out, a2Out;   // each bot runs once; the ratio test reuses the outputs
const act1 = () => a1Out || (a1Out = bot('sim11c.js')), act2 = () => a2Out || (a2Out = bot('sim16c.js', ['AB']));
const near = (v, want, tol, what) => assert.ok(Math.abs(v - want) <= tol, `${what}: ${v} (expected ${want} ± ${tol})`);
test('lean bot: Act I total 5.59 h in-game', () => {
  const m = act1().match(/TOTAL in-game h ([\d.]+)/); assert.ok(m, 'no TOTAL line');
  near(+m[1], 5.59, 0.02, 'Act I hours');
});
test('Act II bot: long watch 6.36, Boarders 3.31, Arrival 1.53 h', {skip: process.env.QUICK ? 'QUICK=1 skips the 1-minute Act II run' : false}, () => {
  const m = act2().match(/long watch h ([\d.]+) boarders h ([\d.]+) arrival h ([\d.]+) act2 h ([\d.]+)/); assert.ok(m, 'no Act II line');
  near(+m[1], 6.36, 0.02, 'long watch'); near(+m[2], 3.31, 0.02, 'Boarders'); near(+m[3], 1.53, 0.02, 'Arrival'); near(+m[4], 11.20, 0.03, 'Act II');
});
// Design rule (owner 2026-11-05): Act II takes about twice as long as Act I (lean bots, in-game hours)
test('Act II takes about twice as long as Act I (1.8-2.2)', {skip: process.env.QUICK ? 'QUICK=1 skips the 1-minute Act II run' : false}, () => {
  const a = +act1().match(/TOTAL in-game h ([\d.]+)/)[1], b = +act2().match(/act2 h ([\d.]+)/)[1], r = b / a;
  assert.ok(r >= 1.8 && r <= 2.2, `Act II / Act I = ${b} / ${a} = ${r.toFixed(2)} (expected 1.8-2.2)`);
});
