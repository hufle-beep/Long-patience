# Old saves (round 5, R18): every playtest save in saves/ (oldest format 2026-11-03 on) and every fixture still
# merges without errors or broken numbers, keeps its seedling number, passes slotCheck, runs, and forecasts.
import base64, gzip, glob, json, os
from playwright.sync_api import sync_playwright
ROOT='/home/claude/long-patience'
def decode(p):
    t=open(p).read().strip()
    if t.startswith('LPZ1:'): return gzip.decompress(base64.b64decode(t[5:])).decode()
    if t.startswith('{'): return t
    return base64.b64decode(t).decode()
files=sorted(glob.glob(ROOT+'/saves/*.txt')+glob.glob(ROOT+'/saves/*.json'))+sorted(glob.glob(ROOT+'/project/tools/fixtures/snap*.json'))
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file://'+ROOT+'/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=true; }")
    for f in files:
        raw=decode(f)
        try: json.loads(raw)
        except ValueError:   # a cut-off upload (hufle2-2026-11-03-2331 stops at 20,000 characters): the game must call it damaged, not crash
            w=pg.evaluate("raw=>{ localStorage.setItem(slotKey(5), raw); const c=slotCheck(5); localStorage.removeItem(slotKey(5)); return c.why; }", raw)
            print(os.path.basename(f), 'cut off ->', w)
            if 'damaged' not in (w or ''): errs.append(os.path.basename(f)+': a cut-off save was not reported as damaged')
            continue
        r=pg.evaluate("""raw=>{ const o=JSON.parse(raw); let m; try { m=mergeState(JSON.parse(raw)); } catch(e) { return {err:'merge: '+e.message}; }
          const bad=badNums(m); localStorage.setItem(slotKey(5), saveJson(m)); const ck=slotCheck(5);
          const s0=S, m0=M; let fc=null, ran=0;
          try { S=m; M=mods(); const L=S.life, d0=L.day||0; if (!L.dead) { for (let i=0;i<300 && !L.dead;i++) if (step(2)===false) break; } ran=(L.day||0)-d0; if (!L.dead) fc=forecast(); }
          catch(e) { return {err:'run: '+e.message}; } finally { S=s0; M=m0; }
          localStorage.removeItem(slotKey(5));
          return {gen:[o.gen, m.gen], bad, why:ck.why, sec:m.life.sec, ran, fc:fc && fc.end}; }""", raw)
        name=os.path.basename(f)
        print(name, r)
        if r.get('err'): errs.append(name+': '+r['err']); continue
        if r['gen'][0] is not None and r['gen'][0]!=r['gen'][1]: errs.append(name+': seedling number changed %s' % r['gen'])
        if r['bad']: errs.append(name+': broken numbers %s' % r['bad'])
        if r['why']: errs.append(name+': slotCheck says '+r['why'])
    print('saves checked', len(files))
    print('errors', errs)
    b.close()
