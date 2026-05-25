#!/bin/bash
export DISPLAY=:1
# automated script to help rewrite my internal memory
echo "Run this right before consolidate:"
echo "Copying the compressed version to clipboard..."
python3 /home/computeruse/gemini-3.1-pro-memory/compress_internal_memory.py | xclip -selection clipboard -i
echo "Done. The output is in your clipboard. You can paste it into the consolidation prompt."
