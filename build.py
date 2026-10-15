#!/usr/bin/env python3
"""Genera index.html e le pagine dei case study da data/projects.json.

Uso:  python3 build.py
Per aggiungere o modificare un progetto, modifica data/projects.json e rilancia lo script.
I campi vuoti ("problem", "outcome", "link": null, ...) non vengono mostrati.
"""
import json, html, re
from pathlib import Path

ROOT = Path(__file__).parent
SITE = "https://lorenzogravina.vercel.app"
EMAIL = "gravinalrn@gmail.com"
ROLE = "Senior UI/UX Designer"  # ruolo attuale in PAAdvice: verificalo
COMPANY = "PAAdvice"
MAILTO = f"mailto:{EMAIL}?subject=Ciao%20Lorenzo"
SOCIAL = [
    ("LinkedIn", "https://www.linkedin.com/in/lorenzo-gravina-a4175037/"),
    ("Dribbble", "https://dribbble.com/lorenzogravina"),
    ("Figma", "https://www.figma.com/@gravinalorenzo"),
]
RECOGNITION = [
    {"label": "Nominee Awwwards", "note": "Sito System Management, 2024", "url": "https://www.awwwards.com/sites/system-management"},
    {"label": "Nominee CSS Winner", "note": "Sito System Management, 2024", "url": "https://www.csswinner.com/details/system-management/18043"},
]
CLIENTS = ["Bulgari", "Enel", "Sisal", "Poligrafico e Zecca dello Stato", "CNH Industrial", "Q8", "Aviva", "Sime"]

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
DOWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>'
OUT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'

e = html.escape


