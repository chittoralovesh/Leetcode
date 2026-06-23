<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=26&pause=1000&color=58A6FF&center=true&vCenter=true&width=800&lines=LeetCode+Journey+%F0%9F%9A%80;50%2B+Problems+Solved;Python+%7C+C%2B%2B+%7C+Java;Preparing+for+SDE+Internships" />

</div>

#!/usr/bin/env python3
"""
Generate an attractive, auto-updating README for the LeetCode repo.
- Parses problem folders + stats.json for difficulty/language
- Fetches topic tags from LeetCode's public GraphQL API (cached to topics_cache.json)
- Renders a polished README with badges, collapsible topic sections, and a full table
"""

import json
import re
import time
from datetime import datetime
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
CACHE_FILE = REPO_ROOT / "topics_cache.json"
LEETCODE_GRAPHQL = "https://leetcode.com/graphql"

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ---------- Data loading ----------

def load_stats():
    stats_file = REPO_ROOT / "stats.json"
    if stats_file.exists():
        with open(stats_file, "r") as f:
            return json.load(f)
    return {"leetcode": {"shas": {}}}


def load_topics_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_topics_cache(cache):
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2, sort_keys=True)
    except Exception as e:
        print(f"Warning: could not save topics cache: {e}")


def fetch_topics_for_slug(slug):
    """Query LeetCode's public GraphQL endpoint for topic tags. Best-effort only."""
    if not HAS_REQUESTS:
        return []

    query = """
    query questionTopicTags($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        topicTags { name }
      }
    }
    """
    try:
        resp = requests.post(
            LEETCODE_GRAPHQL,
            json={"query": query, "variables": {"titleSlug": slug}},
            headers={
                "Content-Type": "application/json",
                "Referer": f"https://leetcode.com/problems/{slug}/",
                "User-Agent": "Mozilla/5.0 (README-bot)",
            },
            timeout=10,
        )
        data = resp.json()
        tags = data["data"]["question"]["topicTags"]
        return [t["name"] for t in tags]
    except Exception as e:
        print(f"  (could not fetch topics for '{slug}': {e})")
        return []


# ---------- Parsing ----------

def parse_problems(topics_cache):
    problems = []
    stats_data = load_stats()
    shas = stats_data.get("leetcode", {}).get("shas", {})

    folders = [
        item for item in sorted(REPO_ROOT.iterdir())
        if item.is_dir() and re.match(r"^\d{4}-", item.name)
    ]

    new_lookups = 0
    for item in folders:
        readme_path = item / "README.md"
        if not readme_path.exists():
            continue

        folder_name = item.name
        slug = folder_name.split("-", 1)[1] if "-" in folder_name else folder_name
        title = slug.replace("-", " ").title()

        problem_stats = shas.get(folder_name, {})
        difficulty = problem_stats.get("difficulty", "medium").upper()

        solution_file = None
        for file in item.iterdir():
            if file.is_file() and file.name.endswith((".cpp", ".java", ".py", ".js", ".go")):
                solution_file = file.name
                break

        # Topics: use cache, fetch if missing (rate-limit friendly)
        if slug in topics_cache:
            topics = topics_cache[slug]
        else:
            topics = fetch_topics_for_slug(slug)
            topics_cache[slug] = topics
            new_lookups += 1
            time.sleep(0.4)  # be polite to LeetCode's API

        problems.append({
            "id": folder_name.split("-")[0],
            "folder": folder_name,
            "title": title,
            "difficulty": difficulty,
            "solution": solution_file or "N/A",
            "language": solution_file.split(".")[-1].upper() if solution_file else "—",
            "topics": topics,
        })

    if new_lookups:
        print(f"Fetched topics for {new_lookups} new problem(s).")

    return sorted(problems, key=lambda x: int(x["id"]))


def calculate_stats(problems):
    stats = {
        "total": len(problems),
        "easy": len([p for p in problems if p["difficulty"] == "EASY"]),
        "medium": len([p for p in problems if p["difficulty"] == "MEDIUM"]),
        "hard": len([p for p in problems if p["difficulty"] == "HARD"]),
        "languages": defaultdict(int),
        "topics": defaultdict(int),
    }
    for p in problems:
        if p["language"] != "—":
            stats["languages"][p["language"].lower()] += 1
        for t in p["topics"]:
            stats["topics"][t] += 1
    return stats


# ---------- Rendering helpers ----------

DIFF_EMOJI = {"EASY": "🟢", "MEDIUM": "🟡", "HARD": "🔴"}
LANG_BADGE_COLOR = {
    "CPP": "00599C", "JAVA": "ED8B00", "PY": "3776AB",
    "PYTHON": "3776AB", "JS": "F7DF1E", "GO": "00ADD8",
}


def shield(label, value, color):
    label_enc = label.replace(" ", "%20")
    value_enc = str(value).replace(" ", "%20")
    return (
        f'<img src="https://img.shields.io/badge/'
        f'{label_enc}-{value_enc}-{color}?style=for-the-badge" '
        f'alt="{label}" />'
    )


