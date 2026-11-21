"""Build the static Sangai First Foundation website into ../site.

Plain HTML + one CSS file + one small vanilla JS file. All copy and data live
here (ported from generate_pages.py, which produced the Design-canvas pages).

    python3 source/build_site.py
"""
import hashlib
import html
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, 'site')

IMG = 'images/'
DEER = IMG + 'deer-hd.jpg'
GROUP = IMG + 'group-hd.jpg'
SPEAKER = IMG + 'speaker-hd.jpg'
CLASS = IMG + 'class-hd.jpg'
ENGRAVE = IMG + 'deer-engraving.png'
NEWSPRINT = IMG + 'founders-newsprint.webp'
# Wikimedia Commons photos (credited in the Discover footer)
PHUMDI = IMG + 'phumdi.jpg'
KEIBUL = IMG + 'keibul-lamjao.jpg'
LOKTAK = IMG + 'loktak.jpg'
RAAS = IMG + 'raas-lila.jpg'
PHEASANT = IMG + 'humes-pheasant.jpg'
LILY = IMG + 'shirui-lily.jpg'
SANGAI2 = IMG + 'sangai-kasambe.jpg'
STAG = IMG + 'sangai-stag.jpg'  # the Foundation's own photo; no credit needed

PAGES = {'Home': 'index.html', 'Discover': 'discover.html', 'Our Work': 'work.html', 'About': 'about.html', 'Contact': 'contact.html'}

e = html.escape

# ---------------------------------------------------------------- CSS / JS
CSS = r''':root{
  --bg:#FBFBFD; --card:#FFFFFF; --card2:#F2F2F7;
  --label:#1D1D1F; --label2:#3A3A3C; --label3:#636366;
  --sep:rgba(60,60,67,0.18);
  --tint:#008932; --on-tint:#FFFFFF; --tint-fill:#E8F5EC;
  --glass:rgba(251,251,253,0.72); --glass-edge:rgba(255,255,255,0.9);
  --shadow:0 10px 40px rgba(0,0,0,0.07);
  color-scheme: light dark;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#000000; --card:#1C1C1E; --card2:#2C2C2E;
    --label:#F5F5F7; --label2:#D1D1D6; --label3:#AEAEB2;
    --sep:rgba(84,84,88,0.65);
    --tint:#30D158; --on-tint:#000000; --tint-fill:rgba(48,209,88,0.14);
    --glass:rgba(28,28,30,0.66); --glass-edge:rgba(255,255,255,0.12);
    --shadow:0 10px 40px rgba(0,0,0,0.5);
  }
  .engrave{filter:invert(1)}
}
@media (prefers-contrast: more){ :root{ --tint:#006B26; --label2:#1C1C1E; --label3:#3A3A3C; --glass:rgba(255,255,255,0.95) } }
@media (prefers-contrast: more) and (prefers-color-scheme: dark){ :root{ --tint:#4AD968; --label2:#F2F2F7; --label3:#D1D1D6; --glass:rgba(28,28,30,0.95) } }
@media (prefers-reduced-transparency: reduce){ :root{ --glass:var(--card) } }

*,*::before,*::after{box-sizing:border-box}
[hidden]{display:none !important}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--label);font-family:-apple-system,BlinkMacSystemFont,"SF Pro Text",Inter,system-ui,sans-serif;font-size:17px;line-height:1.5;-webkit-font-smoothing:antialiased}
main{overflow-x:clip}
img{max-width:100%}
@media (prefers-reduced-motion: no-preference){ html{scroll-behavior:smooth} }
a{color:var(--tint)} a:hover{opacity:0.8}
a:focus-visible,button:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--tint);outline-offset:3px}
.glassbar{-webkit-backdrop-filter:blur(24px) saturate(180%);backdrop-filter:blur(24px) saturate(180%)}
.track{scrollbar-width:none;padding-left:24px;padding-right:24px}
.track::-webkit-scrollbar{display:none}
button{font:inherit}
.skip{position:absolute;left:16px;top:-80px;z-index:20;padding:10px 18px;border-radius:999px;background:var(--tint);color:var(--on-tint);font-weight:600;text-decoration:none}
.skip:focus{top:12px}

/* header: a glass pill; the round logo badge and the CTA sit 8px in from each end */
.site-header{position:sticky;top:0;z-index:10;padding:12px 16px 0}
.nav{max-width:1080px;margin:0 auto;display:flex;flex-wrap:wrap;align-items:center;gap:0 8px;padding:8px;background:var(--glass);border-radius:999px;box-shadow:var(--shadow)}
.brand{display:flex;align-items:center;gap:12px;min-width:0;min-height:44px;padding-right:12px;border-radius:999px;text-decoration:none;color:var(--label);font-weight:600;font-size:16px;letter-spacing:-0.01em;white-space:nowrap}
.brand:hover{opacity:1}
.brand-mark{flex:none;display:block;width:40px;height:44px;overflow:hidden}
/* head and antlers of the engraving on a transparent background; the neck fades out at the bottom */
.brand-mark img{display:block;width:100%;height:100%;object-fit:cover;object-position:20% 0;-webkit-mask-image:linear-gradient(to bottom,#000 72%,transparent);mask-image:linear-gradient(to bottom,#000 72%,transparent)}
.brand-name{overflow:hidden;text-overflow:ellipsis}
.nav-menu{display:flex;align-items:center;margin-left:auto}
.nav-links{display:flex;align-items:center;margin:0;padding:0;list-style:none;font-size:15px}
.nav-links a{display:inline-flex;align-items:center;min-height:44px;padding:0 9px;white-space:nowrap;border-radius:999px;color:var(--label2);font-weight:500;text-decoration:none}
.nav-links a:hover{opacity:1;color:var(--label)}
.nav-links a[aria-current="page"]{color:var(--label);font-weight:600}
/* CTA: a quiet tonal pill, 36px tall to sit inside the bar, with a full 44px tap area */
.nav-cta{position:relative;display:inline-flex;align-items:center;justify-content:center;height:36px;padding:0 16px;margin:4px 0 4px 10px;background:var(--tint-fill);color:var(--tint);text-decoration:none;border-radius:999px;font-weight:600;font-size:15px;white-space:nowrap}
.nav-cta::after{content:"";position:absolute;inset:-4px}
.nav-cta:hover{opacity:1;background:var(--tint);color:var(--on-tint)}
.nav-cta[aria-current="page"]{background:var(--tint);color:var(--on-tint)}
@media (max-width: 760px){
  /* phones: badge + name + Support us on top, the four links in a row underneath */
  .nav{border-radius:30px;padding:8px 8px 2px}
  .nav-menu{display:contents}
  .brand{flex:1 1 0;gap:10px;padding-right:0;white-space:normal}
  .brand-name{font-size:15px;line-height:1.15;max-width:9.5em;overflow:visible}
  .nav-cta{padding:0 14px;margin:4px 0}
  .nav-links{order:3;flex:1 1 100%;margin:0 0 0 50px;justify-content:space-between} /* 50px = logo 40 + gap 10: starts under the name */
  .nav-links li:first-child a{padding-left:0}
  .nav-links li:last-child a{padding-right:0}
}
@media (min-width: 481px) and (max-width: 760px){ .nav-links{justify-content:flex-start;gap:14px} }
@media (max-width: 370px){ .nav-links{font-size:14px} .nav-links a{padding:0 4px} }
@media (max-width: 330px){ .nav-links{font-size:13px} }

/* deer watermark: the engraving, large and faint, peeking from behind carousels and cards */
.has-wm{position:relative;isolation:isolate}
.wm{position:absolute;z-index:-1;height:auto;max-width:none;pointer-events:none;user-select:none;-webkit-user-select:none;opacity:0.07}
@media (prefers-color-scheme: dark){ .wm{filter:invert(1);opacity:0.09} }
.wm-right{right:-70px;top:24px;width:360px}
.wm-left{left:-90px;top:40px;width:340px;transform:scaleX(-1)}
.wm-center{left:50%;top:24px;width:300px;transform:translateX(-50%);opacity:0.05}
.card-wm{position:relative;isolation:isolate;overflow:hidden}
.card-wm .wm{right:-48px;bottom:-70px;width:220px;filter:invert(1);opacity:0.13}
@media (max-width: 720px){
  .wm-right{right:-90px;width:260px}
  .wm-left{left:-100px;width:240px}
  .wm-center{width:220px}
}

/* programme details: a button on the card opens a dialog */
.ev-more{align-self:flex-start;display:inline-flex;align-items:center;gap:4px;min-height:44px;margin:-8px 0 -12px;padding:0;border:0;background:none;color:var(--tint);font-size:15px;font-weight:600;cursor:pointer}
.ev-more:hover{opacity:0.8}
.dlg{width:min(600px,calc(100% - 32px));max-height:min(86vh,760px);margin:auto;padding:0;border:0;border-radius:28px;background:var(--card);color:var(--label);box-shadow:0 30px 80px rgba(0,0,0,0.35);overflow:auto}
.dlg::backdrop{background:rgba(0,0,0,0.42);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}
@media (prefers-reduced-motion: no-preference){ .dlg[open]{animation:dlg-in .22s ease-out} @keyframes dlg-in{from{opacity:0;transform:translateY(12px) scale(.98)}to{opacity:1;transform:none}} }
.dlg-body{position:relative;padding:32px 32px 28px}
.dlg-close{position:absolute;top:16px;right:16px;display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;border:0;border-radius:999px;background:var(--card2);color:var(--label);cursor:pointer}
.dlg-date{margin:0;font-size:13px;font-weight:600;letter-spacing:0.04em;color:var(--tint)}
.dlg-title{margin:6px 56px 0 0;font-size:28px;line-height:1.15;font-weight:700;letter-spacing:-0.02em}
.dlg-place{margin:6px 0 0;font-size:15px;color:var(--label3)}
.dlg-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin:24px 0 0}
.dlg-stat{padding:14px 16px;border-radius:18px;background:var(--tint-fill)}
.dlg-n{margin:0;font-size:28px;line-height:1;font-weight:700;letter-spacing:-0.03em;color:var(--tint)}
.dlg-l{margin:6px 0 0;font-size:13px;color:var(--label2)}
.dlg-h{margin:28px 0 10px;font-size:13px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;color:var(--label3)}
.dlg-points{margin:0;padding:0;list-style:none}
.dlg-points li{position:relative;padding:10px 0 10px 22px;border-top:1px solid var(--sep);font-size:16px;line-height:1.45;color:var(--label2)}
.dlg-points li:first-child{border-top:0;padding-top:0}
.dlg-points li::before{content:"";position:absolute;left:2px;top:19px;width:8px;height:8px;border-radius:999px;background:var(--tint)}
.dlg-points li:first-child::before{top:9px}
.dlg-who{display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;list-style:none}
.dlg-who li{padding:6px 12px;border-radius:999px;background:var(--card2);font-size:14px;color:var(--label2)}
.dlg-src{margin:24px 0 0;font-size:13px;color:var(--label3)}
@media (max-width: 520px){ .dlg-body{padding:28px 20px 24px} .dlg-title{font-size:24px} }

/* stateful controls (state lives in aria attributes, set by site.js) */
.dot span{display:block;width:8px;height:8px;border-radius:999px;background:rgba(255,255,255,0.45)}
.dot[aria-current="true"] span{background:#FFFFFF}
.dtab{min-height:44px;padding:0 16px;border-radius:999px;cursor:pointer;font-size:14px;font-weight:600;border:1px solid rgba(255,255,255,0.35);background:rgba(0,0,0,0.2);color:#FFFFFF}
.dtab[aria-selected="true"]{background:#FFFFFF;color:#111111}
.seg{min-height:40px;padding:0 20px;border:0;border-radius:999px;cursor:pointer;font-size:15px;font-weight:600;background:transparent;color:var(--label2)}
.seg[aria-pressed="true"]{background:var(--card);color:var(--label);box-shadow:0 1px 4px rgba(0,0,0,0.12)}
.answer:focus{outline:none}

/* narrow: Discover slide text sits over a dimmed full-bleed photo */
@media (max-width: 900px){
  .dslide{position:relative !important;min-height:600px}
  .dslide-img{width:100% !important;opacity:0.35}
  .dslide-fade{display:none}
  .dslide-body{padding-bottom:140px !important}
}

/* phone layout */
@media (max-width: 720px){
  .hero{height:520px !important}
  .hero-cap{padding:96px 24px 96px !important}
  .hero-ctrl{right:50% !important;transform:translateX(50%);bottom:20px !important}
  .split{grid-template-columns:1fr !important}
  .split img{height:240px !important}
  .dslide-body{padding:40px 24px 200px !important}
  .dctrl{left:24px !important;right:24px !important}
  .clip{height:510px !important}
  .clip-text{columns:1 !important}
  .pad-card{padding:28px 24px !important}
  .bars{gap:8px !important}
  .bars .lab{display:none}
}
'''