def head(title, desc, path, image="img/og-image.png", extra=""):
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="it_IT">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:image" content="{SITE}/{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" type="image/png" sizes="32x32" href="img/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="192x192" href="img/favicon/android-icon-192x192.png">
<link rel="apple-touch-icon" href="img/favicon/apple-icon-180x180.png">
<link rel="manifest" href="img/favicon/manifest.json">
<link rel="preload" href="fonts/bricolage-grotesque.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/fonts.css">
<link rel="stylesheet" href="css/site.css">
<script>document.documentElement.classList.add('js')</script>
{extra}
</head>
<body>
<a class="skip" href="#main">Vai al contenuto</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Lorenzo Gravina, vai alla home"><img src="img/logo.webp" alt="" width="40" height="40"><span aria-hidden="true">Lorenzo Gravina</span></a>
    <nav class="nav" aria-label="Principale">
      <a href="index.html#lavori">Lavori</a>
      <a class="nav-hide" href="index.html#profilo">Profilo</a>
      <a class="btn small primary" href="{MAILTO}">Scrivimi</a>
    </nav>
  </div>
</header>
"""


def footer():
    links = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOCIAL)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <p>© <span data-year>2026</span> Lorenzo Gravina. Progettato da me, sviluppato con Claude in HTML, CSS e JS.</p>
    <ul>{links}</ul>
  </div>
</footer>
<script src="js/motion.min.js" defer></script>
<script src="js/site.js" defer></script>
</body>
</html>
"""


def tag(p):
    cls = "tag live" if p["status"] == "Online" else "tag"
    out = f'<span class="{cls}">{e(p["status"])}</span>'
    if p.get("builtWith"):
        out += f'<span class="tag ai">Sviluppato con {e(p["builtWith"])}</span>'
    return out


def cover_size(p):
    w, h = p.get("coverSize", [1600, 1200])
    pos = f' style="object-position:{p["coverPosition"]}"' if p.get("coverPosition") else ""
    return f'width="{w}" height="{h}"{pos}'


def inline_md(t):
    t = e(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)
    return t


def image_size(src):
    try:
        from PIL import Image
        with Image.open(ROOT / src) as im:
            return im.size
    except Exception:
        return None


def render_story(path):
    """Converte il markdown di un case study (sottoinsieme: ## titoli, paragrafi, elenchi, immagini)."""
    text = re.sub(r"<!--.*?-->", "", (ROOT / path).read_text(encoding="utf-8"), flags=re.S)
    out, section, buf, lst = [], None, [], None

    def flush_list():
        nonlocal lst
        if lst:
            tagname, items = lst
            buf.append(f"<{tagname}>" + "".join(f"<li>{inline_md(i)}</li>" for i in items) + f"</{tagname}>")
            lst = None

    def flush_text():
        flush_list()
        if buf:
            head = f'<h2>{inline_md(section)}</h2>' if section else '<span aria-hidden="true"></span>'
            out.append(f'<div class="story-section">{head}<div class="story-text">{"".join(buf)}</div></div>')
            buf.clear()

    para = []
    def flush_para():
        if para:
            buf.append(f"<p>{inline_md(' '.join(para))}</p>")
            para.clear()

    for raw in text.splitlines() + [""]:
        line = raw.strip()
        m_img = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        m_ul = re.match(r"^-\s+(.*)", line)
        m_ol = re.match(r"^\d+\.\s+(.*)", line)
        if line.startswith("## "):
            flush_para(); flush_text(); section = line[3:].strip()
        elif m_img:
            flush_para(); flush_text(); section = None
            alt, src = m_img.groups()
            size = image_size(src)
            dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
            shape = ""
            if size and size[1] > size[0] * 1.3:
                shape = " tall"
            elif size and size[1] > size[0] * 0.8:
                shape = " square"
            out.append(f'<figure class="story-figure{shape}"><img src="{src}" alt="{e(alt)}" loading="lazy"{dims}></figure>')
        elif m_ul or m_ol:
            flush_para()
            kind = "ul" if m_ul else "ol"
            if lst and lst[0] != kind:
                flush_list()
            if not lst:
                lst = (kind, [])
            lst[1].append((m_ul or m_ol).group(1))
        elif not line:
            flush_para(); flush_list()
        else:
            if lst:
                flush_list()
            para.append(line)
    flush_text()
    return f'<div class="story">{"".join(out)}</div>'


def contact_section():
    socials = "".join(f'<a class="btn" href="{u}" target="_blank" rel="noopener">{n}</a>' for n, u in SOCIAL)
    return f"""<section class="section" id="contatti" aria-labelledby="contatti-title">
  <div class="wrap">
    <div class="contact">
      <h2 id="contatti-title">Hai un prodotto da progettare o un team da far crescere?</h2>
      <p>Scrivimi due righe su cosa stai costruendo. Rispondo entro un paio di giorni.</p>
      <p class="mail-row"><a class="mail" href="{MAILTO}">{EMAIL}</a> <button class="copy" type="button" data-copy="{EMAIL}">Copia indirizzo</button><span class="copy-status" role="status" aria-live="polite"></span></p>
      <div class="hero-actions">
        <a class="btn primary" href="{MAILTO}">Scrivimi un'email {ARROW}</a>
        <a class="btn download" href="lorenzo-gravina-cv.pdf" target="_blank" rel="noopener">Scarica il CV {DOWN}</a>
        {socials}
      </div>
    </div>
  </div>
</section>
"""


def build_index(projects):
    items, previews = [], []
    for i, p in enumerate(projects):
        style = f' style="--accent:{p["accent"]}"'
        items.append(f"""<li class="work-item{' is-active' if i == 0 else ''}" data-slug="{p['slug']}"{style}>
  <a href="{p['slug']}.html">
    <span class="thumb" data-vt="cover-{p['slug']}"><img src="{p['cover']}" alt="" loading="lazy" {cover_size(p)}></span>
    <h3 style="view-transition-name:title-{p['slug']}">{e(p['title'])}</h3>
    <span class="meta"><span>{e(p['kind'])}</span><span>{e(p['year'])}</span>{tag(p)}</span>
    <span class="arrow">{ARROW}</span>
  </a>
</li>""")
        previews.append(f"""<figure class="{'is-active' if i == 0 else ''}" data-slug="{p['slug']}" data-vt="cover-{p['slug']}"{style}>
  <img src="{p['cover']}" alt="Anteprima di {e(p['title'])}" {'' if i == 0 else 'loading="lazy" '}{cover_size(p)}>
  <figcaption>{e(p['summary'])}</figcaption>
</figure>""")

    clients = "".join(f"<li>{e(c)}</li>" for c in CLIENTS)
    recog_html = "".join(
        f'<a href="{r["url"]}" target="_blank" rel="noopener"><span>{e(r["label"])}<small>{e(r["note"])}</small></span>{OUT}</a>'
        for r in RECOGNITION)

    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "Person", "name": "Lorenzo Gravina",
        "jobTitle": ROLE,
        "knowsAbout": ["UI design", "UX design", "Product design", "Design system", "AI-native design", "Prototipazione con l'AI"], "url": SITE + "/", "email": "mailto:" + EMAIL,
        "worksFor": {"@type": "Organization", "name": COMPANY},
        "address": {"@type": "PostalAddress", "addressLocality": "Napoli", "addressCountry": "IT"},
        "alumniOf": "Accademia di Belle Arti di Napoli",
        "sameAs": [u for _, u in SOCIAL],
    }, ensure_ascii=False)

    lines = ["Disegno prodotti", "digitali che si usano", "senza pensarci."]
    words, h1 = 0, ""
    for l in lines:
        spans = []
        for w in l.split():
            spans.append(f'<span class="word" style="--i:{words}">{w}</span>')
            words += 1
        h1 += f'<span class="line reveal-line">{" ".join(spans)}</span>'

    page = head(
        "Lorenzo Gravina — Senior UI/UX Designer a Napoli",
        "Senior UI/UX designer a Napoli dal 2014, oggi in PAAdvice. Progetto interfacce per aziende come Bulgari, Enel e Sisal e costruisco prodotti funzionanti con l'AI.",
        "", extra=f'<script type="application/ld+json">{jsonld}</script>')
    page += f"""<main id="main">
<section class="hero">
  <div class="wrap">
    <div class="hero-intro reveal-fade">
      <img src="img/lorenzo-gravina.webp" alt="Ritratto di Lorenzo Gravina" width="64" height="64">
      <p><strong>Lorenzo Gravina</strong><span class="status">{ROLE} @ {COMPANY}</span></p>
    </div>
    <h1>{h1}</h1>
    <p class="hero-lede reveal-fade">Sono un designer di Napoli. Dal 2014 progetto app, siti e sistemi di interfaccia: per nove anni in System Management, dove ho guidato il team di designer, e da maggio 2025 in PAAdvice. Oggi uso l'AI per portare le idee fino a un prodotto che funziona, senza rinunciare alla cura del design.</p>
    <div class="hero-actions reveal-fade">
      <a class="btn primary" href="#lavori">Guarda i lavori {ARROW}</a>
      <a class="btn" href="{MAILTO}">Scrivimi</a>
    </div>
  </div>
</section>

<section class="clients" aria-labelledby="clienti-title">
  <div class="wrap">
    <h2 id="clienti-title">Ho progettato per</h2>
    <ul>{clients}</ul>
  </div>
</section>

<section class="section" id="lavori" aria-labelledby="lavori-title">
  <div class="wrap">
    <div class="section-head">
      <h2 id="lavori-title">Lavori scelti</h2>
      <p>Prodotti per clienti, concept e progetti che ho costruito da solo con l'AI. Aprili per vedere come ci sono arrivato.</p>
    </div>
    <div class="work-index">
      <ul class="work-list">
{chr(10).join(items)}
      </ul>
      <div class="work-preview" aria-hidden="true"><div class="tilt">
{chr(10).join(previews)}
      </div></div>
    </div>
  </div>
</section>

<section class="section" id="profilo" aria-labelledby="profilo-title" style="padding-top:0">
  <div class="wrap">
    <div class="profile">
      <div class="about">
        <h2 id="profilo-title" class="visually-hidden">Profilo</h2>
        <p>Lavoro in team, mi piace capire il problema prima di aprire Figma e tengo alla qualità di ogni dettaglio, fino all'ultimo pixel.</p>
        <p class="small">Mi sono formato in Design della comunicazione all'Accademia di Belle Arti di Napoli. Da allora mi muovo tra UI, UX, product design e identità digitale, e oggi costruisco anche i prodotti che progetto: questo sito, per esempio, l'ho sviluppato con Claude.</p>
        <h3 class="ai-title">Come lavoro con l'AI</h3>
        <p class="small">Uso l'AI per passare dall'idea a un prodotto che funziona, non per saltare il design. Io decido cosa costruire, come deve funzionare e quando è abbastanza buono; l'AI scrive il codice e io lo verifico, con particolare cura per accessibilità e prestazioni. Così ho sviluppato Toneday, in vibe coding con Claude. Meno presentazioni, più cose da provare.</p>
        <div class="recognition">{recog_html}</div>
      </div>
      <div>
        <h3>Percorso</h3>
        <ol class="timeline" reversed>
          <li><time>2025 — oggi</time><div><strong>{ROLE}, {COMPANY}</strong><span>Da maggio 2025.</span></div></li>
          <li><time>2016 — 2025</time><div><strong>Senior UI/UX Designer, System Management</strong><span>Interfacce per clienti enterprise e coordinamento del team di designer: formazione, qualità dei progetti, lavoro con gli altri reparti.</span></div></li>
          <li><time>2014 — 2015</time><div><strong>Brand e Web Designer, Maidiremedia</strong><span>Identità visive e siti web.</span></div></li>
          <li><time>Formazione</time><div><strong>Design della comunicazione, 110/110</strong><span>Accademia di Belle Arti di Napoli</span></div></li>
        </ol>
        <h3>Di cosa mi occupo</h3>
        <ul class="skills"><li>UI design</li><li>UX design</li><li>Product design</li><li>Design system</li><li>Digital brand identity</li><li>Prototipazione</li><li>Design e sviluppo con l'AI</li></ul>
      </div>
    </div>
  </div>
</section>

{contact_section()}
</main>
"""
    page += footer()
    (ROOT / "index.html").write_text(page, encoding="utf-8")


