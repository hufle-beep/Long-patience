# No idle charging (build "no idle charging", owner playtest 2026-11-05 17:44): a seedling that only does "Check the seed
# pods" must not wander off to the sap line and burn its life; with work still queued, Auto-charge still steps in.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800)
    run = """q=>{ hideModal(); paused=true; S=defaultState(); M=mods(); S.life.hp=M.maxHp; S.intro=true; const L=S.life; L.queue=q; const seen=new Set();
      for (let i=0;i<20000;i++){ const d0=L.day; step(1); if (L.cur) seen.add(L.cur); if (L.day===d0) break; }
      return {stopped:!L.cur, used:+(15-stationLeft(1)).toFixed(1), hp:Math.round(L.hp), charged:seen.has('algae')}; }"""
    a=pg.evaluate(run, ['wake','vats']); print('only the seed pods', a)
    if not a['stopped'] or a['charged'] or a['used']>0: errs.append('idle seedling charged on its own: %s' % a)
    b2=pg.evaluate(run, ['wake','vats','search','cables']); print('with work queued', b2)
    if not b2['charged']: errs.append('Auto-charge no longer steps in while work is queued: %s' % b2)
    b.close()
print('errors', errs)
