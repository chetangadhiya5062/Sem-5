def create_matrix(message, key):
    message = message.replace(" ", "").upper()
    num_cols = len(key)
    num_rows = -(-len(message) // num_cols)
    matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    idx = 0
    for r in range(num_rows):
        for c in range(num_cols):
            if idx < len(message):
                matrix[r][c] = message[idx]
                idx += 1
    return matrix

def print_matrix(matrix, title):
    print("\n" + title)
    for row in matrix:
        print(" ".join(ch if ch else "_" for ch in row))

def columnar_encrypt(message, key):
    matrix = create_matrix(message, key)
    print_matrix(matrix, "Original Matrix (Message filled row-wise):")
    order = sorted(range(len(key)), key=lambda x: key[x])
    transposed = []
    for r in range(len(matrix)):
        transposed.append([matrix[r][c] for c in order])
    print_matrix(transposed, "Matrix after Column Transposition:")
    ciphertext = ""
    for c in range(len(key)):
        for r in range(len(matrix)):
            if transposed[r][c] != '':
                ciphertext += transposed[r][c]
    print("\nFinal Ciphertext:", ciphertext)
    return ciphertext


def columnar_decrypt(ciphertext, key):
    num_cols = len(key)
    num_rows = -(-len(ciphertext) // num_cols)
    order = sorted(range(len(key)), key=lambda x: key[x])
    col_lengths = [num_rows] * num_cols
    extra = num_cols * num_rows - len(ciphertext)
    for i in range(extra):
        col_lengths[order[-(i+1)]] -= 1
    matrix = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    idx = 0
    for c in range(num_cols):
        for r in range(col_lengths[c]):
            matrix[r][c] = ciphertext[idx]
            idx += 1
    print_matrix(matrix, "Cipher Matrix (filled column-wise):")
    reordered = []
    for r in range(num_rows):
        row = [''] * num_cols
        for i, c in enumerate(order):
            row[c] = matrix[r][i]
        reordered.append(row)
    print_matrix(reordered, "Matrix after Reordering to Original:")
    plaintext = ""
    for r in reordered:
        for c in r:
            if c != '':
                plaintext += c
    print("\nFinal Decrypted Message:", plaintext)
    return plaintext

message = input("Enter message: ")
key = input("Enter numeric key (e.g., 4312567): ")

print("\n--- Encryption Process ---")
cipher = columnar_encrypt(message, key)

print("\n--- Decryption Process ---")
plain = columnar_decrypt(cipher, key)
