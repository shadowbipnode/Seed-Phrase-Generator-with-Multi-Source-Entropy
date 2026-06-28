import subprocess
import sys

from entropyseed.cli import (
    collect_sources,
    confirm_mnemonic,
    confirmation_positions,
    derive_mnemonic,
    numbered_mnemonic,
)
from entropyseed.crypto import sha512_source
from entropyseed.bip39 import validate_mnemonic_checksum


def test_help_command_works():
    result = subprocess.run(
        [sys.executable, "seedgen.py", "--help"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "--strength" in result.stdout
    assert "--confirm" in result.stdout
    assert "--self-test" in result.stdout


def test_self_test_command_works_without_printing_seed():
    result = subprocess.run(
        [sys.executable, "seedgen.py", "--self-test"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "PASS: wordlist length" in result.stdout
    assert "PASS: BIP39 vectors" in result.stdout
    assert "Generated BIP39 mnemonic" not in result.stdout


def test_derive_256_bit_mnemonic_has_24_words():
    mnemonic = derive_mnemonic([sha512_source("os-csprng", b"fixed")], 256)
    assert len(mnemonic.split()) == 24
    assert validate_mnemonic_checksum(mnemonic)


def test_derive_128_bit_mnemonic_validates():
    mnemonic = derive_mnemonic([sha512_source("os-csprng", b"fixed")], 128)
    assert len(mnemonic.split()) == 12
    assert validate_mnemonic_checksum(mnemonic)


def test_confirmation_positions_are_four_unique_sorted_positions():
    positions = confirmation_positions(24)
    assert len(positions) == 4
    assert positions == sorted(positions)
    assert len(set(positions)) == 4
    assert all(0 <= position < 24 for position in positions)


def test_numbered_mnemonic_lists_word_positions():
    assert numbered_mnemonic("alpha beta gamma") == "1. alpha\n2. beta\n3. gamma"


def test_confirm_mnemonic_accepts_selected_words(monkeypatch):
    answers = iter(["alpha", "gamma"])
    monkeypatch.setattr("entropyseed.cli.confirmation_positions", lambda word_count: [0, 2])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    assert confirm_mnemonic("alpha beta gamma") is True


def test_confirm_mnemonic_rejects_wrong_word(monkeypatch):
    monkeypatch.setattr("entropyseed.cli.confirmation_positions", lambda word_count: [1])
    monkeypatch.setattr("builtins.input", lambda prompt: "wrong")

    assert confirm_mnemonic("alpha beta gamma") is False


def test_collect_sources_includes_requested_optional_sources(monkeypatch):
    class Args:
        strength = 256
        manual = True
        dice = True
        timer_jitter = True
        jitter_samples = 2

    monkeypatch.setattr("entropyseed.cli.os_entropy", lambda size: b"o" * size)
    monkeypatch.setattr("entropyseed.cli.manual_entropy", lambda: b"manual")
    monkeypatch.setattr("entropyseed.cli.dice_entropy", lambda min_rolls: b"123456")
    monkeypatch.setattr("entropyseed.cli.timer_jitter", lambda samples: b"jitter")

    sources = collect_sources(Args())
    assert [source.name for source in sources] == [
        "os-csprng",
        "manual-typing",
        "dice-rolls",
        "timer-jitter",
    ]


def test_collect_sources_uses_256_bit_dice_minimum(monkeypatch):
    class Args:
        strength = 256
        manual = False
        dice = True
        timer_jitter = False
        jitter_samples = 2

    observed = {}
    monkeypatch.setattr("entropyseed.cli.os_entropy", lambda size: b"o" * size)

    def fake_dice_entropy(min_rolls):
        observed["min_rolls"] = min_rolls
        return b"1" * min_rolls

    monkeypatch.setattr("entropyseed.cli.dice_entropy", fake_dice_entropy)

    collect_sources(Args())
    assert observed["min_rolls"] == 99
