"""Generates the light and dark SVG panels for the profile README.

Run: python3 assets/build.py   (writes assets/*.svg and assets/dark/*.svg)
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent
W = 1000

PALETTES = {
    "light": dict(ink="#1F2328", muted="#59636E", dim="#8C959F", rule="#D0D7DE",
                  accent="#B35900", ghost="#E6E9ED", glow="#FFE8CC"),
    "dark":  dict(ink="#E6EDF3", muted="#9198A1", dim="#6E7681", rule="#30363D",
                  accent="#F0A35E", ghost="#21262D", glow="#3D2A14"),
}

CSS = """
.mono{font-family:ui-monospace,"SFMono-Regular","SF Mono",Menlo,Consolas,"Liberation Mono",monospace}
.draw{stroke-dasharray:1000;stroke-dashoffset:1000;animation:draw 1.4s cubic-bezier(.6,0,.2,1) forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.rise{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.fade{opacity:0;animation:fade .7s ease forwards}
@keyframes fade{to{opacity:1}}
.rot{opacity:0;animation:rot 12s linear infinite}
@keyframes rot{0%{opacity:0}2%{opacity:1}23%{opacity:1}25%{opacity:0}100%{opacity:0}}
.blink{animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.pulse{transform-origin:center;transform-box:fill-box;animation:pulse 2.2s ease-out infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.9}100%{transform:scale(3.2);opacity:0}}
@media (prefers-reduced-motion:reduce){
  .draw,.rise,.fade,.rot,.blink,.pulse{animation:none}
  .draw{stroke-dashoffset:0}.rise,.fade{opacity:1}.rot{opacity:0}.rot.r0{opacity:1}
}
"""


def delay(i, step=0.15, base=0.1):
    return f'style="animation-delay:{base + i * step:.2f}s"'


def svg(h, body, label, p):
    return (f'<svg viewBox="0 0 {W} {h}" width="{W}" height="{h}" fill="none" '
            f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(label)}">\n'
            f'<style>{CSS}</style>\n{body}\n</svg>\n')


def t(x, y, s, size, fill, extra="", cls="mono", anchor=None, ls=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    l = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{fill}"{a}{l} {extra}>'
            f'{escape(s)}</text>')


# ---------------------------------------------------------------- panels

def header(p):
    focus = [
        "backend systems · AI infrastructure · developer tools",
        "idea → production → keeps it running",
        "4 hackathon wins · $25K+ in prizes and credits",
        "1 of 43 builders · IIMA Ventures AI Residency",
    ]
    rot = "".join(
        f'<g class="rot r{i}" style="animation-delay:{1.6 + i * 3:.1f}s">'
        + t(140, 286, s, 14, p["accent"], ls="0.5") + "</g>"
        for i, s in enumerate(focus))
    body = f"""
<line class="draw" x1="48" y1="58" x2="952" y2="58" stroke="{p['rule']}"/>
<g class="fade" {delay(0)}>
  {t(48, 42, "README — SAISHKORGAONKAR", 11, p['dim'], ls="3.5")}
  {t(952, 42, "MUMBAI, IN — 19.07° N", 11, p['dim'], anchor="end", ls="3.5")}
</g>
<g class="rise" {delay(2)}>{t(44, 168, "Saish Korgaonkar", 72, p['ink'], ls="-2")}</g>
<g class="fade" {delay(4)}>{t(48, 210, "Software engineer. Final-year Computer Engineering, K. J. Somaiya.", 18, p['muted'])}</g>
<g class="fade" {delay(6)}>
  {t(48, 286, "focus  ▸", 12.5, p['dim'], ls="1")}
  {rot}
</g>
<g class="fade" {delay(8)}>
  {t(48, 332, "$ whoami --short", 13, p['dim'])}
  <rect class="blink" x="186" y="321" width="8" height="15" fill="{p['accent']}"/>
</g>
<line class="draw" x1="48" y1="370" x2="952" y2="370" stroke="{p['rule']}" style="animation-delay:.6s"/>
"""
    return svg(390, body, "Saish Korgaonkar, software engineer", p)


def section(n, title, path):
    def make(p):
        body = f"""
<g class="fade">
  {t(48, 68, f"{n:02d}", 52, p['ghost'])}
  {t(128, 58, title.upper(), 14, p['accent'], ls="6")}
  {t(952, 58, path, 11, p['dim'], anchor="end", ls="2")}
</g>
<line class="draw" x1="{140 + len(title) * 14.4:.0f}" y1="53" x2="{946 - len(path) * 8.6:.0f}" y2="53" stroke="{p['rule']}"/>
"""
        return svg(90, body, f"{n:02d} — {title}", p)
    return make


def whoami(p):
    rows = [
        ("MINDSET", "High agency. I own problems end to end and don't wait for the next ticket.", "ink"),
        ("BUILD", "Hand me a rough idea and I'll take it to production, then keep it running.", "ink"),
        ("PROOF", "Won Monad Blitz solo in 6 hours after my team dropped out the night before.", "ink"),
        ("WORKFLOW", "I build with AI agents every day and review every line they write.", "ink"),
        ("NOW", "SWE Intern @ Not Your Idea · open to full-time roles from January 2027", "accent"),
    ]
    out = [
        f'<g class="rise" {delay(0)}>' + t(48, 34, "I build backend systems, AI infrastructure and developer tools,", 16, p['ink']) + "</g>",
        f'<g class="rise" {delay(1)}>' + t(48, 62, "and I care about what happens after the demo: uptime, evals, security, the boring parts.", 15, p['muted']) + "</g>",
        f'<line class="draw" x1="48" y1="92" x2="952" y2="92" stroke="{p["rule"]}"/>',
    ]
    for i, (k, v, c) in enumerate(rows):
        y = 128 + i * 34
        out.append(f'<g class="rise" {delay(i + 2)}>' + t(48, y, k, 11, p['dim'], ls="2.5")
                   + t(170, y, v, 15, p[c]) + "</g>")
    return svg(128 + 4 * 34 + 26, "\n".join(out), "About Saish", p)


def experience(p):
    jobs = [
        ("2026 —", "Not Your Idea · Software Engineering Intern", [
            "production services in Elixir, Phoenix and Ash on PostgreSQL, deployed on Fly.io",
            "auth, transactional write paths, LLM tracing and evals · React 19 + TanStack frontend",
        ]),
        ("2026", "IIMA Ventures · AI Summer Resident · Ahmedabad", [
            "selected as 1 of 43 builders from 11,000+ applicants",
            "built a creator second brain and reel video analysis with a startup team",
        ]),
        ("2025–26", "Commtel Networks · Machine Learning Intern", [
            "distributed edge monitoring with local LLMs, anomaly detection and alerting",
            "MCP servers for agentic workflows",
        ]),
        ("2025", "DCB Bank · Business Intelligence Intern", [
            "serverless RAG and OCR pipelines on AWS Lambda, S3 and Textract",
            "fixed cold-start latency in a production inference path",
        ]),
        ("— 2027", "K. J. Somaiya College of Engineering · B.Tech Computer Engineering", [
            "CGPA 9.64 · Honours in Data Science and Analytics",
        ]),
    ]
    out, y = [], 36
    top = y - 18
    for i, (when, title, lines) in enumerate(jobs):
        g = [t(48, y, when, 12, p['accent'], ls="1.5"),
             f'<circle cx="150" cy="{y - 4}" r="4" fill="{p["accent"] if i == 0 else p["rule"]}"/>',
             t(172, y, title, 15, p['ink'])]
        if i == 0:
            g.insert(1, f'<circle class="pulse" cx="150" cy="{y - 4}" r="4" fill="{p["accent"]}"/>')
        for j, line in enumerate(lines):
            g.append(t(172, y + 26 + j * 22, line, 14, p['muted']))
        out.append(f'<g class="rise" {delay(i)}>' + "".join(g) + "</g>")
        last = y
        y += 26 + len(lines) * 22 + 30
    out.insert(0, f'<line x1="150" y1="{top}" x2="150" y2="{last}" stroke="{p["rule"]}"/>')
    return svg(y - 22, "\n".join(out), "Experience", p)


def wins(p):
    stats = [("4", "hackathon wins"), ("$25K+", "prizes and credits"),
             ("1 of 43", "IIMA Ventures"), ("1 of 83", "ACM Winter School")]
    out = []
    cw = 904 / 4
    for i, (big, small) in enumerate(stats):
        x = 48 + i * cw
        out.append(f'<g class="rise" {delay(i)}>'
                   + f'<rect x="{x:.0f}" y="12" width="{cw - 14:.0f}" height="88" rx="6" fill="{p["glow"]}" opacity=".55"/>'
                   + t(x + 18, 58, big, 30, p['accent'])
                   + t(x + 18, 84, small.upper(), 10.5, p['muted'], ls="2") + "</g>")
    rows = [
        ("1ST", "Monad Blitz Mumbai", "built solo in 6 hours · Monad Foundation grant"),
        ("2ND", "BNB Chain × YZi Labs Hack Series", "$3,000 · fast-track to YZi Labs EASY Residency"),
        ("PRIZE", "ETHOnline 2025", "Blockscout · Best Use of Autoscout"),
        ("2ND", "GDG TechSprint Pune", "RAG study assistant on Vertex AI"),
        ("SEL", "ACM India Winter School, IIIT Hyderabad", "AI and Finance · 1 of 83"),
        ("SEL", "YC Startup School India", "Bengaluru, 2026"),
        ("OSS", "microsoft/highlight-summarize", "fix merged · PR #27"),
    ]
    for i, (tag, what, note) in enumerate(rows):
        y = 148 + i * 34
        out.append(f'<g class="rise" {delay(i + 4, 0.1)}>'
                   + f'<rect x="48" y="{y - 15}" width="58" height="21" rx="3" fill="none" stroke="{p["accent"]}"/>'
                   + t(77, y, tag, 10.5, p['accent'], anchor="middle", ls="1.5")
                   + t(124, y, what, 15, p['ink'])
                   + t(952, y, note, 13, p['muted'], anchor="end") + "</g>")
    return svg(148 + 6 * 34 + 26, "\n".join(out), "Wins and recognition", p)


def community(p):
    rows = [
        ("AWS Student Builder Group, KJSCE", "founded the first chapter · 500+ developers"),
        ("Computer Society of India, KJSCE", "Joint General Secretary · 1,000+ members"),
        ("Perplexity", "campus ambassador"),
    ]
    out = []
    for i, (who, what) in enumerate(rows):
        y = 34 + i * 34
        out.append(f'<g class="rise" {delay(i)}>' + t(48, y, "▸", 14, p['accent'])
                   + t(72, y, who, 15, p['ink']) + t(952, y, what, 13, p['muted'], anchor="end") + "</g>")
    return svg(34 + 2 * 34 + 26, "\n".join(out), "Community", p)


def stack(p):
    rows = [
        ("LANGUAGES", "TypeScript · Python · Go · Elixir · Java · C++ · Solidity · SQL"),
        ("BACKEND", "Phoenix · Ash · Node.js · PostgreSQL · Redis · REST · WebSockets"),
        ("AI", "RAG · agents · MCP · LangChain · local LLMs · evals and tracing"),
        ("INFRA", "Docker · AWS · GCP · Fly.io · Vercel · Cloudflare · CI/CD"),
        ("WEB3", "Circom · Groth16 · ERC-4337 · Hardhat · Foundry"),
    ]
    out = []
    for i, (k, v) in enumerate(rows):
        y = 34 + i * 36
        out.append(f'<g class="rise" {delay(i)}>' + t(48, y, k, 11, p['dim'], ls="2.5")
                   + t(190, y, v, 15, p['ink']) + "</g>")
        if i < len(rows) - 1:
            out.append(f'<line x1="48" y1="{y + 15}" x2="952" y2="{y + 15}" stroke="{p["rule"]}" opacity=".5"/>')
    return svg(34 + 4 * 36 + 24, "\n".join(out), "Stack", p)


def footer(p):
    body = f"""
<line class="draw" x1="48" y1="24" x2="952" y2="24" stroke="{p['rule']}"/>
<circle class="pulse" cx="60" cy="64" r="4" fill="{p['accent']}"/>
<circle cx="60" cy="64" r="4" fill="{p['accent']}"/>
{t(82, 62, "STATUS — SHIPPING", 12, p['ink'], ls="3")}
{t(82, 82, "open to SWE roles from January 2027 · Mumbai · Bengaluru · remote", 11, p['muted'], ls="1")}
{t(952, 70, "saish.xyz  ·  Mumbai, IN", 14, p['muted'], anchor="end")}
"""
    return svg(104, body, "Current status", p)


PANELS = {
    "header": header,
    "s01": section(1, "whoami", "~/01-whoami"), "whoami": whoami,
    "s02": section(2, "experience", "~/02-route"), "experience": experience,
    "s03": section(3, "wins", "~/03-wins"), "wins": wins,
    "s04": section(4, "community", "~/04-community"), "community": community,
    "s05": section(5, "stack", "~/05-stack"), "stack": stack,
    "s06": section(6, "telemetry", "~/06-telemetry"),
    "footer": footer,
}

if __name__ == "__main__":
    (ROOT / "dark").mkdir(exist_ok=True)
    for mode, p in PALETTES.items():
        out = ROOT if mode == "light" else ROOT / "dark"
        for name, fn in PANELS.items():
            (out / f"{name}.svg").write_text(fn(p))
    print("wrote", len(PANELS) * 2, "files")
