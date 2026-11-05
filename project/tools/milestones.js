// Milestone table (round 5, R7; bot outlier check R38): runs the lean whole-game bot and the completionist
// Act I bot, then writes seedlings used and in-game time per section to milestones.md next to this file,
// with the change against the previous table. Flags sections far above their target or a bot that stops early.
//   node milestones.js            (F=<index.html> to test another build; NOSAVE=1 to print without writing)
const fs = require('fs'), path = require('path'), {execFileSync} = require('child_process');
const TOOLS = __dirname, GAME = process.env.F || path.resolve(TOOLS, '../../index.html'), OUT = path.join(TOOLS, 'milestones.md');
const html = fs.readFileSync(GAME, 'utf8'), logic = html.match(/<script id="logic">([\s\S]*?)<\/script>/)[1];
global.localStorage = {getItem(){ return null; }, setItem(){}, removeItem(){}, key(){ return null; }, length:0};
const G = new Function(logic + '; return {ZONES, ROUTE, TARGETS, DPS, BUILD};')();
const run = (script, args, env) => execFileSync(process.execPath, [path.join(TOOLS, script), ...args], {env:{...process.env, F:GAME, ...env}, encoding:'utf8', maxBuffer:1 << 28});
const firstAt = out => { const m = out.match(/FIRSTAT (\{.*\})/); return m ? JSON.parse(m[1]) : {}; };
const lean = firstAt(run('sim16c.js', ['AB'], {})), comp = firstAt(run('simcomp2.js', [], {UPTO:'4', MAXG:'150'}));
const hm = d => { const m = Math.round(d / G.DPS / 60); return Math.floor(m / 60) + ':' + String(m % 60).padStart(2, '0'); };
const used = (fa, i) => {   // seedlings used in route section i: first seedling in the next section minus the first in this one
  const z = G.ROUTE[i], nz = G.ROUTE[i + 1], a = z === 1 ? {g:0, d:0} : fa[z], b = nz != null ? fa[nz] : null;
  return a && b ? {n:b.g - a.g, d:b.d - a.d} : null;
};
const prev = {};
if (fs.existsSync(OUT)) for (const l of fs.readFileSync(OUT, 'utf8').split('\n')) { const c = l.split('|').map(x => x.trim()); if (/^\d+$/.test(c[1] || '')) prev[c[1]] = {lean:c[4], comp:c[6]}; }
const rows = [], flags = [], diffs = [];
G.ROUTE.forEach((z, i) => {
  const zo = G.ZONES.find(x => x.id === z), l = used(lean, i), c = used(comp, i), tgt = G.TARGETS[z];
  const ln = l ? String(l.n) : '-', cn = c ? String(c.n) : '-';
  if (l && tgt && l.n > Math.max(3 * tgt, tgt + 10)) flags.push(zo.name + ': lean bot used ' + l.n + ' seedlings (target ' + tgt + ')');
  if (i < G.ROUTE.length - 1 && !l) flags.push(zo.name + ': the lean bot never crossed it (stuck?)');
  const p = prev[z]; if (p && (p.lean !== ln || p.comp !== cn)) diffs.push(zo.name + ': lean ' + p.lean + ' -> ' + ln + ', completionist ' + p.comp + ' -> ' + cn);
  rows.push(`| ${z} | ${zo.name} | ${tgt || '-'} | ${ln} | ${l ? hm(l.d) : '-'} | ${cn} | ${c ? hm(c.d) : '-'} |`);
});
const build = (html.match(/const BUILD = '([^']*)'/) || [])[1] || '?';
const md = `# Bot milestones\n\nBuild: ${build}. Written by \`node milestones.js\` (lean bot: sim16c.js AB, whole game; completionist bot: simcomp2.js, Act I up to the Heartwood). Seedlings used = first seedling in the next section minus the first in this one; time = in-game h:mm spent in the section.\n\n| id | Section | Target | Lean seedlings | Lean time | Completionist seedlings | Completionist time |\n|---|---|---|---|---|---|---|\n${rows.join('\n')}\n\n${flags.length ? '**Check:** ' + flags.join('; ') + '\n' : 'No section far above its target; the lean bot crossed every section.\n'}`;
console.log(md);
console.log(diffs.length ? 'Changed since the last table:\n- ' + diffs.join('\n- ') : 'No change since the last table.');
if (!process.env.NOSAVE) fs.writeFileSync(OUT, md);
if (flags.length) process.exitCode = 2;
