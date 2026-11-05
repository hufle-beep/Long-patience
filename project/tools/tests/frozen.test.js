// Frozen sections must not move: completionist seedling counts (owner-approved values, playtest-notes.md).
const test = require('node:test'), assert = require('node:assert');
const {bot, firstBySec} = require('./_game');
test('completionist bot: Seedling Vaults 9, Taproot Galleries 14, Shattered Bark 11', () => {
  const f = firstBySec(bot('simcomp2.js', [], {UPTO:'3', MAXG:'80'}));
  assert.strictEqual(f[2], 9, 'Seedling Vaults (FROZEN): first seedling in the Taproot');
  assert.strictEqual(f[15] - f[2], 14, 'Taproot Galleries (FROZEN): seedlings used');
  assert.strictEqual(f[3] - f[15], 11, 'The Shattered Bark: seedlings used (untuned; update when retuned)');
});
