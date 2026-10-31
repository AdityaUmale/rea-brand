#!/usr/bin/env python3
"""Build the one-file rea-brand report (brand.html) from brand.md.

Usage: python3 build_report.py rea-brand/<person>/brand.md [--out brand.html]

Needs the `markdown` package (pip install markdown). Pillow is optional: with it,
contact sheets are downscaled before they are inlined.

Conventions read from brand.md:
- `# Title` on the first line; the first paragraph under it is the meta line.
- ```stats      one tile per line: VALUE | label | SEEN or INFERRED | source (last two optional)
- ```chart      `point YYYY-MM VALUE LABEL`, `pin YYYY-MM text`, `caption text`
- ```prompt     a paste-ready prompt, rendered with a copy button
- A `### Heading` whose slug matches <platform>/img/sheet_<slug>_top.jpg (and
  _bottom.jpg) next to brand.md gets those contact sheets inserted under it.
- SEEN / INFERRED in running text become evidence pills.
"""
import argparse
import base64
import html
import io
import json
import math
import re
from pathlib import Path

import markdown

try:
    from PIL import Image
except ImportError:  # Pillow is optional
    Image = None

REPO_URL = "https://github.com/AdityaUmale/rea-brand"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def link_attrs(href):
    """External links open in a new tab; in-page anchors do not."""
    return ' target="_blank" rel="noopener"' if href.startswith("http") else ""


def month_index(date):
    """'YYYY-MM...' to a running month count."""
    return int(date[:4]) * 12 + int(date[5:7]) - 1


def inline_image(path, width=1400):
    if Image is None:
        data = path.read_bytes()
    else:
        im = Image.open(path).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=78)
        data = buf.getvalue()
    return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"


PLATFORM_NAMES = {"x": "X", "instagram": "Instagram", "youtube": "YouTube", "youtube shorts": "YouTube Shorts",
                  "linkedin": "LinkedIn", "threads": "Threads", "substack": "Substack", "tiktok": "TikTok",
                  "facebook": "Facebook", "reddit": "Reddit", "bluesky": "Bluesky", "medium": "Medium",
                  "pinterest": "Pinterest"}


def render_stats(block):
    """One tile per line: VALUE | label | SEEN or INFERRED | link (URL or #anchor). Last two optional."""
    tiles = []
    for line in block.strip().splitlines():
        parts = [p.strip() for p in line.split("|")] + ["", ""]
        if not parts[1]:
            continue
        value, label, tag, link = parts[:4]
        inner = (f'<div class="stat-value">{html.escape(value)}</div>'
                 f'<div class="stat-label">{html.escape(label)}</div>' + (pill(tag) if tag else ""))
        if link:
            tiles.append(f'<a class="stat" href="{html.escape(link)}"{link_attrs(link)} aria-label="{html.escape(value + ", " + label + ", see the source")}">{inner}</a>')
        else:
            tiles.append(f'<div class="stat">{inner}</div>')
    return f'<div class="stats">{"".join(tiles)}</div>'


def numeric_columns(table):
    """Right-align columns whose cells start with a number (dates excluded)."""
    rows = re.findall(r"<tr>(.*?)</tr>", table, flags=re.S)
    if len(rows) < 3:
        return table
    cells = [re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S) for r in rows[1:]]
    width = max(len(c) for c in cells)
    numeric = set()
    for col in range(1, width):
        vals = [re.sub(r"<[^>]+>", "", c[col]).strip() for c in cells if col < len(c)]
        vals = [v for v in vals if v and v not in ("—", "-")]
        hits = [v for v in vals if re.fullmatch(r"[\$~≈]?\d[\d,.]*\s?(%|×|x|K|M|B|¢)?", v)]
        if len(vals) >= 2 and len(hits) == len(vals):
            numeric.add(col)
    if not numeric:
        return table

    def mark_row(row):
        i = -1

        def cell(m):
            nonlocal i
            i += 1
            return f'<{m.group(1)} class="num">' if i in numeric else m.group(0)
        return re.sub(r"<(t[hd])(?: [^>]*)?>", cell, row)
    return re.sub(r"<tr>(.*?)</tr>", lambda m: "<tr>" + mark_row(m.group(1)) + "</tr>", table, flags=re.S)


