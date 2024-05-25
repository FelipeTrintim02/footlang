%{
#include "parser.tab.h"
extern int yylineno;
%}

%%
"repeat"          { printf("TOKEN: REPEAT\n"); return REPEAT; }
"decide"          { printf("TOKEN: DECIDE\n"); return DECIDE; }
"otherwise"       { printf("TOKEN: OTHERWISE\n"); return OTHERWISE; }
"winner"          { printf("TOKEN: WINNER\n"); return WINNER; }
[0-9]+            { yylval.ival = atoi(yytext); printf("TOKEN: INTEGER (%d)\n", yylval.ival); return INTEGER; }
"="               { printf("TOKEN: =\n"); return '='; }
"("               { printf("TOKEN: (\n"); return '('; }
")"               { printf("TOKEN: )\n"); return ')'; }
"{"               { printf("TOKEN: {\n"); return '{'; }
"}"               { printf("TOKEN: }\n"); return '}'; }
";"               { printf("TOKEN: ;\n"); return ';'; }
">"               { printf("TOKEN: >\n"); return '>'; }
"<"               { printf("TOKEN: <\n"); return '<'; }
">="              { printf("TOKEN: >=\n"); return GE; }
"<="              { printf("TOKEN: <=\n"); return LE; }
"=="              { printf("TOKEN: ==\n"); return EQ; }
"!="              { printf("TOKEN: !=\n"); return NE; }
"&&"              { printf("TOKEN: &&\n"); return AND; }
"||"              { printf("TOKEN: ||\n"); return OR; }
"+"               { printf("TOKEN: +\n"); return '+'; }
"-"               { printf("TOKEN: -\n"); return '-'; }
"*"               { printf("TOKEN: *\n"); return '*'; }
"/"               { printf("TOKEN: /\n"); return '/'; }
"velocity"        { printf("TOKEN: VELOCITY\n"); return VELOCITY; }
"energy"          { printf("TOKEN: ENERGY\n"); return ENERGY; }
[a-zA-Z_][a-zA-Z0-9_]*".""velocity" { yylval.sval = strdup(yytext); printf("TOKEN: IDENTIFIER (%s)\n", yylval.sval); return IDENTIFIER; }
[a-zA-Z_][a-zA-Z0-9_]*".""energy"   { yylval.sval = strdup(yytext); printf("TOKEN: IDENTIFIER (%s)\n", yylval.sval); return IDENTIFIER; }
\"[^\"]*\"        { yylval.sval = strdup(yytext); printf("TOKEN: STRING (%s)\n", yylval.sval); return STRING; }
[ \t\n]           { /* ignore whitespace */ }
.                 { printf("Unexpected character: %s\n", yytext); exit(1); }
%%

int yywrap(void) {
    return 1;
}
