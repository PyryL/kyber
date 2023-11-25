from random import randbytes
from time import time
from kyber.encryption import Encrypt, Decrypt, generate_keys
from kyber.constants import k, n, du, dv

def run(payload: bytes) -> tuple[float, float, float]:
    t0 = time()

    private_key, public_key = generate_keys()

    t1 = time()

    ciphertext = bytearray()
    for i in range(0, len(payload), 32):
        ciphertext += Encrypt(public_key, payload[i:i+32]).encrypt()

    t2 = time()

    ciphertext_chunk_size = du*k*n//8 + dv*n//8
    restored_payload = bytearray()
    for i in range(0, len(ciphertext), ciphertext_chunk_size):
        restored_payload += Decrypt(private_key, ciphertext[i:i+ciphertext_chunk_size]).decrypt()
    
    t3 = time()

    assert payload == restored_payload

    return (t1-t0, t2-t1, t3-t2)

def runner():
    payload = randbytes(10_048)   # about 10 kiB, multipla of 32
    print("Starting encryption performance test (about 1 min)")
    durations = run(payload)
    print("Results:")
    print(f"Keypair generation: {durations[0]:.2f} sec")
    print(f"Encryption: {durations[1]:.2f} sec")
    print(f"Decryption: {durations[2]:.2f} sec")
    print(f"Total: {sum(durations):.2f} sec")

if __name__ == "__main__":
    runner()
