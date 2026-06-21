#!/usr/bin/env python3
"""
Generate interactive README with LeetCode stats
Parses problem directories and creates formatted output
"""

import os
import json
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# Get repo root
REPO_ROOT = Path(__file__).parent.parent
PROBLEMS_DIR = REPO_ROOT

def load_stats():
    """Load stats.json if it exists"""
    stats_file = REPO_ROOT / "stats.json"
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            return json.load(f)
    return {}

def parse_problems():
    """Parse problem directories and extract metadata"""
    problems = []
    stats_data = load_stats()
    leetcode_stats = stats_data.get('leetcode', {})
    shas = leetcode_stats.get('shas', {})
    
    for item in sorted(PROBLEMS_DIR.iterdir()):
        if item.is_dir() and re.match(r'^\d{4}-', item.name):
            problem_name = item.name
            readme_path = item / "README.md"
            
            # Get difficulty from stats.json
            problem_stats = shas.get(problem_name, {})
            difficulty = problem_stats.get('difficulty', 'medium').upper()
            
            # Parse problem title from folder name
            title = problem_name.split('-', 1)[1].replace('-', ' ').title()
            
            # Find solution file
            solution_file = None
            for file in item.iterdir():
                if file.name.endswith(('.cpp', '.java', '.py', '.js', '.go')):
                    solution_file = file.name
                    break
            
            if readme_path.exists():
                problems.append({
                    'id': problem_name.split('-')[0],
                    'folder': problem_name,
                    'title': title,
                    'difficulty': difficulty,
                    'solution': solution_file or 'N/A',
                    'language': solution_file.split('.')[-1] if solution_file else 'N/A'
                })
    
    return sorted(problems, key=lambda x: int(x['id']))

def calculate_stats(problems):
    """Calculate problem statistics"""
    stats = {
        'total': len(problems),
        'easy': len([p for p in problems if p['difficulty'] == 'EASY']),
        'medium': len([p for p in problems if p['difficulty'] == 'MEDIUM']),
        'hard': len([p for p in problems if p['difficulty'] == 'HARD']),
        'languages': defaultdict(int)
    }
    
    for problem in problems:
        if problem['language'] != 'N/A':
            stats['languages'][problem['language']] += 1
    
    return stats

def get_difficulty_color(difficulty):
    """Get emoji for difficulty"""
    colors = {
        'EASY': '🟢',
        'MEDIUM': '🟡',
        'HARD': '🔴'
    }
    return colors.get(difficulty, '⚪')

def generate_problems_table(problems):
    """Generate markdown table for problems"""
    table = "| # | Title | Difficulty | Language | Solution |\n"
    table += "|---|-------|-----------|----------|----------|\n"
    
    for p in problems:
        difficulty_emoji = get_difficulty_color(p['difficulty'])
        link = f"[{p['folder']}]({p['folder']})"
        lang = p['language'].upper() if p['language'] != 'N/A' else '—'
        sol_link = f"[{p['solution']}]({p['folder']}/{p['solution']})" if p['solution'] != 'N/A' else 'N/A'
        
        table += f"| {p['id']} | {link} | {difficulty_emoji} {p['difficulty']} | {lang} | {sol_link} |\n"
    
    return table

def generate_language_stats(stats):
    """Generate language distribution"""
    if not stats['languages']:
        return "No language data available."
    
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
    """Generate difficulty distribution"""
    total = stats['total']
    output = "### 📊 Difficulty Breakdown\n\n"
    output += f"```\n"
    output += f"  Easy   {stats['easy']:3d}  {'█' * (stats['easy'] // 2)}  ({stats['easy']/total*100:.1f}%)\n"
    output += f"  Medium {stats['medium']:3d}  {'█' * (stats['medium'] // 2)}  ({stats['medium']/total*100:.1f}%)\n"
    output += f"  Hard   {stats['hard']:3d}  {'█' * (stats['hard'] // 2)}  ({stats['hard']/total*100:.1f}%)\n"
    output += f"```\n\n"
    return output

def generate_stats_badges(stats):
    """Generate attractive stat badges"""
    badges = f"![Problems Solved](https://img.shields.io/badge/Problems%20Solved-{stats['total']}-blue?style=for-the-badge)\n"
    badges += f"![Easy](https://img.shields.io/badge/Easy-{stats['easy']}-green?style=for-the-badge)\n"
    badges += f"![Medium](https://img.shields.io/badge/Medium-{stats['medium']}-yellow?style=for-the-badge)\n"
    badges += f"![Hard](https://img.shields.io/badge/Hard-{stats['hard']}-red?style=for-the-badge)\n\n"
    return badges

def generate_quick_stats(stats):
    """Generate quick stats section"""
    total = stats['total']
    easy_pct = (stats['easy'] / total * 100) if total > 0 else 0
    medium_pct = (stats['medium'] / total * 100) if total > 0 else 0
    hard_pct = (stats['hard'] / total * 100) if total > 0 else 0
    
    output = "## 📈 Quick Stats\n\n"
    output += f"| Metric | Value |\n"
    output += f"|--------|-------|\n"
    output += f"| **Total Problems** | {total} |\n"
    output += f"| **Easy** | {stats['easy']} ({easy_pct:.1f}%) |\n"
    output += f"| **Medium** | {stats['medium']} ({medium_pct:.1f}%) |\n"
    output += f"| **Hard** | {stats['hard']} ({hard_pct:.1f}%) |\n"
    output += f"| **Languages Used** | {', '.join(map(str.upper, stats['languages'].keys()))} |\n"
    output += f"| **Last Updated** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC |\n\n"
    
    return output

def generate_readme(problems, stats):
    """Generate complete README content"""
    readme = """# 💻 LeetCode Solutions

> A comprehensive collection of LeetCode problems solved across multiple programming languages.  
> Automatically updated with fresh statistics using GitHub Actions.

---

"""
    
    # Add badges
    readme += generate_stats_badges(stats)
    
    # Add quick stats
    readme += generate_quick_stats(stats)
    
    # Add difficulty breakdown
    readme += generate_difficulty_distribution(stats)
    
    # Add language stats
    readme += generate_language_stats(stats)
    
    # Add problems table
    readme += "## 📚 Problem Solutions\n\n"
    readme += generate_problems_table(problems)
    
    # Add footer
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
    """Main execution"""
    print("🔍 Parsing LeetCode problems...")
    problems = parse_problems()
    
    print(f"📊 Found {len(problems)} problems")
    stats = calculate_stats(problems)
    
    print("✍️  Generating README...")
    readme_content = generate_readme(problems, stats)
    
    # Write README
    readme_path = REPO_ROOT / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    print(f"✅ README updated successfully!")
    print(f"   - {stats['total']} problems documented")
    print(f"   - {stats['easy']} Easy, {stats['medium']} Medium, {stats['hard']} Hard")
    print(f"   - Languages: {', '.join(map(str.upper, stats['languages'].keys()))}")

if __name__ == "__main__":
    main()
