# Requirements specification

### Problem to be solved

When two people want to communicate securely with each other using insecure network, they need to use encryption. One way of doing this would be to use asymmetric encryption, in which both would encrypt the payload with recipient's public key. However, asymmetric encryption is relatively slow when the payload gets longer. Therefore it is common to use asymmetric encryption to securely share a key that will then be used in faster asymmetric encryption. This is called key encapsulation mechanism, KEM [6].

Traditionally [Diffie–Hellman](https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange) method has been used for this [6], but because of Shor's algorithm it is thought not to be safe against powerful quantum computers. For this demand of quantum-resistant asymmetric encryption suitable for key-sharing was developed a new algorithm called CRYSTALS-Kyber. In 2022 National Institute of Standards and Technology (NIST) selected Kyber among three other algorithms to be the first post-quantum standards [4]. In August 2023 NIST released a candidate for the final standard [5] and this project is based on that.

### Input and output

This project will be a package that can be used by other Python projects to easily implement Kyber encryption. The package provides three simple functions with a few parameters and return values:

* `private_key, public_key = generate_keys()`
* `secret, ciphertext = encrypt(public_key)`
* `secret = decrypt(private_key, ciphertext)`

When given corresponding public and private keys and right ciphertext as arguments, both `encrypt` and `decrypt` will return the same secret that can then be used as a key in symmetric encryption.

### Algorithms and data structures

At the core Kyber is based on _lattices_ and _module learning with errors_ problem and thus the solution will involve mathematics of polynomial vectors. 
[2, 3]

Calculations will also be performed in modulo of some polynomial and integer, that is, working in [polynomial ring](https://en.wikipedia.org/wiki/Polynomial_ring) structure [1, 3]. For finding a remainder of two polynomials, I expect to use [polynomial long division](https://en.wikipedia.org/wiki/Polynomial_long_division#Polynomial_long_division) algorithm.

As the official specification document states, the solution will include usage of standard hashing functions of SHA-3. This functionality will, however, be imported from a dependency.

There is also a need to generate random bytestreams. This will be implemented by first generating randomity with a dependency and then modifying it according to the reference [1].

### Time and space requirement

Encryption and decryption functions are expected to run at `O(n^2)` time, where n is the length of the payload.

Key generation function has no parameters as will thus run at constant time and memory.

### Language

This project will be written in Python. Documentation, code and comments will all be written in English.

### About me

I am a student of computer science bachelor program (in Finnish: tietojenkäsittelytieteen kandidaatti, TKT).

In addition to Python I can review code in JavaScript and Swift.

### See also

Here are some materials that I found helpful in understanding the operating principle of Kyber but that I did not use as a reference in this document:

* Houston-Edwards, Kelsey: Lattice-based cryptography: The tricky math of dots (2023) [https://youtube.com/watch?v=QDdOoYdb748](https://youtube.com/watch?v=QDdOoYdb748)
* Houston-Edwards, Kelsey: Learning with errors: Encrypting with unsolvable equations (2023) [https://youtube.com/watch?v=K026C5YaB3A](https://youtube.com/watch?v=K026C5YaB3A)

### References

1. Avanzi, Roberto et al.: Algorithm Specifications And Supporting Documentation (version 3.02, 2021), URL: [https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf](https://pq-crystals.org/kyber/data/kyber-specification-round3-20210804.pdf) (accessed 2023-11-02)
2. Cryptographic Suite for Algebraic Lattices: Kyber, URL: [https://pq-crystals.org/kyber/index.shtml](https://pq-crystals.org/kyber/index.shtml) (accessed 2023-11-02)
3. Gonzalez, Ruben: Kyber - How does it work? (2021), URL: [https://cryptopedia.dev/posts/kyber/](https://cryptopedia.dev/posts/kyber/) (accessed 2023-11-03)
4. National Institute of Standards and Technology: NIST Announces First Four Quantum-Resistant Cryptographic Algorithms (2022), URL: [https://www.nist.gov/news-events/news/2022/07/nist-announces-first-four-quantum-resistant-cryptographic-algorithms](https://www.nist.gov/news-events/news/2022/07/nist-announces-first-four-quantum-resistant-cryptographic-algorithms) (accessed 2023-11-02)
5. National Institute of Standards and Technology: NIST to Standardize Encryption Algorithms That Can Resist Attack by Quantum Computers (2023), URL: [https://www.nist.gov/news-events/news/2023/08/nist-standardize-encryption-algorithms-can-resist-attack-quantum-computers](https://www.nist.gov/news-events/news/2023/08/nist-standardize-encryption-algorithms-can-resist-attack-quantum-computers) (accessed 2023-11-03)
6. Wikipedia: Key encapsulation mechanism, URL: [https://en.wikipedia.org/wiki/Key\_encapsulation\_mechanism](https://en.wikipedia.org/wiki/Key_encapsulation_mechanism) (accessed 2023-11-04)
