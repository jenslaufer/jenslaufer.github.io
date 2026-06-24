#!/usr/bin/env python3
"""Static-site generator for jenslaufer.com — paper design, no Jekyll.

Reproduces Jekyll's exact URL scheme so every existing URL stays identical:
  post  -> /<category>/<...>/<slug>.html   (permalink: none = /:categories/:title.html)
  menu  -> /menu/<name>.html
  index -> /  + /page2/ /page3/  (jekyll-paginate, 5 per page)

Run:  .venv/bin/python build.py        # outputs to dist/
"""
import os, re, shutil, html, datetime, glob
import yaml
import markdown as md

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")
SITE_URL = "https://jenslaufer.com"
TITLE = "Jens Laufer"
DESCRIPTION = "writes about Software Development, Data Science, Entrepreneurship, Traveling and Sports"
AUTHOR = "Jens Laufer"
PER_PAGE = 5

MENU = [("About", "/menu/about.html"), ("Writing", "/menu/writing.html"), ("Contact", "/menu/contact.html")]
SOCIAL = [
    ("github", "https://www.github.com/jenslaufer"),
    ("twitter", "https://twitter.com/jenslaufer"),
    ("linkedin", "http://linkedin.com/in/jens-laufer-2b55b13"),
    ("envelope", "mailto:jens.laufer@gmail.com"),
    ("rss-square", "/feed.xml"),
]

FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)
DATE_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$")


def parse(path):
    raw = open(path, encoding="utf-8").read()
    m = FM_RE.match(raw)
    if not m:
        return None, raw
    fm = yaml.safe_load(m.group(1)) or {}
    return fm, m.group(2)


def categories(fm):
    """Mirror Jekyll: a YAML list keeps items verbatim; a bare string splits on whitespace."""
    c = fm.get("categories", fm.get("category"))
    if not c:
        return []
    if isinstance(c, list):
        return [str(x) for x in c]
    return str(c).split()


def post_url(fname, fm):
    m = DATE_RE.match(fname)
    date = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    slug = m.group(4).replace(" ", "-")
    cats = categories(fm)
    path = "/" + "".join(c + "/" for c in cats) + slug + ".html"
    return path, date, slug


MD_EXT = ["extra", "sane_lists", "codehilite", "smarty"]


def render_md(text):
    return md.markdown(text, extensions=MD_EXT, extension_configs={"codehilite": {"guess_lang": False}})


BLOCK_RE = re.compile(r"<(style|script)\b[^>]*>.*?</\1>", re.S | re.I)


def strip_html(text):
    """Plain text from rendered HTML — drops <style>/<script> bodies, not just tags."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", BLOCK_RE.sub(" ", text))).strip()


def read_time(text):
    words = len(strip_html(text).split())
    if words < 180:
        return "less than 1 minute read"
    if words < 360:
        return "1 minute read"
    return f"{words // 180} minute read"


# ---------- templates ----------
def social_icons():
    return "".join(
        f'<a href="{l}" aria-label="{i}"><i class="fa fa-{i}"></i></a>' for i, l in SOCIAL
    )


def menu_nav():
    return "".join(f'<a href="{u}">{n}</a>' for n, u in MENU)


def page(title, body, *, description=None, canonical=None, og_type="website", lead=False, og_image=None):
    desc = html.escape(description or DESCRIPTION)
    can = canonical or "/"
    head_title = TITLE + " | " + DESCRIPTION if title == "Home" else f"{title} | {TITLE}"
    img_url = (og_image if str(og_image).startswith("http") else SITE_URL + og_image) if og_image else None
    img_tags = (f'\n<meta property="og:image" content="{img_url}">'
                f'\n<meta name="twitter:image" content="{img_url}">' if img_url else "")
    twitter_card = "summary_large_image" if img_url else "summary"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(head_title)}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE_URL}{can}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{SITE_URL}{can}">
<meta property="og:site_name" content="{TITLE}">{img_tags}
<meta name="twitter:card" content="{twitter_card}">
<link rel="alternate" type="application/atom+xml" title="{TITLE}" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..500&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<link rel="stylesheet" href="/assets/css/main.css">
</head>
<body>
<div class="wrap">
<header class="masthead">
  <a class="masthead-title" href="/">{TITLE}</a>
  <div class="masthead-subtitle">{DESCRIPTION}</div>
  <nav class="menu">{menu_nav()}</nav>
</header>
<main class="content{' lead' if lead else ''}">
{body}
</main>
<footer class="footer">
  <nav class="social">{social_icons()}</nav>
  <div class="colophon"><a href="/menu/about.html">{TITLE} — {DESCRIPTION}</a></div>
</footer>
</div>
</body>
</html>
"""


