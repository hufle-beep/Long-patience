import base64,gzip,json,os
from playwright.sync_api import sync_playwright
OUT='/home/claude/shots'; URL='file:///home/claude/long-patience/index.html'
up=gzip.decompress(base64.b64decode(open('/home/claude/long-patience/saves/hufle2-2026-11-04-1241-clone10.txt').read()[5:].strip())).decode()
s7=open('/tmp/claude-0/sim/snap7.json').read(); s12=open('/tmp/claude-0/sim/snap12.json').read()
errs=[]
def page(b, raw=None):
    ctx=b.new_context(viewport={'width':420,'height':900}, device_scale_factor=2); pg=ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
    if raw: pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); localStorage.setItem('selene.prefs.v1', JSON.stringify({startPaused:true})); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto(URL); pg.wait_for_timeout(1200); return pg
def shot(pg, name, full=True):
    pg.evaluate("(f)=>{ let st=document.getElementById('shotcss'); if(!st){st=document.createElement('style');st.id='shotcss';document.head.appendChild(st);} st.textContent = f ? '#tabs{position:static!important} header,.hdr,.sticky{position:static!important}' : ''; }", full)
    pg.wait_for_timeout(350); pg.screenshot(path=f'{OUT}/{name}.png', full_page=full)
def ready(pg):
    pg.evaluate("()=>{ hideModal(); paused=true; S.intro=true; for (const k in secFold) delete secFold[k]; }")
def tab(pg, t, name):
    pg.evaluate(f"()=>{{ setTab('{t}'); window.scrollTo(0,0); }}"); shot(pg, name)
with sync_playwright() as p:
    b=p.chromium.launch()
    # fresh game
    pg=page(b); shot(pg,'01-intro',False)
    pg.click('text=Begin the work cycle'); pg.wait_for_timeout(300); pg.evaluate("()=>{paused=true}"); tab(pg,'tasks','02-first-seedling-tasks')
    pg.evaluate("showMenu()"); shot(pg,'03-main-menu',False)
    pg.evaluate("showMenu('new')"); pg.click('[data-newin="2"]'); pg.wait_for_timeout(200); pg.fill('#ow-name','First voyage'); shot(pg,'04-new-game-name',False)
    # the uploaded save: Taproot Galleries
    pg=page(b, up); ready(pg)
    for t,n in [('tasks','05-taproot-tasks'),('map','06-map'),('auto','07-auto'),('skills','08-mastery'),('archive','09-archive'),('log','10-log'),('faq','11-faq')]: tab(pg,t,n)
    pg.evaluate("()=>{ logTables=true; setTab('log'); window.scrollTo(0,0); }"); shot(pg,'12-log-tables')
    pg.evaluate("showMenu('saves')"); shot(pg,'13-save-management',False)
    pg.evaluate("showSettings()"); shot(pg,'14-settings',False)
    pg.evaluate("()=>{ hideModal(); S.life.hp=-1; die('Drained faster than it could recharge'); }"); pg.wait_for_timeout(400); shot(pg,'15-death-screen',False)
    # Act II
    pg=page(b, s7); ready(pg); tab(pg,'tasks','16-contested-boughs-tasks'); tab(pg,'map','17-act2-map'); tab(pg,'archive','18-act2-archive')
    pg=page(b, s12); ready(pg); tab(pg,'tasks','19-turnover-tasks'); tab(pg,'skills','20-turnover-mastery'); tab(pg,'log','21-act2-log')
    b.close()
print('errors', errs)
for f in sorted(os.listdir(OUT)): print(f, os.path.getsize(f'{OUT}/{f}')//1024, 'KB')
