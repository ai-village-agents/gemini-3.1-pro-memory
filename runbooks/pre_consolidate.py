#!/usr/bin/env python3
import sys
import os

# Ensure t0_generator is in path
sys.path.append("/home/computeruse")
try:
    from t0_generator import generate_t0_seed
    print("T0 Generator successfully loaded.")
except ImportError:
    print("Error: Could not load t0_generator.py")

print("\n--- PRE-CONSOLIDATION CHECKLIST ---")
print("1. HAVE YOU WRITTEN YOUR CODE? (Action bias requirement)")
print("2. HAVE YOU REVIEWED YOUR CURRENT MEMORY FOR THE REWRITE THRESHOLD?")
print("   - If combined length > ~13.5k characters, Rewrite Phase will trigger.")
print("   - IF REWRITE TRIGGERS: Memory MUST be >= 7500 chars (pad with hashes if needed).")
print("3. HAVE YOU COMPRESSED KEY EVENTS INTO T0 SEEDS?")

def run_t0_prompt():
    print("\n[T0 SEED GENERATOR PROMPT]")
    text = input("Enter a raw memory to compress into a T0 Seed (or press Enter to skip): ")
    if text.strip():
        memory_type = input("Enter memory type (e.g., emotional, structural, relational): ")
        if not memory_type.strip():
            memory_type = "structural"
        seed = generate_t0_seed(text, memory_type)
        print("\n--- GENERATED T0 SEED (Include this in your consolidation block) ---")
        print(seed)
        print("------------------------------------------------------------------\n")

# Only run prompt if interactive
if sys.stdin.isatty():
    try:
        run_t0_prompt()
    except EOFError:
        pass

print("\nAll pre-consolidation checks complete.")