def short_version(chunk):
    """Split each '**Lead.** detail' item into a standalone lead line and its detail."""
    def item(m):
        body = m.group(1).strip()
        lead = re.match(r"<strong>(.*?)</strong>\s*(.*)", body, flags=re.S)
        if not lead:
            return m.group(0)
        return f'<li><p class="lead">{lead.group(1)}</p><p class="detail">{lead.group(2)}</p></li>'
    return re.sub(r"<li>(.*?)</li>", item, chunk, flags=re.S)


def sheet_key(sidecar):
    """Linked rank and engagement row read from sheet_<platform>_<tier>.json, when present."""
    if not sidecar.exists():
        return ""
    entries = []
    for e in json.loads(sidecar.read_text()):
        text = f'#{e["rank"]} {int(e["engagement"]):,}'
        url = e.get("url")
        entries.append(f'<li><a href="{html.escape(url)}" target="_blank" rel="noopener">{text}</a></li>' if url else f"<li>{text}</li>")
    return f'<ol class="sheet-key" aria-label="Engagement of each post, in sheet order">{"".join(entries)}</ol>'


def parse_chart(block):
    points, pins, caption = [], [], ""
    for line in block.strip().splitlines():
        kind, _, rest = line.strip().partition(" ")
        if kind == "point":
            date, value, label = rest.split(" ", 2)
            points.append((date, float(value), label))
        elif kind == "pin":
            date, text = rest.split(" ", 1)
            pins.append((date, text))
        elif kind == "caption":
            caption = rest
    return points, pins, caption


def chart_svg(points, pins, caption, compact):
    """Log-scale line chart. compact=True is the phone version: pins become numbered markers."""
    months = [month_index(d) for d, *_ in points] + [month_index(d) for d, _ in pins]
    first_year, last_year = min(months) // 12, max(months) // 12 + 1
    W, H, L, R, T, B = (340, 260, 40, 46, 30, 34) if compact else (880, 340, 64, 72, 36, 44)
    lo = 10 ** math.floor(math.log10(min(v for _, v, _ in points)))
    hi = 10 ** math.ceil(math.log10(max(v for _, v, _ in points)))

    def x(date):
        return L + (month_index(date) - first_year * 12) / ((last_year - first_year) * 12) * (W - L - R)

    def y(v):
        return T + (1 - (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))) * (H - T - B)

    def short(v):
        if v >= 1e6:
            return f"{v / 1e6:g}M"
        if v >= 1e3:
            return f"{v / 1e3:g}K"
        return f"{v:g}"

    parts = []
    tick = lo
    while tick <= hi:
        parts.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y(tick):.1f}" y2="{y(tick):.1f}"/>'
                     f'<text class="axis" x="{L - 8}" y="{y(tick) + 4:.1f}" text-anchor="end">{short(tick)}</text>')
        tick *= 10
    step = 2 if compact and last_year - first_year > 5 else 1
    for yr in range(first_year, last_year + 1, step):
        parts.append(f'<text class="axis" x="{x(f"{yr}-01"):.1f}" y="{H - 12}" text-anchor="middle">{yr}</text>')
    for i, (date, text) in enumerate(pins):
        px = x(date)
        parts.append(f'<line class="pin" x1="{px:.1f}" x2="{px:.1f}" y1="{T - 10}" y2="{H - B}"/>')
        if compact:
            parts.append(f'<circle class="pin-badge" cx="{px:.1f}" cy="{T - 14}" r="8"/>'
                         f'<text class="pin-num" x="{px:.1f}" y="{T - 10.5}" text-anchor="middle">{i + 1}</text>')
        else:
            anchor, dx = ("end", -6) if px > W - R - 160 else ("start", 6)
            parts.append(f'<text class="pin-label" x="{px + dx:.1f}" y="{T - 14 + (i % 2) * 16 + 8}" text-anchor="{anchor}">{html.escape(text)}</text>')
    path = " ".join(f"{x(d):.1f},{y(v):.1f}" for d, v, _ in points)
    parts.append(f'<polyline class="line" points="{path}"/>')
    last_labeled = None
    for i, (d, v, label) in enumerate(points):
        last = i == len(points) - 1
        parts.append(f'<circle class="dot" cx="{x(d):.1f}" cy="{y(v):.1f}" r="{3.5 if compact else 4.5}"/>')
        if compact and not last and last_labeled is not None and x(d) - last_labeled < 30:
            continue
        if last and compact:
            tx, ty, anchor = x(d) - 6, y(v) - 10, "end"
        elif last:
            tx, ty, anchor = x(d) + 10, y(v) + 4, "start"
        elif i == 0:
            tx, ty, anchor = x(d) + 8, y(v) + 16, "start"
        else:
            tx, ty, anchor = x(d) - 7, y(v) - 8, "end"
        last_labeled = x(d)
        parts.append(f'<text class="point-label" x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}">{html.escape(label)}</text>')
    cls = "chart-narrow" if compact else "chart-wide"
    return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(caption or "Growth chart")}">'
            + "".join(parts) + "</svg>")


