# Encryption
# make a program that converts the plain text into cipher text using key.
# indexing by default starts from 0

def encryptCipher(plainText, key) : 
    cipher = ""
    
    for ch in plainText:
        if ch.isalpha():
            # ch.lower() - 97 is getting Real Char., 97 is for small a.
            # ch.lower() - 97 + key is for encrypted char.
            # (ord(ch.lower() - 97 + key) % 26 is for choosing the right encryption char.
            # (ord(ch.lower() - 97 + key) % 26 + 97  is for 
            # converting to right ASCII after encryption.
            encrypted = chr(((ord(ch.lower()) - 97 + int(key)) % 26) + 97)
            cipher += encrypted
        
        else : # to deal with special char and nums.
            cipher += ch
        
    return cipher
    

plainText = input("Enter the plain Text here : ")
key = input("Enter the integer key Value here : ")
cipherText = encryptCipher(plainText, key)
print("Cipher Text:", cipherText)


