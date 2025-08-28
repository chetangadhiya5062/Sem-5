import math
from datetime import datetime

def create_matrix(message, key_len):
    rows = math.ceil(len(message) / key_len)
    matrix = [['' for _ in range(key_len)] for _ in range(rows)]
    idx = 0
    for i in range(rows):
        for j in range(key_len):
            if idx < len(message):
                matrix[i][j] = message[idx]
                idx += 1
    return matrix

def transpose(matrix):
    return list(map(list, zip(*matrix)))

message = input("Enter the message: ")
base_key = input("Enter the base key (e.g. numbers or letters): ")

now = datetime.now()
seconds = now.second
rotation = seconds % len(base_key)
rotated_key = base_key[rotation:] + base_key[:rotation]

print("Current Time:", now.strftime("%H:%M:%S"))
print("Seconds:", seconds)
print("Rotation Value:", rotation)
print("Rotated Key:", rotated_key)

matrix = create_matrix(message, len(rotated_key))
print("Matrix:")
for row in matrix:
    print(row)

transposed = transpose(matrix)
print("Transposed Matrix:")
for row in transposed:
    print(row)

final = ''.join([''.join(row) for row in transposed])
print("Final Cipher Text:", final)