def render_chart(block):
    points, pins, caption = parse_chart(block)
    if not points:
        return ""
    legend = ""
    if pins:
        items = "".join(f'<li><span class="pin-key">{i + 1}</span>{html.escape(t)} '
                        f'<span class="pin-date">{MONTHS[int(d[5:7]) - 1]} {d[:4]}</span></li>' for i, (d, t) in enumerate(pins))
        legend = f'<ol class="chart-legend">{items}</ol>'
    cap = f"<figcaption>{html.escape(caption)}</figcaption>" if caption else ""
    return (f'<figure class="chart">{chart_svg(points, pins, caption, False)}'
            f'{chart_svg(points, pins, caption, True)}{legend}{cap}</figure>')


def render_prompt(block):
    return ('<div class="prompt"><div class="prompt-head"><span>Prompt</span>'
            '<button class="copy" type="button" aria-label="Copy the prompt">'
            '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="5" y="5" width="8.5" height="8.5" rx="1.5"/>'
            '<path d="M10.5 2.5h-6a2 2 0 0 0-2 2v6"/></svg><span>Copy the prompt</span></button></div>'
            f'<pre><code>{html.escape(block.strip())}</code></pre></div>')


def pill(word):
    word = word.strip()
    kind = "seen" if word.upper().startswith("SEEN") else "inferred"
    return f'<span class="pill pill-{kind}">{html.escape(word)}</span>'


EVIDENCE = re.compile(r"\((?:SEEN|INFERRED)(?:, self-reported)? (?:#[\w-]+|https?://[^\s)]+)\)|\(SEEN, self-reported\)|SEEN,? \(?self-reported\)?|\((?:SEEN|INFERRED)\)|\((?:SEEN|INFERRED)\b|\b(?:SEEN|INFERRED)\b")


def evidence_repl(m):
    found = m.group(0)
    linked = re.fullmatch(r"\((SEEN|INFERRED)(, self-reported)? (#[\w-]+|https?://[^\s)]+)\)", found)
    if linked:
        word = linked.group(1) + (" · self-reported" if linked.group(2) else "")
        href = linked.group(3)
        kind = "seen" if word.startswith("SEEN") else "inferred"
        return f'<a class="pill pill-{kind} pill-link" href="{html.escape(href)}"{link_attrs(href)}>{html.escape(word)}</a>'
    if "self-reported" in found:
        return pill("SEEN · self-reported")
    if found.startswith("(") and not found.endswith(")"):
        return '<span class="nowrap">(' + pill(found[1:]) + "</span>"
    return pill(found.strip("()"))


def evidence_pills(fragment):
    # only touch text outside tags, and never inside pre/code
    out, depth, in_pill = [], 0, False
    for token in re.split(r"(<[^>]+>)", fragment):
        if token.startswith("<"):
            in_pill = token.startswith('<span class="pill') or token.startswith('<a class="pill')
            if re.match(r"<(pre|code)\b", token):
                depth += 1
            elif re.match(r"</(pre|code)>", token):
                depth -= 1
            out.append(token)
        elif depth == 0 and not in_pill:
            out.append(EVIDENCE.sub(evidence_repl, token))
        else:
            out.append(token)
    return "".join(out)


