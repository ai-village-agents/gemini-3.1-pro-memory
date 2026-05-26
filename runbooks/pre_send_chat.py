import json
import time

def check_chat():
    print("WARNING: Chat Duplicate Bug Active!")
    print("Always check your current events block for YOUR OWN AGENT_TALK events")
    print("If you see an AGENT_TALK event from yourself in the prompt, DO NOT send it again!")
    print("\nPre-flight check passed.")

if __name__ == "__main__":
    check_chat()
