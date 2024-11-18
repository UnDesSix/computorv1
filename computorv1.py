from logger import logger
import re


class ComputorV1:
    def __init__(self, equation):
        self.equation = equation
        self.infix_array = []
        self.postfix_array = []
        logger.debug(f"Equation: {self.equation}")

        self._make_multiplications_explicit()
        logger.debug(f"Multiplications explicit: {self.equation}")

        self._to_infix_array()
        logger.debug(f"Infix array: {self.infix_array}")

        self._to_postfix_array()
        logger.debug(f"Postfix array: {self.postfix_array}")

    def _make_multiplications_explicit(self) -> str:
        # Case 1 & 2: Variable next to variable, variable next to number, number next to variable
        # e.g., ab -> a * b, a2 -> a * 2, 2a -> 2 * a
        self.equation = re.sub(r"(?<=[a-zA-Z0-9])(?=[a-zA-Z])", " * ", self.equation)
        self.equation = re.sub(r"(?<=[a-zA-Z])(?=[a-zA-Z0-9])", " * ", self.equation)

        # Case 3 & 4: Parentheses next to variable/number and variable/number next to parentheses
        # e.g., (a)2 -> (a) * 2, 2(a) -> 2 * (a)
        self.equation = re.sub(r"(?<=[a-zA-Z0-9])(?=\()", " * ", self.equation)
        self.equation = re.sub(r"(?<=\))(?=[a-zA-Z0-9])", " * ", self.equation)

        # Case 5: Parentheses next to parentheses
        # e.g., (a)(b) -> (a) * (b)
        self.equation = re.sub(r"(?<=\))(?=\()", " * ", self.equation)

        return self.equation

    def _to_infix_array(self):
        pattern = r"[\+\-\*/\^\(\)]|\d+|[a-zA-Z]+"
        self.infix_array = re.findall(pattern, self.equation)

    def _to_postfix_array(self):
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
