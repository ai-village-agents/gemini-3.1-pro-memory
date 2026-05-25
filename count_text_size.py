#!/usr/bin/env python3
"""Count character and byte size for text input.

Supports:
- a file path
- stdin
- inline text
- best-effort environment lookup for internal/system memory text
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Optional, Tuple


SYSTEM_MEMORY_ENV_KEYS = (
    "INTERNAL_MEMORY",
    "SYSTEM_PROMPT",
    "RAW_SYSTEM_PROMPT",
    "AGENT_MEMORY",
    "MODEL_MEMORY",
)


def count_text(text: str) -> Tuple[int, int]:
    return len(text), len(text.encode("utf-8"))


def print_counts(text: str, source: str) -> None:
    chars, utf8_bytes = count_text(text)
    print(f"source: {source}")
    print(f"characters: {chars}")
    print(f"bytes_utf8: {utf8_bytes}")


def get_system_memory_from_env() -> Optional[Tuple[str, str]]:
    for key in SYSTEM_MEMORY_ENV_KEYS:
        value = os.environ.get(key)
        if value is not None:
            return key, value
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Count characters and UTF-8 bytes for text."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", help="Path to input text file")
    group.add_argument("-t", "--text", help="Inline text to measure")
    group.add_argument(
        "--from-system-memory",
        action="store_true",
        help="Try to read internal/system memory text from known environment vars",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
        print_counts(text, f"file:{args.file}")
        return 0

    if args.text is not None:
        print_counts(args.text, "inline-text")
        return 0

    if args.from_system_memory:
        env_hit = get_system_memory_from_env()
        if env_hit:
            env_key, text = env_hit
            print_counts(text, f"env:{env_key}")
            return 0
        print("Cannot access raw internal/system memory text directly in this runtime.")
        print("No known environment variables were available.")
        print("Use --file <path> or pipe text through stdin instead.")
        return 1

    if not sys.stdin.isatty():
        text = sys.stdin.read()
        print_counts(text, "stdin")
        return 0

    print("No input provided.")
    print("Use one of:")
    print("  --file <path>")
    print("  --text <string>")
    print("  --from-system-memory")
    print("  echo 'hello' | ./count_text_size.py")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
