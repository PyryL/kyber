from kyber.ccakem import ccakem_generate_keys, ccakem_encrypt, ccakem_decrypt

def main():
    private_key, public_key = ccakem_generate_keys()
    ciphertext, shared_secret1 = ccakem_encrypt(public_key)
    shared_secret2 = ccakem_decrypt(ciphertext, private_key)

    assert shared_secret1 == shared_secret2
    assert len(shared_secret1) == 32
    print("shared secret", shared_secret1.hex())

if __name__ == "__main__":
    main()
