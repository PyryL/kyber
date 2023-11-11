from kyber.keygen import generate_keys
from kyber.encrypt import Encrypt
from kyber.decrypt import Decrypt

def main():
    # generate keypair
    private_key, public_key = generate_keys()

    # encrypt
    encrypter = Encrypt(public_key)
    ciphertext = encrypter.encrypt()
    shared_secret1 = encrypter.secret
    
    # decrypt
    shared_secret2 = Decrypt(private_key, ciphertext).decrypt()

    # analyse
    assert shared_secret1 == shared_secret2
    assert len(shared_secret1) == 32
    print("shared secret", shared_secret1.hex())

if __name__ == "__main__":
    main()
