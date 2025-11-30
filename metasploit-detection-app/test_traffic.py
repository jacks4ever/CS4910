#!/usr/bin/env python3
"""
Test Traffic Generator for Metasploit Attack Detection System
Generates simulated attack patterns for testing detection capabilities
"""

import socket
import time
import random
import argparse
from datetime import datetime

class AttackSimulator:
    def __init__(self, target='127.0.0.1'):
        self.target = target
        
    def log(self, message):
        """Print timestamped log message"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {message}")
    
    def port_scan(self, start_port=20, end_port=100):
        """Simulate a port scanning attack"""
        self.log(f"🔍 Starting port scan on {self.target} (ports {start_port}-{end_port})")
        
        for port in range(start_port, end_port + 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                result = sock.connect_ex((self.target, port))
                sock.close()
                
                if result == 0:
                    self.log(f"  ✓ Port {port} is open")
                
                time.sleep(0.05)  # Small delay between scans
            except Exception as e:
                self.log(f"  ✗ Error scanning port {port}: {e}")
        
        self.log("✓ Port scan complete")
    
    def syn_flood(self, port=80, duration=5, rate=100):
        """Simulate SYN flood attack (connection attempts)"""
        self.log(f"💥 Starting SYN flood simulation on {self.target}:{port}")
        self.log(f"   Duration: {duration}s, Rate: {rate} connections/sec")
        
        start_time = time.time()
        count = 0
        
        while (time.time() - start_time) < duration:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.01)
                sock.connect_ex((self.target, port))
                sock.close()
                count += 1
                time.sleep(1.0 / rate)
            except Exception:
                pass
        
        self.log(f"✓ SYN flood complete ({count} connections attempted)")
    
    def http_attack(self, port=80):
        """Simulate HTTP-based attack patterns"""
        self.log(f"🌐 Sending HTTP attack patterns to {self.target}:{port}")
        
        attack_payloads = [
            b"GET /manager/html HTTP/1.1\r\nHost: target\r\n\r\n",  # Tomcat
            b"GET / HTTP/1.1\r\nUser-Agent: () { :; }; echo vulnerable\r\n\r\n",  # Shellshock
            b"GET /?id=1' OR '1'='1 HTTP/1.1\r\nHost: target\r\n\r\n",  # SQL injection
        ]
        
        for i, payload in enumerate(attack_payloads, 1):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                sock.connect((self.target, port))
                sock.send(payload)
                sock.close()
                self.log(f"  ✓ Sent attack pattern {i}")
                time.sleep(1)
            except Exception as e:
                self.log(f"  ✗ Failed to send pattern {i}: {e}")
        
        self.log("✓ HTTP attacks complete")
    
    def ftp_attack(self, port=21):
        """Simulate FTP backdoor attack"""
        self.log(f"📁 Attempting FTP attack on {self.target}:{port}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((self.target, port))
            
            # Receive banner
            banner = sock.recv(1024)
            self.log(f"  Banner: {banner.decode('utf-8', errors='ignore').strip()}")
            
            # Send backdoor trigger
            sock.send(b"USER test:)\r\n")
            time.sleep(0.5)
            response = sock.recv(1024)
            self.log(f"  Response: {response.decode('utf-8', errors='ignore').strip()}")
            
            sock.close()
            self.log("✓ FTP attack complete")
        except Exception as e:
            self.log(f"✗ FTP attack failed: {e}")
    
    def random_attacks(self, duration=30):
        """Run random attacks for specified duration"""
        self.log(f"🎲 Starting random attack simulation for {duration} seconds")
        
        attacks = [
            (self.port_scan, {'start_port': 20, 'end_port': 50}),
            (self.syn_flood, {'port': 80, 'duration': 3, 'rate': 50}),
            (self.http_attack, {'port': 80}),
            (self.ftp_attack, {'port': 21}),
        ]
        
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            attack_func, kwargs = random.choice(attacks)
            try:
                attack_func(**kwargs)
            except Exception as e:
                self.log(f"✗ Attack failed: {e}")
            
            time.sleep(random.randint(2, 5))
        
        self.log("✓ Random attack simulation complete")

def main():
    parser = argparse.ArgumentParser(
        description='Test traffic generator for Metasploit Attack Detection System'
    )
    parser.add_argument(
        '--target',
        default='127.0.0.1',
        help='Target IP address (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--attack',
        choices=['port-scan', 'syn-flood', 'http', 'ftp', 'random', 'all'],
        default='all',
        help='Attack type to simulate (default: all)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=30,
        help='Duration in seconds for continuous attacks (default: 30)'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Metasploit Attack Detection - Test Traffic Generator")
    print("=" * 60)
    print(f"Target: {args.target}")
    print(f"Attack Type: {args.attack}")
    print("=" * 60)
    print()
    
    simulator = AttackSimulator(target=args.target)
    
    try:
        if args.attack == 'port-scan':
            simulator.port_scan()
        elif args.attack == 'syn-flood':
            simulator.syn_flood(duration=args.duration)
        elif args.attack == 'http':
            simulator.http_attack()
        elif args.attack == 'ftp':
            simulator.ftp_attack()
        elif args.attack == 'random':
            simulator.random_attacks(duration=args.duration)
        elif args.attack == 'all':
            simulator.log("Running all attack simulations...")
            simulator.port_scan(start_port=20, end_port=50)
            time.sleep(2)
            simulator.syn_flood(port=80, duration=5, rate=50)
            time.sleep(2)
            simulator.http_attack()
            time.sleep(2)
            simulator.ftp_attack()
            simulator.log("✓ All attack simulations complete")
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
    except Exception as e:
        print(f"\n[!] Error: {e}")
    
    print("\n" + "=" * 60)
    print("Test complete - Check the dashboard for detections")
    print("=" * 60)

if __name__ == '__main__':
    main()
