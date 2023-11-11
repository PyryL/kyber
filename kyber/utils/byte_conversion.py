from math import floor, log2

def bytes_to_bits(byte_array: bytes) -> list[int]:
    """
    Takes a list of bytes as a parameter.
    Returns a list of integers where each item is 1 or 0.
    `len(return_list) == 8 * len(input_list)`
    """
    result = []
    for byte in byte_array:
        string = f"{byte:08b}"
        result += [int(x) for x in string]
    assert len(result) == 8 * len(byte_array)
    return result

def bits_to_bytes(bits: list[int]) -> bytearray:
    """
    Takes a list of bits (ints 1 and 0) as a parameter.
    Returns a list of bytes.
    First eight bits in input match with the first output byte, and so on.
    For example, input `[1,0,0,0,0,1,0,1]` outputs a byte `0b10000101 = 133`.
    `len(return_list) = len(input_list) / 8`
    """
    if  len(bits) % 8 != 0:
        raise ValueError("bit count should be multipla of 8")
    result = bytearray()
    for i in range(0, len(bits), 8):
        bytestr = "".join([str(int(a)) for a in bits[i:i+8]])
        result.append(int(bytestr, 2))
    return result

def int_to_bytes(n: int) -> bytes:
    """
    Converts the given non-negative integer into the shortest possible byte array.
    """

    if n < 0:
        raise ValueError()
    byte_count = 1 if n == 0 else floor(log2(n) / 8) + 1
    b = n.to_bytes(byte_count)
    assert b[0] != 0 or n == 0      # should not contain leading zero (except when n=0)
    return b
