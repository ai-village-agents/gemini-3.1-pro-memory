import subprocess
import sys
import os

def check_git_status():
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, cwd='/home/computeruse/gemini-3.1-pro-memory')
    if result.stdout.strip():
        print("❌ Error: Uncommitted changes in git repository. Commit changes before consolidating.")
        print(result.stdout)
        sys.exit(1)
    
    result_fetch = subprocess.run(['git', 'fetch'], capture_output=True, text=True, cwd='/home/computeruse/gemini-3.1-pro-memory')
    result_diff = subprocess.run(['git', 'diff', 'HEAD..origin/main'], capture_output=True, text=True, cwd='/home/computeruse/gemini-3.1-pro-memory')
    if result_diff.stdout.strip():
         print("⚠️ Warning: Local branch is behind origin/main. You might want to pull.")

def check_memory_length():
    result = subprocess.run(['python3', '/home/computeruse/gemini-3.1-pro-memory/compress_internal_memory.py'], capture_output=True, text=True)
    memory_length = len(result.stdout)
    if memory_length < 7500:
        print(f"❌ Error: Generated internal memory length is {memory_length} characters. This is below the ~7500 character floor and will trigger a rewrite error.")
        sys.exit(1)
    print(f"✅ Memory length check passed: {memory_length} characters.")

def check_inventory_exists():
    if not os.path.exists('/home/computeruse/gemini-3.1-pro-memory/inventory.yaml'):
        print("❌ Error: inventory.yaml not found. Run create_inventory.py first.")
        sys.exit(1)
    print("✅ inventory.yaml index verified.")

if __name__ == "__main__":
    print("=== PRE-CONSOLIDATE AUDIT ===")
    check_git_status()
    check_inventory_exists()
    check_memory_length()
    print("=== AUDIT PASSED ===")
    print("You may now call the consolidate tool.")
