import argparse
from base64 import b64encode
from kyber.ccakem import ccakem_generate_keys, ccakem_encrypt, ccakem_decrypt
from kyber.constants import k, n

class CLI:
    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser()
        subparsers = self._parser.add_subparsers(title="command", required=True)

        keygen_parser = subparsers.add_parser("keygen")
        keygen_parser.set_defaults(command="keygen")
        keygen_parser.add_argument("outfile")

        pubkey_parser = subparsers.add_parser("pubkey", description="extract public key from private key")
        pubkey_parser.set_defaults(command="pubkey")
        pubkey_parser.add_argument("privkeyfile", help="file that contains the private key")
        pubkey_parser.add_argument("--output", "-o", metavar="FILE", help="file to write the public key (default: stdout)")

        encrypt_parser = subparsers.add_parser("encrypt", description="encrypt 32-byte random shared secret")
        encrypt_parser.set_defaults(command="encrypt")
        encrypt_parser.add_argument("--key", "-k", metavar="FILE", help="file that contains public key", required=True)
        encrypt_parser.add_argument("--secret", "-s", metavar="FILE", help="file to write the shared secret", required=True)
        encrypt_parser.add_argument("--cipher", "-c", metavar="FILE", help="file to write the ciphertext (default: stdout)")

        decrypt_parser = subparsers.add_parser("decrypt", description="decrypt 32-byte shared secret from ciphertext")
        decrypt_parser.set_defaults(command="decrypt")
        decrypt_parser.add_argument("--key", "-k", metavar="FILE", help="file that contains private key", required=True)
        decrypt_parser.add_argument("--output", "-o", metavar="FILE", help="file to write the shared secret (default: stdout)")
        decrypt_parser.add_argument("cipherfile", help="file that contains the ciphertext")

    def parse(self) -> None:
        args = self._parser.parse_args()
        handlers = {
            "keygen": self._handle_keygen,
            "pubkey": self._handle_pubkey,
            "encrypt": self._handle_encrypt,
            "decrypt": self._handle_decrypt,
        }
        handlers[args.command](args)

    def _handle_keygen(self, arguments) -> None:
        private_key, _ = ccakem_generate_keys()
        with open(arguments.outfile, "wb") as file:
            file.write(private_key)

    def _handle_pubkey(self, arguments) -> None:
        with open(arguments.privkeyfile, "rb") as file:
            private_key = file.read()
        public_key = private_key[12*k*n//8 : 24*k*n//8+32]
        if arguments.output is None:
            print(b64encode(public_key).decode("utf-8"))
        else:
            with open(arguments.output, "wb") as file:
                file.write(public_key)

    def _handle_encrypt(self, arguments) -> None:
        with open(arguments.key, "rb") as file:
            public_key = file.read()
        ciphertext, shared_secret = ccakem_encrypt(public_key)
        with open(arguments.secret, "wb") as file:
            file.write(shared_secret)
        if arguments.cipher is None:
            print(b64encode(ciphertext).decode("utf-8"))
        else:
            with open(arguments.cipher, "wb") as file:
                file.write(ciphertext)

    def _handle_decrypt(self, arguments) -> None:
        with open(arguments.key, "rb") as file:
            private_key = file.read()
        with open(arguments.cipherfile, "rb") as file:
            ciphertext = file.read()
        shared_secret = ccakem_decrypt(ciphertext, private_key)
        if arguments.output is None:
            print(b64encode(shared_secret).decode("utf-8"))
        else:
            with open(arguments.output, "wb") as file:
                file.write(shared_secret)

if __name__ == "__main__":
    CLI().parse()
