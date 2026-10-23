"""Every product page served under jenslaufer.com/<repo>/ needs a link from a
page Google already crawls. Measured 2026-10-23: /invoicegrab-site/ was
"URL is unknown to Google" two months after its sitemap was submitted, while
the homepage was crawled on 2026-10-21. Run: python3 tests/test_microsites.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")


def read(rel):
    with open(os.path.join(DIST, rel), encoding="utf-8") as f:
        return f.read()


def main():
    subprocess.run([sys.executable, "build.py"], cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    fails = []
    for page in ["index.html", "menu/about.html", "menu/writing.html"]:
        if 'href="/invoicegrab-site/"' not in read(page):
            fails.append(f"{page}: no link to /invoicegrab-site/")
    if "<loc>https://jenslaufer.com/invoicegrab-site/</loc>" not in read("sitemap.xml"):
        fails.append("sitemap.xml: /invoicegrab-site/ missing")
    for f in fails:
        print("FAIL", f)
    print("OK" if not fails else f"{len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
