%{
#include <stdio.h>
FILE *codeFile, *commentFile;
%}

%%
//[^\n]*        { fprintf(commentFile, "%s\n", yytext); }  
// This matches C++ style comments

"/*"([^*]|\*+[^*/])*\*+"/"   { fprintf(commentFile, "%s\n", yytext); } 

.|\n        { fprintf(codeFile, "%s", yytext); }
%%

int main() {
    codeFile = fopen("input.c", "w");
    commentFile = fopen("comments.txt", "w");

    if (!codeFile || !commentFile) {
        printf("Error opening files.\n");
        return 1;
    }

    yylex();

    fclose(codeFile);
    fclose(commentFile);
    return 0;
}
