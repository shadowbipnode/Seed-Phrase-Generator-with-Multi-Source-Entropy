"""Small cryptographic helpers used by the generator."""

from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass


HASH_LEN = 64
DEFAULT_SALT = b"entropyseed hkdf sha512 v1"


@dataclass(frozen=True)
class EntropySource:
    """A named entropy source and its independent SHA-512 digest."""

    name: str
    digest: bytes


def sha512_source(name: str, data: bytes) -> EntropySource:
    if not name:
        raise ValueError("source name is required")
    if not isinstance(data, bytes):
        raise TypeError("source data must be bytes")
    return EntropySource(name=name, digest=hashlib.sha512(data).digest())


def hkdf_sha512(ikm: bytes, length: int, *, salt: bytes = DEFAULT_SALT, info: bytes = b"") -> bytes:
    """Derive bytes with RFC 5869 HKDF using SHA-512."""

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

    if not sources:
        raise ValueError("at least one entropy source is required")

    ikm = bytearray()
    for source in sources:
        name = source.name.encode("utf-8")
        if len(name) > 255:
            raise ValueError("source name is too long")
        ikm.extend(len(name).to_bytes(1, "big"))
        ikm.extend(name)
        ikm.extend(len(source.digest).to_bytes(2, "big"))
        ikm.extend(source.digest)

    source_names = ",".join(source.name for source in sources).encode("utf-8")
    return hkdf_sha512(bytes(ikm), length, info=info + b";sources=" + source_names)
