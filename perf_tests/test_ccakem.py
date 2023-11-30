from time import time
from kyber.ccakem import ccakem_generate_keys, ccakem_encrypt, ccakem_decrypt

def run_test() -> tuple[float, float, float]:
    t0 = time()

    private_key, public_key = ccakem_generate_keys()

    t1 = time()

    ciphertext, shared_secret1 = ccakem_encrypt(public_key)

    t2 = time()

    shared_secret2 = ccakem_decrypt(ciphertext, private_key)

    t3 = time()

    assert shared_secret1 == shared_secret2

    return (t1-t0, t2-t1, t3-t2)

def runner():
    print("Starting ccakem performance test (about 2 mins)")

    test_iters = 250
    averages = [0, 0, 0]

    for _ in range(test_iters):
        durations = run_test()
        averages = [averages[i]+durations[i] for i in range(3)]

    print("Results (averages):")
    print(f"Keypair generation: {averages[0]/test_iters:.5f} sec")
    print(f"Encryption: {averages[1]/test_iters:.5f} sec")
    print(f"Decryption: {averages[2]/test_iters:.5f} sec")

if __name__ == "__main__":
    runner()
