# Route overview, icons and Credits (build "route and icons"): on a fresh game the route shows the first
# section and '?' for the rest, with no later section names anywhere in it; a late save shows the reached ones
# and a tap gives year, crossing cost and danger. Icons on tabs, section headers, task groups and the death
# screen; the Credits panel in Settings names the icon authors, the licence, the fonts and ZzFX.
import json
from playwright.sync_api import sync_playwright
errs=[]
raw=open('/tmp/claude-0/sim/snap16.json').read()
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ hideModal(); paused=true; setTab('map'); }"); pg.wait_for_timeout(200)
    r=pg.evaluate("()=>{ const m=document.querySelector('.rmap'); return {txt:m.textContent, unk:m.querySelectorAll('.rn.unk').length, known:m.querySelectorAll('[data-routez]').length, names:ZONES.filter(z=>z.id!==1).map(z=>z.name)}; }")
    leak=[n for n in r['names'] if n in r['txt']]
    print('fresh route', r['known'], r['unk'], leak)
    if r['known']!=1 or r['unk']!=15 or leak: errs.append('fresh route shows or names unreached sections')
    ic=pg.evaluate("()=>({tabs:document.querySelectorAll('#tabs .tic').length, tabsText:[...document.querySelectorAll('#tabs [data-tab]')].map(b=>b.textContent.trim()).join(','), gi:Object.keys(GI).length})")
    print('icons', ic)
    if ic['tabs']<8 or ic['tabsText']!='Tasks,Map,Auto,Mastery,Archive,Legacy,Log,FAQ': errs.append('tab icons or labels wrong')
    pg.evaluate("()=>setTab('tasks')"); pg.wait_for_timeout(200)
    if not pg.evaluate("()=>!!document.querySelector('#v-tasks .zh h2 .gi') && !!document.querySelector('#v-tasks .sub .gi')"): errs.append('no icons on the section header or task groups')
    pg.evaluate("()=>{ S.life.hp=0; S.life.dead=true; S.life.cause='Ran out of energy'; showDeath(); }"); pg.wait_for_timeout(200)
    if not pg.evaluate("()=>!!document.querySelector('#mbox .dcause .dico')"): errs.append('no death-cause icon')
    pg.evaluate("()=>{ hideModal(); showSettings('x'); }"); pg.wait_for_timeout(200)
    cr=pg.inner_text('#mbox')
    for w in ['Lorc','Delapouite','Skoll','CC BY 3.0','game-icons.net','Frank Force','Open Font License']:
        if w not in cr: errs.append('Credits lack '+w)
    pg.close()
    pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{ hideModal(); paused=true; setTab('map'); }"); pg.wait_for_timeout(200)
    late=pg.evaluate("()=>({known:document.querySelectorAll('.rmap [data-routez]').length, cur:(document.querySelector('.rmap .rn.cur')||{}).textContent})")
    pg.dispatch_event('[data-routez="16"]', 'click'); pg.wait_for_timeout(200)
    t=pg.evaluate("()=>document.querySelector('#toasts').innerText")
    print('late route', late, t)
    if late['known']!=14 or late['cur']!='The Mending': errs.append('late route wrong')
    if 'Year 478' not in t or 'danger' not in t or 'crossing in costs' not in t: errs.append('route tap info wrong')
    print('errors', errs); b.close()
