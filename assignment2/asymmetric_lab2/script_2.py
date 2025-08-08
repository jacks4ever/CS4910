# Create a CIA-themed decryption challenge
# Generate encrypted numbers from a motivational message
message = "NEVER GIVE UP"
clean_message = message.replace(" ", "")  # Remove spaces for simplicity

# Use our small RSA parameters
n = 77
e = 7
d = 43

# Encrypt each character
encrypted_message = []
for char in clean_message:
    ascii_val = ord(char)
    # For this small example, we need to handle large ASCII values
    # We'll use a simple mapping for letters: A=1, B=2, etc.
    if char.isalpha():
        char_num = ord(char.upper()) - ord('A') + 1  # A=1, B=2, ..., Z=26
        encrypted = pow(char_num, e, n)
        encrypted_message.append({
            'char': char,
            'plaintext': char_num,
            'ciphertext': encrypted
        })

print("CIA Decryption Challenge:")
print("Encrypted Message (each number represents one letter):")
ciphertext_numbers = [item['ciphertext'] for item in encrypted_message]
print(ciphertext_numbers)
print()

print("Decryption key information:")
print(f"n = {n}")
print(f"d = {d}")
print("Use the formula: plaintext = ciphertext^d mod n")
print()

print("Expected decryption (for verification):")
for item in encrypted_message:
    decrypted = pow(item['ciphertext'], d, n)
    print(f"Ciphertext {item['ciphertext']} -> {decrypted} -> '{item['char']}'")

print()
print("Letter-to-number mapping: A=1, B=2, C=3, ..., Z=26")
print(f"Original message: {message}")

# Verify our work
print("\nVerification:")
decrypted_chars = []
for cipher_num in ciphertext_numbers:
    plaintext_num = pow(cipher_num, d, n)
    if 1 <= plaintext_num <= 26:
        char = chr(plaintext_num - 1 + ord('A'))
        decrypted_chars.append(char)
    
decrypted_message = ''.join(decrypted_chars)
print(f"Decrypted message: {decrypted_message}")