# Trigger table and FAQ (build "trigger table"): rules switch off, cover a range of sections, fire for every
# n-th seedling and in priority order (only the highest matching rule fires on one event); the panel reads and
# writes those fields, moves rules up and down; old rules load unchanged. FAQ: search, the entry for the tab you
# came from opens, the Keyboard shortcuts entry comes from the same table the keys use.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ hideModal(); paused=true; S.qpresets[0]=['wake']; S.qpresets[1]=['search']; S.qpresets[2]=['terminal']; }")
    # old rules keep working (migration)
    old=pg.evaluate("()=>mergeState(Object.assign(JSON.parse(JSON.stringify(S)),{qtrig:[{when:'sec',z:2,p:0},{when:'new',p:1,n:1,on:true},{when:'sec',z:2,thru:1,p:0}]})).qtrig")
    print('migrated', old)
    if old!=[{'when':'sec','z':2,'p':0},{'when':'new','p':1},{'when':'sec','z':2,'p':0}]: errs.append('old rules changed by migration')
    def fire(rules, ev, z, gen, sec=1):
        return pg.evaluate("([rules,ev,z,gen,sec])=>{ S.qtrig=rules; S.life.qtf={}; S.gen=gen; S.life.sec=sec; S.life.queue=[]; const got=[]; const h=HOOK.trig; HOOK.trig=(i)=>got.push(i); qTriggers(ev, z); HOOK.trig=h; return got; }", [rules, ev, z, gen, sec])
    r1=fire([{'when':'sec','z':2,'thru':15,'p':0}], 'sec', 15, 1)   # inside the range
    r2=fire([{'when':'sec','z':2,'thru':15,'p':0}], 'sec', 3, 1)    # past it
    r3=fire([{'when':'new','p':1,'on':False},{'when':'new','p':2}], 'new', 1, 1)   # the off rule is skipped
    r4=fire([{'when':'new','p':1,'n':2}], 'new', 1, 3)               # every 2nd seedling: not seedling 3
    r5=fire([{'when':'new','p':1,'n':2}], 'new', 1, 4)
    r6=fire([{'when':'new','p':1},{'when':'new','p':2}], 'new', 1, 1)   # priority: only the first
    print('fires', r1, r2, r3, r4, r5, r6)
    if [r1,r2,r3,r4,r5,r6]!=[[0],[],[1],[],[0],[0]]: errs.append('trigger rules fire wrongly')
    # the panel writes the new fields and moves rules
    pg.evaluate("()=>{ S.gen=1; S.life.sec=1; S.firstAt={2:{d:1,r:1},15:{d:2,r:2}}; S.qtrig=[{when:'new',p:0},{when:'sec',z:2,p:1}]; qTrigPanel(); }")
    pg.select_option('[data-tt="1"]', 'end'); pg.select_option('[data-tn="1"]', '3'); pg.uncheck('[data-ton="0"]')
    pg.click('[data-ow="u1"]'); pg.wait_for_timeout(100)
    pg.select_option('[data-tw="1"]', '15'); pg.wait_for_timeout(100)   # changing When redraws the row
    pg.click('[data-ow="c0"]'); pg.wait_for_timeout(200)
    q=pg.evaluate("()=>S.qtrig"); print('panel', q)
    if q!=[{'when':'sec','z':2,'p':1,'thru':14,'n':3},{'when':'sec','z':15,'p':0,'on':False}]: errs.append('panel did not save the table: '+str(q))
    # FAQ: opening it from Tasks opens that tab's entry; search filters; keys come from HOTKEYS
    pg.evaluate("()=>{ setTab('tasks'); setTab('faq'); }"); pg.wait_for_timeout(200)
    op=pg.evaluate("()=>[...document.querySelectorAll('#v-faq details[open]')].map(d=>d.dataset.faq)")
    print('open', op)
    if 'What are jobs, actions and training?' not in op: errs.append('FAQ did not open the Tasks entry')
    pg.fill('#faq-q', 'shortcut tab'); pg.wait_for_timeout(100)
    vis=pg.evaluate("()=>[...document.querySelectorAll('#v-faq details[data-faq]')].filter(d=>!d.hidden).map(d=>d.dataset.faq)")
    print('search', vis)
    if vis!=['Keyboard shortcuts']: errs.append('search shows '+str(vis))
    pg.fill('#faq-q', 'zzqx'); pg.wait_for_timeout(100)
    if pg.evaluate("()=>document.querySelector('#faq-none').hidden"): errs.append('no "no match" note')
    pg.fill('#faq-q', ''); pg.evaluate("()=>{ document.activeElement.blur(); setTab('tasks'); }")
    keys=pg.evaluate("()=>document.querySelector('.fkeys')===null && [...document.querySelectorAll('#v-faq details')].length")
    pg.keyboard.press('ArrowRight'); pg.wait_for_timeout(100)
    t1=pg.evaluate("()=>tab"); p0=pg.evaluate("()=>!!S.set.paused"); pg.keyboard.press('p'); p1=pg.evaluate("()=>!!S.set.paused")
    print('keys', t1, p0, p1)
    if t1!='map' or p0==p1: errs.append('hotkeys broken')
    print('errors', errs); b.close()
