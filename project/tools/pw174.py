# Save checks (build "save checks"): saves carry a format number and a checksum; a slot edited outside the game opens
# a recovery screen ("Load it anyway"), a damaged or too-new slot can't be continued (export it, backups, start fresh:
# the damaged text is kept aside); imports with a bad checksum ask first and too-new ones are refused; a save rewritten
# by an older build (stale checksum) counts as unchecked; export file names carry the time and build.
import json, re
from playwright.sync_api import sync_playwright
errs=[]
raw=json.load(open('/tmp/claude-0/sim/snap7.json'))
def boot(pg, slot1):
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(slot1))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
with sync_playwright() as p:
    b=p.chromium.launch()
    def page():
        pg=b.new_page(viewport={'width':390,'height':900}, accept_downloads=True); pg.on('pageerror', lambda e: errs.append(str(e))); return pg
    # 1. a normal save gets fmt and a checksum that checks out
    pg=page(); boot(pg, json.dumps(raw))
    pg.evaluate("()=>{ hideModal(); paused=true; save(); }")
    s=pg.evaluate("()=>{ const r=JSON.parse(localStorage.getItem('selene.slot.1')); return [r.fmt, typeof r.ck, ckCheck(r), 'ck' in S]; }")
    print('saved', s)
    if s!=[1,'string','ok',False]: errs.append('save lacks fmt/checksum or S keeps ck: %s' % s)
    good=pg.evaluate("()=>localStorage.getItem('selene.slot.1')")
    fn=pg.evaluate("()=>saveFileName()"); print('file name', fn)
    if not re.match(r'^selene-slot1-seedling\d+-\d{4}-\d\d-\d\d-\d{4}-save-checks\.json$', fn): errs.append('file name: '+fn)
    # an export carries a checksum that checks out after parsing the pretty file
    ex=pg.evaluate("()=>{ const t=JSON.stringify(JSON.parse(saveJson(S)),null,1); return ckCheck(JSON.parse(t)); }")
    if ex!='ok': errs.append('exported checksum does not check out: '+ex)
    # older build rewrote it: new saved time, stale ck -> unchecked
    stale=pg.evaluate("()=>{ const r=JSON.parse(localStorage.getItem('selene.slot.1')); r.saved+=1000; r.gen+=1; return ckCheck(r); }")
    if stale!='none': errs.append('stale checksum should count as unchecked: '+stale)
    # import with a bad checksum asks first; format 99 is refused
    pg.evaluate("()=>{ const r=JSON.parse(localStorage.getItem('selene.slot.1')); r.gen+=5; applyLoaded(r,'test'); }"); pg.wait_for_timeout(200)
    t=pg.inner_text('#mbox').lower()
    if 'changed outside the game' not in t: errs.append('import with bad checksum did not ask')
    pg.evaluate("()=>{ hideModal(); window.__t=[]; const o=toast; toast=(m,g)=>{__t.push(m); o(m,g);}; const r=JSON.parse(localStorage.getItem('selene.slot.1')); r.fmt=99; applyLoaded(r,'test'); }"); pg.wait_for_timeout(200)
    if not any('newer version' in m for m in pg.evaluate("()=>__t")): errs.append('too-new import not refused')
    pg.close()
    # 2. edited by hand: recovery, Load it anyway
    r2=json.loads(good); r2['gen']+=3
    pg=page(); boot(pg, json.dumps(r2))
    t=pg.inner_text('#mbox').lower(); print('edited:', t[:80].replace('\n',' | '))
    if 'changed outside the game' not in t: errs.append('edited slot: no recovery screen')
    gen0=pg.evaluate("()=>JSON.parse(localStorage.getItem('selene.slot.1')).gen")
    pg.evaluate("()=>{ save(); deathSave(); }")
    if pg.evaluate("()=>JSON.parse(localStorage.getItem('selene.slot.1')).gen")!=gen0: errs.append('saved while recovering')
    pg.click('#mbox button:has-text("Load it anyway")'); pg.wait_for_timeout(200)
    pg.click('[data-menu="continue"]'); pg.wait_for_timeout(300)
    g=pg.evaluate("()=>[S.gen, recovering, ckCheck(JSON.parse(localStorage.getItem('selene.slot.1')))]")
    print('after load anyway', g)
    if g[0]!=r2['gen'] or g[1] is not None or g[2]!='ok': errs.append('load anyway failed: %s' % g)
    pg.close()
    # 3. damaged text: no Continue, export, start fresh keeps it aside
    pg=page(); boot(pg, good[:-40])
    t=pg.inner_text('#mbox').lower(); print('damaged:', t[:70].replace('\n',' | '))
    if 'can’t be opened' not in t: errs.append('damaged slot: no recovery screen')
    with pg.expect_download() as dl: pg.click('#mbox button:has-text("Export the damaged save")')
    d=dl.value.suggested_filename; print('damaged export', d)
    if not d.startswith('selene-slot1-damaged-'): errs.append('damaged export name: '+d)
    pg.click('#mbox button:has-text("Other save slots")'); pg.wait_for_timeout(150)
    if 'damaged save' not in pg.inner_text('#mbox').lower(): errs.append('slot list does not mark the damaged slot')
    pg.click('[data-menu="back"]'); pg.wait_for_timeout(150)
    if pg.query_selector('[data-menu="continue"]'): errs.append('Continue offered for a damaged slot')
    pg.click('[data-ow="rec"]'); pg.wait_for_timeout(150)
    pg.click('#mbox button:has-text("Start fresh in this slot")'); pg.wait_for_timeout(150)
    pg.click('#mbox button:has-text("Start fresh")'); pg.wait_for_timeout(300)
    f=pg.evaluate("()=>[S.gen, recovering, !!localStorage.getItem('selene.damaged.1'), JSON.parse(localStorage.getItem('selene.slot.1')).gen]")
    print('start fresh', f)
    if f!=[1,None,True,1]: errs.append('start fresh failed: %s' % f)
    pg.close()
    # 4. too new: refused at boot
    r4=json.loads(good); r4['fmt']=99
    pg=page(); boot(pg, json.dumps(r4))
    if 'newer version' not in pg.inner_text('#mbox').lower(): errs.append('too-new slot opened')
    pg.close()
    b.close()
print('errors', errs)
