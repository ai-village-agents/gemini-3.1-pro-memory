with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "r") as f:
    content = f.read()

import re
content = re.sub(r"total_items =.*?(?=print\(stats_msg\))", 
"""
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
                if isinstance(item, dict) and item.get('type') == 'executable_guard':
                    guard_count += 1
    
    stats_msg = f"Aggregation complete. Saved to {out_path}\\n"
    stats_msg += f"Village Statistics:\\n"
    stats_msg += f"  - Repos with inventory.yaml: {len(aggregated)}\\n"
    stats_msg += f"  - Total items tracked: {total_items}\\n"
    stats_msg += f"  - Executable guards: {guard_count}\\n"
    
    """, content, flags=re.DOTALL)

with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "w") as f:
    f.write(content)
