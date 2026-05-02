# GitHub Wrapped 🎁

A fun “year‑in‑review” style report for my GitHub activity.  
This project fetches my GitHub stats and generates a custom SVG report that auto‑updates daily.

## ✅ What it shows
- Top repositories
- Most used languages
- Busiest days of the week
- Total commits, PRs, and issues
- A shareable SVG report

## ✅ Auto‑updated report
![GitHub Wrapped](https://raw.githubusercontent.com/juni2003/github-wrapped/main/output/github_wrapped.svg)

## ✅ How it works
1. GitHub Actions runs daily.
2. Python scripts call the GitHub API.
3. Data is processed into a clean SVG.
4. The SVG is pushed to `/output/`.

## ✅ Setup
- Add a GitHub token as a secret: `GH_TOKEN`
- Push code to `main`
- Action updates every day

---

Made with Python + GitHub Actions
