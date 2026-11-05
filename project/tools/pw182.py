# Phone comfort and accessibility (build "phone comfort", round 5 chunk 3): text size (page zoom, kept on the
# device), brighter red text, scroll position kept per tab, a close X on pop-ups with a way out (not the death
# screen), tooltips hide on a tab switch or when their element is gone, energy bar as a progressbar, queue rows
# announce their step, the running row is marked and a long queue follows it, arrow keys inside the Log chips.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':800}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    # close X on the intro (its Continue) -> closes
    r=pg.evaluate("()=>[!!$('#mbox .mx'), $('#mbox .mx') && $('#mbox .mx').getAttribute('aria-label')]")
    print('intro X', r)
    if not r[0]: errs.append('no close X on the intro')
    pg.click('#mbox .mx'); pg.wait_for_timeout(200)
    if not pg.evaluate("()=>$('#modal').hidden"): errs.append('X did not close the intro')
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; }")
    # text size
    pg.evaluate("()=>showSettings('game')"); pg.wait_for_timeout(200)
    pg.click('[data-tsize="130"]'); pg.wait_for_timeout(150)
    r=pg.evaluate("()=>[document.documentElement.style.zoom, localStorage.getItem('selene.textsize.v1'), $('[data-tsize=\"130\"]').classList.contains('on'), !!$('#mbox .mx')]")
    print('text size', r)
    if r!=['1.3','130',True,True]: errs.append('text size: %s' % r)
    pg.click('#mbox .mx'); pg.wait_for_timeout(150)
    if not pg.evaluate("()=>$('#modal').hidden"): errs.append('X did not close Settings')
    pg.reload(); pg.wait_for_timeout(900)
    z=pg.evaluate("()=>document.documentElement.style.zoom")
    if z not in ('1.3',): errs.append('text size not applied after reload: %r' % z)
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; setTextSize(100); }")
    if pg.evaluate("()=>document.documentElement.style.zoom")!='': errs.append('100% should clear the zoom')
    # death screen has no X
    has=pg.evaluate("()=>{ showModal('<h2>Seedling 1 has died</h2><button class=\"btn pri\" data-decant>Sprout</button>'); const r=!!$('#mbox .mx'); hideModal(); return r; }")
    if has: errs.append('death-like pop-up got a close X')
    # red text contrast
    c=pg.evaluate("()=>{ const d=document.createElement('div'); d.className='qrow fnr'; d.innerHTML='<small class=\"qfc\">x</small>'; document.body.appendChild(d); const c=getComputedStyle(d.querySelector('.qfc')).color; d.remove(); return c; }")
    print('red text', c)
    if c!='rgb(242, 134, 111)': errs.append('red text colour: '+c)
    # energy progressbar
    r=pg.evaluate("()=>{ S.life.hp=M.maxHp*0.42; updateHud(); const pb=$('#b-hp').parentElement; return [pb.getAttribute('role'), pb.getAttribute('aria-valuenow')]; }")
    print('energy bar', r)
    if r!=['progressbar','42']: errs.append('energy progressbar: %s' % r)
    # queue: step labels, running row marked, long list follows it
    r=pg.evaluate("""()=>{ const L=S.life, acts=TASKS.filter(t=>t.z===1 && t.kind==='act' && !t.cross).map(t=>t.id), a=acts[0], b2=acts[1];
      L.queue=[]; for(let i=0;i<24;i++) L.queue.push(a); L.queue.push(b2); L.cur=b2; L.qskip={}; L.qskip[a]=1; taskKey=''; setTab('tasks'); renderTasks(); updateTasks(); qHandT=-1e9; qFollowI=-1; updateQueueFc();
      const rows=[...document.querySelectorAll('.qlist .qrow[data-qid]')], last=rows[rows.length-1], list=last.closest('.qlist'), lr=list.getBoundingClientRect(), rr=last.getBoundingClientRect();
      const qn=rows[0].querySelector('.qn'); return [(qn.getAttribute('aria-label')||qn.textContent).replace(/:.*/,'').replace(/^Step 1\.?$/,'Step 1.'), last.classList.contains('qnow'), last.getAttribute('aria-current'), list.classList.contains('long'), list.scrollTop>0, rr.top>=lr.top-1 && rr.bottom<=lr.bottom+1]; }""")
    print('queue', r)
    if r!=['Step 1.',True,'step',True,True,True]: errs.append('queue follow/labels: %s' % r)
    # hand scrolling stops following
    r=pg.evaluate("""()=>{ const list=$('.qlist'); list.scrollTop=0; qHandT=performance.now(); qFollowI=-1; updateQueueFc(); return list.scrollTop; }""")
    if r!=0: errs.append('followed although scrolled by hand: %s' % r)
    # scroll kept per tab
    pg.evaluate("()=>{ document.body.style.minHeight='4000px'; window.scrollTo(0, 700); }"); pg.wait_for_timeout(100)
    y0=pg.evaluate("()=>window.scrollY")
    pg.evaluate("()=>setTab('log')"); pg.wait_for_timeout(100); y1=pg.evaluate("()=>window.scrollY")
    pg.evaluate("()=>setTab('tasks')"); pg.wait_for_timeout(100); y2=pg.evaluate("()=>window.scrollY")
    print('scroll', y0, y1, y2)
    if not (y0>600 and y1<y0 and abs(y2-y0)<2): errs.append('scroll per tab: %s %s %s' % (y0,y1,y2))
    pg.evaluate("()=>{ document.body.style.minHeight=''; window.scrollTo(0,0); }")
    # tooltip hides on a tab switch and when its element goes away
    r=pg.evaluate("""()=>{ const card=$('.task[data-id]'); tipShow(card); const a=!tipEl.hidden; setTab('map'); const b=tipEl.hidden; setTab('tasks');
      const x=document.createElement('button'); x.dataset.tip='hello'; document.body.appendChild(x); tipShow(x); const c=!tipEl.hidden; x.remove(); tipCheck(); return [a,b,c,tipEl.hidden]; }""")
    print('tooltip', r)
    if r!=[True,True,True,True]: errs.append('tooltip hiding: %s' % r)
    # arrow keys in the Log chips stay in the chips
    pg.evaluate("()=>{ logKey=''; setTab('log'); }"); pg.wait_for_timeout(200)
    pg.focus('.lchips button'); pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(100)
    r=pg.evaluate("()=>[tab, document.activeElement && document.activeElement.dataset.logf, [...document.querySelectorAll('.lchips button')].map(b=>b.dataset.logf)]")
    print('chips', r)
    if r[0]!='log' or r[1]!=r[2][1]: errs.append('chip arrow keys: %s' % r)
    print('errors', errs)
    b.close()
