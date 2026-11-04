import base64,gzip,json,re
from playwright.sync_api import sync_playwright
URL='file:///home/claude/long-patience/index.html'
up=gzip.decompress(base64.b64decode(open('/home/claude/long-patience/saves/hufle2-2026-11-04-1241-clone10.txt').read()[5:].strip())).decode()
snaps={'taproot(old keys)':up,'contested':open('snap7.json').read(),'turnover':open('snap12.json').read()}
BAD=re.compile(r"\b(undefined|NaN|null|[Cc]lones?|[Ss]alvage|[Dd]ecant\w*|Vat Bay|Hydroponics|Engineering Spine|Command Deck|Main Drive|reactor|stardrive|the The)\b")
errs=[]; problems=[]
with sync_playwright() as p:
    b=p.chromium.launch()
    # data checks
    ctx=b.new_context(); pg=ctx.new_page(); pg.on('pageerror', lambda e: errs.append('fresh: '+str(e))); pg.goto(URL); pg.wait_for_timeout(800)
    print('data:', pg.evaluate("""()=>{ const names=TASKS.filter(t=>t.kind!=='build').map(t=>t.z+':'+t.name); const dup=names.filter((n,i)=>names.indexOf(n)!==i);
      const empty=TASKS.filter(t=>!t.name).length + ITEMS.filter(i=>!i.name||!i.desc).length + PERKS.filter(p=>!p.name||!p.desc).length;
      const gd=ITEMS.map(i=>i.name).filter((n,i,a)=>a.indexOf(n)!==i);
      return {tasks:TASKS.length, items:ITEMS.length, perks:PERKS.length, dupTasks:dup, dupGear:gd, empty}; }"""))
    for name,raw in [('fresh',None)]+list(snaps.items()):
        ctx=b.new_context(viewport={'width':420,'height':900}); pg=ctx.new_page(); pg.on('pageerror', lambda e,n=name: errs.append(n+': '+str(e)))
        if raw:
            key = "long-patience.slot.1" if 'old keys' in name else "selene.slot.1"; ak = key.replace('slot.1','active-slot')
            pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('%s', %s); localStorage.setItem('%s','1'); sessionStorage.setItem('x','1');}" % (key, json.dumps(raw), ak))
        pg.goto(URL); pg.wait_for_timeout(1000)
        if name=='fresh': pg.click('text=Begin the work cycle')
        pg.evaluate("()=>{ hideModal(); S.intro=true; logTables=true; S.set.deathScreen=false; S.set.deathPause=false; S.set.paused=false; paused=false; setSpeed && setSpeed(5); }") if False else pg.evaluate("()=>{ hideModal(); S.intro=true; logTables=true; S.set.deathScreen=false; S.set.paused=false; paused=false; }")
        g0=pg.evaluate('S.gen'); d0=pg.evaluate('S.stats.daysLived+S.life.day')
        # fast-forward the real game loop a lot (advance in-page), with deaths and decants
        pg.evaluate("()=>{ for(let i=0;i<4000;i++){ if(S.life.dead){ decant(); } if(!S.life.queue.length){ S.life.queue=TASKS.filter(t=>t.kind=='act'&&available(t)&&!complete(t)).map(t=>t.id); } if(!S.life.job){ const f=pickFood(); S.life.job=f?f.id:null; } advance(5); } save(); }")
        pg.wait_for_timeout(1500)  # let the UI tick with the real loop
        print(f'{name}: gen {g0}->{pg.evaluate("S.gen")}, sec {pg.evaluate("S.life.sec")}, ticks +{round(pg.evaluate("S.stats.daysLived+S.life.day")-d0)}')
        for t in ['tasks','map','auto','skills','archive','legacy','log','faq']:
            pg.evaluate(f"()=>{{ setTab('{t}'); }}"); pg.wait_for_timeout(150)
            txt=pg.locator(f'#v-{t}').inner_text() if pg.locator(f'#v-{t}').count() else ''
            for m in set(BAD.findall(txt)): problems.append(f'{name}/{t}: "{m}"')
        hdr=pg.locator('header, .ident').first.inner_text() if pg.locator('header, .ident').count() else ''
        for m in set(BAD.findall(hdr)): problems.append(f'{name}/header: "{m}"')
        for fn in ["showMenu()","showMenu('saves')","showMenu('new')","showSettings()","showIntro()","showDeath()","showWin()"]:
            try:
                pg.evaluate(f"()=>{{ {fn}; }}"); pg.wait_for_timeout(120); txt=pg.locator('#mbox').inner_text()
                for m in set(BAD.findall(txt)): problems.append(f'{name}/{fn}: "{m}"')
            except Exception as e: problems.append(f'{name}/{fn}: EXC {str(e)[:120]}')
        pg.evaluate("hideModal()")
    b.close()
print('page errors:', errs or 'none')
print('text problems:', sorted(set(problems)) or 'none')
