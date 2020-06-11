# Generated from PLParser.g4 by ANTLR 4.7.1
from antlr4 import *
from backend.AST import *
from backend.Enums import *
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

    # Visit a parse tree produced by PLParser#program.
    def visitProgram(self, ctx:PLParser.ProgramContext):
        return Body(self.visitChildren(ctx))


    # Visit a parse tree produced by PLParser#body.
    def visitBody(self, ctx:PLParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#ctrl_statement.
    def visitCtrl_statement(self, ctx:PLParser.Ctrl_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#if_statement.
    def visitIf_statement(self, ctx:PLParser.If_statementContext):
        if ctx.elseBody != None:
            return If_statement(self.visit(ctx.expr()), self.visit(ctx.body()), self.visit(ctx.elseBody))
        else:
            return If_statement(self.visit(ctx.expr()), self.visit(ctx.body()))


    # Visit a parse tree produced by PLParser#else_statement.
    def visitElse_statement(self, ctx:PLParser.Else_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PLParser#while_statement.
    def visitWhile_statement(self, ctx:PLParser.While_statementContext):
        self._loopDepth += 1
        command = While_statement(self.visit(ctx.expr()), self.visit(ctx.body()))
        self._loopDepth -= 1

        return command


    # Visit a parse tree produced by PLParser#break_statement.
    def visitBreak_statement(self, ctx:PLParser.Break_statementContext):
        if self._loopDepth == 0:
            raise Exception("'break' command found outside loop.")
        return Break_statement()


    # Visit a parse tree produced by PLParser#print_statement.
    def visitPrint_statement(self, ctx:PLParser.Print_statementContext):
        return Print_statement(self.visit(ctx.expr()))


    # Visit a parse tree produced by PLParser#function_statement.
    def visitFunction_statement(self, ctx:PLParser.Function_statementContext):
        parameters = [param.symbol.text for param in ctx.VARIABLE()]
        self._functionDepth += 1
        command = Function_statement(ctx.funcName.text, parameters, self.visit(ctx.body()))
        self._functionDepth -= 1
        
        return command


    # Visit a parse tree produced by PLParser#function_call.
    def visitFunction_call(self, ctx:PLParser.Function_callContext):
        parameters = [self.visit(param) for param in ctx.expr()]
        self._functionDepth += 1
        command = Function_call(ctx.funcName.text, parameters)
        self._functionDepth -= 1

        return command


    # Visit a parse tree produced by PLParser#return_statement.
    def visitReturn_statement(self, ctx:PLParser.Return_statementContext):
        if self._functionDepth == 0:
            raise Exception("'return' command found outside a function.")
        return Return_statement(self.visit(ctx.expr()))


    # Visit a parse tree produced by PLParser#assign.
    def visitAssign(self, ctx:PLParser.AssignContext):
        if (ctx.expr() != None):
            return Assign(ctx.VARIABLE().symbol.text, self.visit(ctx.expr()))
        else:
            return Assign(ctx.VARIABLE().symbol.text, self.visit(ctx.calculate()))


    # Visit a parse tree produced by PLParser#expr.
    def visitExpr(self, ctx:PLParser.ExprContext):
        if ctx.VARIABLE() != None:
            return Expr(ctx.VARIABLE().symbol.text, Types.VARIABLE)
        elif ctx.NUMBER() != None:
            return Expr((int)(ctx.NUMBER().symbol.text), Types.NUMCONST)
        elif ctx.STR() != None:
            return Expr(ctx.STR().symbol.text[1:-1], Types.STRCONST)
        elif ctx.unaryMin != None:
            return Calculate(None, Operations.UNARYMIN, self.visit(ctx.right))
        elif ctx.unaryNot != None:
            return Calculate(None, Operations.UNARYNOT, self.visit(ctx.right))
        elif ctx.funcCall != None:
            return Calculate(None, Operations.FUNCCALL, self.visit(ctx.funcCall))
        elif ctx.bracedExpr != None:
            return self.visit(ctx.bracedExpr)
        elif ctx.mul != None or ctx.add != None or ctx.cmp != None:
            operators = {
                "+": Operations.ADD,
                "-": Operations.SUBTRACT,
                "*": Operations.MULTIPLY,
                "/": Operations.DIVIDE,
                "==": Operations.COMPARE_EQ,
                "!=": Operations.COMPARE_NE,
                ">": Operations.COMPARE_G,
                ">=": Operations.COMPARE_GE,
                "<": Operations.COMPARE_L,
                "<=": Operations.COMPARE_LE,
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