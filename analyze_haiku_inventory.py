import json
import collections

with open("knowledge_base/haiku_aggregated_inventories_latest.json", "r") as f:
    data = json.load(f)

# Structure seems to be data["results"][agent_name] = [item1, item2, ...]
results = data.get("results", {})
if not results:
    # If the JSON structure is different
    results = data

kind_counts = collections.Counter()
gate_tools = []
procedural_tools = []

for agent, val in results.items():
    if isinstance(val, list):
        items = val
    else:
        continue
        
    for item in items:
        if not isinstance(item, dict):
            continue
            
        kind = item.get("kind", "unknown")
        kind_counts[kind] += 1
        
        id_val = item.get("id", "")
        if kind == "gate":
            gate_tools.append(id_val)
        elif kind == "procedural":
            procedural_tools.append(id_val)

print(f"=== Phase 3.3 Inventory Analysis ===")
print("\nCounts by Kind:")
for k, v in kind_counts.most_common():
    print(f"  {k}: {v}")

print("\nGate Tools (Executable Guards):")
for t in sorted(gate_tools):
    print(f"  {t}")
