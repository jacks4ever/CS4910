#!/usr/bin/env python3
"""
CS4910 Lab 4: Firewall Configuration and IP Blocking Tool
Specifically for Lab 4 Problem 2 - Firewall IP Address Blocking
"""

import json
import datetime
import subprocess
import platform
import socket
import ipaddress
from typing import Dict, List

class FirewallAnalyzer:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.discovered_addresses = {}
        
    def discover_ip_addresses(self) -> Dict:
        """Discover IP addresses using multiple methods"""
        print("\n🔍 IP Address Discovery")
        print("=" * 25)
        
        discovery = {
            'analysis_type': 'ip_discovery',
            'timestamp': datetime.datetime.now().isoformat(),
            'system_info': {
                'os_type': self.os_type,
                'hostname': socket.gethostname()
            },
            'discovery_methods': {},
            'discovered_addresses': {},
            'selected_address': ''
        }
        
        print(f"🖥️ System: {discovery['system_info']['os_type']}")
        print(f"🏠 Hostname: {discovery['system_info']['hostname']}")
        
        # Method 1: Command line discovery
        self.discover_via_commands(discovery)
        
        # Method 2: Python socket discovery
        self.discover_via_python(discovery)
        
        # Method 3: Manual input
        self.discover_via_manual_input(discovery)
        
        # Select primary address
        self.select_primary_address(discovery)
        
        return discovery
    
    def discover_via_commands(self, discovery: Dict):
        """Discover IP addresses using command line tools"""
        print("\n📋 Command Line Discovery Methods:")
        
        if 'linux' in self.os_type:
            commands = [
                ('ifconfig', 'ifconfig'),
                ('ip addr', 'ip addr show'),
                ('hostname -I', 'hostname -I'),
                ('ip route', 'ip route get 8.8.8.8')
            ]
        elif 'darwin' in self.os_type:  # macOS
            commands = [
                ('ifconfig', 'ifconfig'),
                ('networksetup', 'networksetup -getinfo "Wi-Fi"'),
                ('route', 'route get default')
            ]
        else:
            commands = [
                ('ifconfig', 'ifconfig'),
                ('ipconfig', 'ipconfig /all')
            ]
        
        for method_name, command in commands:
            print(f"\n🔧 Method: {method_name}")
            print(f"   Command: {command}")
            
            executed = input(f"Did you execute '{command}'? (y/n): ").lower() == 'y'
            
            if executed:
                output = input("What was the output (paste relevant IP addresses): ")
                addresses_found = input("What IP addresses did you find? (comma-separated): ")
                
                discovery['discovery_methods'][method_name] = {
                    'command': command,
                    'executed': True,
                    'output': output,
                    'addresses_found': [addr.strip() for addr in addresses_found.split(',') if addr.strip()]
                }
            else:
                discovery['discovery_methods'][method_name] = {
                    'command': command,
                    'executed': False,
                    'reason': input(f"Why didn't you execute '{command}'? ")
                }
    
    def discover_via_python(self, discovery: Dict):
        """Discover IP addresses using Python socket methods"""
        print("\n🐍 Python Socket Discovery:")
        
        try:
            # Get hostname IP
            hostname_ip = socket.gethostbyname(socket.gethostname())
            print(f"   Hostname IP: {hostname_ip}")
            
            # Get external IP (connect to external server)
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                external_ip = s.getsockname()[0]
                print(f"   External-facing IP: {external_ip}")
            
            discovery['discovery_methods']['python_socket'] = {
                'method': 'Python socket discovery',
                'hostname_ip': hostname_ip,
                'external_ip': external_ip,
                'success': True
            }
            
        except Exception as e:
            print(f"   Error in Python discovery: {e}")
            discovery['discovery_methods']['python_socket'] = {
                'method': 'Python socket discovery',
                'success': False,
                'error': str(e)
            }
    
    def discover_via_manual_input(self, discovery: Dict):
        """Allow manual input of discovered addresses"""
        print("\n✏️ Manual Address Input:")
        
        manual_addresses = input("Enter any additional IP addresses you discovered (comma-separated): ")
        if manual_addresses.strip():
            addresses = [addr.strip() for addr in manual_addresses.split(',') if addr.strip()]
            discovery['discovery_methods']['manual_input'] = {
                'method': 'Manual input',
                'addresses': addresses
            }
    
    def select_primary_address(self, discovery: Dict):
        """Select the primary IP address to use"""
        print("\n🎯 Primary Address Selection:")
        
        # Collect all discovered addresses
        all_addresses = set()
        
        for method_data in discovery['discovery_methods'].values():
            if method_data.get('addresses_found'):
                all_addresses.update(method_data['addresses_found'])
            if method_data.get('hostname_ip'):
                all_addresses.add(method_data['hostname_ip'])
            if method_data.get('external_ip'):
                all_addresses.add(method_data['external_ip'])
            if method_data.get('addresses'):
                all_addresses.update(method_data['addresses'])
        
        all_addresses = list(all_addresses)
        discovery['discovered_addresses']['all_found'] = all_addresses
        
        if all_addresses:
            print("📋 Discovered addresses:")
            for i, addr in enumerate(all_addresses, 1):
                print(f"   {i}. {addr}")
            
            try:
                choice = int(input(f"\nSelect primary address (1-{len(all_addresses)}): ")) - 1
                if 0 <= choice < len(all_addresses):
                    discovery['selected_address'] = all_addresses[choice]
                else:
                    discovery['selected_address'] = all_addresses[0]
            except ValueError:
                discovery['selected_address'] = all_addresses[0]
        else:
            discovery['selected_address'] = input("No addresses auto-discovered. Please enter your IP address: ")
        
        print(f"✅ Selected address: {discovery['selected_address']}")
    
    def implement_ip_blocking(self, my_address: str) -> Dict:
        """Implement IP address blocking"""
        print("\n🚫 IP Address Blocking Implementation")
        print("=" * 35)
        
        # Calculate target IP (My_address + 1)
        try:
            ip_obj = ipaddress.IPv4Address(my_address)
            target_ip = str(ip_obj + 1)
        except ipaddress.AddressValueError:
            print(f"Invalid IP address: {my_address}")
            target_ip = input("Please enter the target IP to block manually: ")
        
        blocking = {
            'analysis_type': 'ip_blocking',
            'timestamp': datetime.datetime.now().isoformat(),
            'my_address': my_address,
            'target_ip': target_ip,
            'system_info': {
                'os_type': self.os_type,
                'platform': platform.platform()
            },
            'firewall_tool': '',
            'blocking_commands': [],
            'verification_steps': {},
            'screenshots_taken': []
        }
        
        print(f"🎯 My Address: {my_address}")
        print(f"🚫 Target IP to Block: {target_ip}")
        
        # Determine firewall tool
        self.select_firewall_tool(blocking)
        
        # Implement blocking rules
        self.implement_blocking_rules(blocking)
        
        # Verify blocking
        self.verify_blocking(blocking)
        
        return blocking
    
    def select_firewall_tool(self, blocking: Dict):
        """Select appropriate firewall tool"""
        print("\n🔧 Firewall Tool Selection:")
        
        if 'linux' in self.os_type:
            tools = ['iptables', 'ufw', 'firewalld', 'other']
        elif 'darwin' in self.os_type:
            tools = ['pfctl', 'built-in firewall', 'other']
        else:
            tools = ['built-in firewall', 'third-party', 'other']
        
        print("Available firewall tools:")
        for i, tool in enumerate(tools, 1):
            print(f"   {i}. {tool}")
        
        try:
            choice = int(input(f"\nSelect firewall tool (1-{len(tools)}): ")) - 1
            if 0 <= choice < len(tools):
                blocking['firewall_tool'] = tools[choice]
            else:
                blocking['firewall_tool'] = 'other'
        except ValueError:
            blocking['firewall_tool'] = input("Enter the firewall tool you're using: ")
        
        if blocking['firewall_tool'] == 'other':
            blocking['firewall_tool'] = input("Specify the firewall tool: ")
        
        print(f"✅ Selected tool: {blocking['firewall_tool']}")
    
    def implement_blocking_rules(self, blocking: Dict):
        """Implement the actual blocking rules"""
        print(f"\n⚙️ Implementing Blocking Rules with {blocking['firewall_tool']}:")
        
        # Provide tool-specific guidance
        if blocking['firewall_tool'] == 'iptables':
            self.implement_iptables_blocking(blocking)
        elif blocking['firewall_tool'] == 'ufw':
            self.implement_ufw_blocking(blocking)
        elif blocking['firewall_tool'] == 'pfctl':
            self.implement_pfctl_blocking(blocking)
        else:
            self.implement_generic_blocking(blocking)
    
    def implement_iptables_blocking(self, blocking: Dict):
        """Implement iptables blocking rules"""
        target_ip = blocking['target_ip']
        
        suggested_commands = [
            f"sudo iptables -A INPUT -s {target_ip} -j DROP",
            f"sudo iptables -A OUTPUT -d {target_ip} -j DROP",
            "sudo iptables -L -n",
            "sudo iptables-save"
        ]
        
        print("📋 Suggested iptables commands:")
        for i, cmd in enumerate(suggested_commands, 1):
            print(f"   {i}. {cmd}")
        
        for cmd in suggested_commands:
            executed = input(f"\nDid you execute: {cmd}? (y/n): ").lower() == 'y'
            
            if executed:
                output = input("What was the output? ")
                success = input("Was the command successful? (y/n): ").lower() == 'y'
                
                blocking['blocking_commands'].append({
                    'command': cmd,
                    'executed': True,
                    'output': output,
                    'success': success
                })
            else:
                reason = input(f"Why didn't you execute '{cmd}'? ")
                blocking['blocking_commands'].append({
                    'command': cmd,
                    'executed': False,
                    'reason': reason
                })
    
    def implement_ufw_blocking(self, blocking: Dict):
        """Implement UFW blocking rules"""
        target_ip = blocking['target_ip']
        
        suggested_commands = [
            "sudo ufw status",
            f"sudo ufw deny from {target_ip}",
            f"sudo ufw deny to {target_ip}",
            "sudo ufw status numbered"
        ]
        
        print("📋 Suggested UFW commands:")
        for i, cmd in enumerate(suggested_commands, 1):
            print(f"   {i}. {cmd}")
        
        for cmd in suggested_commands:
            executed = input(f"\nDid you execute: {cmd}? (y/n): ").lower() == 'y'
            
            if executed:
                output = input("What was the output? ")
                success = input("Was the command successful? (y/n): ").lower() == 'y'
                
                blocking['blocking_commands'].append({
                    'command': cmd,
                    'executed': True,
                    'output': output,
                    'success': success
                })
    
    def implement_pfctl_blocking(self, blocking: Dict):
        """Implement pfctl blocking rules (macOS)"""
        target_ip = blocking['target_ip']
        
        print("📋 pfctl implementation steps:")
        print("1. Create a pfctl rule file")
        print("2. Add blocking rules")
        print("3. Load the rules")
        
        rule_file = input("What file did you create for pfctl rules? ")
        rules_added = input(f"What rules did you add to block {target_ip}? ")
        load_command = input("What command did you use to load the rules? ")
        
        blocking['blocking_commands'].append({
            'step': 'pfctl rule creation',
            'rule_file': rule_file,
            'rules': rules_added,
            'load_command': load_command
        })
    
    def implement_generic_blocking(self, blocking: Dict):
        """Generic blocking implementation"""
        print(f"📋 Generic {blocking['firewall_tool']} implementation:")
        
        step_count = int(input("How many steps did you perform? "))
        
        for i in range(step_count):
            print(f"\nStep {i+1}:")
            step = {
                'step_description': input("Describe this step: "),
                'command_used': input("Command/action used: "),
                'result': input("What was the result? "),
                'success': input("Was this step successful? (y/n): ").lower() == 'y'
            }
            blocking['blocking_commands'].append(step)
    
    def verify_blocking(self, blocking: Dict):
        """Verify that IP blocking is working"""
        print("\n✅ Blocking Verification")
        print("=" * 20)
        
        verification_methods = [
            "Check firewall rules list",
            "Attempt to ping blocked IP",
            "Check firewall logs",
            "Use network monitoring tools"
        ]
        
        for method in verification_methods:
            print(f"\n🔍 {method}:")
            performed = input(f"Did you perform this verification? (y/n): ").lower() == 'y'
            
            if performed:
                command_used = input("What command/method did you use? ")
                result = input("What were the results? ")
                confirms_blocking = input("Does this confirm blocking is working? (y/n): ").lower() == 'y'
                
                blocking['verification_steps'][method] = {
                    'performed': True,
                    'command': command_used,
                    'result': result,
                    'confirms_blocking': confirms_blocking
                }
            else:
                blocking['verification_steps'][method] = {
                    'performed': False,
                    'reason': input("Why was this verification not performed? ")
                }
        
        # Screenshots
        screenshots = input("What screenshots did you take? (comma-separated descriptions): ")
        if screenshots.strip():
            blocking['screenshots_taken'] = [s.strip() for s in screenshots.split(',')]
    
    def save_analysis(self, analysis: Dict, filename: str):
        """Save analysis to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {filename}")
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate formatted report"""
        analysis_type = analysis.get('analysis_type', 'Unknown')
        
        report = f"""
# Firewall Analysis Report
Generated: {analysis['timestamp']}
Analysis Type: {analysis_type}

## Analysis Results

"""
        
        if analysis_type == 'ip_discovery':
            report += self.generate_discovery_report(analysis)
        elif analysis_type == 'ip_blocking':
            report += self.generate_blocking_report(analysis)
        
        return report
    
    def generate_discovery_report(self, analysis: Dict) -> str:
        """Generate IP discovery report"""
        report = "### IP Address Discovery\n\n"
        report += f"**System**: {analysis['system_info']['os_type']}\n"
        report += f"**Hostname**: {analysis['system_info']['hostname']}\n\n"
        
        report += "**Discovery Methods Used**:\n"
        for method, data in analysis['discovery_methods'].items():
            if data.get('executed'):
                report += f"- {method}: {data.get('command', 'N/A')}\n"
        
        report += f"\n**Selected Address**: {analysis['selected_address']}\n"
        return report
    
    def generate_blocking_report(self, analysis: Dict) -> str:
        """Generate IP blocking report"""
        report = "### IP Address Blocking\n\n"
        report += f"**My Address**: {analysis['my_address']}\n"
        report += f"**Target IP Blocked**: {analysis['target_ip']}\n"
        report += f"**Firewall Tool**: {analysis['firewall_tool']}\n\n"
        
        report += "**Commands Executed**:\n"
        for i, cmd in enumerate(analysis['blocking_commands'], 1):
            if cmd.get('executed'):
                report += f"{i}. `{cmd['command']}`\n"
                report += f"   Result: {cmd.get('success', 'Unknown')}\n"
        
        return report

