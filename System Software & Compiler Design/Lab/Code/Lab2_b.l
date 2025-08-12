%{
#include <stdio.h>
#include <string.h>

char *keywords[] = {"if", "else", "while", "for", "int", "float", "return", "void", "char"};
int is_keyword(char *word) {
    for(int i = 0; i < sizeof(keywords)/sizeof(char*); i++) {
        if(strcmp(word, keywords[i]) == 0)
            return 1;
    }
    return 0;
}
%}

%%
[ \t\n]+            ; // Ignore whitespace
[a-zA-Z_][a-zA-Z0-9_]* {
    if (is_keyword(yytext))
        printf("<KEYWORD, %s>\n", yytext);
    else
        printf("<IDENTIFIER, %s>\n", yytext);
}
[0-9]+              printf("<NUMBER, %s>\n", yytext);
.                   printf("<SYMBOL, %s>\n", yytext);
%%

int main() {
    printf("Enter a statement:\n");
    yylex();
    return 0;
}

int yywrap() {
    return 1;
}
