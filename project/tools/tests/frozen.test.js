// Frozen sections must not move: completionist seedling counts (owner-approved values, playtest-notes.md).
const test = require('node:test'), assert = require('node:assert');
const {bot, firstBySec} = require('./_game');
test('completionist bot: Seedling Vaults 9, Taproot Galleries 13, Shattered Bark 8', () => {
  const f = firstBySec(bot('simcomp2.js', [], {UPTO:'3', MAXG:'80'}));
  assert.strictEqual(f[2], 9, 'Seedling Vaults (since build "automation at practiced"): first seedling in the Taproot');
  assert.strictEqual(f[15] - f[2], 13, 'Taproot Galleries (FROZEN; since build "automation at practiced"): seedlings used');
  assert.strictEqual(f[3] - f[15], 8, 'The Shattered Bark: seedlings used (untuned; since build "automation at practiced")');
});
