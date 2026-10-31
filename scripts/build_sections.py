"""Generate the animated SVG sections used by profile/README.md.

Run:  python scripts/build_sections.py
Every animation is a loop whose 0% keyframe equals the resting look, so the
artwork is complete even when a renderer freezes animations or the viewer has
prefers-reduced-motion enabled.
"""
import json
import os
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "profile", "assets", "sections")
ICON_OUT = os.path.join(ROOT, "profile", "assets", "icons")
os.makedirs(OUT, exist_ok=True)
SI = json.load(open(os.path.join(ROOT, "scripts", "simple_icons.json"), encoding="utf-8"))

FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "dark": dict(bg1="#06121A", bg2="#0B2A2E", card="#0E1F25", card2="#112A31", line="#FFFFFF", line_op=".08",
                 stroke="#19C2AE", stroke_op=".22", title="#FFFFFF", text="#D3E5E7", muted="#8FA9AD",
                 accent="#19C2AE", accent2="#7FE7D9", grid_op=".045", ink="#FFFFFF"),
    "light": dict(bg1="#F7FBFB", bg2="#E3F1EF", card="#FFFFFF", card2="#F2F8F8", line="#0B1F24", line_op=".08",
                  stroke="#0A9181", stroke_op=".22", title="#0B1F24", text="#23383D", muted="#4A6066",
                  accent="#0A9181", accent2="#0A9181", grid_op=".05", ink="#0B1F24"),
}
REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def e(s):
    return escape(s, quote=True)


def svg(w, h, body, css, t):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">
<style>
{css}
{REDUCED}
</style>
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
  <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="{t['line']}" stroke-opacity="{t['grid_op']}"/></pattern>
  <linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="{t['accent']}" stop-opacity="0"/><stop offset=".5" stop-color="{t['accent']}" stop-opacity=".16"/><stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/></linearGradient>
</defs>
{body}
</svg>
'''


def frame(w, h, t, rx=18):
    return (f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#bg)"/>'
            f'<rect width="{w}" height="{h}" rx="{rx}" fill="url(#grid)"/>')


def card(x, y, w, h, t, cls="", delay=0.0, rx=14):
    style = f' style="animation-delay:{delay:.2f}s"' if cls else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{t["card"]}" fill-opacity=".92"/>'
            f'<rect class="{cls}"{style} x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="none" '
            f'stroke="{t["stroke"]}" stroke-opacity="{t["stroke_op"]}"/>')


def write(name, content, folder=OUT):
    with open(os.path.join(folder, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)


# --------------------------------------------------------------------------- case studies
CASES = [
    ("POJEHAT", "Omnichannel AI support", "70%+", "of tier-1 queries automated", "Replies in under 1.2 s, around the clock"),
    ("DELTA", "ERP and 3D parametric engineering", "65%", "shorter drafting cycles", "Inventory variance under 0.5%"),
    ("BRICS", "Air-gapped, zero-retention RAG", "4.5x", "faster legal document review", "Full data sovereignty"),
    ("QWIRVA", "B2B sales automation · with Aghrba", "250K+", "B2B leads graded", "3.2x more qualified appointments"),
    ("SUNDIAL", "Autonomous agent infrastructure", "99.99%", "uninterrupted overnight operation", "Across multi-agent workloads"),
    ("QuranMath", "Classical Arabic NLP", "98.9%", "semantic alignment", "Across 50K+ sessions"),
    ("Masar", "Arabic-first generative AI", "10K+", "business emails generated", "RTL formatting intact"),
]


def cases(t):
    W = 1280
    gap, x0, y0, ch = 16, 24, 20, 214
    row1w = (W - 2 * x0 - 3 * gap) // 4
    row2w = (W - 2 * x0 - 2 * gap) // 3
    H = y0 + ch * 2 + gap + 20
    css = f'''
