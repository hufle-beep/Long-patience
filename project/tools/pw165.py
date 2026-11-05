# One drill per section (build "one drill per section"): an old save with both drills of a pair loads
# cleanly: the kept drill takes the higher automation count, its automation switch carries over, and
# queue entries, the queue plan and presets that name a removed drill drop out without errors.
import base64,gzip,json
from playwright.sync_api import sync_playwright
s=json.loads(gzip.decompress(base64.b64decode(open('/home/claude/long-patience/saves/hufle2-2026-11-05-0101-clone24.txt').read()[5:].strip())).decode())
s.pop('drv1', None)
s['prac']['drill']=12; s['prac']['rewire']=40; s['auto']['rewire']=True; s['auto'].pop('drill', None)   # Vaults: the removed drill was further along
s['prac']['reckon']=30; s['prac']['genes']=5                                                               # Taproot: the kept one was further along
s['life']['queue']=['genes','scars','rewire']; s['life']['qdone']=['locks']; s['qpresets'][0]=['puzzles','scars']
raw=json.dumps(s); errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':420,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(1000)
    r=pg.evaluate("()=>{ hideModal(); paused=true; qLoadPreset(0); const L=S.life; return {drill:S.prac.drill, autoDrill:S.auto.drill, reckon:S.prac.reckon, queue:L.queue, qdone:L.qdone, gone:['rewire','genes','graftdrill','locks','puzzles','seals','podcheck','poddrill','flipdrill','cqb','trapdrill','emberdrill','evadedrill','landdrill'].filter(id=>T[id]), share:drillShare(T.drill)}; }")
    for t in ['tasks','auto','skills']: pg.evaluate(f"setTab('{t}')"); pg.wait_for_timeout(200)
    print(r)
    if r['drill']!=40 or r['autoDrill'] is not True or r['reckon']!=30: errs.append('automation progress not merged')
    if r['gone']: errs.append('removed drills still exist: '+','.join(r['gone']))
    if r['queue']!=['scars'] or 'locks' in r['qdone']: errs.append('removed drills left in the queue')
    if r['share']!=0.2: errs.append('section drill share is not 0.2')
    print('errors', errs); b.close()