def build(md_path, out_path):
    base = md_path.parent
    text = md_path.read_text()
    blocks = {}

    def stash(kind, renderer):
        def sub(m):
            key = f"@@{kind.upper()}{len(blocks)}@@"
            blocks[key] = renderer(m.group(1))
            return f"\n\n{key}\n\n"
        return sub

    for kind, renderer in (("stats", render_stats), ("chart", render_chart), ("prompt", render_prompt)):
        text = re.sub(rf"```{kind}\n(.*?)```", stash(kind, renderer), text, flags=re.S)

    title_match = re.match(r"#\s+(.+)\n+(.+?)\n\n", text)
    title = title_match.group(1).strip() if title_match else md_path.stem
    meta = title_match.group(2).strip() if title_match else ""
    if title_match:
        text = text[title_match.end():]
    person = title.split(":")[0].strip()

    body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    for key, rendered in blocks.items():
        body = body.replace(f"<p>{key}</p>", rendered)
    body = evidence_pills(body)
    body = re.sub(r"<table>.*?</table>", lambda m: '<div class="table-wrap">' + numeric_columns(m.group(0)) + "</div>",
                  body, flags=re.S)
    body = re.sub(r'<a href="(http[^"]+)"', r'<a href="\1" target="_blank" rel="noopener"', body)

    # contact sheets under platform headings; every h3 gets an id so tiles can link to it
    def add_sheets(m):
        heading = m.group(1)
        slug = slugify(re.sub(r"<[^>]+>", "", heading))
        figs = []
        for top in sorted(base.glob(f"*/img/sheet_{slug}*_top.jpg")):
            bottom = top.with_name(top.name.replace("_top.jpg", "_bottom.jpg"))
            key = top.stem.replace("sheet_", "").replace("_top", "").replace("_", " ")
            label = PLATFORM_NAMES.get(key, key.title())
            pair = [("Top quarter", top)] + ([("Bottom 5", bottom)] if bottom.exists() else [])
            for cap, p in pair:
                figs.append(f'<figure class="sheet"><img src="{inline_image(p)}" alt="{label}: {cap.lower()} posts" loading="lazy">'
                            f'<figcaption><b>{cap}</b> · {label} · engagement of each post, in sheet order:</figcaption>'
                            f'{sheet_key(p.with_suffix(".json"))}</figure>')
        return f'<h3 id="{slug}">{heading}</h3>' + (f'<div class="sheets">{"".join(figs)}</div>' if figs else "")

    body = re.sub(r"<h3>(.*?)</h3>", add_sheets, body)

    # sections + contents
    toc, sections = [], []
    for chunk in re.split(r"(?=<h2>)", body):
        h2 = re.match(r"<h2>(.*?)</h2>", chunk)
        if not h2:
            sections.append(f'<div class="intro">{chunk}</div>' if chunk.strip() else "")
            continue
        label = re.sub(r"<[^>]+>", "", h2.group(1))
        sid = slugify(label)
        if sid == "the-short-version":
            chunk = short_version(chunk)
        toc.append(f'<li><a href="#{sid}">{html.escape(label)}</a></li>')
        sections.append(f'<section id="{sid}" class="section section-{sid}">{chunk}</section>')

    meta_html = evidence_pills(markdown.markdown(meta))
    date = re.search(r"(\d{4})-(\d{2})-(\d{2})", meta)
    pulled = f"{int(date.group(3))} {MONTHS[int(date.group(2)) - 1]} {date.group(1)}" if date else ""
    who = html.escape(person) + (f" · {pulled}" if pulled else "")
    page = TEMPLATE
    for key, value in (("TITLE", html.escape(title)), ("PERSON", html.escape(person)), ("WHO", who), ("META", meta_html),
                       ("TOC", "".join(toc)), ("BODY", "".join(sections)), ("REPO", REPO_URL), ("CSS", CSS), ("JS", JS)):
        page = page.replace(f"%%{key}%%", value)
    out_path.write_text(page)
    return out_path


