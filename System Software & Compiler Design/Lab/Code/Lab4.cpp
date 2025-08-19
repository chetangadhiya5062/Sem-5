#include <bits/stdc++.h>
using namespace std;

string s; int i = 0;

void E(); void T(); void F();

void match(char c) {
    if (i < s.size() && s[i] == c) i++;
    else { cout << "Rejected\n"; exit(0); }
}

void E() {
    T();
    while (i < s.size() && (s[i]=='+' || s[i]=='-')) {
        i++;
        T();
    }
}

void T() {
    F();
    while (i < s.size() && (s[i]=='*' || s[i]=='/')) {
        i++;
        F();
    }
}

void F() {
    if (s[i] == '(') {
        match('('); E(); match(')');
    }
    else if (isalpha(s[i])) i++;  
    else { cout << "Rejected\n"; exit(0); }
}

int main() {
    cout << "Enter expression: ";
    cin >> s;
    E();
    if (i == s.size()) cout << "Accepted\n";
    else cout << "Rejected\n";
}
