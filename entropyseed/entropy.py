"""Entropy collection helpers.

All source material stays in memory and is immediately reduced to SHA-512
digests by the caller.
"""

from __future__ import annotations

import getpass
import secrets
import sys
import time


def os_entropy(num_bytes: int) -> bytes:
    if num_bytes <= 0:
        raise ValueError("num_bytes must be positive")
    return secrets.token_bytes(num_bytes)


def manual_entropy() -> bytes:
    print("Type random text, then press Enter. Input is hidden when the terminal supports it.")
    read_secret = getpass.getpass if stdin_is_interactive() else input
    first = read_secret("manual entropy: ")
    print("Add a second line of random text, then press Enter.")
    second = read_secret("manual entropy again: ")
    return f"{time.perf_counter_ns()}:{first}:{second}".encode("utf-8")


def dice_entropy() -> bytes:
    print("Enter dice rolls using only digits 1-6. Spaces are allowed.")
    rolls = input("dice rolls: ").replace(" ", "").strip()
    if not rolls:
        raise ValueError("dice entropy was requested but no rolls were entered")
    invalid = sorted(set(rolls) - set("123456"))
    if invalid:
        raise ValueError(f"dice rolls can only contain digits 1-6, got: {''.join(invalid)}")
    return f"{time.perf_counter_ns()}:{rolls}".encode("ascii")


def timer_jitter(samples: int = 64) -> bytes:
    if samples <= 0:
        raise ValueError("timer jitter samples must be positive")

    values: list[int] = []
    previous = time.perf_counter_ns()
    for _ in range(samples):
        marker = secrets.randbits(16) | 1
        acc = 0
        for index in range(marker % 257 + 1):
            acc ^= (index * marker) & 0xFFFF
        now = time.perf_counter_ns()
        values.append((now - previous) ^ acc)
        previous = now

    return b"".join(value.to_bytes(16, "big", signed=False) for value in values)


def stdin_is_interactive() -> bool:
    return bool(getattr(sys.stdin, "isatty", lambda: False)())
