# Lighter redraws (build "lighter redraws"): the screen redraws about 10 times a second while running and about twice a
# second while paused; a tap redraws at once; unchanged values are not written again (no DOM changes while paused);
# live bars move by transform; the task list still rebuilds when it changes; autosave every 15 s; no 700 display face.
import json
from playwright.sync_api import sync_playwright
errs=[]
raw=open('/tmp/claude-0/sim/snap7.json').read()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=false; S.set.paused=false; S.intro=true; window._hud=0; const f=updateHud; updateHud=function(){ window._hud++; return f.apply(this, arguments); }; }")
    pg.wait_for_timeout(2000)
    run=pg.evaluate("()=>window._hud")/2
    pg.evaluate("()=>{ S.set.paused=true; window._hud=0; }"); pg.wait_for_timeout(2000)
    pz=pg.evaluate("()=>window._hud")/2
    print('redraws per second: running', run, 'paused', pz)
    if not (6 <= run <= 13): errs.append('running redraw rate off: %s' % run)
    if not (1 <= pz <= 3): errs.append('paused redraw rate off: %s' % pz)
    # no DOM writes of unchanged values while paused
    n=pg.evaluate("""()=>new Promise(r=>{ let n=0; const o=new MutationObserver(m=>{ n+=m.length; }); o.observe(document.body,{subtree:true,childList:true,attributes:true,characterData:true}); setTimeout(()=>{ o.disconnect(); r(n); }, 2000); })""")
    print('DOM changes while paused (2 s)', n)
    if n > 10: errs.append('unchanged values written while paused: %d' % n)
    # a tap redraws at once: pausing via the button shows Resume within a frame or two
    pg.evaluate("()=>{ S.set.paused=false; }"); pg.wait_for_timeout(600)
    pg.click('[data-pause]'); pg.wait_for_timeout(60)
    if 'Resume' not in pg.inner_text('#h-spd'): errs.append('tap did not redraw at once')
    # live bars use transform, the energy bar follows energy
    t=pg.evaluate("()=>[$('#b-hp').style.transform, S.life.hp/M.maxHp, $('#b-hp').style.width]")
    print('energy bar', t)
    if not t[0].startswith('scaleX(') or abs(float(t[0][7:-1]) - t[1]) > 0.02 or t[2]: errs.append('energy bar not a transform: %s' % t)
    # the task list still rebuilds when something changes (queue a task)
    k0=pg.evaluate("()=>taskKey")
    pg.evaluate("()=>{ const t=TASKS.find(x=>available(x)&&!complete(x)&&x.kind==='act'); S.life.queue.push(t.id); }"); pg.wait_for_timeout(1300)
    if pg.evaluate("()=>taskKey")==k0: errs.append('task list did not rebuild after a queue change')
    # setT clears setH's memory (same element written both ways)
    pg.evaluate("()=>{ const e=$('#n-eta'); setH(e,'X'); setT(e,''); setH(e,'X'); window._ne=e.textContent; }")
    if pg.evaluate("()=>window._ne")!='X': errs.append('setH skipped after setT')
    src=open('/home/claude/long-patience/index.html',encoding='utf8').read()
    if 'saveT > 15' not in src: errs.append('autosave interval not 15 s')
    if 'font-weight:700' in src: errs.append('a 700 face or rule is still there')
    b.close()
print('errors', errs)
