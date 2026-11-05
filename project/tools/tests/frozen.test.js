// Frozen sections must not move: completionist seedling counts (owner-approved values, playtest-notes.md).
const test = require('node:test'), assert = require('node:assert');
const {bot, firstBySec} = require('./_game');
test('completionist bot: Seedling Vaults 9, Taproot Galleries 11, Shattered Bark 9', () => {
  const f = firstBySec(bot('simcomp2.js', [], {UPTO:'3', MAXG:'80'}));
  assert.strictEqual(f[2], 9, 'Seedling Vaults (since build "act ii twice act i"): first seedling in the Taproot');
  assert.strictEqual(f[15] - f[2], 11, 'Taproot Galleries (FROZEN; since build "act ii twice act i"): seedlings used');
  assert.strictEqual(f[3] - f[15], 9, 'The Shattered Bark: seedlings used (untuned; since build "act ii twice act i")');
});