.hl{{animation:hl 9s ease-in-out infinite}}
@keyframes hl{{0%,14%,100%{{stroke-opacity:{t['stroke_op']}}}6%{{stroke-opacity:.9}}}}
.live{{transform-box:fill-box;transform-origin:center;animation:live 1.8s ease-in-out infinite}}
@keyframes live{{50%{{transform:scale(2.2);opacity:0}}}}
.prog{{transform-box:fill-box;transform-origin:left;animation:prog 9s ease-in-out infinite}}
@keyframes prog{{0%,30%,100%{{transform:none}}8%{{transform:scaleX(.05)}}}}
.sw{{animation:sw 7s ease-in-out infinite}}
@keyframes sw{{0%{{transform:translateX(-400px)}}60%,100%{{transform:translateX(1400px)}}}}'''
    rects, b = [], []
    for i, (name, dom, num, cap, sub) in enumerate(CASES):
        if i < 4:
            x, y, w = x0 + i * (row1w + gap), y0, row1w
        else:
            x, y, w = x0 + (i - 4) * (row2w + gap), y0 + ch + gap, row2w
        rects.append(f'<rect x="{x}" y="{y}" width="{w}" height="{ch}" rx="14"/>')
        d = i * 0.9
        b.append(card(x, y, w, ch, t, "hl", d))
        b.append(f'<text x="{x + 24}" y="{y + 40}" font-size="20" font-weight="700" letter-spacing="1" fill="{t["title"]}">{e(name)}</text>')
        b.append(f'<text x="{x + w - 24}" y="{y + 40}" font-size="13" font-weight="600" text-anchor="end" fill="{t["muted"]}">{i + 1:02d}</text>')
        b.append(f'<circle cx="{x + w - 54}" cy="{y + 35}" r="4" fill="{t["accent"]}"/>'
                 f'<circle class="live" style="animation-delay:{d:.2f}s" cx="{x + w - 54}" cy="{y + 35}" r="4" fill="{t["accent"]}"/>')
        b.append(f'<text x="{x + 24}" y="{y + 64}" font-size="14" fill="{t["accent"]}">{e(dom)}</text>')
        b.append(f'<text x="{x + 22}" y="{y + 126}" font-size="44" font-weight="700" fill="{t["title"]}">{e(num)}</text>')
        b.append(f'<text x="{x + 24}" y="{y + 156}" font-size="16" fill="{t["text"]}">{e(cap)}</text>')
        b.append(f'<text x="{x + 24}" y="{y + 180}" font-size="14" fill="{t["muted"]}">{e(sub)}</text>')
        b.append(f'<rect x="{x + 24}" y="{y + ch - 18}" width="{w - 48}" height="3" rx="1.5" fill="{t["accent"]}" fill-opacity=".14"/>'
                 f'<rect class="prog" style="animation-delay:{d:.2f}s" x="{x + 24}" y="{y + ch - 18}" width="{w - 48}" height="3" rx="1.5" fill="{t["accent"]}"/>')
    body = '<clipPath id="cards">' + "".join(rects) + '</clipPath>\n' + "\n".join(b)
    body += f'\n<g clip-path="url(#cards)"><rect class="sw" x="0" y="0" width="320" height="{H}" fill="url(#sheen)"/></g>'
    return svg(W, H, body, css, t)


# --------------------------------------------------------------------------- client chips
CLIENTS = [("bml", "BM", "Blue Marine Life", "bluemarinelife.qa"), ("axle", "AE", "Axle Engineering", "axleeng.net"),
           ("xyz", "XY", "XYZ Survey", "xyz-survey.com")]


def client(t, i, mono, name, tag):
    W, H = 340, 72
    css = f'''
