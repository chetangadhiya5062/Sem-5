// Lab : 1
// it lists the keyword used in written code in "input.txt";
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX 1000

// List of all C keywords
const char* keywords[] = {
    "auto","break","case","char","const","continue","default","do","double",
    "else","enum","extern","float","for","goto","if","int","long","register",
    "return","short","signed","sizeof","static","struct","switch","typedef",
    "union","unsigned","void","volatile","while"
};
int keyword_count = sizeof(keywords)/sizeof(keywords[0]);

// Check if a word is a keyword
int isKeyword(const char* word) {
    for (int i = 0; i < keyword_count; i++) {
        if (strcmp(word, keywords[i]) == 0)
            return 1;
    }
    return 0;
}

// Check if a word is a valid identifier
int isValidIdentifier(const char* word) {
    if (!(isalpha(word[0]) || word[0] == '_'))
        return 0;

    for (int i = 1; word[i]; i++) {
        if (!(isalnum(word[i]) || word[i] == '_'))
            return 0;
    }
    return 1;
}

int main() {
    FILE *fp = fopen("example.txt", "r");
    if (!fp) {
        printf("Error: Could not open file 'example.txt'\n");
        return 1;
    }

    char word[100];
    char ch;
    int i = 0;

    // To store and print unique results
    char keywords_list[MAX][100], identifiers_list[MAX][100], others_list[MAX][5];
    int k = 0, id = 0, o = 0;

    while ((ch = fgetc(fp)) != EOF) {
        // If letter, digit, or underscore, build a word
        if (isalnum(ch) || ch == '_') {
            word[i++] = ch;
        } else {
            if (i != 0) {
                word[i] = '\0';
                if (isKeyword(word)) {
                    strcpy(keywords_list[k++], word);
                } else if (isValidIdentifier(word)) {
                    strcpy(identifiers_list[id++], word);
                }
                i = 0;
            }

            // Collect others (operators, symbols)
            if (!isspace(ch) && ch != '\n') {
                char temp[2] = {ch, '\0'};
                strcpy(others_list[o++], temp);
            }
        }
    }
    fclose(fp);

    // Remove duplicates
    // Keywords
    printf("Keywords:\n");
    for (int a = 0; a < k; a++) {
        int flag = 0;
        for (int b = 0; b < a; b++) {
            if (strcmp(keywords_list[a], keywords_list[b]) == 0)
                flag = 1;
        }
        if (!flag)
            printf("%s, ", keywords_list[a]);
    }

    // Identifiers
    printf("\n\nIdentifiers:\n");
    for (int a = 0; a < id; a++) {
        int flag = 0;
        for (int b = 0; b < a; b++) {
            if (strcmp(identifiers_list[a], identifiers_list[b]) == 0)
                flag = 1;
        }
        if (!flag)
            printf("%s, ", identifiers_list[a]);
    }

    // Others
    printf("\n\nOthers:\n");
    for (int a = 0; a < o; a++) {
        int flag = 0;
        for (int b = 0; b < a; b++) {
            if (strcmp(others_list[a], others_list[b]) == 0)
                flag = 1;
        }
        if (!flag)
            printf("%s ", others_list[a]);
    }

    printf("\n");
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