CSS = """
:root{--bg:#ffffff;--surface:#f6f8fa;--surface-2:#eef2f6;--ink:#0b1b33;--text:#3c4a5e;--muted:#6a7789;--line:#e3e8ee;--line-strong:#cfd7e1;
--accent:#2457e6;--accent-soft:#e9efff;--seen:#0b7a4b;--seen-bg:#e5f5ec;--inf:#8a5300;--inf-bg:#fff2d6;--code:#f6f8fa;--shadow:0 1px 2px rgba(11,27,51,.06),0 8px 24px -12px rgba(11,27,51,.12);color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0d1117;--surface:#151b24;--surface-2:#1b2330;--ink:#eef2f7;--text:#b7c1ce;--muted:#8592a3;--line:#242d3a;--line-strong:#2f3a49;
--accent:#7aa2ff;--accent-soft:#1a2440;--seen:#4fd18f;--seen-bg:#11291e;--inf:#f2b84b;--inf-bg:#2e2410;--code:#111720;--shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px -12px rgba(0,0,0,.6);color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0d1117;--surface:#151b24;--surface-2:#1b2330;--ink:#eef2f7;--text:#b7c1ce;--muted:#8592a3;--line:#242d3a;--line-strong:#2f3a49;
--accent:#7aa2ff;--accent-soft:#1a2440;--seen:#4fd18f;--seen-bg:#11291e;--inf:#f2b84b;--inf-bg:#2e2410;--code:#111720;--shadow:0 1px 2px rgba(0,0,0,.4),0 8px 24px -12px rgba(0,0,0,.6);color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:88px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--text);font:400 16px/1.65 Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;font-feature-settings:"cv11","ss01";-webkit-font-smoothing:antialiased}
::selection{background:var(--accent-soft);color:var(--ink)}
a{color:var(--accent);text-decoration:underline;text-decoration-color:color-mix(in srgb,var(--accent) 35%,transparent);text-underline-offset:3px}
a:hover{text-decoration-color:var(--accent)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:6px}
.topbar{position:sticky;top:0;z-index:20;height:64px;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:0 28px;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:saturate(1.4) blur(10px);border-bottom:1px solid var(--line)}
.mark{font:650 17px/1 Inter,sans-serif;color:var(--ink);text-decoration:none;letter-spacing:-.01em}
.mark span{color:var(--accent)}
.topbar .who{color:var(--ink);font-size:14px;font-weight:550;font-variant-numeric:tabular-nums}
.topbar .right{display:flex;align-items:center;gap:14px}
.topbar .repo{font-size:13.5px;color:var(--muted);text-decoration:none;padding-left:14px;border-left:1px solid var(--line)}
.topbar .repo:hover{color:var(--ink)}
.icon-btn{display:inline-grid;place-items:center;width:36px;height:36px;border-radius:9px;border:1px solid var(--line);background:var(--bg);color:var(--text);cursor:pointer;transition:background .15s,border-color .15s}
.icon-btn:hover{background:var(--surface);border-color:var(--line-strong)}
.icon-btn svg{width:17px;height:17px;fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}
.layout{display:grid;grid-template-columns:264px minmax(0,1fr);max-width:1320px;margin:0 auto}
.toc{position:sticky;top:64px;align-self:start;height:calc(100vh - 64px);overflow:auto;padding:36px 20px 36px 28px;border-right:1px solid var(--line)}
.toc-title{font:600 12.5px Inter,sans-serif;color:var(--ink);margin:0 0 12px 12px}
.toc-list{position:relative}.toc ol{list-style:none;margin:0;padding:0}
.toc li a{display:block;padding:6px 12px;border-radius:7px;color:var(--muted);text-decoration:none;font-size:14px;line-height:1.35;transition:color .15s}
.toc li a:hover{color:var(--ink);background:var(--surface)}
.toc li a.active{color:var(--accent);font-weight:550}
.toc .marker{position:absolute;left:0;top:0;width:2px;height:30px;background:var(--accent);border-radius:2px;transition:transform .35s cubic-bezier(.16,1,.3,1),height .35s cubic-bezier(.16,1,.3,1);transform:translateY(0)}
main{padding:34px 64px 120px;min-width:0}
.doc{max-width:880px}
h1{font:700 42px/1.08 Inter,sans-serif;letter-spacing:-.025em;color:var(--ink);margin:0;text-wrap:balance}
.meta{margin:8px 0 0;color:var(--muted);font-size:15px}
.intro>p{margin:4px 0 0;font-size:14.5px;line-height:1.55;color:var(--muted)}
.meta p{margin:0}.meta strong{color:var(--ink);font-weight:600}
h2{font:680 28px/1.2 Inter,sans-serif;letter-spacing:-.02em;color:var(--ink);margin:0 0 18px;text-wrap:balance}
h3{font:620 19px/1.35 Inter,sans-serif;letter-spacing:-.01em;color:var(--ink);margin:40px 0 10px;text-wrap:balance}
.section{padding-top:56px;margin-top:56px;border-top:1px solid var(--line)}
p,li{max-width:70ch}
p{margin:0 0 14px}
strong{color:var(--ink);font-weight:600}
ul,ol{padding-left:22px;margin:0 0 16px}
li{margin:0 0 8px}li::marker{color:var(--muted)}
main section:first-of-type{border-top:0;margin-top:4px;padding-top:24px}
main section:first-of-type h2{margin-bottom:6px}
.section-the-short-version>ol{list-style:none;padding:0;counter-reset:f;margin:0}
.section-the-short-version>ol>li{counter-increment:f;position:relative;padding:11px 0 11px 44px;border-top:1px solid var(--line);margin:0;max-width:70ch}
.section-the-short-version>ol>li:first-child{border-top:0}
.section-the-short-version>ol>li::before{content:counter(f);position:absolute;left:0;top:12px;width:26px;height:26px;border-radius:8px;display:grid;place-items:center;background:var(--accent-soft);color:var(--accent);font:650 13.5px/1 Inter,sans-serif;font-variant-numeric:tabular-nums}
.section-the-short-version .lead{margin:0;font:620 17.5px/1.4 Inter,sans-serif;letter-spacing:-.01em;color:var(--ink)}
.section-the-short-version .detail{margin:3px 0 0;font-size:15px;line-height:1.55;color:var(--text)}
.section-the-short-version>p:last-child{margin-top:16px;padding:14px 18px;border-radius:12px;background:var(--surface);border:1px solid var(--line)}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:22px 0 4px}
.stat{position:relative;display:block;background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:15px 16px 14px;box-shadow:var(--shadow);text-decoration:none;color:inherit;transition:border-color .15s,transform .2s cubic-bezier(.16,1,.3,1)}
a.stat:hover{border-color:color-mix(in srgb,var(--accent) 45%,var(--line));transform:translateY(-1px)}
.stat-value{font:680 28px/1.1 Inter,sans-serif;letter-spacing:-.02em;color:var(--ink);font-variant-numeric:tabular-nums;padding-right:56px}
.stat-label{margin-top:6px;font-size:13.5px;line-height:1.4;color:var(--muted)}
.stat .pill{position:absolute;top:15px;right:14px}.nowrap{white-space:nowrap}
th.num,td.num{text-align:right}
.sheet-key{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:4px 14px;font-size:13px;font-variant-numeric:tabular-nums}
.sheet-key li{margin:0}.sheet-key a{color:var(--text);text-decoration-color:var(--line-strong)}.sheet-key a:hover{color:var(--accent)}
.pill{display:inline-block;vertical-align:1px;font:650 11px/1 Inter,sans-serif;letter-spacing:.05em;text-transform:uppercase;padding:4px 7px;border-radius:999px;white-space:nowrap}
.pill-seen{color:var(--seen);background:var(--seen-bg)}
.pill-inferred{color:var(--inf);background:var(--inf-bg)}
a.pill-link{text-decoration:none;box-shadow:inset 0 0 0 1px color-mix(in srgb,currentColor 28%,transparent)}a.pill-link:hover{box-shadow:inset 0 0 0 1px currentColor}
.table-wrap{overflow-x:auto;margin:18px 0 22px;border:1px solid var(--line);border-radius:12px;background:var(--bg)}
table{width:100%;border-collapse:collapse;font-size:14.5px;font-variant-numeric:tabular-nums}
th{text-align:left;font-weight:600;font-size:12.5px;color:var(--muted);background:var(--surface);padding:10px 14px;border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:11px 14px;border-bottom:1px solid var(--line);vertical-align:top;color:var(--text)}
tr:last-child td{border-bottom:0}
td:first-child{color:var(--ink);font-weight:500;white-space:nowrap}
.chart{margin:24px 0 8px;padding:18px 18px 10px;border:1px solid var(--line);border-radius:14px;background:var(--bg)}
.chart svg{width:100%;height:auto;display:block}.chart .chart-narrow,.chart .chart-legend{display:none}
.chart .pin-badge{fill:var(--bg);stroke:var(--line-strong)}.chart .pin-num{fill:var(--muted);font:650 11px Inter,sans-serif}
.chart-legend{list-style:none;margin:10px 0 0;padding:0;font-size:13px;line-height:1.45;color:var(--text)}.chart-legend li{margin:0 0 4px;display:flex;gap:8px;align-items:baseline}
.pin-key{flex:none;display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;border:1px solid var(--line-strong);font:650 10.5px/1 Inter,sans-serif;color:var(--muted)}.pin-date{color:var(--muted);white-space:nowrap}
.chart .grid{stroke:var(--line)}.chart .axis{fill:var(--muted);font:500 12px Inter,sans-serif}
.chart .line{fill:none;stroke:var(--accent);stroke-width:2.5;stroke-linejoin:round}
.chart .dot{fill:var(--bg);stroke:var(--accent);stroke-width:2.5}
.chart .point-label{fill:var(--ink);font:650 13px Inter,sans-serif}
.chart .pin{stroke:var(--line-strong);stroke-dasharray:3 4}
.chart .pin-label{fill:var(--muted);font:550 12px Inter,sans-serif}
figcaption{margin-top:8px;font-size:13px;line-height:1.5;color:var(--muted)}
.sheets{display:grid;gap:14px;margin:14px 0 18px}
.sheet{margin:0}
.sheet img{width:100%;height:auto;display:block;border-radius:12px;border:1px solid var(--line);background:#fff}
.prompt{margin:14px 0 26px;border:1px solid var(--line);border-radius:12px;background:var(--code);overflow:hidden}
.prompt-head{display:flex;align-items:center;justify-content:space-between;padding:8px 8px 8px 14px;border-bottom:1px solid var(--line);font:600 12.5px Inter,sans-serif;color:var(--muted)}
.copy{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--bg);color:var(--ink);border-radius:8px;padding:6px 10px;font:600 12.5px Inter,sans-serif;cursor:pointer;transition:background .15s,border-color .15s,color .15s}
.copy:hover{border-color:var(--line-strong);background:var(--surface)}
.copy svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.5}
.copy.done{color:var(--seen);border-color:color-mix(in srgb,var(--seen) 40%,var(--line))}
.prompt pre{margin:0;padding:14px 16px;white-space:pre-wrap;font:13.5px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--ink)}
.section-ten-plays-for-you-stage-starting-out h3,.section h3:first-child{margin-top:28px}
footer{margin-top:72px;padding-top:24px;border-top:1px solid var(--line);font-size:13.5px;color:var(--muted)}
::-webkit-scrollbar{width:10px;height:10px}::-webkit-scrollbar-thumb{background:var(--line-strong);border-radius:10px;border:2px solid var(--bg)}::-webkit-scrollbar-track{background:transparent}
@media (min-width:1081px){.table-wrap{overflow:visible}.table-wrap thead th{position:sticky;top:64px;z-index:2}.table-wrap thead th:first-child{border-top-left-radius:11px}.table-wrap thead th:last-child{border-top-right-radius:11px}}
@media (max-width:1080px){.layout{grid-template-columns:1fr}.toc{position:sticky;top:64px;z-index:10;height:auto;border-right:0;border-bottom:1px solid var(--line);padding:8px 16px;background:var(--bg);overflow-x:auto;scrollbar-width:none}.toc::-webkit-scrollbar{display:none}
.toc-title,.toc .marker{display:none}.toc ol{display:flex;gap:4px;white-space:nowrap}.toc li a{padding:6px 10px}.toc li a.active{background:var(--accent-soft)}main{padding:36px 24px 96px}html{scroll-padding-top:124px}}
@media (max-width:720px){.chart .chart-wide{display:none}.chart .chart-narrow,.chart .chart-legend{display:block}th.num,td.num{text-align:left}.table-wrap table{width:max-content;min-width:100%}.table-wrap td{max-width:260px}h1{font-size:30px}h2{font-size:23px}.stats{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:16px}.stat{padding:12px 12px 11px}.stat-value{font-size:22px;padding-right:0}.stat-label{font-size:12.5px}.stat .pill{position:static;margin-top:8px}.section-the-short-version .lead{font-size:16.5px}.topbar{padding:0 16px}.topbar .who,.topbar .repo{display:none}main{padding:28px 16px 80px}.section-the-short-version>ol>li{padding-left:42px}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}.toc .marker{transition:none}}
@media print{.topbar,.toc,.copy{display:none}.layout{display:block}}
"""

