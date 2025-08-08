#!/usr/bin/env python3
"""
CS 4910 Lab 2: Password Security and Brute Force Analysis
Interactive script for analyzing password security and brute force resistance.

Author: CS 4910 Course Materials
Fall 2025 Semester
"""

import math
import random
import string
import time
import hashlib
from itertools import product

class PasswordSecurityAnalyzer:
    """Class for analyzing password security and brute force resistance."""
    
    def __init__(self):
        self.consonants = "bcdfghjklmnpqrstvwxyz"
        self.vowels = "aeiou"
        self.digits = "0123456789"
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
    def calculate_password_entropy(self, charset_size, length):
        """Calculate password entropy: H = log₂(N^L)"""
        total_combinations = charset_size ** length
        entropy = math.log2(total_combinations)
        return entropy, total_combinations
    
    def estimate_brute_force_time(self, total_combinations, attempts_per_second=1e9):
        """Estimate average brute force time."""
        # Average case: need to try half of all combinations
        avg_attempts = total_combinations / 2
        avg_time_seconds = avg_attempts / attempts_per_second
        return avg_time_seconds
    
    def format_time(self, seconds):
        """Format time in human-readable format."""
        if seconds < 1:
            return f"{seconds*1000:.2f} milliseconds"
        elif seconds < 60:
            return f"{seconds:.2f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.2f} minutes"
        elif seconds < 86400:
            return f"{seconds/3600:.2f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.2f} days"
        else:
            return f"{seconds/31536000:.2f} years"
    
    def traditional_password_analysis(self):
        """Analyze traditional 8-character mixed passwords."""
        print("=" * 60)
        print("TRADITIONAL PASSWORD ANALYSIS")
        print("=" * 60)
        
        # Character set analysis
        charset_sizes = {
            "Lowercase only": len(self.lowercase),
            "Lowercase + Uppercase": len(self.lowercase) + len(self.uppercase),
            "Alphanumeric": len(self.lowercase) + len(self.uppercase) + len(self.digits),
            "Full ASCII": len(self.lowercase) + len(self.uppercase) + len(self.digits) + len(self.symbols)
        }
        
        password_length = 8
        
        print(f"Password length: {password_length} characters")
        print(f"Assumed attack rate: 1 billion attempts/second")
        print()
        
        for charset_name, charset_size in charset_sizes.items():
            entropy, total_combinations = self.calculate_password_entropy(charset_size, password_length)
            avg_time = self.estimate_brute_force_time(total_combinations)
            
            print(f"{charset_name}:")
            print(f"  Character set size: {charset_size}")
            print(f"  Total combinations: {total_combinations:,}")
            print(f"  Entropy: {entropy:.2f} bits")
            print(f"  Average brute force time: {self.format_time(avg_time)}")
            print()
        
        return charset_sizes
    
    def cvcn_password_analysis(self):
        """Analyze CVCN (Consonant-Vowel-Consonant-Number) password generation."""
        print("=" * 60)
        print("CVCN PASSWORD ANALYSIS")
        print("=" * 60)
        
        # CVCN segment analysis
        consonant_count = len(self.consonants)
        vowel_count = len(self.vowels)
        digit_count = len(self.digits)
        
        print(f"CVCN Format Analysis:")
        print(f"Consonants available: {consonant_count} ({self.consonants})")
        print(f"Vowels available: {vowel_count} ({self.vowels})")
        print(f"Digits available: {digit_count} ({self.digits})")
        print()
        
        # Single CVCN segment
        single_segment_combinations = consonant_count * vowel_count * consonant_count * digit_count
        single_segment_entropy = math.log2(single_segment_combinations)
        
        print(f"Single CVCN segment:")
        print(f"  Combinations: {consonant_count} × {vowel_count} × {consonant_count} × {digit_count} = {single_segment_combinations:,}")
        print(f"  Entropy: {single_segment_entropy:.2f} bits")
        print()
        
        # Two CVCN segments (8 characters total)
        two_segment_combinations = single_segment_combinations ** 2
        two_segment_entropy = 2 * single_segment_entropy
        avg_time = self.estimate_brute_force_time(two_segment_combinations)
        
        print(f"Two CVCN segments (8 characters):")
        print(f"  Total combinations: {two_segment_combinations:,}")
        print(f"  Entropy: {two_segment_entropy:.2f} bits")
        print(f"  Average brute force time: {self.format_time(avg_time)}")
        print()
        
        # Generate sample CVCN passwords
        print("Sample CVCN passwords:")
        for i in range(5):
            password = self.generate_cvcn_password()
            print(f"  {password}")
        
        return {
            'single_segment_combinations': single_segment_combinations,
            'two_segment_combinations': two_segment_combinations,
            'entropy': two_segment_entropy
        }
    
    def generate_cvcn_password(self):
        """Generate a random CVCN password (two segments)."""
        password = ""
        for _ in range(2):  # Two segments
            password += random.choice(self.consonants)  # C
            password += random.choice(self.vowels)      # V
            password += random.choice(self.consonants)  # C
            password += random.choice(self.digits)      # N
        return password
    
    def compare_password_methods(self):
        """Compare different password generation methods."""
        print("=" * 60)
        print("PASSWORD METHOD COMPARISON")
        print("=" * 60)
        
        # Traditional 8-character alphanumeric
        traditional_charset = len(self.lowercase) + len(self.uppercase) + len(self.digits)
        traditional_entropy, traditional_combinations = self.calculate_password_entropy(traditional_charset, 8)
        traditional_time = self.estimate_brute_force_time(traditional_combinations)
        
        # CVCN method
        cvcn_results = self.cvcn_password_analysis()
        cvcn_entropy = cvcn_results['entropy']
        cvcn_combinations = cvcn_results['two_segment_combinations']
        cvcn_time = self.estimate_brute_force_time(cvcn_combinations)
        
        print(f"Comparison Summary:")
        print(f"{'Method':<20} {'Entropy (bits)':<15} {'Combinations':<15} {'Brute Force Time'}")
        print("-" * 80)
        print(f"{'Traditional':<20} {traditional_entropy:<15.2f} {traditional_combinations:<15,} {self.format_time(traditional_time)}")
        print(f"{'CVCN':<20} {cvcn_entropy:<15.2f} {cvcn_combinations:<15,} {self.format_time(cvcn_time)}")
        print()
        
        if traditional_entropy > cvcn_entropy:
            print("Traditional method provides higher entropy and better security.")
            security_ratio = traditional_combinations / cvcn_combinations
            print(f"Traditional is {security_ratio:.1f}x more secure than CVCN.")
        else:
            print("CVCN method provides higher entropy and better security.")
            security_ratio = cvcn_combinations / traditional_combinations
            print(f"CVCN is {security_ratio:.1f}x more secure than traditional.")
        
        print("\nTrade-offs:")
        print("Traditional method:")
        print("  + Higher entropy")
        print("  - Harder to remember")
        print("  - More prone to user errors")
        
        print("CVCN method:")
        print("  + Easier to remember (pronounceable)")
        print("  + Less prone to typing errors")
        print("  - Lower entropy")
        print("  - Predictable structure")
    
    def brute_force_simulation(self):
        """Simulate a brute force attack on short passwords."""
        print("=" * 60)
        print("BRUTE FORCE ATTACK SIMULATION")
        print("=" * 60)
        
        # Create a target password
        target_password = "abc1"  # Simple 4-character password
        target_hash = hashlib.sha256(target_password.encode()).hexdigest()
        
        print(f"Target password: {target_password}")
        print(f"Target hash (SHA-256): {target_hash[:32]}...")
        print()
        
        # Character set for brute force
        charset = self.lowercase + self.digits
        password_length = len(target_password)
        
        print(f"Brute force parameters:")
        print(f"Character set: {charset}")
        print(f"Character set size: {len(charset)}")
        print(f"Password length: {password_length}")
        print(f"Total combinations: {len(charset)**password_length:,}")
        print()
        
        # Simulate brute force attack
        print("Starting brute force attack simulation...")
        start_time = time.time()
        attempts = 0
        
        # Generate all possible combinations
        for combination in product(charset, repeat=password_length):
            attempts += 1
            candidate = ''.join(combination)
            candidate_hash = hashlib.sha256(candidate.encode()).hexdigest()
            
            if candidate_hash == target_hash:
                end_time = time.time()
                elapsed_time = end_time - start_time
                
                print(f"PASSWORD FOUND: {candidate}")
                print(f"Attempts: {attempts:,}")
                print(f"Time elapsed: {elapsed_time:.4f} seconds")
                print(f"Rate: {attempts/elapsed_time:,.0f} attempts/second")
                break
            
            # Show progress every 1000 attempts
            if attempts % 1000 == 0:
                print(f"Attempts: {attempts:,}, Current: {candidate}")
        
        return attempts, elapsed_time
    
    def advanced_attack_analysis(self):
        """Analyze advanced attack scenarios."""
        print("=" * 60)
        print("ADVANCED ATTACK ANALYSIS")
        print("=" * 60)
        
        print("1. DICTIONARY ATTACKS:")
        print("   - Use common passwords and variations")
        print("   - Much faster than brute force for weak passwords")
        print("   - Effectiveness depends on password predictability")
        print()
        
        print("2. HYBRID ATTACKS:")
        print("   - Combine dictionary words with numbers/symbols")
        print("   - Target common password patterns")
        print("   - Example: 'password123', 'admin!@#'")
        print()
        
        print("3. RAINBOW TABLE ATTACKS:")
        print("   - Pre-computed hash tables")
        print("   - Trade space for time")
        print("   - Defeated by salting")
        print()
        
        print("4. DISTRIBUTED ATTACKS:")
        print("   - Use multiple computers/GPUs")
        print("   - Can increase attack rate by orders of magnitude")
        print("   - Cloud computing makes this accessible")
        print()
        
        print("5. SPECIALIZED HARDWARE:")
        print("   - ASIC miners for specific hash functions")
        print("   - GPU clusters for parallel processing")
        print("   - Can achieve billions of attempts per second")
        print()
        
        # Calculate impact of increased computational power
        base_rate = 1e9  # 1 billion attempts/second
        gpu_rate = 1e11  # 100 billion attempts/second
        asic_rate = 1e12  # 1 trillion attempts/second
        
        password_combinations = 62**8  # 8-char alphanumeric
        
        print("Attack time comparison for 8-character alphanumeric password:")
        print(f"CPU (1B/sec):  {self.format_time(password_combinations/(2*base_rate))}")
        print(f"GPU (100B/sec): {self.format_time(password_combinations/(2*gpu_rate))}")
        print(f"ASIC (1T/sec): {self.format_time(password_combinations/(2*asic_rate))}")
    
    def interactive_analysis(self):
        """Interactive password security analysis tool."""
        print("\n" + "=" * 60)
        print("INTERACTIVE PASSWORD ANALYSIS")
        print("=" * 60)
        
        while True:
            print("\nOptions:")
            print("1. Analyze custom password parameters")
            print("2. Compare password generation methods")
            print("3. Run brute force simulation")
            print("4. Advanced attack analysis")
            print("5. Generate secure passwords")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.custom_password_analysis()
            elif choice == '2':
                self.compare_password_methods()
            elif choice == '3':
                self.brute_force_simulation()
            elif choice == '4':
                self.advanced_attack_analysis()
            elif choice == '5':
                self.generate_secure_passwords()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def custom_password_analysis(self):
        """Analyze custom password parameters."""
        print("\nCustom Password Analysis")
        print("-" * 25)
        
        try:
            charset_size = int(input("Character set size: "))
            length = int(input("Password length: "))
            
            entropy, combinations = self.calculate_password_entropy(charset_size, length)
            avg_time = self.estimate_brute_force_time(combinations)
            
            print(f"\nResults:")
            print(f"Total combinations: {combinations:,}")
            print(f"Entropy: {entropy:.2f} bits")
            print(f"Average brute force time: {self.format_time(avg_time)}")
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    def generate_secure_passwords(self):
        """Generate secure passwords using different methods."""
        print("\nSecure Password Generator")
        print("-" * 25)
        
        print("1. Traditional random password:")
        charset = self.lowercase + self.uppercase + self.digits + self.symbols
        traditional = ''.join(random.choice(charset) for _ in range(12))
        print(f"   {traditional}")
        
        print("2. CVCN-based password:")
        cvcn = self.generate_cvcn_password() + self.generate_cvcn_password()[:4]
        print(f"   {cvcn}")
        
        print("3. Passphrase (4 random words):")
        words = ["apple", "bridge", "castle", "dragon", "eagle", "forest", "guitar", "harbor"]
        passphrase = '-'.join(random.choice(words) for _ in range(4))
        print(f"   {passphrase}")
        
        # Analyze each method
        print("\nSecurity analysis:")
        trad_entropy, _ = self.calculate_password_entropy(len(charset), 12)
        cvcn_entropy = math.log2((len(self.consonants) * len(self.vowels) * len(self.consonants) * len(self.digits))**3)
        phrase_entropy = math.log2(len(words)**4)
        
        print(f"Traditional (12 chars): {trad_entropy:.1f} bits")
        print(f"CVCN (12 chars): {cvcn_entropy:.1f} bits")
        print(f"Passphrase (4 words): {phrase_entropy:.1f} bits")

def main():
    """Main function to run the password security analysis."""
    print("CS 4910 Lab 2: Password Security Analysis")
    print("=" * 42)
    
    analyzer = PasswordSecurityAnalyzer()
    
    # Run main analyses
    analyzer.traditional_password_analysis()
    analyzer.cvcn_password_analysis()
    analyzer.compare_password_methods()
    
    # Interactive analysis
    analyzer.interactive_analysis()
    
    print("\nPassword security analysis complete!")

if __name__ == "__main__":
    main()