def main():
    analyzer = FirewallAnalyzer()
    
    print("🔥 CS4910 Lab 4: Firewall Configuration and IP Blocking Tool")
    print("=" * 60)
    print("This tool helps with Lab 4 Problem 2 - Firewall IP Address Blocking")
    
    options = [
        "Discover IP Addresses (Part a)",
        "Implement IP Blocking (Part b)",
        "Complete Workflow (Parts a + b)",
        "Exit"
    ]
    
    while True:
        print("\nAnalysis Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            if choice == 1:
                discovery = analyzer.discover_ip_addresses()
                filename = f"ip_discovery_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(discovery, filename)
                
                # Generate report
                report = analyzer.generate_report(discovery)
                report_filename = f"ip_discovery_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 2:
                my_address = input("Enter your IP address (My_address): ")
                blocking = analyzer.implement_ip_blocking(my_address)
                filename = f"ip_blocking_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(blocking, filename)
                
                # Generate report
                report = analyzer.generate_report(blocking)
                report_filename = f"ip_blocking_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 3:
                # Complete workflow
                print("🔄 Complete Firewall Analysis Workflow")
                
                # Part a: Discovery
                discovery = analyzer.discover_ip_addresses()
                my_address = discovery['selected_address']
                
                # Part b: Blocking
                blocking = analyzer.implement_ip_blocking(my_address)
                
                # Save both analyses
                discovery_filename = f"complete_ip_discovery_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                blocking_filename = f"complete_ip_blocking_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                analyzer.save_analysis(discovery, discovery_filename)
                analyzer.save_analysis(blocking, blocking_filename)
                
                # Generate combined report
                combined_report = analyzer.generate_report(discovery) + "\n" + analyzer.generate_report(blocking)
                report_filename = f"complete_firewall_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(combined_report)
                print(f"📄 Combined report generated: {report_filename}")
                
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