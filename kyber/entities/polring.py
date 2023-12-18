from kyber.constants import q, n

class PolynomialRing:
    def __init__(self, coefs: list[int], check_limits: bool = True) -> None:
        """
        :param coefs: Coefficients of the polynomial. E.g. `[1, 2, 3]` represents `1+2x+3x^2`.
        :param check_limits: Set to `False` if coefs is already taken to modulo.
        """
        self._coefs = [int(c) for c in coefs]
        if check_limits:
            self._apply_limits()

    @property
    def coefs(self) -> list[int]:
        """Coefficients of the polynomial. E.g. `[1, 2, 3]` represents `1+2x+3x^2`."""
        return self._coefs

    def _apply_limits(self) -> None:
        """Take this polynomial to modulo `x^n+1` and coefs to modulo `q`."""
        # apply degree limit by dividing self by x^n+1
        self._apply_polynomial_modulo_limit()

        # apply coef limit
        self._coefs = [c % q for c in self._coefs]

        # remove trailing zero coefficients
        while len(self._coefs) > 0 and self._coefs[-1] == 0:
            self._coefs.pop()

    def _apply_polynomial_modulo_limit(self) -> None:
        """Replaces `self._coefs` with the remainder of division `self._coefs / (x^n+1)`."""
        # this is an optimal version of polynomial long division
        coef_count = len(self._coefs)
        while coef_count >= n+1:
            self._coefs[-n-1] -= self._coefs[-1]
            self._coefs[-1] = 0
            while coef_count > 0 and self._coefs[-1] == 0:
                self._coefs.pop()
                coef_count -= 1

    def __add__(self, other: "PolynomialRing") -> "PolynomialRing":
        result = []
        self_length = len(self._coefs)
        other_length = len(other.coefs)
        for i in range(max(self_length, other_length)):
            self_coef = self.coefs[i] if i < self_length else 0
            other_coef = other.coefs[i] if i < other_length else 0
            result.append(self_coef + other_coef)
        return PolynomialRing(result)

    def __sub__(self, other: "PolynomialRing") -> "PolynomialRing":
        result = []
        self_length = len(self._coefs)
        other_length = len(other.coefs)
        for i in range(max(self_length, other_length)):
            self_coef = self.coefs[i] if i < self_length else 0
            other_coef = other.coefs[i] if i < other_length else 0
            result.append(self_coef - other_coef)
        return PolynomialRing(result)

    def __mul__(self, other: "PolynomialRing") -> "PolynomialRing":
        result = [0 for _ in range(len(self.coefs) + len(other.coefs) - 1)]
        for a in range(len(self.coefs)):
            for b in range(len(other.coefs)):
                result[a+b] += self.coefs[a] * other.coefs[b]
        return PolynomialRing(result)

    def __eq__(self, other: "PolynomialRing") -> bool:
        return self.coefs == other.coefs

    def __repr__(self) -> str:
        return "PolRing(" + ", ".join([str(c) for c in self.coefs]) + ")"
