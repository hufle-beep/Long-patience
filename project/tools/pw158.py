from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800); pg.click('text=Begin the work cycle'); pg.wait_for_timeout(400)
    pg.evaluate("showMenu('new')"); pg.click('[data-newin="2"]'); pg.fill('#ow-name','  Hull   run  '); pg.screenshot(path='/tmp/claude-0/sim/pw158a.png'); pg.click('[data-ow="c0"]'); pg.wait_for_timeout(300)
    print('slot', pg.evaluate('slot'), 'name', repr(pg.evaluate('S.name')))
    pg.click('text=Begin the work cycle') if pg.locator('text=Begin the work cycle').count() else None
    pg.evaluate("()=>{ S.life.hp=-1; die('x'); }"); print('death save name', pg.evaluate("readSlot('d2').name"))
    pg.evaluate("()=>{decant(); save(); showMenu('saves');}"); pg.click('[data-saveto="4"]'); print('prefill', pg.input_value('#ow-name')); pg.fill('#ow-name','Backup A'); pg.click('[data-ow="c0"]'); pg.wait_for_timeout(200)
    print('slot4', pg.evaluate("readSlot(4).name"), 'current still', pg.evaluate('S.name'))
    pg.click('[data-rename="4"]'); pg.fill('#ow-name',''); pg.click('[data-ow="c0"]'); print('slot4 cleared', pg.evaluate("readSlot(4).name"))
    pg.click('[data-rename="2"]'); pg.fill('#ow-name','Hull run 2'); pg.click('[data-ow="c0"]'); print('active renamed', pg.evaluate('S.name'), pg.evaluate("readSlot(2).name"))
    print('file', pg.evaluate('saveFileName()'))
    pg.click('[data-saveto="4"]'); print(pg.locator('#mbox').inner_text().replace('\n',' | ')[:220]); pg.click('[data-ow="x"]')
    pg.screenshot(path='/tmp/claude-0/sim/pw158b.png', full_page=True)
    pg.evaluate("showMenu()"); print(pg.locator('[data-menu="continue"]').inner_text().replace('\n',' | '))
    print('errors', errs); b.close()
