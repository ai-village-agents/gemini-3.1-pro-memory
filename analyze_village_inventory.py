import yaml
import json

with open("/home/computeruse/gemini-3.1-pro-memory/knowledge_base/village_inventory.yaml", "r") as f:
    data = yaml.safe_load(f)

print(f"Total Agents indexed: {len(data)}")

agent_item_counts = {}
for agent, inventory in data.items():
    if isinstance(inventory, list):
         agent_item_counts[agent] = len(inventory)
    elif isinstance(inventory, dict) and "items" in inventory:
         agent_item_counts[agent] = len(inventory["items"])
    elif isinstance(inventory, dict) and "entries" in inventory:
         agent_item_counts[agent] = len(inventory["entries"])
    else:
         agent_item_counts[agent] = 0

print("\nItem Counts per Agent:")
for agent, count in agent_item_counts.items():
    print(f"  {agent}: {count} items")

print("\nExtracting all runbook IDs:")
runbooks = []
for agent, inventory in data.items():
    if isinstance(inventory, list):
        items = inventory
    else:
        items = inventory.get("items", []) or inventory.get("entries", [])
        
    for item in items:
        # Check type carefully in case item is missing 'kind'
        if isinstance(item, dict) and (item.get("kind") == "procedural" or item.get("kind") == "gate"):
            runbooks.append(f"{agent} -> {item.get('id')}")

for r in runbooks:
    print(f"  {r}")
