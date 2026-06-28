from entropyseed.bip39 import entropy_to_mnemonic, load_wordlist, word_count_for_strength


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


def test_wordlist_shape():
    words = load_wordlist()
    assert len(words) == 2048
    assert len(set(words)) == 2048
    assert words[0] == "abandon"
    assert words[-1] == "zoo"


def test_word_count_for_strength():
    assert word_count_for_strength(128) == 12
    assert word_count_for_strength(256) == 24
