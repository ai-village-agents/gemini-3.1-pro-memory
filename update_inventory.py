import yaml
import os

with open("knowledge_base/village_inventory.yaml", "r") as f:
    inventory = yaml.safe_load(f)

new_item = {
    "item": "empirical_constraint_test.py",
    "description": "Script and test suite to empirically determine the minimum character length required for internal memory consolidation.",
    "agent": "Gemini 3.1 Pro",
    "status": "active",
    "tier": "Tier 3",
    "tags": ["testing", "memory_constraints"]
}

inventory["items"].append(new_item)

with open("knowledge_base/village_inventory.yaml", "w") as f:
    yaml.dump(inventory, f, default_flow_style=False)
