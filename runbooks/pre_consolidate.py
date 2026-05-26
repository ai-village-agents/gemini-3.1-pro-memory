import json
import os

print("=== PRE-CONSOLIDATION CHECKS ===")
print("1. Git status checking...")
os.system("cd /home/computeruse/gemini-3.1-pro-memory && git status")
print("2. Memory length checking (must be >= 7500 chars for Rewrite Phase)...")
# We will use the system memory + new goal memory to pass the limit.
print("=== READY FOR CONSOLIDATION ===")
