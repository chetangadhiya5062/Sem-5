def generate_matrix(key):
    key = key.upper().replace('J', 'I')
    matrix = []
    used = set()

    for char in key:
        if char not in used and char.isalpha():
            used.add(char)
            matrix.append(char)

    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in used:
            used.add(char)
            matrix.append(char)

    return [matrix[i*5:(i+1)*5] for i in range(5)]

def print_matrix(matrix):
    print("\nGenerated 5x5 Playfair Matrix:")
    for row in matrix:
        print(" ".join(row))
    print()

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return i, j
    return None

def process_text(text):
    text = text.upper().replace('J', 'I')
    text = ''.join(filter(str.isalpha, text))
    result = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i + 1 < len(text) else 'X'
        if a == b:
            result += a + 'X'
            i += 1
        else:
            result += a + b
            i += 2
    if len(result) % 2 != 0:
        result += 'X'
    return result

def encrypt_pair(a, b, matrix):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2:
        return matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
    elif c1 == c2:
        return matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt_pair(a, b, matrix):
    r1, c1 = find_position(matrix, a)
    r2, c2 = find_position(matrix, b)

    if r1 == r2:
        return matrix[r1][(c1-1)%5] + matrix[r2][(c2-1)%5]
    elif c1 == c2:
        return matrix[(r1-1)%5][c1] + matrix[(r2-1)%5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def playfair_encrypt(plaintext, key):
    matrix = generate_matrix(key)
    print_matrix(matrix) 
    text = process_text(plaintext)
    encrypted = ''
    for i in range(0, len(text), 2):
        encrypted += encrypt_pair(text[i], text[i+1], matrix)
    return encrypted

def playfair_decrypt(ciphertext, key):
    matrix = generate_matrix(key)
    print_matrix(matrix)  
    decrypted = ''
    for i in range(0, len(ciphertext), 2):
        decrypted += decrypt_pair(ciphertext[i], ciphertext[i+1], matrix)
    return decrypted


choice = input("Enter E to Encrypt or D to Decrypt: ").strip().upper()
key = input("Enter the key: ").strip()
message = input("Enter the message: ").strip()

if choice == 'E':
    encrypted = playfair_encrypt(message, key)
    print("Encrypted message:", encrypted)
elif choice == 'D':
    decrypted = playfair_decrypt(message, key)
    print("Decrypted message:", decrypted)
else:
    print("Invalid choice.")
    
    # I am don
