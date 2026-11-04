import base64,gzip,json
from playwright.sync_api import sync_playwright
raw=gzip.decompress(base64.b64decode(open('/home/claude/long-patience/saves/hufle2-2026-11-04-1241-clone10.txt').read()[5:].strip())).decode()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(600)
    print('gear req types', pg.evaluate("[...new Set(ITEMS.map(i=>Array.isArray(i.req)?'arr':typeof i.req))]"))
    pg.click('text=Begin the work cycle'); pg.wait_for_timeout(500)
    print('fresh first card:', pg.locator('.task.act').first.inner_text().replace('\n',' | '))
    pg.screenshot(path='/tmp/claude-0/sim/pw159a.png')
    pg2=b.new_page(viewport={'width':420,'height':900}); pg2.on('pageerror', lambda e: errs.append(str(e)))
    pg2.add_init_script("localStorage.setItem('long-patience.slot.1', %s); localStorage.setItem('long-patience.active-slot','1');" % json.dumps(raw)); pg2.goto('file:///home/claude/long-patience/index.html'); pg2.wait_for_timeout(1200); pg=pg2
    pg.evaluate("()=>{hideModal(); paused=true; taskKey=''; setTab('tasks');}"); pg.wait_for_timeout(400)
    for i in range(min(4,pg.locator('.task.act').count())): print('card:', pg.locator('.task.act').nth(i).inner_text().replace('\n',' | ')[:200])
    pg.screenshot(path='/tmp/claude-0/sim/pw159b.png', full_page=True)
    pg.evaluate("setTab('skills')"); pg.wait_for_timeout(300); t=pg.locator('#v-skills').inner_text(); print('mastery gear:', 'Gear' in t, t[t.find('Gear'):t.find('Gear')+160].replace('\n',' | ') if 'Gear' in t else '')
    pg.evaluate("setTab('auto')"); pg.wait_for_timeout(300); t=pg.locator('#v-auto').inner_text(); i=t.find('Not yet'); print('auto pending:', t[i:i+260].replace('\n',' | '))
    pg.screenshot(path='/tmp/claude-0/sim/pw159c.png', full_page=True)
    print('errors', errs); b.close()
