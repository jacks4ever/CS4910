#!/usr/bin/env python3
"""
CS 4910 Lab 2: Information Theory and Entropy Analysis
Interactive script for calculating and analyzing information entropy in security contexts.

Author: CS 4910 Course Materials
Fall 2025 Semester
"""

import math
import random
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

class EntropyAnalyzer:
    """Class for calculating and analyzing information entropy."""
    
    def __init__(self):
        self.results = {}
    
    def calculate_entropy(self, probabilities):
        """
        Calculate information entropy given a list of probabilities.
        H(X) = -Σ p(x) log₂ p(x)
        """
        entropy = 0
        for p in probabilities:
            if p > 0:  # Avoid log(0)
                entropy -= p * math.log2(p)
        return entropy
    
    def balls_in_bin_analysis(self):
        """Analyze the balls in bin scenario from the homework."""
        print("=" * 60)
        print("BALLS IN BIN ENTROPY ANALYSIS")
        print("=" * 60)
        
        # Initial setup: 4 red, 2 yellow, 3 green
        red, yellow, green = 4, 2, 3
        total = red + yellow + green
        
        print(f"Initial setup: {red} red, {yellow} yellow, {green} green balls")
        print(f"Total balls: {total}")
        
        # Calculate probabilities
        p_red = red / total
        p_yellow = yellow / total
        p_green = green / total
        
        print(f"\nProbabilities:")
        print(f"P(red) = {p_red:.4f}")
        print(f"P(yellow) = {p_yellow:.4f}")
        print(f"P(green) = {p_green:.4f}")
        
        # Part a: Entropy for one event
        entropy_one = self.calculate_entropy([p_red, p_yellow, p_green])
        print(f"\nPart a: Entropy for one event = {entropy_one:.4f} bits")
        
        # Part b: Entropy for five events (independent)
        entropy_five = 5 * entropy_one
        print(f"Part b: Entropy for five events = {entropy_five:.4f} bits")
        
        # Part c: Add 2 yellow balls
        yellow_new = yellow + 2
        total_new = total + 2
        p_red_new = red / total_new
        p_yellow_new = yellow_new / total_new
        p_green_new = green / total_new
        
        print(f"\nAfter adding 2 yellow balls: {red} red, {yellow_new} yellow, {green} green")
        print(f"New probabilities:")
        print(f"P(red) = {p_red_new:.4f}")
        print(f"P(yellow) = {p_yellow_new:.4f}")
        print(f"P(green) = {p_green_new:.4f}")
        
        entropy_new = self.calculate_entropy([p_red_new, p_yellow_new, p_green_new])
        print(f"Part c: New entropy = {entropy_new:.4f} bits")
        
        # Part d: Maximize entropy
        print(f"\nPart d: Finding action to maximize entropy...")
        self.analyze_entropy_changes(red, yellow_new, green, total_new, "maximize")
        
        # Part e: Minimize entropy
        print(f"\nPart e: Finding action to minimize entropy...")
        self.analyze_entropy_changes(red, yellow_new, green, total_new, "minimize")
        
        return {
            'initial_entropy': entropy_one,
            'five_events_entropy': entropy_five,
            'modified_entropy': entropy_new
        }
    
    def analyze_entropy_changes(self, red, yellow, green, total, goal):
        """Analyze how adding or removing balls affects entropy."""
        current_entropy = self.calculate_entropy([red/total, yellow/total, green/total])
        
        options = []
        
        # Try adding one ball of each color
        for color, count in [('red', red), ('yellow', yellow), ('green', green)]:
            new_total = total + 1
            new_counts = [red, yellow, green]
            if color == 'red':
                new_counts[0] += 1
            elif color == 'yellow':
                new_counts[1] += 1
            else:
                new_counts[2] += 1
            
            new_probs = [c/new_total for c in new_counts]
            new_entropy = self.calculate_entropy(new_probs)
            options.append(('add', color, new_entropy, new_entropy - current_entropy))
        
        # Try removing one ball of each color (if possible)
        for color, count in [('red', red), ('yellow', yellow), ('green', green)]:
            if count > 1:  # Can't remove if only one left
                new_total = total - 1
                new_counts = [red, yellow, green]
                if color == 'red':
                    new_counts[0] -= 1
                elif color == 'yellow':
                    new_counts[1] -= 1
                else:
                    new_counts[2] -= 1
                
                new_probs = [c/new_total for c in new_counts]
                new_entropy = self.calculate_entropy(new_probs)
                options.append(('remove', color, new_entropy, new_entropy - current_entropy))
        
        # Sort options based on goal
        if goal == "maximize":
            best_option = max(options, key=lambda x: x[2])
            print(f"To maximize entropy: {best_option[0]} one {best_option[1]} ball")
        else:
            best_option = min(options, key=lambda x: x[2])
            print(f"To minimize entropy: {best_option[0]} one {best_option[1]} ball")
        
        print(f"Current entropy: {current_entropy:.4f} bits")
        print(f"New entropy: {best_option[2]:.4f} bits")
        print(f"Change: {best_option[3]:+.4f} bits")
    
    def communication_entropy_analysis(self):
        """Analyze entropy in communication systems."""
        print("\n" + "=" * 60)
        print("COMMUNICATION ENTROPY ANALYSIS")
        print("=" * 60)
        
        # Part a: Uniform English letters
        num_letters = 26
        uniform_prob = 1 / num_letters
        uniform_entropy = self.calculate_entropy([uniform_prob] * num_letters)
        
        print(f"Part a: Uniform English letter distribution")
        print(f"Number of letters: {num_letters}")
        print(f"Probability per letter: {uniform_prob:.4f}")
        print(f"Entropy per letter: {uniform_entropy:.4f} bits")
        
        # Part b: Bits needed per letter
        bits_per_letter = math.ceil(math.log2(num_letters))
        print(f"\nPart b: Bits needed per letter (efficient encoding): {bits_per_letter} bits")
        
        # Part c: Ten-letter sequence encoding
        total_combinations = num_letters ** 10
        bits_for_sequence = math.ceil(math.log2(total_combinations))
        bits_per_letter_sequence = bits_for_sequence / 10
        
        print(f"\nPart c: Ten-letter sequence analysis")
        print(f"Total possible 10-letter combinations: {total_combinations:,}")
        print(f"Bits needed for sequence: {bits_for_sequence} bits")
        print(f"Bits per letter in sequence: {bits_per_letter_sequence:.1f} bits")
        
        # Part d: English language entropy comparison
        english_entropy_estimate = 4.03  # Approximate entropy of English text
        print(f"\nPart d: English language entropy comparison")
        print(f"Uniform distribution entropy: {uniform_entropy:.4f} bits")
        print(f"English language entropy (X): ~{english_entropy_estimate:.2f} bits")
        print(f"English entropy is LOWER because:")
        print("- Letters have unequal frequencies (e.g., 'e' is more common than 'z')")
        print("- Language has structure and predictable patterns")
        print("- Context reduces uncertainty about next letters")
        
        # Part e: Single sender with header
        header_bits = 8  # 1 byte
        message_bits = 10 * english_entropy_estimate
        total_bits_single = header_bits + message_bits
        
        print(f"\nPart e: Single sender with 1-byte header")
        print(f"Header entropy (single sender): 0 bits (no uncertainty)")
        print(f"Message entropy: 10 × {english_entropy_estimate} = {message_bits:.1f} bits")
        print(f"Total entropy: {total_bits_single:.1f} bits")
        
        # Part f: Multiple senders
        num_senders = 1024
        header_entropy = math.log2(num_senders)
        total_bits_multi = header_entropy + message_bits
        
        print(f"\nPart f: {num_senders} senders with headers")
        print(f"Header entropy: log₂({num_senders}) = {header_entropy:.1f} bits")
        print(f"Message entropy: {message_bits:.1f} bits")
        print(f"Total entropy: {total_bits_multi:.1f} bits")
        
        return {
            'uniform_entropy': uniform_entropy,
            'english_entropy': english_entropy_estimate,
            'single_sender_total': total_bits_single,
            'multi_sender_total': total_bits_multi
        }
    
    def password_entropy_calculator(self):
        """Calculate password entropy based on character set and length."""
        print("\nPassword Entropy Calculator")
        print("-" * 27)
        
        try:
            charset_size = int(input("Character set size (e.g., 26 for lowercase, 62 for alphanumeric): "))
            length = int(input("Password length: "))
            
            # Calculate entropy
            total_combinations = charset_size ** length
            entropy = math.log2(total_combinations)
            
            print(f"\nResults:")
            print(f"Total possible passwords: {total_combinations:,}")
            print(f"Entropy: {entropy:.2f} bits")
            
            # Estimate brute force time
            attempts_per_second = 1e9  # 1 billion attempts per second
            avg_time_seconds = total_combinations / (2 * attempts_per_second)
            
            if avg_time_seconds < 60:
                print(f"Average brute force time: {avg_time_seconds:.2f} seconds")
            elif avg_time_seconds < 3600:
                print(f"Average brute force time: {avg_time_seconds/60:.2f} minutes")
            elif avg_time_seconds < 86400:
                print(f"Average brute force time: {avg_time_seconds/3600:.2f} hours")
            elif avg_time_seconds < 31536000:
                print(f"Average brute force time: {avg_time_seconds/86400:.2f} days")
            else:
                print(f"Average brute force time: {avg_time_seconds/31536000:.2f} years")
                
        except ValueError:
            print("Invalid input. Please enter numeric values.")

def main():
    """Main function to run the entropy analysis."""
    print("CS 4910 Lab 2: Information Theory and Entropy Analysis")
    print("=" * 55)
    
    analyzer = EntropyAnalyzer()
    
    # Run the main analyses
    balls_results = analyzer.balls_in_bin_analysis()
    comm_results = analyzer.communication_entropy_analysis()
    
    # Store results for later use
    analyzer.results.update(balls_results)
    analyzer.results.update(comm_results)
    
    print("\nAnalysis complete! Results saved to analyzer.results")
    print("Use these results in your lab report and AI discussions.")

if __name__ == "__main__":
    main()