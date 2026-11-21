import json, os
OUT = '/home/claude/sff/site/project'
DEER = '../images/deer-hd.jpg'
GROUP = '../images/group-hd.jpg'
SPEAKER = '../images/speaker-hd.jpg'
CLASS = '../images/class-hd.jpg'
ENGRAVE = '../images/deer-engraving.png'

HELMET = '''<helmet>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Playfair+Display:wght@900&amp;display=swap">
<style>
:root{
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
body{margin:0;background:var(--bg)}
@media (prefers-reduced-motion: no-preference){ html{scroll-behavior:smooth} }
a{color:var(--tint)}a:hover{opacity:0.8}
a:focus-visible,button:focus-visible{outline:3px solid var(--tint);outline-offset:3px}
.glassbar{-webkit-backdrop-filter:blur(24px) saturate(180%);backdrop-filter:blur(24px) saturate(180%)}
.track{scrollbar-width:none}
.track::-webkit-scrollbar{display:none}
button{font:inherit}
</style>
</helmet>'''

ROOT_OPEN = '<div style="font-family: -apple-system, BlinkMacSystemFont, &quot;SF Pro Text&quot;, Inter, system-ui, sans-serif; color: var(--label); background: var(--bg); font-size: 17px; line-height: 1.5; -webkit-font-smoothing: antialiased">'

def nav(active):
    items = [('Home', 'Main.dc.html'), ('Discover', 'Discover.dc.html'), ('Our Work', 'Work.dc.html'), ('About', 'About.dc.html')]
    links = ''
    for name, href in items:
        cur = ' aria-current="page"' if name == active else ''
        weight = '600' if name == active else '500'
        color = 'var(--label)' if name == active else 'var(--label2)'
        links += f'\n        <a href="{href}"{cur} style="display: inline-flex; align-items: center; min-height: 44px; padding: 0 14px; color: {color}; font-weight: {weight}; text-decoration: none">{name}</a>'
    return f'''  <header style="position: sticky; top: 0; z-index: 10; padding: 12px 16px 0">
    <nav aria-label="Main" class="glassbar" style="max-width: 1080px; margin: 0 auto; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 4px 16px; padding: 6px 6px 6px 18px; background: var(--glass); border: 1px solid var(--glass-edge); border-radius: 999px; box-shadow: var(--shadow)">
      <a href="Main.dc.html" style="display: flex; align-items: center; gap: 10px; min-height: 44px; text-decoration: none; color: var(--label); font-weight: 600; font-size: 16px; letter-spacing: -0.01em">
        <img class="engrave" src="{ENGRAVE}" alt="" style="width: 24px; height: 34px; object-fit: contain">
        Sangai First Foundation
      </a>
      <div style="display: flex; flex-wrap: wrap; align-items: center; font-size: 15px">{links}
        <a href="Contact.dc.html" style="display: inline-flex; align-items: center; min-height: 44px; padding: 0 20px; margin-left: 6px; background: var(--tint); color: var(--on-tint); text-decoration: none; border-radius: 999px; font-weight: 600">Support us</a>
      </div>
    </nav>
  </header>'''

FOOTER = '''  <footer>
    <div style="max-width: 1080px; margin: 0 auto; padding: 40px 32px 48px; border-top: 1px solid var(--sep); display: flex; flex-wrap: wrap; gap: 8px 32px; justify-content: space-between; font-size: 13px; color: var(--label3)">
      <p style="margin: 0">© Sangai First Foundation, Manipur · Reg. no. 442 of 02/10/2025, Indian Trusts Act, 1882</p>
      <a href="https://www.facebook.com/profile.php?id=61573232295835" style="display: inline-flex; align-items: center; min-height: 44px; margin: -12px 0">Facebook</a>
    </div>
  </footer>'''

def arrows(label):
    btn = 'display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 999px; border: 1px solid var(--sep); background: var(--card); color: var(--label); cursor: pointer; padding: 0'
    return f'''<div style="display: flex; gap: 8px">
            <button type="button" aria-label="Previous {label}" onClick="{{{{scrollPrev}}}}" style="{btn}"><svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2L2 8l6 6"></path></svg></button>
            <button type="button" aria-label="Next {label}" onClick="{{{{scrollNext}}}}" style="{btn}"><svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 2l6 6-6 6"></path></svg></button>
          </div>'''

TRACK = 'display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 4px 24px 24px; scroll-padding-left: 24px'

SCROLL_JS = '''  scroller(dir) {
    return (e) => {
      const t = e.currentTarget.closest('[data-carousel]').querySelector('[data-track]');
      const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      t.scrollBy({ left: dir * t.clientWidth * 0.8, behavior: reduce ? 'auto' : 'smooth' });
    };
  }'''

