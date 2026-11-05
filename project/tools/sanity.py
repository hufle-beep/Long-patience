import base64,gzip,json,re
from playwright.sync_api import sync_playwright
URL='file:///home/claude/long-patience/index.html'
up=gzip.decompress(base64.b64decode(open('/home/claude/long-patience/saves/hufle2-2026-11-04-1241-clone10.txt').read()[5:].strip())).decode()
snaps={'mending':open('snap16.json').read(),'taproot(old keys)':up,'canopy(old build, ward-lock)':open('snap4old.json').read(),'contested':open('snap7.json').read(),'turnover':open('snap12.json').read()}
BAD=re.compile(r"\b(undefined|NaN|null|[Cc]lones?|[Ss]alvage|[Dd]ecant\w*|Vat Bay|Hydroponics|Engineering Spine|Command Deck|Main Drive|reactor|stardrive|the The|pod bay|power bus|wall panels|main drive|drive is lit|lights it|section.s rest|[Dd]rive ignited|[Ll]it the main drive|drive is lit|drive is first lit)\b")
errs=[]; problems=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    # data checks
    ctx=b.new_context(); pg=ctx.new_page(); pg.on('pageerror', lambda e: errs.append('fresh: '+str(e))); pg.goto(URL); pg.wait_for_timeout(800)
    print('data:', pg.evaluate("""()=>{ const names=TASKS.filter(t=>t.kind!=='build').map(t=>t.z+':'+t.name); const dup=names.filter((n,i)=>names.indexOf(n)!==i);
      const empty=TASKS.filter(t=>!t.name).length + ITEMS.filter(i=>!i.name||!i.desc).length + PERKS.filter(p=>!p.name||!p.desc).length;
      const gd=ITEMS.map(i=>i.name).filter((n,i,a)=>a.indexOf(n)!==i);
      const did=a=>a.map(x=>x.id).filter((x,i,arr)=>arr.indexOf(x)!==i); return {tasks:TASKS.length, items:ITEMS.length, perks:PERKS.length, dupTasks:dup, dupGear:gd, dupIds:did(TASKS).concat(did(ITEMS), did(PERKS)), empty}; }"""))
    for name,raw in [('fresh',None)]+list(snaps.items()):
        ctx=b.new_context(viewport={'width':420,'height':900}); pg=ctx.new_page(); pg.on('pageerror', lambda e,n=name: errs.append(n+': '+str(e)))
        if raw:
            key = "long-patience.slot.1" if 'old keys' in name else "selene.slot.1"; ak = key.replace('slot.1','active-slot')
            pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('%s', %s); localStorage.setItem('%s','1'); sessionStorage.setItem('x','1');}" % (key, json.dumps(raw), ak))
        pg.goto(URL); pg.wait_for_timeout(1000)
        if name=='fresh': pg.click('text=Begin the work cycle')
        pg.evaluate("()=>{ hideModal(); S.intro=true; logTables=true; S.set.deathScreen=false; S.set.deathPause=false; S.set.paused=false; paused=false; setSpeed && setSpeed(5); }") if False else pg.evaluate("()=>{ hideModal(); S.intro=true; logTables=true; S.set.deathScreen=false; S.set.paused=false; paused=false; }")
        if name in ('contested','turnover'):   # built before the Act II reorder: themes revealed by the old rule stay revealed
            print('act II:', name, pg.evaluate("()=>({sec:S.life.sec, lrev:Object.keys(S.a2run.lrev||{}).sort().join(','), done:Object.keys(S.a2run.done||{}).join(',')})"))
        if 'ward-lock' in name:   # a seedling from before the Shattered Bark, already past the Taproot: sealed out of the kindling; tables moved to six Act I columns
            print('ward-lock:', pg.evaluate("()=>({sec:S.life.sec, sealed:!reqMet('wardlift') && T.ignite.req.includes('wardlift'), finCols:(S.hist||[]).every(e=>!e.fin||e.fin.length===6), bestSec:(S.bestSec||[]).length, best:S.best&&S.best.sec, hullv:S.hullv})"))
        g0=pg.evaluate('S.gen'); d0=pg.evaluate('S.stats.daysLived+S.life.day')
        # fast-forward the real game loop a lot (advance in-page), with deaths and decants
        pg.evaluate("()=>{ for(let i=0;i<4000;i++){ if(S.life.dead){ decant(); } if(!S.life.queue.length || !S.life.cur){ const a=TASKS.filter(t=>t.kind=='act'&&available(t)&&!complete(t)).map(t=>t.id); if(a.length) S.life.queue=a.concat(S.life.queue.filter(q=>!a.includes(q))); }   /* a kept queue may hold only later sections' work */ if(!S.life.job){ const f=pickFood(); S.life.job=f?f.id:null; } advance(5); } save(); }")
        pg.wait_for_timeout(1500)  # let the UI tick with the real loop
        print(f'{name}: gen {g0}->{pg.evaluate("S.gen")}, sec {pg.evaluate("S.life.sec")}, ticks +{round(pg.evaluate("S.stats.daysLived+S.life.day")-d0)}')
        for t in ['tasks','map','auto','skills','archive','legacy','log','faq']:
            pg.evaluate(f"()=>{{ setTab('{t}'); }}"); pg.wait_for_timeout(150)
            txt=pg.locator(f'#v-{t}').inner_text() if pg.locator(f'#v-{t}').count() else ''
            for m in set(BAD.findall(txt)): problems.append(f'{name}/{t}: "{m}"')
        hdr=pg.locator('header, .ident').first.inner_text() if pg.locator('header, .ident').count() else ''
        for m in set(BAD.findall(hdr)): problems.append(f'{name}/header: "{m}"')
        for fn in ["showMenu()","showMenu('saves')","showMenu('new')","showSettings()","showIntro()","showDeath()","showActEnd(1, true)","showActEnd(2)"]:
            try:
                pg.evaluate(f"()=>{{ {fn}; }}"); pg.wait_for_timeout(120); txt=pg.locator('#mbox').inner_text()
                for m in set(BAD.findall(txt)): problems.append(f'{name}/{fn}: "{m}"')
            except Exception as e: problems.append(f'{name}/{fn}: EXC {str(e)[:120]}')
        pg.evaluate("hideModal()")
    b.close()
