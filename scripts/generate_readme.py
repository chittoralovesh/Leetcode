#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import re

REPO_ROOT = Path(__file__).parent.parent

def load_stats():
    stats_file = REPO_ROOT / "stats.json"
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            return json.load(f)
    return {'leetcode': {'shas': {}}}

def parse_problems():
    problems = []
    stats_data = load_stats()
    shas = stats_data.get('leetcode', {}).get('shas', {})
    
    for item in sorted(REPO_ROOT.iterdir()):
        if not item.is_dir():
            continue
        if not re.match(r'^\d{4}-', item.name):
            continue
        readme_path = item / "README.md"
        if not readme_path.exists():
            continue
        
        problem_stats = shas.get(item.name, {})
        difficulty = problem_stats.get('difficulty', 'medium').upper()
        title = item.name.split('-', 1)[1].replace('-', ' ').title()
        
        solution_file = None
        for file in item.iterdir():
            if file.is_file() and file.name.endswith(('.cpp', '.java', '.py', '.js', '.go')):
                solution_file = file.name
                break
        
        problems.append({
            'id': item.name.split('-')[0],
            'folder': item.name,
            'title': title,
            'difficulty': difficulty,
            'solution': solution_file or 'N/A',
            'language': solution_file.split('.')[-1].upper() if solution_file else '-'
        })
    
    return sorted(problems, key=lambda x: int(x['id']))

def calculate_stats(problems):
    stats = {
        'total': len(problems),
        'easy': len([p for p in problems if p['difficulty'] == 'EASY']),
        'medium': len([p for p in problems if p['difficulty'] == 'MEDIUM']),
        'hard': len([p for p in problems if p['difficulty'] == 'HARD']),
        'languages': defaultdict(int)
    }
    for p in problems:
        if p['language'] != '-':
            stats['languages'][p['language'].lower()] += 1
    return stats

def build_table(problems):
    if not problems:
        return "No problems yet.\n"
    table = "| # | Title | Difficulty | Language |\n|---|---|---|---|\n"
    for p in problems:
        emoji = '🟢' if p['difficulty'] == 'EASY' else ('🟡' if p['difficulty'] == 'MEDIUM' else '🔴')
        link = f"[{p['folder']}]({p['folder']})"
        table += f"| {p['id']} | {link} | {emoji} {p['difficulty']} | {p['language']} |\n"
    return table

def main():
    problems = parse_problems()
    stats = calculate_stats(problems)
    
    readme = "# 💻 LeetCode Solutions\n\n"
    readme += f"![Total](https://img.shields.io/badge/Total-{stats['total']}-blue)\n"
    readme += f"![Easy](https://img.shields.io/badge/Easy-{stats['easy']}-green)\n"
    readme += f"![Medium](https://img.shields.io/badge/Medium-{stats['medium']}-yellow)\n"
    readme += f"![Hard](https://img.shields.io/badge/Hard-{stats['hard']}-red)\n\n"
    readme += f"**Total Problems:** {stats['total']}\n\n"
    readme += "## Problems\n\n"
    readme += build_table(problems)
    readme += f"\n\n_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC_\n"
    
    with open(REPO_ROOT / "README.md", 'w') as f:
        f.write(readme)
    
    print(f"Done! {stats['total']} problems processed.")

if __name__ == "__main__":
    main()