def render_badges(stats):
    badges = [
        shield("Total Solved", stats["total"], "5865F2"),
        shield("Easy", stats["easy"], "2ECC71"),
        shield("Medium", stats["medium"], "F1C40F"),
        shield("Hard", stats["hard"], "E74C3C"),
    ]
    return '<p align="center">\n' + "\n".join(badges) + "\n</p>\n"


def render_lang_badges(stats):
    if not stats["languages"]:
        return ""

    badges = []
    for lang, count in sorted(
        stats["languages"].items(),
        key=lambda x: -x[1]
    ):
        color = LANG_BADGE_COLOR.get(lang.upper(), "777777")
        badges.append(
            shield(lang.upper(), f"{count} solved", color)
        )

    return '<p align="center">\n' + "\n".join(badges) + "\n</p>\n"


def render_difficulty_bars(stats):
    total = stats["total"] or 1
    lines = ["```text"]
    for label, key, emoji in [("Easy", "easy", "🟢"), ("Medium", "medium", "🟡"), ("Hard", "hard", "🔴")]:
        count = stats[key]
        pct = count / total * 100
        filled = max(1, round(pct / 5)) if count else 0
        bar = "█" * filled + "░" * (20 - filled)
        lines.append(f"{emoji} {label:<7} {count:>3}  {bar}  {pct:5.1f}%")
    lines.append("```")
    return "\n".join(lines) + "\n"


def render_topic_sections(problems, stats):
    """Collapsible <details> block per topic, sorted by problem count."""
    topic_map = defaultdict(list)
    for p in problems:
        for t in p["topics"]:
            topic_map[t].append(p)

    if not topic_map:
        return (
            "_Topic tags will appear here automatically once fetched from LeetCode "
            "on the next workflow run._\n"
        )

    out = []
    for topic, plist in sorted(topic_map.items(), key=lambda x: -len(x[1])):
        out.append(f"<details>\n<summary><b>{topic}</b> &nbsp;\u00b7&nbsp; {len(plist)} problem(s)</summary>\n")
        out.append("\n| # | Problem | Difficulty |")
        out.append("|---|---|---|")
        for p in sorted(plist, key=lambda x: int(x["id"])):
            emoji = DIFF_EMOJI.get(p["difficulty"], "⚪")
            out.append(f"| {p['id']} | [{p['title']}]({p['folder']}) | {emoji} {p['difficulty']} |")
        out.append("\n</details>\n")
    return "\n".join(out)


def render_full_table(problems):
    if not problems:
        return "No problems found yet.\n"
    table = ["| # | Title | Difficulty | Topics | Language |", "|---|---|---|---|---|"]
    for p in problems:
        emoji = DIFF_EMOJI.get(p["difficulty"], "⚪")
        link = f"[{p['title']}]({p['folder']})"
        topics_str = ", ".join(p["topics"][:3]) if p["topics"] else "—"
        if len(p["topics"]) > 3:
            topics_str += f" +{len(p['topics']) - 3}"
        table.append(f"| {p['id']} | {link} | {emoji} {p['difficulty']} | {topics_str} | {p['language']} |")
    return "\n".join(table) + "\n"


# ---------- Main README assembly ----------

def generate_readme(problems, stats):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    top_topics = sorted(stats["topics"].items(), key=lambda x: -x[1])[:5]
    top_topics_str = ", ".join(f"`{t}` ({c})" for t, c in top_topics) if top_topics else "—"

    readme = f"""<div align="center">

# 💻 LeetCode Solutions

### A continuously growing, auto-tracked collection of solved problems

{render_badges(stats)}
{render_lang_badges(stats)}

</div>

---

## 📈 Snapshot

| | |
|---|---|
| **Total problems solved** | {stats['total']} |
| **Languages used** | {', '.join(sorted(map(str.upper, stats['languages'].keys()))) or '—'} |
| **Most-practiced topics** | {top_topics_str} |
| **Last updated** | {now} UTC (auto via GitHub Actions) |

### Difficulty split

{render_difficulty_bars(stats)}

---

## 🗂️ Browse by topic

<sub>Click a topic to expand its problem list.</sub>

{render_topic_sections(problems, stats)}

---

## 📚 All problems

{render_full_table(problems)}

---

<div align="center">

### ⚙️ How this README stays fresh

This file is regenerated automatically by a GitHub Actions workflow every time a new
solution is pushed (and on a daily schedule). Topic tags are pulled live from
LeetCode's API and cached in `topics_cache.json` so repeat runs are fast.

_Generated on {now} UTC_

</div>
"""
    return readme


# ---------- Entry point ----------

def main():
    print("Loading topics cache...")
    topics_cache = load_topics_cache()

    print("Parsing LeetCode problems...")
    problems = parse_problems(topics_cache)
    save_topics_cache(topics_cache)

    print(f"Found {len(problems)} problems")
    stats = calculate_stats(problems)
    print(f"   Easy: {stats['easy']}  Medium: {stats['medium']}  Hard: {stats['hard']}")
    print(f"   Unique topics tracked: {len(stats['topics'])}")

    print("Generating README...")
    readme_content = generate_readme(problems, stats)

    with open(REPO_ROOT / "README.md", "w") as f:
        f.write(readme_content)

    print("README updated successfully!")


if __name__ == "__main__":
    main()
