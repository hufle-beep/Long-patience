from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e))); pg.on('console', lambda m: m.type=='error' and errs.append('console: '+m.text))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800); pg.click('text=Begin the work cycle'); pg.wait_for_timeout(300)
    pg.click('text=Climb out of the seed pod'); 
    # let it run for real at x5 until death
    pg.evaluate("()=>{ S.set.speed=5; }")
    for i in range(150):
        pg.wait_for_timeout(1000)
        if pg.evaluate("S.life.dead"): break
        if not pg.evaluate("$('#modal').hidden") and pg.locator('#mbox [data-storyok]').count(): pg.click('#mbox [data-storyok]')
        if not pg.evaluate("S.life.queue.length") and not pg.evaluate("S.life.cur"):
            pg.evaluate("()=>{ S.life.queue=TASKS.filter(t=>t.kind==='act'&&available(t)&&!complete(t)).map(t=>t.id); }")
        pg.evaluate("()=>{ S.set.paused=false; paused=false; }")
    print('dead', pg.evaluate("S.life.dead"), 'gen', pg.evaluate("S.gen"))
    pg.wait_for_timeout(800)
    print('modal:', pg.locator('#mbox').inner_text()[:400].replace('\n',' | '))
    btns=pg.evaluate("[...document.querySelectorAll('#mbox button')].map(b=>b.outerHTML.slice(0,120))"); print(btns)
    pg.screenshot(path='/tmp/claude-0/sim/dbgdeath.png')
    for sel in ['#mbox button.pri','#mbox button']:
        if pg.locator(sel).count():
            pg.locator(sel).first.click(); pg.wait_for_timeout(600); break
    print('after click modal hidden:', pg.evaluate("$('#modal').hidden"), 'gen', pg.evaluate("S.gen"), 'dead', pg.evaluate("S.life.dead"))
    print('SPROUT OK' if pg.evaluate('S.gen')==2 and not pg.evaluate('S.life.dead') else 'SPROUT FAILED')
    # scroll lock: open a pop-up and try to scroll the page behind it
    pg.evaluate("window.scrollTo(0,0); showSettings()"); pg.wait_for_timeout(200)
    pg.mouse.move(200, 30); pg.mouse.wheel(0, 1500); pg.wait_for_timeout(300)
    y=pg.evaluate("document.scrollingElement.scrollTop"); print('page scroll behind pop-up:', y, 'LOCK OK' if y==0 else 'LOCK FAILED', 'html class', pg.evaluate("document.documentElement.className"))
    pg.evaluate("hideModal()"); pg.mouse.wheel(0, 800); pg.wait_for_timeout(300); print('page scrolls after closing:', pg.evaluate("document.scrollingElement.scrollTop")>0)
    print('modal now:', pg.locator('#mbox').inner_text()[:200].replace('\n',' | '))
    print('errors', errs); b.close()
