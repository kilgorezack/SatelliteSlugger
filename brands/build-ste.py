#!/usr/bin/env python3
"""Build ste/index.html (the STE Communications edition) from the main index.html.

The game itself lives in one place: index.html. This script copies it and swaps in STE's
branding (colors, fonts, logo, copy, sign-up link, separate leaderboard). After changing the
main game, re-run:  python3 brands/build-ste.py
"""
import base64, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text()
logo = base64.b64encode((ROOT / 'brands' / 'ste-logo-white.png').read_bytes()).decode()

def sub(old, new, count=1):
    """Replace exactly `count` occurrences (0 = all, at least one); fail loudly if the game changed."""
    global src
    n = src.count(old)
    if n == 0 or (count and n != count):
        sys.exit(f'build-ste: expected {count or "1+"} of {old!r}, found {n}')
    src = src.replace(old, new)

# ---- page meta, fonts ---------------------------------------------------------------
sub('<title>Satellite Slugger</title>', '<title>Satellite Slugger · STE</title>')
sub('content="Time your swing, launch the ball into low Earth orbit, and knock satellite internet out of the sky."',
    'content="Satellite Slugger from STE: time your swing and knock satellite internet out of the sky. Fiber Internet from neighbors who actually pick up the phone."')
sub('<meta name="theme-color" content="#070b1f">', '<meta name="theme-color" content="#0b0628">')
sub('family=Bowlby+One&family=Martian+Mono:wght@400;600;800', 'family=Archivo:wght@800;900&family=Work+Sans:wght@400;600;800')

# ---- palette: STE navy / magenta / red / amber ---------------------------------------
for old, new in [
    ('--night:#070b1f;', '--night:#0b0628;'),
    ('--panel:#0f1536;', '--panel:#150c48;'),
    ('--panel-edge:#232c63;', '--panel-edge:#30238f;'),
    ('--chalk:#f2efe4;', '--chalk:#f7f5fc;'),
    ('--muted:#8c94c4;', '--muted:#a59fd6;'),
    ('--amber:#ffb547;', '--amber:#ffb236;'),
    ('--fiber:#3fe3ff;', '--fiber:#ff2e63;'),
    ('--flare:#ff5a3c;', '--flare:#ff8a3c;'),
    ("--display:'Bowlby One', Impact, 'Arial Black', sans-serif;", "--display:'Archivo', 'Arial Black', sans-serif;"),
    ("--mono:'Martian Mono', ui-monospace, 'SFMono-Regular', Menlo, monospace;", "--mono:'Work Sans', system-ui, sans-serif;"),
]:
    sub(old, new)
sub('font-family:var(--display);font-weight:400', 'font-family:var(--display);font-weight:900', 0)
sub('.slot .ch{font-family:var(--display);', '.slot .ch{font-family:var(--display);font-weight:900;')
sub('rgba(63,227,255', 'rgba(255,46,99', 0)
sub('rgba(255,181,71', 'rgba(255,178,54', 0)
sub('#1a8fb3', '#960263')                  # gigabit meter: STE magenta into STE red
sub('#138aa3', '#a3002e', 0)               # fiber button shadows
sub('color:#002a33', 'color:#fff', 0)      # text on fiber-red buttons
sub('#bff6ff', '#ffd0dd')
sub('#c9cdea', '#d4d0ee', 0)
sub('background:#04061a', 'background:#06031a')
sub('#3fe3ff', '#ff2e63', 0)               # canvas: gigabit text + banner
sub('#ff5a3c', '#ff8a3c', 0)               # canvas: strikes / outs
sub('#ffb547', '#ffb236', 0)
sub("'#7cefff'", "'#ff7aa0'")              # charged bat
sub("'#e6fdff'", "'#ffe3ec'")
sub("g.addColorStop(0,'#03051a'); g.addColorStop(.5,'#0d1440'); g.addColorStop(.8,'#33275a'); g.addColorStop(.94,'#a44f68'); g.addColorStop(1,'#ea8b58');",
    "g.addColorStop(0,'#04021a'); g.addColorStop(.5,'#110a50'); g.addColorStop(.8,'#33135e'); g.addColorStop(.94,'#8a0a5c'); g.addColorStop(1,'#e0305a');")
