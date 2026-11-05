# Clearer buttons (build "clearer buttons"): Recharge and Repair turn yellow when they can be used; New game is yellow
# on a fresh launch only; plain buttons get a fill and a clearer border; the queue "+" is amber; presets are compact rows
# under the queue; the Sap cells warning is on short lines; pop-ups focus themselves; no pace when nothing gets done;
# the Auto tab's explanation folds (kept on the device).
import json
from playwright.sync_api import sync_playwright
errs=[]
raw=open('/tmp/claude-0/sim/snap7.json').read()
AMBER='rgb(240, 160, 60)'
with sync_playwright() as p:
    b=p.chromium.launch()
    # fresh launch: New game is the yellow one
    pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ localStorage.removeItem('selene.slot.1'); showMenu(); }"); pg.wait_for_timeout(200)
    if 'pri' not in pg.get_attribute('#mbox [data-menu="new"]','class'): errs.append('New game not yellow on a fresh launch')
    pg.close()
    pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    m=pg.evaluate("()=>[document.querySelector('#mbox [data-menu=\"new\"]').className, document.activeElement===$('#mbox'), getComputedStyle(document.querySelector('#mbox [data-menu=\"saves\"]')).backgroundColor, getComputedStyle(document.querySelector('#mbox [data-menu=\"saves\"]')).fontSize]")
    print('menu', m)
    if 'pri' in m[0]: errs.append('New game yellow although a save can be continued')
    if not m[1]: errs.append('pop-up did not take focus itself')
    if m[2] in ('rgba(0, 0, 0, 0)','transparent'): errs.append('plain button has no fill')
    if m[3]!='15px': errs.append('menu button text not 15px: '+m[3])
    pg.evaluate("()=>{ hideModal(); paused=true; S.set.paused=true; S.life.food.ration=10; S.life.hp=M.maxHp*0.4; S.life.mcd={}; S.life.salvage=40; S.life.rcd=0; S.life.shipWear=2; }"); pg.wait_for_timeout(700)
    r=pg.evaluate("()=>[$('#eatb').disabled, getComputedStyle($('#eatb')).backgroundColor, $('#repb').disabled, getComputedStyle($('#repb')).backgroundColor, getComputedStyle($('#t-ratt')).whiteSpace, $('#t-ratt').textContent.split('\\n').length]")
    print('recharge/repair/warning', r)
    if r[0] or r[1]!=AMBER: errs.append('Recharge not yellow when ready: %s' % r[:2])
    if r[2] or r[3]!=AMBER: errs.append('Repair not yellow when possible: %s' % r[2:4])
    if r[4]!='pre-line' or r[5]<2: errs.append('warning not on short lines')
    pg.evaluate("()=>{ S.life.food.ration=0; S.life.salvage=0; }"); pg.wait_for_timeout(700)
    r2=pg.evaluate("()=>[$('#eatb').disabled, getComputedStyle($('#eatb')).backgroundColor]")
    if not r2[0] or r2[1]==AMBER: errs.append('disabled Recharge still yellow: %s' % r2)
    pg.evaluate("()=>{ S.life.queue=[]; taskKey=''; }"); pg.wait_for_timeout(500)
    q=pg.evaluate("""()=>{ const t=document.querySelector('.tq:not(.in)'); const pre=document.querySelector('.qpre'), rows=[...document.querySelectorAll('.qpre .qps:not(.qtx)')];
      return [t?getComputedStyle(t).color:null, rows.length, Math.max(...rows.map(r=>r.offsetHeight)), pre.getBoundingClientRect().top > document.querySelector('.qmain').getBoundingClientRect().bottom - 1]; }""")
    print('plus/presets', q)
    if q[0]!=AMBER: errs.append('queue + not amber: %s' % q[0])
    if q[1]!=5 or q[2]>40 or not q[3]: errs.append('presets not compact rows under the queue: %s' % q)
    pc=pg.evaluate("()=>fcRateTxt({end:'dead', day0:0, endDay:TPD*60, done0:5, s:{life:{done:{a:5}}}})")
    if pc!='': errs.append('pace shown with nothing done: '+pc)
    # Auto intro folds, opens, kept
    pg.evaluate("()=>{ setTab('auto'); }"); pg.wait_for_timeout(300)
    a=pg.evaluate("()=>[!!document.querySelector('#v-auto [data-secfold=\"au:intro\"]'), document.querySelector('#v-auto').innerText.includes('Tasks finished often enough')]")
    if a!=[True,False]: errs.append('Auto intro not folded by default: %s' % a)
    pg.dispatch_event('#v-auto [data-secfold="au:intro"]','click'); pg.wait_for_timeout(300)
    a2=pg.evaluate("()=>[document.querySelector('#v-auto').innerText.includes('Tasks finished often enough'), localStorage.getItem('selene.secfold.v1')]")
    print('auto intro', a2)
    if not a2[0] or 'au:intro' not in (a2[1] or ''): errs.append('Auto intro did not open or was not kept: %s' % a2)
    b.close()
print('errors', errs)
