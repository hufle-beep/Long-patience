# Map folds (build "map folds"): fully mapped sections fold by themselves (not the current one, and optional
# legacy drills don't count); tapping a header folds or opens it; the choice is kept on the device across a reload.
import json
from playwright.sync_api import sync_playwright
errs=[]
s=json.load(open('/tmp/claude-0/sim/snap7.json'))
for d in ['drill','reckon','faults','flightsim','zerog']: s['ever'][d]=1
raw=json.dumps(s)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=true; setTab('map'); }"); pg.wait_for_timeout(200)
    st=lambda: pg.evaluate("()=>ROUTE.filter(z=>document.querySelector('#v-map [data-mapfold=\"'+z+'\"]')).map(z=>z+(document.querySelector('#v-map .mfold [data-mapfold=\"'+z+'\"]')?'c':'o'))")
    a=st(); print('default', a, 'current', pg.evaluate("()=>S.life.sec"))
    if a!=['1c','2c','3c','4c','5c','6o','7o']: errs.append('default folds wrong: '+str(a))
    pg.dispatch_event('[data-mapfold="2"]', 'click'); pg.dispatch_event('[data-mapfold="6"]', 'click'); pg.wait_for_timeout(200)
    b2=st(); print('toggled', b2, pg.evaluate("()=>localStorage.getItem('selene.mapfold.v1')"))
    if b2!=['1c','2o','3c','4c','5c','6c','7o']: errs.append('tap did not fold/open')
    pg.reload(); pg.wait_for_timeout(900); pg.evaluate("()=>{ hideModal(); paused=true; setTab('map'); }"); pg.wait_for_timeout(200)
    c=st(); print('after reload', c)
    if c!=b2: errs.append('folds not kept on the device')
    pg.dispatch_event('[data-mapfold="2"]', 'click'); pg.wait_for_timeout(100)
    if '"2"' in (pg.evaluate("()=>localStorage.getItem('selene.mapfold.v1')") or ''): errs.append('back to the default should drop the stored choice')
    print('errors', errs); b.close()
