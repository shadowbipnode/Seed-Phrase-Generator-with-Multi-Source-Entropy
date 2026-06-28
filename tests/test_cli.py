import subprocess
import sys

from entropyseed.cli import collect_sources, confirmation_positions, derive_mnemonic, numbered_mnemonic
from entropyseed.crypto import sha512_source


def test_help_command_works():
    result = subprocess.run(
        [sys.executable, "seedgen.py", "--help"],
        text=True,
        capture_output=True,
        check=True,
    )
    assert "--strength" in result.stdout
    assert "--confirm" in result.stdout


def test_derive_256_bit_mnemonic_has_24_words():
    mnemonic = derive_mnemonic([sha512_source("os-csprng", b"fixed")], 256)
    assert len(mnemonic.split()) == 24


def test_confirmation_positions_are_four_unique_sorted_positions():
    positions = confirmation_positions(24)
    assert len(positions) == 4
    assert positions == sorted(positions)
    assert len(set(positions)) == 4
    assert all(0 <= position < 24 for position in positions)


def test_numbered_mnemonic_lists_word_positions():
    assert numbered_mnemonic("alpha beta gamma") == "1. alpha\n2. beta\n3. gamma"


def test_collect_sources_includes_requested_optional_sources(monkeypatch):
    class Args:
        strength = 256
        manual = True
        dice = True
        timer_jitter = True
        jitter_samples = 2

    monkeypatch.setattr("entropyseed.cli.os_entropy", lambda size: b"o" * size)
    monkeypatch.setattr("entropyseed.cli.manual_entropy", lambda: b"manual")
    monkeypatch.setattr("entropyseed.cli.dice_entropy", lambda: b"123456")
    monkeypatch.setattr("entropyseed.cli.timer_jitter", lambda samples: b"jitter")

    sources = collect_sources(Args())
    assert [source.name for source in sources] == [
        "os-csprng",
        "manual-typing",
        "dice-rolls",
        "timer-jitter",
    ]
