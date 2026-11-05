# Save safety (build "save safety"): rolling backups (5 min / 30 min / 2 h of play, and one just before a
# slot is replaced), restoring one, backups in "Export all saves", the broken-number guard on save and import,
# fix tips when pasting a queue, and the average row under the recent seedlings.
import json
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800)
    pg.evaluate("()=>{ hideModal(); paused=true; save(); }"); pg.wait_for_timeout(300)
    # rolling backups: the first one at once, the others as play time passes
    keys=[]
    for pl in [10, 400, 2000, 8000]:
        pg.evaluate(f"()=>{{ S.stats.played={pl}; save(); }}"); pg.wait_for_timeout(300)
        keys.append(sorted(pg.evaluate("()=>Object.keys(readBk(1))")))
    print('rolling', keys)
    if keys[-1]!=['h2','m30','m5']: errs.append('rolling backups missing: '+str(keys[-1]))
    t5=pg.evaluate("()=>readBk(1).m5.pl")
    if t5!=400 and t5!=8000: errs.append('m5 not refreshed after 5 min of play: '+str(t5))
    # broken numbers: nothing is written, a toast says so
    before=pg.evaluate("()=>localStorage.getItem('selene.slot.1')")
    pg.evaluate("()=>{ S.life.hp=NaN; save(); }")
    after=pg.evaluate("()=>localStorage.getItem('selene.slot.1')"); toast=pg.evaluate("()=>document.body.innerText.includes('Not saved: the game has broken numbers')")
    print('nan guard', before==after, toast, pg.evaluate("()=>badNums(S)"))
    if before!=after or not toast: errs.append('NaN save was written or not reported')
    pg.evaluate("()=>{ S.life.hp=50; }")
    # restart backs the slot up first
    pg.evaluate("()=>{ S.gen=7; save(); showMenu('saves'); }"); pg.wait_for_timeout(200)
    pg.click('[data-askreset]'); pg.wait_for_timeout(200); pg.click('[data-ow="c0"]'); pg.wait_for_timeout(600)
    pre=pg.evaluate("()=>{ const e=readBk(1).pre; return e && [e.note, e.info]; }")
    print('pre', pre)
    if not pre or pre[0]!='before a restart' or 'Seedling 7' not in pre[1]: errs.append('no backup before restart')
    # restore it from the Backups panel
    pg.evaluate("()=>{ hideModal(); showMenu('saves'); }"); pg.wait_for_timeout(200)
    pg.click('[data-bkslot="1"]'); pg.wait_for_timeout(300)
    txt=pg.inner_text('#modal'); print('panel', txt[:160].replace('\n',' | '))
    n=pg.evaluate("()=>BK_KINDS.filter(([k])=>readBk(1)[k]).findIndex(([k])=>k==='pre')")
    pg.click(f'[data-ow="c{n}"]'); pg.wait_for_timeout(500); pg.click('[data-ow="c0"]'); pg.wait_for_timeout(800)
    g=pg.evaluate("()=>S.gen"); print('restored gen', g)
    if g!=7: errs.append('backup not restored (gen %s)' % g)
    if 'before restoring a backup' not in (pg.evaluate("()=>readBk(1).pre.note") or ''): errs.append('no backup before restoring')
    # export all carries the backups
    if not pg.evaluate("()=>!!(allSaves().backups[1]||allSaves().backups['1'])"): errs.append('export all has no backups')
    # import check uses the guard
    pr=pg.evaluate("()=>{ const r=JSON.parse(JSON.stringify(S)); return [saveProblem(r), badNums({a:{b:[1,Infinity]},c:NaN})]; }")
    print('import', pr)
    if pr[0]!='' or pr[1]!=['a.b.1','c']: errs.append('import check wrong')
    # pasting a queue: a typo gets a suggestion, a locked task its reason
    pg.evaluate("()=>{ hideModal(); paused=true; if(S.life.dead) decant(); hideModal(); qTextPanel(); document.querySelector('#qtext').value='Serch the seedling vault\\nForce the root-lock iris\\nxyzzy plugh'; }")
    pg.click('[data-ow="c1"]'); pg.wait_for_timeout(300)
    rep=pg.inner_text('#modal'); print('paste', rep.replace('\n',' | ')[:400])
    for want in ['Did you mean “Search the seedling vault”', 'locked: opens after', 'xyzzy plugh: unknown name']:
        if want not in rep: errs.append('paste report lacks: '+want)
    pg.click('[data-ow="c0"]'); pg.wait_for_timeout(200)
    if 'Serch the seedling vault' not in pg.evaluate("()=>document.querySelector('#qtext').value"): errs.append('Back to the text lost the pasted text')
    # average row
    pg.evaluate("()=>{ hideModal(); S.hist=[{g:1,sec:1,z:1,d:800,r:50,cause:'x'},{g:2,sec:2,z:2,d:1600,r:100,cause:'x'},{g:3,sec:2,z:2,d:2400,r:150,cause:'x'}]; logTables=true; logKey=''; setTab('log'); }"); pg.wait_for_timeout(300)
    avg=pg.evaluate("()=>{ const r=document.querySelector('tr.havg'); return r && r.innerText; }")
    print('avg', (avg or '').replace('\n',' | ').replace('\t',' '))
    if not avg or 'Taproot' not in avg or '2/3' not in avg: errs.append('average row wrong')
    print('errors', errs); b.close()
