# Quieter audio (build "quieter audio"): one shared 2 s reverb, its sends follow the music and sound volumes; with
# music off and no sound for 10 s audio sleeps (context suspended, scheduler stopped); a sound wakes it and plays;
# turning music on wakes it; the Android app pauses WebView timers in the background after saving.
from playwright.sync_api import sync_playwright
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']); pg=b.new_page(viewport={'width':420,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); sessionStorage.setItem('x','1');}")
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(800)
    pg.mouse.click(5, 5); pg.wait_for_timeout(600)
    r=pg.evaluate("()=>({state:A.ctx.state, ir:+A.verb.buffer.duration.toFixed(2), mvs:!!A.mvs, svs:!!A.svs})")
    print('graph', r)
    if r['state']!='running' or r['ir']!=2 or not r['mvs'] or not r['svs']: errs.append('reverb graph wrong: %s' % r)
    # music on: never sleeps
    pg.evaluate("()=>{ ASET.musicOn=true; audioVolumes(); A.lastSnd=0; audioNap(); }"); pg.wait_for_timeout(200)
    if pg.evaluate("()=>A.slept||false"): errs.append('slept with music on')
    # music off and quiet for 10 s: sleeps
    pg.evaluate("()=>{ ASET.musicOn=false; audioVolumes(); A.lastSnd=performance.now()-11000; audioNap(); }"); pg.wait_for_timeout(300)
    s=pg.evaluate("()=>[A.slept, A.ctx.state, A.timer]")
    print('asleep', s)
    if s[0] is not True or s[1]!='suspended' or s[2] is not None: errs.append('did not sleep: %s' % s)
    # a sound wakes it and plays
    pg.evaluate("()=>{ window.__z=0; const o=zzPlay; zzPlay=k=>{ __z++; o(k); }; sfx('gear'); }"); pg.wait_for_timeout(400)
    w=pg.evaluate("()=>[A.slept, A.ctx.state, !!A.timer, __z]")
    print('after a sound', w)
    if w[0] or w[1]!='running' or not w[2] or w[3]!=1: errs.append('sound did not wake and play: %s' % w)
    # asleep again, then music on wakes it
    pg.evaluate("()=>{ A.lastSnd=performance.now()-11000; audioNap(); }"); pg.wait_for_timeout(300)
    pg.evaluate("()=>{ ASET.musicOn=true; audioVolumes(); }"); pg.wait_for_timeout(300)
    m=pg.evaluate("()=>[A.slept, A.ctx.state]")
    print('music on', m)
    if m[0] or m[1]!='running': errs.append('music on did not wake audio: %s' % m)
    b.close()
import glob
j=open(glob.glob('/home/claude/long-patience/android/**/MainActivity.java', recursive=True)[0], encoding='utf8').read()
if 'pauseTimers()' not in j or 'resumeTimers()' not in j: errs.append('Android timers not paused/resumed')
print('errors', errs)
