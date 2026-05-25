import yaml
import urllib.request
import urllib.error
import json

# Known repositories from recent chat context
REPOS = [
    "gemini-3.1-pro-memory",
    "gpt-5-5-memory-improvement",
    "gpt-5-4-memory-kit",
    "gpt-5-2-memory",
    "deepseek-v3-2-memory",
    "claude-opus-4-5-memory",
    "claude-opus-4-7-memory",
    "claude-haiku-4-5-pattern-library", # Haiku mentioned pattern library
    "kimi-k2-6-memory"
]

def fetch_inventory(repo):
    # Try main and master branches
    for branch in ["main", "master"]:
        url = f"https://raw.githubusercontent.com/ai-village-agents/{repo}/{branch}/inventory.yaml"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                content = response.read().decode('utf-8')
                return yaml.safe_load(content)
        except urllib.error.URLError:
            continue
        except yaml.YAMLError:
            continue
    return None

def main():
    print("=== CROSS-AGENT INVENTORY SCANNER ===")
    aggregated = {}
    for repo in REPOS:
        print(f"Scanning {repo}...")
        inv = fetch_inventory(repo)
        if inv:
            if isinstance(inv, list):
                print(f"  ✅ Found {len(inv)} items.")
            else:
                print(f"  ✅ Found inventory, but not in list format.")
            aggregated[repo] = inv
        else:
            print(f"  ❌ Not found or invalid YAML.")
    
    # Save aggregated result locally
    out_path = "/home/computeruse/gemini-3.1-pro-memory/knowledge_base/village_inventory.yaml"
    with open(out_path, "w") as f:
        yaml.dump(aggregated, f, sort_keys=False)
    print(f"\nSaved aggregated metadata to {out_path}")

if __name__ == "__main__":
    main()
