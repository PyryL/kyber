# Usage guide

## Installation

Make sure that you have [Poetry](https://python-poetry.org/) installed. After cloning the repository to your computer move to its root directory and run

```
poetry install
```

## Usage

Currently `kyber` provides three main functions that can be used directly from Python code. A sample usage is included in  `main.py`.

Kyber can also be used via command-line interface that can be accessed with `poetry run python cli.py`. It has four subcommands: `keygen`, `pubkey`, `encrypt` and `decrypt`. Run any subcommand with `-h` flag to get help. Below is a usage example:

```
# Alice
poetry run python cli.py keygen private.txt
poetry run python cli.py pubkey --output public.txt private.txt

# Alice sends her public.txt file to Bob

# Bob
poetry run python cli.py encrypt --key alice_public.txt --secret secret.txt --cipher cipher.txt

# Bob sends his cipher.txt file to Alice

# Alice
poetry run python cli.py decrypt --key private.txt --output secret.txt bob_cipher.txt
```

In the first line Alice generates herself a private key. On the second line she generates a public key matching the freshly-generated private key, after which she sends this public key to Bob. On the third line Bob encrypts a random shared secret with Alice's public key, after which he sends the ciphertext to Alice. On the last line Alice decrypts the ciphertext with her private key. At the end, both Alice and Bob have a file called `secret.txt` that contain the same shared secret.

### Tests

Unit tests can be run with

```
poetry run invoke test
```

### Coverage

Coverage report can be created with

```
poetry run invoke coverage-report
```

after which the report will appear at `htmlcov/index.html`.

### Performance tests

Run performance tests with

```
poetry run invoke performance
```

### Lint

Run static style cheking with

```
poetry run invoke lint
```
