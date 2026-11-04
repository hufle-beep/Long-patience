import json
from playwright.sync_api import sync_playwright
U='file:///home/claude/long-patience/index.html'
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':420,'height':900}); pg=ctx.new_page(); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(U); pg.wait_for_timeout(800); pg.click('text=Begin the work cycle'); pg.wait_for_timeout(300)
    def faq(): pg.evaluate("()=>{ faqDone=''; setTab('faq'); }"); pg.wait_for_timeout(200); return pg.evaluate("[...document.querySelectorAll('#v-faq details')].map(d=>d.dataset.faq+(d.querySelector('.fnew')?'*':''))")
    print('fresh FAQ:', faq())
    pg.evaluate("()=>{ setTab('tasks'); S.life.hp=-1; die('x'); decant(); faqCheck(true); renderView(true); }"); pg.wait_for_timeout(200)
    print('dot after death:', pg.evaluate("document.querySelector('[data-tab=faq]').classList.contains('dot')"))
    print('after death:', faq()); print('dot on faq tab:', pg.evaluate("document.querySelector('[data-tab=faq]').classList.contains('dot')"))
    print('stored:', pg.evaluate("localStorage.getItem('selene.faq.v1')")[:120])
    # new game keeps unlocks
    pg.evaluate("()=>{ S=defaultState(); M=mods(); S.life.hp=M.maxHp; save(); }"); print('new game FAQ count:', len(faq()))
    # export-all + soft reset keeps saves
    pg.evaluate("()=>{ S.name='Keep me'; save(); }")
    pg.evaluate("showSettings()"); pg.click('[data-reset="soft"]'); pg.wait_for_timeout(150); print(pg.locator('#mbox').inner_text()[:150].replace('\n',' | '))
    pg.click('[data-ow="c0"]'); pg.wait_for_timeout(1500)
    print('after soft reset: save kept', pg.evaluate("(JSON.parse(localStorage.getItem('selene.slot.1')||'{}').name)"), 'faq key', pg.evaluate("localStorage.getItem('selene.faq.v1')") is not None and 'recomputed' or 'gone', 'speed5 open', pg.evaluate("speedOpen(5)"))
    bundle=pg.evaluate("JSON.stringify(allSaves())")
    pg.evaluate("showSettings()"); pg.click('[data-reset="full"]'); pg.wait_for_timeout(150); print(pg.locator('#mbox').inner_text()[:200].replace('\n',' | '))
    pg.click('[data-ow="c1"]'); pg.wait_for_timeout(150); print(pg.locator('#mbox h2').inner_text()); pg.click('[data-ow="c0"]'); pg.wait_for_timeout(1500)
    print('after full reset keys:', pg.evaluate("Object.keys(localStorage).filter(k=>k.startsWith('selene.'))"), 'intro shown:', pg.locator('text=Begin the work cycle').count())
    # restore from the all-saves file
    pg.evaluate("(t)=>parseSaveAny(t).then(r=>applyLoaded(r,'file'))", bundle); pg.wait_for_timeout(300); print(pg.locator('#mbox').inner_text()[:160].replace('\n',' | '))
    pg.click('[data-ow="c0"]'); pg.wait_for_timeout(1500); print('restored slot1 name:', pg.evaluate("(JSON.parse(localStorage.getItem('selene.slot.1')||'{}').name)"))
    print('errors', errs); b.close()
