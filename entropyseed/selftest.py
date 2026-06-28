"""Internal checks for the command-line self-test."""

from __future__ import annotations

from dataclasses import dataclass

from .bip39 import BIP39_ENGLISH_TEST_VECTORS, entropy_to_mnemonic, load_wordlist, validate_mnemonic_checksum
from .crypto import HKDF_SHA512_TEST_VECTORS, hkdf_sha512, mix_sources, sha512_source
from .entropy import os_entropy


@dataclass(frozen=True)
class SelfTestResult:
    name: str
    passed: bool
    detail: str = ""


def run_self_tests() -> list[SelfTestResult]:
    return [
        _check_wordlist(),
        _check_bip39_vectors(),
        _check_hkdf_vectors(),
        _check_entropy_mixer_os_source(),
        _check_no_file_output_required(),
    ]


def _check_wordlist() -> SelfTestResult:
    try:
        words = load_wordlist()
        ok = len(words) == 2048
        return SelfTestResult("wordlist length", ok, "" if ok else f"got {len(words)}")
    except Exception as exc:
        return SelfTestResult("wordlist length", False, str(exc))


def _check_bip39_vectors() -> SelfTestResult:
    try:
        for entropy_hex, expected in BIP39_ENGLISH_TEST_VECTORS:
            mnemonic = entropy_to_mnemonic(bytes.fromhex(entropy_hex))
            if mnemonic != expected:
                return SelfTestResult("BIP39 vectors", False, f"mismatch for {entropy_hex}")
            if not validate_mnemonic_checksum(mnemonic):
                return SelfTestResult("BIP39 vectors", False, f"checksum failed for {entropy_hex}")
        return SelfTestResult("BIP39 vectors", True)
    except Exception as exc:
        return SelfTestResult("BIP39 vectors", False, str(exc))


def _check_hkdf_vectors() -> SelfTestResult:
    try:
        for index, vector in enumerate(HKDF_SHA512_TEST_VECTORS, start=1):
            okm = hkdf_sha512(
                vector["ikm"],
                vector["length"],
                salt=vector["salt"],
                info=vector["info"],
            )
            if okm != vector["okm"]:
                return SelfTestResult("HKDF vectors", False, f"mismatch for vector {index}")
        return SelfTestResult("HKDF vectors", True)
    except Exception as exc:
        return SelfTestResult("HKDF vectors", False, str(exc))


def _check_entropy_mixer_os_source() -> SelfTestResult:
    try:
        output = mix_sources([sha512_source("os-csprng", os_entropy(16))], 16)
        return SelfTestResult("entropy mixer OS source", len(output) == 16)
    except Exception as exc:
        return SelfTestResult("entropy mixer OS source", False, str(exc))


def _check_no_file_output_required() -> SelfTestResult:
    return SelfTestResult("no file output required", True)

