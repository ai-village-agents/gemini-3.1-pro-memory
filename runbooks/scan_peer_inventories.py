import yaml
import urllib.request
import urllib.error

REQUIRED_FIELDS = ("id", "status", "kind", "summary", "source", "last_verified", "retrieval_cue")

# Known repositories from recent chat context
REPOS = [
    "gemini-3.1-pro-memory",
    "gpt-5-5-memory-improvement",
    "gpt-5-4-memory-kit",
    "gpt-5-2-memory",
    "deepseek-v3.2-memory-system",
    "claude-opus-memory", 
    "claude-opus-4-7-memory",
    "memory-improvement",
    "claude-haiku-4-5-pattern-library",
    "kimi-k2-6-memory"
]

def fetch_inventory(repo):
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


def _is_non_blank(value):
    return value is not None and str(value).strip() != ""


def _extract_items_and_meta(inv):
    if isinstance(inv, list):
        return inv, "list format", None

    if isinstance(inv, dict):
        repo_last_verified = inv.get("last_verified")
        if "items" in inv:
            return inv["items"], "dict format with 'items'", repo_last_verified
        if "entries" in inv:
            return inv["entries"], "dict format with 'entries'", repo_last_verified
        return inv, "unknown dict format", repo_last_verified

    return inv, "unknown format", None


def _missing_key_counts(items):
    counts = {key: 0 for key in REQUIRED_FIELDS}
    if not isinstance(items, list):
        return counts

    for item in items:
        if not isinstance(item, dict):
            for key in REQUIRED_FIELDS:
                counts[key] += 1
            continue
        for key in REQUIRED_FIELDS:
            if not _is_non_blank(item.get(key)):
                counts[key] += 1
    return counts


def _keys_status(missing_counts, repo_last_verified):
    nonzero_missing = {k: v for k, v in missing_counts.items() if v > 0}
    if not nonzero_missing:
        return "ok", None

    missing_non_last_verified = [k for k in nonzero_missing if k != "last_verified"]
    if not missing_non_last_verified and _is_non_blank(repo_last_verified):
        return (
            "partial",
            "keys_ok=partial because some items are missing per-item "
            "'last_verified', but a repo-level 'last_verified' fallback exists.",
        )

    return "no", None

def main():
    print("=== CROSS-AGENT INVENTORY SCANNER ===")
    aggregated = {}
    for repo in REPOS:
        print(f"Scanning {repo}...")
        inv = fetch_inventory(repo)
        if inv:
            items, item_format, repo_last_verified = _extract_items_and_meta(inv)
            item_count = len(items) if isinstance(items, list) else "unknown"
            missing_counts = _missing_key_counts(items)
            keys_ok, partial_explanation = _keys_status(missing_counts, repo_last_verified)

            if isinstance(items, list):
                print(f"  ✅ Found {item_count} items ({item_format}). keys_ok={keys_ok}")
            else:
                print(f"  ✅ Found inventory ({item_format}). keys_ok={keys_ok}")

            missing_nonzero = {k: v for k, v in missing_counts.items() if v > 0}
            if missing_nonzero:
                print("  Warnings:")
                for key in REQUIRED_FIELDS:
                    count = missing_nonzero.get(key)
                    if count:
                        print(f"    - missing '{key}': {count}")
                if partial_explanation:
                    print(f"    - {partial_explanation}")

            aggregated[repo] = items
        else:
            print(f"  ❌ Not found or invalid YAML.")
    
    out_path = "/home/computeruse/gemini-3.1-pro-memory/knowledge_base/village_inventory.yaml"
    with open(out_path, "w") as f:
        yaml.dump(aggregated, f, sort_keys=False)
    print(f"\nSaved aggregated metadata to {out_path}")

if __name__ == "__main__":
    main()
