# Map folds (rewritten for build "folds", the owner's pick M2): Map sections fold like the other tabs: behind the
# seedling folded, the current one and those ahead open, a finished act folded under its act header; a tap stores
# 'o' or 'c' in selene.secfold.v1 (device-wide); old Map choices (selene.mapfold.v1) are moved over once.
# Checks the stored values instead of reloading (headless reloads of a local file sometimes lost the newest writes).
import json
from playwright.sync_api import sync_playwright
errs=[]
s=json.load(open('/tmp/claude-0/sim/snap7.json'))
raw=json.dumps(s)
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); localStorage.setItem('selene.mapfold.v1', '{\"6\":\"o\"}'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    mig=pg.evaluate("()=>[localStorage.getItem('selene.mapfold.v1'), secFold['mp:6']]")
    print('migration', mig)
    if mig!=[None,'o']: errs.append('old Map choices not moved over: %s' % mig)
    pg.evaluate("()=>{ hideModal(); paused=true; setTab('map'); }"); pg.wait_for_timeout(300)
    st=lambda: pg.evaluate("()=>[...document.querySelectorAll('#v-map [data-fold]')].map(b=>b.dataset.fold.split(':')[1]+(b.getAttribute('aria-expanded')==='true'?'o':'c'))")
    a=st(); print('default', a, 'current', pg.evaluate("()=>S.life.sec"))
    if a!=['act1c','6o','7o']: errs.append('default folds wrong: '+str(a))   # 6 opened by the moved choice
    pg.dispatch_event('#v-map [data-fold="mp:act1"]', 'click'); pg.wait_for_timeout(300)
    b2=st(); print('act I opened', b2)
    a1=[x for x in b2 if x[:-1] in ('1','2','15','3','4','5')]
    if b2[0]!='act1o' or len(a1)<5 or any(x[-1]!='c' for x in a1): errs.append('act I did not open with its sections folded: '+str(b2))
    pg.dispatch_event('#v-map [data-fold="mp:2"]', 'click'); pg.dispatch_event('#v-map [data-fold="mp:6"]', 'click'); pg.wait_for_timeout(300)
    c=st(); store=pg.evaluate("()=>JSON.parse(localStorage.getItem('selene.secfold.v1'))")
    print('after taps', c, store)
    if '2o' not in c or '6c' not in c: errs.append('tap did not fold/open: '+str(c))
    if store.get('mp:2')!='o' or store.get('mp:6')!='c' or store.get('mp:act1')!='o': errs.append('choices not stored on the device: %s' % store)
    b.close()
print('errors', errs)
