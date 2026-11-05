# Folds (build "folds"): the Ship log reads oldest first, grouped by the section of the task that wrote it and folded
# like the other tabs (behind the seedling folded, current and ahead open); Records and Automation lists read oldest
# first; Archive, Mastery and Auto fold by section and by finished act; folds survive a crossing's redraw.
import json
from playwright.sync_api import sync_playwright
errs=[]
raw=open('/tmp/claude-0/sim/snap7.json').read()
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':390,'height':900}); pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script("if(!sessionStorage.getItem('x')){localStorage.clear(); localStorage.setItem('selene.slot.1', %s); localStorage.setItem('selene.active-slot','1'); sessionStorage.setItem('x','1');}" % json.dumps(raw))
    pg.goto('file:///home/claude/long-patience/index.html'); pg.wait_for_timeout(900)
    # Ship log: entries from tasks in three sections, written in this order; the seedling is in Contested Boughs (7)
    BZ=pg.evaluate("()=>[6,12,11,10,9].find(z=>TASKS.filter(t=>t.z===z&&t.log).length>=2)")
    pg.evaluate("""(BZ)=>{ hideModal(); paused=true; const pick=z=>TASKS.filter(t=>t.z===z&&t.log).slice(0,2);
      S.log=[]; [[BZ,0],[7,0],[BZ,1],[1,0]].forEach(([z,i],n)=>{ const t=pick(z)[i]; S.log.push({g:10+n, a:1, t:t.name, x:t.log}); });
      S.log.push({g:99, a:1, t:'Something else', x:'An entry no task wrote.'});
      S.evlog=[{k:'rec',g:1,a:1,t:'First record'},{k:'rec',g:2,a:1,t:'Second record'}]; logKey=''; setTab('log'); }""", BZ)
    pg.wait_for_timeout(300)
    r=pg.evaluate("""()=>{ const v=document.querySelector('#v-log');
      return {folds:[...v.querySelectorAll('[data-fold]')].map(b=>b.dataset.fold+(b.getAttribute('aria-expanded')==='true'?'+':'-')),
        arts:[...v.querySelectorAll('article.le h3')].map(h=>h.textContent), recs:[...v.querySelectorAll('.evl li b')].map(b=>b.textContent),
        other:v.innerText.includes('Other entries')}; }""")
    names=pg.evaluate("(BZ)=>{ const pick=z=>TASKS.filter(t=>t.z===z&&t.log).slice(0,2).map(t=>t.name); return {z9:pick(BZ), z7:pick(7), z1:pick(1)}; }", BZ)
    print('log', r)
    if r['folds']!=['lg:act1-','lg:%d-' % BZ,'lg:7+']: errs.append('Ship log folds wrong: %s' % r['folds'])
    if r['arts'][:1]!=names['z7'][:1] or r['arts'][1]!='Something else': errs.append('Ship log order wrong (open section oldest first, then other): %s' % r['arts'])
    if r['recs']!=['First record','Second record']: errs.append('Records list not oldest first: %s' % r['recs'])
    pg.dispatch_event('#v-log [data-fold="lg:%d"]' % BZ,'click'); pg.wait_for_timeout(300)
    arts=pg.evaluate("()=>[...document.querySelectorAll('#v-log article.le h3')].map(h=>h.textContent)")
    if arts[:2]!=names['z9']: errs.append('opened section not oldest first: %s' % arts[:4])
    # Archive, Mastery, Auto: finished Act I folded under its header, current section open
    for tab, k in [('archive','ar'),('skills','sk'),('auto','au')]:
        pg.evaluate("(t)=>{ setTab(t); }", tab); pg.wait_for_timeout(300)
        f=pg.evaluate("(k)=>[...document.querySelectorAll('#v-'+(k==='ar'?'archive':k==='sk'?'skills':'auto')+' [data-fold]')].map(b=>b.dataset.fold.split(':')[1]+(b.getAttribute('aria-expanded')==='true'?'+':'-'))", k)
        print(tab, f)
        if not f or f[0]!='act1-' or '7+' not in f: errs.append('%s folds wrong: %s' % (tab, f))
    # opening Act I on the Archive shows its sections (behind the seedling: folded)
    pg.evaluate("()=>{ setTab('archive'); }"); pg.wait_for_timeout(200)
    pg.dispatch_event('#v-archive [data-fold="ar:act1"]','click'); pg.wait_for_timeout(300)
    f=pg.evaluate("()=>[...document.querySelectorAll('#v-archive [data-fold]')].slice(0,7).map(b=>b.dataset.fold.split(':')[1]+(b.getAttribute('aria-expanded')==='true'?'+':'-'))")
    if f[0]!='act1+' or not all(x.endswith('-') for x in f[1:6]): errs.append('Archive Act I did not open with its sections: %s' % f)
    b.close()
print('errors', errs)
