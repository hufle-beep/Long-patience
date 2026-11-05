# Runs (build "runs"): the safe orbit opens the ending pop-up; a new run goes back to the Seedling Vaults with a new
# seedling (count goes on), keeps familiarity, automation, records and legacy reveals, resets the route and the run's
# totals; revealed legacy themes show in Act I on the next run; targets are not judged after the first run; the main
# menu offers a new run once the game is finished.
from playwright.sync_api import sync_playwright
import json
errs=[]
s=open('/home/claude/long-patience/project/tools/fixtures/snap16.json').read()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(s))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.click('[data-menu="continue"]'); pg.wait_for_timeout(300)
    r=pg.evaluate("""()=>{ hideModal(); paused=true; S.intro=true; const L=S.life; S.won=true; S.a2run.lrev={drain:1}; L.sec=14; finishBranch(T.safeorbit);
      return [!!document.querySelector('#mbox [data-newrun]') || null, a2Done()]; }""")
    pg.wait_for_timeout(200)
    r[0]=bool(pg.query_selector('#mbox [data-newrun]')); print('ending', r)
    if r!=[True, True]: errs.append('no ending pop-up with Begin again: %s' % r)
    before=pg.evaluate("()=>({gen:S.gen, fam:Object.keys(S.fam).length, perks:Object.keys(S.perks).length, auto:Object.keys(S.auto).length})")
    pg.click('#mbox [data-newrun]'); pg.wait_for_timeout(200); pg.click('#mbox [data-newrungo]'); pg.wait_for_timeout(400)
    after=pg.evaluate("""()=>({gen:S.gen, fam:Object.keys(S.fam).length, perks:Object.keys(S.perks).length, auto:Object.keys(S.auto).length, sec:S.life.sec, won:S.won, run:runNo(),
      lrev:S.a2run.lrev, fin:S.a2.fin, firstAt:Object.keys(S.firstAt).length, q:S.life.queue.filter(x=>!isCQ(x)).length, done:!!S.a2run.done.C,
      leg:available(T.lg1da1)===false && legacyOpen(T.lg1da1), runs:S.pr.runs.length, modal:!document.querySelector('#modal').hidden, qs:S.life.queue.slice(0,6), mh:(document.querySelector('#mbox h2')||{}).textContent})""")
    print('before', before); print('after', after)
    exp={'gen':before['gen']+1, 'fam':before['fam'], 'perks':before['perks'], 'auto':before['auto'], 'sec':1, 'won':False, 'run':1, 'fin':0, 'firstAt':0, 'q':0, 'modal':False, 'done':False, 'leg':True, 'runs':1}
    for k,v in exp.items():
        if after[k]!=v: errs.append('after new run %s = %r (expected %r)' % (k, after[k], v))
    # targets are not judged on later runs
    r=pg.evaluate("()=>{ const n=Object.keys(S.tgts||{}).length; S.firstAt={2:{d:1,r:1,g:S.gen}}; tgtCheck(2); return Object.keys(S.tgts||{}).length===n; }")
    if not r: errs.append('a target was judged on a later run')
    # main menu offers a new run only once the game is finished
    r=pg.evaluate("()=>{ showMenu(); return !!document.querySelector('#mbox [data-newrun]'); }")
    if r: errs.append('menu offers a new run before this run is finished')
    r=pg.evaluate("()=>{ hideModal(); S.a2run.done.C=1; showMenu(); return !!document.querySelector('#mbox [data-newrun]'); }")
    if not r: errs.append('menu does not offer a new run after the finish')
    b.close()
print('errors', errs)
