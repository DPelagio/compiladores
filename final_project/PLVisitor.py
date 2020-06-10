# Generated from PLParser.g4 by ANTLR 4.7.1
from antlr4 import *
from calc.AstClasses import *
from calc.Enums import *
if __name__ is not None and "." in __name__:
    from .PLParser import PLParser
    
else:
    from PLParser import PLParser

# This class defines a complete generic visitor for a parse tree produced by PLParser.

class PLVisitor(ParseTreeVisitor):

    def __init__(self):
        self._loopDepth = 0
        self._functionDepth = 0

    def visitChildren(self, node):
        result = self.defaultResult()
        n = node.getChildCount()
        for i in range(n):
            if not self.shouldVisitNextChild(node, result):
                return result

            c = node.getChild(i)
            childResult = c.accept(self)
            result = self.aggregateResult(result, childResult)

        return result

    def defaultResult(self):
        return []

    def aggregateResult(self, aggregate, childResult):
        if childResult != None:
            if isinstance(childResult, list):
                aggregate.extend(childResult)
            else:
                aggregate.append(childResult)
        return aggregate

    # Visit a parse tree produced by PLParser#script.
    def visitScript(self, ctx:PLParser.ScriptContext):
        return Body(self.visitChildren(ctx))


    # Visit a parse tree produced by PLParser#body.
    def visitBody(self, ctx:PLParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#command.
    def visitCommand(self, ctx:PLParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#IfCommandBody.
    def visitIfCommandBody(self, ctx:PLParser.IfCommandBodyContext):
        if ctx.elseBody != None:
            return IfCommand(self.visit(ctx.value()), self.visit(ctx.body()), self.visit(ctx.elseBody))
        else:
            return IfCommand(self.visit(ctx.value()), self.visit(ctx.body()))


    # Visit a parse tree produced by PLParser#IfCommandSingle.
    def visitIfCommandSingle(self, ctx:PLParser.IfCommandSingleContext):
        if ctx.elseBody != None:
            return IfCommand(self.visit(ctx.value()), self.visit(ctx.command()), self.visit(ctx.elseBody))
        else:
            return IfCommand(self.visit(ctx.value()), self.visit(ctx.command()))


    # Visit a parse tree produced by PLParser#ElseCommandBody.
    def visitElseCommandBody(self, ctx:PLParser.ElseCommandBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#ElseCommandSingle.
    def visitElseCommandSingle(self, ctx:PLParser.ElseCommandSingleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#WhileCommandBody.
    def visitWhileCommandBody(self, ctx:PLParser.WhileCommandBodyContext):
        self._loopDepth += 1
        command = WhileCommand(self.visit(ctx.value()), self.visit(ctx.body()))
        self._loopDepth -= 1

        return command


    # Visit a parse tree produced by PLParser#WhileCommandSingle.
    def visitWhileCommandSingle(self, ctx:PLParser.WhileCommandSingleContext):
        self._loopDepth += 1
        command = WhileCommand(self.visit(ctx.value()), self.visit(ctx.command()))
        self._loopDepth -= 1

        return command


    # Visit a parse tree produced by PLParser#BreakCommand.
    def visitBreakCommand(self, ctx:PLParser.BreakCommandContext):
        if self._loopDepth == 0:
            raise Exception("'break' command found outside loop.")
        return BreakCommand()

    # Visit a parse tree produced by PLParser#PrintCommand.
    def visitPrintCommand(self, ctx:PLParser.PrintCommandContext):
        return PrintCommand(self.visit(ctx.value()))

    # Visit a parse tree produced by PLParser#FunctionCommand.
    def visitFunctionCommand(self, ctx:PLParser.FunctionCommandContext):
        parameters = [param.symbol.text for param in ctx.VARIABLE()]
        return FunctionCommand(ctx.funcName.text, parameters, self.visit(ctx.body()))


    # Visit a parse tree produced by PLParser#FunctionCall.
    def visitFunctionCall(self, ctx:PLParser.FunctionCallContext):
        parameters = [self.visit(param) for param in ctx.value()]
        self._functionDepth += 1
        command = FunctionCall(ctx.funcName.text, parameters)
        self._functionDepth -= 1

        return command


    # Visit a parse tree produced by PLParser#ReturnCommand.
    def visitReturnCommand(self, ctx:PLParser.ReturnCommandContext):
        if self._functionDepth == 0:
            raise Exception("'return' command found outside a function.")
        return ReturnCommand(self.visit(ctx.value()))


    # Visit a parse tree produced by PLParser#comment.
    def visitComment(self, ctx:PLParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#assign.
    def visitAssign(self, ctx:PLParser.AssignContext):
        if (ctx.value() != None):
            return Assign(ctx.VARIABLE().symbol.text, self.visit(ctx.value()))
        else:
            return Assign(ctx.VARIABLE().symbol.text, self.visit(ctx.calculate()))


    # Visit a parse tree produced by PLParser#value.
    def visitValue(self, ctx:PLParser.ValueContext):
        if ctx.VARIABLE() != None:
            return Value(ctx.VARIABLE().symbol.text, ValueType.VARIABLE)
        elif ctx.NUMBER() != None:
            return Value((int)(ctx.NUMBER().symbol.text), ValueType.NUMCONST)
        elif ctx.STR() != None:
            return Value(ctx.STR().symbol.text[1:-1], ValueType.STRCONST)
        elif ctx.unaryMin != None:
            return Calculate(None, OperatorType.UNARYMIN, self.visit(ctx.right))
        elif ctx.unaryNot != None:
            return Calculate(None, OperatorType.UNARYNOT, self.visit(ctx.right))
        elif ctx.funcCall != None:
            return Calculate(None, OperatorType.FUNCCALL, self.visit(ctx.funcCall))
        elif ctx.bracedValue != None:
            return self.visit(ctx.bracedValue)
        elif ctx.mul != None or ctx.add != None or ctx.cmp != None:
            operators = {
                "+": OperatorType.ADD,
                "-": OperatorType.SUBTRACT,
                "*": OperatorType.MULTIPLY,
                "/": OperatorType.DIVIDE,
                "==": OperatorType.COMPARE_EQ,
                "!=": OperatorType.COMPARE_NE,
                ">": OperatorType.COMPARE_G,
                ">=": OperatorType.COMPARE_GE,
                "<": OperatorType.COMPARE_L,
                "<=": OperatorType.COMPARE_LE,
            }
            if ctx.mul != None:
                op = operators[ctx.mul.text]
            elif ctx.cmp != None:
                op = operators[ctx.cmp.text]
            else:
                op = operators[ctx.add.text]

            return Calculate(self.visit(ctx.left), op, self.visit(ctx.right))
        else:
            return self.visitChildren(ctx)



del PLParser