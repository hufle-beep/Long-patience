// Act totals from the lean bots (playtest-notes.md). Update the expected values whenever balance changes on purpose.
const test = require('node:test'), assert = require('node:assert');
const {bot} = require('./_game');
const near = (v, want, tol, what) => assert.ok(Math.abs(v - want) <= tol, `${what}: ${v} (expected ${want} ± ${tol})`);
test('lean bot: Act I total 5.40 h in-game', () => {
  const m = bot('sim11c.js').match(/TOTAL in-game h ([\d.]+)/); assert.ok(m, 'no TOTAL line');
  near(+m[1], 5.40, 0.02, 'Act I hours');
});
test('Act II bot: long watch 3.96, Boarders 2.11, Arrival 1.04 h', {skip: process.env.QUICK ? 'QUICK=1 skips the 1-minute Act II run' : false}, () => {
  const m = bot('sim16c.js', ['AB']).match(/long watch h ([\d.]+) boarders h ([\d.]+) arrival h ([\d.]+) act2 h ([\d.]+)/); assert.ok(m, 'no Act II line');
  near(+m[1], 3.96, 0.02, 'long watch'); near(+m[2], 2.11, 0.02, 'Boarders'); near(+m[3], 1.04, 0.02, 'Arrival'); near(+m[4], 7.11, 0.03, 'Act II');
});
