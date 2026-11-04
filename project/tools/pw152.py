from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800); pg.click('text=Begin the work cycle'); pg.wait_for_timeout(1500)
    d0=pg.evaluate("S.life.day")
    pg.evaluate("()=>{ Object.defineProperty(document,'hidden',{configurable:true,get:()=>true}); document.dispatchEvent(new Event('visibilitychange')); }"); pg.wait_for_timeout(2500)
    d1=pg.evaluate("S.life.day"); print('ran while hidden?', round(d1-d0,2))
    pg.evaluate("()=>{ S.perks.watch1=true; S.perks.watch2=true; M=mods(); }"); print('stasis', pg.evaluate("M.stasis"), 'drain ratio', pg.evaluate("(()=>{const a=drainNow(0,0,1); S.perks.watch1=false;S.perks.watch2=false;M=mods(); return a/drainNow(0,0,1);})()"))
    print('errors', errs); b.close()
