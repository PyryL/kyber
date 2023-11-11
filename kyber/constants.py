
# all of these values are percisely defined in the official Kyber specification document

n = 256
"""
Plaintext size in bits.
"""


q = 3329
"""
Divider of polynomial coefficient modulos.
"""


k = 4
"""
Dimension of polynomial matrices.
Higher values mean improved security.
Value `4` is specifically for Kyber1024 variant.
"""


eta1 = 2
"""
Defines noise level for some polynomials.
Value `2` is specifically for Kyber1024 variant.
"""


eta2 = 2
"""
Defines noise level for some polynomials.
Value `2` is specifically for Kyber1024 variant.
"""


du = 11
"""
Specifies compression and encoding level for some polynomials.
Value `11` is specifically for Kyber1024 variant.
"""


dv = 5
"""
Specifies compression and encoding level for some polynomials.
Value `5` is specifically for Kyber1024 variant.
"""
