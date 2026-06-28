from entropyseed.crypto import mix_sources, sha512_source


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
