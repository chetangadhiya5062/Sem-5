%{
#include <stdio.h>
int charCount = 0, wordCount = 0, lineCount = 0;
%}

%%
[ \t]+              { charCount += yyleng; } /* spaces & tabs */
\n                  { charCount++; lineCount++; }
[^ \t\n]+           { charCount += yyleng; wordCount++; }
%%

int main() {
    yylex();
    printf("Characters: %d\n", charCount);
    printf("Words: %d\n", wordCount);
    printf("Lines: %d\n", lineCount);
    return 0;
}
