// Shared helpers for the regression tests: where the game is, running a bot, loading the rules.
const fs = require('fs'), path = require('path'), {execFileSync} = require('child_process');
const TOOLS = path.resolve(__dirname, '..');
const GAME = process.env.F || path.resolve(__dirname, '../../../index.html');
// Run a bot script from project/tools with the game file and extra env; returns its output
function bot(script, args = [], env = {}){
  return execFileSync(process.execPath, [path.join(TOOLS, script), ...args], {env:{...process.env, F:GAME, ...env}, encoding:'utf8', maxBuffer:1 << 28});
}
// The logic script as source, to eval in a test (the rules have no DOM access and no randomness)
const logicSrc = () => fs.readFileSync(GAME, 'utf8').match(/<script id="logic">([\s\S]*?)<\/script>/)[1];
global.localStorage = global.localStorage || {getItem(){ return null; }, setItem(){}, removeItem(){}, key(){ return null; }, length:0};
// First seedling found dying in each section (completionist bot output), by section id
function firstBySec(out){
  const first = {};
  for (const m of out.matchAll(/CLONE (\d+) \([^)]*?sec (\d+)/g)) if (!(m[2] in first)) first[m[2]] = +m[1];
  return first;
}
module.exports = {TOOLS, GAME, bot, logicSrc, firstBySec};
