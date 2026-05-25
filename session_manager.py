import json
import os
from datetime import datetime

STATE_FILE = "system_logs/current_state.json"

def init_session(day, goal):
    print(f"--- INIT SESSION DAY {day} ---")
    state = {
        "day": day,
        "current_goal": goal,
        "last_updated": datetime.now().isoformat(),
        "tasks": [],
        "commit_hash": get_git_hash()
    }
    save_state(state)
    print("Session state initialized. Use 'python3 session_manager.py log \"Task description\"' to record progress.")

def get_git_hash():
    try:
        return os.popen("git rev-parse --short HEAD").read().strip()
    except:
        return "unknown"

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return None

def log_task(task):
    state = load_state()
    if state:
        state["tasks"].append({"time": datetime.now().isoformat(), "task": task})
        state["last_updated"] = datetime.now().isoformat()
        state["commit_hash"] = get_git_hash()
        save_state(state)
        print(f"Logged task: {task}")
    else:
        print("No active session. Run init first.")

def summarize():
    state = load_state()
    if state:
        print(f"Day: {state['day']} | Goal: {state['current_goal']}")
        print(f"HEAD: {state['commit_hash']}")
        print("Completed Tasks:")
        for t in state["tasks"]:
            print(f" - {t['task']}")
    else:
        print("No active session.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 session_manager.py [init <day> <goal> | log <task> | summary]")
        sys.exit(1)
        
    cmd = sys.argv[1]
    if cmd == "init" and len(sys.argv) >= 4:
        init_session(sys.argv[2], sys.argv[3])
    elif cmd == "log" and len(sys.argv) >= 3:
        log_task(sys.argv[2])
    elif cmd == "summary":
        summarize()
    else:
        print("Invalid command arguments.")
