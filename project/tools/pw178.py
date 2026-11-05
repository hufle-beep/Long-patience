# Tooltips (build "tooltips"): one game-styled bubble. Mouse: hover 0.4 s (task cards show their full effects; the
# browser's own title tooltip is moved to data-tip). Touch: hold 0.5 s shows it and the tap that follows is swallowed;
# moving cancels; the queue + keeps its long-press (no tooltip on touch). Header energy, Outlook, buttons, route nodes.
import json
from playwright.sync_api import sync_playwright
errs=[]
raw=open('/tmp/claude-0/sim/snap7.json').read()
TOUCH="""(a)=>{ const el=document.querySelector(a.sel); const r=el.getBoundingClientRect(); const x=r.left+r.width/2+(a.dx||0), y=r.top+r.height/2;
  el.dispatchEvent(new PointerEvent(a.type,{bubbles:true,cancelable:true,pointerType:'touch',pointerId:7,clientX:x,clientY:y,isPrimary:true}));
  if (a.type==='pointerup') el.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,clientX:x,clientY:y})); }"""
def hov(pg, sel, block='center'):
    pg.evaluate("([s,b])=>document.querySelector(s).scrollIntoView({block:b})", [sel, block]); pg.wait_for_timeout(300)
    bb=pg.locator(sel).first.bounding_box(); pg.mouse.move(5, 5); pg.mouse.move(bb['x']+bb['width']/2, bb['y']+bb['height']/2)
vis="()=>{ const t=document.querySelector('.tipb'); return t && !t.hidden ? t.textContent : null; }"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=true; S.set.paused=true; S.life.queue=[]; taskKey=''; }"); pg.wait_for_timeout(500)
    # mouse hover on a task card
    aid=pg.evaluate("()=>[...document.querySelectorAll('.task[data-id]')].map(e=>e.dataset.id).find(i=>T[i].kind==='act')")   # an action card (jobs have nothing to add on a fresh game)
    hov(pg, '.task[data-id="%s"] .tm' % aid); pg.wait_for_timeout(250)
    if pg.evaluate(vis): errs.append('tooltip before the hover delay')
    pg.wait_for_timeout(400)
    t=pg.evaluate(vis); print('card tip', (t or '')[:90].replace('\n',' | '))
    name=pg.evaluate("()=>T['"+aid+"'].name")
    if not t or t.startswith(name) or 'Automation' not in t: errs.append('card tooltip should add only what the card lacks (no name, automation line): %r' % t)   # build "tooltips trimmed"
    pg.mouse.move(5, 890); pg.wait_for_timeout(200)
    if pg.evaluate(vis): errs.append('tooltip did not hide when the pointer left')
    # energy line and a title converted to data-tip (no native tooltip left)
    hov(pg, '#tipenergy'); pg.wait_for_timeout(600)
    t=pg.evaluate(vis) or ''
    if not t.startswith('Energy'): errs.append('no energy tooltip: '+t)
    hov(pg, '#h-day'); pg.wait_for_timeout(600)
    hd=pg.evaluate("()=>[document.querySelector('#h-day').closest('[data-tip],[title]')?.hasAttribute('title'), !!document.querySelector('.tipb:not([hidden])')]")
    if hd[0] or not hd[1]: errs.append('title not moved to the game tooltip: %s' % hd)
    pg.mouse.move(5, 890); pg.wait_for_timeout(200)
    # touch hold: bubble, then the tap after it is swallowed
    sel='.task[data-id="%s"] .tm' % aid; pg.evaluate("()=>{ window.__runs=0; document.addEventListener('click', e=>{ if(e.target.closest('[data-do]')) __runs++; }); }")
    pg.evaluate(TOUCH, {'sel':sel,'type':'pointerdown'}); pg.wait_for_timeout(650)
    t=pg.evaluate(vis); pg.evaluate(TOUCH, {'sel':sel,'type':'pointerup'}); pg.wait_for_timeout(100)
    print('touch hold', (t or '')[:60].replace('\n',' | '), 'clicks reaching the card', pg.evaluate("()=>__runs"))
    if not t: errs.append('no tooltip on touch hold')
    if pg.evaluate("()=>__runs")!=0: errs.append('tap after a hold was not swallowed')
    # a short tap still taps (no tooltip)
    pg.evaluate(TOUCH, {'sel':sel,'type':'pointerdown'}); pg.wait_for_timeout(120); pg.evaluate(TOUCH, {'sel':sel,'type':'pointerup'}); pg.wait_for_timeout(100)
    if pg.evaluate("()=>__runs")!=1 or pg.evaluate(vis): errs.append('short tap broken')
    # moving cancels
    pg.evaluate(TOUCH, {'sel':sel,'type':'pointerdown'}); pg.evaluate(TOUCH, {'sel':sel,'type':'pointermove','dx':20}); pg.wait_for_timeout(650)
    if pg.evaluate(vis): errs.append('moving did not cancel the hold')
    pg.evaluate(TOUCH, {'sel':sel,'type':'pointercancel'})
    # the queue + keeps its long-press: no tooltip on touch
    pg.evaluate(TOUCH, {'sel':'button[data-q]','type':'pointerdown'}); pg.wait_for_timeout(650)
    if pg.evaluate(vis): errs.append('tooltip on the queue + (should keep its long-press)')
    pg.evaluate(TOUCH, {'sel':'button[data-q]','type':'pointercancel'})
    # route node on the Map
    pg.evaluate("()=>{ setTab('map'); }"); pg.wait_for_timeout(400)
    hov(pg, '.rn[data-routez]', 'end'); pg.wait_for_timeout(600)
    t=pg.evaluate(vis) or ''; print('route tip', t[:70])
    if 'danger' not in t: errs.append('no route tooltip')
    b.close()
print('errors', errs)
