# Settings merged (build "settings merged", cleanup chunk 1): one Auto-charge switch (the old Charge when needed
# folded in, old values mapped over); "At a death" and "Pause at crossings" choices set the old switches;
# Pause when... chips toggle their switches; the Auto tab has no Charge when needed row any more.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.prefs.v1', JSON.stringify({autoFood:false, autoFeed:true})); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    r=pg.evaluate("()=>[S.set.autoFood, 'autoFeed' in S.set, typeof feedJob, PREF_KEYS.includes('autoFeed')]")
    print('old prefs mapped', r); assert r==[True, False, 'function', False]
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; S.stats.deaths=12; }")
    # Auto tab: no Charge when needed row
    pg.evaluate("()=>{ setTab('auto'); autoKey=''; renderAuto(); }")
    t=pg.inner_text('#v-auto') if pg.query_selector('#v-auto') else pg.content()
    print('auto tab has Charge when needed:', 'Charge when needed' in t); assert 'Charge when needed' not in t
    # settings: choices
    pg.evaluate("()=>showSettings('hud')")
    pg.click('[data-setto="deathScreen=false,deathQueue=true"]')
    r=pg.evaluate("()=>[S.set.deathScreen, S.set.deathQueue, document.querySelector('[data-setto=\"deathScreen=false,deathQueue=true\"]').classList.contains('on')]")
    print('death choice', r); assert r==[False, True, True]
    pg.click('[data-setto="pauseFirst=true,pauseCross=true"]')
    r=pg.evaluate("()=>[S.set.pauseFirst, S.set.pauseCross]"); print('crossing every', r); assert r==[True, True]
    pg.click('[data-setto="pauseFirst=false,pauseCross=false"]')
    r=pg.evaluate("()=>[S.set.pauseFirst, S.set.pauseCross]"); print('crossing never', r); assert r==[False, False]
    for k in ['pauseDone','startPaused','deathPause']:
        before=pg.evaluate(f"()=>S.set.{k}")
        pg.click(f'#modal [data-set="{k}"]')
        after=pg.evaluate(f"()=>[S.set.{k}, document.querySelector('#modal [data-set=\"{k}\"]').classList.contains('on')]")
        print(k, before, after); assert after[0]==(not (before is not False if k=='deathPause' else bool(before))) and after[1]==after[0]
    prefs=pg.evaluate("()=>JSON.parse(localStorage.getItem('selene.prefs.v1'))")
    print('prefs saved', {k:prefs.get(k) for k in ['deathScreen','deathQueue','pauseFirst','pauseCross','autoFeed']})
    assert 'autoFeed' not in prefs
    b.close()
print('errors', errs)
