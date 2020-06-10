import sys
import antlr4
from PLLexer import PLLexer
from PLParser import PLParser
from PLVisitor import PLVisitor
from calc.Calculator import Calculator

def main(argv):
    istream = antlr4.FileStream(argv[1])
    lexer = PLLexer(istream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = PLParser(stream)
    tree = parser.script()
    #print(tree.toStringTree(recog=parser))

    visitor = PLVisitor()
    astTree = visitor.visit(tree)
    calculator = Calculator()
    calculator.calculate(astTree)

    print(astTree)

if __name__ == '__main__':
    main(sys.argv)

