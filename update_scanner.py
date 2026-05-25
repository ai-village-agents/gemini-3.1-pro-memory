with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "r") as f:
    content = f.read()

new_content = content.replace(
    "    print(f\"Aggregation complete. Saved to {out_path}\")",
    """
    total_items = sum(len(items) if isinstance(items, list) else 0 for repo_data in aggregated.values() for items in [repo_data.get('items', [])])
    guard_count = sum(1 for repo_data in aggregated.values() if isinstance(repo_data.get('items', []), list) for item in repo_data.get('items', []) if isinstance(item, dict) and item.get('type') == 'executable_guard')
    
    stats_msg = f"Aggregation complete. Saved to {out_path}\\n"
    stats_msg += f"Village Statistics:\\n"
    stats_msg += f"  - Repos with inventory.yaml: {len(aggregated)}\\n"
    stats_msg += f"  - Total items tracked: {total_items}\\n"
    stats_msg += f"  - Executable guards: {guard_count}\\n"
    
    print(stats_msg)
    
    with open("knowledge_base/village_stats.txt", "w") as sf:
        sf.write(stats_msg)
"""
)

with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "w") as f:
    f.write(new_content)
