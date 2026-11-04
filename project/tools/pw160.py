import base64,gzip,json
from playwright.sync_api import sync_playwright
raw=gzip.decompress(base64.b64decode(open('/home/claude/long-patience/saves/hufle2-2026-11-04-1241-clone10.txt').read()[5:].strip())).decode()
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':420,'height':900}); pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///tmp/claude-0/sim/blank.html'); pg.wait_for_timeout(100)
    pg.evaluate("(r)=>{ localStorage.clear(); localStorage.setItem('long-patience.slot.3', r); localStorage.setItem('long-patience.active-slot','3'); localStorage.setItem('long-patience.prefs.v1', JSON.stringify({speed:2})); localStorage.setItem('long-patience.speeds.v1','2'); }", raw)
    pg2=ctx.new_page(); pg2.on('pageerror', lambda e: errs.append(str(e))); pg.close()
    pg2.goto('file:///home/claude/long-patience/index.html'); pg2.wait_for_timeout(1200)
    print('keys', pg2.evaluate("Object.keys(localStorage).sort()"))
    print('active slot', pg2.evaluate('slot'), 'gen', pg2.evaluate('S.gen'), 'title', pg2.title())
    print('menu', pg2.locator('#mbox h2').first.inner_text() if pg2.locator('#mbox h2').count() else '-')
    print('file name', pg2.evaluate('saveFileName()'))
    print('errors', errs); b.close()
