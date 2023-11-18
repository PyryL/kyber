from random import randbytes
from kyber.encryption import generate_keys, Encrypt, Decrypt
from kyber.utils.pseudo_random import H, G, kdf
from kyber.constants import k, n, du, dv

def ccakem_generate_keys() -> tuple[bytes, bytes]:
    """
    Generates a new keypair.
    :returns (private_key, public_key) tuple
    """

    z = randbytes(32)
    sk, pk = generate_keys()
    sk = sk + pk + H(pk) + z

    assert len(pk) == 12 * k * n//8 + 32
    assert len(sk) == 24 * k * n//8 + 96

    return (
        sk,     # private key
        pk      # public key
    )

def ccakem_encrypt(public_key: bytes) -> tuple[bytes, bytes]:
    """
    Takes public key as input and returns (ciphertext, shered_secret) as a tuple.
    Shared secret is 32 bytes in length.
    """

    assert len(public_key) == 12 * k * n//8 + 32

    m = H(randbytes(32))
    Kr = G(m + H(public_key))
    K, r = Kr[:32], Kr[32:]
    c = Encrypt(public_key, m, r).encrypt()
    K = kdf(K + H(c), 32)

    return (
        c,      # ciphertext
        K       # shared secret
    )

def ccakem_decrypt(ciphertext: bytes, private_key: bytes) -> bytes:
    """
    Decrypts the given ciphertext with the private key.
    :returns Decrypted 32-byte shared secret.
    """

    assert len(ciphertext) == du * k * n//8 + dv * n//8
    assert len(private_key) == 24 * k * n//8 + 96

    sk = private_key[: 12*k*n//8]
    pk = private_key[12*k*n//8 : 24*k*n//8+32]
    h = private_key[24*k*n//8+32 : 24*k*n//8+64]
    z = private_key[24*k*n//8+64 :]

    assert h == H(pk)

    m = Decrypt(sk, ciphertext).decrypt()
    Kr = G(m + h)
    K, r = Kr[:32], Kr[32:]
    c = Encrypt(pk, m, r).encrypt()

    if c == ciphertext:
        return kdf(K + H(c), 32)
    return kdf(z + H(c), 32)
