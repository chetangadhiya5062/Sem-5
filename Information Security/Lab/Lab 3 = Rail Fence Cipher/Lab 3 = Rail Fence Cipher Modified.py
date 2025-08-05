def encrypt_rail_fence_unicode(text, key):
    # Create a matrix to cipher the plain text
    rail = [['\n' for _ in range(len(text))] for _ in range(key)]
    
    # Fill the rail matrix in a zig-zag manner
    dir_down = False
    row, col = 0, 0

    for char in text:
        if row == 0 or row == key - 1:
            dir_down = not dir_down

        rail[row][col] = char
        col += 1

        row += 1 if dir_down else -1

    # Construct the cipher by reading the matrix row-wise
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return ''.join(result)


def decrypt_rail_fence_unicode(cipher, key):
    # Create the empty rail matrix
    rail = [['\n' for _ in range(len(cipher))] for _ in range(key)]
    
    # Mark the places with '*'
    dir_down = None
    row, col = 0, 0
    for _ in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        rail[row][col] = '*'
        col += 1
        row += 1 if dir_down else -1

    # Fill the rail matrix with cipher characters
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1

    # Read the matrix in zig-zag to reconstruct the message
    result = []
    row, col = 0, 0
    for _ in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False

        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1

        row += 1 if dir_down else -1

    return ''.join(result)


# ---- 📥 User Input Section ----
message = input("🔤 Enter message to encrypt (any language or emoji supported): ")
rails = int(input("🔢 Enter number of rails: "))

encrypted = encrypt_rail_fence_unicode(message, rails)
print("\n🔐 Encrypted:", encrypted)

decrypted = decrypt_rail_fence_unicode(encrypted, rails)
print("🔓 Decrypted:", decrypted)
