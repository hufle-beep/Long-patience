# Act choices and runs (builds "runs", "act choices"): the first kindling of a run asks Replay Act I / Move on / Main menu
# (later seedlings carry on into Act II at once); an Act I replay keeps everything and asks again at its end; the safe orbit
# asks Restart the whole game / Main menu; a restart is a prestige reset (regular familiarity and automation start over;
# records, legacy familiarity, the death award stay) and later runs don't judge targets; Continue brings a pending choice
# back; saves past their first run are coloured and show their run.
from playwright.sync_api import sync_playwright
import json
errs=[]
s=open('/home/claude/long-patience/project/tools/fixtures/snap16.json').read()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(s))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.click('[data-menu="continue"]'); pg.wait_for_timeout(300)
    # --- end of the voyage: restart the whole game (prestige reset)
    r=pg.evaluate("""()=>{ hideModal(); paused=true; S.intro=true; S.won=true; S.a2run.lrev={drain:1}; S.life.sec=14; finishBranch(T.safeorbit); return [S.actEnd, a2Done()]; }"""); pg.wait_for_timeout(200)
    if r!=[2, True] or not pg.query_selector('#mbox [data-newrun]'): errs.append('no Act II choice at the orbit: %s' % r)
    before=pg.evaluate("()=>({gen:S.gen, perks:Object.keys(S.perks).length, vit:S.vit, legFam:(S.fam.lg1d||0)+(S.fam.lg1da1||0)})")
    pg.click('#mbox [data-newrun]'); pg.wait_for_timeout(200); pg.click('#mbox [data-newrungo]'); pg.wait_for_timeout(400)
    after=pg.evaluate("""()=>({gen:S.gen, perks:Object.keys(S.perks).length, vit:S.vit, legFam:(S.fam.lg1d||0)+(S.fam.lg1da1||0), sec:S.life.sec, won:S.won, run:runNo(),
      regFam:Object.keys(S.fam).filter(k=>T[k]&&!T[k].legacy).length, regAuto:Object.keys(S.auto).filter(k=>T[k]&&!T[k].legacy).length, gauto:Object.keys(S.gauto).length,
      fin:S.a2.fin, firstAt:Object.keys(S.firstAt).length, leg:legacyOpen(T.lg1da1), actEnd:S.actEnd, tag:runTag(S)})""")
    print('before', before); print('after', after)
    exp={'gen':before['gen']+1, 'perks':before['perks'], 'vit':before['vit'], 'legFam':before['legFam'], 'sec':1, 'won':False, 'run':1, 'regFam':0, 'regAuto':0, 'gauto':0, 'fin':0, 'firstAt':0, 'leg':True, 'actEnd':None, 'tag':'Run 2'}
    for k,v in exp.items():
        if after[k]!=v: errs.append('after a restart %s = %r (expected %r)' % (k, after[k], v))
    r=pg.evaluate("()=>{ const n=Object.keys(S.tgts||{}).length; S.firstAt={2:{d:1,r:1,g:S.gen}}; tgtCheck(2); return Object.keys(S.tgts||{}).length===n; }")
    if not r: errs.append('a target was judged on a later run')
    # --- end of Act I in this run: the choice; replay keeps everything and asks again; later seedlings carry on
    r=pg.evaluate("""()=>{ hideModal(); const L=S.life; L.sec=5; T.ignite.req.forEach(id=>L.done[id]=T[id].reps); L.done.ignite=0; L.prog.ignite=T.ignite.days; L.done.ignite=1;
      L.queue=[]; finish(T.ignite); return [S.actEnd, L.sec, S.won]; }"""); pg.wait_for_timeout(200)
    if r!=[1, 5, True] or not pg.query_selector('#mbox [data-actreplay]'): errs.append('no Act I choice at the first kindling: %s' % r)
    fam0=pg.evaluate("()=>Object.keys(S.fam).length")
    pg.click('#mbox [data-actreplay]'); pg.wait_for_timeout(400)
    r=pg.evaluate("()=>[S.life.sec, S.replay1, (S.pr||{}).r1, Object.keys(S.fam).length, runTag(S)]"); print('replay', r)
    if r[:3]!=[1, True, 1] or r[3]!=fam0 or r[4]!='Run 2 · Act I replay 1': errs.append('Act I replay wrong: %s' % r)
    r=pg.evaluate("""()=>{ hideModal(); const L=S.life; L.sec=5; T.ignite.req.forEach(id=>L.done[id]=T[id].reps); L.done.ignite=1; finish(T.ignite); return S.actEnd; }"""); pg.wait_for_timeout(200)
    if r!=1: errs.append('no choice at the end of the Act I replay: %s' % r)
    pg.click('#mbox [data-acton]'); pg.wait_for_timeout(300)
    r=pg.evaluate("()=>[S.life.sec, S.actEnd, S.replay1]"); print('moved on', r)
    if r!=[9, None, False]: errs.append('Move on did not enter Act II: %s' % r)
    r=pg.evaluate("""()=>{ decant(); const L=S.life; L.sec=5; T.ignite.req.forEach(id=>L.done[id]=T[id].reps); L.done.ignite=1; finish(T.ignite); return [S.actEnd, L.sec]; }""")
    if r!=[None, 9]: errs.append('a later seedling was asked again instead of carrying on: %s' % r)
    # --- a pending choice comes back on Continue; the save list colours run 2
    r=pg.evaluate("()=>{ hideModal(); S.actEnd=2; save(); startGame(); return !!document.querySelector('#mbox [data-newrun]'); }")
    if not r: errs.append('Continue did not bring the pending choice back')
    r=pg.evaluate("()=>{ hideModal(); S.actEnd=null; save(); showMenu('saves'); const el=document.querySelector('#mbox .slot.ngp'); return el ? el.textContent : null; }")
    print('save card', (r or '')[:80])
    if not r or 'Run 2' not in r: errs.append('run-2 save not coloured or no run counter: %r' % r)
    b.close()
print('errors', errs)
