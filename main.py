from kyber.keygen import generate_keys

def main():
    private_key, public_key = generate_keys()
    print(private_key)
    print(public_key)

if __name__ == "__main__":
    main()
