import os
import requests
from collections import Counter
from datetime import datetime

GITHUB_API = "https://api.github.com"
USERNAME = os.getenv("GITHUB_USER")

def gh_request(url, token):
    headers = {}
    auth_token = token.strip() if token else ""
    if auth_token:
        scheme = "token"
        parts = auth_token.split(None, 1)
        prefix = parts[0].lower()
        if prefix in {"token", "bearer"}:
            scheme = "Bearer" if prefix == "bearer" else "token"
            if len(parts) != 2 or not parts[1].strip():
                raise ValueError("Token prefix provided without a token value.")
            auth_token = parts[1].strip()
        if auth_token:
            headers = {"Authorization": f"{scheme} {auth_token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def get_repos(token):
    repos = []
    page = 1
    while True:
        data = gh_request(f"{GITHUB_API}/users/{USERNAME}/repos?per_page=100&page={page}", token)
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_languages(repos, token):
    lang_counter = Counter()
    for r in repos[:30]:
        langs = gh_request(r["languages_url"], token)
        for lang, bytes_ in langs.items():
            lang_counter[lang] += bytes_
    return lang_counter

def get_totals_via_search(token):
    # Total PRs
    prs = gh_request(f"{GITHUB_API}/search/issues?q=type:pr+author:{USERNAME}", token)["total_count"]
    # Total issues
    issues = gh_request(f"{GITHUB_API}/search/issues?q=type:issue+author:{USERNAME}", token)["total_count"]
    # Total commits (may be approximate, needs token)
    commits = gh_request(f"{GITHUB_API}/search/commits?q=author:{USERNAME}", token)["total_count"]
    return commits, prs, issues

def get_busiest_day(token):
    # still from events (recent activity)
    events = []
    page = 1
    while True:
        data = gh_request(f"{GITHUB_API}/users/{USERNAME}/events?per_page=100&page={page}", token)
        if not data:
            break
        events.extend(data)
        page += 1
        if page > 3:
            break

    days = Counter()
    for e in events:
        created = e.get("created_at")
        if created:
            day = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").strftime("%A")
            days[day] += 1
    return days.most_common(1)[0][0] if days else "N/A"

def fetch_all(token):
    repos = get_repos(token)
    languages = get_languages(repos, token)
    commits, prs, issues = get_totals_via_search(token)
    busiest_day = get_busiest_day(token)

    top_repos = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
    top_repos = [r["name"] for r in top_repos]

    top_langs = [lang for lang, _ in languages.most_common(5)]

    total_stars = sum(r["stargazers_count"] for r in repos)

    return {
        "user": USERNAME,
        "total_repos": len(repos),
        "commits": commits,
        "prs": prs,
        "issues": issues,
        "busiest_day": busiest_day,
        "top_repos": top_repos,
        "top_langs": top_langs,
        "total_stars": total_stars
    }
