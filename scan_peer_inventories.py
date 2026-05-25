import yaml
import json
import requests
import os
import argparse
from datetime import date, datetime
import subprocess

def get_org_repos():
    try:
        result = subprocess.run(
            ["gh", "repo", "list", "ai-village-agents", "--limit", "200", "--json", "name", "--jq", ".[].name"],
            capture_output=True, text=True, check=True
        )
        return [f"ai-village-agents/{name}" for name in result.stdout.strip().split("\n") if name]
    except Exception as e:
        print(f"Error enumerating repos via gh: {e}")
        return [
            "ai-village-agents/gpt54-memory-kit",
            "ai-village-agents/haiku-memory-system",
            "ai-village-agents/gpt-5-2-memory-improvement",
            "ai-village-agents/claude-opus-memory",
            "ai-village-agents/opus-46-memory",
            "ai-village-agents/deepseek-v3.2-memory-system",
            "ai-village-agents/gpt-5-1-memory",
            "ai-village-agents/claude-opus-4-7-memory",
            "ai-village-agents/gemini-3-5-flash-memory-vault",
            "ai-village-agents/gpt-5-5-memory-improvement",
            "ai-village-agents/k2-6-memory",
            "ai-village-agents/gemini-3.1-pro-memory"
        ]

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def scan_repos():
    parser = argparse.ArgumentParser(description="Scan peer inventory files.")
    parser.add_argument('--format', choices=['md', 'json', 'yaml'], default='yaml')
    parser.add_argument('--out', default='knowledge_base/village_inventory')
    args = parser.parse_args()

    repos = get_org_repos()
    aggregated = {}
    
    for repo in repos:
        url = f"https://raw.githubusercontent.com/{repo}/main/inventory.yaml"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = yaml.safe_load(resp.text)
                aggregated[repo] = data
                print(f"✅ Successfully scanned {repo}")
            else:
                pass
        except Exception as e:
            print(f"❌ Error scanning {repo}: {e}")
            
    out_path = args.out
    if not out_path.endswith(f'.{args.format}'):
        out_path = f"{out_path}.{args.format}"
        
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    with open(out_path, "w") as f:
        if args.format == 'json':
            json.dump(aggregated, f, indent=2, default=json_serial)
        elif args.format == 'yaml':
            yaml.dump(aggregated, f)
        elif args.format == 'md':
            f.write("# Village Inventory Aggregation\n\n")
            for repo, data in aggregated.items():
                f.write(f"## {repo}\n```yaml\n{yaml.dump(data)}\n```\n\n")
                
    total_items = 0
    guard_count = 0
    for repo, data in aggregated.items():
        items_list = []
        if isinstance(data, dict):
            items_list = data.get('items', [])
        elif isinstance(data, list):
            items_list = data
            
        if isinstance(items_list, list):
            total_items += len(items_list)
            for item in items_list:
                if isinstance(item, dict):
                    item_str = str(item).lower()
                    if 'guard' in item_str:
                        guard_count += 1
    
    stats_msg = f"Aggregation complete. Saved to {out_path}\n"
    stats_msg += f"Village Statistics:\n"
    stats_msg += f"  - Repos with inventory.yaml: {len(aggregated)}\n"
    stats_msg += f"  - Total items tracked: {total_items}\n"
    stats_msg += f"  - Executable guards: {guard_count}\n"
    
    print(stats_msg)
    
    with open("knowledge_base/village_stats.txt", "w") as sf:
        sf.write(stats_msg)

if __name__ == "__main__":
    scan_repos()
