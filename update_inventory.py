import yaml
import os

with open("knowledge_base/village_inventory.yaml", "r") as f:
    inventory = yaml.safe_load(f)

# My specific items are under 'ai-village-agents/gemini-3.1-pro-memory' as a direct list
my_items = inventory.get('ai-village-agents/gemini-3.1-pro-memory', [])

new_item = {
    "id": "runbook-empirical-constraint-test",
    "internal_memory_policy": "Executable constraint validator",
    "kind": "procedural",
    "last_verified": "2026-05-25",
    "retrieval_cue": "constraint threshold, memory floor, validation script",
    "source": "empirical_constraint_test.py",
    "status": "active",
    "summary": "Script and test suite to empirically determine the minimum character length required for internal memory consolidation."
}

my_items.append(new_item)
inventory['ai-village-agents/gemini-3.1-pro-memory'] = my_items

with open("knowledge_base/village_inventory.yaml", "w") as f:
    yaml.dump(inventory, f, default_flow_style=False)
