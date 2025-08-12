%{
#include <stdio.h>
int token_count = 0;
%}

%%
[ \t\n]+              ;
[a-zA-Z_][a-zA-Z0-9_]* { 
    token_count++; 
    printf("Token: %-15s Length: %d\n", yytext, yyleng); 
}
[0-9]+               { 
    token_count++; 
    printf("Token: %-15s Length: %d\n", yytext, yyleng); 
}
.                    {
    token_count++; 
    printf("Token: %-15s Length: %d\n", yytext, yyleng); 
}
%%

int main() {
    printf("Enter a statement:\n");
    yylex();
    printf("\nTotal Tokens: %d\n", token_count);
    return 0;
}

int yywrap() {
    return 1;
}