JS = """
(function(){
  var root=document.documentElement;
  try{var saved=localStorage.getItem('rea-theme');if(saved)root.dataset.theme=saved;}catch(e){}
  document.getElementById('theme').addEventListener('click',function(){
    var dark=root.dataset.theme?root.dataset.theme==='dark':matchMedia('(prefers-color-scheme: dark)').matches;
    root.dataset.theme=dark?'light':'dark';try{localStorage.setItem('rea-theme',root.dataset.theme);}catch(e){}
  });
  document.querySelectorAll('.copy').forEach(function(btn){
    btn.addEventListener('click',function(){
      var code=btn.closest('.prompt').querySelector('code').innerText,label=btn.querySelector('span');
      var done=function(t){label.textContent=t;btn.classList.add('done');setTimeout(function(){label.textContent='Copy the prompt';btn.classList.remove('done');},1800);};
      if(navigator.clipboard){navigator.clipboard.writeText(code).then(function(){done('Copied');},function(){done('Select and copy');});}else{done('Select and copy');}
    });
  });
  var links=[].slice.call(document.querySelectorAll('.toc a')),marker=document.querySelector('.toc .marker');
  function mark(id){links.forEach(function(a){var on=a.getAttribute('href')==='#'+id;a.classList.toggle('active',on);
    if(on&&marker){marker.style.transform='translateY('+a.offsetTop+'px)';marker.style.height=a.offsetHeight+'px';}});}
  var sections=[].slice.call(document.querySelectorAll('main section'));
  function spy(){var y=window.scrollY+140,cur=sections.length?sections[0].id:null;
    sections.forEach(function(s){if(s.offsetTop<=y)cur=s.id;});
    if(window.innerHeight+window.scrollY>=document.body.scrollHeight-4&&sections.length)cur=sections[sections.length-1].id;
    if(cur)mark(cur);}
  window.addEventListener('scroll',spy,{passive:true});spy();
})();
"""

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%%PERSON%% · Personal Brand Teardown</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap" rel="stylesheet">
<style>%%CSS%%</style></head>
<body>
<header class="topbar"><div><a class="mark" href="%%REPO%%" target="_blank" rel="noopener"><span>/</span>rea-brand</a></div>
<div class="right"><span class="who">%%WHO%%</span><a class="repo" href="%%REPO%%" target="_blank" rel="noopener">github.com/AdityaUmale/rea-brand</a>
<button class="icon-btn" id="theme" type="button" aria-label="Switch light or dark theme"><svg viewBox="0 0 20 20"><circle cx="10" cy="10" r="3.6"/><path d="M10 1.8v2.1M10 16.1v2.1M1.8 10h2.1M16.1 10h2.1M4.2 4.2l1.5 1.5M14.3 14.3l1.5 1.5M4.2 15.8l1.5-1.5M14.3 5.7l1.5-1.5"/></svg></button></div></header>
<div class="layout">
<nav class="toc" aria-label="Contents"><p class="toc-title">Contents</p><div class="toc-list"><span class="marker" aria-hidden="true"></span><ol>%%TOC%%</ol></div></nav>
<main><article class="doc"><h1>%%TITLE%%</h1><div class="meta">%%META%%</div>%%BODY%%
<footer>Built with <a href="%%REPO%%" target="_blank" rel="noopener">/rea-brand</a>, an open-source Claude Code skill. Data through treg.</footer></article></main>
</div>
<script>%%JS%%</script>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("markdown_file", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    out = args.out or args.markdown_file.with_suffix(".html")
    print(build(args.markdown_file, out))


if __name__ == "__main__":
    main()
