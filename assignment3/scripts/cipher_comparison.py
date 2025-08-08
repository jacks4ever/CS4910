#!/usr/bin/env python3
"""
CS 4910 Lab 2: Symmetric Cipher Security Comparison
Interactive script for comparing DES and AES encryption algorithms.

Author: CS 4910 Course Materials
Fall 2025 Semester
"""

import math
import time
import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import matplotlib.pyplot as plt

class CipherComparison:
    """Class for comparing symmetric encryption algorithms."""
    
    def __init__(self):
        self.backend = default_backend()
        
    def analyze_key_space(self):
        """Analyze and compare key spaces of different algorithms."""
        print("=" * 60)
        print("KEY SPACE ANALYSIS")
        print("=" * 60)
        
        algorithms_info = {
            "DES": {
                "key_length": 56,  # Effective key length (64 bits with 8 parity bits)
                "block_size": 64,
                "year_introduced": 1977
            },
            "3DES": {
                "key_length": 112,  # Effective (168 bits with some weaknesses)
                "block_size": 64,
                "year_introduced": 1998
            },
            "AES-128": {
                "key_length": 128,
                "block_size": 128,
                "year_introduced": 2001
            },
            "AES-192": {
                "key_length": 192,
                "block_size": 128,
                "year_introduced": 2001
            },
            "AES-256": {
                "key_length": 256,
                "block_size": 128,
                "year_introduced": 2001
            }
        }
        
        print(f"{'Algorithm':<12} {'Key Length':<12} {'Key Space':<20} {'Security Level'}")
        print("-" * 70)
        
        for alg_name, info in algorithms_info.items():
            key_length = info["key_length"]
            key_space = 2 ** key_length
            
            print(f"{alg_name:<12} {key_length:<12} {key_space:<20.2e} {key_length//2} bits")
        
        print("\nKey Space Comparison:")
        des_space = 2 ** 56
        aes128_space = 2 ** 128
        aes256_space = 2 ** 256
        
        print(f"AES-128 vs DES: {aes128_space / des_space:.2e} times larger")
        print(f"AES-256 vs DES: {aes256_space / des_space:.2e} times larger")
        print(f"AES-256 vs AES-128: {aes256_space / aes128_space:.2e} times larger")
        
        return algorithms_info
    
    def brute_force_analysis(self):
        """Analyze brute force attack resistance."""
        print("\n" + "=" * 60)
        print("BRUTE FORCE ATTACK ANALYSIS")
        print("=" * 60)
        
        # Different computational scenarios
        scenarios = {
            "Single CPU (2020)": 1e6,      # 1 million keys/second
            "High-end GPU (2020)": 1e9,    # 1 billion keys/second
            "GPU Cluster (100 GPUs)": 1e11, # 100 billion keys/second
            "Theoretical Quantum": 1e15,    # 1 petakey/second (hypothetical)
        }
        
        algorithms = {
            "DES": 56,
            "AES-128": 128,
            "AES-256": 256
        }
        
        print(f"Time to break encryption (average case):")
        print(f"{'Scenario':<25} {'DES (56-bit)':<15} {'AES-128':<15} {'AES-256'}")
        print("-" * 80)
        
        for scenario_name, keys_per_second in scenarios.items():
            times = []
            for alg_name, key_bits in algorithms.items():
                # Average case: need to try half the key space
                avg_attempts = (2 ** key_bits) / 2
                time_seconds = avg_attempts / keys_per_second
                times.append(self.format_time(time_seconds))
            
            print(f"{scenario_name:<25} {times[0]:<15} {times[1]:<15} {times[2]}")
        
        print("\nSecurity Implications:")
        print("- DES is completely broken against modern attacks")
        print("- AES-128 provides adequate security for most applications")
        print("- AES-256 provides long-term security against quantum computers")
        
    def format_time(self, seconds):
        """Format time in human-readable format."""
        if seconds < 1:
            return f"{seconds*1000:.1f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        elif seconds < 3600:
            return f"{seconds/60:.1f}min"
        elif seconds < 86400:
            return f"{seconds/3600:.1f}hr"
        elif seconds < 31536000:
            return f"{seconds/86400:.1f}days"
        elif seconds < 31536000000:
            return f"{seconds/31536000:.1f}yrs"
        else:
            return f"{seconds/31536000:.1e}yrs"
    
    def performance_benchmark(self):
        """Benchmark encryption/decryption performance."""
        print("\n" + "=" * 60)
        print("PERFORMANCE BENCHMARK")
        print("=" * 60)
        
        # Test data
        test_data = b"A" * 1024 * 1024  # 1 MB of data
        
        # AES-128 benchmark
        aes128_key = os.urandom(16)
        aes128_iv = os.urandom(16)
        
        start_time = time.time()
        cipher = Cipher(algorithms.AES(aes128_key), modes.CBC(aes128_iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(test_data) + encryptor.finalize()
        aes128_encrypt_time = time.time() - start_time
        
        start_time = time.time()
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        aes128_decrypt_time = time.time() - start_time
        
        # AES-256 benchmark
        aes256_key = os.urandom(32)
        aes256_iv = os.urandom(16)
        
        start_time = time.time()
        cipher = Cipher(algorithms.AES(aes256_key), modes.CBC(aes256_iv), backend=self.backend)
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(test_data) + encryptor.finalize()
        aes256_encrypt_time = time.time() - start_time
        
        start_time = time.time()
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
        aes256_decrypt_time = time.time() - start_time
        
        # Results
        data_size_mb = len(test_data) / (1024 * 1024)
        
        print(f"Test data size: {data_size_mb:.1f} MB")
        print(f"{'Algorithm':<12} {'Encrypt Time':<15} {'Decrypt Time':<15} {'Throughput (MB/s)'}")
        print("-" * 65)
        
        aes128_throughput = data_size_mb / aes128_encrypt_time
        aes256_throughput = data_size_mb / aes256_encrypt_time
        
        print(f"{'AES-128':<12} {aes128_encrypt_time:<15.4f} {aes128_decrypt_time:<15.4f} {aes128_throughput:<15.1f}")
        print(f"{'AES-256':<12} {aes256_encrypt_time:<15.4f} {aes256_decrypt_time:<15.4f} {aes256_throughput:<15.1f}")
        
        print(f"\nPerformance Analysis:")
        if aes128_throughput > aes256_throughput:
            ratio = aes128_throughput / aes256_throughput
            print(f"AES-128 is {ratio:.1f}x faster than AES-256")
        else:
            ratio = aes256_throughput / aes128_throughput
            print(f"AES-256 is {ratio:.1f}x faster than AES-128")
        
        print("Note: Performance depends on hardware, implementation, and CPU features")
        
        return {
            'aes128_encrypt_time': aes128_encrypt_time,
            'aes256_encrypt_time': aes256_encrypt_time,
            'aes128_throughput': aes128_throughput,
            'aes256_throughput': aes256_throughput
        }
    
    def security_evolution_analysis(self):
        """Analyze the evolution of symmetric cipher security."""
        print("\n" + "=" * 60)
        print("CIPHER SECURITY EVOLUTION")
        print("=" * 60)
        
        timeline = [
            (1977, "DES", "56-bit key, revolutionary for its time"),
            (1993, "DES Cracked", "First academic break of DES"),
            (1998, "DES Cracker", "Hardware device breaks DES in 56 hours"),
            (1998, "3DES", "Triple DES extends DES lifetime"),
            (2001, "AES Selected", "Rijndael chosen as AES"),
            (2005, "AES Adoption", "Widespread AES deployment begins"),
            (2020, "Post-Quantum", "Preparation for quantum-resistant crypto")
        ]
        
        print("Cryptographic Timeline:")
        for year, event, description in timeline:
            print(f"{year}: {event:<15} - {description}")
        
        print(f"\nSecurity Margin Analysis:")
        print(f"DES (1977-2005): ~28 years of practical security")
        print(f"AES (2001-present): 20+ years and counting")
        print(f"Expected AES lifetime: 30+ years (conservative estimate)")
        
        print(f"\nWhy AES Replaced DES:")
        print(f"1. Key Length: 56 bits → 128/192/256 bits")
        print(f"2. Block Size: 64 bits → 128 bits")
        print(f"3. Algorithm Design: More rounds, better diffusion")
        print(f"4. Cryptanalysis Resistance: No practical attacks on full AES")
        print(f"5. Performance: Optimized for modern processors")
    
    def quantum_impact_analysis(self):
        """Analyze the impact of quantum computing on symmetric ciphers."""
        print("\n" + "=" * 60)
        print("QUANTUM COMPUTING IMPACT")
        print("=" * 60)
        
        print("Grover's Algorithm Impact on Symmetric Ciphers:")
        print("- Provides quadratic speedup for brute force attacks")
        print("- Effectively halves the security level of symmetric keys")
        print("- Does not break symmetric ciphers completely (unlike RSA)")
        
        print(f"\nEffective Security Levels Against Quantum Attacks:")
        algorithms = {
            "DES": (56, 28),
            "AES-128": (128, 64),
            "AES-192": (192, 96),
            "AES-256": (256, 128)
        }
        
        print(f"{'Algorithm':<12} {'Classical Security':<18} {'Quantum Security'}")
        print("-" * 50)
        for alg, (classical, quantum) in algorithms.items():
            print(f"{alg:<12} {classical:<18} {quantum}")
        
        print(f"\nRecommendations:")
        print(f"- AES-128: Adequate for near-term (10-15 years)")
        print(f"- AES-256: Recommended for long-term security")
        print(f"- Key doubling: Simple mitigation strategy")
        print(f"- Post-quantum algorithms: For asymmetric crypto only")
    
    def practical_implementation_analysis(self):
        """Analyze practical implementation considerations."""
        print("\n" + "=" * 60)
        print("PRACTICAL IMPLEMENTATION ANALYSIS")
        print("=" * 60)
        
        print("Implementation Considerations:")
        
        print(f"\n1. HARDWARE SUPPORT:")
        print(f"   - Modern CPUs have AES-NI instructions")
        print(f"   - Hardware acceleration provides 4-10x speedup")
        print(f"   - DES hardware support is legacy/deprecated")
        
        print(f"\n2. MEMORY REQUIREMENTS:")
        print(f"   - DES: Small lookup tables, minimal memory")
        print(f"   - AES: Larger S-boxes, more memory efficient than expected")
        print(f"   - Both suitable for embedded systems")
        
        print(f"\n3. POWER CONSUMPTION:")
        print(f"   - AES generally more power efficient per bit")
        print(f"   - Hardware implementations much more efficient")
        print(f"   - Important for mobile and IoT devices")
        
        print(f"\n4. SIDE-CHANNEL RESISTANCE:")
        print(f"   - DES vulnerable to timing and power analysis")
        print(f"   - AES designed with side-channel resistance in mind")
        print(f"   - Proper implementation crucial for both")
        
        print(f"\n5. COMPLIANCE AND STANDARDS:")
        print(f"   - DES deprecated by NIST (2005)")
        print(f"   - AES required for US government (FIPS 140-2)")
        print(f"   - International standards mandate AES")
    
    def interactive_comparison(self):
        """Interactive cipher comparison tool."""
        print("\n" + "=" * 60)
        print("INTERACTIVE CIPHER COMPARISON")
        print("=" * 60)
        
        while True:
            print("\nOptions:")
            print("1. Key space analysis")
            print("2. Brute force resistance")
            print("3. Performance benchmark")
            print("4. Security evolution")
            print("5. Quantum computing impact")
            print("6. Implementation considerations")
            print("7. Custom security analysis")
            print("8. Exit")
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.analyze_key_space()
            elif choice == '2':
                self.brute_force_analysis()
            elif choice == '3':
                self.performance_benchmark()
            elif choice == '4':
                self.security_evolution_analysis()
            elif choice == '5':
                self.quantum_impact_analysis()
            elif choice == '6':
                self.practical_implementation_analysis()
            elif choice == '7':
                self.custom_security_analysis()
            elif choice == '8':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def custom_security_analysis(self):
        """Custom security analysis tool."""
        print("\nCustom Security Analysis")
        print("-" * 24)
        
        try:
            key_length = int(input("Enter key length in bits: "))
            attack_rate = float(input("Enter attack rate (keys/second): "))
            
            key_space = 2 ** key_length
            avg_time = key_space / (2 * attack_rate)
            
            print(f"\nResults:")
            print(f"Key space: {key_space:.2e}")
            print(f"Average break time: {self.format_time(avg_time)}")
            
            # Security level assessment
            if avg_time < 86400:  # Less than 1 day
                security_level = "BROKEN"
            elif avg_time < 31536000:  # Less than 1 year
                security_level = "WEAK"
            elif avg_time < 31536000 * 10:  # Less than 10 years
                security_level = "MARGINAL"
            elif avg_time < 31536000 * 100:  # Less than 100 years
                security_level = "ADEQUATE"
            else:
                security_level = "STRONG"
            
            print(f"Security assessment: {security_level}")
            
        except ValueError:
            print("Invalid input. Please enter numeric values.")
    
    def generate_security_report(self):
        """Generate a comprehensive security comparison report."""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE SECURITY REPORT")
        print("=" * 60)
        
        print("EXECUTIVE SUMMARY:")
        print("- DES is cryptographically broken and should not be used")
        print("- AES-128 provides adequate security for most applications")
        print("- AES-256 recommended for high-security and long-term use")
        print("- Performance difference between AES variants is minimal")
        
        print(f"\nDETAILED COMPARISON:")
        
        # Key space comparison
        des_space = 2**56
        aes128_space = 2**128
        aes256_space = 2**256
        
        print(f"Key Space Security:")
        print(f"  DES:     {des_space:.2e} keys ({56} bits)")
        print(f"  AES-128: {aes128_space:.2e} keys ({128} bits)")
        print(f"  AES-256: {aes256_space:.2e} keys ({256} bits)")
        
        print(f"\nBrute Force Resistance (1 billion keys/sec):")
        print(f"  DES:     {self.format_time(des_space/(2*1e9))}")
        print(f"  AES-128: {self.format_time(aes128_space/(2*1e9))}")
        print(f"  AES-256: {self.format_time(aes256_space/(2*1e9))}")
        
        print(f"\nRECOMMENDations:")
        print(f"1. Migrate from DES immediately")
        print(f"2. Use AES-128 for general applications")
        print(f"3. Use AES-256 for:")
        print(f"   - Government/military applications")
        print(f"   - Long-term data protection (>20 years)")
        print(f"   - High-value targets")
        print(f"   - Quantum-resistant requirements")

def main():
    """Main function to run the cipher comparison analysis."""
    print("CS 4910 Lab 2: Symmetric Cipher Security Comparison")
    print("=" * 52)
    
    try:
        comparison = CipherComparison()
        
        # Run main analyses
        comparison.analyze_key_space()
        comparison.brute_force_analysis()
        comparison.performance_benchmark()
        
        # Interactive comparison
        comparison.interactive_comparison()
        
        # Generate final report
        comparison.generate_security_report()
        
        print("\nCipher comparison analysis complete!")
        
    except ImportError as e:
        print(f"Error: Missing required cryptography library")
        print(f"Install with: pip install cryptography matplotlib")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()