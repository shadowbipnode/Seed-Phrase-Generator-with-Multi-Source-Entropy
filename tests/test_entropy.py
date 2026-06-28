import pytest

from entropyseed.entropy import dice_entropy, timer_jitter


def test_dice_entropy_accepts_valid_rolls(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "123456 123456")
    monkeypatch.setattr("entropyseed.entropy.time.perf_counter_ns", lambda: 123)

    assert dice_entropy(min_rolls=12).endswith(b":123456123456")


def test_dice_entropy_rejects_invalid_digits(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "123407")

    with pytest.raises(ValueError, match="digits 1-6"):
        dice_entropy(min_rolls=6)


def test_dice_entropy_rejects_too_short_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "123456")

    with pytest.raises(ValueError, match="at least 10 rolls"):
        dice_entropy(min_rolls=10)


def test_timer_jitter_prints_clear_collection_message(capsys):
    data = timer_jitter(samples=2, show_progress=True)

    captured = capsys.readouterr()
    assert "Collecting 2 local timer jitter samples" in captured.out
    assert "done" in captured.out
    assert len(data) == 32


def test_timer_jitter_rejects_invalid_sample_count():
    with pytest.raises(ValueError, match="positive"):
        timer_jitter(samples=0, show_progress=False)
