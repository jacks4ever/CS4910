#!/usr/bin/env python3
"""
CS4910 Lab 4: TCP SYN Cookie Analysis Tool
Specifically for Lab 4 Problem 1 - TCP SYN Cookies and DoS Defense
"""

import json
import datetime
import subprocess
import platform
import os
from typing import Dict, List

class SYNCookieAnalyzer:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.syn_cookie_statements = [
            "SYN cookies disallow an attacker from completing the TCP handshake. An attacker cannot complete the TCP handshake.",
            "SYN cookies cause major degradation of service.",
            "SYN cookies cause TCP resets."
        ]
        
    def analyze_syn_cookie_defense(self) -> Dict:
        """Analyze how SYN cookies defend against SYN flooding"""
        print("\n🛡️ TCP SYN Cookie Defense Analysis")
        print("=" * 40)
        
        analysis = {
            'analysis_type': 'syn_cookie_defense',
            'timestamp': datetime.datetime.now().isoformat(),
            'defense_mechanism': {},
            'effective_against': [],
            'implementation_details': {}
        }
        
        print("📋 SYN Cookie Defense Mechanism Analysis:")
        
        # Defense mechanism explanation
        print("\n1. How do SYN cookies defend against SYN flooding?")
        analysis['defense_mechanism']['explanation'] = input("Enter your explanation: ")
        analysis['defense_mechanism']['key_principles'] = input("What are the key principles? (comma-separated): ").split(',')
        analysis['defense_mechanism']['state_elimination'] = input("How do SYN cookies eliminate connection state storage? ")
        
        # Types of DoS attacks it's effective against
        print("\n2. What types of DoS attacks are SYN cookies effective against?")
        dos_types = [
            "TCP SYN Flood attacks",
            "Connection exhaustion attacks", 
            "Memory exhaustion attacks",
            "Bandwidth consumption attacks",
            "Application layer attacks"
        ]
        
        for i, dos_type in enumerate(dos_types, 1):
            print(f"{i}. {dos_type}")
        
        effective_indices = input("\nSelect effective attack types (comma-separated numbers): ")
        try:
            indices = [int(x.strip()) - 1 for x in effective_indices.split(',')]
            analysis['effective_against'] = [dos_types[i] for i in indices if 0 <= i < len(dos_types)]
        except ValueError:
            analysis['effective_against'] = ["TCP SYN Flood attacks"]  # Default
        
        return analysis
    
    def analyze_syn_cookie_statements(self) -> Dict:
        """Analyze true/false statements about SYN cookies"""
        print("\n📝 SYN Cookie Statement Analysis")
        print("=" * 35)
        
        analysis = {
            'analysis_type': 'syn_cookie_statements',
            'timestamp': datetime.datetime.now().isoformat(),
            'statement_analysis': {}
        }
        
        for i, statement in enumerate(self.syn_cookie_statements, 1):
            print(f"\n📋 Statement {i}:")
            print(f'"{statement}"')
            
            statement_analysis = {
                'statement': statement,
                'true_false': input(f"\nIs this statement TRUE or FALSE? ").upper(),
                'explanation': input("Explain your reasoning: "),
                'technical_details': input("Provide technical details: "),
                'implications': input("What are the implications? ")
            }
            
            analysis['statement_analysis'][f'statement_{i}'] = statement_analysis
        
        return analysis
    
    def implement_syn_cookies(self) -> Dict:
        """Guide implementation of SYN cookies on Unix system"""
        print("\n⚙️ SYN Cookie Implementation")
        print("=" * 30)
        
        implementation = {
            'analysis_type': 'syn_cookie_implementation',
            'timestamp': datetime.datetime.now().isoformat(),
            'system_info': {
                'os_type': self.os_type,
                'os_version': platform.platform(),
                'kernel_version': platform.release()
            },
            'implementation_steps': [],
            'verification_results': {},
            'configuration_files': {}
        }
        
        print(f"🖥️ Detected OS: {implementation['system_info']['os_type']}")
        print(f"📋 Platform: {implementation['system_info']['os_version']}")
        
        # Provide OS-specific guidance
        if 'linux' in self.os_type:
            self.implement_linux_syn_cookies(implementation)
        elif 'darwin' in self.os_type:  # macOS
            self.implement_macos_syn_cookies(implementation)
        else:
            self.implement_generic_syn_cookies(implementation)
        
        return implementation
    
    def implement_linux_syn_cookies(self, implementation: Dict):
        """Linux-specific SYN cookie implementation"""
        print("\n🐧 Linux SYN Cookie Implementation:")
        
        steps = [
            "Check current SYN cookie status",
            "Enable SYN cookies temporarily", 
            "Make SYN cookies persistent",
            "Verify implementation",
            "Test effectiveness"
        ]
        
        commands = [
            "cat /proc/sys/net/ipv4/tcp_syncookies",
            "sudo sysctl -w net.ipv4.tcp_syncookies=1",
            "echo 'net.ipv4.tcp_syncookies = 1' | sudo tee -a /etc/sysctl.conf",
            "sysctl net.ipv4.tcp_syncookies",
            "netstat -s | grep -i syn"
        ]
        
        for i, (step, command) in enumerate(zip(steps, commands), 1):
            print(f"\n{i}. {step}")
            print(f"   Command: {command}")
            
            executed = input(f"Did you execute this command? (y/n): ").lower() == 'y'
            if executed:
                output = input(f"What was the output? ")
                implementation['implementation_steps'].append({
                    'step': step,
                    'command': command,
                    'executed': True,
                    'output': output
                })
            else:
                implementation['implementation_steps'].append({
                    'step': step,
                    'command': command,
                    'executed': False,
                    'reason': input("Why not executed? ")
                })
        
        # Configuration file analysis
        print(f"\n📁 Configuration Files:")
        config_files = ['/proc/sys/net/ipv4/tcp_syncookies', '/etc/sysctl.conf']
        
        for config_file in config_files:
            if input(f"Did you modify {config_file}? (y/n): ").lower() == 'y':
                implementation['configuration_files'][config_file] = {
                    'modified': True,
                    'changes': input(f"What changes were made to {config_file}? "),
                    'backup_created': input(f"Did you create a backup? (y/n): ").lower() == 'y'
                }
    
    def implement_macos_syn_cookies(self, implementation: Dict):
        """macOS-specific SYN cookie implementation"""
        print("\n🍎 macOS SYN Cookie Implementation:")
        print("Note: macOS has different SYN flood protection mechanisms")
        
        steps = [
            "Check current TCP settings",
            "Review network parameters",
            "Configure SYN flood protection",
            "Verify settings"
        ]
        
        commands = [
            "sysctl -a | grep tcp",
            "netstat -s -p tcp",
            "sudo sysctl -w net.inet.tcp.blackhole=2",
            "sysctl net.inet.tcp.blackhole"
        ]
        
        for i, (step, command) in enumerate(zip(steps, commands), 1):
            print(f"\n{i}. {step}")
            print(f"   Command: {command}")
            
            executed = input(f"Did you execute this command? (y/n): ").lower() == 'y'
            if executed:
                output = input(f"What was the output? ")
                implementation['implementation_steps'].append({
                    'step': step,
                    'command': command,
                    'executed': True,
                    'output': output
                })
    
    def implement_generic_syn_cookies(self, implementation: Dict):
        """Generic Unix SYN cookie implementation guidance"""
        print(f"\n🖥️ Generic Unix SYN Cookie Implementation:")
        print("Please provide the specific commands you used for your system:")
        
        step_count = int(input("How many implementation steps did you perform? "))
        
        for i in range(step_count):
            print(f"\nStep {i+1}:")
            step = {
                'step_description': input("Describe this step: "),
                'command_used': input("Command used: "),
                'output': input("Output received: "),
                'success': input("Was this step successful? (y/n): ").lower() == 'y'
            }
            implementation['implementation_steps'].append(step)
    
    def verify_syn_cookie_implementation(self, implementation: Dict):
        """Verify SYN cookie implementation"""
        print("\n✅ SYN Cookie Verification")
        print("=" * 25)
        
        verification_tests = [
            "Check SYN cookie parameter value",
            "Monitor network statistics",
            "Test under simulated load",
            "Verify log entries"
        ]
        
        for test in verification_tests:
            print(f"\n🔍 {test}:")
            performed = input(f"Did you perform this verification? (y/n): ").lower() == 'y'
            
            if performed:
                result = input(f"What were the results? ")
                success = input(f"Was verification successful? (y/n): ").lower() == 'y'
                
                implementation['verification_results'][test] = {
                    'performed': True,
                    'result': result,
                    'success': success
                }
            else:
                implementation['verification_results'][test] = {
                    'performed': False,
                    'reason': input(f"Why was this verification not performed? ")
                }
    
    def save_analysis(self, analysis: Dict, filename: str):
        """Save analysis to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {filename}")
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate formatted report"""
        analysis_type = analysis.get('analysis_type', 'Unknown')
        
        report = f"""
# TCP SYN Cookie Analysis Report
Generated: {analysis['timestamp']}
Analysis Type: {analysis_type}

## Analysis Results

"""
        
        if analysis_type == 'syn_cookie_defense':
            report += self.generate_defense_report(analysis)
        elif analysis_type == 'syn_cookie_statements':
            report += self.generate_statements_report(analysis)
        elif analysis_type == 'syn_cookie_implementation':
            report += self.generate_implementation_report(analysis)
        
        return report
    
    def generate_defense_report(self, analysis: Dict) -> str:
        """Generate defense mechanism report"""
        report = "### SYN Cookie Defense Mechanism\n\n"
        report += f"**Explanation**: {analysis['defense_mechanism']['explanation']}\n\n"
        report += f"**Key Principles**:\n"
        for principle in analysis['defense_mechanism']['key_principles']:
            report += f"- {principle.strip()}\n"
        report += f"\n**Effective Against**:\n"
        for attack_type in analysis['effective_against']:
            report += f"- {attack_type}\n"
        return report
    
    def generate_statements_report(self, analysis: Dict) -> str:
        """Generate statements analysis report"""
        report = "### SYN Cookie Statement Analysis\n\n"
        for statement_id, statement_data in analysis['statement_analysis'].items():
            report += f"**{statement_id.replace('_', ' ').title()}**:\n"
            report += f"Statement: \"{statement_data['statement']}\"\n"
            report += f"Answer: {statement_data['true_false']}\n"
            report += f"Explanation: {statement_data['explanation']}\n\n"
        return report
    
    def generate_implementation_report(self, analysis: Dict) -> str:
        """Generate implementation report"""
        report = "### SYN Cookie Implementation\n\n"
        report += f"**System**: {analysis['system_info']['os_type']} - {analysis['system_info']['os_version']}\n\n"
        report += f"**Implementation Steps**:\n"
        for i, step in enumerate(analysis['implementation_steps'], 1):
            report += f"{i}. {step['step']}\n"
            report += f"   Command: `{step['command']}`\n"
            if step.get('executed'):
                report += f"   Output: {step['output']}\n"
            report += "\n"
        return report

