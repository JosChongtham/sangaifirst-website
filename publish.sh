#!/bin/sh
# Rebuild the site and publish it to GitHub Pages (sangaifirst.com).
# Usage: ./publish.sh "What changed"
set -e
cd "$(dirname "$0")"
python3 source/build_site.py
git add -A
git commit -m "${1:-Update site}" || echo "Nothing new to commit."
git push origin main
git push origin "$(git subtree split --prefix site main)":refs/heads/gh-pages --force
echo "Published. Live at https://sangaifirst.com in a minute or two."
