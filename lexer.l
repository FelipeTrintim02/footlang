%{
#include "parser.tab.h"  // Inclui os tipos de tokens do Bison
%}

digit           [0-9]
letter          [a-zA-Z]
identifier      {letter}({letter}|{digit})*
number          {digit}+

%%

"pass"                          { return PASS; }
"move"                          { return MOVE; }
"decide"                        { return DECIDE; }
"otherwise"                     { return OTHERWISE; }
"repeat"                        { return REPEAT; }
"energy"                        { return ENERGY; }
"positionx"                     { return POSITIONX; }
"positiony"                     { return POSITIONY; }
"+"                             { return PLUS; }
"-"                             { return MINUS; }
"*"                             { return MULT; }
"/"                             { return DIV; }
">"                             { return GT; }
"<"                             { return LT; }
"=="                            { return EQ; }
"!="                            { return NEQ; }
"{"                             { return LBRACE; }
"}"                             { return RBRACE; }
"("                             { return LPAREN; }
")"                             { return RPAREN; }
";"                             { return SEMICOLON; }
","                             { return COMMA; }
"="                             { return ASSIGN; }

{identifier}"."{identifier}    { yylval.str = strdup(yytext); return PROPERTY; }
{identifier}                    { yylval.str = strdup(yytext); return IDENTIFIER; }
{number}                        { yylval.num = atoi(yytext); return NUMBER; }

[ \t\n\r]+                      { /* Ignore whitespace */ }

.                               { return yytext[0]; }  // Default action

%%
