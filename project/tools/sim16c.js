// Act II pacing: play a fresh run to the first ignition, then the chosen branch (A, B or AB = merge).
const fs=require('fs');
let html=fs.readFileSync(process.env.F||'/home/claude/long-patience/index.html','utf8');
let logic=html.match(/<script id="logic">([\s\S]*?)<\/script>/)[1];
const BR=process.argv[2]||'A';
eval(logic+`
globalThis.C2={}; { const _d=die; die=function(c){ const z=S.life.sec||1; const k=(z>=6?"A2 ":"A1 ")+(String(c).startsWith("Ran out")?"starved":String(c).startsWith("Drained")?"drain":"other"); C2[k]=(C2[k]||0)+1; return _d.apply(this,arguments); }; }
S=defaultState(); M=mods(); S.life.hp=M.maxHp; S.perks.survival=true; S.set.autoFeed=true; S.set.foodPct=55; S.set.autoFood=true; S.set.autoEat=true;
let won=false, winGen=0, winDays=0, done=false; HOOK.win=()=>{won=true};
const first={}; const lives=[];
for(let life=0;life<400&&!done;life++){
  const L=S.life;
  while(!L.dead&&!done){
    const acts=TASKS.filter(t=>(t.kind==='act')&&available(t)&&!complete(t)).sort((a,b)=>a.days/speedOf(a)-b.days/speedOf(b));
    let safe=acts.filter(t=>!t.haz||Math.min(hazDmg(t),MAX_DRAIN)*t.days*t.reps/speedOf(t)<L.hp*0.8);
    const nonCross=safe.filter(t=>!t.cross&&!t.finale&&!t.win); const cross=safe.filter(t=>t.cross||t.finale||t.win);
    const drills=TASKS.filter(t=>t.kind==='train'&&available(t)&&!complete(t));
    L.queue=(process.env.DR&&drills.length)?drills.map(t=>t.id):(nonCross.length?nonCross:cross.length?cross:safe.length?safe:acts).map(t=>t.id);
    let bj=null,bs=0;TASKS.forEach(t=>{if(t.kind==='job'&&t.prod&&t.prod.salvage&&available(t)&&!jobFull(t)){const r=t.prod.salvage*speedOf(t)*(t.upkeep&&L.shipWear>2?3:1);if(r>bs){bs=r;bj=t}}});
    if(!bj) bj=pickFood();
    L.job=bj?bj.id:null;
    ITEMS.forEach(i=>{if(typeof BT==="object"){buyItem(i.id,false);}else if(isDone(i.req)&&!L.owned[i.id]&&L.salvage>=i.cost){L.salvage-=i.cost;L.owned[i.id]=true;M=mods();}});
    if(won&&!S.branch){ S.branch=BR==='B'?'B':'A'; if(BR==='AB') S.merge=true; winGen=S.gen; winDays=(S.stats.daysLived+L.day)/TPD; if(L.sec===5&&complete(T.ignite)) enterZone(S.branch==='A'?6:9,5); }
    const z=L.sec; if(!first[z])first[z]=S.gen;
    if(!globalThis.T9&&L.sec===9){globalThis.T9=(S.stats.daysLived+L.day)/TPD;} if(!globalThis.T6&&L.sec===6){globalThis.T6=(S.stats.daysLived+L.day)/TPD;} const d0=L.day; const spd=ngpSpeed(); advance(20); const dd=L.day-d0; globalThis.RT=(globalThis.RT||0)+dd/(DPS*spd); if(L.sec>=6&&!globalThis.R6)globalThis.R6=globalThis.RT; if(L.sec>=9&&!globalThis.R9)globalThis.R9=globalThis.RT; if(L.sec>=12&&!globalThis.R12)globalThis.R12=globalThis.RT; globalThis.LV=[ngpLv('growth'),ngpLv('drain'),ngpLv('hp'),ngpLv('speed')].map(x=>x.toFixed(2)).join('/'); if(L.day===d0&&!L.dead){ if(!L.queue.length&&!L.job){L.job=pickFood()?pickFood().id:'algae'} advance(20); if(L.day===d0) die('stuck'); }
    if(BR==='A'&&S.a2run.done.A) done=true; if(BR!=='A'&&S.a2run.done.C) done=true;
  }
  lives.push(S.gen+':'+Math.round(L.day/DPS)+'s/z'+L.sec+(L.cause==='stuck'?'S':''));
  {const L=S.life; (globalThis.LIVES=globalThis.LIVES||[]).push([S.gen,Math.round(L.day/DPS)+'s',L.sec,(L.cause||'').slice(0,22),Math.round(M.maxHp),(L.strain||1).toFixed(1)]);}
  if(done)break; decant();
}
const days=(S.stats.daysLived+S.life.day)/TPD;
console.log("CAUSES",JSON.stringify(C2));console.log('REAL with overclock: boarders h',((globalThis.R9-globalThis.R6)/3600).toFixed(2),'long watch h',((globalThis.R12-globalThis.R9)/3600).toFixed(2),'arrival h',((globalThis.RT-globalThis.R12)/3600).toFixed(2),'act2 h',((globalThis.RT-globalThis.R6)/3600).toFixed(2),'legacy levels at end',globalThis.LV);console.log('boarders h',((globalThis.T9-globalThis.T6)*TPD/DPS/3600).toFixed(2),'long watch h',((days-globalThis.T9)*TPD/DPS/3600).toFixed(2));console.log('branch',BR,'first',JSON.stringify(first),'done',done,'winGen',winGen,'endGen',S.gen,'act2 clones',S.gen-winGen,'act2 h',((days-winDays)*TPD/DPS/3600).toFixed(2),'total h',(days*TPD/DPS/3600).toFixed(2),'honours',S.a2.hon);
console.log(lives.slice(-12).join(' '));
`);
