import random
from datetime import datetime

def log_action(action, key, input_text, output_text):
    with open("cipher_history.log", "a") as log_file:
        log_file.write(f"{datetime.now()} | {action} | Key: {key} | Input: {input_text} | Output: {output_text}\n")

def encrypt_char(ch, key):
    if ch.islower():
        return chr((ord(ch) - ord('a') + key) % 26 + ord('a'))
    elif ch.isupper():
        return chr((ord(ch) - ord('A') + key) % 26 + ord('A'))
    else:
        return ch

def decrypt_char(ch, key):
    if ch.islower():
        return chr((ord(ch) - ord('a') - key) % 26 + ord('a'))
    elif ch.isupper():
        return chr((ord(ch) - ord('A') - key) % 26 + ord('A'))
    else:
        return ch

def encrypt_text(text, key):
    return ''.join(encrypt_char(ch, key) for ch in text)

def decrypt_text(text, key):
    return ''.join(decrypt_char(ch, key) for ch in text)

def selective_encrypt(text, key, words_to_encrypt):
    words = text.split()
    encrypted_words = []
    for word in words:
        if word in words_to_encrypt:
            encrypted_words.append(encrypt_text(word, key))
        else:
            encrypted_words.append(word)
    return ' '.join(encrypted_words)

def show_menu():
    print("\n----- Caesar Cipher Menu -----")
    print("1. Encrypt full text with manual key")
    print("2. Encrypt full text with random key")
    print("3. Encrypt only specific words (for selective encryption)")
    print("4. Decrypt text with known key")
    print("5. View log history")
    print("6. Exit")

while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == '1':
        plain_text = input("Enter the text to encrypt: ")
        key = int(input("Enter the key (1-25): "))
        cipher_text = encrypt_text(plain_text, key)
        log_action("Manual Encrypt", key, plain_text, cipher_text)
        print("Encrypted Text:", cipher_text)

    elif choice == '2':
        plain_text = input("Enter the text to encrypt: ")
        key = random.randint(1, 25)
        cipher_text = encrypt_text(plain_text, key)
        log_action("Random Encrypt", key, plain_text, cipher_text)
        print(f"Encrypted Text: {cipher_text} (Key: {key})")

    elif choice == '3':
        plain_text = input("Enter the full sentence: ")
        key = int(input("Enter the key (1-25): "))
        specific_words = input("Enter the words to encrypt (comma separated): ").split(',')
        specific_words = [w.strip() for w in specific_words]
        cipher_text = selective_encrypt(plain_text, key, specific_words)
        log_action("Selective Encrypt", key, plain_text, cipher_text)
        print("Encrypted Text:", cipher_text)

    elif choice == '4':
        cipher_text = input("Enter the text to decrypt: ")
        key = int(input("Enter the key used during encryption: "))
        decrypted_text = decrypt_text(cipher_text, key)
        log_action("Decrypt", key, cipher_text, decrypted_text)
        print("Decrypted Text:", decrypted_text)

    elif choice == '5':
        print("\n--- Cipher History Log ---")
        try:
            with open("cipher_history.log", "r") as log_file:
                print(log_file.read())
        except FileNotFoundError:
            print("No log history found.")

    elif choice == '6':
        print("Exited.")
        break

    else:
        print("Invalid choice. Please try again.")