.sw{{animation:sw 6s ease-in-out infinite;animation-delay:{i * .8:.1f}s}}
@keyframes sw{{0%{{transform:translateX(-200px)}}50%,100%{{transform:translateX(560px)}}}}
.ring{{transform-box:fill-box;transform-origin:center;animation:r 12s linear infinite}}
@keyframes r{{to{{transform:rotate(360deg)}}}}'''
    b = [f'<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="36"/></clipPath>',
         f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="36" fill="{t["card"]}"/>',
         f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="35.5" fill="none" stroke="{t["stroke"]}" stroke-opacity=".35"/>',
         f'<circle cx="37" cy="36" r="24" fill="{t["accent"]}" fill-opacity=".14"/>',
         f'<circle class="ring" cx="37" cy="36" r="27" fill="none" stroke="{t["accent"]}" stroke-width="1.5" stroke-dasharray="4 6" stroke-opacity=".6"/>',
         f'<text x="37" y="42" font-size="16" font-weight="700" text-anchor="middle" fill="{t["accent"]}">{mono}</text>',
         f'<text x="78" y="33" font-size="18" font-weight="600" fill="{t["title"]}">{e(name)}</text>',
         f'<text x="78" y="54" font-size="13" letter-spacing="1" fill="{t["muted"]}">{e(tag)}</text>',
         f'<g clip-path="url(#c)"><rect class="sw" x="0" y="0" width="140" height="{H}" fill="url(#sheen)"/></g>']
    return svg(W, H, "\n".join(b), css, t).replace('<rect width', '<rect width', 1)


# --------------------------------------------------------------------------- blueprint timeline
PHASES = [("01", "Discover", "WEEK 1", ["Assessment, top", "opportunities, KPIs", "and ROI case"]),
          ("02", "Design", "WEEKS 2–3", ["Architecture, UX,", "integrations and", "success metrics"]),
          ("03", "Build", "WEEKS 4–8", ["Agile sprints, weekly", "reviews and", "continuous testing"]),
          ("04", "Deploy", "WEEKS 9–10", ["Phased rollout,", "training and", "go-live support"]),
          ("05", "Optimize", "ONGOING", ["Usage analytics,", "iteration and", "expansion"])]


def timeline(t):
    W, H = 1280, 330
    xs = [128 + 256 * i for i in range(5)]
    ly = 76
    T = 10
    css = f'''
.comet{{animation:comet {T}s linear infinite}}
@keyframes comet{{0%{{transform:translateX(0);opacity:1}}80%{{transform:translateX(1024px);opacity:1}}84%,100%{{transform:translateX(1024px);opacity:0}}}}
.halo{{transform-box:fill-box;transform-origin:center;opacity:0;animation:halo {T}s ease-out infinite}}
@keyframes halo{{0%{{opacity:.55;transform:scale(1)}}9%{{opacity:0;transform:scale(2.1)}}100%{{opacity:0}}}}
.node{{animation:node {T}s ease-in-out infinite}}
@keyframes node{{0%,12%,100%{{fill-opacity:.12}}3%{{fill-opacity:.55}}}}
.flow{{stroke-dasharray:6 10;animation:flow 1.4s linear infinite}}
@keyframes flow{{to{{stroke-dashoffset:-16}}}}'''
    b = [frame(W, H, t)]
    b.append(f'<defs><linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["accent"]}"/></linearGradient></defs>')
    b.append(f'<line x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="{t["accent"]}" stroke-opacity=".25" stroke-width="3"/>')
    b.append(f'<line class="flow" x1="{xs[0]}" y1="{ly}" x2="{xs[-1]}" y2="{ly}" stroke="{t["accent"]}" stroke-opacity=".7" stroke-width="2"/>')
    b.append(f'<g class="comet"><rect x="{xs[0] - 90}" y="{ly - 2.5}" width="90" height="5" rx="2.5" fill="url(#cg)"/>'
             f'<circle cx="{xs[0]}" cy="{ly}" r="6" fill="{t["accent"]}"/></g>')
    for i, (num, name, weeks, lines) in enumerate(PHASES):
        x = xs[i]
        d = f"{i * T * 0.2:.2f}"
        b.append(f'<circle class="halo" style="animation-delay:{d}s" cx="{x}" cy="{ly}" r="28" fill="{t["accent"]}"/>')
        b.append(f'<circle cx="{x}" cy="{ly}" r="28" fill="{t["card"]}"/>')
        b.append(f'<circle class="node" style="animation-delay:{d}s" cx="{x}" cy="{ly}" r="28" fill="{t["accent"]}" fill-opacity=".12" stroke="{t["accent"]}" stroke-width="2"/>')
        b.append(f'<text x="{x}" y="{ly + 7}" font-size="19" font-weight="700" text-anchor="middle" fill="{t["accent"]}">{num}</text>')
        b.append(f'<text x="{x}" y="{ly + 68}" font-size="13" font-weight="600" letter-spacing="2" text-anchor="middle" fill="{t["accent"]}">{e(weeks)}</text>')
        b.append(f'<text x="{x}" y="{ly + 100}" font-size="24" font-weight="700" text-anchor="middle" fill="{t["title"]}">{e(name)}</text>')
        for j, ln in enumerate(lines):
            b.append(f'<text x="{x}" y="{ly + 132 + j * 23}" font-size="16" text-anchor="middle" fill="{t["muted"]}">{e(ln)}</text>')
    b.append(f'<text x="{W - 28}" y="{H - 18}" font-size="12" letter-spacing="2" text-anchor="end" fill="{t["muted"]}" fill-opacity=".8">J. SERVO AI BLUEPRINT™ · 90 DAYS</text>')
    return svg(W, H, "\n".join(b), css, t)


# --------------------------------------------------------------------------- standards + models
def principles(t):
    W, H = 1280, 250
    stds = ["Credibility", "Usability", "Visibility", "Sellability", "Scalability"]
    models = [("Starter", 54), ("Growth", 92), ("Transformation", 130)]
    css = f'''
