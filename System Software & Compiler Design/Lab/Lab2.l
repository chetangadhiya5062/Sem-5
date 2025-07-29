%{
    #include <stdio.h>
    int n = 0;
%}

%%
[a-zA-Z_][a-zA-Z0-9_]*  { printf("Identifier: %s\n" , yytext); ++n;}


[ \t\n]+                 { /* skip whitespace */ }

.                       { /* ignore other characters */ }

%%
int main(){
    yylex();
    printf("\nTotal number of identifiers: %d\n", n);
    printf("Enter input (Ctrl+Z or Ctrl+D to end):\n");
    return 0;
}

int yywrap(){
    return 1;
}