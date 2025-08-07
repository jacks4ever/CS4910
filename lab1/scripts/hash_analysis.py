#!/usr/bin/env python3
# hash_analysis.py - Interactive Hash Function Analysis Tool

import hashlib
import random
import string
import time
import json
from datetime import datetime
from collections import defaultdict

class InteractiveHashAnalyzer:
    def __init__(self):
        self.algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        self.results = {}
    
    def hash_string(self, data, algorithm='sha256'):
        """Hash a string using specified algorithm"""
        hasher = hashlib.new(algorithm)
        hasher.update(data.encode('utf-8'))
        return hasher.hexdigest()
    
    def get_user_string(self, prompt="Enter a string to hash: "):
        """Get string input from user"""
        user_input = input(prompt).strip()
        while not user_input:
            print("Please enter a non-empty string.")
            user_input = input(prompt).strip()
        return user_input
    
    def demonstrate_avalanche_effect_interactive(self):
        """Interactively demonstrate avalanche effect"""
        print("\n" + "=" * 60)
        print("AVALANCHE EFFECT DEMONSTRATION")
        print("=" * 60)
        print("The avalanche effect shows how small input changes cause large output changes.")
        print("You'll provide a base string, then see how minor modifications affect the hash.")
        
        base_string = self.get_user_string("Enter your base string: ")
        
        print(f"\nBase string: '{base_string}'")
        base_hash = self.hash_string(base_string)
        print(f"SHA256 Hash: {base_hash}")
        
        # Interactive modifications
        print("\nNow we'll make small modifications and see the effect:")
        modifications = []
        
        # Predefined modifications
        auto_mods = [
            (base_string + "!", "Added '!' at the end"),
            (base_string.replace(base_string[0], base_string[0].swapcase()) if base_string else base_string + "X", "Changed case of first character"),
            (base_string.replace(" ", "_") if " " in base_string else base_string.replace(base_string[0], "_") if base_string else "_" + base_string, "Replaced character"),
            (base_string[:-1] if len(base_string) > 1 else base_string + "X", "Removed last character")
        ]
        
        # Ask user if they want to add custom modifications
        print("\nWould you like to add your own modifications? (y/n)")
        if input().strip().lower() in ['y', 'yes']:
            while True:
                custom_mod = input("Enter a modified version of your string (or 'done' to finish): ").strip()
                if custom_mod.lower() == 'done':
                    break
                if custom_mod:
                    modifications.append((custom_mod, "User-defined modification"))
        
        # Add automatic modifications
        modifications.extend(auto_mods)
        
        avalanche_results = []
        
        for i, (modified, description) in enumerate(modifications):
            mod_hash = self.hash_string(modified)
            print(f"\n--- Modification {i+1}: {description} ---")
            print(f"Modified string: '{modified}'")
            print(f"SHA256 Hash: {mod_hash}")
            
            # Calculate bit differences
            try:
                diff_bits = bin(int(base_hash, 16) ^ int(mod_hash, 16)).count('1')
                total_bits = len(base_hash) * 4  # Each hex digit = 4 bits
                diff_percentage = (diff_bits / total_bits) * 100
                
                print(f"Bit differences: {diff_bits}/{total_bits} ({diff_percentage:.1f}%)")
                
                avalanche_results.append({
                    'modification': description,
                    'original': base_string,
                    'modified': modified,
                    'bit_differences': diff_bits,
                    'total_bits': total_bits,
                    'difference_percentage': diff_percentage
                })
            except ValueError:
                print("Error calculating bit differences")
        
        self.results['avalanche_effect'] = {
            'base_string': base_string,
            'base_hash': base_hash,
            'modifications': avalanche_results
        }
        
        # Summary
        if avalanche_results:
            avg_diff = sum(r['difference_percentage'] for r in avalanche_results) / len(avalanche_results)
            print(f"\n--- Avalanche Effect Summary ---")
            print(f"Average bit difference: {avg_diff:.1f}%")
            print("Good avalanche effect should show ~50% bit differences for small changes.")
    
    def birthday_attack_simulation_interactive(self):
        """Interactive birthday attack simulation"""
        print("\n" + "=" * 60)
        print("BIRTHDAY ATTACK SIMULATION")
        print("=" * 60)
        print("This simulates finding hash collisions using the birthday paradox.")
        print("We'll use truncated hashes to make collisions findable in reasonable time.")
        
        # Get hash bit length from user
        print("\nChoose hash bit length for simulation:")
        print("12 bits: Very fast (~16 attempts expected)")
        print("16 bits: Fast (~256 attempts expected)")
        print("20 bits: Moderate (~1024 attempts expected)")
        print("24 bits: Slow (~4096 attempts expected)")
        
        while True:
            try:
                hash_bits = int(input("Enter bit length (12, 16, 20, or 24): "))
                if hash_bits in [12, 16, 20, 24]:
                    break
                else:
                    print("Please choose 12, 16, 20, or 24 bits.")
            except ValueError:
                print("Please enter a valid number.")
        
        print(f"\nStarting birthday attack simulation with {hash_bits}-bit hashes...")
        print("This may take a moment...")
        
        hash_map = {}
        attempts = 0
        max_attempts = 2 ** (hash_bits + 2)  # Reasonable upper limit
        
        start_time = time.time()
        
        while attempts < max_attempts:
            # Generate random string
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            # Get truncated hash
            full_hash = self.hash_string(random_string)
            hex_digits = hash_bits // 4
            truncated_hash = full_hash[:hex_digits]
            
            if truncated_hash in hash_map:
                end_time = time.time()
                print(f"\n🎉 COLLISION FOUND! 🎉")
                print(f"Attempts needed: {attempts}")
                print(f"String 1: '{hash_map[truncated_hash]}'")
                print(f"String 2: '{random_string}'")
                print(f"Matching hash ({hash_bits} bits): {truncated_hash}")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                
                # Theoretical vs actual
                theoretical = 2 ** (hash_bits / 2)
                print(f"\nTheoretical attempts expected: ~{theoretical:.0f}")
                print(f"Actual attempts needed: {attempts}")
                efficiency = (theoretical / attempts) * 100 if attempts > 0 else 0
                print(f"Efficiency: {efficiency:.1f}% of theoretical")
                
                self.results['birthday_attack'] = {
                    'hash_bits': hash_bits,
                    'attempts': attempts,
                    'theoretical_attempts': theoretical,
                    'time_taken': end_time - start_time,
                    'collision_strings': [hash_map[truncated_hash], random_string],
                    'collision_hash': truncated_hash
                }
                
                return attempts
            
            hash_map[truncated_hash] = random_string
            attempts += 1
            
            # Progress indicator
            if attempts % 500 == 0:
                print(f"Attempts: {attempts}...")
        
        print(f"No collision found after {attempts} attempts")
        return attempts
    
    def compare_algorithms_interactive(self):
        """Interactive hash algorithm comparison"""
        print("\n" + "=" * 60)
        print("HASH ALGORITHM COMPARISON")
        print("=" * 60)
        print("Compare how different hash algorithms process the same input.")
        
        test_string = self.get_user_string("Enter a string to hash with different algorithms: ")
        
        print(f"\nHashing '{test_string}' with different algorithms:")
        print("-" * 60)
        
        algorithm_results = {}
        
        for algo in self.algorithms:
            try:
                hash_value = self.hash_string(test_string, algo)
                hash_length = len(hash_value)
                bit_length = hash_length * 4
                
                print(f"{algo.upper():>6}: {hash_value}")
                print(f"       Length: {hash_length} hex chars ({bit_length} bits)")
                print()
                
                algorithm_results[algo] = {
                    'hash': hash_value,
                    'hex_length': hash_length,
                    'bit_length': bit_length
                }
                
            except ValueError:
                print(f"{algo.upper():>6}: Not available on this system")
        
        self.results['algorithm_comparison'] = {
            'input_string': test_string,
            'algorithms': algorithm_results
        }
        
        # Security note
        print("Security Note:")
        print("- MD5 and SHA1 are cryptographically broken (collision attacks exist)")
        print("- SHA256 and SHA512 are currently considered secure")
        print("- Longer hashes generally provide better security")
    
    def save_results(self, filename="hash_analysis_results.txt"):
        """Save analysis results to formatted plaintext file"""
        if not self.results:
            print("No results to save")
            return
        
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs("../outputs/hash", exist_ok=True)
        output_file = f"../outputs/hash/{filename}"
        
        # Create formatted plaintext content
        content = []
        content.append("=" * 80)
        content.append("CS4910 Lab 1 - Hash Function Analysis Results")
        content.append("=" * 80)
        content.append(f"Analysis Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        content.append("")
        
        # Avalanche Effect Analysis
        if 'avalanche_tests' in self.results:
            content.append("AVALANCHE EFFECT ANALYSIS")
            content.append("-" * 50)
            
            for i, test in enumerate(self.results['avalanche_tests'], 1):
                content.append(f"Test {i}:")
                content.append(f"  Original Input: '{test.get('original_input', 'N/A')}'")
                content.append(f"  Modified Input: '{test.get('modified_input', 'N/A')}'")
                content.append(f"  Original Hash:  {test.get('original_hash', 'N/A')}")
                content.append(f"  Modified Hash:  {test.get('modified_hash', 'N/A')}")
                content.append(f"  Bits Changed:   {test.get('bits_changed', 0)} out of {test.get('total_bits', 0)} ({test.get('change_percentage', 0):.1f}%)")
                content.append(f"  Good Avalanche: {'Yes' if test.get('good_avalanche', False) else 'No'}")
                content.append("")
            
            if self.results['avalanche_tests']:
                content.append("AVALANCHE EFFECT SUMMARY:")
                avg_change = sum(test.get('change_percentage', 0) for test in self.results['avalanche_tests']) / len(self.results['avalanche_tests'])
                content.append(f"  Average bit change: {avg_change:.1f}%")
                content.append(f"  Expected for good hash: ~50%")
                content.append("")
        
        # Birthday Attack Analysis
        if 'birthday_experiments' in self.results:
            content.append("BIRTHDAY ATTACK ANALYSIS")
            content.append("-" * 50)
            
            for exp in self.results['birthday_experiments']:
                content.append(f"Hash Algorithm: {exp.get('algorithm', 'N/A')}")
                content.append(f"  Truncated to: {exp.get('truncated_bits', 'N/A')} bits")
                content.append(f"  Theoretical collision probability (50%): ~{exp.get('theoretical_attempts', 'N/A')} attempts")
                content.append(f"  Actual attempts needed: {exp.get('actual_attempts', 'N/A')}")
                content.append(f"  Efficiency: {exp.get('efficiency', 0):.1f}% of theoretical")
                collision_pair = exp.get('collision_pair', ['N/A', 'N/A'])
                content.append(f"  Colliding inputs: '{collision_pair[0]}' and '{collision_pair[1]}'")
                content.append(f"  Collision hash: {exp.get('collision_hash', 'N/A')}")
                content.append("")
        
        # Algorithm Comparison
        if 'algorithm_comparison' in self.results:
            content.append("HASH ALGORITHM COMPARISON")
            content.append("-" * 50)
            
            comparison_data = self.results['algorithm_comparison']
            # Check for both old and new key names for compatibility
            test_input = comparison_data.get('test_input') or comparison_data.get('input_string')
            if test_input:
                content.append(f"Test Input: '{test_input}'")
                content.append("")
            
            # Check for both old and new key names for compatibility
            results_data = comparison_data.get('results') or comparison_data.get('algorithms')
            if results_data:
                for algo, data in results_data.items():
                    content.append(f"{algo.upper()}:")
                    content.append(f"  Hash: {data.get('hash', 'N/A')}")
                    # Handle both 'length' and 'hex_length' keys
                    length = data.get('length') or data.get('hex_length', 'N/A')
                    content.append(f"  Length: {length} characters")
                    # Add bit length if available
                    if 'bit_length' in data:
                        content.append(f"  Bit Length: {data['bit_length']} bits")
                    # Security level assessment
                    security_level = data.get('security_level')
                    if not security_level:
                        if algo.lower() in ['md5', 'sha1']:
                            security_level = 'Weak (Cryptographically Broken)'
                        elif algo.lower() in ['sha256', 'sha512']:
                            security_level = 'Strong'
                        else:
                            security_level = 'Unknown'
                    content.append(f"  Security Level: {security_level}")
                    content.append("")
        
        # Theoretical Questions (if answered)
        if 'theoretical_answers' in self.results:
            content.append("THEORETICAL ANALYSIS")
            content.append("-" * 50)
            
            for question, answer in self.results['theoretical_answers'].items():
                content.append(f"{question.replace('_', ' ').title()}:")
                content.append(f"  {answer}")
                content.append("")
        
        content.append("=" * 80)
        content.append("End of Hash Function Analysis")
        content.append("=" * 80)
        
        # Save to file
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(content))
            print(f"\nResults saved to {output_file}")
            print("You can copy and paste this content directly into your Word document.")
        except FileNotFoundError:
            # Fallback to current directory
            with open(filename, 'w') as f:
                f.write('\n'.join(content))
            print(f"\nResults saved to {filename}")
            print("You can copy and paste this content directly into your Word document.")
    
    def run_interactive_analysis(self):
        """Run the complete interactive analysis"""
        print("CS4910 Lab 1 - Interactive Hash Function Analysis Tool")
        print("=" * 60)
        print("This tool will guide you through hash function analysis experiments.")
        print("You'll explore the avalanche effect, birthday attacks, and algorithm comparison.")
        
        # Menu system
        while True:
            print("\n" + "=" * 60)
            print("ANALYSIS MENU")
            print("=" * 60)
            print("1. Avalanche Effect Demonstration")
            print("2. Birthday Attack Simulation")
            print("3. Hash Algorithm Comparison")
            print("4. View Results Summary")
            print("5. Save Results and Exit")
            
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == '1':
                self.demonstrate_avalanche_effect_interactive()
            elif choice == '2':
                self.birthday_attack_simulation_interactive()
            elif choice == '3':
                self.compare_algorithms_interactive()
            elif choice == '4':
                self.display_results_summary()
            elif choice == '5':
                self.save_results()
                print("\nAnalysis complete! Your results are ready for your lab report.")
                print("You can copy and paste the content directly into your Word document.")
                
                # AI-Enhanced Learning Suggestions
                print("\n" + "=" * 70)
                print("🤖 AI-ENHANCED LEARNING SUGGESTIONS")
                print("=" * 70)
                print("Use AI to deepen your hash function understanding with these prompts:")
                print("\n1. CONCEPT CLARIFICATION:")
                print('   "Explain the difference between weak and strong collision resistance"')
                print('   "Why is the avalanche effect important in cryptographic hashes?"')
                print("\n2. MATHEMATICAL UNDERSTANDING:")
                print('   "Explain the birthday paradox in simple terms with examples"')
                print('   "How does hash output length affect collision probability?"')
                print("\n3. PRACTICAL APPLICATIONS:")
                print('   "Where are hash functions used in real-world security systems?"')
                print('   "What happens when a hash function is cryptographically broken?"')
                print("\n4. ATTACK SCENARIOS:")
                print('   "How do attackers exploit hash collisions in practice?"')
                print('   "What are rainbow tables and how do they work?"')
                print("\n5. VERIFICATION:")
                print('   "Review my hash analysis results: [paste summary]. What"')
                print('   "additional insights or implications should I consider?"')
                print("\n💡 Remember: Use AI to enhance understanding, not replace analysis!")
                print("   Document all AI interactions in your lab report.")
                print("=" * 70)
                break
            else:
                print("Invalid choice. Please select 1-5.")
    
    def display_results_summary(self):
        """Display summary of all results"""
        if not self.results:
            print("\nNo analysis results yet. Complete some experiments first!")
            return
        
        print("\n" + "=" * 60)
        print("ANALYSIS RESULTS SUMMARY")
        print("=" * 60)
        
        if 'avalanche_effect' in self.results:
            print("✓ Avalanche Effect Analysis completed")
            avg_diff = sum(r['difference_percentage'] for r in self.results['avalanche_effect']['modifications']) / len(self.results['avalanche_effect']['modifications'])
            print(f"  Average bit difference: {avg_diff:.1f}%")
        
        if 'birthday_attack' in self.results:
            print("✓ Birthday Attack Simulation completed")
            print(f"  Found collision in {self.results['birthday_attack']['attempts']} attempts")
        
        if 'algorithm_comparison' in self.results:
            print("✓ Hash Algorithm Comparison completed")
            print(f"  Compared {len(self.results['algorithm_comparison']['algorithms'])} algorithms")

def main():
    analyzer = InteractiveHashAnalyzer()
    analyzer.run_interactive_analysis()

if __name__ == "__main__":
    main()