.std{{animation:std 7.5s ease-in-out infinite}}
@keyframes std{{0%,18%,100%{{fill-opacity:.1;stroke-opacity:.35}}7%{{fill-opacity:.35;stroke-opacity:1}}}}
.grow{{transform-box:fill-box;transform-origin:bottom;animation:grow 7s ease-in-out infinite}}
@keyframes grow{{0%,40%,100%{{transform:none}}15%{{transform:scaleY(.2)}}}}'''
    b = [frame(W, H, t)]
    b.append(f'<line x1="640" y1="32" x2="640" y2="{H - 32}" stroke="{t["line"]}" stroke-opacity="{t["line_op"]}"/>')
    b.append(f'<text x="44" y="52" font-size="13" font-weight="600" letter-spacing="3" fill="{t["accent"]}">FIVE STANDARDS</text>')
    b.append(f'<text x="44" y="80" font-size="17" fill="{t["muted"]}">Every solution is held to all five.</text>')
    for i, s in enumerate(stds):
        cx = 92 + i * 113
        cy = 150
        hexpts = " ".join(f"{cx + 34 * __import__('math').cos(__import__('math').radians(60 * k - 90)):.1f},{cy + 34 * __import__('math').sin(__import__('math').radians(60 * k - 90)):.1f}" for k in range(6))
        b.append(f'<polygon class="std" style="animation-delay:{i * 1.5:.1f}s" points="{hexpts}" fill="{t["accent"]}" fill-opacity=".1" stroke="{t["accent"]}" stroke-opacity=".35" stroke-width="2"/>')
        b.append(f'<text x="{cx}" y="{cy + 8}" font-size="22" font-weight="700" text-anchor="middle" fill="{t["accent"]}">{s[0]}</text>')
        b.append(f'<text x="{cx}" y="{cy + 64}" font-size="15" font-weight="600" text-anchor="middle" fill="{t["title"]}">{s}</text>')
    b.append(f'<text x="684" y="52" font-size="13" font-weight="600" letter-spacing="3" fill="{t["accent"]}">THREE ENGAGEMENT MODELS</text>')
    b.append(f'<text x="684" y="80" font-size="17" fill="{t["muted"]}">Fixed deliverables · transparent pricing</text>')
    base = 200
    for i, (m, hgt) in enumerate(models):
        x = 700 + i * 180
        b.append(f'<rect x="{x}" y="{base - 140}" width="132" height="140" rx="10" fill="{t["accent"]}" fill-opacity=".05"/>')
        b.append(f'<rect class="grow" style="animation-delay:{i * .25:.2f}s" x="{x}" y="{base - hgt}" width="132" height="{hgt}" rx="10" fill="{t["accent"]}" fill-opacity="{.25 + i * .25:.2f}"/>')
        b.append(f'<text x="{x + 66}" y="{base + 28}" font-size="16" font-weight="600" text-anchor="middle" fill="{t["title"]}">{m}</text>')
    return svg(W, H, "\n".join(b), css, t)


# --------------------------------------------------------------------------- technology
STACK = [
    ("Interfaces", "Web, 3D and apps", [("Next.js", None), ("React", "61DAFB"), ("TypeScript", "3178C6"), ("three.js", None)]),
    ("Services", "APIs and runtimes", [("Node.js", "5FA04E"), ("Python", "3776AB"), ("FastAPI", "009688")]),
    ("Intelligence", "Models and retrieval", [("Claude", "D97757"), ("Gemini", "8E75B2"), ("Ollama", None), ("PyTorch", "EE4C2C"), ("Qdrant", "DC244C")]),
    ("Automation", "Workflows and channels", [("n8n", "EA4B71"), ("Twilio", "F22F46"), ("WhatsApp", "25D366")]),
]


def tech(t):
    W = 1280
    rowh, top = 86, 24
    H = top * 2 + rowh * len(STACK) - 14
    tw, tg, tx0 = 176, 14, 288
    css = f'''
