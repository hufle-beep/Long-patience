#!/usr/bin/env python3
"""Rebuild the embedded font block in index.html (<style id="fonts">).

The game ships trimmed copies of three SIL OFL fonts from github.com/google/fonts,
renamed because the originals carry Reserved Font Names ("Saira", "Plex"):
  Selene Display = Saira Condensed 500/600/700   (Omnibus-Type, OFL)
  Selene Text    = IBM Plex Sans 400/500/600     (IBM Corp., OFL; fixed weights cut from the variable font)
  Selene Mono    = IBM Plex Mono 400/500         (IBM Corp., OFL)
Each copy keeps its copyright and licence fields (name IDs 0, 13, 14). Licences: project/fonts/.

Characters kept: printable ASCII, Latin-1 (U+00A0-00FF) and every other character that appears in
index.html, literally or as a \\uXXXX / &#x...; escape. Rerun this after new texts add characters.

Needs: fonttools, and the brotli module for WOFF2 (PyPI has none in the cloud workspace; build it
from source: git clone --depth 1 --branch v1.1.0 https://github.com/google/brotli &&
pip install --break-system-packages --no-build-isolation ./brotli).
Fonts: a sparse clone of google/fonts at FONTS (default /home/claude/google/fonts), made if missing.

Usage: python3 fontpack.py [path/to/index.html]
"""
import base64, io, os, re, subprocess, sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

HTML = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/long-patience/index.html'
FONTS = os.environ.get('FONTS', '/home/claude/google/fonts')
DIRS = ['ofl/sairacondensed', 'ofl/ibmplexsans', 'ofl/ibmplexmono']

# (css family, weight, source file, variable-font weight to cut, or None)
FACES = [
    ('Selene Display', 500, 'ofl/sairacondensed/SairaCondensed-Medium.ttf', None),
    ('Selene Display', 600, 'ofl/sairacondensed/SairaCondensed-SemiBold.ttf', None),
    ('Selene Display', 700, 'ofl/sairacondensed/SairaCondensed-Bold.ttf', None),
    ('Selene Text', 400, 'ofl/ibmplexsans/IBMPlexSans[wdth,wght].ttf', 400),
    ('Selene Text', 500, 'ofl/ibmplexsans/IBMPlexSans[wdth,wght].ttf', 500),
    ('Selene Text', 600, 'ofl/ibmplexsans/IBMPlexSans[wdth,wght].ttf', 600),
    ('Selene Mono', 400, 'ofl/ibmplexmono/IBMPlexMono-Regular.ttf', None),
    ('Selene Mono', 500, 'ofl/ibmplexmono/IBMPlexMono-Medium.ttf', None),
]
STYLE = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold'}
START, END = '<style id="fonts">', '</style>'


def ensure_fonts():
    if not os.path.isdir(os.path.join(FONTS, DIRS[0])):
        os.makedirs(os.path.dirname(FONTS), exist_ok=True)
        env = dict(os.environ, GIT_LFS_SKIP_SMUDGE='1')
        subprocess.run(['git', 'clone', '-q', '--depth', '1', '--filter=blob:none', '--sparse',
                        'https://github.com/google/fonts', FONTS], check=True, env=env)
        subprocess.run(['git', '-C', FONTS, 'sparse-checkout', 'set'] + DIRS, check=True)


def game_chars(html):
    body = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', html, flags=re.S)   # never count the font data itself
    cs = set(body)
    cs |= {chr(int(h, 16)) for h in re.findall(r'\\u([0-9a-fA-F]{4})', body)}
    cs |= {chr(int(h, 16)) for h in re.findall(r'&#x([0-9a-fA-F]+);', body)}
    cs |= {chr(c) for c in range(0x20, 0x7f)} | {chr(c) for c in range(0xa0, 0x100)}
    return ''.join(sorted(c for c in cs if ord(c) >= 0x20))


def rename(font, family, weight):
    style = STYLE[weight]
    name = font['name']
    for rec in list(name.names):
        if rec.nameID in (16, 17, 21, 22, 25) or rec.nameID >= 256:
            name.removeNames(nameID=rec.nameID)   # typographic/variation names of the original
    full = family + (' ' + style if style != 'Regular' else '')
    vals = {1: full if style not in ('Regular', 'Bold') else family, 2: style if style in ('Regular', 'Bold') else 'Regular',
            3: full.replace(' ', '') + ';trimmed for Selene: Tidelocked', 4: full, 6: full.replace(' ', '-')}
    for nid, v in vals.items():
        name.removeNames(nameID=nid)
        name.setName(v, nid, 3, 1, 0x409)
        name.setName(v, nid, 1, 0, 0)
    if 'STAT' in font: del font['STAT']


def face(family, weight, src, vw, chars):
    f = TTFont(os.path.join(FONTS, src))
    if vw is not None:
        f = instancer.instantiateVariableFont(f, {'wght': vw, 'wdth': 100})
    opts = subset.Options()
    opts.flavor = 'woff2'
    opts.layout_features = ['kern', 'liga', 'tnum']
    opts.name_IDs = [0, 1, 2, 3, 4, 5, 6, 13, 14]
    opts.name_languages = ['*']
    s = subset.Subsetter(opts)
    s.populate(text=chars)
    s.subset(f)
    rename(f, family, weight)
    f.flavor = 'woff2'
    buf = io.BytesIO(); f.save(buf)
    return buf.getvalue()


def main():
    ensure_fonts()
    html = open(HTML, encoding='utf8').read()
    chars = game_chars(html)
    rules, total = [], 0
    for family, weight, src, vw in FACES:
        data = face(family, weight, src, vw, chars)
        total += len(data)
        rules.append("@font-face{font-family:'%s';font-style:normal;font-weight:%d;font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2')}"
                     % (family, weight, base64.b64encode(data).decode()))
    block = (START + '\n/* Fonts, embedded so the game looks right offline. Trimmed and renamed copies of SIL Open Font License 1.1 fonts '
             '(github.com/google/fonts): Selene Display = Saira Condensed, (c) 2016 The Saira Project Authors; Selene Text = IBM Plex Sans and '
             'Selene Mono = IBM Plex Mono, (c) 2017 IBM Corp. Renamed because "Saira" and "Plex" are Reserved Font Names. '
             'Licences: project/fonts/ in the repo. Rebuilt by project/tools/fontpack.py. */\n' + '\n'.join(rules) + '\n' + END)
    if START in html:
        html = re.sub(re.escape(START) + r'.*?' + re.escape(END), lambda m: block, html, count=1, flags=re.S)
    else:
        html = html.replace('<style>\n', block + '\n<style>\n', 1)
    open(HTML, 'w', encoding='utf8').write(html)
    print('fonts: %d faces, %d KB woff2, %d chars kept' % (len(FACES), total // 1024, len(chars)))


if __name__ == '__main__':
    main()