def page(title, body, js, h):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
{ROOT_OPEN}
{body}
{FOOTER}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{h}}}}}'>
class Component extends DCLogic {{
{js}
}}
</script>
</body>
</html>
'''

H2 = 'margin: 0; font-size: 34px; line-height: 1.15; font-weight: 700; letter-spacing: -0.022em'
SEC = 'max-width: 1080px; margin: 0 auto; padding: 120px 24px 0'

# ---------------- HOME ----------------
home_body = nav('Home') + f'''
  <main>
    <section aria-roledescription="carousel" aria-label="Highlights" style="max-width: 1080px; margin: 0 auto; padding: 32px 24px 0">
      <div style="position: relative; border-radius: 28px; overflow: hidden; background: #0B0F0B; height: 600px">
        <sc-for list="{{{{slides}}}}" as="s" hint-placeholder-count="1">
          <sc-if value="{{{{s.active}}}}" hint-placeholder-val="{{{{true}}}}">
            <div role="group" aria-roledescription="slide" aria-label="{{{{s.label}}}}" style="position: absolute; inset: 0">
              <img src="{{{{s.img}}}}" alt="{{{{s.alt}}}}" style="width: 100%; height: 100%; object-fit: cover; object-position: center 35%">
              <div style="position: absolute; inset: auto 0 0 0; padding: 120px 48px 40px; background: linear-gradient(to top, rgba(0,0,0,0.62), rgba(0,0,0,0))">
                <p style="margin: 0 0 8px; font-size: 15px; font-weight: 600; color: rgba(255,255,255,0.85)">{{{{s.kicker}}}}</p>
                <p style="margin: 0; max-width: 18em; font-size: clamp(32px, 4.5vw, 52px); line-height: 1.08; font-weight: 700; letter-spacing: -0.025em; color: #FFFFFF">{{{{s.title}}}}</p>
              </div>
            </div>
          </sc-if>
        </sc-for>
        <div class="glassbar" style="position: absolute; right: 24px; bottom: 32px; display: flex; align-items: center; gap: 4px; padding: 4px; border-radius: 999px; background: rgba(0,0,0,0.35)">
          <button type="button" aria-label="Previous slide" onClick="{{{{prevSlide}}}}" style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border: 0; border-radius: 999px; background: transparent; color: #FFFFFF; cursor: pointer; padding: 0"><svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2L2 8l6 6"></path></svg></button>
          <sc-for list="{{{{slides}}}}" as="s" hint-placeholder-count="3">
            <button type="button" aria-label="Show slide {{{{s.n}}}}" aria-current="{{{{s.current}}}}" onClick="{{{{s.go}}}}" style="display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 44px; border: 0; background: transparent; cursor: pointer; padding: 0"><span style="{{{{s.dot}}}}"></span></button>
          </sc-for>
          <button type="button" aria-label="Next slide" onClick="{{{{nextSlide}}}}" style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border: 0; border-radius: 999px; background: transparent; color: #FFFFFF; cursor: pointer; padding: 0"><svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 2l6 6-6 6"></path></svg></button>
        </div>
      </div>
    </section>

    <section style="max-width: 760px; margin: 0 auto; padding: 120px 24px 0; text-align: center">
      <div aria-hidden="true" style="display: flex; justify-content: center; margin-bottom: 32px">
        <img src="{DEER}" alt="" style="width: 72px; height: 72px; object-fit: cover; border-radius: 999px; border: 3px solid var(--bg)">
        <img src="{GROUP}" alt="" style="width: 72px; height: 72px; object-fit: cover; border-radius: 999px; border: 3px solid var(--bg); margin-left: -16px">
        <img src="{CLASS}" alt="" style="width: 72px; height: 72px; object-fit: cover; border-radius: 999px; border: 3px solid var(--bg); margin-left: -16px">
      </div>
      <p style="margin: 0; font-size: clamp(26px, 3vw, 34px); line-height: 1.3; font-weight: 600; letter-spacing: -0.018em">A non-profit trust in Manipur, building a people’s movement for the Sangai and Keibul Lamjao, the world’s only floating national park.</p>
      <a href="About.dc.html" style="display: inline-flex; align-items: center; gap: 6px; min-height: 44px; margin-top: 20px; font-size: 17px; font-weight: 500; text-decoration: none">Learn about us <span aria-hidden="true">›</span></a>
    </section>

    <section style="{SEC}">
      <a href="Work.dc.html" style="display: flex; flex-wrap: wrap; align-items: center; gap: 24px 40px; padding: 40px; border-radius: 28px; background: var(--tint-fill); color: var(--label); text-decoration: none">
        <div aria-hidden="true" style="text-align: center; line-height: 1; color: var(--tint)">
          <p style="margin: 0; font-size: 72px; font-weight: 700; letter-spacing: -0.04em">10</p>
          <p style="margin: 6px 0 0; font-size: 15px; font-weight: 700; letter-spacing: 0.12em">DECEMBER</p>
        </div>
        <div style="flex: 1 1 360px; min-width: 0">
          <p style="margin: 0; font-size: 15px; font-weight: 600; color: var(--tint)">Coming up</p>
          <p style="margin: 4px 0 0; font-size: 28px; line-height: 1.2; font-weight: 700; letter-spacing: -0.02em">The 3rd Sangai Day</p>
          <p style="margin: 8px 0 0; color: var(--label2)">Every 10 December, recalling the 1954 resolution to protect the Sangai. This year’s quiz winners will be honoured.</p>
        </div>
        <img src="{GROUP}" alt="Students holding a Sangai Day banner" style="flex: 0 1 280px; width: 280px; max-width: 100%; aspect-ratio: 3 / 2; object-fit: cover; border-radius: 18px">
      </a>
    </section>

    <section data-carousel="" aria-label="Recent work" style="padding: 120px 0 0">
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px">
        <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; margin-bottom: 24px">
          <div>
            <h2 style="{H2}">Recent work</h2>
            <a href="Work.dc.html" style="display: inline-flex; align-items: center; min-height: 44px; font-weight: 500; text-decoration: none">See all programmes ›</a>
          </div>
          {arrows('programmes')}
        </div>
      </div>
      <div style="max-width: 1128px; margin: 0 auto">
        <ul data-track="" class="track" style="{TRACK}; list-style: none; margin: 0">
          <sc-for list="{{{{recent}}}}" as="ev" hint-placeholder-count="6">
            <sc-if value="{{{{ev.photo}}}}" hint-placeholder-val="{{{{false}}}}">
              <li style="flex: 0 0 300px; scroll-snap-align: start; min-height: 260px; border-radius: 24px; overflow: hidden; position: relative; box-shadow: var(--shadow)">
                <img src="{{{{ev.img}}}}" alt="{{{{ev.alt}}}}" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover">
                <p style="position: absolute; left: 0; right: 0; bottom: 0; margin: 0; padding: 48px 24px 20px; font-size: 15px; font-weight: 600; color: #FFFFFF; background: linear-gradient(to top, rgba(0,0,0,0.6), rgba(0,0,0,0))">{{{{ev.caption}}}}</p>
              </li>
            </sc-if>
            <sc-if value="{{{{ev.text}}}}" hint-placeholder-val="{{{{true}}}}">
            <li style="flex: 0 0 300px; scroll-snap-align: start; display: flex; flex-direction: column; justify-content: space-between; min-height: 260px; padding: 28px; border-radius: 24px; background: var(--card); box-shadow: var(--shadow)">
              <p style="margin: 0; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; color: var(--label3)">{{{{ev.date}}}}</p>
              <div>
                <h3 style="margin: 0; font-size: 22px; line-height: 1.25; font-weight: 600; letter-spacing: -0.01em">{{{{ev.title}}}}</h3>
                <p style="margin: 8px 0 0; font-size: 15px; color: var(--label3)">{{{{ev.place}}}}</p>
              </div>
            </li>
            </sc-if>
          </sc-for>
        </ul>
      </div>
    </section>

    <section data-carousel="" aria-label="Sangai quiz" style="padding: 120px 0 0">
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px">
        <div style="display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; margin-bottom: 24px">
          <div>
            <h2 style="{H2}">How well do you know the Sangai?</h2>
            <a href="Discover.dc.html" style="display: inline-flex; align-items: center; min-height: 44px; font-weight: 500; text-decoration: none">Discover more ›</a>
          </div>
          {arrows('questions')}
        </div>
      </div>
      <div style="max-width: 1128px; margin: 0 auto">
        <ul data-track="" class="track" style="{TRACK}; list-style: none; margin: 0">
          <sc-for list="{{{{quiz}}}}" as="q" hint-placeholder-count="5">
            <li style="{{{{q.cardStyle}}}}">
              <p style="margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.08em; opacity: 0.8">QUESTION {{{{q.n}}}} OF {{{{q.total}}}}</p>
              <p style="margin: 0; flex: 1; font-size: 24px; line-height: 1.25; font-weight: 600; letter-spacing: -0.01em">{{{{q.q}}}}</p>
              <sc-if value="{{{{q.shown}}}}" hint-placeholder-val="{{{{false}}}}">
                <div aria-live="polite">
                  <p style="margin: 0; font-size: 44px; line-height: 1; font-weight: 700; letter-spacing: -0.03em">{{{{q.a}}}}</p>
                  <p style="margin: 10px 0 0; font-size: 15px; line-height: 1.45; opacity: 0.92">{{{{q.more}}}}</p>
                </div>
              </sc-if>
              <sc-if value="{{{{q.hidden}}}}" hint-placeholder-val="{{{{true}}}}">
                <button type="button" onClick="{{{{q.reveal}}}}" style="align-self: flex-start; min-height: 44px; padding: 0 22px; border: 0; border-radius: 999px; background: rgba(255,255,255,0.92); color: #10251A; font-size: 15px; font-weight: 600; cursor: pointer">Reveal the answer</button>
              </sc-if>
            </li>
          </sc-for>
        </ul>
      </div>
    </section>

    <section style="{SEC}; padding-bottom: 120px; text-align: center">
      <h2 style="{H2}">Stand with the Sangai</h2>
      <p style="margin: 12px auto 28px; max-width: 30em; color: var(--label2)">Host a programme at your school, partner with us, or support our work.</p>
      <a href="Contact.dc.html" style="display: inline-flex; align-items: center; min-height: 50px; padding: 0 28px; background: var(--tint); color: var(--on-tint); text-decoration: none; border-radius: 999px; font-weight: 600">Get in touch</a>
    </section>
  </main>'''

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
recent_items = []
for i, (d, t, p) in enumerate(recent):
    recent_items.append(dict(text=True, photo=False, date=d, title=t, place=p))
    if i == 1: recent_items.append(dict(text=False, photo=True, img=CLASS, alt='Students at a school programme', caption='Students at one of our school programmes'))
    if i == 3: recent_items.append(dict(text=False, photo=True, img=SPEAKER, alt='A trustee speaking at a school programme', caption='A talk on the Sangai’s history and ecology'))
quiz = [
    dict(q='How many Sangai did the 2026 census find in the wild?', a='172', more='Down from 260 in 2016. Every one lives in Keibul Lamjao.'),
    dict(q='What does the name “Sangai” mean?', a='The one that waits', more='From “sa” (animal) and “ngai” (awaiting): a running stag stops to look back.'),
    dict(q='How thick is the floating phumdi the Sangai walks on?', a='Up to 1.2 m', more='Only about a fifth of it sits above the water, enough to carry a deer.'),
    dict(q='When does the Sangai like to graze?', a='Dawn and dusk', more='Roughly 4:30 to 8 am and 3 to 6 pm, resting under tall reeds in between.'),
    dict(q='Which sport was born in Manipur as Sagol Kangjei?', a='Polo', more='Manipur is known as the birthplace of modern polo.'),
]
home_js = f'''  constructor(props) {{ super(props); this.state = {{ slide: 0, rev: {{}} }}; }}
{SCROLL_JS}
  renderVals() {{
    const raw = {json.dumps(slides, ensure_ascii=False)};
    const n = raw.length, cur = this.state.slide;
    const go = (i) => this.setState({{ slide: (i + n) % n }});
    const slides = raw.map((s, i) => ({{ ...s, n: i + 1, active: i === cur, current: i === cur ? 'true' : 'false', go: () => go(i),
      dot: 'display:block;width:8px;height:8px;border-radius:999px;background:' + (i === cur ? '#FFFFFF' : 'rgba(255,255,255,0.45)') }}));
    const recent = {json.dumps(recent_items, ensure_ascii=False)};
    const qraw = {json.dumps(quiz, ensure_ascii=False)};
    const colors = ['#0F3D24', '#0B3A53', '#5B3412', '#1F2F5C', '#3D2A52'];
    const rev = this.state.rev || {{}};
    const quiz = qraw.map((q, i) => ({{ ...q, n: i + 1, total: qraw.length, shown: !!rev[i], hidden: !rev[i],
      reveal: () => this.setState({{ rev: {{ ...rev, [i]: true }} }}),
      cardStyle: 'flex:0 0 320px;scroll-snap-align:start;display:flex;flex-direction:column;gap:20px;min-height:340px;padding:28px;border-radius:24px;color:#FFFFFF;background:' + colors[i % colors.length] }}));
    return {{ slides, recent, quiz, prevSlide: () => go(cur - 1), nextSlide: () => go(cur + 1), scrollPrev: this.scroller(-1), scrollNext: this.scroller(1) }};
  }}'''

# ---------------- WORK ----------------
work_body = nav('Our Work') + f'''
  <main>
    <section style="max-width: 1080px; margin: 0 auto; padding: 96px 24px 0">
      <h1 style="margin: 0; font-size: clamp(40px, 5vw, 56px); line-height: 1.05; font-weight: 700; letter-spacing: -0.028em">Our work</h1>
      <p style="margin: 16px 0 0; max-width: 34em; font-size: 20px; color: var(--label2)">Talks, quizzes, books and a pledge, in a different school almost every month.</p>
      <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 16px; margin-top: 48px">
        <img src="{CLASS}" alt="A hall full of students at a sensitisation programme" style="width: 100%; height: 360px; object-fit: cover; border-radius: 28px">
        <img src="{SPEAKER}" alt="A trustee speaking at a school programme" style="width: 100%; height: 360px; object-fit: cover; border-radius: 28px">
      </div>
    </section>

    <section data-carousel="" aria-label="Programmes" style="padding: 64px 0 0">
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px 24px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px">
        <div role="group" aria-label="Year" style="display: inline-flex; padding: 3px; border-radius: 999px; background: var(--card2)">
          <sc-for list="{{{{years}}}}" as="y" hint-placeholder-count="2">
            <button type="button" aria-pressed="{{{{y.pressed}}}}" onClick="{{{{y.pick}}}}" style="{{{{y.style}}}}">{{{{y.label}}}}</button>
          </sc-for>
        </div>
        {arrows('programmes')}
      </div>
      <div style="max-width: 1128px; margin: 0 auto">
        <ul data-track="" class="track" style="{TRACK}; list-style: none; margin: 0">
          <sc-for list="{{{{events}}}}" as="ev" hint-placeholder-count="6">
            <li style="flex: 0 0 340px; scroll-snap-align: start; display: flex; flex-direction: column; gap: 16px; min-height: 300px; padding: 28px; border-radius: 24px; background: var(--card); box-shadow: var(--shadow)">
              <p style="margin: 0; font-size: 13px; font-weight: 600; letter-spacing: 0.04em; color: var(--tint)">{{{{ev.date}}}}</p>
              <div style="flex: 1">
                <h2 style="margin: 0; font-size: 22px; line-height: 1.25; font-weight: 600; letter-spacing: -0.01em">{{{{ev.title}}}}</h2>
                <p style="margin: 6px 0 0; font-size: 15px; color: var(--label3)">{{{{ev.place}}}}</p>
              </div>
              <p style="margin: 0; font-size: 15px; line-height: 1.45; color: var(--label2)">{{{{ev.note}}}}</p>
            </li>
          </sc-for>
        </ul>
      </div>
    </section>

    <section style="{SEC}">
      <figure style="margin: 0">
        <img src="{GROUP}" alt="Students and teachers at Toubul Government High School holding a Sangai Day banner" style="display: block; width: 100%; aspect-ratio: 16 / 9; object-fit: cover; border-radius: 28px">
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
    </section>
  </main>'''

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
    ('19 Apr 2025', 'Sangai Day at school', 'Chingmei High School', '12 books donated; 71 students took the quiz.'),
    ('8 Mar 2025', 'Let’s Know Our Sangai', 'Sekmaijin High School, Imphal West', 'With the Chief Conservator of Forests (Wildlife).'),
    ('22 Feb 2025', 'Sangai Day at school', 'Sambanlei Sekpil School, Kumbi', '145 students, 7 teachers and 12 parents.'),
    ('28 Jan 2025', 'First Responsible School', 'New Model Public School, Moirang', 'Our first adopted school.'),
    ('10 Dec 2024', '1st Sangai Day', 'Manipur Zoological Garden', 'The launch of our year-long school programme.'),
]
work_js = f'''  constructor(props) {{ super(props); this.state = {{ year: '2026' }}; }}
{SCROLL_JS}
  renderVals() {{
    const data = {{ '2026': {json.dumps([dict(date=a, title=b, place=c, note=d) for a, b, c, d in ev2026], ensure_ascii=False)},
      '2024–25': {json.dumps([dict(date=a, title=b, place=c, note=d) for a, b, c, d in ev2025], ensure_ascii=False)} }};
    const base = 'min-height:40px;padding:0 20px;border:0;border-radius:999px;cursor:pointer;font-size:15px;font-weight:600;';
    const years = Object.keys(data).map((k) => ({{ label: k, pressed: k === this.state.year ? 'true' : 'false',
      pick: (e) => {{ this.setState({{ year: k }}); const t = e.currentTarget.closest('[data-carousel]').querySelector('[data-track]'); t.scrollLeft = 0; }},
      style: base + (k === this.state.year ? 'background:var(--card);color:var(--label);box-shadow:0 1px 4px rgba(0,0,0,0.12)' : 'background:transparent;color:var(--label2)') }}));
    return {{ years, events: data[this.state.year], scrollPrev: this.scroller(-1), scrollNext: this.scroller(1) }};
  }}'''

# ---------------- ABOUT ----------------
FOUNDERS = '../images/founders-cutout.webp'
trustees = [
    ('Dr Khangembam Shamungou', 'President · Managing Trustee', 'Founder. Author of 23 books on nature and the Sangai.'),
    ('Kumam Jugeshor', 'Vice-President', 'Founder. Ornithologist and retired Principal of Kumbi College.'),
    ('Salam Prasanta', 'Trustee', 'Founder.'),
    ('Khwairakpam Budha', 'Trustee', 'Founder.'),
    ('Elangbam Premjit', 'Trustee', ''),
    ('Salam Brajakumar', 'Trustee', ''),
    ('Tongbram Budhi', 'Trustee', ''),
]
story = [
    dict(when='1954', title='A sanctuary is born', text='On 10 December, the Manipur Board for Wildlife, chaired by V.S. Sundram, resolved to create a 50 km² sanctuary for the Sangai.'),
    dict(when='24 Nov 2024', title='Four friends, two decisions', text='At Dr Shamungou’s home in Nambol Makha Leikai, the founders declared 10 December “Sangai Day” and founded Sangai First Foundation.'),
    dict(when='10 Dec 2024', title='The first Sangai Day', text='Held at Manipur Zoological Garden, Iroisemba, with the Forest Department’s Wildlife Wing. A year-long school campaign begins.'),
    dict(when='27 Feb 2025', title='Going online', text='Our Facebook page launches. By November 2026 it has 107 posts this year and 4.5K views.'),
    dict(when='10 Dec 2025', title='2nd Sangai Day', text='At Phouoibee Community Hall, Keibul Lamjao. 152 quiz winners and the top five of Yarou Sangai 2025 are honoured.'),
    dict(when='2026', title='Roots and wheels', text='Nine more schools, a Save Sangai Campaign Block in Kakching, native tree drives and a 15 km Green Ride.'),
    dict(when='10 Dec 2026', title='Sangai Heritage Hub', text='On the 3rd Sangai Day, we plan to open a permanent centre for conservation education at Keibul Ching.'),
]
stats = [('1,054', 'students reached across 11 schools in 2025'), ('586', 'students reached across 9 schools in 2026'), ('269', 'quiz winners recognised in 2025 and 2026'), ('268', 'people joined our 2026 planting drives')]
stat_html = ''.join(f"""
        <div style="padding: 28px; border-radius: 24px; background: var(--card)">
          <p style="margin: 0; font-size: 48px; line-height: 1; font-weight: 700; letter-spacing: -0.035em; color: var(--tint)">{n}</p>
          <p style="margin: 10px 0 0; font-size: 15px; color: var(--label2)">{t}</p>
        </div>""" for n, t in stats)
about_body = nav('About') + f"""
  <main>
    <section style="max-width: 1080px; margin: 0 auto; padding: 96px 24px 0; display: flex; flex-wrap: wrap; align-items: center; gap: 72px 56px">
      <div style="flex: 1 1 380px; min-width: 0">
        <p style="margin: 0 0 12px; font-size: 15px; font-weight: 600; color: var(--tint)">Our story</p>
        <h1 style="margin: 0; font-size: clamp(40px, 5vw, 60px); line-height: 1.03; font-weight: 700; letter-spacing: -0.032em">It began with four friends and one idea.</h1>
        <p style="margin: 24px 0 0; font-size: 19px; line-height: 1.55; color: var(--label2)">On 24 November 2024, four environmentalists met at a home in Nambol Makha Leikai. They left with a plan: give the Sangai a day of its own, and a trust to protect it.</p>
        <p style="margin: 20px 0 0; font-size: 15px; color: var(--label3)">Dr Khangembam Shamungou · Kumam Jugeshor · Salam Prasanta · Khwairakpam Budha</p>
      </div>
      <figure style="flex: 1 1 460px; min-width: 0; margin: 0; padding: 24px 0 48px; perspective: 1400px">
        <div style="position: relative; height: 560px; transform: rotate(-2.2deg) rotateY(-8deg); filter: drop-shadow(0 30px 40px rgba(0,0,0,0.28)) drop-shadow(0 4px 6px rgba(0,0,0,0.18))">
          <div style="position: absolute; inset: 0; clip-path: polygon(0.0% 0.5%, 3.6% 0.2%, 7.1% 1.0%, 10.7% 0.1%, 14.3% 0.9%, 17.9% 0.6%, 21.4% 0.1%, 25.0% 0.8%, 28.6% 0.1%, 32.1% 0.7%, 35.7% 0.1%, 39.3% 0.1%, 42.9% 0.7%, 46.4% 1.3%, 50.0% 0.2%, 53.6% 0.4%, 57.1% 1.0%, 60.7% 1.5%, 64.3% 0.9%, 67.9% 0.6%, 71.4% 1.6%, 75.0% 0.1%, 78.6% 1.4%, 82.1% 0.5%, 85.7% 0.2%, 89.3% 0.2%, 92.9% 0.5%, 96.4% 1.3%, 100.0% 0.3%, 99.5% 12.5%, 99.4% 25.0%, 99.7% 37.5%, 99.5% 50.0%, 99.9% 62.5%, 99.9% 75.0%, 99.8% 87.5%, 100.0% 98.9%, 96.4% 99.3%, 92.9% 99.5%, 89.3% 99.1%, 85.7% 99.3%, 82.1% 99.5%, 78.6% 98.7%, 75.0% 98.9%, 71.4% 99.6%, 67.9% 99.1%, 64.3% 99.2%, 60.7% 98.6%, 57.1% 98.8%, 53.6% 99.5%, 50.0% 98.4%, 46.4% 99.8%, 42.9% 99.3%, 39.3% 98.8%, 35.7% 99.8%, 32.1% 99.2%, 28.6% 99.9%, 25.0% 98.9%, 21.4% 98.8%, 17.9% 99.1%, 14.3% 98.6%, 10.7% 99.5%, 7.1% 98.9%, 3.6% 99.0%, 0.0% 99.1%, 0.4% 87.5%, 0.8% 75.0%, 0.9% 62.5%, 0.4% 50.0%, 0.6% 37.5%, 0.1% 25.0%, 0.6% 12.5%); background-color: #EFE7D4; background-image: radial-gradient(rgba(40,32,20,0.07) 1px, transparent 1.3px); background-size: 5px 5px; color: #1C1A16; font-family: Georgia, &quot;Times New Roman&quot;, serif; padding: 26px 30px">
            <div style="display: flex; justify-content: space-between; gap: 12px; padding-bottom: 6px; border-bottom: 3px double #1C1A16; font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase">
              <span>Sangai First Foundation</span><span>Nambol · 24 Nov 2024</span>
            </div>
            <p style="margin: 14px 0 0; font-family: &quot;Playfair Display&quot;, Georgia, serif; font-size: 30px; line-height: 1.05; font-weight: 900; letter-spacing: -0.01em">Four friends resolve to give the Sangai its own day</p>
            <p style="margin: 10px 0 0; padding-top: 8px; border-top: 1px solid rgba(28,26,22,0.6); font-size: 13px; line-height: 1.45; font-style: italic; columns: 2; column-gap: 20px; column-rule: 1px solid rgba(28,26,22,0.35)">Meeting at a home in Nambol Makha Leikai, the four agreed to mark every 10 December as Sangai Day, recalling the 1954 resolution that created the Sangai sanctuary, and to found a trust to carry the work into schools.</p>
          </div>
          <img src="../images/founders-newsprint.webp" alt="Halftone newspaper-style cutout of the four founders standing together: Dr Khangembam Shamungou, Kumam Jugeshor, Salam Prasanta and Khwairakpam Budha" style="position: absolute; left: -5%; bottom: -36px; width: 110%; height: auto; transform: translateZ(50px) rotate(1.2deg); filter: drop-shadow(0 10px 14px rgba(0,0,0,0.35))">
        </div>
      </figure>
    </section>

    <section style="max-width: 820px; margin: 0 auto; padding: 120px 24px 0; text-align: center">
      <p style="margin: 0 0 16px; font-size: 15px; font-weight: 600; color: var(--tint)">The genesis of Sangai Day</p>
      <p style="margin: 0; font-size: clamp(26px, 3vw, 36px); line-height: 1.25; font-weight: 600; letter-spacing: -0.02em">After years of informal talks about the declining ecology of Loktak Lake and Keibul Lamjao, the founders made two decisions: mark every 10 December as Sangai Day, recalling the 1954 resolution that created the Sangai sanctuary, and start a trust to carry the work forward.</p>
    </section>

    <section data-carousel="" aria-label="Our story so far" style="padding: 96px 0 0">
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px 24px; display: flex; align-items: flex-end; justify-content: space-between; gap: 16px">
        <h2 style="{H2}">The story so far</h2>
        {arrows('milestones')}
      </div>
      <div style="max-width: 1128px; margin: 0 auto">
        <ol data-track="" class="track" style="{TRACK}; list-style: none; margin: 0">
          <sc-for list="{{{{story}}}}" as="m" hint-placeholder-count="7">
            <li style="{{{{m.style}}}}">
              <p style="margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.08em; opacity: 0.8">CHAPTER {{{{m.n}}}}</p>
              <p style="margin: 0; font-size: 40px; line-height: 1.02; font-weight: 700; letter-spacing: -0.03em">{{{{m.when}}}}</p>
              <div style="flex: 1"></div>
              <h3 style="margin: 0; font-size: 21px; line-height: 1.25; font-weight: 600">{{{{m.title}}}}</h3>
              <p style="margin: 0; font-size: 15px; line-height: 1.45; opacity: 0.92">{{{{m.text}}}}</p>
            </li>
          </sc-for>
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
        <img src="{DEER}" alt="A Sangai stag in grassland" style="flex: 1 1 420px; min-width: 0; width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 28px">
        <div style="flex: 1 1 380px; min-width: 0">
          <h2 style="{H2}">Why the Sangai</h2>
          <p style="margin: 16px 0 0; color: var(--label2)">The brow-antlered deer is Manipur’s State Animal. In the wild it lives only in Keibul Lamjao, on the floating meadows of Loktak Lake.</p>
          <p style="margin: 12px 0 0; color: var(--label2)">Habitat loss, the Ithai Barrage and a small population put it at risk. That’s why we work with the next generation.</p>
          <a href="Discover.dc.html" style="display: inline-flex; align-items: center; min-height: 44px; margin-top: 8px; font-weight: 500; text-decoration: none">Discover the Sangai ›</a>
        </div>
      </div>
    </section>

    <section data-carousel="" aria-label="Trustees" style="padding: 120px 0 0">
      <div style="max-width: 1080px; margin: 0 auto; padding: 0 24px 24px; display: flex; align-items: flex-end; justify-content: space-between; gap: 16px">
        <h2 style="{H2}">Our trustees</h2>
        {arrows('trustees')}
      </div>
      <div style="max-width: 1128px; margin: 0 auto">
        <ul data-track="" class="track" style="{TRACK}; list-style: none; margin: 0">
          <sc-for list="{{{{trustees}}}}" as="t" hint-placeholder-count="4">
            <li style="flex: 0 0 260px; scroll-snap-align: start; min-height: 200px; padding: 28px; border-radius: 24px; background: var(--card); box-shadow: var(--shadow); display: flex; flex-direction: column; gap: 12px">
              <span aria-hidden="true" style="display: inline-flex; align-items: center; justify-content: center; width: 52px; height: 52px; border-radius: 999px; background: var(--tint-fill); color: var(--tint); font-weight: 700; font-size: 18px">{{{{t.initials}}}}</span>
              <div>
                <h3 style="margin: 0; font-size: 19px; line-height: 1.3; font-weight: 600">{{{{t.name}}}}</h3>
                <p style="margin: 2px 0 0; font-size: 15px; color: var(--tint); font-weight: 500">{{{{t.role}}}}</p>
                <p style="margin: 8px 0 0; font-size: 15px; color: var(--label3)">{{{{t.note}}}}</p>
              </div>
            </li>
          </sc-for>
        </ul>
      </div>
    </section>

    <section style="{SEC}; padding-bottom: 120px">
      <div style="display: flex; flex-wrap: wrap; gap: 40px; align-items: center; padding: 40px; border-radius: 28px; background: var(--card)">
        <img src="{SPEAKER}" alt="A trustee speaking to students" style="flex: 0 0 200px; width: 200px; height: 200px; object-fit: cover; border-radius: 999px">
        <div style="flex: 1 1 420px; min-width: 0">
          <h2 style="{H2}">Read about the Sangai</h2>
          <p style="margin: 12px 0 0; color: var(--label2)">We give Dr Shamungou’s books to every school we visit, among them “Sangai” (1993), “Endangered Manipur Brow-antlered Deer” (2010) and “Loktak Eidi Wareda” (2009).</p>
        </div>
      </div>
    </section>
  </main>"""
about_js = f"""{SCROLL_JS}
  renderVals() {{
    const raw = {json.dumps([dict(name=a, role=b, note=c) for a, b, c in trustees], ensure_ascii=False)};
    const trustees = raw.map((t) => {{ const p = t.name.replace('Dr ', '').split(' '); return {{ ...t, initials: p[0][0] + p[p.length - 1][0] }}; }});
    const colors = ['#5B3412', '#0F3D24', '#1F6B3A', '#0B3A53', '#1F2F5C', '#3D2A52', '#008932'];
    const story = {json.dumps(story, ensure_ascii=False)}.map((m, i) => ({{ ...m, n: i + 1,
      style: 'flex:0 0 300px;scroll-snap-align:start;display:flex;flex-direction:column;gap:12px;min-height:360px;padding:28px;border-radius:24px;color:#FFFFFF;background:' + colors[i % colors.length] }}));
    return {{ trustees, story, scrollPrev: this.scroller(-1), scrollNext: this.scroller(1) }};
  }}"""

# ---------------- CONTACT ----------------
contact_body = nav('') + f'''
  <main>
    <section style="max-width: 720px; margin: 0 auto; padding: 96px 24px 120px">
      <h1 style="margin: 0; font-size: clamp(40px, 5vw, 56px); line-height: 1.05; font-weight: 700; letter-spacing: -0.028em">Stand with the Sangai</h1>
      <p style="margin: 16px 0 40px; font-size: 20px; color: var(--label2)">To donate, host a programme at your school, or partner with us, write or call. We only use your details to reply.</p>
      <ul style="list-style: none; margin: 0; padding: 0 28px; background: var(--card); border-radius: 24px; box-shadow: var(--shadow)">
        <li style="padding: 20px 0; border-bottom: 1px solid var(--sep)"><p style="margin: 0; font-size: 13px; color: var(--label3)">Email</p><a href="mailto:sangaiff2024@gmail.com" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 19px; font-weight: 500">sangaiff2024@gmail.com</a></li>
        <li style="padding: 20px 0; border-bottom: 1px solid var(--sep)"><p style="margin: 0; font-size: 13px; color: var(--label3)">Phone</p><a href="tel:+919856177030" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 19px; font-weight: 500; margin-right: 20px">+91 98561 77030</a><a href="tel:+918014366698" style="display: inline-flex; align-items: center; min-height: 44px; font-size: 19px; font-weight: 500">+91 80143 66698</a></li>
        <li style="padding: 20px 0"><p style="margin: 0; font-size: 13px; color: var(--label3)">Address</p><p style="margin: 6px 0 0; font-size: 17px">Nambol Makha Leikai, Nambol Sub-Division<br>Bishnupur District 795134, Manipur, India</p></li>
      </ul>
      <a href="mailto:sangaiff2024@gmail.com" style="display: inline-flex; align-items: center; min-height: 50px; margin-top: 32px; padding: 0 28px; background: var(--tint); color: var(--on-tint); text-decoration: none; border-radius: 999px; font-weight: 600">Email us</a>
    </section>
  </main>'''
contact_js = '''  renderVals() { return {}; }'''


# ---------------- DISCOVER ----------------
WIKI_S = 'https://en.wikipedia.org/wiki/Sangai'
WIKI_K = 'https://en.wikipedia.org/wiki/Keibul_Lamjao_National_Park'
WIKI_L = 'https://en.wikipedia.org/wiki/Loktak_Lake'
WIKI_M = 'https://en.wikipedia.org/wiki/Manipur'
WWF = 'https://www.wwfindia.org/about_wwf/priority_species/threatened_species/brow_antlered_deer'
MT = 'https://manipurtourism.gov.in/about-us/'
dslides = [
    dict(label='The Sangai', bg='#0F3D24', img=DEER, alt='A Sangai stag with tall brow antlers in grassland',
         kicker='The dancing deer', title='Found nowhere else on Earth.',
         text='The Sangai is Manipur’s State Animal, a subspecies of Eld’s deer that lives in the wild only in Keibul Lamjao. Its name joins “sa” (animal) and “ngai” (awaiting): a running stag stops to look back.',
         chips=['Endangered · IUCN', 'Schedule I · India', 'Antlers 100–110 cm'], src='Wikipedia · WWF-India', url=WIKI_S),
    dict(label='Phumdi', bg='#0B3A53', img='', alt='',
         kicker='Loktak Lake', title='Islands that float.',
         text='Loktak, the largest freshwater lake in Northeast India, is dotted with phumdi: floating mats of plants, soil and organic matter. About a fifth of each mat rises above the water, strong enough to carry a deer.',
         chips=['~287 km² lake', 'Phumdi up to 1.2 m thick', 'Ramsar site since 1990'], src='Wikipedia', url=WIKI_L),
    dict(label='Keibul Lamjao', bg='#3E4A1E', img='', alt='',
         kicker='Keibul Lamjao National Park', title='The world’s only floating national park.',
         text='About 40 km² of floating grassland on Loktak’s southern shore, home to the last wild Sangai. The Ithai Barrage, built in 1983, keeps water high in the dry months, and the phumdi is thinning.',
         chips=['Sanctuary 1966', 'National park 1977', 'Hog deer, otters, cranes'], src='Wikipedia', url=WIKI_K),
    dict(label='Manipur', bg='#5B3412', img='', alt='',
         kicker='Manipur', title='The Land of Jewels.',
         text='The birthplace of modern polo, Sagol Kangjei, and of the Raas Lila dance. In Meitei tradition, killing a Sangai is a grave sin, and its antlered head adorns the royal boat Hiyang Hiren.',
         chips=['Polo’s birthplace', 'Raas Lila', 'Hiyang Hiren'], src='Manipur Tourism · Wikipedia', url=MT),
]
pop = [('1953', 6, 'Six found after near extinction'), ('1975', 14, 'First aerial census'), ('1995', 155, 'About 155'), ('2016', 260, 'Peak count'), ('2026', 172, 'Latest census: down by a third')]
bars = ''
for yr, n, lab in pop:
    h = max(4, round(n/260*220))
    bars += f"""
          <li style="flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 10px; text-align: center">
            <span style="font-size: 22px; font-weight: 700; letter-spacing: -0.02em">{n}</span>
            <span aria-hidden="true" style="display: block; width: 100%; max-width: 88px; height: {h}px; border-radius: 12px 12px 4px 4px; background: {'#C2410C' if yr == '2026' else 'var(--tint)'}"></span>
            <span style="font-size: 15px; font-weight: 600">{yr}</span>
            <span style="font-size: 13px; line-height: 1.3; color: var(--label3)">{lab}</span>
          </li>"""
nums = [('40 km²', 'of floating grassland in Keibul Lamjao'), ('287 km²', 'typical area of Loktak Lake'), ('1.2 m', 'the thickest phumdi'), ('100,000', 'people living around the lake')]
num_html = ''.join(f"""
        <div style="padding: 28px; border-radius: 24px; background: var(--card)">
          <p style="margin: 0; font-size: 44px; line-height: 1; font-weight: 700; letter-spacing: -0.035em">{n}</p>
          <p style="margin: 10px 0 0; font-size: 15px; color: var(--label2)">{t}</p>
        </div>""" for n, t in nums)
symbols = [('Animal', 'Sangai', 'Rucervus eldii eldii', '#0F3D24', DEER), ('Bird', 'Nongyeen', 'Mrs Hume’s pheasant', '#1F2F5C', ''), ('Flower', 'Shirui lily', 'Lilium mackliniae', '#7A2E4A', ''), ('Tree', 'Uningthou', 'Phoebe hainesiana', '#3E4A1E', ''), ('Fish', 'Pengba', 'Osteobrama belangeri', '#0B3A53', '')]
sym_html = ''
for kind, name, sci, col, img in symbols:
    bgimg = f'<img src="{img}" alt="" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0.55">' if img else ''
    sym_html += f"""
        <div style="position: relative; overflow: hidden; min-height: 220px; padding: 24px; border-radius: 24px; background: {col}; color: #FFFFFF; display: flex; flex-direction: column; justify-content: flex-end">{bgimg}
          <p style="position: relative; margin: 0; font-size: 13px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.85">State {kind}</p>
          <p style="position: relative; margin: 4px 0 0; font-size: 26px; line-height: 1.1; font-weight: 700; letter-spacing: -0.02em">{name}</p>
          <p style="position: relative; margin: 4px 0 0; font-size: 15px; font-style: italic; opacity: 0.9">{sci}</p>
        </div>"""
discover_body = nav('Discover') + f"""
  <main>
    <section style="max-width: 1080px; margin: 0 auto; padding: 72px 24px 32px">
      <h1 style="margin: 0; font-size: clamp(40px, 5vw, 56px); line-height: 1.04; font-weight: 700; letter-spacing: -0.03em">Discover the Sangai’s world</h1>
      <p style="margin: 14px 0 0; max-width: 34em; font-size: 20px; color: var(--label2)">A deer that looks back, islands that float, and the land that holds them.</p>
    </section>

    <section aria-roledescription="carousel" aria-label="Discover" style="max-width: 1080px; margin: 0 auto; padding: 0 24px">
      <div style="position: relative; min-height: 560px; border-radius: 32px; overflow: hidden">
        <sc-for list="{{{{dslides}}}}" as="s" hint-placeholder-count="1">
          <sc-if value="{{{{s.active}}}}" hint-placeholder-val="{{{{true}}}}">
            <div role="group" aria-roledescription="slide" aria-label="{{{{s.label}}}}" style="{{{{s.bgStyle}}}}">
              <sc-if value="{{{{s.hasImg}}}}" hint-placeholder-val="{{{{false}}}}">
                <img src="{{{{s.img}}}}" alt="{{{{s.alt}}}}" style="position: absolute; top: 0; right: 0; width: 62%; height: 100%; object-fit: cover; object-position: 40% 35%">
                <div aria-hidden="true" style="position: absolute; top: 0; bottom: 0; left: 38%; width: 22%; background: linear-gradient(to right, #0F3D24, rgba(15,61,36,0))"></div>
              </sc-if>
              <sc-if value="{{{{s.noImg}}}}" hint-placeholder-val="{{{{false}}}}">
                <img class="engrave-art" src="{ENGRAVE}" alt="" style="position: absolute; right: -40px; bottom: -40px; width: 420px; opacity: 0.12; filter: invert(1)">
              </sc-if>
              <div style="position: relative; max-width: 560px; padding: 56px 48px 120px; color: #FFFFFF">
                <p style="margin: 0 0 12px; font-size: 15px; font-weight: 600; opacity: 0.85">{{{{s.kicker}}}}</p>
                <h2 style="margin: 0; font-size: clamp(36px, 4.6vw, 56px); line-height: 1.04; font-weight: 700; letter-spacing: -0.03em">{{{{s.title}}}}</h2>
                <p style="margin: 18px 0 0; font-size: 18px; line-height: 1.5; opacity: 0.92">{{{{s.text}}}}</p>
                <ul style="list-style: none; margin: 22px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 8px">
                  <sc-for list="{{{{s.chips}}}}" as="c" hint-placeholder-count="3">
                    <li style="padding: 6px 14px; border-radius: 999px; background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.28); font-size: 14px; font-weight: 600">{{{{c}}}}</li>
                  </sc-for>
                </ul>
                <a href="{{{{s.url}}}}" style="display: inline-flex; align-items: center; min-height: 44px; margin-top: 10px; color: #FFFFFF; font-size: 13px; font-weight: 600; opacity: 0.85">Source: {{{{s.src}}}} ↗</a>
              </div>
            </div>
          </sc-if>
        </sc-for>
        <div style="position: absolute; left: 40px; right: 40px; bottom: 28px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px">
          <div role="tablist" aria-label="Topics" style="display: flex; flex-wrap: wrap; gap: 6px">
            <sc-for list="{{{{dslides}}}}" as="s" hint-placeholder-count="4">
              <button type="button" role="tab" aria-selected="{{{{s.current}}}}" onClick="{{{{s.go}}}}" style="{{{{s.tabStyle}}}}">{{{{s.label}}}}</button>
            </sc-for>
          </div>
          <div class="glassbar" style="display: flex; gap: 4px; padding: 4px; border-radius: 999px; background: rgba(0,0,0,0.3)">
            <button type="button" aria-label="Previous topic" onClick="{{{{prevSlide}}}}" style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border: 0; border-radius: 999px; background: transparent; color: #FFFFFF; cursor: pointer; padding: 0"><svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2L2 8l6 6"></path></svg></button>
            <button type="button" aria-label="Next topic" onClick="{{{{nextSlide}}}}" style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border: 0; border-radius: 999px; background: transparent; color: #FFFFFF; cursor: pointer; padding: 0"><svg aria-hidden="true" width="10" height="16" viewBox="0 0 10 16" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 2l6 6-6 6"></path></svg></button>
          </div>
        </div>
      </div>
    </section>

    <section style="{SEC}">
      <h2 style="{H2}">A comeback now slipping away</h2>
      <p style="margin: 8px 0 32px; max-width: 38em; color: var(--label2)">Brought back from near extinction in the 1950s, the Sangai grew to 260 by 2016. The 2026 census found only 172, as its floating home thins and deer drown where the phumdi gives way.</p>
      <div style="padding: 40px 32px 32px; border-radius: 28px; background: var(--card)">
        <ol aria-label="Sangai population by year" style="list-style: none; margin: 0; padding: 0; display: flex; align-items: flex-end; gap: 16px; min-height: 340px">{bars}
        </ol>
      </div>
      <p style="margin: 16px 8px 0; font-size: 15px; color: var(--label2)">Independent monitoring by the Wildlife Institute of India paints an even starker picture: 91 Sangai in 2006, 76 in 2019 and 64 in 2023.</p>
      <p style="margin: 8px 8px 0; font-size: 13px; color: var(--label3)">Manipur Forest Department counts. Sources: <a href="{WIKI_S}">Wikipedia</a>, <a href="https://www.easternmirrornagaland.com/hog-deer-outnumber-sangai-in-keibul-lamjao-national-park">Eastern Mirror (2026 census)</a>, <a href="https://indiawildlifenews.com/2026/06/14/sangai-manipur-eld-deer-keibul-lamjao-antlers-antelopes-part-9/">India Wildlife News (WII figures)</a>, <a href="https://www.downtoearth.org.in/wildlife-biodiversity/drowning-in-its-home">Down To Earth</a>.</p>
    </section>

    <section style="{SEC}">
      <h2 style="{H2}; margin-bottom: 24px">Loktak by the numbers</h2>
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

    <section style="{SEC}; padding-bottom: 120px; text-align: center">
      <h2 style="{H2}">Help keep these stories alive</h2>
      <p style="margin: 12px auto 28px; max-width: 30em; color: var(--label2)">Invite us to your school, or support our work for the Sangai.</p>
      <a href="Contact.dc.html" style="display: inline-flex; align-items: center; min-height: 50px; padding: 0 28px; background: var(--tint); color: var(--on-tint); text-decoration: none; border-radius: 999px; font-weight: 600">Get in touch</a>
    </section>
  </main>"""
discover_js = f"""  constructor(props) {{ super(props); this.state = {{ slide: 0 }}; }}
  renderVals() {{
    const raw = {json.dumps(dslides, ensure_ascii=False)};
    const n = raw.length, cur = this.state.slide;
    const go = (i) => this.setState({{ slide: (i + n) % n }});
    const dslides = raw.map((s, i) => ({{ ...s, active: i === cur, current: i === cur ? 'true' : 'false', go: () => go(i),
      hasImg: !!s.img, noImg: !s.img,
      bgStyle: 'position:absolute;inset:0;background:' + s.bg,
      tabStyle: 'min-height:44px;padding:0 16px;border-radius:999px;cursor:pointer;font-size:14px;font-weight:600;border:1px solid rgba(255,255,255,0.35);' + (i === cur ? 'background:#FFFFFF;color:#111111' : 'background:rgba(0,0,0,0.2);color:#FFFFFF') }}));
    return {{ dslides, prevSlide: () => go(cur - 1), nextSlide: () => go(cur + 1) }};
  }}"""

pages = [
    ('Main.dc.html', 'Sangai First Foundation', home_body, home_js, 3400, 'Home'),
    ('Discover.dc.html', 'Discover · Sangai First Foundation', discover_body, discover_js, 2900, 'Discover'),
    ('Work.dc.html', 'Our work · Sangai First Foundation', work_body, work_js, 2600, 'Our Work'),
    ('About.dc.html', 'About · Sangai First Foundation', about_body, about_js, 3400, 'About'),
    ('Contact.dc.html', 'Contact · Sangai First Foundation', contact_body, contact_js, 1200, 'Contact'),
]
boards = {}; x = 0
for fn, title, body, js, h, name in pages:
    open(os.path.join(OUT, fn), 'w').write(page(title, body, js, h))
    boards[fn] = {"x": x, "y": 0, "w": 1440, "h": h, "title": name, "expand": "fill", "is_interactive": True}
    x += 1440 + 80
c = json.load(open(os.path.join(OUT, 'canvas.json')))
c['boards'] = boards; c['order'] = [p[0] for p in pages]
json.dump(c, open(os.path.join(OUT, 'canvas.json'), 'w'), ensure_ascii=False)
print('ok')
