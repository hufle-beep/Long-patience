# Section targets (build "section targets"): each section has a target seedling count; the count is the seedling that
# first cleared it minus the one that first reached it (0 for the Seedling Vaults); first arrivals store the seedling
# (older saves: a complete run history); clearing within the target gives a star on the route and a Log entry (once);
# the section header shows the target and "now N" or "cleared in N".
import json
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; }")
    # counts from first arrivals (owner's Taproot run: reached by 10, crossed by 24 -> 14)
    r=pg.evaluate("""()=>{ S.gen=26; S.life.sec=15; S.firstAt={2:{d:1,r:1,g:10}, 15:{d:2,r:2,g:24}};
      return [secUsed(1), secUsed(2), secUsed(15), secSoFar(15), tgtMet(1), tgtMet(2), TARGETS[1], TARGETS[2], TARGETS[15]]; }""")
    print('counts', r)
    if r!=[10,14,None,2,False,True,9,14,11]: errs.append('counts wrong: %s' % r)
    # runTotal stores the seedling
    g=pg.evaluate("()=>{ runTotal(3); return S.firstAt[3].g; }")
    if g!=26: errs.append('runTotal did not store the seedling: %s' % g)
    # badge once, at the crossing out of the section
    e=pg.evaluate("""()=>{ S.tgts={}; S.evlog=[]; tgtCheck(15); tgtCheck(15); return [S.evlog.map(x=>x.t), S.tgts]; }""")
    print('badge', e)
    if len(e[0])!=1 or 'Taproot Galleries' not in e[0][0] or e[1].get('2')!=14: errs.append('badge not logged once: %s' % e)
    # older saves: first arrivals from a complete history only
    h=pg.evaluate("""()=>{ S.firstAt={2:{d:1,r:1}}; S.hist=[]; for (let g=1; g<=12; g++) S.hist.push({g, sec:g<5?1:2, z:g<5?1:2, d:10, r:1, cause:'x', fin:[g>=5?[1,1]:null,null,null,null,null,null]});
      const a=firstGen(2); S.hist=S.hist.slice(3); const b=firstGen(2); return [a,b]; }""")
    print('from history', h)
    if h!=[5,None]: errs.append('history fallback wrong: %s' % h)
    # header (on the Contested Boughs fixture) and route star
    raw=open('/tmp/claude-0/sim/snap7.json').read()
    pg2=b.new_page(viewport={'width':390,'height':900}); pg2.on('pageerror', lambda e: errs.append(str(e)))
    pg2.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg2.goto('file:///home/claude/long-patience/index.html'); pg2.wait_for_timeout(900)
    pg2.evaluate("()=>{ hideModal(); paused=true; S.intro=true; S.firstAt=Object.assign(S.firstAt||{}, {7:{d:1,r:1,g:S.gen-2}, 2:{d:1,r:1,g:10}, 15:{d:2,r:2,g:24}}); taskKey=''; setTab('tasks'); }"); pg2.wait_for_timeout(300)
    ht=pg2.inner_text('#v-tasks .zh .tgt')
    print('header', ht)
    if 'Target 3 seedlings' not in ht or 'now 2' not in ht: errs.append('header line wrong: '+ht)
    pg2.evaluate("()=>{ mapKey=''; setTab('map'); }"); pg2.wait_for_timeout(300)
    st=pg2.evaluate("()=>[...document.querySelectorAll('.rn[data-routez]')].filter(n=>n.querySelector('.rstar')).map(n=>n.dataset.routez)")
    print('stars', st)
    if st!=['2']: errs.append('route star wrong: %s' % st)
    b.close()
print('errors', errs)
