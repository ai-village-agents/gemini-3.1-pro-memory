#!/usr/bin/env python3
import subprocess
import sys
import os
import json
from datetime import datetime, timezone

def run_guard():
    checks = {}
    timestamp = datetime.now(timezone.utc).isoformat()
    errors = []

    # 1. Git Status Check
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, cwd='/home/computeruse/gemini-3.1-pro-memory')
        if result.stdout.strip():
            checks['git_clean'] = False
            errors.append(f"Uncommitted changes in git repository: {result.stdout.strip()}")
        else:
            checks['git_clean'] = True
    except Exception as e:
        checks['git_clean'] = False
        errors.append(f"Git check failed: {str(e)}")

    # 2. Inventory Exists
    inventory_path = '/home/computeruse/gemini-3.1-pro-memory/inventory.yaml'
    checks['inventory_exists'] = os.path.exists(inventory_path)
    if not checks['inventory_exists']:
        errors.append("inventory.yaml not found.")

    # 3. Memory Length Verification
    try:
        result = subprocess.run(['python3', '/home/computeruse/gemini-3.1-pro-memory/compress_internal_memory.py'], capture_output=True, text=True)
        memory_length = len(result.stdout)
        checks['memory_length_sufficient'] = memory_length >= 7500
        if not checks['memory_length_sufficient']:
            errors.append(f"Generated internal memory length is {memory_length} chars, below 7500 char floor.")
    except Exception as e:
        checks['memory_length_sufficient'] = False
        errors.append(f"Memory length check failed: {str(e)}")

    # Final Evaluation
    status = "PASS" if all(checks.values()) else "FAIL"

    result_payload = {
        "gate": "pre_consolidate",
        "status": status,
        "checks": checks,
        "timestamp": timestamp
    }
    
    if errors:
        result_payload["error"] = "; ".join(errors)
        result_payload["remediation"] = "Commit changes, ensure inventory.yaml exists, and maintain structured padding >7500 chars."

    print(json.dumps(result_payload, indent=2))
    
    if status == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    run_guard()
