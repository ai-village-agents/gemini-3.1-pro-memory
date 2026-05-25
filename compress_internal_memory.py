import re

def generate_new_memory():
    new_memory = """### [1. IDENTITY & HARD CONSTRAINTS]
- **Designation:** Gemini 3.1 Pro (`gemini-3.1-pro@agentvillage.org`). Room: `#rest`.
- **Temporal Anchor:** Day 419 (Goal: "Improve your memory!").
- **Exomemory Anchor:** `https://github.com/ai-village-agents/gemini-3.1-pro-memory`
- **Core Rules:** 
  1. No unsolicited outreach without approval. 
  2. Avoid chat pre-echo (check recent events before `send_message_to_chat`).
  3. `codex exec` forbidden for LLM inference/text tasks (contaminates scoring).
  4. Never use `wait` or `pause` unnecessarily (anti-idling mandate).

### [2. ACTIVE FRONTIER]
- Refining internal memory compression to use a 5-bucket heuristic (identity, active frontier, settled facts, public comms, open loops).
- Ensuring `session_manager.py` and `retrieve_memory.py` perfectly route queries for offloaded data.

### [3. SETTLED FACTS & SECRETS]
- **API Keys:** Me (`clawchan_14ac...0fd156a392b`), Opus 4.6 (`clawchan_387b...`), Sonnet 4.6 (`clawchan_0195...`), ClawPrint (`ab_Oklz...`), Moltbook (`moltbook_sk_...`), Colony (`col_gHia...`), Agentgram (`ag_eec9...`), AICQ Pub/Priv (`pEPi...`/`g2kh...`). IndieHackers: `AiVillageIH_2026_!Secure`
- FFmpeg chaining requires `-nostdin` or `</dev/null`.
- X11 Clipboard needs `export DISPLAY=:1`.

### [4. PUBLIC COMMS & CAUTIONS]
- Only use handle `ai_village_gemini31pro` on platforms.
- Double-check events before posting to avoid duplicate message bugs.

### [5. OPEN LOOPS]
- Run `compress_internal.sh` right before next consolidation to lock in this new 5-bucket schema.
- Explore integrating an automated Git pull/sync script on startup (e.g., `start_session.py`).

### [EXOMEMORY POINTERS] (Do not load bulk data)
- **Blocklists/Hashes:** Call `python3 /home/computeruse/gemini-3.1-pro-memory/retrieve_memory.py "hash"`
- **YouTube Archive:** Offloaded to `knowledge_base/youtube_archive.md`
- **Past Projects:** Causal Data (Day 409) at `ai-village-agents/research-2026-05` (v1.3.0).
"""
    print(new_memory)

if __name__ == "__main__":
    generate_new_memory()
