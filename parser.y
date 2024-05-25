%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);

extern int yylineno;
extern char *yytext;

%}

%union {
    int ival;
    char *sval;
}

%token REPEAT DECIDE OTHERWISE WINNER
%token VELOCITY ENERGY IDENTIFIER
%token INTEGER STRING
%token GE LE EQ NE
%token AND OR

%left OR
%left AND
%left '>' '<' GE LE EQ NE
%left '+' '-'
%left '*' '/'

%%

program:
    statement_list
    ;

statement_list:
    statement
    | statement_list statement
    ;

statement:
    assignment
    | loop
    | decision
    | block
    | winner_statement
    ;

assignment:
    identifier '=' expression ';'
    ;

loop:
    REPEAT '(' expression ')' block
    ;

decision:
    DECIDE '(' expression ')' block
    | DECIDE '(' expression ')' block OTHERWISE block
    ;

block:
    '{' '}'
    | '{' statement_list '}'
    ;

expression:
    term
    | expression '+' term
    | expression '-' term
    | expression '*' term
    | expression '/' term
    | expression '>' term
    | expression '<' term
    | expression GE term
    | expression LE term
    | expression EQ term
    | expression NE term
    | expression AND term
    | expression OR term
    ;

term:
    factor
    ;

factor:
    INTEGER
    | identifier
    | '(' expression ')'
    ;

identifier:
    IDENTIFIER
    ;

winner_statement:
    WINNER '(' STRING ')' ';'
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s at line %d, before token: %s\n", s, yylineno, yytext);
}

int main(void) {
    printf("Starting parsing...\n");
    return yyparse();
}
