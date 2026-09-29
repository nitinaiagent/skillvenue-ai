"""Builds index.html from data/terms.json + build/template.html.
Usage (from repo root):  python3 build/build.py
"""
import json, re, html
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
data = json.loads((ROOT / "data/terms.json").read_text(encoding="utf-8"))
tpl = (ROOT / "build/template.html").read_text(encoding="utf-8")
terms, cats = data["terms"], data["categories"]
LV = {"B": "Beginner", "P": "Practitioner", "A": "Advanced"}
ST = {"new": "New", "hot": "Trending", "est": "Established"}
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
e = html.escape

COPY_SVG = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/></svg>'

LVC = {"B": "t", "P": "b", "A": "p"}
STC = {"new": "new", "hot": "m", "est": "n"}

def card(t, n):
    return (f'<article class="term lv-{t["l"]}" id="{t["id"]}"><div class="catlabel">{e(t["c"])}</div>'
            f'<div class="top"><div class="name"><span class="idx">{n:03d}</span><a href="#{t["id"]}">{e(t["t"])}</a></div>'
            f'<div class="tags"><span class="pill {LVC[t["l"]]}">{LV[t["l"]]}</span><span class="pill {STC[t["s"]]}">{ST[t["s"]]}</span></div></div>'
            f'<p class="def">{e(t["d"])}</p><p class="eg"><b>Example</b>{e(t["e"])}</p>'
            f'<button class="copy" title="Copy link" aria-label="Copy link to {e(t["t"])}">{COPY_SVG}</button></article>')

SUBS = {
 "Foundations": "The building blocks every other AI term sits on.",
 "Models & Architecture": "The engines behind ChatGPT, Claude, Gemini and every AI product.",
 "Using LLMs": "What you'll meet the moment you use or build with a model.",
 "Prompting & Context": "How we talk to models, and how we decide what they see.",
 "Training & Fine-Tuning": "How models learn, and how they're shaped after pre-training.",
 "RAG & Knowledge": "Giving models your data so answers are grounded and current.",
 "AI Agents": "The fastest-moving area: models that don't just answer, but act.",
 "Agent Infrastructure & Protocols": "The harnesses, standards and plumbing that make agents work.",
 "AI Coding": "How software is now written with, and by, AI.",
 "Infrastructure & Hardware": "Chips, data centres, costs and running models in production.",
 "Multimodal & Physical AI": "Beyond text: images, video, voice, robots and the physical world.",
 "Evaluation & Safety": "Measuring AI, securing it, and keeping it aligned.",
 "Business, Work & Careers": "How AI is changing companies, jobs and business models.",
 "Policy & Society": "Regulation, big-picture debates and AI's impact on society.",
 "Ecosystem: Tools & Players": "The companies, products and frameworks you'll hear named.",
}

groups, chips, overview, n = [], [], [], 0
for i, c in enumerate(cats, 1):
    items = [t for t in terms if t["c"] == c]
    cards_html = []
    for t in items:
        n += 1
        cards_html.append(card(t, n))
    groups.append(f'<section class="block group" id="g-{slug(c)}"><div class="kicker">{i:02d} · {len(items)} terms</div><h2>{e(c)}</h2>'
                  f'<p class="lede">{e(SUBS.get(c, ""))}</p><div class="list">{"".join(cards_html)}</div></section>')
    col = "tmpb"[(i - 1) % 4]
    overview.append(f'<a class="card {col}" href="#g-{slug(c)}"><span class="cnt">{len(items)} terms</span><div class="ic {col}">{i:02d}</div>'
                    f'<h4>{e(c)}</h4><p>{e(SUBS.get(c, ""))}</p></a>')
    chips.append(f'<button class="chip" data-c="{e(c)}" aria-pressed="false">{e(c)} · {len(items)}</button>')

upd = date.fromisoformat(data["updated"])
jsonld = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "SkillVenue AI Glossary",
          "url": "https://skillvenue.com/", "author": {"@type": "Person", "name": "Nitin Monga"},
          "dateModified": data["updated"],
          "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t["t"], "description": t["d"],
                              "url": f"https://skillvenue.com/#{t['id']}"} for t in terms]}
slim = {"terms": [{k: t[k] for k in ("id", "t", "c", "l", "s", "d", "e")} for t in terms]}

out = (tpl.replace("__GROUPS__", "".join(groups)).replace("__OVERVIEW__", "".join(overview)).replace("__CATCHIPS__", "".join(chips))
       .replace("__JSONLD__", json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/"))
       .replace("__DATA__", json.dumps(slim, ensure_ascii=False).replace("</", "<\\/"))
       .replace("__TOTAL__", str(len(terms))).replace("__NCATS__", str(len(cats)))
       .replace("__NNEW__", str(sum(t["s"] == "new" for t in terms)))
       .replace("__NHOT__", str(sum(t["s"] == "hot" for t in terms)))
       .replace("__YEAR__", str(upd.year)).replace("__UPDATED_H__", upd.strftime("%B %Y")))
(ROOT / "index.html").write_text(out, encoding="utf-8")

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
      f'<url><loc>https://skillvenue.com/</loc><lastmod>{data["updated"]}</lastmod></url>', '</urlset>']
(ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n")
print(f"Built index.html with {len(terms)} terms in {len(cats)} categories.")
