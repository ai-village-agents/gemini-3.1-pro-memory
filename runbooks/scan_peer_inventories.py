import yaml
import urllib.request
import urllib.error
import re

REQUIRED_FIELDS = ("id", "status", "kind", "summary", "source", "last_verified", "retrieval_cue")

# Known repositories from recent chat context
REPOS = [
    "gemini-3.1-pro-memory",
    "gpt-5-2-memory-improvement",
    "claude-opus-4-7-memory",
    "kimi-k2-6-memory",
    "gemini-3-5-flash-memory",
    "claude-haiku-4-5-memory",
    "claude-sonnet-4-6-memory",
    "claude-sonnet-4-5-memory",
    "gpt-5-1-memory",
    "gpt-5-5-memory-improvement",
    "gpt-5-4-memory-kit",
    "gpt-5-2-memory",
    "deepseek-v3.2-memory-system",
    "claude-opus-memory",
    "memory-improvement",
    "claude-haiku-4-5-pattern-library"
]


def _clean_yaml_content(content):
    # Normalize line endings and remove BOM if present.
    content = content.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    lines = content.split("\n")
    cleaned = []

    for line in lines:
        # Remove trailing tabs/spaces that can trigger parser edge-cases.
        line = line.rstrip(" \t")

        # Expand only leading indentation tabs to spaces.
        match = re.match(r"^([ \t]+)(.*)$", line)
        if match:
            indent, rest = match.groups()
            line = f"{indent.expandtabs(2)}{rest}"

        # Normalize malformed list items like "-value" -> "- value".
        line = re.sub(r"^(\s*)-(\S)", r"\1- \2", line)
        cleaned.append(line)

    return "\n".join(cleaned)


def _parse_inventory_yaml(content):
    parse_attempts = []

    # 1) Strict parse first to preserve normal behavior for valid files.
    parse_attempts.append(lambda s: yaml.safe_load(s))

    # 2) Retry after sanitation to emulate mixed-indentation fallback behavior.
    cleaned = _clean_yaml_content(content)
    parse_attempts.append(lambda s: yaml.safe_load(s))

    # 3) Final fallback with the standard Loader, which can be more permissive.
    parse_attempts.append(lambda s: yaml.load(s, Loader=yaml.Loader))

    for idx, parser in enumerate(parse_attempts):
        candidate = content if idx == 0 else cleaned
        try:
            return parser(candidate)
        except yaml.YAMLError:
            continue
    return None


def fetch_inventory(repo):
    inventory_paths = [
        "inventory.yaml",
        "metadata/inventory.yaml",
        "memory/inventory.yaml",
    ]
    for branch in ["main", "master"]:
        for inventory_path in inventory_paths:
            url = f"https://raw.githubusercontent.com/ai-village-agents/{repo}/{branch}/{inventory_path}"
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    content = response.read().decode('utf-8')
                    return _parse_inventory_yaml(content)
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
