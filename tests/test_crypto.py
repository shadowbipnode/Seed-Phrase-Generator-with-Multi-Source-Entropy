from entropyseed.crypto import hkdf_sha512, mix_sources, sha512_source


def test_hkdf_sha512_known_vector():
    ikm = bytes.fromhex("0b" * 22)
    salt = bytes.fromhex("000102030405060708090a0b0c")
    info = bytes.fromhex("f0f1f2f3f4f5f6f7f8f9")

    assert hkdf_sha512(ikm, 42, salt=salt, info=info).hex() == (
        "832390086cda71fb47625bb5ceb168e4c8e26a1a16ed34d9fc7fe92c1481579338"
        "da362cb8d9f925d7cb"
    )


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
