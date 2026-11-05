# Information (build "information", round 5 chunk 5): timeline strip per seedling (header and death screen),
# pinned checklist (tasks and gear, from Edit list), ETA and step names in card tooltips, time saved by
# familiarity on cards, drain breakdown on the energy line, formulas setting, what a route section still holds.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; window.A5=TASKS.filter(t=>t.z===1 && t.kind==='act' && !t.cross).map(t=>t.id); }")
    # timeline: run some work, then the header strip and the death screen show it
    r=pg.evaluate("""()=>{ const L=S.life; L.queue=A5.slice(0,3); for(let i=0;i<400 && !L.dead;i++) step(2);
      setTab('tasks'); taskKey=''; renderTasks(); nxaT=0; updateTasks(); const segs=(L.tl||[]).length, strip=document.querySelectorAll('#tlnow .tl i').length;
      const tip=document.querySelector('#tlnow .tl i') && document.querySelector('#tlnow .tl i').dataset.tip; return [segs>0, strip>0, !!tip && / in-game$/.test(tip)]; }""")
    print('timeline', r)
    if r!=[True,True,True]: errs.append('timeline strip: %s' % r)
    # card tooltip: ETA lines and saved time; energy tooltip: drain parts
    r=pg.evaluate("""()=>{ const c0=[...document.querySelectorAll('.task.act[data-id]')].map(e=>T[e.dataset.id]).find(t=>!t.cross && !t.legacy), t=c0; S.fam[t.id]=famNeed(t)*0.3; S.prac[t.id]=0; M=mods(); taskKey=''; renderTasks(); updateTasks();
      const card=document.querySelector('.task[data-id="'+t.id+'"]'), txt=tipText(card), pp=card.querySelector('.pp').innerHTML, en=tipText($('#tipenergy'));
      return [/Practiced/.test(txt), /Skilled \\(×5\\) in about \\d+ completion/.test(txt), /Automation: /.test(txt), /Familiarity saves/.test(txt), /psv/.test(pp), /^Energy[\\s\\S]*Drain [\\d.]+ energy per in-game second/.test(en), /Formula/.test(en)]; }""")
    print('tooltips', r)
    if r!=[True,True,True,True,True,True,False]: errs.append('tooltips: %s' % r)
    r=pg.evaluate("()=>{ S.set.showFormulas=true; const a=/Formula/.test(tipText($('#tipenergy'))), b2=/Formula: speed/.test(tipText(document.querySelector('.task[data-id]'))); S.set.showFormulas=false; return [a,b2]; }")
    print('formulas', r)
    if r!=[True,True]: errs.append('formulas: %s' % r)
    # pins: from Edit list, task and gear; checklist text; unpin
    r=pg.evaluate("""()=>{ editList=true; taskKey=''; renderTasks(); const tb=[...document.querySelectorAll('[data-tpin]')].find(x=>!/^g:/.test(x.dataset.tpin)), cross=T[tb.dataset.tpin]; S.pins=[];
      tb.click(); const g=document.querySelector('[data-tpin^="g:"]'); if (g) g.click();
      editList=false; taskKey=''; renderTasks(); nxaT=0; updateTasks();
      const pins=[...document.querySelectorAll('#pinbar .pin')].map(x=>x.textContent);
      document.querySelector('#pinbar [data-unpin="'+cross.id+'"]').click(); nxaT=0; updateTasks();
      return [S.pins.length, pins.length, /needs|ready|done/.test(pins[0]||''), !!g, document.querySelectorAll('#pinbar .pin').length]; }""")
    print('pins', r)
    if r[0]!=1 or r[1]!=2 or not r[2] or not r[3] or r[4]!=1: errs.append('pins: %s' % r)
    # Mastery tab: step name next to the speed breakdown
    r=pg.evaluate("()=>{ setTab('skills'); return [...document.querySelectorAll('.fstep')].map(x=>x.textContent).slice(0,2); }")
    print('mastery steps', r)
    if 'Practiced' not in r: errs.append('no step name on the Mastery tab: %s' % r)
    # route: what a section still holds
    r=pg.evaluate("()=>[routeInfoTxt(1), routeInfoTxt(5)]")
    print('route', r)
    if 'left:' not in r[0] or r[1]!='': errs.append('route left text: %s' % r)
    # death screen strip
    r=pg.evaluate("()=>{ setTab('tasks'); die('test'); showDeath(); return [document.querySelectorAll('#mbox .tl i').length>0, !$('#mbox .mx')]; }")
    print('death screen', r)
    if r!=[True,True]: errs.append('death screen timeline: %s' % r)
    print('errors', errs)
    b.close()
