# Tests

All functions and methods are tested individually with sample inputs. In addition to testing with correct inputs, code is tested to fail with invalid inputs. Outputs are tested to be in correct type and to match all criteria.

In addition to unit tests, Kyber is also tested with some intergration tests. That is, a function and its inverse function are called consecutively and the output is checked to equal the original input.

Current test report:

```
tests/test_byte_conversion.py ........      [ 15%]
tests/test_cbd.py ....                      [ 22%]
tests/test_ccakem.py ....                   [ 30%]
tests/test_compression.py ......            [ 41%]
tests/test_decrypt.py ...                   [ 47%]
tests/test_encoding.py ........             [ 62%]
tests/test_encrypt.py ...                   [ 67%]
tests/test_encryption.py .                  [ 69%]
tests/test_key_generation.py ..             [ 73%]
tests/test_modulo.py ..                     [ 77%]
tests/test_parse.py ...                     [ 83%]
tests/test_pseudo_random.py ........        [ 98%]
tests/test_round.py .                       [100%]

=============== 53 passed in 0.33s ================
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
kyber/encryption/decrypt.py         26      0      6      0   100%
kyber/encryption/encrypt.py         57      0     12      0   100%
kyber/encryption/keygen.py          35      0      8      0   100%
kyber/utils/byte_conversion.py      23      0     12      0   100%
kyber/utils/cbd.py                  16      0      6      0   100%
kyber/utils/compression.py          23      0      8      0   100%
kyber/utils/encoding.py             36      0     22      0   100%
kyber/utils/modulo.py               17      0      8      0   100%
kyber/utils/parse.py                22      0      6      0   100%
kyber/utils/pseudo_random.py        23      0      0      0   100%
kyber/utils/round.py                 5      0      2      0   100%
------------------------------------------------------------------
TOTAL                              331      0     92      0   100%
```

For more detailed report, run `poetry run invoke coverage-report` and then open `htmlcov/index.html`.
