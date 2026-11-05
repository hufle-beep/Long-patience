# Runs (build "runs", round 5 chunk 7): best section runs kept at each crossing (no run beaten on every number,
# at most three, pinned ones stay), loadable into the queue; splits against the other games on this device in
# the section header and route info, recorded when a section is judged; Auto tab All on / All off per section.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; window.A5=TASKS.filter(t=>t.z===1 && t.kind==='act' && !t.cross).map(t=>t.id); window.CR=TASKS.find(t=>t.z===1 && t.cross).id; }")
    r=pg.evaluate("""()=>{ const mk=(hp, gen)=>{ S.gen=gen; const L=S.life; L.sec=1; L.secAt={1:{d:0}}; L.day=500; L.hp=hp; L.order=[A5[0],A5[1],CR]; L.done={}; L.order.forEach(id=>L.done[id]=T[id].reps||1); L.salvage=1; L.food.ration=0.5; L.owned={}; S.firstAt={2:{d:1,r:1,g:1}}; enterZone(2,1); };
      S.runs={}; mk(30, 5); const a=S.runs[1].length, q=S.runs[1][0].q.slice();
      mk(20, 6); const b2=S.runs[1].length;          // worse on energy, same otherwise: not kept
      mk(40, 7); const c=S.runs[1].length, top=S.runs[1][0].hp;   // better: replaces the beaten one
      S.runs[1][0].pin=true; mk(45, 8); const d=S.runs[1].map(r=>[r.hp, !!r.pin]);
      return [a, q.includes(CR) && q.includes(A5[0]), b2, c, top, d]; }""")
    print('runs', r)
    if r[0]!=1 or not r[1] or r[2]!=1 or r[3]!=1 or r[4]!=40 or r[5]!=[[40,True],[45,False]]: errs.append('best runs: %s' % r)
    r=pg.evaluate("""()=>{ const L=S.life; L.sec=1; L.queue=[]; L.done={}; taskKey=''; setTab('tasks'); renderTasks(); const rows=document.querySelectorAll('.bruns .brun').length;
      document.querySelector('[data-runload="1:1"]').click(); const q=L.queue.slice(); document.querySelector('[data-runpin="1:1"]').click(); return [rows, q.length>0 && q.includes(A5[0]), S.runs[1][1].pin]; }""")
    print('load/pin', r)
    if r!=[2,True,True]: errs.append('load or pin a run: %s' % r)
    # splits
    r=pg.evaluate("""()=>{ localStorage.setItem(SPLIT_KEY, JSON.stringify({other1:{t:Date.now()-5000, s:{1:{n:7,d:100}}}, other2:{t:Date.now()-9000, s:{1:{n:4,d:90}}}})); S.gid='me';
      S.firstAt={2:{d:1000,r:1,g:9}}; S.tgts={}; tgtCheck(2); const st=JSON.parse(localStorage.getItem(SPLIT_KEY)); const h=tgtHtml(1), info=routeInfoTxt(1);
      return [st.me && st.me.s[1].n, /best 4/.test(h) && /last 7/.test(h), /sslow|sfast|seven/.test(h), /other games here: best 4, last 7/.test(info)]; }""")
    print('splits', r)
    if r!=[9,True,True,True]: errs.append('splits: %s' % r)
    # Auto: all on / all off for a section
    r=pg.evaluate("""()=>{ [A5[0],A5[1]].forEach(id=>{ S.fam[id]=autoFam(T[id]); S.auto[id]=false; }); autoKey=''; setTab('auto'); secFold['au:1']=true; autoKey=''; renderAuto();
      const on=document.querySelector('[data-aubulk="1:1"]'); if(!on) return 'no button'; on.click(); const a=[S.auto[A5[0]], S.auto[A5[1]]]; document.querySelector('[data-aubulk="1:0"]').click(); return a.concat([S.auto[A5[0]], S.auto[A5[1]]]); }""")
    print('bulk', r)
    if r!=[True,True,False,False]: errs.append('auto bulk: %s' % r)
    print('errors', errs)
    b.close()
