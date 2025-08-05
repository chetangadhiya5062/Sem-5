def encrypt_rail_fence(text, key):
    rail = [['\n' for i in range(len(text))]
                  for j in range(key)]
     
    dir_down = False
    row, col = 0, 0
     
    for ch in text:
        if row == 0 or row == key - 1:
            dir_down = not dir_down
         
        rail[row][col] = ch
        col += 1
         
        row += 1 if dir_down else -1
     
    result = []
    for i in range(key):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)


def decrypt_rail_fence(cipher, key):
    rail = [['\n' for i in range(len(cipher))]
                  for j in range(key)]
     
    dir_down = None
    row, col = 0, 0
     
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key - 1:
            dir_down = False
         
        rail[row][col] = '*'
        col += 1
         
        row += 1 if dir_down else -1
     
    index = 0
    for i in range(key):
        for j in range(len(cipher)):
            if rail[i][j] == '*' and index < len(cipher):
                rail[i][j] = cipher[index]
                index += 1
     
 
    result = []
    row, col = 0, 0
    for i in range(len(cipher)):
        if row == 0:
            dir_down = True
        if row == key-1:
            dir_down = False
         
        if rail[row][col] != '\n':
            result.append(rail[row][col])
            col += 1
         
        row += 1 if dir_down else -1
    return "".join(result)


text = input("Enter the message: ").replace(" ", "")
key = int(input("Enter the number of rails (key): "))

cipher_text = encrypt_rail_fence(text, key)
print("\nEncrypted Text:", cipher_text)

decrypted_text = decrypt_rail_fence(cipher_text, key)
print("Decrypted Text:", decrypted_text)