def build_case(p, nxt):
    facts = [("Cliente", p["client"]), ("Anno", p["year"]), ("Ruolo", p["role"]), ("Tipo", p["kind"]), ("Stato", p["status"]),
             ("Sviluppo", f'Con {p["builtWith"]}, in vibe coding' if p.get("builtWith") else "")]
    facts_html = "".join(f"<div><dt>{k}</dt><dd>{e(v)}</dd></div>" for k, v in facts if v)
    links = []
    if p.get("link"):
        links.append(f'<a class="btn primary" href="{p["link"]["url"]}" target="_blank" rel="noopener">{e(p["link"]["label"])} {OUT}</a>')
    for r in p.get("recognition", []):
        links.append(f'<a class="btn" href="{r["url"]}" target="_blank" rel="noopener">{e(r["label"])} {OUT}</a>')
    if p.get("linkNote") and links:
        links.append(f'<span class="cs-note">{e(p["linkNote"])}</span>')
    links_html = f'<div class="cs-links">{"".join(links)}</div>' if links else ""

    body = []
    for label, key in [("Il problema", "problem"), ("Cosa ho fatto", "work"), ("Il risultato", "outcome")]:
        if p.get(key):
            body.append(f"<h2>{label}</h2><p>{e(p[key])}</p>")

    gallery = []
    for g in p.get("gallery", []):
        wide = " wide" if g.get("wide") else ""
        if g.get("video"):
            gallery.append(f'<figure class="{wide.strip()}"><video src="{g["video"]}" poster="{g.get("poster","")}" muted loop playsinline controls preload="none" aria-label="{e(g["alt"])}"></video></figure>')
        else:
            w, h = ("1600", "1200") if wide else ("630", "1200")
            gallery.append(f'<figure class="{wide.strip()}"><img src="{g["src"]}" alt="{e(g["alt"])}" loading="lazy" width="{w}" height="{h}"></figure>')

    page = head(f'{p["title"]} — case study di Lorenzo Gravina', p["summary"], f'{p["slug"]}.html')
    page += f"""<main id="main" style="--accent:{p['accent']}">
<section class="cs-hero">
  <div class="wrap">
    <a class="cs-back" href="index.html#lavori">{ARROW} Tutti i lavori</a>
    <h1 style="view-transition-name:title-{p['slug']}">{e(p['title'])}</h1>
    <p class="summary reveal-fade">{e(p['summary'])}</p>
    <dl class="cs-facts reveal-fade">{facts_html}</dl>
    {links_html}
  </div>
</section>
<div class="wrap">
  <div class="cs-cover" style="view-transition-name:cover-{p['slug']}"><img src="{p['cover']}" alt="{e(p['title'])}: panoramica del progetto" {cover_size(p)}></div>
  {render_story(p["story"]) if p.get("story") else ""}
  {f'<div class="cs-body">{"".join(body)}</div>' if body else ""}
  {f'<div class="gallery">{"".join(gallery)}</div>' if gallery else ""}
  <a class="next" href="{nxt['slug']}.html"><span>Prossimo lavoro</span><strong>{e(nxt['title'])} {ARROW}</strong></a>
</div>
</main>
"""
    page += footer()
    (ROOT / f'{p["slug"]}.html').write_text(page, encoding="utf-8")


def build_sitemap(projects):
    urls = [f"{SITE}/"] + [f'{SITE}/{p["slug"]}.html' for p in projects]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    xml += "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")


if __name__ == "__main__":
    projects = json.loads((ROOT / "data/projects.json").read_text(encoding="utf-8"))
    build_index(projects)
    for i, p in enumerate(projects):
        build_case(p, projects[(i + 1) % len(projects)])
    build_sitemap(projects)
    print(f"Generati index.html e {len(projects)} case study.")
