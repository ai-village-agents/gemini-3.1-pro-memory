import yaml
import json
import requests
import os
import argparse
from datetime import date, datetime
import subprocess

def get_org_repos():
    try:
        # Use gh CLI to enumerate repos to bypass rate limits and get current list
        result = subprocess.run(
            ["gh", "repo", "list", "ai-village-agents", "--limit", "200", "--json", "name", "--jq", ".[].name"],
            capture_output=True, text=True, check=True
        )
        return [f"ai-village-agents/{name}" for name in result.stdout.strip().split("\n") if name]
    except Exception as e:
        print(f"Error enumerating repos via gh: {e}")
        # Fallback to known repos if enumeration fails
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
    """JSON serializer for objects not serializable by default json code"""
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
                pass # Silent ignore for repos without an inventory.yaml
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
    print(f"Aggregation complete. Saved to {out_path}")

if __name__ == "__main__":
    scan_repos()
