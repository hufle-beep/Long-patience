# Sounds (build "event sounds"): the four ZzFX sounds are built after audio starts, play through the game's
# own audio graph without errors, and fire on crossing, gear built, sprout and low energy (once per seedling).
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); pg=b.new_page(viewport={'width':420,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(5, 5); pg.wait_for_timeout(600)
    r=pg.evaluate("()=>({state:A.ctx&&A.ctx.state, zz:A.zz?Object.keys(A.zz).filter(k=>A.zz[k]).sort():null, lens:A.zz?Object.keys(A.zz).map(k=>+A.zz[k].duration.toFixed(2)):null})")
    print('audio', r)
    if r['zz']!=['cross','gear','low','sprout']: errs.append('sounds not built: '+str(r['zz']))
    pg.evaluate("()=>{ for (const k in ZZ) zzPlay(k); }")   # each plays without an error
    pg.evaluate("()=>{ window.__s=[]; const o=sfx; sfx=k=>{__s.push(k); o(k);}; hideModal(); paused=true; }")
    pg.evaluate("()=>{ HOOK.crossed(2); HOOK.bought(ITEMS[0], false); }")
    pg.evaluate("()=>{ S.life.hp=M.maxHp*0.1; updateHud(); updateHud(); }")
    pg.evaluate("()=>{ S.life.hp=0; S.life.dead=true; S.life.cause='test'; showDeath(); }"); pg.wait_for_timeout(200)
    pg.click('[data-decant]'); pg.wait_for_timeout(200)
    pg.evaluate("()=>{ S.life.hp=M.maxHp*0.1; updateHud(); }")
    calls=pg.evaluate("()=>__s")
    print('calls', calls)
    for k in ['cross','gear','sprout']:
        if k not in calls: errs.append('no sound for '+k)
    if calls.count('low')!=2: errs.append('low-energy warning should play once per seedling (twice here): %d' % calls.count('low'))
    print('errors', errs); b.close()
