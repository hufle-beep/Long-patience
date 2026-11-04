from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800); pg.click('text=Begin the work cycle'); pg.wait_for_timeout(400)
    sel=pg.locator('select').filter(has=pg.locator('option[value="5"]'))
    print('speed select visible:', sel.count() and sel.first.is_visible(), 'options:', pg.evaluate("[...document.querySelectorAll('select option')].filter(o=>['1','2','5'].includes(o.value)).map(o=>o.value+(o.disabled?'(off)':''))"))
    if sel.count(): sel.first.select_option('5'); pg.wait_for_timeout(200)
    print('gameSpeed', pg.evaluate('gameSpeed()'), 'device unlock', pg.evaluate("localStorage.getItem('selene.speeds.v1')"), 'save unlock', pg.evaluate('S.spdUnl||1'))
    pg.evaluate("unlockSpeeds(true); save()"); print('after unlockSpeeds: device', pg.evaluate("localStorage.getItem('selene.speeds.v1')"), 'save', pg.evaluate('S.spdUnl||1'))
    print('errors', errs); b.close()
