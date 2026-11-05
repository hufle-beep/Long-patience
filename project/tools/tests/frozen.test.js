// Frozen sections must not move: completionist seedling counts (owner-approved values, playtest-notes.md).
const test = require('node:test'), assert = require('node:assert');
const {bot, firstBySec} = require('./_game');
test('completionist bot: Seedling Vaults 10, Taproot Galleries 13, Shattered Bark 10', () => {
  const f = firstBySec(bot('simcomp2.js', [], {UPTO:'3', MAXG:'80'}));
  assert.strictEqual(f[2], 10, 'Seedling Vaults (retuned B 2026-11-05: length 2.81; owner played 6 at 2.212): first seedling in the Taproot');
  assert.strictEqual(f[15] - f[2], 13, 'Taproot Galleries (FROZEN; 14 before the longer Vaults): seedlings used');
  assert.strictEqual(f[3] - f[15], 10, 'The Shattered Bark: seedlings used (untuned; update when retuned)');
});