def date_long(d):
    suf = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd", 31: "st"}.get(d.day, "th")
    return d.strftime(f"%B {d.day}{suf}, %Y")


def write(relpath, content):
    p = os.path.join(OUT, relpath.lstrip("/"))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


# ---------- build ----------
def build():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    posts = []
    for path in glob.glob(os.path.join(ROOT, "_posts", "*.md")):
        fname = os.path.basename(path)
        if not DATE_RE.match(fname):
            continue  # drafts / undated files are not published
        fm, body = parse(path)
        url, date, slug = post_url(fname, fm)
        h = render_md(body)
        posts.append({
            "url": url, "date": date, "slug": slug,
            "title": fm.get("title", slug), "subtitle": fm.get("subtitle"),
            "image": fm.get("image"), "image_subtitle": fm.get("image_subtitle"),
            "html": h, "rt": read_time(h), "author": fm.get("author", AUTHOR),
            "og_image": fm.get("og_image") or fm.get("image"),
        })
    posts.sort(key=lambda p: p["date"], reverse=True)

    # --- posts ---
    for p in posts:
        sub = f'<p class="post-subtitle">{html.escape(p["subtitle"])}</p>' if p["subtitle"] else ""
        img = ""
        if p["image"]:
            cap = f'<figcaption>{html.escape(p["image_subtitle"])}</figcaption>' if p["image_subtitle"] else ""
            img = f'<figure class="post-hero"><img src="{p["image"]}" alt="">{cap}</figure>'
        tweet = ("https://twitter.com/intent/tweet?text=" +
                 html.escape(p["title"]) + "&url=" + SITE_URL + p["url"])
        body = f"""<article class="post">
<p class="kicker">{p['date'].strftime('%B %-d, %Y')} · {p['rt']}</p>
<h1>{html.escape(p['title'])}</h1>
{sub}
{img}
<div class="post-body">
{p['html']}
</div>
<p class="byline">Written on {date_long(p['date'])} by {html.escape(p['author'])}</p>
<p class="share"><a href="{tweet}">Feel free to share &rarr;</a></p>
</article>"""
        write(p["url"], page(p["title"], body, description=p["subtitle"] or p["title"],
                             canonical=p["url"], og_type="article", lead=True,
                             og_image=p["og_image"]))

    # --- index pagination (/, /page2/, /page3/) ---
    pages = [posts[i:i + PER_PAGE] for i in range(0, len(posts), PER_PAGE)] or [[]]
    n = len(pages)
    for idx, chunk in enumerate(pages):
        items = []
        for p in chunk:
            sub = f'<p class="card-subtitle">{html.escape(p["subtitle"])}</p>' if p["subtitle"] else ""
            excerpt = strip_html(p["html"])
            excerpt = (excerpt[:300].rsplit(" ", 1)[0] + "…") if len(excerpt) > 300 else excerpt
            items.append(f"""<article class="card">
<p class="kicker">{p['date'].strftime('%B %-d, %Y')} · {p['rt']}</p>
<h2><a href="{p['url']}">{html.escape(p['title'])}</a></h2>
{sub}
<p class="card-excerpt">{html.escape(excerpt)} <a href="{p['url']}">Read more</a></p>
</article>""")
        # pager: newer = lower idx, older = higher idx (matches Jekyll Older/Newer)
        older = f'<a class="pg" href="{"/page" + str(idx + 2) + "/" if idx + 1 < n else ""}">Older</a>' if idx + 1 < n else '<span class="pg off">Older</span>'
        if idx == 0:
            newer = '<span class="pg off">Newer</span>'
        elif idx == 1:
            newer = '<a class="pg" href="/">Newer</a>'
        else:
            newer = f'<a class="pg" href="/page{idx}/">Newer</a>'
        pager = f'<nav class="pagination">{older}{newer}</nav>'
        body = '<div class="cards">' + "\n".join(items) + "</div>" + pager
        rel = "index.html" if idx == 0 else f"page{idx + 1}/index.html"
        can = "/" if idx == 0 else f"/page{idx + 1}/"
        write(rel, page("Home", body, canonical=can))

    # --- menu pages ---
    for name, fname in [("about", "About me"), ("contact", "Contact")]:
        fm, mbody = parse(os.path.join(ROOT, "menu", f"{name}.md"))
        img = f'<figure class="post-hero"><img src="{fm.get("image")}" alt=""></figure>' if fm.get("image") else ""
        body = f'<article class="post"><h1>{html.escape(fm.get("title", fname))}</h1>{img}<div class="post-body">{render_md(mbody)}</div></article>'
        write(f"menu/{name}.html", page(fm.get("title", fname), body, canonical=f"/menu/{name}.html", lead=True))

    # writing index (all posts grouped by year)
    rows, cur = [], None
    for p in posts:
        y = p["date"].year
        if y != cur:
            rows.append(f'<h3 class="year">{y}</h3>')
            cur = y
        rows.append(f'<li><a href="{p["url"]}">{html.escape(p["title"])}</a>'
                    f'<span class="li-date">{p["date"].strftime("%B %-d")} · {p["rt"]}</span></li>')
    body = f'<article class="post"><h1>Writing</h1><ul class="archive">{"".join(rows)}</ul></article>'
    write("menu/writing.html", page("Writing", body, canonical="/menu/writing.html", lead=True))

    # --- sitemap + feed ---
    urls = ["/"] + [p["url"] for p in posts] + ["/menu/about.html", "/menu/contact.html", "/menu/writing.html"]
    urls += [f"/page{i+1}/" for i in range(1, n)]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"<url><loc>{SITE_URL}{u}</loc></url>")
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm))

    updated = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    feed = ['<?xml version="1.0" encoding="utf-8"?>',
            '<feed xmlns="http://www.w3.org/2005/Atom">',
            f"<title>{TITLE}</title><subtitle>{DESCRIPTION}</subtitle>",
            f'<link href="{SITE_URL}/feed.xml" rel="self"/><link href="{SITE_URL}/"/>',
            f"<updated>{updated}</updated><id>{SITE_URL}/</id>",
            f"<author><name>{AUTHOR}</name></author>"]
    for p in posts[:20]:
        d = p["date"].strftime("%Y-%m-%dT00:00:00Z")
        feed.append(f"<entry><title>{html.escape(p['title'])}</title>"
                    f'<link href="{SITE_URL}{p["url"]}"/><id>{SITE_URL}{p["url"]}</id>'
                    f"<updated>{d}</updated><published>{d}</published>"
                    f'<content type="html">{html.escape(p["html"][:500])}</content></entry>')
    feed.append("</feed>")
    write("feed.xml", "\n".join(feed))

    # --- static passthrough ---
    for d in ["assets/img", "figure"]:
        src = os.path.join(ROOT, d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(OUT, d), dirs_exist_ok=True)
    for f in ["favicon.ico", "CNAME"]:
        if os.path.exists(os.path.join(ROOT, f)):
            shutil.copy(os.path.join(ROOT, f), os.path.join(OUT, f))
    # keep its-just-math microsite untouched
    if os.path.isdir(os.path.join(ROOT, "its-just-math")):
        shutil.copytree(os.path.join(ROOT, "its-just-math"),
                        os.path.join(OUT, "its-just-math"), dirs_exist_ok=True)
    open(os.path.join(OUT, ".nojekyll"), "w").close()
    # 404
    write("404.html", page("Not found", '<article class="post"><h1>Page not found</h1>'
                           '<p class="post-body">The page you were looking for doesn\'t exist. '
                           '<a href="/">Back to the front page</a>.</p></article>', lead=True))
    # css written separately by build_css()
    build_css()

    print(f"Built {len(posts)} posts, {n} index pages -> {OUT}")
    return posts


def build_css():
    css = open(os.path.join(ROOT, "assets", "css", "paper.css"), encoding="utf-8").read()
    os.makedirs(os.path.join(OUT, "assets", "css"), exist_ok=True)
    open(os.path.join(OUT, "assets", "css", "main.css"), "w", encoding="utf-8").write(css)


if __name__ == "__main__":
    build()
