# Let's create some RSA examples with small numbers for educational purposes
import math
import random

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(e, phi):
    gcd_val, x, y = extended_gcd(e, phi)
    if gcd_val != 1:
        raise ValueError("Modular inverse does not exist")
    return (x % phi + phi) % phi

def generate_small_rsa_example():
    # Use small primes for educational purposes
    p = 7
    q = 11
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Choose e
    e = 3
    while gcd(e, phi_n) != 1:
        e += 2
    
    # Calculate d
    d = mod_inverse(e, phi_n)
    
    return {
        'p': p, 'q': q, 'n': n, 'phi_n': phi_n,
        'e': e, 'd': d,
        'public_key': (e, n),
        'private_key': (d, n)
    }

# Generate example
rsa_example = generate_small_rsa_example()
print("Small RSA Example for Educational Lab:")
print(f"p = {rsa_example['p']}")
print(f"q = {rsa_example['q']}")
print(f"n = p × q = {rsa_example['n']}")
print(f"φ(n) = (p-1)(q-1) = {rsa_example['phi_n']}")
print(f"e = {rsa_example['e']} (public exponent)")
print(f"d = {rsa_example['d']} (private exponent)")
print(f"Public Key: (e={rsa_example['e']}, n={rsa_example['n']})")
print(f"Private Key: (d={rsa_example['d']}, n={rsa_example['n']})")

# Test encryption/decryption
message = 5
encrypted = pow(message, rsa_example['e'], rsa_example['n'])
decrypted = pow(encrypted, rsa_example['d'], rsa_example['n'])
print(f"\nTest: Message = {message}")
print(f"Encrypted = {message}^{rsa_example['e']} mod {rsa_example['n']} = {encrypted}")
print(f"Decrypted = {encrypted}^{rsa_example['d']} mod {rsa_example['n']} = {decrypted}")