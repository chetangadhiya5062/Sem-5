%{
#include <stdio.h>
%}

%%
\<[A-Za-z0-9/ ]+\>       { printf("HTML Tag Found: %s\n", yytext); }
\</?[A-Za-z]+(\s+[A-Za-z]+=\"[^\"]*\")*\>  { printf("HTML Tag Found: %s\n", yytext); }
\[[A-Za-z0-9_]+\]        { printf("SQL Tag/Clause Found: %s\n", yytext); }
SELECT|FROM|WHERE|INSERT|UPDATE|DELETE  { printf("SQL Keyword Found: %s\n", yytext); }
.|\n                  { /* Ignore everything else */ }
%%

int main() {
    printf("Enter input (Ctrl+D to stop):\n");
    yylex();
    return 0;
}
