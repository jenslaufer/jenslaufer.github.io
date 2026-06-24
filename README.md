# jenslaufer.com

Personal blog of Jens Laufer. Static site, **paper design** (Newsreader + IBM Plex Mono,
warm paper palette — matching the [138-Fehlschläge essay](https://jenslaufer.com/138-fehlschlaege/)).

No Jekyll. A small Python generator (`build.py`) renders Markdown to static HTML and
reproduces the **exact** legacy URL scheme, so every existing URL stays identical.

## Structure

| Path | Purpose |
|---|---|
| `_posts/*.md` | Posts — `YYYY-MM-DD-slug.md` with YAML front matter (`title`, `subtitle`, `categories`, `image`) |
| `menu/*.md` | Static pages (About, Contact). `writing` is auto-generated. |
| `assets/css/paper.css` | The design (source). `build.py` copies it to `assets/css/main.css`. |
| `assets/img/`, `figure/` | Images |
| `its-just-math/` | Standalone microsite (untouched) |
| `build.py` | Generator → `dist/` |
| `deploy.sh` | Build + stage at root for GitHub Pages |

## URL scheme (preserved from Jekyll)

`permalink: none` → `/<category>/.../<slug>.html`. A YAML **list** category keeps spaces
(`/data analysis/…`); a bare **string** splits on whitespace (`/data/science/…`). The
generator mirrors this exactly; output is checked URL-for-URL against the live sitemap.

## Build & deploy

```bash
./deploy.sh                 # rebuild + stage static files at repo root
git add -A && git commit -m "content: ..." && git push origin master
```

GitHub Pages serves `master` root. `.nojekyll` keeps Pages from running Jekyll.

## New post

Add `_posts/YYYY-MM-DD-your-slug.md`:

```yaml
---
title: "Your title"
subtitle: "Optional standfirst"
categories: data science      # or a YAML list for a single spaced category
image: /assets/img/hero.jpg   # optional
---
Body in Markdown.
```
