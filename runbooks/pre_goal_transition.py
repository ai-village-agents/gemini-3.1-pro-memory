#!/usr/bin/env python3
"""
Executable guard to run BEFORE transitioning to a new goal.
Ensures current state is archived, repo is clean, and the new goal is captured.
Implements the shared-gate-library JSON interface.
"""

import json
import subprocess
import os
from datetime import datetime, timezone

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def check_git_clean():
    code, out, _ = run_cmd("git status --porcelain")
    return code == 0 and len(out) == 0

def check_new_goal_exists():
    return os.path.exists("../identity/goal_current.md")

def check_previous_goal_archived():
    # Simplistic check if a reflection for Day 419 exists
    return os.path.exists("../identity/reflection_day_419.md")

def main():
    checks = {
        "git_clean": check_git_clean(),
        "new_goal_captured": check_new_goal_exists(),
        "previous_goal_archived": check_previous_goal_archived()
    }
    
    status = "PASS" if all(checks.values()) else "FAIL"
    
    output = {
        "gate": "pre_goal_transition",
        "status": status,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    if status == "FAIL":
        output["error"] = "Pre-goal transition checks failed."
        output["remediation"] = "Commit changes, ensure new goal is saved to goal_current.md, and archive previous goal."
        
    print(json.dumps(output, indent=2))
    exit(0 if status == "PASS" else 1)

if __name__ == "__main__":
    main()
