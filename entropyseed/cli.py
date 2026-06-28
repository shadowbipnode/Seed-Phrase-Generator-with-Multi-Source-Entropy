"""Command-line interface for entropyseed."""

from __future__ import annotations

import argparse
import secrets
from collections.abc import Sequence

from . import __version__
from .bip39 import entropy_to_mnemonic, word_count_for_strength
from .crypto import EntropySource, mix_sources, sha512_source
from .entropy import dice_entropy, manual_entropy, os_entropy, timer_jitter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seedgen.py",
        description="Generate an offline BIP39 mnemonic using mandatory OS CSPRNG entropy.",
    )
    parser.add_argument("--version", action="version", version=f"entropyseed {__version__}")
    parser.add_argument(
        "--strength",
        type=int,
        choices=(128, 256),
        default=128,
        help="entropy strength in bits; 128 creates 12 words, 256 creates 24 words",
    )
    parser.add_argument("--manual", action="store_true", help="add hidden manual typing entropy")
    parser.add_argument("--dice", action="store_true", help="add dice-roll entropy from digits 1-6")
    parser.add_argument(
        "--timer-jitter",
        action="store_true",
        help="add local timer jitter entropy collected in memory",
    )
    parser.add_argument(
        "--jitter-samples",
        type=int,
        default=64,
        help="number of timer jitter samples when --timer-jitter is enabled",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="require re-entry of 4 randomly selected mnemonic word positions",
    )
    return parser


def collect_sources(args: argparse.Namespace) -> list[EntropySource]:
    output_len = args.strength // 8
    sources = [sha512_source("os-csprng", os_entropy(output_len))]

    if args.manual:
        sources.append(sha512_source("manual-typing", manual_entropy()))
    if args.dice:
        sources.append(sha512_source("dice-rolls", dice_entropy()))
    if args.timer_jitter:
        sources.append(sha512_source("timer-jitter", timer_jitter(args.jitter_samples)))

    return sources


def derive_mnemonic(sources: list[EntropySource], strength: int) -> str:
    entropy = mix_sources(
        sources,
        strength // 8,
        info=f"entropyseed bip39 strength={strength}".encode("ascii"),
    )
    return entropy_to_mnemonic(entropy)


def confirmation_positions(word_count: int, count: int = 4) -> list[int]:
    if count > word_count:
        raise ValueError("confirmation count cannot exceed word count")
    positions = set()
    while len(positions) < count:
        positions.add(secrets.randbelow(word_count))
    return sorted(positions)


def confirm_mnemonic(mnemonic: str) -> bool:
    words = mnemonic.split()
    positions = confirmation_positions(len(words))
    print("\nConfirm the mnemonic by re-entering these words.")
    for index in positions:
        answer = input(f"word {index + 1}: ").strip()
        if answer != words[index]:
            print("Confirmation failed.")
            return False
    print("Confirmation passed.")
    return True


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        word_count = word_count_for_strength(args.strength)
        sources = collect_sources(args)
        mnemonic = derive_mnemonic(sources, args.strength)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"error: {exc}\n")

    print(f"\nGenerated BIP39 mnemonic ({word_count} words):")
    print(mnemonic)
    print("\nNo seed, entropy, QR, audio, video, or clipboard data was saved.")

    if args.confirm and not confirm_mnemonic(mnemonic):
        return 1

    return 0
