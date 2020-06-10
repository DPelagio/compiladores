
class Body(object):
    def __init__(self, lines):
        self.lines = lines

class IfCommand(object):
    def __init__(self, condition, body, elseBody=None):
        self.condition = condition
        self.body = body
        self.elseBody = elseBody

class WhileCommand(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class BreakCommand(object):
    def __init__(self):
        pass

class PrintCommand(object):
    def __init__(self, str):
        self.str = str

class FunctionCommand(object):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(object):
    def __init__(self, name, params):
        self.name = name
        self.params = params

class ReturnCommand(object):
    def __init__(self, value):
        self.value = value

class Value(object):
    def __init__(self, value, type):
        self.value = value
        self.type = type

class Calculate(object):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assign(object):
    def __init__(self, varibale, value):
        self.variable = varibale
        self.value = value