from kyber.utils.byte_conversion import bytes_to_bits
from kyber.entities.polring import PolynomialRing

def cbd(b: bytes, eta: int) -> PolynomialRing:
    """
    Deterministically creates and returns a polynomial (degree 255)
    from the given byte array (length 64*eta).
    """

    if len(b) != 64*eta:
        raise ValueError("the length of the byte list in CBD should be 64*eta")

    bits: list[int] = bytes_to_bits(b)
    assert len(bits) == 512*eta
    f: list[int] = []
    for i in range(256):
        a, b = 0, 0
        for j in range(eta):
            a += bits[2 * i * eta + j]
            b += bits[2 * i * eta + eta + j]
        f.append(a-b)
    assert len(f) == 256
    return PolynomialRing(f)