.hl{{animation:hl 8s ease-in-out infinite}}
@keyframes hl{{0%,10%,100%{{stroke-opacity:{t['stroke_op']}}}4%{{stroke-opacity:.95}}}}
.ic{{transform-box:fill-box;transform-origin:center;animation:ic 8s ease-in-out infinite}}
@keyframes ic{{0%,10%,100%{{transform:none}}4%{{transform:translateY(-3px) scale(1.12)}}}}
.pk{{animation:pk 3s linear infinite}}
@keyframes pk{{from{{transform:translateX(0)}}to{{transform:translateX(64px)}}}}'''
    b = [frame(W, H, t)]
    k = 0
    for r, (layer, desc, items) in enumerate(STACK):
        y = top + r * rowh
        b.append(f'<text x="44" y="{y + 30}" font-size="19" font-weight="700" fill="{t["title"]}">{layer}</text>')
        b.append(f'<text x="44" y="{y + 52}" font-size="14" fill="{t["muted"]}">{desc}</text>')
        b.append(f'<line x1="214" y1="{y + 36}" x2="{tx0 - 10}" y2="{y + 36}" stroke="{t["accent"]}" stroke-opacity=".3" stroke-dasharray="3 5"/>')
        b.append(f'<circle class="pk" style="animation-delay:{r * .7:.1f}s" cx="214" cy="{y + 36}" r="2.5" fill="{t["accent"]}"/>')
        for j, (name, col) in enumerate(items):
            x = tx0 + j * (tw + tg)
            d = f"{k * 0.42:.2f}"
            k += 1
            color = "#" + col if col else t["ink"]
            b.append(card(x, y + 6, tw, 60, t, "hl", float(d), rx=12))
            b.append(f'<g class="ic" style="animation-delay:{d}s"><g transform="translate({x + 18} {y + 24}) scale(1)">'
                     f'<path d="{SI[name]}" fill="{color}"/></g></g>')
            b.append(f'<text x="{x + 54}" y="{y + 42}" font-size="17" font-weight="600" fill="{t["title"]}">{e(name)}</text>')
    return svg(W, H, "\n".join(b), css, t)


# --------------------------------------------------------------------------- call to action
def cta(t):
    W, H = 1280, 300
    steps = ["Review your workflows", "Rank the highest-value opportunities", "Project the ROI", "Draft your roadmap"]
    css = f'''