JS = r'''// Sangai First Foundation: carousels, slideshows, quiz and year switch.
(function () {
  var reduce = function () {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  };

  // Horizontal carousels: arrow buttons scroll the visible track.
  document.querySelectorAll('[data-carousel]').forEach(function (c) {
    c.querySelectorAll('[data-scroll]').forEach(function (b) {
      b.addEventListener('click', function () {
        var t = c.querySelector('[data-track]:not([hidden])');
        t.scrollBy({ left: Number(b.dataset.scroll) * t.clientWidth * 0.8, behavior: reduce() ? 'auto' : 'smooth' });
      });
    });
  });

  // Slideshows (Home hero, Discover topics): one slide visible at a time.
  document.querySelectorAll('[data-slideshow]').forEach(function (root) {
    var slides = Array.prototype.slice.call(root.querySelectorAll('[data-slide]'));
    var pickers = Array.prototype.slice.call(root.querySelectorAll('[data-go]'));
    var cur = 0;
    function show(i) {
      cur = (i + slides.length) % slides.length;
      slides.forEach(function (s, j) { s.hidden = j !== cur; });
      pickers.forEach(function (p) {
        var on = String(Number(p.dataset.go) === cur);
        p.setAttribute(p.getAttribute('role') === 'tab' ? 'aria-selected' : 'aria-current', on);
      });
    }
    root.querySelector('[data-prev]').addEventListener('click', function () { show(cur - 1); });
    root.querySelector('[data-next]').addEventListener('click', function () { show(cur + 1); });
    pickers.forEach(function (p) {
      p.addEventListener('click', function () { show(Number(p.dataset.go)); });
    });
    root.addEventListener('keydown', function (ev) {
      if (ev.target.closest('a')) return;
      if (ev.key === 'ArrowLeft') { show(cur - 1); }
      else if (ev.key === 'ArrowRight') { show(cur + 1); }
    });
    show(0);
  });

  // Quiz: reveal an answer and move focus to it.
  document.querySelectorAll('[data-reveal]').forEach(function (b) {
    b.addEventListener('click', function () {
      var a = b.parentElement.querySelector('[data-answer]');
      a.hidden = false;
      a.focus();
      b.remove();
    });
  });

  // Programme details dialogs.
  document.querySelectorAll('[data-open]').forEach(function (b) {
    var d = document.getElementById(b.dataset.open);
    if (!d || !d.showModal) return;
    b.addEventListener('click', function () { d.showModal(); });
    d.addEventListener('click', function (ev) { if (ev.target === d) d.close(); });
  });

  // Year switch on Our Work.
  document.querySelectorAll('[data-years]').forEach(function (group) {
    var c = group.closest('[data-carousel]');
    group.querySelectorAll('[data-year]').forEach(function (b) {
      b.addEventListener('click', function () {
        group.querySelectorAll('[data-year]').forEach(function (o) {
          o.setAttribute('aria-pressed', String(o === b));
        });
        c.querySelectorAll('[data-panel]').forEach(function (p) {
          p.hidden = p.dataset.panel !== b.dataset.year;
          p.scrollLeft = 0;
        });
      });
    });
  });
})();
'''

# cache-busting version: changes whenever the CSS or JS changes
VER = hashlib.sha1((CSS + JS).encode('utf-8')).hexdigest()[:8]

# ---------------------------------------------------------------- shared parts
def wm(pos):
    """Decorative deer watermark; pos is right, left, center or card."""
    cls = '' if pos == 'card' else f' wm-{pos}'
    return f'<img class="wm{cls}" src="{ENGRAVE}" alt="" aria-hidden="true" loading="lazy">'


def nav(active):
    links = ''
    for name in ('Home', 'Discover', 'Our Work', 'About'):
        cur = ' aria-current="page"' if name == active else ''
        links += f'\n        <li><a href="{PAGES[name]}"{cur}>{name}</a></li>'
    cur = ' aria-current="page"' if active == 'Contact' else ''
    return f'''  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <nav aria-label="Main" class="glassbar nav">
      <a class="brand" href="index.html">
        <span class="brand-mark" aria-hidden="true"><img class="engrave" src="{ENGRAVE}" alt=""></span>
        <span class="brand-name">Sangai First Foundation</span>
      </a>
      <div class="nav-menu" id="nav-menu">
        <ul class="nav-links">{links}
        </ul>
        <a class="nav-cta" href="contact.html"{cur}>Support us</a>
      </div>
    </nav>
  </header>'''


def footer(credits=''):
    extra = f'\n      <p style="flex: 1 1 100%; margin: 0; line-height: 1.6">{credits}</p>' if credits else ''
    return f'''  <footer>
    <div style="max-width: 1080px; margin: 0 auto; padding: 40px 32px 48px; border-top: 1px solid var(--sep); display: flex; flex-wrap: wrap; gap: 8px 32px; justify-content: space-between; font-size: 13px; color: var(--label3)">
      <p style="margin: 0">© Sangai First Foundation, Manipur · Reg. no. 442 of 02/10/2025, Indian Trusts Act, 1882</p>
      <a href="https://www.facebook.com/profile.php?id=61573232295835" style="display: inline-flex; align-items: center; min-height: 44px; margin: -12px 0">Facebook</a>{extra}
    </div>
  </footer>'''


CHEV_L = '<svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2L2 8l6 6"></path></svg>'
CHEV_R = '<svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 2l6 6-6 6"></path></svg>'


def arrows(label):
    btn = 'display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 999px; border: 1px solid var(--sep); background: var(--card); color: var(--label); cursor: pointer; padding: 0'
    return f'''<div style="display: flex; gap: 8px; flex: none">
            <button type="button" aria-label="Previous {label}" data-scroll="-1" style="{btn}">{CHEV_L}</button>
            <button type="button" aria-label="Next {label}" data-scroll="1" style="{btn}">{CHEV_R}</button>
          </div>'''


GLASS_BTN = 'display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border: 0; border-radius: 999px; background: transparent; color: #FFFFFF; cursor: pointer; padding: 0'
TRACK = 'display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding-top: 4px; padding-bottom: 24px; scroll-padding-left: 24px; list-style: none; margin: 0'
H2 = 'margin: 0; font-size: 34px; line-height: 1.15; font-weight: 700; letter-spacing: -0.022em'
SEC = 'max-width: 1080px; margin: 0 auto; padding: 120px 24px 0'
CTA = 'display: inline-flex; align-items: center; min-height: 50px; padding: 0 28px; background: var(--tint); color: var(--on-tint); text-decoration: none; border-radius: 999px; font-weight: 600'


