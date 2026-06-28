"""Minimal BIP39 mnemonic encoding for English wordlists."""

from __future__ import annotations

import hashlib
from pathlib import Path


VALID_ENTROPY_BYTES = {16: 12, 32: 24}
VALID_WORD_COUNTS = {12: 16, 24: 32}
WORDLIST_PATH = Path(__file__).with_name("wordlist_english.txt")

BIP39_ENGLISH_TEST_VECTORS = (
    (
        "00000000000000000000000000000000",
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
    ),
    (
        "7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f",
        "legal winner thank year wave sausage worth useful legal winner thank yellow",
    ),
    (
        "ffffffffffffffffffffffffffffffff",
        "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo wrong",
    ),
    (
        "0000000000000000000000000000000000000000000000000000000000000000",
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon "
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art",
    ),
    (
        "7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f7f",
        "legal winner thank year wave sausage worth useful legal winner thank year wave sausage worth useful "
        "legal winner thank year wave sausage worth title",
    ),
    (
        "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
        "zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo zoo vote",
    ),
)


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


def validate_mnemonic_checksum(mnemonic: str, wordlist: list[str] | None = None) -> bool:
    """Return True when a BIP39 English mnemonic has valid words and checksum."""

    words = wordlist if wordlist is not None else load_wordlist()
    if len(words) != 2048:
        raise ValueError("wordlist must contain exactly 2048 words")

    mnemonic_words = mnemonic.strip().split()
    if len(mnemonic_words) not in VALID_WORD_COUNTS:
        return False

    indexes = {word: index for index, word in enumerate(words)}
    try:
        bits = "".join(f"{indexes[word]:011b}" for word in mnemonic_words)
    except KeyError:
        return False

    entropy_len = VALID_WORD_COUNTS[len(mnemonic_words)] * 8
    checksum_len = entropy_len // 32
    entropy_bits = bits[:entropy_len]
    checksum_bits = bits[entropy_len : entropy_len + checksum_len]
    entropy = int(entropy_bits, 2).to_bytes(entropy_len // 8, "big")
    expected = "".join(f"{byte:08b}" for byte in hashlib.sha256(entropy).digest())[:checksum_len]
    return checksum_bits == expected


def word_count_for_strength(strength: int) -> int:
    if strength not in (128, 256):
        raise ValueError("strength must be 128 or 256")
    return 12 if strength == 128 else 24
