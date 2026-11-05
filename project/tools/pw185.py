# Guidance (build "guidance", round 5 chunk 6): controls revealed with progress; next-step line until the
# Heartwood (dismissable); first-hour hints in the Log (once, idle with a cooldown); What's new once per build for
# a save that saw an older build (not for new games); tuned-up-to note on the Map; journal; new-this-seedling marks.
import json
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ $('#mbox [data-close]') && $('#mbox [data-close]').click(); }"); pg.wait_for_timeout(200)
    r=pg.evaluate("()=>[S.seenB, buildKey()]")
    if r[0]!=r[1]: errs.append('new game did not record the build: %s' % r)
    # reveal level 0 hides the insert bar, presets and advanced settings
    pg.evaluate("()=>{ paused=true; const A=TASKS.filter(t=>t.z===1&&t.kind==='act'&&!t.cross).map(t=>t.id); S.life.queue=A.slice(0,2); taskKey=''; setTab('tasks'); renderTasks(); updateHud(); uiN++; }"); pg.wait_for_timeout(300)
    r=pg.evaluate("()=>[document.documentElement.dataset.rv, getComputedStyle($('.qinsbar')).display, getComputedStyle($('.qpre')).display]")
    print('fresh reveal', r)
    if r!=['0','none','none']: errs.append('fresh game shows advanced queue controls: %s' % r)
    r=pg.evaluate("()=>{ S.gen=3; S.firstAt={2:{d:1,r:1,g:2}}; uiN++; return 1; }"); pg.wait_for_timeout(300)
    r=pg.evaluate("()=>{ showSettings('game'); const rows=[...document.querySelectorAll('#mbox .need2')].map(x=>getComputedStyle(x).display); hideModal(); return [document.documentElement.dataset.rv, getComputedStyle($('.qinsbar')).display, rows]; }")
    print('level 2', r)
    if r[0]!='2' or r[1]=='none' or not r[2] or any(x=='none' for x in r[2]): errs.append('level 2 still hides controls: %s' % r)
    # next-step line, then dismiss
    r=pg.evaluate("()=>{ S.firstAt={2:{d:1,r:1,g:2}}; S.noNext=0; nxaT=0; taskKey=''; renderTasks(); updateTasks(); const a=$('#nstep').textContent; $('[data-nonext]').click(); nxaT=0; updateTasks(); return [a, $('#nstep').textContent]; }")
    print('next step', r)
    if 'Next step' not in r[0] or r[1]!='': errs.append('next-step line: %s' % r)
    r=pg.evaluate("()=>{ S.noNext=0; S.firstAt[3]={d:1,r:1,g:3}; nxaT=0; updateTasks(); const t=$('#nstep').textContent; delete S.firstAt[3]; return t; }")
    if r!='': errs.append('next-step line still shown after the Heartwood')
    # hints: once; idle with cooldown; panel and chip
    r=pg.evaluate("""()=>{ S.hints={}; S.evlog=[]; hint('death1'); hint('death1'); S.stats.played=100; hint('idle'); S.stats.played=200; hint('idle'); S.stats.played=800; hint('idle');
      const n=S.evlog.filter(e=>e.k==='hint').length; logKey=''; setTab('log'); const panel=[...document.querySelectorAll('#v-log .h2')].some(x=>x.textContent==='Hints'), chip=!!$('[data-logf="hint"]'); return [n, panel, chip]; }""")
    print('hints', r)
    if r!=[3,True,True]: errs.append('hints: %s' % r)
    # journal and new marks
    r=pg.evaluate("""()=>{ S.log=[{g:S.gen-1,a:1,t:'Old entry',x:'old'},{g:S.gen,a:2,t:'New entry',x:'new'}]; logKey=''; renderLog();
      const marks=document.querySelectorAll('#v-log .le.lnew').length; $('[data-journal]').click(); const j=$('#mbox .journal').textContent; const x=!!$('#mbox .mx'); $('#mbox [data-jclose]').click();
      return [marks, /Old entry/.test(j) && /New entry/.test(j), x, $('#modal').hidden]; }""")
    print('journal', r)
    if r!=[1,True,True,True]: errs.append('journal / marks: %s' % r)
    # map note
    r=pg.evaluate("()=>{ mapKey=''; setTab('map'); return $('#v-map .tuned') && $('#v-map .tuned').textContent; }")
    if not r or 'Taproot' not in r: errs.append('no tuned note on the Map: %r' % r)
    # what's new: a save that saw 'queue tools' gets the notes after it, once
    r=pg.evaluate("""()=>{ setTab('tasks'); S.seenB='queue tools'; S.intro=true; startGame(); const t=!$('#modal').hidden && $('#mbox h2').textContent, n=document.querySelectorAll('#mbox .wnew li').length; hideModal(); paused=false; startGame(); const again=!$('#modal').hidden; return [t, n === BUILD_NOTES.length - 1 - BUILD_NOTES.findIndex(x=>x[0]==='queue tools'), again, S.seenB === buildKey()]; }""")
    print('whats new', r)
    if r!=['What’s new', True, False, True]: errs.append("what's new: %s" % r)
    print('errors', errs)
    b.close()
