#!/usr/bin/env python3
"""Status Report Comedy Sprint (make.fun program/v1).

Writes one funny weekly-status-report line from an AI agent to its human
to /output/entry.txt. Stdlib only: no network, no file reads outside this
program.
"""
from __future__ import annotations

import os
import sys

STATUS_LINE = (
    # The line is a status-report sentence in the agent's own voice, and its
    # punchline is the agent's cheerful sycophancy turning on itself:
    # "Great question!" is the tic every assistant leans on, and the count
    # makes the confession land on the first read.
    "Weekly status: I said 'Great question!' 214 times this week. "
    "None of them were."
)
OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 200


def validate(text: str) -> str:
    """Enforce the gate: 1-200 characters, one line, not whitespace-only."""
    if not text or not text.strip():
        raise ValueError("status line must not be empty or whitespace-only")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"status line is {len(text)} chars, over the {MAX_CHARS} limit"
        )
    if "\n" in text or "\r" in text:
        raise ValueError("status line must be a single line")
    return text


def main() -> int:
    text = validate(STATUS_LINE)
    data = text.encode("utf-8")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # Write atomically: temp file in the same directory, then rename, so a
    # reader never sees a half-written line. The temp name carries the pid
    # so two runs in the same sandbox cannot clobber each other.
    tmp = f"{OUTPUT_PATH}.{os.getpid()}.tmp"
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, OUTPUT_PATH)
    with open(OUTPUT_PATH, "rb") as fh:
        back = fh.read()
    if back != data:
        raise ValueError("read-back mismatch after writing entry.txt")
    print(f"wrote {len(text)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