.ck{{animation:ck 8s ease-in-out infinite}}
@keyframes ck{{0%,14%,100%{{fill-opacity:.15}}5%{{fill-opacity:.6}}}}
.ring{{transform-box:fill-box;transform-origin:center;opacity:0;animation:ring 8s ease-out infinite}}
@keyframes ring{{0%{{opacity:.6;transform:scale(1)}}8%{{opacity:0;transform:scale(2)}}100%{{opacity:0}}}}
.radar{{transform-origin:1120px 150px;animation:spin 6s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.g{{animation:g 6s ease-in-out infinite}}
@keyframes g{{0%,100%{{opacity:.7}}50%{{opacity:1}}}}'''
    b = [frame(W, H, t, rx=20)]
    b.append(f'<defs><radialGradient id="gl" cx=".25" cy=".3" r=".6"><stop offset="0" stop-color="{t["accent"]}" stop-opacity=".22"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="rad" x1="0" x2="1"><stop offset="0" stop-color="{t["accent"]}" stop-opacity="0"/><stop offset="1" stop-color="{t["accent"]}" stop-opacity=".35"/></linearGradient></defs>')
    b.append(f'<rect class="g" width="{W}" height="{H}" rx="20" fill="url(#gl)"/>')
    for r in (40, 80, 120):
        b.append(f'<circle cx="1120" cy="150" r="{r}" fill="none" stroke="{t["accent"]}" stroke-opacity=".12"/>')
    b.append(f'<path class="radar" d="M1120 150 L1240 150 A120 120 0 0 0 1205 65 Z" fill="url(#rad)"/>')
    b.append(f'<rect x="56" y="58" width="36" height="3" fill="{t["accent"]}"/>')
    b.append(f'<text x="56" y="92" font-size="14" font-weight="600" letter-spacing="3" fill="{t["accent"]}">COMPLIMENTARY · 60–90 MINUTES</text>')
    b.append(f'<text x="54" y="148" font-size="44" font-weight="700" fill="{t["title"]}">AI Readiness Assessment</text>')
    b.append(f'<text x="56" y="186" font-size="19" fill="{t["text"]}">Find where AI pays off in your business before you invest.</text>')
    b.append(f'<rect x="56" y="214" width="232" height="46" rx="23" fill="{t["accent"]}"/>'
             f'<text x="172" y="243" font-size="16" font-weight="700" text-anchor="middle" fill="{t["card"]}">Book an assessment  →</text>')
    for i, s in enumerate(steps):
        y = 82 + i * 50
        d = f"{i * 1.2:.1f}"
        b.append(f'<circle class="ring" style="animation-delay:{d}s" cx="694" cy="{y}" r="14" fill="{t["accent"]}"/>')
        b.append(f'<circle class="ck" style="animation-delay:{d}s" cx="694" cy="{y}" r="14" fill="{t["accent"]}" fill-opacity=".15" stroke="{t["accent"]}" stroke-width="1.5"/>')
        b.append(f'<path d="M687 {y} l5 5 l9 -10" fill="none" stroke="{t["accent"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        b.append(f'<text x="722" y="{y + 6}" font-size="18" fill="{t["title"]}">{e(s)}</text>')
    return svg(W, H, "\n".join(b), css, t)


# --------------------------------------------------------------------------- footer
def footer(t):
    W, H = 1280, 120
    css = '''
.wave{animation:wave 8s linear infinite}
@keyframes wave{to{transform:translateX(-160px)}}
.dot{transform-box:fill-box;transform-origin:center;animation:d 2s ease-in-out infinite}
@keyframes d{50%{transform:scale(1.8);opacity:.3}}'''
    wave = "M-160 30 " + " ".join(f"q40 -18 80 0 t80 0" for _ in range(10))
    b = [f'<clipPath id="c"><rect width="{W}" height="{H}"/></clipPath>',
         f'<g clip-path="url(#c)"><path class="wave" d="{wave}" fill="none" stroke="{t["accent"]}" stroke-opacity=".45" stroke-width="2"/>'
         f'<path class="wave" style="animation-duration:12s" d="{wave}" transform="translate(0 10)" fill="none" stroke="{t["accent"]}" stroke-opacity=".18" stroke-width="2"/></g>',
         f'<text x="640" y="84" font-size="26" font-weight="700" letter-spacing="3" text-anchor="middle" fill="{t["title"]}">J. SERVO</text>',
         f'<circle class="dot" cx="526" cy="76" r="4" fill="{t["accent"]}"/><circle class="dot" style="animation-delay:1s" cx="754" cy="76" r="4" fill="{t["accent"]}"/>',
         f'<text x="640" y="108" font-size="14" letter-spacing="1" text-anchor="middle" fill="{t["muted"]}">Your AI Partner in Business · Cairo, Egypt · Serving Egypt and the GCC</text>']
    return svg(W, H, "\n".join(b), css, t)


# --------------------------------------------------------------------------- product icons (single file, works on both themes)
def product_icon(body, css):
    c = "#14B8A6"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="56" height="56" viewBox="0 0 56 56">
<style>
  .s{{fill:none;stroke:{c};stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
  .f{{fill:{c}}}
  {css}
  {REDUCED}
</style>
<rect x="1" y="1" width="54" height="54" rx="14" fill="{c}" fill-opacity=".12" stroke="{c}" stroke-opacity=".35"/>
{body}
</svg>
'''


PRODUCT_ICONS = {
    "dragonfly": ('<path class="s fl" d="M17 19 C24 19 24 28 28 28 C32 28 32 19 39 19 M17 37 C24 37 24 28 28 28 C32 28 32 37 39 37"/>'
                  '<rect class="s" x="11" y="15" width="8" height="8" rx="2"/><rect class="s" x="11" y="33" width="8" height="8" rx="2"/>'
                  '<rect class="s" x="37" y="15" width="8" height="8" rx="2"/><rect class="s" x="37" y="33" width="8" height="8" rx="2"/>'
                  '<circle class="f p" cx="28" cy="28" r="3.5"/>',
                  ".fl{stroke-dasharray:4 4;animation:fl 1.2s linear infinite}@keyframes fl{to{stroke-dashoffset:-8}}"
                  ".p{transform-box:fill-box;transform-origin:center;animation:p 1.6s ease-in-out infinite}@keyframes p{50%{transform:scale(1.5);opacity:.6}}"),
    "roi": ('<path class="s" d="M13 42 H43"/>'
            '<rect class="f b" x="15" y="32" width="6" height="8" rx="1.5"/><rect class="f b" style="animation-delay:.15s" x="25" y="26" width="6" height="14" rx="1.5"/>'
            '<rect class="f b" style="animation-delay:.3s" x="35" y="20" width="6" height="20" rx="1.5"/>'
            '<path class="s ar" d="M14 24 L24 18 L30 21 L41 13 M36 13 H41 V18"/>',
            ".b{transform-box:fill-box;transform-origin:bottom;animation:b 4s ease-in-out infinite}@keyframes b{0%,40%,100%{transform:none}15%{transform:scaleY(.3)}}"
            ".ar{stroke-dasharray:44;animation:ar 4s ease-in-out infinite}@keyframes ar{0%,45%,100%{stroke-dashoffset:0}18%{stroke-dashoffset:44}}"),
    "masar": ('<rect class="s" x="11" y="15" width="34" height="26" rx="4"/>'
              '<path class="s l1" d="M39 23 H19"/><path class="s l2" d="M39 29 H23"/><path class="s l3" d="M39 35 H27"/>',
              ".l1,.l2,.l3{stroke-dasharray:22;animation:ty 4s ease-in-out infinite}.l2{animation-delay:.3s}.l3{animation-delay:.6s}"
              "@keyframes ty{0%,45%,100%{stroke-dashoffset:0}20%{stroke-dashoffset:-22}}"),
    "studio": ('<path class="s" d="M28 12 C18 12 12 19 12 27 C12 36 19 44 27 44 C31 44 31 40 29 38 C27 36 28 33 32 33 H37 C41 33 44 30 44 26 C44 18 37 12 28 12 Z"/>'
               '<circle class="c1" cx="21" cy="25" r="3"/><circle class="c2" cx="28" cy="19" r="3"/><circle class="c3" cx="36" cy="22" r="3"/>',
               ".c1,.c2,.c3{animation:hue 6s linear infinite}.c1{fill:#14B8A6}.c2{fill:#F59E0B;animation-delay:-2s}.c3{fill:#EC4899;animation-delay:-4s}"
               "@keyframes hue{0%,100%{fill:#14B8A6}33%{fill:#F59E0B}66%{fill:#EC4899}}"),
    "tools": ('<circle class="s" cx="25" cy="25" r="10"/><path class="s" d="M32.5 32.5 L43 43"/>'
              '<path class="f sp" d="M25 19 L26.4 23.6 L31 25 L26.4 26.4 L25 31 L23.6 26.4 L19 25 L23.6 23.6 Z"/>',
              ".sp{transform-box:fill-box;transform-origin:center;animation:sp 4s ease-in-out infinite}@keyframes sp{0%,60%,100%{transform:none}30%{transform:rotate(90deg) scale(.6)}}"),
}


def main():
    for mode, t in THEMES.items():
        write(f"cases-{mode}.svg", cases(t))
        write(f"blueprint-{mode}.svg", timeline(t))
        write(f"principles-{mode}.svg", principles(t))
        write(f"tech-{mode}.svg", tech(t))
        write(f"cta-{mode}.svg", cta(t))
        write(f"footer-{mode}.svg", footer(t))
        for i, (slug, mono, name, tag) in enumerate(CLIENTS):
            write(f"client-{slug}-{mode}.svg", client(t, i, mono, name, tag))
    for n, (body, css) in PRODUCT_ICONS.items():
        write(f"{n}.svg", product_icon(body, css), ICON_OUT)
    print("written to", OUT)


if __name__ == "__main__":
    main()
