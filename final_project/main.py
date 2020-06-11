import sys
import antlr4
from PLLexer import PLLexer
from PLParser import PLParser
from PLVisitor import PLVisitor
from backend.Handler import Handler

def main(argv):
    if len(sys.argv) > 1 :
        if argv[1].endswith(".please"):
            istream = antlr4.FileStream(argv[1])
            lexer = PLLexer(istream)
            stream = antlr4.CommonTokenStream(lexer)
            parser = PLParser(stream)
            tree = parser.program()
            visitor = PLVisitor()
            astTree = visitor.visit(tree)
            handler = Handler()
            handler.calculate(astTree)

            print(tree.toStringTree(recog=parser), "\n")
            print(astTree.__dict__)

        else:
            print("The file extension is not valid for the 'Nice Language'.\nPlease use a file with the .please extension.\n")
    else:
        print("There was no file specified. Please provide a file name with the .please extension as an argument to the python3 command.\n")

if __name__ == '__main__':
    main(sys.argv)

