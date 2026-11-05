# Before-publishing set (build "publishing set"): pause all automation (automated tasks, auto-built gear and
# section runs wait; the queue keeps working), the header switch, screen-reader announcements (live region,
# dialog labels), Log filter chips with the new Records / Automation events, and the welcome-back recap.
import json, time
from playwright.sync_api import sync_playwright
errs=[]
s=json.load(open('/tmp/claude-0/sim/snap12.json'))
s['saved']=int(time.time()*1000)-3*86400000; s['intro']=True; s['seenB']='queue tools'   # last played three days ago
raw=json.dumps(s)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(1000)
    pg.click('[data-menu="continue"]'); pg.wait_for_timeout(300)
    wb=pg.inner_text('#mbox'); print('welcome', wb.replace('\n',' | ')[:300])
    if 'WELCOME BACK' not in wb.upper() or '3 days' not in wb or 'Seedling' not in wb: errs.append('no welcome-back recap')
    if pg.evaluate("()=>document.querySelector('#mbox').getAttribute('aria-label')")!='Welcome back': errs.append('pop-up has no dialog label')
    wn=pg.evaluate("()=>[document.querySelectorAll('#mbox .wnew li').length, S.seenB===buildKey()]"); print('notes in welcome', wn)
    if wn[0] < 2 or not wn[1]: errs.append("What's new not in the welcome pop-up: %s" % wn)
    pg.click('[data-ow="c0"]'); pg.wait_for_timeout(200)
    # pause all automation
    r=pg.evaluate("""()=>{ paused=true; const auto=TASKS.filter(t=>S.auto[t.id]&&practiced(t)&&t.kind!=='job'); const g=ITEMS.filter(i=>S.gauto&&S.gauto[i.id]&&gearPracticed(i));
      const before=[auto.filter(isAuto).length, g.filter(gearAuto).length, !!document.querySelector('[data-autopause]')];
      document.querySelector('[data-autopause]').click();
      const L=S.life; L.queue=[]; L.now=null; const a=active();
      const after=[auto.filter(isAuto).length, g.filter(gearAuto).length, S.set.autoPaused, !!document.querySelector('[data-autopause].on'), a?a.id:null, a?(S.auto[a.id]&&practiced(a)&&a.kind!=='job'):null];
      return {n:auto.length, before, after}; }""")
    print('pause', r)
    if r['n']==0 or r['before'][0]==0 or not r['before'][2]: errs.append('fixture has no automation to pause')
    if r['after'][0]!=0 or r['after'][1]!=0 or not r['after'][2] or not r['after'][3] or r['after'][5]: errs.append('automation not paused')
    q=pg.evaluate("()=>{ const L=S.life; const t=TASKS.find(t=>S.auto[t.id]&&practiced(t)&&t.kind==='act'&&available(t)&&!complete(t)); if(!t) return 'none'; L.queue=[t.id]; const a=active(); return a&&a.id===t.id; }")
    print('queue runs', q)
    if q is not True and q!='none': errs.append('queue stopped while automation paused')
    pg.evaluate("()=>document.querySelector('[data-autopause]').click()")
    if pg.evaluate("()=>S.set.autoPaused"): errs.append('switch did not turn automation back on')
    # announcements
    pg.evaluate("()=>toast('Test message for readers')")
    if 'Test message for readers' not in pg.evaluate("()=>document.querySelector('#sr').textContent"): errs.append('toast not announced')
    if pg.evaluate("()=>document.querySelector('#sr').getAttribute('aria-live')")!='polite': errs.append('no polite live region')
    # log events and chips
    pg.evaluate("()=>{ HOOK.perk({name:'Test record'}); HOOK.practiced(TASKS.find(t=>t.kind==='act')); setTab('log'); }"); pg.wait_for_timeout(200)
    has=pg.evaluate("()=>[...document.querySelectorAll('#v-log .h2')].map(x=>x.textContent)")
    print('log panels', has)
    for want in ['Recent seedlings','Records found','Automation','Ship log']:
        if want not in has: errs.append('log lacks '+want)
    if 'Test record' not in pg.inner_text('#v-log'): errs.append('record event not listed')
    pg.dispatch_event('[data-logf="dead"]', 'click'); pg.wait_for_timeout(100); pg.dispatch_event('[data-logf="story"]', 'click'); pg.wait_for_timeout(200)
    has2=pg.evaluate("()=>[...document.querySelectorAll('#v-log .h2')].map(x=>x.textContent)")
    print('filtered', has2)
    if 'Recent seedlings' in has2 or 'Ship log' in has2 or 'Records found' not in has2: errs.append('log filters wrong')
    if pg.evaluate("()=>[S.ev, Array.isArray(S.evlog), mergeState(JSON.parse(JSON.stringify(S))).ev]")!=[2,True,2]: errs.append('save-version marker S.ev clobbered')
    print('errors', errs); b.close()
