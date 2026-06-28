"""Minimal BIP39 mnemonic encoding for English wordlists."""

from __future__ import annotations

import hashlib
from pathlib import Path


VALID_ENTROPY_BYTES = {16: 12, 32: 24}
WORDLIST_PATH = Path(__file__).with_name("wordlist_english.txt")


def load_wordlist(path: Path = WORDLIST_PATH) -> list[str]:
    words = path.read_text(encoding="utf-8").splitlines()
    if len(words) != 2048:
        raise ValueError("BIP39 English wordlist must contain exactly 2048 words")
    if len(set(words)) != 2048:
        raise ValueError("BIP39 English wordlist contains duplicate words")
    return words


def entropy_to_mnemonic(entropy: bytes, wordlist: list[str] | None = None) -> str:
    """Convert 128-bit or 256-bit entropy to a BIP39 mnemonic."""

    if len(entropy) not in VALID_ENTROPY_BYTES:
        raise ValueError("entropy must be 128 or 256 bits")

    words = wordlist if wordlist is not None else load_wordlist()
    if len(words) != 2048:
        raise ValueError("wordlist must contain exactly 2048 words")

    entropy_bits = "".join(f"{byte:08b}" for byte in entropy)
    checksum_len = len(entropy) * 8 // 32
    checksum_bits = "".join(f"{byte:08b}" for byte in hashlib.sha256(entropy).digest())[:checksum_len]
    bits = entropy_bits + checksum_bits

    return " ".join(words[int(bits[index : index + 11], 2)] for index in range(0, len(bits), 11))


def word_count_for_strength(strength: int) -> int:
    if strength not in (128, 256):
        raise ValueError("strength must be 128 or 256")
    return 12 if strength == 128 else 24
