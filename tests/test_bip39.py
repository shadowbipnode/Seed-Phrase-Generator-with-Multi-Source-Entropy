from entropyseed.bip39 import (
    BIP39_ENGLISH_TEST_VECTORS,
    entropy_to_mnemonic,
    load_wordlist,
    validate_mnemonic_checksum,
    word_count_for_strength,
)


def test_bip39_vector_zero_128_bits():
    entropy = bytes.fromhex("00000000000000000000000000000000")
    assert (
        entropy_to_mnemonic(entropy)
        == "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    )


def test_bip39_vector_zero_256_bits():
    entropy = bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000")
    assert entropy_to_mnemonic(entropy) == (
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon "
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art"
    )


def test_official_bip39_english_vectors_pass():
    for entropy_hex, mnemonic in BIP39_ENGLISH_TEST_VECTORS:
        assert entropy_to_mnemonic(bytes.fromhex(entropy_hex)) == mnemonic
        assert validate_mnemonic_checksum(mnemonic)


def test_generated_128_and_256_bit_mnemonics_validate():
    assert validate_mnemonic_checksum(entropy_to_mnemonic(bytes(range(16))))
    assert validate_mnemonic_checksum(entropy_to_mnemonic(bytes(range(32))))


def test_validate_mnemonic_checksum_rejects_bad_checksum():
    mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
    assert not validate_mnemonic_checksum(mnemonic)


def test_validate_mnemonic_checksum_rejects_unknown_word():
    mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon notaword"
    assert not validate_mnemonic_checksum(mnemonic)


def test_wordlist_shape():
    words = load_wordlist()
    assert len(words) == 2048
    assert len(set(words)) == 2048
    assert words[0] == "abandon"
    assert words[-1] == "zoo"


def test_word_count_for_strength():
    assert word_count_for_strength(128) == 12
    assert word_count_for_strength(256) == 24
