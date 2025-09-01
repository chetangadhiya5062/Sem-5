#include <bits/stdc++.h>
using namespace std;

// Grammar:
// E -> T X
// X -> + T X | ε
// T -> F Y
// Y -> * F Y | ε
// F -> (E) | i

map<pair<char,char>, string> table;

void initTable() {
    table[{'E','i'}] = "TX";
    table[{'E','('}] = "TX";

    table[{'X','+'}] = "+TX";
    table[{'X',')'}] = "#";
    table[{'X','$'}] = "#";

    table[{'T','i'}] = "FY";
    table[{'T','('}] = "FY";

    table[{'Y','*'}] = "*FY";
    table[{'Y','+'}] = "#";
    table[{'Y',')'}] = "#";
    table[{'Y','$'}] = "#";

    table[{'F','i'}] = "i";
    table[{'F','('}] = "(E)";
}

int main() {
    initTable();
    string input; 
    cin >> input;
    input += "$";

    stack<char> st;
    st.push('$');
    st.push('E');

    int i = 0;
    while(!st.empty()) {
        char top = st.top();
        char cur = input[i];

        if(top == cur) {
            st.pop(); i++;
        }
        else if(isupper(top)) {
            string prod = table[{top,cur}];
            st.pop();
            if(prod != "#" && prod != "") {
                for(int j = prod.size()-1; j>=0; j--)
                    st.push(prod[j]);
            }
            else if(prod=="") {
                cout << "Error\n";
                return 0;
            }
        }
        else {
            cout << "Error\n";
            return 0;
        }
    }
    if(i == (int)input.size()) cout << "Accepted\n";
    else cout << "Rejected\n";
}
