// Lab : 1
// it lists the keyword used in written code in "input.txt";

#include <stdio.h>

int main() {
    FILE *file;
    char word[100];

    const char *keywords[] = {
        "auto", "break", "case", "char", "const", "continue", "default", "do",
        "double", "else", "enum", "extern", "float", "for", "goto", "if",
        "int", "long", "register", "return", "short", "signed", "sizeof", "static",
        "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
    };

    int num_keyword = sizeof(keywords)/sizeof(keywords[0]);

    file = fopen("example.txt", "r");

    if (file == NULL) {
        printf("File not found or cannot be opened.\n");
        return 1;
    }

    printf("Keyword Found : ");

    
    while (fscanf(file, "%s", word) != EOF) {
        for (int i = 0; i < num_keyword; i++){
            if (strcmp(word, keywords[i]) == 0){
                printf("%s\n", word);
            }
        }
        // putchar(ch);
    }
    

    fclose(file);

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
