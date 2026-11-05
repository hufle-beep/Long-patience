# Charging serves the work (builds "no idle charging", "work first"; owner playtest 2026-11-05):
# 1. only "Check the seed pods": no charging on its own, time stops;
# 2. with work queued, Auto-charge still steps in (the charging rule itself waits for the owner's pick).
# Also: gear descriptions show from the start in the test version; a gear card keeps its height when the list redraws.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800)
    run = """([q, hp, famAlgae])=>{ hideModal(); paused=true; S=defaultState(); if (famAlgae) S.fam.algae=famAlgae; M=mods(); S.intro=true; const L=S.life; L.hp=hp||M.maxHp; L.done.wake=1; L.done.vats=1; L.queue=q;
      const seen=[]; for (let i=0;i<20000;i++){ const d0=L.day; step(1); if (L.cur && seen[seen.length-1]!==L.cur) seen.push(L.cur); if (L.day===d0 || L.dead) break; }
      return {order:seen.slice(0,4), used:+(15-stationLeft(1)).toFixed(1), hp:Math.round(L.hp), dead:L.dead}; }"""
    a=pg.evaluate(run, [[], 0, 0]); print('idle', a)
    if a['order'] or a['used']>0: errs.append('idle seedling charged on its own: %s' % a)
    c=pg.evaluate(run, [['search','cables','terminal'], 0, 0]); print('work queued', c)
    if 'algae' not in c['order']: errs.append('Auto-charge no longer steps in while work is queued: %s' % c)
    # gear descriptions in the test version; the gear card keeps its height across a list redraw
    r=pg.evaluate("""()=>{ S=defaultState(); M=mods(); S.intro=true; S.storyQ=[]; S.life.done.wake=1; setTab('tasks'); taskKey=''; renderView(true);
      const card=()=>document.querySelector('.geta[data-g="toolkit"]').closest('.item'); const h0=card().getBoundingClientRect().height, d0=card().textContent;
      taskKey=''; renderView(true); const h1=card().getBoundingClientRect().height; return [TEST_SHOW_EFFECTS, d0.includes(IT.toolkit.desc), h0, h1]; }""")
    print('gear card', r)
    if r[0] and not r[1]: errs.append('gear description hidden in the test version')
    if r[2]!=r[3]: errs.append('gear card height changes on a redraw: %s -> %s' % (r[2], r[3]))
    b.close()
print('errors', errs)
