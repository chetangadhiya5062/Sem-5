import math

def encrypt_columnar(message, key):
    message = message.replace(" ", "").upper()
    key_len = len(key)
    rows = math.ceil(len(message) / key_len)
    padded = message.ljust(rows * key_len, 'X')
    matrix = [list(padded[i:i+key_len]) for i in range(0, len(padded), key_len)]
    print("Matrix:")
    for row in matrix:
        print(row)
    order = sorted(list(enumerate(key)), key=lambda x: x[1])
    ciphertext = ''
    for idx, _ in order:
        for r in matrix:
            ciphertext += r[idx]
    return ciphertext

msg = input("Enter message: ")
key = input("Enter key: ")
cipher = encrypt_columnar(msg, key)
print("Ciphertext:", cipher)
