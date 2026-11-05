# Computed-style snapshot: loads a fresh game and three fixture saves at phone width, visits every tab and the
# Settings and death pop-ups, and writes every visible element's computed style (and text) to OUT, so a CSS or
# markup refactor can be checked for "no visible change": run before and after, then compare the two files.
# Usage: OUT=/tmp/a.json python3 stylesnap.py ; OUT=/tmp/b.json python3 stylesnap.py ; python3 stylesnap.py diff /tmp/a.json /tmp/b.json
import json, os, sys
LIVE = ['#surv', '#s-why', '#s-plan', '.tgm', '.trl', 'tgm#', 'trl#', '.qfc', 'qfc#', '#h-day', '#nxa', '#tlnow']
PROPS = ['display','position','width','height','margin','padding','border','border-radius','color','background-color','font-family','font-size','font-weight','line-height','white-space','text-align','gap','grid-template-columns','flex','flex-wrap','align-items','justify-content','opacity','transform','box-shadow','text-transform','letter-spacing','overflow','visibility','min-width','max-width','min-height','cursor','text-decoration-line']
if len(sys.argv) > 1 and sys.argv[1] == 'diff':
    import difflib
    a, b = json.load(open(sys.argv[2])), json.load(open(sys.argv[3])); n = 0; moved = 0
    for k in a:
        if k not in b: print('missing view', k); n += 1; continue
        ka, kb = [x['_p'] for x in a[k]], [x['_p'] for x in b[k]]   # align by element structure first (timing can add a row)
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ka, kb, autojunk=False).get_opcodes():
            if tag != 'equal': moved += max(i2 - i1, j2 - j1); continue
            for x, y in zip(a[k][i1:i2], b[k][j1:j2]):
                live = any(s in x['_p'] for s in LIVE)   # live readouts: their text (and so their size) depends on timing
                d = {p: (x.get(p), y.get(p)) for p in set(x) | set(y) if x.get(p) != y.get(p) and p != 'height' and not ((live or (p == '_t' and any(c.isdigit() for c in str(x.get(p))))) and p in ('_t', 'width'))}   # heights follow content; clock texts tick
                if d:
                    print(k, x['_p'], d); n += 1
                    if n > 60: sys.exit(1)
    print('style differences:', n, '· unmatched elements:', moved); sys.exit(1 if n else 0)
from playwright.sync_api import sync_playwright
R = '/home/claude/long-patience/'
JS = "(props)=>[...document.querySelectorAll('body *')].filter(e=>e.getClientRects().length && !e.closest('#fonts,script,style')).map(e=>{ const c=getComputedStyle(e), o={_p:e.tagName+'.'+(typeof e.className==='string'?e.className:'')+'#'+e.id}; props.forEach(p=>o[p]=c.getPropertyValue(p)); if(!e.children.length) o._t=(e.textContent||'').slice(0,60); return o; })"
out = {}
def shoot(pg, name):
    pg.wait_for_timeout(250); out[name] = pg.evaluate(JS, PROPS)
with sync_playwright() as p:
    b = p.chromium.launch()
    for save in [None, 'snap4old.json', 'snap7.json', 'snap16.json']:
        pg = b.new_page(viewport={'width': 390, 'height': 900})
        pg.add_init_script("Date.now=()=>1762300000000; Math.random=()=>0.5;")
        if save:
            raw = open(R + 'project/tools/fixtures/' + save).read()
            pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
        else:
            pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
        pg.goto('file://' + R + 'index.html'); pg.wait_for_timeout(900)
        tag = save or 'fresh'
        shoot(pg, tag + ':start')
        if save: pg.click('[data-menu="continue"]'); pg.wait_for_timeout(300)
        pg.evaluate("()=>{ hideModal(); paused=true; S.set.paused=true; S.intro=true; }")
        for t in ['tasks', 'map', 'auto', 'skills', 'archive', 'legacy', 'log', 'faq']:
            pg.evaluate("t=>{ if (document.querySelector('[data-tab=\"'+t+'\"]')) { taskKey=''; mapKey=''; autoKey=''; logKey=''; setTab(t); } }", t); shoot(pg, tag + ':' + t)
        pg.evaluate("()=>showSettings('hud')"); shoot(pg, tag + ':settings')
        pg.evaluate("()=>{ hideModal(); showMenu(); }"); shoot(pg, tag + ':menu')
        pg.close()
    b.close()
json.dump(out, open(os.environ.get('OUT', '/tmp/stylesnap.json'), 'w'))
print('views', len(out), 'elements', sum(len(v) for v in out.values()))
