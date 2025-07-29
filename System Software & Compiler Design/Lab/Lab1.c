// Lab : 1
// it lists the keyword used in written code in "input.txt";

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#define MAX_LEN 100

// List of C keywords
const char *keywords[] = {
    "auto", "break", "case", "char", "const", "continue", "default", "do", "double",
    "else", "enum", "extern", "float", "for", "goto", "if", "int", "long",
    "register", "return", "short", "signed", "sizeof", "static", "struct", "switch",
    "typedef", "union", "unsigned", "void", "volatile", "while", "_Bool", "_Complex", "_Imaginary"
};

int isKeyword(const char *word) {
    for (int i = 0; i < sizeof(keywords)/sizeof(keywords[0]); i++) {
        if (strcmp(word, keywords[i]) == 0)
            return 1;
    }
    return 0;
}

// DFA to validate identifier
int isValidIdentifier(const char *str) {
    int i = 0;
    if (!(isalpha(str[0]) || str[0] == '_'))
        return 0;
    for (i = 1; str[i] != '\0'; i++) {
        if (!(isalnum(str[i]) || str[i] == '_'))
            return 0;
    }
    return 1;
}

int isDelimiter(char ch) {
    return isspace(ch) || ch == ';' || ch == ',' || ch == '(' || ch == ')' ||
           ch == '{' || ch == '}' || ch == '[' || ch == ']' || ch == '#' || 
           ch == '<' || ch == '>' || ch == '+' || ch == '-' || ch == '*' || 
           ch == '/' || ch == '=' || ch == '&' || ch == '|' || ch == '!' || 
           ch == '%' || ch == '^' || ch == '~' || ch == '"' || ch == '\'';
}

int main() {
    FILE *fp;
    char ch, buffer[MAX_LEN];
    int i = 0;

    fp = fopen("input.c", "r");
    if (fp == NULL) {
        printf("Error: Cannot open input.c file!\n");
        return 1;
    }

    printf("Keywords:\n");
    printf("Identifiers:\n");
    printf("Others:\n");

    while ((ch = fgetc(fp)) != EOF) {
        if (isDelimiter(ch)) {
            if (i > 0) {
                buffer[i] = '\0';

                if (isKeyword(buffer)) {
                    printf("[Keyword]    : %s\n", buffer);
                } else if (isValidIdentifier(buffer)) {
                    printf("[Identifier] : %s\n", buffer);
                } else {
                    printf("[Others]     : %s\n", buffer);
                }

                i = 0;
            }

            if (!isspace(ch)) {
                // If not a space, consider as separate token
                char op[2] = {ch, '\0'};
                printf("[Others]     : %s\n", op);
            }
        } else {
            buffer[i++] = ch;
        }
    }

    fclose(fp);
    return 0;
}






/*Line By Line read*/

//#include <stdio.h>

// int main() {
//     FILE *file;
//     char buffer[1000];

//     file = fopen("example.txt", "r");

//     if (file == NULL) {
//         printf("File not found or cannot be opened.\n");
//         return 1;
//     }

//     while (fgets(buffer, sizeof(buffer), file)) {
//         printf("%s", buffer);
//         // printf("\n");
//     }

//     fclose(file);
//     return 0;
// }
