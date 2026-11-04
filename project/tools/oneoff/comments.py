import re
P='/home/claude/long-patience/index.html'; s=open(P).read()
MAP=[(r"\bVat Bay\b","Seedling Vaults"),(r"\bvat bay\b","seedling vaults"),(r"\bHydroponics Ring\b","Taproot Galleries"),(r"\bEngineering Spine\b","Heartwood"),
 (r"\bCommand Deck\b","Canopy Gardens"),(r"\bMain Drive\b","Ember Crown"),(r"\bHull Breach\b","Bark Breach"),(r"\bContested Decks\b","Contested Boughs"),(r"\bthe Cruise\b","the Long Current"),(r"\bThe Cruise\b","The Long Current"),
 (r"\bthe lit drive\b","the kindled Hearth Tree"),(r"\bfirst lit drive\b","first kindling"),(r"\blights the drive\b","kindles the Hearth Tree"),(r"\bdrive is lit\b","Hearth Tree is kindled"),(r"\bLighting the drive\b","Kindling the Hearth Tree"),(r"\blighting the drive\b","kindling the Hearth Tree"),(r"\bdrive lit\b","Hearth Tree kindled"),
 (r"\bship days\b","day units (10 s in-game each)"),(r"\bship day\b","day unit"),(r"\bShip days\b","Day units"),(r"\bShip time\b","In-game time"),
 (r"\bnew game plus\b","legacy levels"),(r"\bNew game plus\b","Legacy levels"),
 (r"\bkitchen upgrades?\b","charger upgrade"),(r"\brations come more often\b","recharges come more often"),(r"\brations\b","cells"),(r"\bRations\b","Cells"),
 (r"\bfood jobs?\b","charging station"),(r"\bmeals\b","recharges"),(r"\bMeals\b","Recharges"),(r"\bmeal\b","recharge"),
 (r"\bstrain alone (limits|ends) a life\b",r"energy alone \1 a life"),(r"\band rests\b",""),(r"\brests\b","patches (removed)"),
 (r"\bspare parts\b","grafts"),(r"\bsalvage\b","deadwood"),(r"\bSalvage\b","Deadwood"),(r"\bdecanted\b","sprouted"),(r"\bdecant\b","sprout"),(r"\bDecant\b","Sprout"),
 (r"\bbay terminal\b","thinking-knot"),(r"\bclones\b","seedlings"),(r"\bClones\b","Seedlings"),(r"\bclone\b","seedling"),(r"\bClone\b","Seedling"),(r"\bHealth\b","Energy")]
def fx(c):
    for a,b in MAP: c=re.sub(a,b,c)
    return c
out=[]; pos=0
for m in re.finditer(r'(<script[^>]*>)([\s\S]*?)(</script>)', s):
    out.append(s[pos:m.start(2)]); js=m.group(2); i=0; o=[]; n=len(js); prev=''
    while i<n:
        c=js[i]
        if c=='/' and js[i+1:i+2]=='/':
            j=js.find('\n',i); j=n if j<0 else j; o.append(fx(js[i:j])); i=j; continue
        if c=='/' and js[i+1:i+2]=='*':
            j=js.find('*/',i+2)+2; o.append(fx(js[i:j])); i=j; continue
        if c in '\'"`':
            j=i+1; depth=0
            while j<n:
                if js[j]=='\\': j+=2; continue
                if c=='`' and js[j]=='$' and js[j+1:j+2]=='{': depth+=1; j+=2; continue
                if c=='`' and depth and js[j]=='}': depth-=1; j+=1; continue
                if js[j]==c and not depth: break
                j+=1
            o.append(js[i:j+1]); i=j+1; prev='x'; continue
        if c=='/' and prev in '(,=:[!&|?{};+-*%<>~^':
            j=i+1; cls=False
            while j<n:
                if js[j]=='\\': j+=2; continue
                if js[j]=='[': cls=True
                elif js[j]==']': cls=False
                elif js[j]=='/' and not cls: break
                j+=1
            j+=1
            while j<n and js[j].isalpha(): j+=1
            o.append(js[i:j]); i=j; prev='/'; continue
        o.append(c)
        if not c.isspace(): prev = c if not (c.isalnum() or c in '_$') else 'x'
        i+=1
    out.append(''.join(o)); pos=m.end(2)
out.append(s[pos:]); s=''.join(out)
# CSS comments
s=re.sub(r'/\*[^*]*emergency[^*]*\*/', lambda m: m.group(0), s)
open(P,'w').write(s); print('comments ok')
