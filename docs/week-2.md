# Week 2

_6. - 12.11.2023_

This week I started implementing basic functionality of Kyber. I ended up writing keypair generation, encryption and decryption functions of CPAPKE section of [the official specification](https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf). What I didn't implement yet is conversion between polynomial matrices and byte arrays, so ciphertext and other outputs are temporarily just numpy arrays instead of data. An example usage is included in [`main.py`](/main.py) and [usage guide](/docs/usage.md) is now available.

* **Monday 6.11.** Started implementing keypair generation **2h**
* **Tuesday 7.11.** Implemented encryption **2h**
* **Thursday 9.11.** Implemented decryption. Shared secrets do not match, so there must be an error somewhere in en/decryption functions. **2h**
* **Friday 10.11.** Found and fixed the error. Implementation is now functioning. **1h**
* **Saturday 11.11.** Improved code quality. Added documentation, invoke tasks, code coverage and linting. **2h**

Total working time 9 hours.

What I discovered this week was that even the official specification is not always unequivocal. I improved at combining information – especially pseudocode – from multiple sources and debugging mathematically complex algorithm.
