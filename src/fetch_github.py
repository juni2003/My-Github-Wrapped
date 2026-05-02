import os
import requests
from collections import Counter
from datetime import datetime, timedelta

GITHUB_API = "https://api.github.com"
USERNAME = os.getenv("GITHUB_USER")

def gh_request(url, token):
    headers = {"Authorization": f"token {token}"} if token else {}
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
    for r in repos[:20]:
        langs = gh_request(r["languages_url"], token)
        for lang, bytes_ in langs.items():
            lang_counter[lang] += bytes_
    return lang_counter

def get_user_events(token):
    events = []
    page = 1
    while True:
        data = gh_request(f"{GITHUB_API}/users/{USERNAME}/events?per_page=100&page={page}", token)
        if not data:
            break
        events.extend(data)
        page += 1
    return events

def summarize_events(events):
    commits = 0
    prs = 0
    issues = 0
    days = Counter()

    for e in events:
        created = e.get("created_at")
        if created:
            day = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").strftime("%A")
            days[day] += 1

        if e["type"] == "PushEvent":
            commits += sum(len(c["shas"]) if "shas" in c else 1 for c in e["payload"].get("commits", []))
        elif e["type"] == "PullRequestEvent":
            prs += 1
        elif e["type"] == "IssuesEvent":
            issues += 1

    busiest_day = days.most_common(1)[0][0] if days else "N/A"
    return commits, prs, issues, busiest_day

def fetch_all(token):
    repos = get_repos(token)
    languages = get_languages(repos, token)
    events = get_user_events(token)
    commits, prs, issues, busiest_day = summarize_events(events)

    top_repos = sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)[:5]
    top_repos = [r["name"] for r in top_repos]

    top_langs = [lang for lang, _ in languages.most_common(5)]

    return {
        "user": USERNAME,
        "total_repos": len(repos),
        "commits": commits,
        "prs": prs,
        "issues": issues,
        "busiest_day": busiest_day,
        "top_repos": top_repos,
        "top_langs": top_langs
    }
