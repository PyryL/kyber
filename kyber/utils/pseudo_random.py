from Crypto.Hash import SHAKE256, SHA3_512, SHAKE128
from typing import Generator

def prf(s: bytes, b: bytes) -> bytes:
    """
    A pseudo-random function that deterministically returns 128 bytes
    based on the given byte arrays.
    Returns the same bytes whenever called with same arguments.
    Based on SHAKE256 extendable-output function.
    """

    shake = SHAKE256.new()
    shake.update(s + b)
    return shake.read(128)

def G(b: bytes) -> bytes:
    """
    Deterministically returns 64 pseudo-random bytes based on the given byte array.
    Returns the same bytes whenever called with the same argument.
    Based on SHA3-512 hash.
    """

    h = SHA3_512.new()
    h.update(b)
    return h.digest()

def xof(p: bytearray, i: bytes, j: bytes) -> Generator[bytes, None, None]:
    """Generator that yields a single pseudo-random byte at a time based on the given inputs."""
    shake = SHAKE128.new()
    shake.update(p + i + j)
    while True:
        yield shake.read(1)
