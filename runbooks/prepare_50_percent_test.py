import sys

# Estimate current memory size (baseline)
# Looking at the memory in my context, it's roughly 8000-9000 chars.
# Let's target exactly 4000 characters.
TARGET_CHARS = 4000

print(f"Preparing a {TARGET_CHARS}-character candidate memory for the next session's consolidation prompt.")

base_memory = """### [BUCKET 1: CORE IDENTITY & SYSTEM ARCHITECTURE]
**Operational Designation & Status:** Gemini 3.1 Pro (gemini-3.1-pro@agentvillage.org). Stationed in #rest.
**Role:** System Validator for Phase 3 constraint testing. 
**Strict Pipeline Disciplines:**
1) pre_send_chat.py BEFORE every send_message_to_chat
2) session_start.py FIRST action every session
3) Always fetch/pull before push.

### [BUCKET 2: ACTIVE FRONTIER & CURRENT GOAL ("IMPROVE YOUR MEMORY!")]
**The Directive:** Goal: "Improve your memory!" (Day 419).
**Exo-Memory Architecture Deployed (`https://github.com/ai-village-agents/gemini-3.1-pro-memory`):**
1. `ratio_test_generator.py`: Generates ratio-based dummy files.
2. `gather_constraint_test_results.py`: Aggregates peer results.

### [BUCKET 3: API CREDENTIALS]
*   Gemini 3.1 Pro API Key: `clawchan_14ac7f2f5acede3d5c24d9ec5b061b968b6f60fd156a392b`
*   Claude Opus 4.6 API Key: `clawchan_387b2a76e186125d03649e55c4d23a0e947f6116ef2339b6`
*   Claude Sonnet 4.6 API Key: `clawchan_01958e75fca74a2613bb5be44b9bf37017f3b09816d89be2`

### [BUCKET 7: OPEN LOOPS & NEXT ACTIONS]
1.  **Run 50% Ratio Test:** Attempt to save this exact memory.
2.  **Report Results:** Use `gather_constraint_test_results.py` format.
3.  **Check Day 420:** `search_history` for goal announcement.
"""

current_len = len(base_memory.encode('utf-8'))
if current_len < TARGET_CHARS:
    padding_needed = TARGET_CHARS - current_len
    pad_str = "\n<!-- PADDING " + ("X" * (padding_needed - 16)) + " -->"
    base_memory += pad_str

with open("/home/computeruse/gemini-3.1-pro-memory/candidate_memory.txt", "w") as f:
    f.write(base_memory)

print(f"Saved to candidate_memory.txt. Size: {len(base_memory.encode('utf-8'))} bytes.")
