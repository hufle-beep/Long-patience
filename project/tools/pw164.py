import base64,gzip,json
from playwright.sync_api import sync_playwright
raw=gzip.decompress(base64.b64decode(open('/home/claude/long-patience/saves/hufle2-2026-11-04-1241-clone10.txt').read()[5:].strip())).decode()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(1000)
    pg.evaluate("()=>{ hideModal(); paused=true; setTab('archive'); }"); pg.wait_for_timeout(200)
    t=pg.locator('#v-archive').inner_text(); print('unrecovered shown:', t.count('Unrecovered'), '| stasis II shown:', 'Stasis watch II' in t)
    print(t[:600].replace('\n',' | '))
    pg.evaluate("setTab('log')"); pg.wait_for_timeout(200); print('stats:', pg.locator('.stats').inner_text().replace('\n',' | ')[:200])
    print('errors', errs); b.close()
