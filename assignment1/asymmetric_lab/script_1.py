# Create practice problems for modular arithmetic
practice_problems = []

# Problem 1: Modular multiplication
prob1 = {
    'problem': 'Calculate: 23 × 19 mod 13',
    'solution': (23 * 19) % 13,
    'work': '23 × 19 = 437, 437 mod 13 = 7'
}
practice_problems.append(prob1)

# Problem 2: GCD using Euclidean algorithm
def euclidean_gcd_steps(a, b):
    steps = []
    while b != 0:
        q = a // b
        r = a % b
        steps.append(f"{a} = {b} × {q} + {r}")
        a, b = b, r
    return steps, a

steps, gcd_result = euclidean_gcd_steps(48, 18)
prob2 = {
    'problem': 'Find GCD(48, 18) using Euclidean algorithm',
    'solution': gcd_result,
    'work': '\n'.join(steps)
}
practice_problems.append(prob2)

# Problem 3: Modular inverse
prob3 = {
    'problem': 'Find the modular inverse of 7 mod 26',
    'solution': mod_inverse(7, 26),
    'work': 'Use extended Euclidean algorithm: 7 × 15 ≡ 1 mod 26'
}
practice_problems.append(prob3)

# Problem 4: Modular exponentiation
prob4 = {
    'problem': 'Calculate: 3^5 mod 7',
    'solution': pow(3, 5, 7),
    'work': '3^5 = 243, 243 mod 7 = 5'
}
practice_problems.append(prob4)

# Problem 5: More complex modular arithmetic
prob5 = {
    'problem': 'Calculate: (15 + 28) × 7 mod 11',
    'solution': ((15 + 28) * 7) % 11,
    'work': '15 + 28 = 43, 43 × 7 = 301, 301 mod 11 = 4'
}
practice_problems.append(prob5)

for i, prob in enumerate(practice_problems, 1):
    print(f"Problem {i}: {prob['problem']}")
    print(f"Answer: {prob['solution']}")
    print(f"Working: {prob['work']}")
    print()

# Create ASCII conversion example
print("ASCII Conversion Examples:")
message = "HI"
ascii_values = [ord(c) for c in message]
print(f"Message '{message}' -> ASCII: {ascii_values}")

# Show encryption of each character with small RSA
for i, char in enumerate(message):
    ascii_val = ord(char)
    if ascii_val < rsa_example['n']:  # Make sure it's smaller than modulus
        encrypted = pow(ascii_val, rsa_example['e'], rsa_example['n'])
        print(f"'{char}' (ASCII {ascii_val}) -> Encrypted: {encrypted}")
    else:
        print(f"'{char}' (ASCII {ascii_val}) -> Too large for this example modulus")