# static check: every data-* marker in the markup has code that reacts to it
src=open('/home/claude/long-patience/index.html').read()
marks=set(re.findall(r'\sdata-([a-z][a-z0-9-]*)(?=[\s=>])', src))
def camel(x): p=x.split('-'); return p[0]+''.join(w.title() for w in p[1:])
PASSIVE={'lock','r','used'}   # labels only, nothing reacts to them by design
orphan=[m for m in sorted(marks-PASSIVE) if not re.search(r"(d\.%s\b|'%s' in d|\.dataset\.%s\b|\[data-%s[\]=])" % (camel(m),camel(m),camel(m),m), src)]
print('data markers without a handler:', orphan or 'none')
# real taps on the pop-up buttons players must press
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); pg.on('pageerror', lambda e: errs.append('taps: '+str(e)))
    pg.goto(URL); pg.wait_for_timeout(800)
    def vis(): return not pg.evaluate("$('#modal').hidden")
    pg.click('#mbox button.pri'); taps=['intro:'+('ok' if not vis() else 'STUCK')]
    pg.evaluate("()=>{ paused=true; S.storyQ=[{t:'Test',x:'Story'}]; showStory(); }"); pg.wait_for_timeout(100); pg.click('#mbox [data-storyok]'); taps.append('story:'+('ok' if not vis() else 'STUCK'))
    pg.evaluate("()=>{ S.life.hp=-1; die('x'); }"); pg.wait_for_timeout(300); g=pg.evaluate('S.gen'); pg.click('#mbox button.pri'); pg.wait_for_timeout(200); taps.append('death:'+('ok' if pg.evaluate('S.gen')==g+1 and not vis() else 'STUCK'))
    pg.evaluate("showMenu()"); pg.click('#mbox [data-menu="continue"]'); taps.append('menu:'+('ok' if not vis() else 'STUCK'))
    pg.evaluate("showSettings()"); pg.click('#mbox [data-settingsclose]'); taps.append('settings:'+('ok' if not vis() else 'STUCK'))
    b.close()
print('pop-up taps:', taps)
print('page errors:', errs or 'none')
print('text problems:', sorted(set(problems)) or 'none')
