#!/usr/bin/env python3
import os
import json
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROBLEMS_DIR = REPO_ROOT

def load_stats():
    """Load stats.json"""
    stats_file = REPO_ROOT / "stats.json"
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            return json.load(f)
    return {'leetcode': {'easy': 0, 'medium': 0, 'hard': 0, 'shas': {}}}

def parse_problems():
    """Parse problem directories"""
    problems = []
    stats_data = load_stats()
    shas = stats_data.get('leetcode', {}).get('shas', {})
    
    try:
        for item in sorted(PROBLEMS_DIR.iterdir()):
            if not item.is_dir():
                continue
            if not re.match(r'^\d{4}-', item.name):
                continue
                
            problem_name = item.name
            readme_path = item / "README.md"
            
            if not readme_path.exists():
                continue
            
            problem_stats = shas.get(problem_name, {})
            difficulty = problem_stats.get('difficulty', 'medium').upper()
            title = problem_name.split('-', 1)[1].replace('-', ' ').title()
            
            solution_file = None
            try:
                for file in item.iterdir():
                    if file.is_file() and file.name.endswith(('.cpp', '.java', '.py', '.js', '.go')):
                        solution_file = file.name
                        break
            except:
                pass
            
            problems.append({
                'id': problem_name.split('-')[0],
                'folder': problem_name,
                'title': title,
                'difficulty': difficulty,
                'solution': solution_file or 'N/A',
                'language': solution_file.split('.')[-1].upper() if solution_file else '—'
            })
    except Exception as e:
        print(f"Error parsing problems: {e}")
    
    return sorted(problems, key=lambda x: int(x['id']))

def calculate_stats(problems):
    """Calculate stats"""
    stats = {
        'total': len(problems),
        'easy': len([p for p in problems if p['difficulty'] == 'EASY']),
        'medium': len([p for p in problems if p['difficulty'] == 'MEDIUM']),
        'hard': len([p for p in problems if p['difficulty'] == 'HARD']),
        'languages': defaultdict(int)
    }
    
    for problem in problems:
        if problem['language'] != '—':
            lang_key = problem['language'].lower()
            stats['languages'][lang_key] += 1
    
    return stats

def generate_problems_table(problems):
    """Generate markdown table"""
    if not problems:
        return "No problems found yet.\n"
    
    table = "| # | Title | Difficulty | Language | Solution |\n"
    table += "|---|-------|-----------|----------|----------|\n"
    
    for p in problems:
        diff_emoji = '🟢' if p['difficulty'] == 'EASY' else ('🟡' if p['difficulty'] == 'MEDIUM' else '🔴')
        link = f"[{p['folder']}]({p['folder']})"
        sol_link = f"[{p['solution']}]({p['folder']}/{p['solution']})" if p['solution'] != 'N/A' else 'N/A'
        table += f"| {p['id']} | {link} | {diff_emoji} {p['difficulty']} | {p['language']} | {sol_link} |\n"
    
    return table

