%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();
void yyerror(const char *s);
%}

%union {
    int num;      // Para armazenar valores numéricos
    char* str;    // Para armazenar strings
}

%token <str> IDENTIFIER PROPERTY
%token <num> NUMBER
%token PASS MOVE DECIDE OTHERWISE REPEAT ENERGY POSITIONX POSITIONY
%token PLUS MINUS MULT DIV GT LT EQ NEQ
%token LBRACE RBRACE LPAREN RPAREN SEMICOLON COMMA ASSIGN

%type <num> expression number  // Definindo o tipo para 'number'
%type <str> identifier property

%%

program:
        | program statement
        ;

statement:
          assignment
        | decision
        | loop
        | action_statement
        ;

assignment:
        property ASSIGN expression SEMICOLON
        {
            printf("Assigning %s = %d\n", $1, $3);
        }
    | identifier ASSIGN expression SEMICOLON
        {
            printf("Assigning %s = %d\n", $1, $3);
        }
        ;

expression:
          number
        | identifier
        | property
        | expression PLUS expression
        | expression MINUS expression
        | expression MULT expression
        | expression DIV expression
        | expression GT expression
        | expression LT expression
        | expression EQ expression
        | expression NEQ expression
        ;


property:
    PROPERTY
    {
        $$ = strdup($1);
    }
    ;

identifier:
    IDENTIFIER
    {
        $$ = strdup($1);
    }
    ;

number:
    NUMBER
    {
        $$ = $1; // Confirmado que 'number' é um inteiro.
    }
    ;

loop:
    REPEAT LPAREN expression RPAREN LBRACE program RBRACE
    {
        printf("Loop with condition.\n");
    }
    ;

decision:
    DECIDE LPAREN expression RPAREN LBRACE program RBRACE OTHERWISE LBRACE program RBRACE
    {
        printf("Decision made on condition.\n");
    }
    ;

action_statement:
    identifier LPAREN identifier RPAREN SEMICOLON
    {
        printf("Action: %s(%s)\n", $1, $3);
    }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

int main(void) {
    yyparse();
    return 0;
}
