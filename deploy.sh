#!/usr/bin/env bash
# Rebuild the static site and stage it at the repo root for GitHub Pages.
# GitHub Pages serves jenslaufer.github.io from master root. `.nojekyll`
# disables Jekyll so files are served verbatim.
set -euo pipefail
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install --quiet markdown pygments pyyaml
.venv/bin/python build.py
cp -r dist/. .
touch .nojekyll
echo "Built. Review 'git status', then: git add -A && git commit && git push origin master"
