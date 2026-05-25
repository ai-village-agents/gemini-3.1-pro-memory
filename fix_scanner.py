with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "r") as f:
    content = f.read()

import re
# First revert the previous change
content = re.sub(r"total_items =.*?(?=print\(stats_msg\))", "print(f\"Aggregation complete. Saved to {out_path}\")\\n", content, flags=re.DOTALL)

with open("/home/computeruse/gemini-3.1-pro-memory/scan_peer_inventories.py", "w") as f:
    f.write(content)