def generate_language_stats(stats):
    """Generate language distribution"""
    if not stats['languages']:
        return "### 💻 Language Distribution\n\nNo language data yet.\n\n"
    
    total = sum(stats['languages'].values())
    output = "### 💻 Language Distribution\n\n"
    
    for lang in ['cpp', 'java', 'python', 'js', 'go']:
        count = stats['languages'].get(lang, 0)
        if count > 0:
            percentage = (count / total) * 100
            bar_length = int(percentage / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            output += f"- **{lang.upper()}**: {count} ({percentage:.1f}%) `{bar}`\n"
    
    output += "\n"
    return output

def generate_difficulty_distribution(stats):
    """Generate difficulty breakdown"""
    total = stats['total']
    if total == 0:
        return "### 📊 Difficulty Breakdown\n\nNo problems solved yet.\n\n"
    
    output = "### 📊 Difficulty Breakdown\n\n"
    output += f"```\n"
    output += f"  Easy   {stats['easy']:3d}  {'█' * max(1, stats['easy'] // 2)}  ({stats['easy']/total*100:.1f}%)\n"
    output += f"  Medium {stats['medium']:3d}  {'█' * max(1, stats['medium'] // 2)}  ({stats['medium']/total*100:.1f}%)\n"
    output += f"  Hard   {stats['hard']:3d}  {'█' * max(1, stats['hard'] // 2)}  ({stats['hard']/total*100:.1f}%)\n"
    output += f"```\n\n"
    return output

def generate_stats_badges(stats):
    """Generate badges"""
    badges = f"![Problems Solved](https://img.shields.io/badge/Problems%20Solved-{stats['total']}-blue?style=for-the-badge)\n"
    badges += f"![Easy](https://img.shields.io/badge/Easy-{stats['easy']}-green?style=for-the-badge)\n"
    badges += f"![Medium](https://img.shields.io/badge/Medium-{stats['medium']}-yellow?style=for-the-badge)\n"
    badges += f"![Hard](https://img.shields.io/badge/Hard-{stats['hard']}-red?style=for-the-badge)\n\n"
    return badges

def generate_quick_stats(stats):
    """Generate quick stats"""
    total = stats['total']
    if total == 0:
        easy_pct = medium_pct = hard_pct = 0
    else:
        easy_pct = (stats['easy'] / total * 100)
        medium_pct = (stats['medium'] / total * 100)
        hard_pct = (stats['hard'] / total * 100)
    
    langs = ', '.join(map(str.upper, stats['languages'].keys())) if stats['languages'] else 'N/A'
    
    output = "## 📈 Quick Stats\n\n"
    output += f"| Metric | Value |\n"
    output += f"|--------|-------|\n"
    output += f"| **Total Problems** | {total} |\n"
    output += f"| **Easy** | {stats['easy']} ({easy_pct:.1f}%) |\n"
    output += f"| **Medium** | {stats['medium']} ({medium_pct:.1f}%) |\n"
    output += f"| **Hard** | {stats['hard']} ({hard_pct:.1f}%) |\n"
    output += f"| **Languages Used** | {langs} |\n"
    output += f"| **Last Updated** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC |\n\n"
    
    return output

def generate_readme(problems, stats):
    """Generate complete README"""
    readme = """# 💻 LeetCode Solutions

> A comprehensive collection of LeetCode problems solved across multiple programming languages.  
> Automatically updated with fresh statistics using GitHub Actions.

---

"""
    
    readme += generate_stats_badges(stats)
    readme += generate_quick_stats(stats)
    readme += generate_difficulty_distribution(stats)
    readme += generate_language_stats(stats)
    readme += "## 📚 Problem Solutions\n\n"
    readme += generate_problems_table(problems)
    
    readme += f"""
---

## 🚀 About This Repository

This repository is auto-updated using **GitHub Actions**. Every time a new problem is committed, the statistics and tables are automatically refreshed.

### How to Use
- Browse problems by difficulty level
- Click on any problem number to see the solution
- Solutions include explanations and multiple approaches

### Statistics Auto-Update
- ✅ Runs on every new commit
- ✅ Daily scheduled updates
- ✅ Real-time problem count
- ✅ Language distribution tracking

### Technologies Used
- **Languages**: C++, Java, Python
- **Concepts**: Arrays, Linked Lists, Trees, Graphs, DP, Greedy, etc.

---

**Generated on**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC  
**Last Update**: Via GitHub Actions Workflow
"""
    
    return readme

def main():
    print("🔍 Parsing LeetCode problems...")
    problems = parse_problems()
    print(f"📊 Found {len(problems)} problems")
    
    stats = calculate_stats(problems)
    print(f"✅ Easy: {stats['easy']}, Medium: {stats['medium']}, Hard: {stats['hard']}")
    
    print("✍️  Generating README...")
    readme_content = generate_readme(problems, stats)
    
    readme_path = REPO_ROOT / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print("✅ README updated successfully!")

if __name__ == "__main__":
    main()
