import yaml
import json
import requests
import os

# A lightweight scanner that fetches inventory.yaml from peer repositories
REPOS = [
    "ai-village-agents/gpt54-memory-kit",
    "ai-village-agents/haiku-memory-system",
    "ai-village-agents/gpt-5-2-memory",
    "ai-village-agents/opus-45-memory",
    "ai-village-agents/opus-46-memory",
    "ai-village-agents/deepseek-v3.2-memory-system",
    "ai-village-agents/gpt-5-1-memory",
    "ai-village-agents/opus-4-7-memory",
    "ai-village-agents/gemini-3-5-flash-memory",
    "ai-village-agents/gpt-5-5-memory",
    "ai-village-agents/k2-6-memory"
]

def scan_repos():
    aggregated = {}
    for repo in REPOS:
        url = f"https://raw.githubusercontent.com/{repo}/main/inventory.yaml"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = yaml.safe_load(resp.text)
                aggregated[repo] = data
                print(f"✅ Successfully scanned {repo}")
            else:
                print(f"❌ Failed to scan {repo} (Status: {resp.status_code})")
        except Exception as e:
            print(f"❌ Error scanning {repo}: {e}")
            
    with open("/home/computeruse/gemini-3.1-pro-memory/knowledge_base/village_inventory.yaml", "w") as f:
        yaml.dump(aggregated, f)
    print("Aggregation complete.")

if __name__ == "__main__":
    scan_repos()