def main():
    analyzer = SYNCookieAnalyzer()
    
    print("🛡️ CS4910 Lab 4: TCP SYN Cookie Analysis Tool")
    print("=" * 50)
    print("This tool helps with Lab 4 Problem 1 - TCP SYN Cookies and DoS Defense")
    
    options = [
        "Analyze SYN Cookie Defense Mechanism",
        "Analyze SYN Cookie Statements (True/False)",
        "Implement SYN Cookies on Unix System",
        "Exit"
    ]
    
    while True:
        print("\nAnalysis Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            if choice == 1:
                analysis = analyzer.analyze_syn_cookie_defense()
                filename = f"syn_cookie_defense_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(analysis, filename)
                
                # Generate report
                report = analyzer.generate_report(analysis)
                report_filename = f"syn_cookie_defense_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 2:
                analysis = analyzer.analyze_syn_cookie_statements()
                filename = f"syn_cookie_statements_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(analysis, filename)
                
                # Generate report
                report = analyzer.generate_report(analysis)
                report_filename = f"syn_cookie_statements_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 3:
                implementation = analyzer.implement_syn_cookies()
                analyzer.verify_syn_cookie_implementation(implementation)
                filename = f"syn_cookie_implementation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(implementation, filename)
                
                # Generate report
                report = analyzer.generate_report(implementation)
                report_filename = f"syn_cookie_implementation_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 4:
                print("👋 Goodbye!")
                break
                
            else:
                print("Please enter a number between 1 and 4.")
                
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()