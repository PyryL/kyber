from kyber.constants import q, n
from numpy.polynomial.polynomial import Polynomial

class PolynomialRing:
    def __init__(self, coefs: list[int]) -> None:
        """Input `(1, 2, 3)` represents `1+2x+3x^2`."""
        self._coefs = coefs
        self._coef_limit = q
        self._degree_limit = n-1
        self._apply_limits()

    @property
    def coefs(self) -> list[int]:
        return self._coefs

    def _apply_limits(self) -> None:
        # apply degree limit
        divisor = Polynomial([1] + [0 for _ in range(self._degree_limit)] + [1])    # x^n + 1
        self._coefs = [int(c) for c in (Polynomial(self.coefs) % divisor).coef]

        # apply coef limit
        for i in range(len(self._coefs)):
            self._coefs[i] %= self._coef_limit

        # remove trailing zero coefficients
        while len(self._coefs) > 0 and self._coefs[-1] == 0:
            self._coefs.pop()

    def __add__(self, other: "PolynomialRing") -> "PolynomialRing":
        result = []
        for i in range(max(len(self.coefs), len(other.coefs))):
            self_coef = self.coefs[i] if i < len(self.coefs) else 0
            other_coef = other.coefs[i] if i < len(other.coefs) else 0
            result.append(self_coef + other_coef)
        return PolynomialRing(result)

    def __sub__(self, other: "PolynomialRing") -> "PolynomialRing":
        result = []
        for i in range(max(len(self.coefs), len(other.coefs))):
            self_coef = self.coefs[i] if i < len(self.coefs) else 0
            other_coef = other.coefs[i] if i < len(other.coefs) else 0
            result.append(self_coef - other_coef)
        return PolynomialRing(result)

    def __mul__(self, other: "PolynomialRing") -> "PolynomialRing":
        result = [0 for _ in range(256)]
        for a in range(len(self.coefs)):
            for b in range(len(other.coefs)):
                # check if the term of this degree would be too high
                if a+b > 255:
                    continue
                result[a+b] += self.coefs[a] * other.coefs[b]
        return PolynomialRing(result)

    def __eq__(self, other: "PolynomialRing") -> bool:
        return self.coefs == other.coefs

    # modulo with another polring (is needed?)

    # subtraction

    # equal with another (at least for debug)

    def __repr__(self) -> str:
        return "PolRing(" + ", ".join([str(c) for c in self.coefs]) + ")"
