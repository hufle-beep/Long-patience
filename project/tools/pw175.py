# Queue history (build "queue history"): each seedling's starting queue is kept on the last 10 run-history entries and
# "Load queue" in the Log puts it back (Undo works); consecutive deaths in one section of one cause share a row; the
# setting "Pause when the queue is finished" pauses once the last own row is worked off (not when cleared by hand);
# the queue line gives the forecast's tasks per real minute; the Mastery tab shows each task's speed factors.
import json
from playwright.sync_api import sync_playwright
errs=[]
raw=open('/tmp/claude-0/sim/snap7.json').read()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=false; S.intro=true; S.set.deathScreen=true; }")
    # starting queue recorded at sprout, kept in history at death
    r=pg.evaluate("""()=>{ const ids=TASKS.filter(t=>available(t)&&!complete(t)&&t.kind==='act').slice(0,2).map(t=>t.id);
      S.life.queue=ids.slice(); S.set.keepQueue=true; die('Test'); decant(); const q0=S.life.q0.slice();
      die('Test'); const e=S.hist[S.hist.length-1]; return [ids, q0, e.q||null, e.g]; }""")
    print('starting queue', r)
    if not r[1] or r[2]!=r[1]: errs.append('starting queue not kept in history: %s' % r)
    pg.evaluate("()=>{ for (let i=0;i<14;i++){ S.hist.push({g:900+i, sec:2, z:2, d:100, r:10, cause:'Ran out of energy', q:['x']}); if (S.hist.length>10) delete S.hist[S.hist.length-11].q; } }")
    kept=pg.evaluate("()=>S.hist.filter(e=>e.q).length")
    if kept>10: errs.append('more than 10 starting queues kept: %d' % kept)
    # merged rows and Load queue in the Log
    pg.evaluate("""()=>{ S.hist=S.hist.slice(0,-14); const q=S.life.queue.length?S.life.queue.slice():[TASKS.find(t=>available(t)&&!complete(t)&&t.kind==='act').id];
      for (let i=0;i<4;i++) S.hist.push({g:500+i, sec:2, z:2, d:100+i*10, r:10+i, cause:'Ran out of energy', q:q});
      S.hist.push({g:504, sec:2, z:2, d:90, r:9, cause:'Killed by a hazard'});
      if (S.life.dead) { decant(); } hideModal(); paused=false; logTables=true; logKey=''; setTab('log'); }""")
    pg.wait_for_timeout(300)
    rows=pg.evaluate("()=>{ const tb=[...document.querySelectorAll('#v-log table.dt')].find(x=>x.innerText.toLowerCase().includes('furthest')); return tb?[...tb.querySelectorAll('tbody tr:not(.havg)')].map(r=>r.cells[0].firstChild.textContent):[]; }")
    print('rows', rows[:4])
    if not rows or rows[0]!='504' or rows[1]!='500–503': errs.append('death rows not merged: %s' % rows[:4])
    pg.evaluate("()=>{ S.life.queue=[]; }")
    pg.click('[data-histq="503"]'); pg.wait_for_timeout(200)
    lq=pg.evaluate("()=>[S.life.queue.length, !!qUndo]")
    print('loaded queue', lq)
    if lq[0]<1 or not lq[1]: errs.append('Load queue failed: %s' % lq)
    # pause when the queue is finished
    pg.evaluate("""()=>{ setTab('tasks'); S.set.pauseQueue=true; S.set.paused=false; const t=TASKS.find(x=>available(x)&&!complete(x)&&x.kind==='act'&&(x.reps||1)===1);
      S.life.queue=[t.id]; S.life.prog[t.id]=t.days-0.5; S.life.hp=M.maxHp; S.set.autoScav=false; S.set.autoRepair=false; S.life.salvage=M.salCap; S.life.shipWear=0; S.set.autoPaused=true; qFin=null; }""")
    pg.wait_for_timeout(2500)
    pq=pg.evaluate("()=>[S.set.paused, S.life.queue.length]")
    print('pause when finished', pq)
    if pq[0] is not True: errs.append('did not pause when the queue finished: %s' % pq)
    pg.evaluate("()=>{ S.set.paused=false; const t=TASKS.find(x=>available(x)&&!complete(x)&&x.kind==='act'); S.life.queue=[t.id]; qFin=null; }"); pg.wait_for_timeout(400)
    pg.evaluate("()=>{ S.life.queue=[]; }"); pg.wait_for_timeout(600)
    if pg.evaluate("()=>S.set.paused"): errs.append('paused after clearing the queue by hand')
    # speed breakdown on the Mastery tab
    pg.evaluate("()=>{ setTab('skills'); renderSkills(); }"); pg.wait_for_timeout(200)
    bd=pg.evaluate("()=>{ const el=document.querySelector('#v-skills .skbd'); return el?el.textContent:''; }")
    print('breakdown', bd)
    if not bd.startswith('Speed ×') or 'familiarity ×' not in bd: errs.append('no speed breakdown')
    # pace: tasks per real minute over the forecast life (shown on the queue line)
    pc=pg.evaluate("()=>[fcRateTxt({end:'dead', day0:0, endDay:TPD*60, done0:2, s:{life:{done:{a:10, b:4}}}}), fcRateTxt({end:'idle', day0:0, endDay:2, done0:0, s:{life:{done:{a:3}}}}), realSecs(TPD*60)]")
    print('pace', pc)
    if 'tasks per real minute' not in pc[0] or pc[1]!='': errs.append('pace text wrong: %s' % pc)
    if '+ fcRateTxt(fc)' not in open('/home/claude/long-patience/index.html',encoding='utf8').read(): errs.append('pace not on the queue line')
    b.close()
print('errors', errs)
