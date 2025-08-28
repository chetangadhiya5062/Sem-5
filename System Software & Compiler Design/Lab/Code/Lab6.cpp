#include <bits/stdc++.h>
using namespace std;



map<string,map<string,char>> table = {
    {"id", { {"+", '>'}, {"*", '>'}, {")", '>'}, {"#", '>'} }},
    {"+",  { {"id", '<'}, {"+", '>'}, {"*", '<'}, {"(", '<'}, {")", '>'}, {"#", '>'} }},
    {"*",  { {"id", '<'}, {"+", '>'}, {"*", '>'}, {"(", '<'}, {")", '>'}, {"#", '>'} }},
    {"(",  { {"id", '<'}, {"+", '<'}, {"*", '<'}, {"(", '<'}, {")", '='} }},
    {")",  { {"+", '>'}, {"*", '>'}, {")", '>'}, {"#", '>'} }},
    {"#",  { {"id", '<'}, {"+", '<'}, {"*", '<'}, {"(", '<'}, {"#", '='} }}
};

bool parse(vector<string> input);
    stack<string> st;
    st.push("#");
    int i=0;
    while (i < input.size()) {
        string a = input[i];
        string top = st.top();


    return false;g
    }

int main() {
    cout << "Enter input string (tokens separated by space, end with #):\n";
    string line; getline(cin, line);
    if(line.empty()) getline(cin,line);

    stringstream ss(line);
    vector<string> input;
    string tok;
    while (ss >> tok) input.push_back(tok);

    if (parse(input)) cout << "Valid string\n";
    else cout << "Invalid string\n";
}
