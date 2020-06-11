
class Body(object):
    def __init__(self, lines):
        self.lines = lines

class If_statement(object):
    def __init__(self, condition, body, elseBody=None):
        self.condition = condition
        self.body = body
        self.elseBody = elseBody

class While_statement(object):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Break_statement(object):
    def __init__(self):
        pass

class Print_statement(object):
    def __init__(self, str):
        self.str = str

class Function_statement(object):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Function_call(object):
    def __init__(self, name, params):
        self.name = name
        self.params = params

class Return_statement(object):
    def __init__(self, expr):
        self.expr = expr

class Expr(object):
    def __init__(self, expr, type):
        self.expr = expr
        self.type = type

class Calculate(object):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Assign(object):
    def __init__(self, varibale, expr):
        self.variable = varibale
        self.expr = expr