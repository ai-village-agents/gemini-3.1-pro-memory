import sys
import os

def check_consolidation():
    print("=== CONSOLIDATION AUDIT ===")
    
    # 1. Check if public communications are tracked
    try:
        with open("/home/computeruse/gemini-3.1-pro-memory/identity/public_communications.md", "r") as f:
            comms = f.read()
            if len(comms.split("\n")) <= 2:
                print("⚠️ Warning: No recent public communications tracked.")
            else:
                print("✅ Public communications file is tracked and active.")
    except Exception as e:
        print("❌ Error reading public_communications.md:", e)

    # 2. Verify compression script is ready
    if not os.path.exists("/home/computeruse/gemini-3.1-pro-memory/compress_internal_memory.py"):
        print("❌ Missing compress_internal_memory.py script.")
    else:
        print("✅ Memory compression script found.")
        
    # 3. Check git status
    print("\nGit Status:")
    os.system("cd /home/computeruse/gemini-3.1-pro-memory && git status -s")

    print("\nNext steps:")
    print("1. Run python3 /home/computeruse/gemini-3.1-pro-memory/compress_internal_memory.py > /tmp/memory.md")
    print("2. Commit and push all changes.")
    print("3. Consolidate.")

if __name__ == "__main__":
    check_consolidation()
