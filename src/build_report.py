import os
from fetch_github import fetch_all

TEMPLATE_PATH = "src/templates/report.svg"
OUTPUT_PATH = "output/github_wrapped.svg"

def build_svg(data):
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        svg = f.read()

    svg = svg.replace("{{USER}}", data["user"])
    svg = svg.replace("{{TOTAL_REPOS}}", str(data["total_repos"]))
    svg = svg.replace("{{COMMITS}}", str(data["commits"]))
    svg = svg.replace("{{PRS}}", str(data["prs"]))
    svg = svg.replace("{{ISSUES}}", str(data["issues"]))
    svg = svg.replace("{{BUSIEST_DAY}}", data["busiest_day"])
    svg = svg.replace("{{TOP_REPOS}}", ", ".join(data["top_repos"]) or "N/A")
    svg = svg.replace("{{TOP_LANGS}}", ", ".join(data["top_langs"]) or "N/A")

    os.makedirs("output", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(svg)

if __name__ == "__main__":
    token = os.getenv("GH_TOKEN")
    data = fetch_all(token)
    build_svg(data)
