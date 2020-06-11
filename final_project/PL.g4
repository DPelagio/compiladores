grammar PL;

program : 'Dear Program,' body 'Thank you.';
body : (ctrl_statement)*;
ctrl_statement : assign 'please'
        | if_statement
        | while_statement
        | break_statement 'please'
        | print_statement 'please'
        | function_statement
        | function_call 'please'
        | return_statement 'please' ;
        
if_statement : IF '->' expr ':' '{' body '}' (elseBody=else_statement)?;
else_statement : ELSE '{' elseBody=body '}';
while_statement : WHILE '->' expr ':' '{' body '}';
break_statement : BREAK;
print_statement : 'say' '->' (printParams=expr)? ;
function_statement : DEF funcName=NAME '=' ( '(' VARIABLE* ')' '=>' )? '{' body '}';
function_call : 'call' funcName=NAME '(' expr* ')';
return_statement : RETURN (expr)?;
assign : 'save' expr 'in' VARIABLE;

// The order of the following matters - operator priority:
expr : unaryMin='-' right=expr
      | unaryNot='!' right=expr
      | funcCall=function_call
      | '(' bracedExpr=expr ')'
      | left=expr cmp=('==' | '!=' | '>' | '>=' | '<' | '<=') right=expr
      | left=expr mul=('*' | '/') right=expr
      | left=expr add=('+' | '-') right=expr
      | VARIABLE
      | STR
      | NUMBER;


VARIABLE: '@' NAME_CHAR+;
NUMBER: DIGIT+ (DOT DIGIT+)?;
STR: '"' .*? '"';

IF: 'if';
ELSE: 'else';
WHILE: 'while';
BREAK: 'break';
PRINT: 'print';
DEF: 'const';
RETURN: 'return';
NAME: NAME_CHAR+;

WS: [ \n\t\r]+ -> skip;

fragment DIGIT: ('0'..'9');
fragment DOT: '.';
fragment NAME_CHAR: ('0'..'9'|'a'..'z'|'A'..'Z'|'_'|'-');