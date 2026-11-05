// Act totals from the lean bots (playtest-notes.md). Update the expected values whenever balance changes on purpose.
const test = require('node:test'), assert = require('node:assert');
const {bot} = require('./_game');
const near = (v, want, tol, what) => assert.ok(Math.abs(v - want) <= tol, `${what}: ${v} (expected ${want} ± ${tol})`);
test('lean bot: Act I total 4.75 h in-game', () => {
  const m = bot('sim11c.js').match(/TOTAL in-game h ([\d.]+)/); assert.ok(m, 'no TOTAL line');
  near(+m[1], 4.75, 0.02, 'Act I hours');
});
test('Act II bot: long watch 2.63, Boarders 1.56, Arrival 0.88 h', {skip: process.env.QUICK ? 'QUICK=1 skips the 1-minute Act II run' : false}, () => {
  const m = bot('sim16c.js', ['AB']).match(/long watch h ([\d.]+) boarders h ([\d.]+) arrival h ([\d.]+) act2 h ([\d.]+)/); assert.ok(m, 'no Act II line');
  near(+m[1], 2.63, 0.02, 'long watch'); near(+m[2], 1.56, 0.02, 'Boarders'); near(+m[3], 0.88, 0.02, 'Arrival'); near(+m[4], 5.07, 0.03, 'Act II');
});
