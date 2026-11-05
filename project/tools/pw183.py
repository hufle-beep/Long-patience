# Queue tools (build "queue tools", round 5 chunk 4): pause once on first reaching a section; one-shot rows
# (left out of the next seedling's queue); insert point (tap a row number; Next = after the running row);
# long-press the remove button removes every copy; keys 1-5 load presets; Return to the roots on the Now line.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; window.A5=TASKS.filter(t=>t.z===1 && t.kind==='act' && !t.cross).map(t=>t.id); }")
    # first arrival pause, once
    r=pg.evaluate("""()=>{ S.set.paused=false; S.set.pauseCross=false; S.firstAt=Object.assign(S.firstAt||{}, {15:{d:1,r:1,g:S.gen}}); HOOK.crossed(15); const a=S.set.paused;
      S.set.paused=false; HOOK.crossed(15); const b=S.set.paused; S.set.pauseFirst=false; S.firstAt[3]={d:1,r:1,g:S.gen}; HOOK.crossed(3); const c=S.set.paused; S.set.pauseFirst=true;
      S.firstAt[4]={d:1,r:1,g:S.gen-1}; HOOK.crossed(4); const d=S.set.paused; S.set.paused=false; return [a,b,c,d]; }""")
    print('first-arrival pause', r)
    if r!=[True,False,False,False]: errs.append('first-arrival pause: %s' % r)
    # insert point and Next
    r=pg.evaluate("""()=>{ const [a,b2,c]=A5, d=a, L=S.life; L.queue=[a,b2,c]; L.qdone=[]; L.cur=b2; taskKey=''; setTab('tasks'); renderTasks();
      $('[data-qins="0"]').click(); const q1=qIns; document.querySelector('[data-q="'+d+'"]').click(); const after=L.queue.slice(), q2=qIns;
      renderTasks(); $('[data-qinsnext]').click(); const q3=qIns; $('[data-qins="-1"]').click(); return [q1, after.join()==[a,d,b2,c].join(), q2, L.queue.indexOf(b2)===q3, qIns]; }""")
    print('insert point', r)
    if r!=[0,True,1,True,None]: errs.append('insert point: %s' % r)
    # one-shot rows leave the next queue
    r=pg.evaluate("""()=>{ const [a,b2,c]=A5, L=S.life; L.queue=[a,b2,a,c]; L.qdone=[]; L.qonce={}; taskKey=''; renderTasks();
      $('[data-qonce="0"]').click(); const marks=[0,1,2,3].map(qOnceAt); S.set.keepQueue=true; const g=S.gen; die('test'); decant(); hideModal();
      return [marks.join(), S.gen===g+1, S.life.queue.join()===[b2,a,c].join()]; }""")
    print('one-shot', r)
    if r!=['true,false,false,false',True,True]: errs.append('one-shot rows: %s' % r)
    # long-press remove: every copy
    pg.evaluate("()=>{ const [a,b2]=A5, L=S.life; L.queue=[a,b2,a,a]; S.set.paused=true; taskKey=''; setTab('tasks'); renderTasks(); }")
    bx=pg.locator('[data-unqi="0"]'); box=bx.bounding_box()
    pg.mouse.move(box['x']+box['width']/2, box['y']+box['height']/2); pg.mouse.down(); pg.wait_for_timeout(750); pg.mouse.up(); pg.wait_for_timeout(150)
    r=pg.evaluate("()=>S.life.queue.join()===A5[1]")
    print('long-press remove', r)
    if not r: errs.append('long-press remove: %s' % pg.evaluate("()=>S.life.queue"))
    # number keys load presets
    pg.evaluate("()=>{ S.qpresets[1]=[A5[2], A5[3]]; S.qpresets[2]=[]; document.activeElement && document.activeElement.blur(); }")
    pg.keyboard.press('2'); pg.wait_for_timeout(100)
    r=pg.evaluate("()=>S.life.queue.join()===[A5[2],A5[3]].join()")
    print('key 2', r)
    if not r: errs.append('key 2 did not load preset 2: %s' % pg.evaluate("()=>S.life.queue"))
    # Return to the roots on the Now line
    r=pg.evaluate("()=>{ const b=$('.nowrow .rtr'); b.click(); return [b.textContent, S.life.dead]; }")
    pg.wait_for_timeout(3300)
    r2=pg.evaluate("()=>$('.nowrow .rtr').textContent")
    print('now-line button', r, r2)
    if r!=['Tap again',False] or r2!='↺': errs.append('Return to the roots button: %s %s' % (r, r2))
    print('errors', errs)
    b.close()