sub("ctx.strokeStyle = '#1f6fd1'", "ctx.strokeStyle = '#3a2ee6'", 0)   # jersey: STE blue
sub("ctx.fillStyle = '#14204a'; ctx.beginPath(); ctx.arc(5,-100", "ctx.fillStyle = '#f80040'; ctx.beginPath(); ctx.arc(5,-100")  # helmet: STE red

# ---- canvas fonts ----
sub('"Martian Mono", monospace', '"Work Sans", sans-serif', 0)
sub('`400 ${58*sc}px "Bowlby One", Impact, sans-serif`', '`900 ${58*sc}px "Archivo", "Arial Black", sans-serif`')

# ---- masthead with the STE logo ----
sub('.masthead h1 span{color:var(--fiber)}',
    '.masthead h1 span{color:var(--fiber)}\n'
    '.masthead{align-items:center}\n'
    '.masthead h1{display:flex;align-items:center;gap:.45em}\n'
    '.masthead .logo{height:1.15em;width:auto;display:block;flex:none}\n'
    '.masthead .logo-link{display:block;flex:none;border-radius:3px}\n'
    '.masthead .logo-link:focus-visible{outline:3px solid var(--fiber);outline-offset:3px}')
sub('<h1>Satellite <span>Slugger</span></h1>',
    f'<h1><a class="logo-link" href="https://goste.net/" target="_blank" rel="noopener"><img class="logo" src="data:image/png;base64,{logo}" alt="STE" width="264" height="98"></a><span style="color:inherit">Satellite</span> <span>Slugger</span></h1>')

# ---- brand constants ----
sub("const BRAND = 'Your Local Fiber';", "const BRAND = 'STE';")
sub("const JERSEY = 'FIBER';", "const JERSEY = 'STE';")
sub("const CTA_TEXT = 'Check fiber at your address';", "const CTA_TEXT = 'See what’s available at your address';")
sub("const CTA_URL = '';", "const CTA_URL = 'https://ste.smarthub.coop/Shop.html';")
sub("$('brandLine').textContent = 'Presented by ' + BRAND;", "$('brandLine').textContent = 'Presented by STE · Proudly local since 1952';")
sub("$('presented').textContent = BRAND + ' · Ground beats orbit';", "$('presented').textContent = 'Internet that’s totally you';")

# ---- copy with a local STE accent ----
sub("'Called support. A local human answered. Same zip code.',", "'Called STE. A neighbor picked up. Same zip code.',")
sub("'No dish to aim. No tree to trim. Just internet.',",
    "'No dish to aim. No tree to trim. Just internet.',\n"
    "    'Friday night game streamed all over Steelville. Not one buffer.',\n"
    "    'The {n}s’ internet is as unique as their fingerprint. And way faster.',\n"
    "    'Local since 1952. Still answering the phone.',")
sub("in Satellite Slugger (${S.score.toLocaleString()} pts). Ground beats orbit.`",
    "in Satellite Slugger from STE (${S.score.toLocaleString()} pts). Ground beats orbit. goste.net`")

# ---- its own leaderboard ----
sub("const API = '/api/scores',", "const API = '/api/scores?board=ste',")
sub("localStorage.getItem('ffBest')", "localStorage.getItem('steBest')")
sub("localStorage.setItem('ffBest', best)", "localStorage.setItem('steBest', best)")
sub("'ssIni'", "'steIni'", 0)
sub("'ssBoard'", "'steBoard'", 0)

(ROOT / 'ste' / 'index.html').write_text(src)
print('wrote ste/index.html')
