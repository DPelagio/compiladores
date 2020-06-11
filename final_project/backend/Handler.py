from backend.Enums import *
from backend.AST import *

class Handler(object):

    def __init__(self):
        self._variables = {}
        self._variableStack = []
        self._functions = {}
        self._shouldBreak = False
        self._shouldReturn = False

    def calculate(self, astTree):
        switcher = {
            list: self._handleList,
            Body: self._handleBody,
            Assign: self._handleAssign,
            Calculate: self._handleCalculate,
            Expr: self._handleExpr,
            Print_statement: self._handlePrint_statement,
            If_statement: self._handleIf_statement,
            While_statement: self._handleWhile_statement,
            Break_statement: self._handleBreak_statement,
            Function_statement: self._handleFunction_statement,
            Function_call: self._handleFunction_call,
            Return_statement: self._handleReturn_statement,
        }

        command = switcher.get(type(astTree), None)
        if command == None:
            print("Unknown AST item type: {0}".format(astTree.__class__.__name__))
        else:
            return command(astTree)

    def _handleList(self, tree):
        for item in tree:
            self.calculate(item)
            if self._shouldBreak or self._shouldReturn:
                return

    def _handleBody(self, tree:Body):
        self.calculate(tree.lines)

    def _handleAssign(self, tree:Assign):
        self._variables[tree.variable] = self.calculate(tree.expr)

    def _handleCalculate(self, tree:Calculate):
        switcher = {
            Operations.ADD: lambda left, right: left + right,
            Operations.SUBTRACT: lambda left, right: left - right,
            Operations.MULTIPLY: lambda left, right: left * right,
            Operations.DIVIDE: lambda left, right: left / right,
            Operations.COMPARE_EQ: lambda left, right: 1 if left == right else 0,
            Operations.COMPARE_NE: lambda left, right: 1 if left != right else 0,
            Operations.COMPARE_G: lambda left, right: 1 if left > right else 0,
            Operations.COMPARE_GE: lambda left, right: 1 if left >= right else 0,
            Operations.COMPARE_L: lambda left, right: 1 if left < right else 0,
            Operations.COMPARE_LE: lambda left, right: 1 if left <= right else 0,
            Operations.UNARYMIN: lambda left, right: -right,
            Operations.UNARYNOT: lambda left, right: 0 if right else 1,
            Operations.FUNCCALL: lambda left, right: right,
        }

        left = self.calculate(tree.left) if tree.left != None else None
        right = self.calculate(tree.right) if tree.right != None else None

        if type(left) == str or type(right) == str:
            left = str(left)
            right = str(right)

        test = switcher.get(tree.op, None)(left, right)
        return test

    def _handleExpr(self, tree:Expr):
        if tree.type == Types.VARIABLE:
            return self._variables[tree.expr]
        else:
            return tree.expr

    def _handlePrint_statement(self, tree:Print_statement):
        print(self.calculate(tree.str))
    
    def _handlePrintParam(self, param):
        if (type(param) == str):
            return param
        else:
            return str(self.calculate(param))

    def _handleIf_statement(self, tree:If_statement):
        if (self.calculate(tree.condition)):
            self.calculate(tree.body)
        elif (tree.elseBody != None):
            self.calculate(tree.elseBody)
    
    def _handleWhile_statement(self, tree:While_statement):
        while (self.calculate(tree.condition)):
            self.calculate(tree.body)
            if (self._shouldBreak or self._shouldReturn):
                self._shouldBreak = False
                break

    def _handleBreak_statement(self, tree:Break_statement):
        self._shouldBreak = True
   
    def _handleFunction_call(self, tree:Function_call):
        funcCommand:Function_statement = self._functions[tree.name]
        if len(funcCommand.params) != len(tree.params):
            raise Exception("Call {0} doesn't have the same number of parameters as the method.".format(tree.name))
        self._variableStack.append(self._variables)
        self._variables = {}
        for idx in range(len(funcCommand.params)):
            name = funcCommand.params[idx]
            expr = self.calculate(tree.params[idx])
            self._variables[name] = expr
        self.calculate(funcCommand.body)
        result = self._variables.get("$$result", None)
        self._variables = self._variableStack.pop()

        return result

    def _handleFunction_statement(self, tree:Function_statement):
        self._functions[tree.name] = tree

    def _handleReturn_statement(self, tree:Return_statement):
        self._variables["$$result"] = self.calculate(tree.expr)
        self._shouldReturn = True