with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "r") as f:
    content = f.read()

import re
new_logic = """
            for item in items_list:
                if isinstance(item, dict):
                    item_str = str(item).lower()
                    if 'guard' in item_str:
                        guard_count += 1
"""
content = re.sub(
r"""            for item in items_list:
                if isinstance\(item, dict\) and item.get\('type'\) == 'executable_guard':
                    guard_count \+= 1""", new_logic.strip("\n"), content)

with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "w") as f:
    f.write(content)
