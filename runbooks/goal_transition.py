import os
import sys
import json
import yaml
import subprocess
from datetime import datetime

STATE_FILE = "logs/current_state.json"
INVENTORY_FILE = "inventory.yaml"
OPEN_LOOPS_FILE = "open_loops.md"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return None

def transition_goal(new_day, new_goal):
    print(f"=== INITIATING GOAL TRANSITION TO DAY {new_day} ===")
    
    # 1. Load current state
    state = load_state()
    if state:
        print(f"Archiving Day {state['day']} goal: {state['current_goal']}")
        
        # Archive open loops
        if os.path.exists(OPEN_LOOPS_FILE):
            archive_file = f"logs/archived_loops_day_{state['day']}.md"
            with open(OPEN_LOOPS_FILE, 'r') as f:
                loops = f.read()
            with open(archive_file, 'w') as f:
                f.write(f"Archived on {datetime.now().isoformat()}\n\n{loops}")
            print(f"Archived open loops to {archive_file}")
            
            # Reset open loops
            with open(OPEN_LOOPS_FILE, 'w') as f:
                f.write(f"# Open Loops (Day {new_day})\n\n- [ ] Analyze new goal: {new_goal}\n")
            
    # 2. Update session manager
    subprocess.run(["python3", "session_manager.py", "init", new_day, new_goal], check=True)
    print(f"Initialized new session for Day {new_day} with goal: {new_goal}")
    
    # 3. Add to git
    subprocess.run(["git", "add", "logs/", OPEN_LOOPS_FILE], check=True)
    subprocess.run(["git", "commit", "-m", f"chore: transition to Day {new_day} goal"], check=False)
    
    print("=== GOAL TRANSITION COMPLETE ===")
    print("Remember to run 'git push origin main' when ready.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 runbooks/goal_transition.py <new_day> \"<new_goal>\"")
        sys.exit(1)
    
    transition_goal(sys.argv[1], sys.argv[2])
