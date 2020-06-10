
grammar PL;

options { tokenVocab=PLLexer; }

script : GREETING body END;
body : (command | comment)*;
command : assign SEMI
        | if_command
        | while_command
        | break_command SEMI
        | print_command SEMI
        | function_command
        | function_call SEMI
        | return_command SEMI;
if_command : IF ARROW value COLUMN CURLY_L body CURLY_R (elseBody=else_command)?    # IfCommandBody
           | IF ARROW value COLUMN command (elseBody=else_command)?                 # IfCommandSingle;
else_command : ELSE CURLY_L elseBody=body CURLY_R                                      # ElseCommandBody
             | ELSE elseLine=command                                                   # ElseCommandSingle;
while_command : WHILE BRACE_L value BRACE_R CURLY_L body CURLY_R                       # WhileCommandBody
              | WHILE BRACE_L value BRACE_R command                                    # WhileCommandSingle;
break_command : BREAK                                                                  # BreakCommand;
print_command : PRINT BRACE_L (printParams=value)? BRACE_R                             # PrintCommand;
function_command : DEF funcName=NAME BRACE_L VARIABLE* BRACE_R CURLY_L body CURLY_R    # FunctionCommand;
function_call : funcName=NAME BRACE_L value* BRACE_R                                   # FunctionCall;
return_command : RETURN (value)?                                                       # ReturnCommand;
comment : COMMENT;
assign : SAVE value IN VARIABLE;

// The order of the following matters - operator priority:
value : unaryMin=SUBTRACT right=value
      | unaryNot=EXCL right=value
      | funcCall=function_call
      | BRACE_L bracedValue=value BRACE_R
      | left=value cmp=(COMPARE_EQ | COMPARE_NE | COMPARE_G | COMPARE_GE | COMPARE_L | COMPARE_LE) right=value
      | left=value mul=(MULTIPLY | DIVIDE) right=value
      | left=value add=(ADD | SUBTRACT) right=value
      | VARIABLE
      | STR
      | NUMBER;

COLUMN: ':';
ARROW: '->';
GREETING: 'Dear Program,';
IN: 'in';
SAVE: 'save';
END: 'Thank you.';
EQUAL: '=';
ADD: '+';
SUBTRACT: '-';
MULTIPLY: '*';
DIVIDE: '/';
SEMI: ';';
BRACE_L: '(';
BRACE_R: ')';
CURLY_L: '{';
CURLY_R: '}';
EXCL: '!';
COMMA: ',';
VARIABLE: '@' NAME_CHAR+;
COMMENT: '#' .*?;
NUMBER: DIGIT+ (DOT DIGIT+)?;
STR: '"' .*? '"';

COMPARE_EQ: '==';
COMPARE_NE: '!=';
COMPARE_G: '>';
COMPARE_GE: '>=';
COMPARE_L: '<';
COMPARE_LE: '<=';

IF: 'if';
ELSE: 'else';
WHILE: 'while';
BREAK: 'break';
PRINT: 'print';
DEF: 'def';
RETURN: 'return';
NAME: NAME_CHAR+;

WS: [ \n\t\r]+ -> skip;

fragment DIGIT: ('0'..'9');
fragment DOT: '.';
fragment NAME_CHAR: ('0'..'9'|'a'..'z'|'A'..'Z'|'_'|'-');