from kyber.constants import q, n

class PolynomialRing:
    def __init__(self, coefs: list[int]) -> None:
        """Input `(1, 2, 3)` represents `1+2x+3x^2`."""
        self._coefs = [int(c) for c in coefs]
        self._coef_limit = q
        self._degree_limit = n-1
        self._apply_limits()

    @property
    def coefs(self) -> list[int]:
        return self._coefs

    def _apply_limits(self) -> None:
        # apply degree limit by dividing self by x^n+1
        self._apply_polynomial_modulo_limit()

        # apply coef limit
        for i in range(len(self._coefs)):
            self._coefs[i] %= self._coef_limit

        # remove trailing zero coefficients
        while len(self._coefs) > 0 and self._coefs[-1] == 0:
            self._coefs.pop()

    def _apply_polynomial_modulo_limit(self) -> None:
        """Replaces `self._coefs` with the remainder of division `self._coefs / (x^n+1)`."""
        # this is an optimal version of polynomial long division
        while len(self._coefs) >= n+1:
            self._coefs[-n-1] -= self._coefs[-1]
            self._coefs[-1] = 0
            while self._coefs[-1] == 0:
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

    def __repr__(self) -> str:
        return "PolRing(" + ", ".join([str(c) for c in self.coefs]) + ")"
