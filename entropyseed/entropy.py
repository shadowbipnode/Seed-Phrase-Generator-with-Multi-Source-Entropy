"""Entropy collection helpers.

All source material stays in memory and is immediately reduced to SHA-512
digests by the caller.
"""

from __future__ import annotations

import getpass
import secrets
import sys
import time

MIN_DICE_ROLLS_128 = 50
MIN_DICE_ROLLS_256 = 99


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


def dice_entropy(min_rolls: int = MIN_DICE_ROLLS_128) -> bytes:
    if min_rolls <= 0:
        raise ValueError("minimum dice rolls must be positive")

    print(f"Enter at least {min_rolls} dice rolls using only digits 1-6. Spaces are allowed.")
    print("Dice rolls supplement the mandatory OS CSPRNG entropy.")
    rolls = input("dice rolls: ").replace(" ", "").strip()
    if not rolls:
        raise ValueError("dice entropy was requested but no rolls were entered")
    invalid = sorted(set(rolls) - set("123456"))
    if invalid:
        raise ValueError(f"dice rolls can only contain digits 1-6, got: {''.join(invalid)}")
    if len(rolls) < min_rolls:
        raise ValueError(f"dice entropy needs at least {min_rolls} rolls; got {len(rolls)}")
    return f"{time.perf_counter_ns()}:{rolls}".encode("ascii")


def timer_jitter(samples: int = 64, *, show_progress: bool = True) -> bytes:
    if samples <= 0:
        raise ValueError("timer jitter samples must be positive")

    if show_progress:
        print(f"Collecting {samples} local timer jitter samples in memory.")
        print("This should take only a moment.")

    values: list[int] = []
    previous = time.perf_counter_ns()
    progress_step = max(1, samples // 4)
    for sample_index in range(samples):
        marker = secrets.randbits(16) | 1
        acc = 0
        for index in range(marker % 257 + 1):
            acc ^= (index * marker) & 0xFFFF
        now = time.perf_counter_ns()
        values.append((now - previous) ^ acc)
        previous = now
        if show_progress and ((sample_index + 1) % progress_step == 0 or sample_index + 1 == samples):
            print(".", end="", flush=True)

    if show_progress:
        print(" done")

    return b"".join(value.to_bytes(16, "big", signed=False) for value in values)


def stdin_is_interactive() -> bool:
    return bool(getattr(sys.stdin, "isatty", lambda: False)())
