#!/usr/bin/env python3
"""
CS 4910 Lab 2: Digital Envelope System Implementation
Interactive script for implementing and analyzing digital envelope systems.

Author: CS 4910 Course Materials
Fall 2025 Semester
"""

import hashlib
import os
import base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import json

class DigitalEnvelope:
    """Implementation of a digital envelope system providing confidentiality and authentication."""
    
    def __init__(self):
        self.sender_private_key = None
        self.sender_public_key = None
        self.receiver_private_key = None
        self.receiver_public_key = None
        
    def generate_key_pairs(self):
        """Generate RSA key pairs for sender and receiver."""
        print("Generating RSA key pairs...")
        
        # Generate sender's key pair
        self.sender_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.sender_public_key = self.sender_private_key.public_key()
        
        # Generate receiver's key pair
        self.receiver_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.receiver_public_key = self.receiver_private_key.public_key()
        
        print("Key pairs generated successfully!")
        
    def create_digital_envelope(self, message, sender_private_key, receiver_public_key):
        """
        Create a digital envelope that provides both confidentiality and authentication.
        
        Process:
        1. Generate symmetric key for message encryption
        2. Encrypt message with symmetric key (confidentiality)
        3. Encrypt symmetric key with receiver's public key (key confidentiality)
        4. Create message hash for integrity
        5. Sign hash with sender's private key (authentication)
        6. Package everything into digital envelope
        """
        print(f"\nCreating digital envelope for message: '{message}'")
        print("-" * 50)
        
        # Step 1: Generate symmetric key (AES-256)
        symmetric_key = os.urandom(32)  # 256 bits
        print(f"1. Generated symmetric key: {base64.b64encode(symmetric_key).decode()[:32]}...")
        
        # Step 2: Encrypt message with symmetric key
        iv = os.urandom(16)  # 128-bit IV for AES
        cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # Pad message to block size
        message_bytes = message.encode('utf-8')
        padding_length = 16 - (len(message_bytes) % 16)
        padded_message = message_bytes + bytes([padding_length] * padding_length)
        
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        print(f"2. Encrypted message with AES-256-CBC")
        
        # Step 3: Encrypt symmetric key with receiver's public key
        encrypted_key = receiver_public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"3. Encrypted symmetric key with receiver's public key")
        
        # Step 4: Create message hash for integrity
        message_hash = hashlib.sha256(message_bytes).digest()
        print(f"4. Created SHA-256 hash of original message")
        
        # Step 5: Sign hash with sender's private key (authentication)
        signature = sender_private_key.sign(
            message_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print(f"5. Signed message hash with sender's private key")
        
        # Step 6: Package digital envelope
        envelope = {
            'encrypted_message': base64.b64encode(encrypted_message).decode(),
            'iv': base64.b64encode(iv).decode(),
            'encrypted_key': base64.b64encode(encrypted_key).decode(),
            'signature': base64.b64encode(signature).decode(),
            'message_hash': base64.b64encode(message_hash).decode()
        }
        
        print(f"6. Packaged digital envelope")
        print(f"\nDigital envelope created successfully!")
        print(f"Envelope size: {len(json.dumps(envelope))} bytes")
        
        return envelope
    
    def open_digital_envelope(self, envelope, sender_public_key, receiver_private_key):
        """
        Open and verify a digital envelope.
        
        Process:
        1. Extract components from envelope
        2. Decrypt symmetric key with receiver's private key
        3. Decrypt message with symmetric key
        4. Verify signature with sender's public key
        5. Verify message integrity with hash
        """
        print(f"\nOpening digital envelope...")
        print("-" * 30)
        
        try:
            # Step 1: Extract components
            encrypted_message = base64.b64decode(envelope['encrypted_message'])
            iv = base64.b64decode(envelope['iv'])
            encrypted_key = base64.b64decode(envelope['encrypted_key'])
            signature = base64.b64decode(envelope['signature'])
            received_hash = base64.b64decode(envelope['message_hash'])
            print(f"1. Extracted envelope components")
            
            # Step 2: Decrypt symmetric key
            symmetric_key = receiver_private_key.decrypt(
                encrypted_key,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            print(f"2. Decrypted symmetric key with receiver's private key")
            
            # Step 3: Decrypt message
            cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv), backend=default_backend())
            decryptor = cipher.decryptor()
            padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
            
            # Remove padding
            padding_length = padded_message[-1]
            message_bytes = padded_message[:-padding_length]
            message = message_bytes.decode('utf-8')
            print(f"3. Decrypted message with symmetric key")
            
            # Step 4: Verify message integrity
            calculated_hash = hashlib.sha256(message_bytes).digest()
            if calculated_hash != received_hash:
                raise ValueError("Message integrity check failed!")
            print(f"4. Verified message integrity (hash match)")
            
            # Step 5: Verify signature (authentication)
            sender_public_key.verify(
                signature,
                calculated_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            print(f"5. Verified sender's signature (authentication successful)")
            
            print(f"\nDigital envelope opened successfully!")
            print(f"Decrypted message: '{message}'")
            print(f"All security properties verified:")
            print(f"  ✓ Confidentiality (message encrypted)")
            print(f"  ✓ Authentication (signature verified)")
            print(f"  ✓ Integrity (hash verified)")
            print(f"  ✓ Non-repudiation (digital signature)")
            
            return message
            
        except Exception as e:
            print(f"ERROR: Failed to open digital envelope: {str(e)}")
            return None
    
    def analyze_security_properties(self):
        """Analyze the security properties achieved by the digital envelope system."""
        print("\n" + "=" * 60)
        print("DIGITAL ENVELOPE SECURITY ANALYSIS")
        print("=" * 60)
        
        print("\n1. CONFIDENTIALITY:")
        print("   - Message encrypted with AES-256 symmetric encryption")
        print("   - Symmetric key encrypted with RSA-2048 public key encryption")
        print("   - Only receiver with private key can decrypt")
        print("   - Provides strong confidentiality protection")
        
        print("\n2. AUTHENTICATION:")
        print("   - Message hash signed with sender's private key")
        print("   - Signature verified using sender's public key")
        print("   - Proves message came from claimed sender")
        print("   - Prevents impersonation attacks")
        
        print("\n3. INTEGRITY:")
        print("   - SHA-256 hash of original message included")
        print("   - Hash verified after decryption")
        print("   - Detects any message tampering")
        print("   - Ensures message hasn't been modified")
        
        print("\n4. NON-REPUDIATION:")
        print("   - Digital signature provides non-repudiation")
        print("   - Sender cannot deny sending the message")
        print("   - Signature is cryptographically bound to sender")
        print("   - Provides legal evidence of communication")
        
        print("\n5. KEY MANAGEMENT:")
        print("   - Hybrid approach combines symmetric and asymmetric crypto")
        print("   - Symmetric key provides efficient bulk encryption")
        print("   - Asymmetric encryption secures key exchange")
        print("   - No need for pre-shared secrets")
    
    def demonstrate_attack_scenarios(self):
        """Demonstrate various attack scenarios and how the system resists them."""
        print("\n" + "=" * 60)
        print("ATTACK SCENARIO DEMONSTRATIONS")
        print("=" * 60)
        
        # Generate test message and envelope
        test_message = "This is a confidential message for testing."
        envelope = self.create_digital_envelope(
            test_message, 
            self.sender_private_key, 
            self.receiver_public_key
        )
        
        print("\n1. EAVESDROPPING ATTACK:")
        print("   Attacker intercepts the digital envelope...")
        print("   Without receiver's private key, cannot decrypt symmetric key")
        print("   Without symmetric key, cannot decrypt message")
        print("   → ATTACK FAILED: Confidentiality maintained")
        
        print("\n2. MESSAGE TAMPERING ATTACK:")
        print("   Attacker modifies encrypted message...")
        tampered_envelope = envelope.copy()
        tampered_data = base64.b64decode(envelope['encrypted_message'])
        tampered_data = tampered_data[:-1] + b'\x00'  # Modify last byte
        tampered_envelope['encrypted_message'] = base64.b64encode(tampered_data).decode()
        
        result = self.open_digital_envelope(
            tampered_envelope, 
            self.sender_public_key, 
            self.receiver_private_key
        )
        if result is None:
            print("   → ATTACK FAILED: Tampering detected")
        
        print("\n3. SIGNATURE FORGERY ATTACK:")
        print("   Attacker tries to forge sender's signature...")
        forged_envelope = envelope.copy()
        fake_signature = os.urandom(256)  # Random signature
        forged_envelope['signature'] = base64.b64encode(fake_signature).decode()
        
        result = self.open_digital_envelope(
            forged_envelope, 
            self.sender_public_key, 
            self.receiver_private_key
        )
        if result is None:
            print("   → ATTACK FAILED: Signature verification failed")
        
        print("\n4. REPLAY ATTACK:")
        print("   Attacker resends old digital envelope...")
        print("   System should implement timestamp/nonce mechanisms")
        print("   Current implementation vulnerable to replay")
        print("   → MITIGATION: Add timestamps and sequence numbers")
    
    def interactive_demo(self):
        """Interactive demonstration of the digital envelope system."""
        print("\n" + "=" * 60)
        print("INTERACTIVE DIGITAL ENVELOPE DEMO")
        print("=" * 60)
        
        while True:
            print("\nOptions:")
            print("1. Send a message (create digital envelope)")
            print("2. Receive a message (open digital envelope)")
            print("3. Analyze security properties")
            print("4. Demonstrate attack scenarios")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == '1':
                message = input("Enter message to send: ")
                envelope = self.create_digital_envelope(
                    message, 
                    self.sender_private_key, 
                    self.receiver_public_key
                )
                print(f"\nEnvelope JSON (first 200 chars):")
                print(json.dumps(envelope, indent=2)[:200] + "...")
                
            elif choice == '2':
                message = input("Enter a test message to send and receive: ")
                envelope = self.create_digital_envelope(
                    message, 
                    self.sender_private_key, 
                    self.receiver_public_key
                )
                received_message = self.open_digital_envelope(
                    envelope, 
                    self.sender_public_key, 
                    self.receiver_private_key
                )
                
            elif choice == '3':
                self.analyze_security_properties()
                
            elif choice == '4':
                self.demonstrate_attack_scenarios()
                
            elif choice == '5':
                break
                
            else:
                print("Invalid choice. Please try again.")

def main():
    """Main function to run the digital envelope demonstration."""
    print("CS 4910 Lab 2: Digital Envelope System")
    print("=" * 40)
    
    try:
        # Initialize digital envelope system
        envelope_system = DigitalEnvelope()
        envelope_system.generate_key_pairs()
        
        # Run interactive demo
        envelope_system.interactive_demo()
        
        print("\nDigital envelope demonstration complete!")
        
    except ImportError as e:
        print(f"Error: Missing required cryptography library")
        print(f"Install with: pip install cryptography")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()