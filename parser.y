%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex(void);

%}

%union {
    int ival;
    char *sval;
}

%token <sval> IDENTIFIER STRING
%token <ival> INTEGER
%token REPEAT DECIDE OTHERWISE WINNER
%token GE LE EQ NE AND OR

%type <sval> expression term factor identifier
%type <sval> statement loop decision block winner_statement

%%

program:
    statement_list
    { printf("Parsing completed successfully.\n"); }
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
    '{' statement_list '}'
    | '{' '}'
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
    INTEGER              { $$ = (char*) malloc(20); sprintf($$, "%d", $1); }
    | identifier        { $$ = strdup($1); }
    | '(' expression ')' { $$ = strdup($2); }
    ;

identifier:
    IDENTIFIER
    ;

winner_statement:
    WINNER '(' STRING ')' ';'
    | WINNER '(' identifier ')' ';'
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    printf("Starting parsing...\n");
    return yyparse();
}
