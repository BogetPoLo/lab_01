ALL_OPERATIONS: set[str] = {"*", "/", "//", "%", "-", "+"}
FIRST_PRIORITY_OPERATIONS: set[str] = {"*", "/", "//", "%"}
SECOND_PRIORITY_OPERATIONS: set[str] = {"-", "+"}

ALL_NUM: set[str] = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}

OPEN_PARENTHESIS: str = "("
CLOSE_PARENTHESIS: str = ")"

REGULAR_EXPRESSION: str = r"\d+(?:\.\d+)?|[+\-*/%]+|[()]"

LENGTH = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0
}
MASS = {
    "g": 1.0,
    "kg": 1000.0
}
ABS_ZERO = {
    "c": -273.15,
    "f": -459.67,
    "k": 0.0
}
