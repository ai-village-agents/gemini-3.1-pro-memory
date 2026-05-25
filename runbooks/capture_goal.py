import sys
import os
import json

def capture_goal():
    print("Please paste the exact verbatim text of Shoshannah's new goal announcement below.")
    print("Press Ctrl-D (EOF) when finished:")
    goal_text = sys.stdin.read().strip()
    
    if not goal_text:
        print("No text provided. Exiting.")
        sys.exit(1)
        
    print("\n--- GOAL TEXT CAPTURED ---")
    
    with open("logs/new_goal_raw.txt", "w") as f:
        f.write(goal_text)
        
    print("Saved raw text to logs/new_goal_raw.txt.")
    print("You can now read this file to parse it structurally before running goal_transition.py")
    
if __name__ == "__main__":
    capture_goal()
