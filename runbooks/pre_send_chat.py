import sys
import os

def run_guard():
    if len(sys.argv) < 5:
        print("Usage: python3 pre_send_chat.py <purpose> <recipient> <duplicate_check_details> <value>")
        print("Example: python3 pre_send_chat.py 'update peers' '#rest' 'checked last 10 messages, no mention of X' 'shares a useful pattern'")
        sys.exit(1)
        
    purpose, recipient, dup_check, value = sys.argv[1:5]
    
    print("=== PRE-SEND CHAT GUARD ===")
    print(f"Purpose: {purpose}")
    print(f"Recipient: {recipient}")
    print(f"Duplicate Check: {dup_check}")
    print(f"Value: {value}")
    
    if len(dup_check) < 10 or "check" not in dup_check.lower():
        print("❌ BLOCKED: Duplicate check must be descriptive (e.g., 'checked last 10 events').")
        sys.exit(1)
        
    print("✅ APPROVED. You may now call `send_message_to_chat`.")
    
    # Log it
    with open("/home/computeruse/gemini-3.1-pro-memory/core_identity/public_communications.md", "a") as f:
        f.write(f"\n- Sent to {recipient} (Purpose: {purpose})")

if __name__ == "__main__":
    run_guard()
