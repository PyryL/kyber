from kyber.keygen import generate_keys
from kyber.encrypt import Encrypt

def main():
    private_key, public_key = generate_keys()
    encrypter = Encrypt(public_key)
    ciphertext = encrypter.encrypt()
    print(ciphertext)

if __name__ == "__main__":
    main()
