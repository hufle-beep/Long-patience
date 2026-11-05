// usage: node sim2.js [salvageMult] [z4] [z5] [echo]
var HIST=[];const fs=require('fs');
let html=fs.readFileSync(process.env.F||'/home/claude/long-patience/index.html','utf8'); if(process.env.DC) html=html.replace(/const DRILL_CREDIT = [\d.]+/,'const DRILL_CREDIT = '+process.env.DC);
let logic=html.match(/<script id="logic">([\s\S]*?)<\/script>/)[1];
const [sm,z4,z5,ec]=process.argv.slice(2).map(Number);
if(ec) logic=logic.replace(/Math\.pow\(1\.\d+, S\.echo\[s\]\)/,`Math.pow(${ec}, S.echo[s])`);
if(z4) logic=logic.replace(/4:\d+, 5:\d+\}/,`4:${z4}, 5:${z5}}`);
eval(logic+`
const fmtG=t=>{const q=Math.ceil(t/DPS),h=Math.floor(q/3600),m=Math.floor(q%3600/60),x=q%60;return (h?h+':'+String(m).padStart(2,'0'):m)+':'+String(x).padStart(2,'0');};
if(sm) TASKS.forEach(t=>{if(t.prod&&t.prod.salvage)t.prod.salvage*=sm; if(t.lifeEff&&t.lifeEff.pSal)t.lifeEff.pSal*=sm;});
S=defaultState(); M=mods(); S.life.hp=M.maxHp; S.perks.survival=true; S.set.autoFeed=true; S.set.foodPct=55; S.set.autoFood=true; S.set.autoEat=true;
let first={},won=false; HOOK.win=()=>{won=true}; const TR=[]; let cur=[]; HOOK.taskDone=t=>{cur.push((t.kind==='build'?'BUILD '+t.name.replace('Assemble: ',''):t.name)+' @'+fmtG(S.life.day));}; 
for(let life=0;life<250&&!won;life++){
  const L=S.life;
  while(!L.dead&&!won){
    const acts=TASKS.filter(t=>t.kind==='act'&&available(t)&&!complete(t)).sort((a,b)=>a.days/speedOf(a)-b.days/speedOf(b));
    let safe=acts.filter(t=>!t.haz||Math.min(hazDmg(t),MAX_DRAIN)*t.days*t.reps/speedOf(t)<L.hp*0.8);
    const nonCross=safe.filter(t=>!t.cross); const cross=safe.filter(t=>t.cross);
    // cross when nothing else left, or when remaining items are too slow for the time left
    const left=Infinity;
    const useful=nonCross.filter(t=>t.days*t.reps/speedOf(t) < left*0.5);
    const drills=TASKS.filter(t=>t.kind==='train'&&available(t)&&!complete(t)&&!t.act2&&!isA2(t.z));
    const gearLeft=ITEMS.filter(i=>gearZone(i)===(L.sec||1)&&isDone(i.req)&&!L.owned[i.id]);
    const allDrills=TASKS.filter(t=>t.kind==='train'&&available(t)&&!complete(t));
    L.queue=(nonCross.length?nonCross:allDrills.length?allDrills:gearLeft.length?gearLeft.map(i=>'g:'+i.id):cross).map(t=>typeof t==='string'?t:t.id);
    let bj=null,bs=0;TASKS.forEach(t=>{if(t.kind==='job'&&t.prod&&t.prod.salvage&&available(t)&&!jobFull(t)){const r=t.prod.salvage*speedOf(t);if(r>bs){bs=r;bj=t}}});
    if(!bj) bj=pickFood();
    L.job=bj?bj.id:null;
    ITEMS.forEach(i=>buyItem(i.id,false));   // builds at once when affordable
    const z=L.sec||1; if(!first[z])first[z]=S.gen; /* section reached (by id; the route is pathOf()) */
    const d0=L.day; advance(20); if(L.day===d0&&!L.dead){ if(!L.queue.length&&!L.job){L.job='algae'} advance(20); if(L.day===d0) die('stuck'); }
  }
  TR.push('CLONE '+S.gen+' ('+(L.cause||'crossed')+' at '+fmtG(L.day)+' in-game, sec '+L.sec+', cells '+(L.food.ration||0).toFixed(1)+', fam hatch '+((S.fam||{}).hatch||0).toFixed(1)+') :: '+cur.join(' > ')); cur=[]; if(S.gen>=(+process.env.MAXG||60)||pathOf().indexOf(L.sec)>=pathOf().indexOf(+process.env.UPTO||2)){ /* UPTO=<section id>: stop once a seedling reaches it (default 2: the Seedling Vaults count) */ console.log(TR.join(' ##### ')); console.log('FIRSTAT '+JSON.stringify(S.firstAt||{})); process.exit(0); }
  HIST.push(S.gen+":"+fmtG(L.day)+"/"+Math.min(500,100+Math.floor(S.vit||0))+(L.cause&&L.cause.startsWith("Telo")?"T":L.cause?"x":"W")); if(false) console.log(1,L.cause||'WON','done',L.order.length,SKILLS.map(k=>k.ab+L.lv[k.id]).join(' '));
  if(won)break; decant();
}
console.log("first",JSON.stringify(first),"won",won,"gen",S.gen); console.log(HIST.slice(0,6).join(" ")+" ... "+HIST.slice(-8).join(" ")); console.log(HIST.filter((h,i)=>i%3==0).join(" ")); const F=S.hist.filter(e=>e.fin);[10,20,30,40,46].forEach(g=>{const e=S.hist.find(x=>x.g===g);if(e)console.log("clone",g,"finish in-game min",JSON.stringify(e.fin.map(f=>f?+(f[0]*TPD/DPS/60).toFixed(1):null)))});console.log("TOTAL in-game h",((S.stats.daysLived+S.life.day)/DPS/3600).toFixed(2),"(real time at x1 speed is the same)");console.log("baseHP end", Math.min(500,100+Math.floor(S.vit||0)), "vit", (S.vit||0).toFixed(0));
`);
