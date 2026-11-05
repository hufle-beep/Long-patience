// Act II pacing: play a fresh run to the first ignition, then the chosen branch (A, B or AB = merge).
const fs=require('fs');
let html=fs.readFileSync(process.env.F||'/home/claude/long-patience/index.html','utf8');
let logic=html.match(/<script id="logic">([\s\S]*?)<\/script>/)[1];
const BR=process.argv[2]||'A';
eval(logic+`
globalThis.C2={}; { const _d=die; die=function(c){ const z=S.life.sec||1; const k=(isA2(z)?"A2 ":"A1 ")+(String(c).startsWith("Ran out")?"starved":String(c).startsWith("Drained")?"drain":"other"); C2[k]=(C2[k]||0)+1; return _d.apply(this,arguments); }; }
S=defaultState(); M=mods(); S.life.hp=M.maxHp; S.perks.survival=true; S.set.autoFeed=true; S.set.foodPct=55; S.set.autoFood=true; S.set.autoEat=true;
let won=false, winGen=0, winDays=0, done=false; HOOK.win=()=>{won=true};
const first={}; const lives=[];
for(let life=0;life<400&&!done;life++){
  const L=S.life;
  while(!L.dead&&!done){
    if(S.actEnd===1) moveOnToAct2();   // the Act I choice (build "act choices"): the bots move on
    const acts=TASKS.filter(t=>(t.kind==='act')&&available(t)&&!complete(t)).sort((a,b)=>a.days/speedOf(a)-b.days/speedOf(b));
    let safe=acts.filter(t=>!t.haz||Math.min(hazDmg(t),MAX_DRAIN)*t.days*t.reps/speedOf(t)<L.hp*0.8);
    const nonCross=safe.filter(t=>!t.cross&&!t.finale&&!t.win); const cross=safe.filter(t=>t.cross||t.finale||t.win);
    const drills=TASKS.filter(t=>t.kind==='train'&&available(t)&&!complete(t));
    L.queue=(process.env.DR&&drills.length)?drills.map(t=>t.id):(nonCross.length?nonCross:cross.length?cross:safe.length?safe:acts).map(t=>t.id);
    let bj=null,bs=0;TASKS.forEach(t=>{if(t.kind==='job'&&t.prod&&t.prod.salvage&&available(t)&&!jobFull(t)){const r=t.prod.salvage*speedOf(t)*(t.upkeep&&L.shipWear>2?3:1);if(r>bs){bs=r;bj=t}}});
    if(!bj) bj=pickFood();
    L.job=bj?bj.id:null;
    ITEMS.forEach(i=>buyItem(i.id,false));   // builds at once when affordable
    if(won&&!S.branch){ S.branch=BR==='B'?'B':'A'; if(BR==='AB') S.merge=true; winGen=S.gen; winDays=(S.stats.daysLived+L.day)/TPD; if(L.sec===5&&complete(T.ignite)) enterZone(9,5); }
    const z=L.sec; if(!first[z])first[z]=S.gen;
    if(!globalThis.T6&&L.sec===6){globalThis.T6=(S.stats.daysLived+L.day)/TPD;} if(!globalThis.T9&&isA2(L.sec)){globalThis.T9=(S.stats.daysLived+L.day)/TPD;} /* T9: Act II start (the long watch), T6: the Boarders start */ const d0=L.day; const spd=ngpSpeed(); advance(20); const dd=L.day-d0; globalThis.RT=(globalThis.RT||0)+dd/(DPS*spd); if(isA2(L.sec)&&!globalThis.RA)globalThis.RA=globalThis.RT; if(L.sec===6&&!globalThis.RB)globalThis.RB=globalThis.RT; if(L.sec===13&&!globalThis.RC)globalThis.RC=globalThis.RT; /* Act II route: long watch (RA..RB), Boarders (RB..RC), Arrival (RC..end) */ globalThis.LV=[ngpLv('growth'),ngpLv('drain'),ngpLv('hp'),ngpLv('speed'),ngpLv('wear')].map(x=>x.toFixed(2)).join('/'); if(L.day===d0&&!L.dead){ if(!L.queue.length&&!L.job){L.job=pickFood()?pickFood().id:'algae'} advance(20); if(L.day===d0) die('stuck'); }
    const RT_=(typeof ROUTE!=='undefined'?ROUTE:[1,2,3,4,5,6,7,8,9,10,11,12,13,14]); if(process.env.STOPZ&&RT_.indexOf(L.sec)>=RT_.indexOf(+process.env.STOPZ)&&(L.day-(L.secAt&&L.secAt[L.sec]?L.secAt[L.sec].d:0))>(+process.env.STOPT||400)){fs.writeFileSync(process.env.OUT,JSON.stringify(S));done=true;break;} if(BR==='A'&&S.a2run.done.A) done=true; if(BR!=='A'&&S.a2run.done.C) done=true;
  }
  lives.push(S.gen+':'+Math.round(L.day/DPS)+'s/z'+L.sec+(L.cause==='stuck'?'S':''));
  {const L=S.life; (globalThis.LIVES=globalThis.LIVES||[]).push([S.gen,Math.round(L.day/DPS)+'s',L.sec,(L.cause||'').slice(0,22),Math.round(M.maxHp),(L.strain||1).toFixed(1)]);}
  if(done)break; decant();
}
const days=(S.stats.daysLived+S.life.day)/TPD;
console.log("CAUSES",JSON.stringify(C2));console.log('REAL with overclock: long watch h',((globalThis.RB-globalThis.RA)/3600).toFixed(2),'boarders h',((globalThis.RC-globalThis.RB)/3600).toFixed(2),'arrival h',((globalThis.RT-globalThis.RC)/3600).toFixed(2),'act2 h',((globalThis.RT-globalThis.RA)/3600).toFixed(2),'legacy levels at end',globalThis.LV);console.log('in-game: long watch h',((globalThis.T6-globalThis.T9)*TPD/DPS/3600).toFixed(2),'boarders and arrival h',((days-globalThis.T6)*TPD/DPS/3600).toFixed(2));console.log('branch',BR,'first',JSON.stringify(first),'done',done,'winGen',winGen,'endGen',S.gen,'act2 clones',S.gen-winGen,'act2 h',((days-winDays)*TPD/DPS/3600).toFixed(2),'total h',(days*TPD/DPS/3600).toFixed(2),'honours',S.a2.hon);
console.log(lives.slice(-12).join(' '));
`);
