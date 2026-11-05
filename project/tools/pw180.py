# Robustness (build "robustness", round 5 chunk 1): a failed save says why, opens the export pop-up once and
# leaves "last saved" alone; a slot that can't be merged is never loaded over the current game; the export
# reminder fires after an hour of play and a day; errors show one bar and the game loop keeps running;
# stalls and backward clocks count no time; a double tap on a confirm button counts once.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900})
    perr=[]; pg.on('pageerror', lambda e: perr.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    pg.evaluate("()=>{ hideModal(); paused=false; S.intro=true; save(); }")
    # 1. storage full
    r=pg.evaluate("""()=>{ const t0=S.saved, orig=Storage.prototype.setItem;
      Storage.prototype.setItem=function(k,v){ if(/selene\\.slot\\./.test(k)){ const e=new Error('exceeded'); e.name='QuotaExceededError'; throw e; } return orig.call(this,k,v); };
      S.saved=t0; save(); save(); Storage.prototype.setItem=orig;
      return [S.saved===t0, !$('#modal').hidden, $('#mbox h2') && $('#mbox h2').textContent, !!$('#mbox [data-exportjson]'), [...document.querySelectorAll('.toast')].map(x=>x.textContent).filter(x=>/Couldn/.test(x)).length, saveFailN]; }""")
    print('save failure', r)
    if r[:4]!=[True,True,'The game couldn’t be saved',True] or r[4]!=1 or r[5]!=2: errs.append('save failure handling: %s' % r)
    pg.evaluate("()=>{ hideModal(); paused=false; }")
    # 2. a slot that can't be merged is not loaded over the game
    r=pg.evaluate("""()=>{ localStorage.setItem(slotKey(2), saveJson(Object.assign(JSON.parse(JSON.stringify(S)), {gen:77}))); const m0=mergeState, g0=S.gen, s0=slot;
      let n=0; mergeState=function(x){ if(x && x.gen===77 && ++n>1) throw new Error('bad merge'); return m0(x); };
      const bt=document.createElement('button'); bt.dataset.loadslot='2'; document.body.appendChild(bt); bt.click(); bt.remove(); mergeState=m0;
      return [slot===s0, S.gen===g0, [...document.querySelectorAll('.toast')].some(x=>/Couldn’t open Slot 2|Couldn’t open slot 2/i.test(x.textContent))]; }""")
    print('failed load', r)
    if r!=[True,True,True]: errs.append('failed load switched slots: %s' % r)
    # 3. export reminder
    r=pg.evaluate("""()=>{ document.querySelectorAll('.toast').forEach(x=>x.remove()); S.intro=true;
      localStorage.setItem(EXP_KEY, JSON.stringify({t:Date.now()-2*86400000, pl:0})); S.stats.played=1000; expRemind();
      const a=[...document.querySelectorAll('.toast')].filter(x=>/No save exported/.test(x.textContent)).length;
      S.stats.played=4000; expRemind(); const b=[...document.querySelectorAll('.toast')].filter(x=>/No save exported/.test(x.textContent)).length;
      S.stats.played=9000; expRemind(); const c=[...document.querySelectorAll('.toast')].filter(x=>/No save exported/.test(x.textContent)).length;
      const o=expState(); o.off=true; o.t=Date.now()-3*86400000; o.pl=0; expWrite(o); S.stats.played=99999; expRemind();
      const d=[...document.querySelectorAll('.toast')].filter(x=>/No save exported/.test(x.textContent)).length; expWrite({});
      return [a,b,c,d]; }""")
    print('export reminder', r)
    if r!=[0,1,1,1]: errs.append('export reminder: %s' % r)
    # 4. error bar and loop keeps running
    pg.evaluate("()=>{ setTimeout(()=>{ throw new Error('round5 test boom'); }, 0); setTimeout(()=>{ throw new Error('round5 test boom'); }, 10); }")
    pg.wait_for_timeout(200)
    d0=pg.evaluate("()=>{ S.life.now=TASKS.find(t=>t.z===1 && available(t) && t.kind!=='job' && !complete(t)).id; return S.life.day||0; }")
    pg.evaluate("()=>{ const f=updateHud; let n=0; updateHud=function(){ if(++n===1) { updateHud=f; throw new Error('hud boom'); } return f.apply(this, arguments); }; }")
    pg.wait_for_timeout(1200)
    r=pg.evaluate("()=>[!!document.getElementById('errbar') && !document.getElementById('errbar').hidden, errN, (S.life.day||0)]")
    print('error bar', r, d0)
    if not r[0] or r[1]!=2 or not r[2]>d0: errs.append('error catcher: %s (age before %s)' % (r, d0))
    pg.click('[data-errclose]')
    if pg.evaluate("()=>!document.getElementById('errbar').hidden"): errs.append('error bar did not close')
    # 5. stalls and backward clocks
    r=pg.evaluate("()=>{ paused=true; last=performance.now(); const a=tick(last-500); last=performance.now(); const b=tick(last+5000); last=performance.now(); const c=tick(last+100); paused=false; return [a,b,Math.round(c*1000)]; }")
    print('clock', r)
    if r!=[0,0,100]: errs.append('clock clamp: %s' % r)
    # 6. double tap on a confirm button counts once
    r=pg.evaluate("""()=>{ const bt=document.createElement('button'); bt.dataset.confirm='recycle'; bt.textContent='Return to the roots'; document.body.appendChild(bt);
      bt.click(); bt.click(); const a=[bt.textContent, S.life.dead]; return a; }""")
    pg.wait_for_timeout(500)
    r2=pg.evaluate("()=>{ const bt=[...document.querySelectorAll('button[data-confirm=recycle]')].pop(); bt.click(); const r=[S.life.dead]; bt.remove(); return r; }")
    print('double tap', r, r2)
    if r!=['Tap again', False] or r2!=[True]: errs.append('tap guard: %s %s' % (r, r2))
    unexpected=[e for e in perr if 'boom' not in e]
    print('errors', errs + unexpected)
    b.close()
