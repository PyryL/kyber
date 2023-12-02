from random import seed, randbytes
from time import time
from Crypto.Cipher import AES
from kyber.ccakem import ccakem_generate_keys, ccakem_encrypt, ccakem_decrypt

def run(payload: bytes) -> tuple[float, float, float]:
    """:returns Durations of handshake and actual payload transfer in seconds as a tuple."""

    t0 = time()

    # Alice
    private_key, public_key = ccakem_generate_keys()

    # send public_key Alice->Bob

    # Bob
    ss_ciphertext, shared_secret1 = ccakem_encrypt(public_key)

    # send ss_ciphertext Bob->Alice

    # Alice
    shared_secret2 = ccakem_decrypt(ss_ciphertext, private_key)

    t1 = time()

    # Alice
    aes_cipher = AES.new(shared_secret2, AES.MODE_GCM)
    payload_nonce = aes_cipher.nonce
    payload_ciphertext, payload_tag = aes_cipher.encrypt_and_digest(payload)

    # send payload_ciphertext, payload_tag and payload_nonce Alice->Bob

    # Bob
    aes_cipher = AES.new(shared_secret1, AES.MODE_GCM, nonce=payload_nonce)
    decrypted_payload = aes_cipher.decrypt_and_verify(payload_ciphertext, payload_tag)

    assert payload == decrypted_payload

    return (t1-t0, time()-t1)

def runner():
    seed(42)
    payload = randbytes(100_000_000)      # 100 megabytes
    print("Starting AES integration performance test (about 3 seconds)")
    durations = run(payload)
    print("Results:")
    print(f"Handshake: {durations[0]:.2f} sec")
    print(f"Payload transfer: {durations[1]:.2f} sec")
    print(f"Total: {sum(durations):.2f} sec")

if __name__ == "__main__":
    runner()