def page(title, desc, active, body, credits=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#FBFBFD" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{ENGRAVE}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Playfair+Display:wght@900&amp;display=swap">
<link rel="stylesheet" href="assets/styles.css?v={VER}">
<script src="assets/site.js?v={VER}" defer></script>
</head>
<body>
{nav(active)}
  <main id="main">
{body}
  </main>
{footer(credits)}
</body>
</html>
'''


def section_head(title, link_html, label):
    return f'''      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px">
        <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; margin-bottom: 24px">
          <div>
            <h2 style="{H2}">{title}</h2>
            {link_html}
          </div>
          {arrows(label)}
        </div>
      </div>'''


# ---------------------------------------------------------------- HOME
slides = [
    dict(img=DEER, alt='A Sangai stag with tall brow antlers standing in grassland', kicker='Manipur’s State Animal', title='Protecting the Sangai and its floating home.', label='The Sangai'),
    dict(img=GROUP, alt='Students and teachers at Toubul Government High School holding a Sangai Day banner', kicker='Responsible Schools for Sangai', title='A new school, almost every month.', label='School programmes'),
    dict(img=CLASS, alt='A hall full of students in uniform at a sensitisation programme', kicker='Sangai Ambassadors', title='Young people carrying the message home.', label='Students'),
]
recent = [
    ('2 NOV 2026', 'Sangai Day at school', 'Children Model Academy, Thanga'),
    ('18 OCT 2026', '15 km Green Ride', 'To Keibul Lamjao'),
    ('17 OCT 2026', 'Sangai Day at school', 'Thanga Higher Secondary School'),
    ('29 SEP 2026', 'Sangai Day at school', 'Loktak Christian Model High School'),
    ('18 JUL 2026', 'Uningthou planting', 'Paradise Gardening School, Chandpur'),
    ('11 JUL 2026', 'Native tree drive', 'Thanga Chingjao Hillock, Loktak'),
]
recent_photos = {1: (CLASS, 'Students at a school programme', 'Students at one of our school programmes'),
                 3: (SPEAKER, 'A trustee speaking at a school programme', 'A talk on the Sangai’s history and ecology')}
quiz = [
    dict(q='How many Sangai did the 2026 census find in the wild?', a='172', more='Down from 260 in 2016. Every one lives in Keibul Lamjao.'),
    dict(q='What does the name “Sangai” mean?', a='The one that waits', more='From “sa” (animal) and “ngai” (awaiting): a running stag stops to look back.'),
    dict(q='How thick is the floating phumdi the Sangai walks on?', a='Up to 1.2 m', more='Only about a fifth of it sits above the water, enough to carry a deer.'),
    dict(q='When does the Sangai like to graze?', a='Dawn and dusk', more='Roughly 4:30 to 8 am and 3 to 6 pm, resting under tall reeds in between.'),
    dict(q='Which sport was born in Manipur as Sagol Kangjei?', a='Polo', more='Manipur is known as the birthplace of modern polo.'),
]
QUIZ_COLORS = ['#0F3D24', '#0B3A53', '#5B3412', '#1F2F5C', '#3D2A52']

hero_slides = ''
for i, s in enumerate(slides):
    hero_slides += f'''
        <div data-slide role="group" aria-roledescription="slide" aria-label="{i + 1} of {len(slides)}: {s['label']}"{' hidden' if i else ''} style="position: absolute; inset: 0">
          <img src="{s['img']}" alt="{s['alt']}" style="width: 100%; height: 100%; object-fit: cover; object-position: center 35%">
          <div class="hero-cap" style="position: absolute; inset: auto 0 0 0; padding: 120px 48px 40px; background: linear-gradient(to top, rgba(0,0,0,0.62), rgba(0,0,0,0))">
            <p style="margin: 0 0 8px; font-size: 15px; font-weight: 600; color: rgba(255,255,255,0.85)">{s['kicker']}</p>
            <p style="margin: 0; max-width: 18em; font-size: clamp(32px, 4.5vw, 52px); line-height: 1.08; font-weight: 700; letter-spacing: -0.025em; color: #FFFFFF">{s['title']}</p>
          </div>
        </div>'''
hero_dots = ''.join(f'''
          <button type="button" class="dot" data-go="{i}" aria-label="Show slide {i + 1}" aria-current="{'true' if i == 0 else 'false'}" style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 44px; border: 0; background: transparent; cursor: pointer; padding: 0"><span></span></button>''' for i in range(len(slides)))

recent_html = ''
for i, (d, t, p) in enumerate(recent):
    recent_html += f'''
          <li style="flex: 0 0 300px; scroll-snap-align: start; display: flex; flex-direction: column; justify-content: space-between; min-height: 260px; padding: 28px; border-radius: 24px; background: var(--card); box-shadow: var(--shadow)">
            <p style="margin: 0; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; color: var(--label3)">{d}</p>
            <div>
              <h3 style="margin: 0; font-size: 22px; line-height: 1.25; font-weight: 600; letter-spacing: -0.01em">{t}</h3>
              <p style="margin: 8px 0 0; font-size: 15px; color: var(--label3)">{p}</p>
            </div>
          </li>'''
    if i in recent_photos:
        img, alt, cap = recent_photos[i]
        recent_html += f'''
          <li style="flex: 0 0 300px; scroll-snap-align: start; min-height: 260px; border-radius: 24px; overflow: hidden; position: relative; box-shadow: var(--shadow)">
            <img src="{img}" alt="{alt}" loading="lazy" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover">
            <p style="position: absolute; left: 0; right: 0; bottom: 0; margin: 0; padding: 48px 24px 20px; font-size: 15px; font-weight: 600; color: #FFFFFF; background: linear-gradient(to top, rgba(0,0,0,0.6), rgba(0,0,0,0))">{cap}</p>
          </li>'''

quiz_html = ''
for i, q in enumerate(quiz):
    quiz_html += f'''
          <li class="card-wm" style="flex: 0 0 320px; scroll-snap-align: start; display: flex; flex-direction: column; gap: 20px; min-height: 340px; padding: 28px; border-radius: 24px; color: #FFFFFF; background: {QUIZ_COLORS[i % len(QUIZ_COLORS)]}">
            {wm("card")}
            <p style="margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.08em; opacity: 0.8">QUESTION {i + 1} OF {len(quiz)}</p>
            <p style="margin: 0; flex: 1; font-size: 24px; line-height: 1.25; font-weight: 600; letter-spacing: -0.01em">{q['q']}</p>
            <div class="answer" data-answer tabindex="-1" aria-live="polite" hidden>
              <p style="margin: 0; font-size: 44px; line-height: 1; font-weight: 700; letter-spacing: -0.03em">{q['a']}</p>
              <p style="margin: 10px 0 0; font-size: 15px; line-height: 1.45; opacity: 0.92">{q['more']}</p>
            </div>
            <button type="button" data-reveal style="align-self: flex-start; min-height: 44px; padding: 0 22px; border: 0; border-radius: 999px; background: rgba(255,255,255,0.92); color: #10251A; font-size: 15px; font-weight: 600; cursor: pointer">Reveal the answer</button>
          </li>'''

home_body = f'''    <section data-slideshow aria-roledescription="carousel" aria-label="Highlights" style="max-width: 1080px; margin: 0 auto; padding: 32px 24px 0">
      <div class="hero" style="position: relative; border-radius: 28px; overflow: hidden; background: #0B0F0B; height: 600px">{hero_slides}
        <div class="glassbar hero-ctrl" style="position: absolute; right: 24px; bottom: 32px; display: flex; align-items: center; gap: 4px; padding: 4px; border-radius: 999px; background: rgba(0,0,0,0.35)">
          <button type="button" data-prev aria-label="Previous slide" style="{GLASS_BTN}">{CHEV_L}</button>{hero_dots}
          <button type="button" data-next aria-label="Next slide" style="{GLASS_BTN}">{CHEV_R}</button>
        </div>
      </div>
    </section>

    <section style="max-width: 760px; margin: 0 auto; padding: 120px 24px 0; text-align: center">
      <div aria-hidden="true" style="display: flex; justify-content: center; margin-bottom: 32px">
        <img src="{DEER}" alt="" style="width: 72px; height: 72px; object-fit: cover; border-radius: 999px; border: 3px solid var(--bg)">
        <img src="{GROUP}" alt="" style="width: 72px; height: 72px; object-fit: cover; border-radius: 999px; border: 3px solid var(--bg); margin-left: -16px">
        <img src="{CLASS}" alt="" style="width: 72px; height: 72px; object-fit: cover; border-radius: 999px; border: 3px solid var(--bg); margin-left: -16px">
      </div>
      <h1 style="margin: 0; font-size: clamp(26px, 3vw, 34px); line-height: 1.3; font-weight: 600; letter-spacing: -0.018em">A non-profit trust in Manipur, building a people’s movement for the Sangai and Keibul Lamjao, the world’s only floating national park.</h1>
      <a href="about.html" style="display: inline-flex; align-items: center; gap: 6px; min-height: 44px; margin-top: 20px; font-size: 17px; font-weight: 500; text-decoration: none">Learn about us <span aria-hidden="true">›</span></a>
    </section>

    <section style="{SEC}">
      <a href="work.html" class="pad-card" style="display: flex; flex-wrap: wrap; align-items: center; gap: 24px 40px; padding: 40px; border-radius: 28px; background: var(--tint-fill); color: var(--label); text-decoration: none">
        <div aria-hidden="true" style="text-align: center; line-height: 1; color: var(--tint)">
          <p style="margin: 0; font-size: 72px; font-weight: 700; letter-spacing: -0.04em">10</p>
          <p style="margin: 6px 0 0; font-size: 15px; font-weight: 700; letter-spacing: 0.12em">DECEMBER</p>
        </div>
        <div style="flex: 1 1 360px; min-width: 0">
          <p style="margin: 0; font-size: 15px; font-weight: 600; color: var(--tint)">Coming up</p>
          <p style="margin: 4px 0 0; font-size: 28px; line-height: 1.2; font-weight: 700; letter-spacing: -0.02em">The 3rd Sangai Day</p>
          <p style="margin: 8px 0 0; color: var(--label2)">Every 10 December, recalling the 1954 resolution to protect the Sangai. This year’s quiz winners will be honoured.</p>
        </div>
        <img src="{GROUP}" alt="Students holding a Sangai Day banner" loading="lazy" style="flex: 0 1 280px; width: 280px; max-width: 100%; aspect-ratio: 3 / 2; object-fit: cover; border-radius: 18px">
      </a>
    </section>

    <section data-carousel aria-label="Recent work" class="has-wm" style="padding: 120px 0 0">
      {wm("right")}
{section_head('Recent work', '<a href="work.html" style="display: inline-flex; align-items: center; min-height: 44px; font-weight: 500; text-decoration: none">See all programmes ›</a>', 'programmes')}
      <div style="max-width: 1128px; margin: 0 auto">
        <ul data-track class="track" style="{TRACK}">{recent_html}
        </ul>
      </div>
    </section>

    <section data-carousel aria-label="Sangai quiz" class="has-wm" style="padding: 120px 0 0">
      {wm("left")}
{section_head('How well do you know the Sangai?', '<a href="discover.html" style="display: inline-flex; align-items: center; min-height: 44px; font-weight: 500; text-decoration: none">Discover more ›</a>', 'questions')}
      <div style="max-width: 1128px; margin: 0 auto">
        <ul data-track class="track" style="{TRACK}">{quiz_html}
        </ul>
      </div>
    </section>

    <section class="has-wm" style="{SEC}; padding-bottom: 120px; text-align: center">
      {wm("center")}
      <h2 style="{H2}">Stand with the Sangai</h2>
      <p style="margin: 12px auto 28px; max-width: 30em; color: var(--label2)">Host a programme at your school, partner with us, or support our work.</p>
      <a href="contact.html" style="{CTA}">Get in touch</a>
    </section>'''

# ---------------------------------------------------------------- WORK
ev2026 = [
    ('2 Nov', 'Sangai Day at school', 'Children Model Academy, Thanga', '51 participants; 8 quiz winners.'),
    ('18 Oct', '15 km Green Ride', 'To Keibul Lamjao National Park', 'Students and trustees cycled to the Sangai’s home.'),
    ('17 Oct', 'Sangai Day at school', 'Thanga Higher Secondary School', '53 participants; 15 teachers joined.'),
    ('12 Oct', 'Sangai Day at school', 'Little Birds School, Moirang', '51 participants, shared as part of our media initiative.'),
    ('29 Sep', 'Sangai Day at school', 'Loktak Christian Model High School, Moirang Lamkhai', '127 participants; 28 quiz winners.'),
    ('26 Sep', 'Sangai Day at school', 'L. Dhananjoy Memorial English School, Tronglaobi', 'A song on the Sangai and an Uningthou planting.'),
    ('8 Aug', 'Sangai Day at school', 'Bethel School, Nambol Chingmang', '50 participants.'),
    ('18 Jul', 'Uningthou planting', 'Paradise Gardening School, Chandpur', '87 participants and planting of the State Tree.'),
    ('11 Jul', 'Native tree drive', 'Thanga Chingjao Hillock, Loktak', 'With Loktak Folklore Museum, restoring the hillock’s forest.'),
    ('25 Jun', 'Sangai Day at school', 'Padma Ratna English School, Kakching', '112 participants; 28 quiz winners.'),
    ('14 Jun', 'World Environment Day', 'Hanubi Hillock, Moirang', 'Around 80 young people planted 250 native saplings.'),
    ('9 Jan', 'Sangai Day at school', 'Special Regular English School, Nambol', '70 participants; 17 quiz winners.'),
]
ev2025 = [
    ('10 Dec 2025', '2nd Sangai Day', 'Phouoibee Community Hall, Keibul Lamjao', '152 quiz winners from 11 schools honoured; 1,054 students reached in 2025.'),
    ('18 Nov 2025', 'School programme', 'Advanced Intermediate College, Moirang', '53 students and 12 teachers.'),
    ('9 Nov 2025', 'Yarou Sangai 2025', 'Bishnupur Higher Secondary School', 'A district painting competition: 93 students took part.'),
    ('27 Oct 2025', 'Sangaigi Numit', 'Toubul Government High School', 'A spot quiz with 47 students.'),
    ('15 Sep 2025', 'Sangai Day at school', 'Sanatombi Oriental English School, Kumbi', '14 books donated; 203 took the quiz.'),
    ('16 Aug 2025', 'Sangai Day at school', 'Loyalam Public School, Moirangkhunou', 'Closed with a cultural performance on the Sangai.'),
    ('12 Jul 2025', 'Sangai Day at school', 'Diligent Public School, Moirang', '159 students, 14 teachers and 5 parents.'),
    ('7 Jun 2025', 'Sangai Day at school', 'Ideal School, Thanga', '85 participants; 70 students took the quiz.'),
    ('10 May 2025', 'Sangai Day at school', 'Phoubakchao High School, Imphal West', '16 books donated; winners got free zoo entry.'),
    ('19 Apr 2025', 'Let’s Know Our Sangai', 'Chingmei High School, Chandpur', '12 books donated; 71 students took the quiz.'),
    ('8 Mar 2025', 'School programme', 'Sekmaijin High School, Imphal West', 'With the Chief Conservator of Forests (Wildlife).'),
    ('22 Feb 2025', 'Sangai Day at school', 'Sambanlei Sekpil School, Kumbi', '145 students, 7 teachers and 12 parents.'),
    ('28 Jan 2025', 'First Responsible School', 'New Model Public School, Moirang', 'Our first adopted school.'),
    ('10 Dec 2024', '1st Sangai Day', 'Manipur Zoological Garden', 'The launch of our year-long school programme.'),
    ('24 Nov 2024', 'Consultation on Sangai Conservation', 'Dr Shamungou’s home, Nambol Makha Leikai', 'Where Sangai Day and the Foundation were born.'),
]
years = [('2026', ev2026), ('2024–25', ev2025)]

# Programme details from the 2024–25 brochure (reference/brochure-2024-25.pdf), keyed by card date.
# counts: attendance tiles; points: what happened; who: key attendees.
EV_DETAILS = {
    '24 Nov 2024': dict(
        counts=[],
        points=['Earlier observances such as World Wetlands Day had stayed at the level of words, not sustained action.',
                'Proposal to mark “Sangai Day” every 10 December, recalling the 1954 resolution to create a sanctuary for the Sangai.',
                'Agreement that school students must be at the heart of any long-term conservation effort.',
                'Decision to start a trust, later registered as Sangai First Foundation, to run year-long programmes.'],
        who=['Dr Kh. Shamungou', 'Wildlife enthusiasts, teachers and conservation workers']),
    '10 Dec 2024': dict(
        counts=[('27', 'students'), ('27', 'volunteers'), ('6', 'zoo staff'), ('6', 'trustees')],
        points=['The historical significance of 10 December 1954 and the Sangai’s conservation journey.',
                'Sangai Day as a public platform to protect rare species and revive ecological values.',
                'A call for a year-long School Students’ Programme and “Responsible Schools for Sangai”.',
                'A public appeal for collective action and support.'],
        who=['Dr Kh. Shamungou, Chairman, Technical Committee, Manipur State Board for Wildlife',
             'L. Biramangol, MFS, Director, Manipur Zoological Garden', 'Gyanic Thangjam, RFO', 'Dr L. Sharatchandra',
             'Trustees and members of the Foundation']),
    '28 Jan 2025': dict(
        counts=[('66', 'students'), ('8', 'teachers')],
        points=['Launch of the year-long School Students’ Sensitisation Programme.',
                'What Sangai Day is, why the Sangai is unique, and the fragile habitat of Keibul Lamjao.',
                'Students invited to become Sangai Ambassadors and take a conservation pledge.',
                'Top students selected; the next adopted school to be announced soon.'],
        who=['Dr Kh. Yaimchou', 'Dr Kh. Shamungou, Managing Trustee', 'K. Jugeshor', 'Kh. Budha', 'Kh. Ajitkumar']),
    '22 Feb 2025': dict(
        counts=[('145', 'students'), ('7', 'teachers'), ('12', 'parents')],
        points=['The historical, ecological, socio-cultural and biological importance of the Sangai.',
                'The role of students as guardians of the environment and wildlife.',
                'A written spot quiz: 145 students took part, many winning prizes to be given on Sangai Day.',
                'Students encouraged to take the Sangai’s message beyond school into the community.'],
        who=['Dr Kh. Shamungou', 'K. Jugeshor', 'M. Mangi, National Teacher’s Awardee', 'Kh. Budha', 'T. Budhi',
             'A. Ajitkumar', 'S. Brajakumar']),
    '8 Mar 2025': dict(
        counts=[('63', 'students'), ('10', 'teachers')],
        points=['The Foundation’s mission, and the need for youth-led conservation of Manipur’s State Animal.',
                'Manipur Zoological Garden as a second home for the Sangai, and its captive breeding.',
                'The links between the Sangai, local communities and the Loktak wetland.',
                'A spot quiz with 82 participants; winners to be honoured on Sangai Day.'],
        who=['L. Joykumar, Chief Conservator of Forests (Wildlife)', 'L. Biramangol, MFS, Director, Manipur Zoological Garden',
             'Dr Kh. Shamungou', 'K. Jugeshor', 'Kh. Budha', 'Kh. Ajitkumar',
             'Principal, teachers and Youth and Eco Club volunteers']),
    '19 Apr 2025': dict(
        counts=[('74', 'students'), ('12', 'teachers')],
        points=['Why Keibul Lamjao, the world’s only floating national park, matters.',
                'The Sangai’s ecology and behaviour, and its dependence on the phumdi.',
                '12 wildlife and ecology books by Dr Shamungou donated to the school library.',
                'A pledge for the Sangai, wetlands and the wider environment; eleven teachers supported the programme.'],
        who=['L. Biramangol', 'Dr Kh. Shamungou', 'K. Jugeshor', 'N. Binoy, National Teacher’s Awardee and Headmaster',
             'Kh. Budha', 'Kh. Ajitkumar', 'S. Brajakumar']),
    '10 May 2025': dict(
        counts=[('95', 'students'), ('13', 'teachers')],
        points=['The critical need to protect the wetlands and grasslands that support the Sangai.',
                'Field experiences shared from Keibul Lamjao and Loktak Lake.',
                'Sangai literature and handouts given to the school library.',
                'A spot quiz on the Sangai and wildlife; winners recognised on Sangai Day.'],
        who=['L. Joykumar, Chief Conservator of Forests (Wildlife)', 'L. Biramangol', 'Dr Kh. Shamungou', 'K. Jugeshor',
             'Md. Samad, Headmaster and State Teacher Awardee', 'Kh. Budha', 'Kh. Ajitkumar']),
    '7 Jun 2025': dict(
        counts=[('65', 'students'), ('7', 'teachers'), ('5', 'parents')],
        points=['A talk by student Ningthoujam Lanchenbi on her own community conservation work.',
                'A spot quiz on the Sangai and wildlife.',
                'Books by Dr Shamungou donated to the Ideal School library.'],
        who=['Dr Kh. Shamungou', 'K. Jugeshor',
             'S. Brajakumar, Vice-President, Environmental Social Reformation and Sangai Protection Forum',
             'T. Brojen, Principal', 'Kh. Budha', 'Kh. Ajitkumar']),
    '12 Jul 2025': dict(
        counts=[('159', 'students'), ('14', 'teachers'), ('5', 'parents')],
        points=['The aims of the year-long programme and building conservation values in young minds.',
                'A talk on the history and status of the Sangai, Keibul Lamjao and Manipur’s biodiversity.',
                'Books and information on the Sangai given to students.',
                'A student’s speech, “Malemda Houjik Oiriba Sangai gi Thajaba”, on youth responsibility.',
                'A written spot quiz; winners to be awarded on the 2nd Sangai Day.'],
        who=['Dr K. Bijya, Principal', 'Dr Kh. Shamungou', 'K. Jugeshor', 'E. Premjit', 'S. Brajakumar', 'Kh. Budha',
             'Telheiba Kumam']),
    '16 Aug 2025': dict(
        counts=[('68', 'students'), ('23', 'teachers'), ('4', 'parents')],
        points=['An introduction to Sangai conservation and what makes Keibul Lamjao unique.',
                'A detailed talk asking students to see themselves as custodians of biodiversity.',
                'Moirangkhunou’s closeness to the Sangai Ethnic Park, and the need for local leadership.',
                'An indigenous cultural performance on the Sangai.'],
        who=['Dr Kh. Shamungou', 'K. Jugeshor', 'P. Robin, Principal', 'Oinam Basanta, Assistant Teacher',
             'S. Brajakumar', 'Kh. Ajitkumar', 'Kh. Budha', 'Telheiba Kumam']),
    '15 Sep 2025': dict(
        counts=[('203', 'students'), ('12', 'teachers')],
        points=['The school named a “Responsible School for Sangai”.',
                'The threats facing Keibul Lamjao, above all habitat loss.',
                'An in-depth talk by Dr Shamungou on the Sangai’s history, ecology, behaviour and biology.',
                'Books and learning materials donated, and a pledge ceremony.'],
        who=['Dr Kh. Shamungou', 'K. Jugeshor', 'N. Santakumar, National Youth Awardee', 'Kh. Budha', 'E. Premjit',
             'T. Budhi', 'Telheiba Kumam']),
    '27 Oct 2025': dict(
        counts=[('47', 'students in the quiz')],
        points=['Why Keibul Lamjao, the world’s only floating national park, matters.',
                'A spot quiz with 47 students.',
                'The district-level competition “Yarou Sangai 2025” announced as a curtain-raiser to the 2nd Sangai Day.'],
        who=['Kh. Nishikanta, Headmaster', 'Dr Kh. Shamungou', 'Th. Rachandra, retired Headmaster', 'Th. Jhalajit',
             'E. Premjit', 'Kh. Budha', 'Telheiba Kumam']),
    '9 Nov 2025': dict(
        counts=[('113', 'registered'), ('93', 'took part')],
        points=['A district-level competition for the title “Yarou Sangai 2025”.',
                'Students from schools across Bishnupur District took part.'],
        who=['Dr Kh. Shamungou', 'L. Biramangol', 'Kh. Budha', 'Kh. Ajitkumar', 'E. Premjit', 'S. Brajakumar',
             'Telheiba Kumam']),
    '18 Nov 2025': dict(
        counts=[('53', 'students'), ('12', 'teachers')],
        points=['K. Jugeshor, Vice-President of the Foundation, spoke on the Sangai’s current status.',
                'Principal Y. Modhu thanked the Foundation for the programme.'],
        who=['Dr Kh. Shamungou', 'K. Jugeshor', 'Y. Modhu, Principal', 'S. Brajakumar', 'Kh. Budha', 'Kh. Ajitkumar']),
}


def ev_id(date):
    return 'ev-' + date.lower().replace(' ', '-')


def ev_dialogs(evs):
    out = ''
    for d, t, p, n in evs:
        det = EV_DETAILS.get(d)
        if not det:
            continue
        counts = ''.join(f'<div class="dlg-stat"><p class="dlg-n">{c}</p><p class="dlg-l">{l}</p></div>' for c, l in det['counts'])
        counts = f'<div class="dlg-stats">{counts}</div>' if counts else ''
        points = ''.join(f'<li>{x}</li>' for x in det['points'])
        who = ''.join(f'<li>{x}</li>' for x in det['who'])
        out += f'''
    <dialog class="dlg" id="{ev_id(d)}" aria-labelledby="{ev_id(d)}-t">
      <div class="dlg-body">
        <form method="dialog"><button class="dlg-close" aria-label="Close"><svg aria-hidden="true" width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M2 2l10 10M12 2L2 12"></path></svg></button></form>
        <p class="dlg-date">{d}</p>
        <h2 class="dlg-title" id="{ev_id(d)}-t">{t}</h2>
        <p class="dlg-place">{p}</p>
        {counts}
        <h3 class="dlg-h">What happened</h3>
        <ul class="dlg-points">{points}</ul>
        <h3 class="dlg-h">Who was there</h3>
        <ul class="dlg-who">{who}</ul>
        <p class="dlg-src">From our 2024–25 programme brochure.</p>
      </div>
    </dialog>'''
    return out


def more_btn(d):
    if d not in EV_DETAILS:
        return ''
    return f'\n            <button type="button" class="ev-more" data-open="{ev_id(d)}" aria-haspopup="dialog">Details <span aria-hidden="true">›</span></button>'


def event_cards(evs):
    return ''.join(f'''
          <li style="flex: 0 0 340px; scroll-snap-align: start; display: flex; flex-direction: column; gap: 16px; min-height: 300px; padding: 28px; border-radius: 24px; background: var(--card); box-shadow: var(--shadow)">
            <p style="margin: 0; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; color: var(--tint)">{d}</p>
            <div style="flex: 1">
              <h2 style="margin: 0; font-size: 22px; line-height: 1.25; font-weight: 600; letter-spacing: -0.01em">{t}</h2>
              <p style="margin: 6px 0 0; font-size: 15px; color: var(--label3)">{p}</p>
            </div>
            <p style="margin: 0; font-size: 15px; line-height: 1.45; color: var(--label2)">{n}</p>{more_btn(d)}
          </li>''' for d, t, p, n in evs)


year_btns = ''.join(f'''
          <button type="button" class="seg" data-year="{k}" aria-pressed="{'true' if i == 0 else 'false'}">{k}</button>''' for i, (k, _) in enumerate(years))
year_panels = ''.join(f'''
        <ul data-track data-panel="{k}" aria-label="Programmes in {k}" class="track" style="{TRACK}"{' hidden' if i else ''}>{event_cards(evs)}
        </ul>''' for i, (k, evs) in enumerate(years))

work_body = f'''    <section style="max-width: 1080px; margin: 0 auto; padding: 96px 24px 0">
      <h1 style="margin: 0; font-size: clamp(40px, 5vw, 56px); line-height: 1.05; font-weight: 700; letter-spacing: -0.028em">Our work</h1>
      <p style="margin: 16px 0 0; max-width: 34em; font-size: 20px; color: var(--label2)">Talks, quizzes, books and a pledge, in a different school almost every month.</p>
      <div class="split" style="display: grid; grid-template-columns: 2fr 1fr; gap: 16px; margin-top: 48px">
        <img src="{CLASS}" alt="A hall full of students at a sensitisation programme" style="width: 100%; height: 360px; object-fit: cover; border-radius: 28px">
        <img src="{SPEAKER}" alt="A trustee speaking at a school programme" style="width: 100%; height: 360px; object-fit: cover; border-radius: 28px">
      </div>
    </section>

    <section data-carousel aria-label="Programmes" class="has-wm" style="padding: 64px 0 0">
      {wm("right")}
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px 24px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px">
        <div role="group" aria-label="Year" data-years style="display: inline-flex; padding: 3px; border-radius: 999px; background: var(--card2)">{year_btns}
        </div>
        {arrows('programmes')}
      </div>
      <div style="max-width: 1128px; margin: 0 auto">{year_panels}
      </div>
    </section>
{ev_dialogs(ev2025)}

    <section style="{SEC}">
      <figure style="margin: 0">
        <img src="{GROUP}" alt="Students and teachers at Toubul Government High School holding a Sangai Day banner" loading="lazy" style="display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 28px">
        <figcaption style="margin-top: 12px; font-size: 13px; color: var(--label3)">Sangaigi Numit at Toubul Government High School, 27 October 2025.</figcaption>
      </figure>
    </section>

    <section style="{SEC}; padding-bottom: 120px">
      <h2 style="{H2}; margin-bottom: 24px">News</h2>
      <ul style="list-style: none; margin: 0; padding: 0 28px; background: var(--card); border-radius: 24px">
        <li style="padding: 22px 0; border-bottom: 1px solid var(--sep)"><p style="margin: 0; font-size: 13px; color: var(--label3)">5 June 2026</p><p style="margin: 2px 0 0; font-weight: 600">Dr Khangembam Shamungou receives the Lifetime Achievement in Environment Award</p></li>
        <li style="padding: 22px 0; border-bottom: 1px solid var(--sep)"><p style="margin: 0; font-size: 13px; color: var(--label3)">5 June 2026</p><p style="margin: 2px 0 0; font-weight: 600">Kumam Jugeshor receives the Ningombam Pheiraba Award 2026</p></li>
        <li style="padding: 22px 0"><p style="margin: 0; font-size: 13px; color: var(--label3)">23 May 2026</p><p style="margin: 2px 0 0; font-weight: 600">Dr Shamungou’s 23rd book, “Ningsingli Ngasisu”, is released</p></li>
      </ul>
    </section>'''

# ---------------------------------------------------------------- ABOUT
trustees = [  # order as in the trust deed
    ('Dr Khangembam Shamungou', 'President · Managing Trustee', 'Founder. Author of 23 books on nature and the Sangai.'),
    ('Kumam Jugeshor', 'Vice-President', 'Founder. Ornithologist and retired Principal of Kumbi College.'),
    ('Tongbram Budhi', 'Trustee', ''),
    ('Elangbam Premjit', 'Trustee', ''),
    ('Khwairakpam Budha', 'Trustee', 'Founder.'),
    ('Khangembam Ajitkumar', 'Trustee', ''),
    ('Salam Brajakumar', 'Trustee', ''),
    ('Salam Prasanta', 'Trustee', 'Founder.'),
    ('Telheiba Kumam', 'Trustee', ''),
]
story = [
    ('1954', 'A sanctuary is born', 'On 10 December, the Manipur Board for Wildlife, chaired by V.S. Sundram, resolved to create a 50 km² sanctuary for the Sangai.'),
    ('24 Nov 2024', 'Four friends, two decisions', 'At Dr Shamungou’s home in Nambol Makha Leikai, the founders declared 10 December “Sangai Day” and founded Sangai First Foundation.'),
    ('10 Dec 2024', 'The first Sangai Day', 'Held at Manipur Zoological Garden, Iroisemba, with the Forest Department’s Wildlife Wing. A year-long school campaign begins.'),
    ('27 Feb 2025', 'Going online', 'Our Facebook page launches. By November 2026 it has 107 posts this year and 4.5K views.'),
    ('10 Dec 2025', '2nd Sangai Day', 'At Phouoibee Community Hall, Keibul Lamjao. 152 quiz winners and the top five of Yarou Sangai 2025 are honoured.'),
    ('2026', 'Roots and wheels', 'Nine more schools, a Save Sangai Campaign Block in Kakching, native tree drives and a 15 km Green Ride.'),
    ('10 Dec 2026', 'Sangai Heritage Hub', 'On the 3rd Sangai Day, we plan to open a permanent centre for conservation education at Keibul Ching.'),
]
STORY_COLORS = ['#5B3412', '#0F3D24', '#1F6B3A', '#0B3A53', '#1F2F5C', '#3D2A52', '#008932']
stats = [('1,054', 'students reached across 11 schools in 2025'), ('586', 'students reached across 9 schools in 2026'), ('269', 'quiz winners recognised in 2025 and 2026'), ('268', 'people joined our 2026 planting drives')]


# Trustee portraits (add more as the Foundation sends them); others show initials.
# Background removed and cropped to head and shoulders (originals: iCloud "Sangai First/Passport").
TRUSTEE_PHOTOS = {
    'Dr Khangembam Shamungou': IMG + 'trustee-shamungou.png',
    'Kumam Jugeshor': IMG + 'trustee-jugeshor.png',
    'Tongbram Budhi': IMG + 'trustee-budhi.png',
    'Elangbam Premjit': IMG + 'trustee-premjit.png',
    'Khwairakpam Budha': IMG + 'trustee-budha.png',
    'Khangembam Ajitkumar': IMG + 'trustee-ajitkumar.png',
    'Salam Brajakumar': IMG + 'trustee-brajakumar.png',
    'Salam Prasanta': IMG + 'trustee-prasanta.png',
    'Telheiba Kumam': IMG + 'trustee-telheiba.png',
}


def avatar(name):
    style = 'flex: none; display: inline-flex; align-items: center; justify-content: center; width: 72px; height: 72px; border-radius: 999px'
    if name in TRUSTEE_PHOTOS:
        return f'<img src="{TRUSTEE_PHOTOS[name]}" alt="" loading="lazy" style="{style}; object-fit: cover; background: var(--tint-fill)">'
    return f'<span aria-hidden="true" style="{style}; background: var(--tint-fill); color: var(--tint); font-weight: 700; font-size: 18px">{initials(name)}</span>'


def initials(name):
    p = name.replace('Dr ', '').split(' ')
    return p[0][0] + p[-1][0]


stat_html = ''.join(f'''
        <div style="padding: 28px; border-radius: 24px; background: var(--card)">
          <p style="margin: 0; font-size: 48px; line-height: 1; font-weight: 700; letter-spacing: -0.035em; color: var(--tint)">{n}</p>
          <p style="margin: 10px 0 0; font-size: 15px; color: var(--label2)">{t}</p>
        </div>''' for n, t in stats)
story_html = ''.join(f'''
          <li class="card-wm" style="flex: 0 0 300px; scroll-snap-align: start; display: flex; flex-direction: column; gap: 12px; min-height: 360px; padding: 28px; border-radius: 24px; color: #FFFFFF; background: {STORY_COLORS[i % len(STORY_COLORS)]}">
            {wm("card")}
            <p style="margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.08em; opacity: 0.8">CHAPTER {i + 1}</p>
            <p style="margin: 0; font-size: 40px; line-height: 1.02; font-weight: 700; letter-spacing: -0.03em">{w}</p>
            <div style="flex: 1"></div>
            <h3 style="margin: 0; font-size: 21px; line-height: 1.25; font-weight: 600">{t}</h3>
            <p style="margin: 0; font-size: 15px; line-height: 1.45; opacity: 0.92">{x}</p>
          </li>''' for i, (w, t, x) in enumerate(story))
trustee_html = ''.join(f'''
          <li style="flex: 0 0 260px; scroll-snap-align: start; min-height: 200px; padding: 28px; border-radius: 24px; background: var(--card); box-shadow: var(--shadow); display: flex; flex-direction: column; gap: 12px">
            {avatar(n)}
            <div>
              <h3 style="margin: 0; font-size: 19px; line-height: 1.3; font-weight: 600">{n}</h3>
              <p style="margin: 2px 0 0; font-size: 15px; color: var(--tint); font-weight: 500">{r}</p>
              {f'<p style="margin: 8px 0 0; font-size: 15px; color: var(--label3)">{note}</p>' if note else ''}
            </div>
          </li>''' for n, r, note in trustees)

TORN = 'polygon(0.0% 0.5%, 3.6% 0.2%, 7.1% 1.0%, 10.7% 0.1%, 14.3% 0.9%, 17.9% 0.6%, 21.4% 0.1%, 25.0% 0.8%, 28.6% 0.1%, 32.1% 0.7%, 35.7% 0.1%, 39.3% 0.1%, 42.9% 0.7%, 46.4% 1.3%, 50.0% 0.2%, 53.6% 0.4%, 57.1% 1.0%, 60.7% 1.5%, 64.3% 0.9%, 67.9% 0.6%, 71.4% 1.6%, 75.0% 0.1%, 78.6% 1.4%, 82.1% 0.5%, 85.7% 0.2%, 89.3% 0.2%, 92.9% 0.5%, 96.4% 1.3%, 100.0% 0.3%, 99.5% 12.5%, 99.4% 25.0%, 99.7% 37.5%, 99.5% 50.0%, 99.9% 62.5%, 99.9% 75.0%, 99.8% 87.5%, 100.0% 98.9%, 96.4% 99.3%, 92.9% 99.5%, 89.3% 99.1%, 85.7% 99.3%, 82.1% 99.5%, 78.6% 98.7%, 75.0% 98.9%, 71.4% 99.6%, 67.9% 99.1%, 64.3% 99.2%, 60.7% 98.6%, 57.1% 98.8%, 53.6% 99.5%, 50.0% 98.4%, 46.4% 99.8%, 42.9% 99.3%, 39.3% 98.8%, 35.7% 99.8%, 32.1% 99.2%, 28.6% 99.9%, 25.0% 98.9%, 21.4% 98.8%, 17.9% 99.1%, 14.3% 98.6%, 10.7% 99.5%, 7.1% 98.9%, 3.6% 99.0%, 0.0% 99.1%, 0.4% 87.5%, 0.8% 75.0%, 0.9% 62.5%, 0.4% 50.0%, 0.6% 37.5%, 0.1% 25.0%, 0.6% 12.5%)'

about_body = f'''    <section style="max-width: 1080px; margin: 0 auto; padding: 96px 24px 0; display: flex; flex-wrap: wrap; align-items: center; gap: 72px 56px">
      <div style="flex: 1 1 380px; min-width: 0">
        <p style="margin: 0 0 12px; font-size: 15px; font-weight: 600; color: var(--tint)">Our story</p>
        <h1 style="margin: 0; font-size: clamp(40px, 5vw, 60px); line-height: 1.03; font-weight: 700; letter-spacing: -0.032em">It began with four friends and one idea.</h1>
        <p style="margin: 24px 0 0; font-size: 19px; line-height: 1.55; color: var(--label2)">On 24 November 2024, four environmentalists met at a home in Nambol Makha Leikai. They left with a plan: give the Sangai a day of its own, and a trust to protect it.</p>
        <p style="margin: 20px 0 0; font-size: 15px; color: var(--label3)">Dr Khangembam Shamungou · Kumam Jugeshor · Salam Prasanta · Khwairakpam Budha</p>
      </div>
      <figure style="flex: 1 1 460px; min-width: 0; margin: 0; padding: 24px 0 48px; perspective: 1400px">
        <div class="clip" style="position: relative; height: 560px; transform: rotate(-2.2deg) rotateY(-8deg); filter: drop-shadow(0 30px 40px rgba(0,0,0,0.28)) drop-shadow(0 4px 6px rgba(0,0,0,0.18))">
          <div style="position: absolute; inset: 0; clip-path: {TORN}; background-color: #EFE7D4; background-image: radial-gradient(rgba(40,32,20,0.07) 1px, transparent 1.3px); background-size: 5px 5px; color: #1C1A16; font-family: Georgia, &quot;Times New Roman&quot;, serif; padding: 26px 30px">
            <div style="display: flex; justify-content: space-between; gap: 12px; padding-bottom: 6px; border-bottom: 3px double #1C1A16; font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase">
              <span>Sangai First Foundation</span><span>Nambol · 24 Nov 2024</span>
            </div>
            <p style="margin: 14px 0 0; font-family: &quot;Playfair Display&quot;, Georgia, serif; font-size: 30px; line-height: 1.05; font-weight: 900; letter-spacing: -0.01em">Four friends resolve to give the Sangai its own day</p>
            <p class="clip-text" style="margin: 10px 0 0; padding-top: 8px; border-top: 1px solid rgba(28,26,22,0.6); font-size: 13px; line-height: 1.45; font-style: italic; columns: 2; column-gap: 20px; column-rule: 1px solid rgba(28,26,22,0.35)">Meeting at a home in Nambol Makha Leikai, the four agreed to mark every 10 December as Sangai Day, recalling the 1954 resolution that created the Sangai sanctuary, and to found a trust to carry the work into schools.</p>
          </div>
          <img src="{NEWSPRINT}" alt="Halftone newspaper-style cutout of the four founders standing together: Dr Khangembam Shamungou, Kumam Jugeshor, Salam Prasanta and Khwairakpam Budha" style="position: absolute; left: -5%; bottom: -36px; width: 110%; max-width: none; height: auto; transform: translateZ(50px) rotate(1.2deg); filter: drop-shadow(0 10px 14px rgba(0,0,0,0.35))">
        </div>
      </figure>
    </section>

    <section style="max-width: 820px; margin: 0 auto; padding: 120px 24px 0; text-align: center">
      <p style="margin: 0 0 16px; font-size: 15px; font-weight: 600; color: var(--tint)">The genesis of Sangai Day</p>
      <p style="margin: 0; font-size: clamp(26px, 3vw, 36px); line-height: 1.25; font-weight: 600; letter-spacing: -0.02em">After years of informal talks about the declining ecology of Loktak Lake and Keibul Lamjao, the founders made two decisions: mark every 10 December as Sangai Day, recalling the 1954 resolution that created the Sangai sanctuary, and start a trust to carry the work forward.</p>
    </section>

    <section data-carousel aria-label="Our story so far" class="has-wm" style="padding: 96px 0 0">
      {wm("right")}
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px 24px; display: flex; align-items: flex-end; justify-content: space-between; gap: 16px">
        <h2 style="{H2}">The story so far</h2>
        {arrows('milestones')}
      </div>
      <div style="max-width: 1128px; margin: 0 auto">
        <ol data-track class="track" style="{TRACK}">{story_html}
        </ol>
      </div>
    </section>

    <section style="{SEC}">
      <h2 style="{H2}; margin-bottom: 24px">Two years in numbers</h2>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px">{stat_html}
      </div>
    </section>

    <section style="{SEC}">
      <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 48px">
        <img src="{STAG}" alt="A Sangai stag with brow antlers standing in tall green grass, looking at the camera" loading="lazy" style="flex: 1 1 420px; min-width: 0; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; object-position: center 15%; border-radius: 28px">
        <div style="flex: 1 1 300px; min-width: 0">
          <h2 style="{H2}">Why the Sangai</h2>
          <p style="margin: 16px 0 0; color: var(--label2)">The brow-antlered deer is Manipur’s State Animal. In the wild it lives only in Keibul Lamjao, on the floating meadows of Loktak Lake.</p>
          <p style="margin: 12px 0 0; color: var(--label2)">Habitat loss, the Ithai Barrage and a small population put it at risk. That’s why we work with the next generation.</p>
          <a href="discover.html" style="display: inline-flex; align-items: center; min-height: 44px; margin-top: 8px; font-weight: 500; text-decoration: none">Discover the Sangai ›</a>
        </div>
      </div>
    </section>

    <section data-carousel aria-label="Trustees" class="has-wm" style="padding: 120px 0 0">
      {wm("left")}
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px 24px; display: flex; align-items: flex-end; justify-content: space-between; gap: 16px">
        <h2 style="{H2}">Our trustees</h2>
        {arrows('trustees')}
      </div>
      <div style="max-width: 1128px; margin: 0 auto">
        <ul data-track class="track" style="{TRACK}">{trustee_html}
        </ul>
      </div>
    </section>

    <section style="{SEC}; padding-bottom: 120px">
      <div class="pad-card" style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center; padding: 40px; border-radius: 28px; background: var(--card)">
        <img src="{SPEAKER}" alt="A trustee speaking to students" loading="lazy" style="flex: 0 0 200px; width: 200px; height: 200px; object-fit: cover; border-radius: 999px">
        <div style="flex: 1 1 300px; min-width: 0">
          <h2 style="{H2}">Read about the Sangai</h2>
          <p style="margin: 12px 0 0; color: var(--label2)">We give Dr Shamungou’s books to every school we visit, among them “Sangai” (1993), “Endangered Manipur Brow-antlered Deer” (2010) and “Loktak Eidi Wareda” (2009).</p>
        </div>
      </div>
    </section>'''

# ---------------------------------------------------------------- CONTACT
contact_body = f'''    <section class="has-wm" style="max-width: 720px; margin: 0 auto; padding: 96px 24px 120px">
      {wm("right")}
      <h1 style="margin: 0; font-size: clamp(40px, 5vw, 56px); line-height: 1.05; font-weight: 700; letter-spacing: -0.028em">Stand with the Sangai</h1>
      <p style="margin: 16px 0 40px; font-size: 20px; color: var(--label2)">To donate, host a programme at your school, or partner with us, write or call. We only use your details to reply.</p>
      <ul style="list-style: none; margin: 0; padding: 0 28px; background: var(--card); border-radius: 24px; box-shadow: var(--shadow)">
        <li style="padding: 20px 0; border-bottom: 1px solid var(--sep)"><p style="margin: 0; font-size: 13px; color: var(--label3)">Email</p><a href="mailto:sangaiff2024@gmail.com" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 19px; font-weight: 500; overflow-wrap: anywhere">sangaiff2024@gmail.com</a></li>
        <li style="padding: 20px 0; border-bottom: 1px solid var(--sep)"><p style="margin: 0; font-size: 13px; color: var(--label3)">Phone</p><a href="tel:+919856177030" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 19px; font-weight: 500; margin-right: 20px">+91 98561 77030</a><a href="tel:+918014366698" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 19px; font-weight: 500">+91 80143 66698</a></li>
        <li style="padding: 20px 0"><p style="margin: 0; font-size: 13px; color: var(--label3)">Address</p><p style="margin: 6px 0 0; font-size: 17px">Nambol Makha Leikai, Nambol Sub-Division<br>Bishnupur District 795134, Manipur, India</p></li>
      </ul>
      <a href="mailto:sangaiff2024@gmail.com" style="{CTA}; margin-top: 32px">Email us</a>
    </section>'''

# ---------------------------------------------------------------- DISCOVER
WIKI_S = 'https://en.wikipedia.org/wiki/Sangai'
WIKI_K = 'https://en.wikipedia.org/wiki/Keibul_Lamjao_National_Park'
WIKI_L = 'https://en.wikipedia.org/wiki/Loktak_Lake'
WIKI_M = 'https://en.wikipedia.org/wiki/Manipur'
MT = 'https://manipurtourism.gov.in/about-us/'
dslides = [
    dict(label='The Sangai', bg='#0F3D24', img=DEER, pos='40% 35%', alt='A Sangai stag with tall brow antlers in grassland',
         kicker='The dancing deer', title='Found nowhere else on Earth.',
         text='The Sangai is Manipur’s State Animal, a subspecies of Eld’s deer that lives in the wild only in Keibul Lamjao. Its name joins “sa” (animal) and “ngai” (awaiting): a running stag stops to look back.',
         chips=['Endangered · IUCN', 'Schedule I · India', 'Antlers 100–110 cm'], src='Wikipedia · WWF-India', url=WIKI_S),
    dict(label='Phumdi', bg='#0B3A53', img=PHUMDI, pos='center 72%', alt='Aerial view of Loktak Lake dotted with round, floating phumdi',
         kicker='Loktak Lake', title='Islands that float.',
         text='Loktak, the largest freshwater lake in Northeast India, is dotted with phumdi: floating mats of plants, soil and organic matter. About a fifth of each mat rises above the water, strong enough to carry a deer.',
         chips=['~287 km² lake', 'Phumdi up to 1.2 m thick', 'Ramsar site since 1990'], src='Wikipedia', url=WIKI_L),
    dict(label='Keibul Lamjao', bg='#3E4A1E', img=KEIBUL, pos='center 50%', alt='Wooden boats moored among water plants on Loktak Lake',
         kicker='Keibul Lamjao National Park', title='The world’s only floating national park.',
         text='About 40 km² of floating grassland on Loktak’s southern shore, home to the last wild Sangai. The Ithai Barrage, built in 1983, keeps water high in the dry months, and the phumdi is thinning.',
         chips=['Sanctuary 1966', 'National park 1977', 'Hog deer, otters, cranes'], src='Wikipedia', url=WIKI_K),
    dict(label='Manipur', bg='#5B3412', img=RAAS, pos='55% 40%', alt='Dancers performing Raas Lila in the Manipuri style',
         kicker='Manipur', title='The Land of Jewels.',
         text='The birthplace of modern polo, Sagol Kangjei, and of the Raas Lila dance. In Meitei tradition, killing a Sangai is a grave sin, and its antlered head adorns the royal boat Hiyang Hiren.',
         chips=['Polo’s birthplace', 'Raas Lila', 'Hiyang Hiren'], src='Manipur Tourism · Wikipedia', url=MT),
]


def hex_rgba(h, a):
    h = h.lstrip('#')
    return f'rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})'


dslide_html = ''
for i, s in enumerate(dslides):
    chips = ''.join(f'''
              <li style="padding: 6px 14px; border-radius: 999px; background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.28); font-size: 14px; font-weight: 600">{c}</li>''' for c in s['chips'])
    dslide_html += f'''
        <div data-slide class="dslide" id="topic-{i}" role="tabpanel" aria-label="{s['label']}"{' hidden' if i else ''} style="position: absolute; inset: 0; background: {s['bg']}">
          <img class="dslide-img" src="{s['img']}" alt="{s['alt']}" style="position: absolute; top: 0; right: 0; width: 62%; height: 100%; object-fit: cover; object-position: {s['pos']}">
          <div class="dslide-fade" aria-hidden="true" style="position: absolute; top: 0; bottom: 0; left: 38%; width: 22%; background: linear-gradient(to right, {s['bg']}, {hex_rgba(s['bg'], 0)})"></div>
          <div class="dslide-body" style="position: relative; max-width: 560px; padding: 56px 48px 120px; color: #FFFFFF">
            <p style="margin: 0 0 12px; font-size: 15px; font-weight: 600; opacity: 0.85">{s['kicker']}</p>
            <h2 style="margin: 0; font-size: clamp(36px, 4.6vw, 56px); line-height: 1.04; font-weight: 700; letter-spacing: -0.03em">{s['title']}</h2>
            <p style="margin: 18px 0 0; font-size: 18px; line-height: 1.5; opacity: 0.92">{s['text']}</p>
            <ul style="list-style: none; margin: 22px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 8px">{chips}
            </ul>
            <a href="{s['url']}" style="display: inline-flex; align-items: center; min-height: 44px; margin-top: 10px; color: #FFFFFF; font-size: 13px; font-weight: 600; opacity: 0.85">Source: {s['src']} <span aria-hidden="true">&nbsp;↗</span></a>
          </div>
        </div>'''
dtabs = ''.join(f'''
            <button type="button" class="dtab" role="tab" data-go="{i}" aria-controls="topic-{i}" aria-selected="{'true' if i == 0 else 'false'}">{s['label']}</button>''' for i, s in enumerate(dslides))

pop = [('1953', 6, 'Six found after near extinction'), ('1975', 14, 'First aerial census'), ('1995', 155, 'About 155'), ('2016', 260, 'Peak count'), ('2026', 172, 'Latest census: down by a third')]
bars = ''
for yr, n, lab in pop:
    h = max(4, round(n / 260 * 220))
    color = '#C2410C' if yr == '2026' else 'var(--tint)'
    bars += f'''
          <li aria-label="{yr}: {n}. {lab}" style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 10px; text-align: center">
            <span aria-hidden="true" style="font-size: 22px; font-weight: 700; letter-spacing: -0.02em">{n}</span>
            <span aria-hidden="true" style="display: block; width: 100%; max-width: 88px; height: {h}px; border-radius: 12px 12px 4px 4px; background: {color}"></span>
            <span aria-hidden="true" style="font-size: 15px; font-weight: 600">{yr}</span>
            <span aria-hidden="true" class="lab" style="font-size: 13px; line-height: 1.3; color: var(--label3)">{lab}</span>
          </li>'''
nums = [('40 km²', 'of floating grassland in Keibul Lamjao'), ('287 km²', 'typical area of Loktak Lake'), ('1.2 m', 'the thickest phumdi'), ('100,000', 'people living around the lake')]
num_html = ''.join(f'''
        <div style="padding: 28px; border-radius: 24px; background: var(--card)">
          <p style="margin: 0; font-size: 44px; line-height: 1; font-weight: 700; letter-spacing: -0.035em">{n}</p>
          <p style="margin: 10px 0 0; font-size: 15px; color: var(--label2)">{t}</p>
        </div>''' for n, t in nums)
symbols = [
    ('Animal', 'Sangai', 'Rucervus eldii eldii', '#0F3D24', STAG, '25% 30%'),
    ('Bird', 'Nongyeen', 'Mrs Hume’s pheasant', '#1F2F5C', PHEASANT, '45% 50%'),
    ('Flower', 'Shirui lily', 'Lilium mackliniae', '#7A2E4A', LILY, 'center 40%'),
    ('Tree', 'Uningthou', 'Phoebe hainesiana', '#3E4A1E', '', ''),
    ('Fish', 'Pengba', 'Osteobrama belangeri', '#0B3A53', '', ''),
]
sym_html = ''
for kind, name, sci, col, img, pos in symbols:
    bgimg = f'<img src="{img}" alt="" loading="lazy" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: {pos}; opacity: 0.55">' if img else ''
    sym_html += f'''
        <div style="position: relative; overflow: hidden; min-height: 220px; padding: 24px; border-radius: 24px; background: {col}; color: #FFFFFF; display: flex; flex-direction: column; justify-content: flex-end">{bgimg}
          <p style="position: relative; margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.85">State {kind}</p>
          <p style="position: relative; margin: 4px 0 0; font-size: 26px; line-height: 1.1; font-weight: 700; letter-spacing: -0.02em">{name}</p>
          <p style="position: relative; margin: 4px 0 0; font-size: 15px; font-style: italic; opacity: 0.9">{sci}</p>
        </div>'''

discover_body = f'''    <section style="max-width: 1080px; margin: 0 auto; padding: 72px 24px 32px">
      <h1 style="margin: 0; font-size: clamp(40px, 5vw, 56px); line-height: 1.04; font-weight: 700; letter-spacing: -0.03em">Discover the Sangai’s world</h1>
      <p style="margin: 14px 0 0; max-width: 34em; font-size: 20px; color: var(--label2)">A deer that looks back, islands that float, and the land that holds them.</p>
    </section>

    <section data-slideshow aria-roledescription="carousel" aria-label="Discover" style="max-width: 1080px; margin: 0 auto; padding: 0 24px">
      <div style="position: relative; min-height: 560px; border-radius: 32px; overflow: hidden; background: #0F3D24">{dslide_html}
        <div class="dctrl" style="position: absolute; left: 40px; right: 40px; bottom: 28px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px">
          <div role="tablist" aria-label="Topics" style="display: flex; flex-wrap: wrap; gap: 6px">{dtabs}
          </div>
          <div class="glassbar" style="display: flex; gap: 4px; padding: 4px; border-radius: 999px; background: rgba(0,0,0,0.3)">
            <button type="button" data-prev aria-label="Previous topic" style="{GLASS_BTN}">{CHEV_L}</button>
            <button type="button" data-next aria-label="Next topic" style="{GLASS_BTN}">{CHEV_R}</button>
          </div>
        </div>
      </div>
    </section>

    <section style="{SEC}">
      <div style="display: flex; flex-wrap: wrap; align-items: flex-end; gap: 24px 40px; margin-bottom: 32px">
        <div style="flex: 1 1 420px; min-width: 0">
          <h2 style="{H2}">A comeback now slipping away</h2>
          <p style="margin: 8px 0 0; max-width: 38em; color: var(--label2)">Brought back from near extinction in the 1950s, the Sangai grew to 260 by 2016. The 2026 census found only 172, as its floating home thins and deer drown where the phumdi gives way.</p>
        </div>
        <img src="{SANGAI2}" alt="A Sangai hind looking at the camera, with a stag half-hidden in the tall grass behind her" loading="lazy" style="flex: 0 1 300px; width: 300px; max-width: 100%; aspect-ratio: 4 / 3; object-fit: cover; object-position: 50% 40%; border-radius: 24px">
      </div>
      <div class="pad-card" style="padding: 40px 32px 32px; border-radius: 28px; background: var(--card)">
        <ol class="bars" aria-label="Sangai population by year" style="list-style: none; margin: 0; padding: 0; display: flex; align-items: flex-end; gap: 16px; min-height: 340px">{bars}
        </ol>
      </div>
      <p style="margin: 16px 8px 0; font-size: 15px; color: var(--label2)">Independent monitoring by the Wildlife Institute of India paints an even starker picture: 91 Sangai in 2006, 76 in 2019 and 64 in 2023.</p>
      <p style="margin: 8px 8px 0; font-size: 13px; color: var(--label3)">Manipur Forest Department counts. Sources: <a href="{WIKI_S}">Wikipedia</a>, <a href="https://www.easternmirrornagaland.com/hog-deer-outnumber-sangai-in-keibul-lamjao-national-park">Eastern Mirror (2026 census)</a>, <a href="https://indiawildlifenews.com/2026/06/14/sangai-manipur-eld-deer-keibul-lamjao-antlers-antelopes-part-9/">India Wildlife News (WII figures)</a>, <a href="https://www.downtoearth.org.in/wildlife-biodiversity/drowning-in-its-home">Down To Earth</a>.</p>
    </section>

    <section style="{SEC}">
      <h2 style="{H2}; margin-bottom: 24px">Loktak by the numbers</h2>
      <img src="{LOKTAK}" alt="Loktak Lake under a clear sky, with a wooded hill on its shore" loading="lazy" style="display: block; width: 100%; aspect-ratio: 21 / 9; object-fit: cover; object-position: center 58%; border-radius: 28px; margin-bottom: 16px">
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px">{num_html}
      </div>
      <p style="margin: 12px 8px 0; font-size: 13px; color: var(--label3)">Source: <a href="{WIKI_L}">Wikipedia, Loktak Lake</a> and <a href="{WIKI_K}">Keibul Lamjao National Park</a>.</p>
    </section>

    <section style="{SEC}">
      <h2 style="{H2}">Manipur’s state symbols</h2>
      <p style="margin: 8px 0 24px; color: var(--label2)">Five living emblems, with the Sangai at the head.</p>
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px">{sym_html}
      </div>
      <p style="margin: 12px 8px 0; font-size: 13px; color: var(--label3)">Source: <a href="{WIKI_M}">Wikipedia, Manipur</a>.</p>
    </section>

    <section class="has-wm" style="{SEC}; padding-bottom: 120px; text-align: center">
      {wm("center")}
      <h2 style="{H2}">Help keep these stories alive</h2>
      <p style="margin: 12px auto 28px; max-width: 30em; color: var(--label2)">Invite us to your school, or support our work for the Sangai.</p>
      <a href="contact.html" style="{CTA}">Get in touch</a>
    </section>'''

LIC = {
    'CC BY-SA 4.0': 'https://creativecommons.org/licenses/by-sa/4.0/',
    'CC BY 2.0': 'https://creativecommons.org/licenses/by/2.0/',
    'CC BY 4.0': 'https://creativecommons.org/licenses/by/4.0/',
}
credits = [
    ('Phumdi', 'The_Phumdis_on_Loktak_Lake.jpg', 'Ishani Nath', 'CC BY-SA 4.0'),
    ('Keibul Lamjao', 'Loktak_Lake_Manipur_02.jpg', 'ch_15march', 'CC BY 2.0'),
    ('Loktak Lake', 'Loktak_Lake_Manipur_01.jpg', 'ch_15march', 'CC BY 2.0'),
    ('Raas Lila', 'Rasa_Lila_in_Manipuri_dance_style.jpg', 'matsukin (Flickr)', 'CC BY 2.0'),
    ('Mrs Hume’s pheasant', 'Syrmaticus_humiae_104702127.jpg', 'Christoph Moning', 'CC BY 4.0'),
    ('Shirui lily', 'Shirui_Lily.jpg', 'Mashangva', 'CC BY-SA 4.0'),
    ('Sangai hind and stag', 'Sangai_Brow-antlered_Deer_Rucervus_eldii_eldii_Manipur_by_Dr._Raju_Kasambe_(1).jpg', 'Raju Kasambe', 'CC BY-SA 4.0'),
]
credits_html = 'Photos from Wikimedia Commons: ' + '; '.join(
    f'<a href="https://commons.wikimedia.org/wiki/File:{e(f)}">{what}</a> by {who}, <a href="{LIC[lic]}">{lic}</a>'
    for what, f, who, lic in credits) + '.'

# ---------------------------------------------------------------- write
site_pages = [
    ('index.html', 'Sangai First Foundation', 'A non-profit trust in Manipur building a people’s movement for the Sangai and Keibul Lamjao, the world’s only floating national park.', 'Home', home_body, ''),
    ('discover.html', 'Discover · Sangai First Foundation', 'The Sangai, the floating phumdi of Loktak Lake, Keibul Lamjao National Park and Manipur.', 'Discover', discover_body, credits_html),
    ('work.html', 'Our work · Sangai First Foundation', 'Sangai Day programmes, quizzes, tree drives and news from Sangai First Foundation.', 'Our Work', work_body, ''),
    ('about.html', 'About · Sangai First Foundation', 'How four friends founded Sangai First Foundation, our story so far and our trustees.', 'About', about_body, ''),
    ('contact.html', 'Contact · Sangai First Foundation', 'Donate, host a programme at your school, or partner with Sangai First Foundation.', 'Contact', contact_body, ''),
]

os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
with open(os.path.join(OUT, 'assets', 'styles.css'), 'w', encoding='utf-8') as f:
    f.write(CSS)
with open(os.path.join(OUT, 'assets', 'site.js'), 'w', encoding='utf-8') as f:
    f.write(JS)
for fn, title, desc, active, body, cred in site_pages:
    with open(os.path.join(OUT, fn), 'w', encoding='utf-8') as f:
        f.write(page(title, desc, active, body, cred))

# Custom domain for GitHub Pages.
with open(os.path.join(OUT, 'CNAME'), 'w', encoding='utf-8') as f:
    f.write('sangaifirst.com\n')

# Copy the images the site uses (skip founders-cutout.webp, which no page uses).
img_out = os.path.join(OUT, 'images')
os.makedirs(img_out, exist_ok=True)
for name in sorted(os.listdir(os.path.join(ROOT, 'images'))):
    if name == 'founders-cutout.webp' or name.startswith('.'):
        continue
    shutil.copy2(os.path.join(ROOT, 'images', name), os.path.join(img_out, name))
print('built', len(site_pages), 'pages into', OUT)
