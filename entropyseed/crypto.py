"""Small cryptographic helpers used by the generator."""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass


HASH_LEN = 64
DEFAULT_SALT = b"entropyseed hkdf sha512 v1"

HKDF_SHA512_TEST_VECTORS = (
    {
        "ikm": bytes.fromhex("0b" * 22),
        "salt": bytes.fromhex("000102030405060708090a0b0c"),
        "info": bytes.fromhex("f0f1f2f3f4f5f6f7f8f9"),
        "length": 42,
        "okm": bytes.fromhex(
            "832390086cda71fb47625bb5ceb168e4c8e26a1a16ed34d9fc7fe92c1481579338"
            "da362cb8d9f925d7cb"
        ),
    },
    {
        "ikm": bytes.fromhex(
            "000102030405060708090a0b0c0d0e0f"
            "101112131415161718191a1b1c1d1e1f"
            "202122232425262728292a2b2c2d2e2f"
            "303132333435363738393a3b3c3d3e3f"
            "404142434445464748494a4b4c4d4e4f"
        ),
        "salt": bytes.fromhex(
            "606162636465666768696a6b6c6d6e6f"
            "707172737475767778797a7b7c7d7e7f"
            "808182838485868788898a8b8c8d8e8f"
            "909192939495969798999a9b9c9d9e9f"
            "a0a1a2a3a4a5a6a7a8a9aaabacadaeaf"
        ),
        "info": bytes.fromhex(
            "b0b1b2b3b4b5b6b7b8b9babbbcbdbebf"
            "c0c1c2c3c4c5c6c7c8c9cacbcccdcecf"
            "d0d1d2d3d4d5d6d7d8d9dadbdcdddedf"
            "e0e1e2e3e4e5e6e7e8e9eaebecedeeef"
            "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"
        ),
        "length": 82,
        "okm": bytes.fromhex(
            "ce6c97192805b346e6161e821ed165673b84f400a2b514b2fe23d84cd189ddf1"
            "b695b48cbd1c8388441137b3ce28f16aa64ba33ba466b24df6cfcb021ecff2"
            "35f6a2056ce3af1de44d572097a8505d9e7a93"
        ),
    },
)


@dataclass(frozen=True)
class EntropySource:
    """A named entropy source and its independent SHA-512 digest."""

    name: str
    digest: bytes


def sha512_source(name: str, data: bytes) -> EntropySource:
    if not isinstance(name, str):
        raise TypeError("source name must be a string")
    if not name:
        raise ValueError("source name is required")
    if not isinstance(data, bytes):
        raise TypeError("source data must be bytes")
    return EntropySource(name=name, digest=hashlib.sha512(data).digest())


def hkdf_sha512(ikm: bytes, length: int, *, salt: bytes = DEFAULT_SALT, info: bytes = b"") -> bytes:
    """Derive bytes with RFC 5869 HKDF using SHA-512."""

    if not isinstance(ikm, bytes):
        raise TypeError("ikm must be bytes")
    if not isinstance(length, int):
        raise TypeError("length must be an integer")
    if not isinstance(salt, bytes):
        raise TypeError("salt must be bytes")
    if not isinstance(info, bytes):
        raise TypeError("info must be bytes")
    if length <= 0:
        raise ValueError("length must be positive")
    if length > 255 * HASH_LEN:
        raise ValueError("length is too large for HKDF-SHA512")
    if not salt:
        salt = b"\x00" * HASH_LEN

    prk = hmac.new(salt, ikm, hashlib.sha512).digest()
    output = bytearray()
    previous = b""
    counter = 1

    while len(output) < length:
        previous = hmac.new(prk, previous + info + bytes([counter]), hashlib.sha512).digest()
        output.extend(previous)
        counter += 1

    return bytes(output[:length])


def mix_sources(sources: list[EntropySource], length: int, *, info: bytes = b"bip39 entropy") -> bytes:
    """Mix independently hashed sources into final entropy with HKDF-SHA512."""

    if not isinstance(length, int):
        raise TypeError("length must be an integer")
    if not isinstance(info, bytes):
        raise TypeError("info must be bytes")
    if length <= 0:
        raise ValueError("length must be positive")
    if not sources:
        raise ValueError("at least one entropy source is required")

    ikm = bytearray()
    for source in sources:
        if not isinstance(source, EntropySource):
            raise TypeError("sources must contain EntropySource values")
        if not source.name:
            raise ValueError("source name is required")
        if not isinstance(source.digest, bytes):
            raise TypeError("source digest must be bytes")
        if len(source.digest) != HASH_LEN:
            raise ValueError("source digest must be a SHA-512 digest")
        name = source.name.encode("utf-8")
        if len(name) > 255:
            raise ValueError("source name is too long")
        ikm.extend(len(name).to_bytes(1, "big"))
        ikm.extend(name)
        ikm.extend(len(source.digest).to_bytes(2, "big"))
        ikm.extend(source.digest)

    source_names = ",".join(source.name for source in sources).encode("utf-8")
    return hkdf_sha512(bytes(ikm), length, info=info + b";sources=" + source_names)
