# Tests

All functions and methods are tested individually with both sample and random inputs. In addition to testing with correct inputs, code is tested to fail with invalid inputs. Outputs are tested to be in correct type and to match all criteria.

In addition to unit tests, Kyber is also tested with some intergration tests. That is, a function and its inverse function are called consecutively and the output is checked to equal the original input.

Current test report:

```
tests/test_byte_conversion.py ........              [ 11%]
tests/test_cbd.py .....                             [ 18%]
tests/test_ccakem.py .....                          [ 26%]
tests/test_compression.py ......                    [ 34%]
tests/test_decrypt.py ...                           [ 39%]
tests/test_encoding.py .......                      [ 49%]
tests/test_encrypt.py ...                           [ 53%]
tests/test_encryption.py .                          [ 55%]
tests/test_key_generation.py ..                     [ 57%]
tests/test_parse.py ...                             [ 62%]
tests/test_polring.py ........                      [ 73%]
tests/test_pseudo_random.py .................       [ 98%]
tests/test_round.py .                               [100%]

=================== 69 passed in 5.08s ===================
```

Tests can be run with `poetry run invoke test`.

## Test coverage

[![codecov](https://codecov.io/gh/PyryL/kyber/graph/badge.svg?token=MXM7CFK9YQ)](https://codecov.io/gh/PyryL/kyber)

Current test coverage report:

```
Name                             Stmts   Miss Branch BrPart  Cover
------------------------------------------------------------------
kyber/ccakem.py                     34      0      2      0   100%
kyber/constants.py                  14      0      0      0   100%
kyber/encryption/decrypt.py         24      0      6      0   100%
kyber/encryption/encrypt.py         51      0     12      0   100%
kyber/encryption/keygen.py          31      0      8      0   100%
kyber/entities/polring.py           50      0     26      0   100%
kyber/utils/byte_conversion.py      23      0     12      0   100%
kyber/utils/cbd.py                  16      0      6      0   100%
kyber/utils/compression.py          23      0      8      0   100%
kyber/utils/encoding.py             34      0     20      0   100%
kyber/utils/parse.py                22      0      6      0   100%
kyber/utils/pseudo_random.py        23      0      0      0   100%
kyber/utils/round.py                 5      0      2      0   100%
------------------------------------------------------------------
TOTAL                              350      0    108      0   100%
```

For more detailed report, run `poetry run invoke coverage-report` and then open `htmlcov/index.html`.

## Performance tests

The asymmetric encryption part of Kyber (called CPAPKE in the specification document) only works with fixed-lengthed input, but we can split larger payload into 32-byte chunks and encrypt them separately. Ciphertexts can be concatenated and the whole process can be reversed during decryption. Using this method, encryption is tested in `perf_tests/test_encryption.py` with about 10 kibibytes of random payload.

End-to-end process of Kyber handshake is iterated a couple of hundred times in `perf_tests/test_ccakem.py`.

In addition, there is an illustrative and comparable test in `perf_tests/test_aes_integration.py` that integrates Kyber with AES encryption to point out how much faster it is to use key encapsulation mechanism instead of asymmetric encryption.

Performance tests can be run with `poetry run invoke performance`.
