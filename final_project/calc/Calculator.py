from calc.Enums import *
from calc.AstClasses import *

class Calculator(object):

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
            Value: self._handleValue,
            PrintCommand: self._handlePrintCommand,
            IfCommand: self._handleIfCommand,
            WhileCommand: self._handleWhileCommand,
            BreakCommand: self._handleBreakCommand,
            FunctionCommand: self._handleFunctionCommand,
            FunctionCall: self._handleFunctionCall,
            ReturnCommand: self._handleReturnCommand,
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
        self._variables[tree.variable] = self.calculate(tree.value)

    def _handleCalculate(self, tree:Calculate):
        switcher = {
            OperatorType.ADD: lambda left, right: left + right,
            OperatorType.SUBTRACT: lambda left, right: left - right,
            OperatorType.MULTIPLY: lambda left, right: left * right,
            OperatorType.DIVIDE: lambda left, right: left / right,
            OperatorType.COMPARE_EQ: lambda left, right: 1 if left == right else 0,
            OperatorType.COMPARE_NE: lambda left, right: 1 if left != right else 0,
            OperatorType.COMPARE_G: lambda left, right: 1 if left > right else 0,
            OperatorType.COMPARE_GE: lambda left, right: 1 if left >= right else 0,
            OperatorType.COMPARE_L: lambda left, right: 1 if left < right else 0,
            OperatorType.COMPARE_LE: lambda left, right: 1 if left <= right else 0,
            OperatorType.UNARYMIN: lambda left, right: -right,
            OperatorType.UNARYNOT: lambda left, right: 0 if right else 1,
            OperatorType.FUNCCALL: lambda left, right: right,
        }

        left = self.calculate(tree.left) if tree.left != None else None
        right = self.calculate(tree.right) if tree.right != None else None

        if type(left) == str or type(right) == str:
            left = str(left)
            right = str(right)

        test = switcher.get(tree.op, None)(left, right)
        return test

    def _handleValue(self, tree:Value):
        if tree.type == ValueType.VARIABLE:
            return self._variables[tree.value]
        else:
            return tree.value

    def _handlePrintCommand(self, tree:PrintCommand):
        print(self.calculate(tree.str))
    
    def _handlePrintParam(self, param):
        if (type(param) == str):
            return param
        else:
            return str(self.calculate(param))

    def _handleIfCommand(self, tree:IfCommand):
        if (self.calculate(tree.condition)):
            self.calculate(tree.body)
        elif (tree.elseBody != None):
            self.calculate(tree.elseBody)
    
    def _handleWhileCommand(self, tree:WhileCommand):
        while (self.calculate(tree.condition)):
            self.calculate(tree.body)
            if (self._shouldBreak or self._shouldReturn):
                self._shouldBreak = False
                break

    def _handleBreakCommand(self, tree:BreakCommand):
        self._shouldBreak = True
   
    def _handleFunctionCall(self, tree:FunctionCall):
        funcCommand:FunctionCommand = self._functions[tree.name]
        if len(funcCommand.params) != len(tree.params):
            raise Exception("Call {0} doesn't have the same number of parameters as the method.".format(tree.name))
        self._variableStack.append(self._variables)
        self._variables = {}
        for idx in range(len(funcCommand.params)):
            name = funcCommand.params[idx]
            value = self.calculate(tree.params[idx])
            self._variables[name] = value
        self.calculate(funcCommand.body)
        result = self._variables.get("$$result", None)
        self._variables = self._variableStack.pop()

        return result

    def _handleFunctionCommand(self, tree:FunctionCommand):
        self._functions[tree.name] = tree

    def _handleReturnCommand(self, tree:ReturnCommand):
        self._variables["$$result"] = self.calculate(tree.value)
        self._shouldReturn = True