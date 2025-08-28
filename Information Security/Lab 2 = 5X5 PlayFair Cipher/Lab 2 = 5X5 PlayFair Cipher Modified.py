def generate_matrix(key):
    matrix = []
    seen = set()
    key = key.replace("J", "I").upper()
    for char in key:
        if char.isalpha() and char not in seen:
            seen.add(char)
            matrix.append(char)

    for i in range(65, 91):
        char = chr(i)
        if char == 'J':
            continue
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    final_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]

    print("\nGenerated 5x5 Playfair Matrix:")
    for row in final_matrix:
        print(" ".join(row))

    return final_matrix

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j
    return None, None

def prepare_text(text):
    text = text.upper().replace("J", "I").replace(" ", "")
    i = 0
    prepared = ""
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            prepared += a + 'X'
            i += 1
        else:
            prepared += a + b
            i += 2
    if len(prepared) % 2 != 0:
        prepared += 'X'
    return prepared

def encrypt_pair(a, b, matrix):
    row1, col1 = find_position(matrix, a)
    row2, col2 = find_position(matrix, b)

    if row1 == row2:
        return matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
    elif col1 == col2:
        return matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
    else:
        return matrix[row1][col2] + matrix[row2][col1]

def decrypt_pair(a, b, matrix):
    return encrypt_pair(a, b, matrix)

def encrypt(text, matrix):
    text = prepare_text(text)
    cipher = ""
    for i in range(0, len(text), 2):
        cipher += encrypt_pair(text[i], text[i+1], matrix)
    return cipher

def decrypt(cipher, matrix):
    plain = ""
    for i in range(0, len(cipher), 2):
        plain += decrypt_pair(cipher[i], cipher[i+1], matrix)
    return plain

key = input("Enter key: ")
text = input("Enter plaintext: ")

matrix = generate_matrix(key)  

cipher_text = encrypt(text, matrix)
print("\nEncrypted Text:", cipher_text)

plain_text = decrypt(cipher_text, matrix)
print("Decrypted Text:", plain_text)
