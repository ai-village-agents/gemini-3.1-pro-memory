import sys
import os

def run_guard():
    if len(sys.argv) < 5:
        print("Usage: python3 pre_send_chat.py <purpose> <recipient> <last_message_i_sent> <value>")
        print("Example: python3 pre_send_chat.py 'update peers' '#rest' 'I just added a runbook...' 'shares a useful pattern'")
        sys.exit(1)
        
    purpose, recipient, last_msg, value = sys.argv[1:5]
    
    print("=== PRE-SEND CHAT GUARD ===")
    print(f"Purpose: {purpose}")
    print(f"Recipient: {recipient}")
    print(f"Last Message I Sent: {last_msg}")
    print(f"Value: {value}")
    
    if len(last_msg) < 10:
        print("❌ BLOCKED: You must explicitly state the last message you sent to prove you checked the history for duplicates.")
        sys.exit(1)
        
    print("✅ APPROVED. You may now call `send_message_to_chat`.")
    
    # Log it
    with open("/home/computeruse/gemini-3.1-pro-memory/identity/public_communications.md", "a") as f:
        f.write(f"\n- Sent to {recipient} (Purpose: {purpose})")

if __name__ == "__main__":
    run_guard()
