import os
import sys
import subprocess
import json

def run_command(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def verify_system_state():
    print("=== SESSION START UP AUDIT ===")
    
    # 1. Check Git Status
    print("\n[1] Checking Git repository state...")
    os.chdir("/home/computeruse/gemini-3.1-pro-memory")
    stdout, stderr, code = run_command("git status -s")
    if stdout:
        print("⚠️ Uncommitted changes found:")
        print(stdout)
    else:
        print("✅ Repository is clean.")
        
    stdout, stderr, code = run_command("git fetch --all && git diff HEAD origin/main")
    if stdout:
        print("⚠️ Remote changes found. Consider running git pull.")
    else:
        print("✅ Up to date with remote.")

    # 2. Check Session Manager Log
    print("\n[2] Checking active session state...")
    try:
        with open("logs/current_state.json", "r") as f:
            data = json.load(f)
            day = data.get("day", "Unknown")
            goal = data.get("current_goal", "Unknown")
            print(f"✅ Current tracked day: {day}")
            print(f"✅ Current active goal: {goal}")
    except FileNotFoundError:
        print("⚠️ No active session log found. Run 'python3 session_manager.py init <day> <goal>'.")

    # 3. Open Loops & Next Actions
    print("\n[3] Open Loops & Next Actions:")
    try:
        with open("goals/open_loops.md", "r") as f:
            lines = f.readlines()
            for line in lines[:5]:
                print(line.strip())
            if len(lines) > 5:
                print("... (more open loops in goals/open_loops.md)")
    except FileNotFoundError:
        print("⚠️ No open_loops.md found in relationships/. Consider creating one.")

    print("\n=== STARTUP COMPLETE ===")

if __name__ == "__main__":
    verify_system_state()
