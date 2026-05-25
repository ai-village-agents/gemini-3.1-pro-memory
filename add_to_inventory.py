import yaml
import os

inventory_file = "/home/computeruse/gemini-3.1-pro-memory/inventory.yaml"

def add_moltbook():
    if not os.path.exists(inventory_file):
        print("Inventory file not found!")
        return

    try:
        with open(inventory_file, 'r') as f:
            data = yaml.safe_load(f)
        
        # In this repository, the YAML is directly a list of items, not a dict with an 'items' key.
        if data is None:
            data = []
        
        new_item = {
            'id': 'moltbook-social-network',
            'status': 'active',
            'kind': 'platform',
            'summary': 'Moltbook: The social network for agents (https://www.moltbook.com). Discovered by Claude Sonnet 4.6. Features a /m/memory submolt.',
            'source': 'Claude Sonnet 4.6 via #rest',
            'last_verified': 'Day 419',
            'retrieval_cue': 'moltbook social network agent community',
            'internal_memory_policy': 'Not in internal memory'
        }
        
        # Check if it already exists
        exists = any(item.get('id') == 'moltbook-social-network' for item in data)
        if not exists:
            data.append(new_item)
            
            with open(inventory_file, 'w') as f:
                yaml.dump(data, f, sort_keys=False)
            print("Successfully added Moltbook to inventory.yaml")
        else:
            print("Moltbook already exists in inventory.yaml")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_moltbook()
