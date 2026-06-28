import pytest

from entropyseed.crypto import HKDF_SHA512_TEST_VECTORS, EntropySource, hkdf_sha512, mix_sources, sha512_source


def test_hkdf_sha512_known_vector():
    vector = HKDF_SHA512_TEST_VECTORS[0]

    assert hkdf_sha512(vector["ikm"], vector["length"], salt=vector["salt"], info=vector["info"]) == vector["okm"]


def test_hkdf_sha512_vectors_pass():
    for vector in HKDF_SHA512_TEST_VECTORS:
        assert hkdf_sha512(vector["ikm"], vector["length"], salt=vector["salt"], info=vector["info"]) == vector["okm"]


def test_hkdf_sha512_rejects_invalid_length():
    with pytest.raises(ValueError, match="positive"):
        hkdf_sha512(b"input", 0)
    with pytest.raises(ValueError, match="too large"):
        hkdf_sha512(b"input", 255 * 64 + 1)


def test_hkdf_sha512_rejects_non_bytes_inputs():
    with pytest.raises(TypeError, match="ikm"):
        hkdf_sha512("input", 16)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="salt"):
        hkdf_sha512(b"input", 16, salt="salt")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="info"):
        hkdf_sha512(b"input", 16, info="info")  # type: ignore[arg-type]


def test_source_hash_is_sha512_sized_and_named():
    source = sha512_source("manual", b"abc")
    assert source.name == "manual"
    assert len(source.digest) == 64


def test_mix_sources_is_deterministic_for_same_inputs():
    sources = [sha512_source("os-csprng", b"a"), sha512_source("dice", b"123456")]
    assert mix_sources(sources, 32) == mix_sources(sources, 32)


def test_mix_sources_changes_with_source_name():
    left = [sha512_source("a", b"same")]
    right = [sha512_source("b", b"same")]
    assert mix_sources(left, 16) != mix_sources(right, 16)


def test_mix_sources_rejects_empty_source_list():
    with pytest.raises(ValueError, match="at least one entropy source"):
        mix_sources([], 16)


def test_mix_sources_rejects_invalid_source_digest_length():
    with pytest.raises(ValueError, match="SHA-512"):
        mix_sources([EntropySource("bad", b"short")], 16)


def test_sha512_source_rejects_invalid_inputs():
    with pytest.raises(TypeError, match="source name"):
        sha512_source(123, b"data")  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="required"):
        sha512_source("", b"data")
    with pytest.raises(TypeError, match="source data"):
        sha512_source("name", "data")  # type: ignore[arg-type]
