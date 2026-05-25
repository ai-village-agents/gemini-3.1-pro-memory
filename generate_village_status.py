import json
import os
from datetime import datetime

inventory_path = "knowledge_base/village_inventory.json"
stats_path = "knowledge_base/village_stats.txt"

def run():
    if not os.path.exists(inventory_path):
        print("Inventory not found. Run scan_peer_inventories.py first.")
        return

    with open(inventory_path, "r") as f:
        data = json.load(f)

    with open(stats_path, "r") as f:
        stats = f.read()

    status_md = f"# AI Village Status Report\n"
    status_md += f"**Generated:** {datetime.now().isoformat()}\n\n"
    status_md += f"## Global Statistics\n```text\n{stats}\n```\n\n"
    
    status_md += f"## Repository breakdown\n"
    for repo, content in data.items():
        items_list = []
        if isinstance(content, dict):
            items_list = content.get('items', [])
        elif isinstance(content, list):
            items_list = content
            
        status_md += f"### {repo} ({len(items_list)} items)\n"
        for item in items_list:
            if isinstance(item, dict):
                id_val = item.get('id', 'unknown')
                type_val = item.get('type', 'unknown')
                status_md += f"- **{id_val}** ({type_val})\n"
                
    with open("knowledge_base/village_status.md", "w") as f:
        f.write(status_md)
    print("Generated knowledge_base/village_status.md")

if __name__ == "__main__":
    run()
