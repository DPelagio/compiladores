from enum import Enum

class Types(Enum):
    VARIABLE = 1
    NUMCONST = 2
    STRCONST = 3

class Operations(Enum):
    ADD = 1
    SUBTRACT = 2
    MULTIPLY = 3
    DIVIDE = 4
    UNARYMIN = 5
    UNARYNOT = 6
    COMPARE_EQ = 7
    COMPARE_NE = 8
    COMPARE_G = 9
    COMPARE_GE = 10
    COMPARE_L = 11
    COMPARE_LE = 12
    FUNCCALL = 13