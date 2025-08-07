#!/usr/bin/env python3
"""
CS4910 Lab 4: SMTP Packet Filtering Analysis Tool
Specifically for Lab 4 Textbook Problems 9.5 and 9.6 - SMTP Filtering Rules
"""

import json
import datetime
from typing import Dict, List, Tuple

class SMTPFilteringAnalyzer:
    def __init__(self):
        self.smtp_port = 25
        self.high_ports_start = 1023
        
        # Standard SMTP filtering rules (Problem 9.5)
        self.standard_rules = [
            {
                'rule_id': 1,
                'action': 'ALLOW',
                'protocol': 'TCP',
                'src_ip': 'ANY',
                'src_port': '>1023',
                'dst_ip': '172.16.1.1',
                'dst_port': '25',
                'description': 'Allow inbound SMTP connections'
            },
            {
                'rule_id': 2,
                'action': 'ALLOW',
                'protocol': 'TCP',
                'src_ip': '172.16.1.1',
                'src_port': '25',
                'dst_ip': 'ANY',
                'dst_port': '>1023',
                'description': 'Allow outbound SMTP responses'
            },
            {
                'rule_id': 3,
                'action': 'ALLOW',
                'protocol': 'TCP',
                'src_ip': '172.16.1.1',
                'src_port': '>1023',
                'dst_ip': 'ANY',
                'dst_port': '25',
                'description': 'Allow outbound SMTP connections'
            },
            {
                'rule_id': 4,
                'action': 'ALLOW',
                'protocol': 'TCP',
                'src_ip': 'ANY',
                'src_port': '25',
                'dst_ip': '172.16.1.1',
                'dst_port': '>1023',
                'description': 'Allow inbound SMTP responses'
            },
            {
                'rule_id': 5,
                'action': 'DENY',
                'protocol': 'ANY',
                'src_ip': 'ANY',
                'src_port': 'ANY',
                'dst_ip': 'ANY',
                'dst_port': 'ANY',
                'description': 'Default deny all'
            }
        ]
        
        # Test packets for Problem 9.5
        self.test_packets = [
            {
                'packet_id': 1,
                'protocol': 'TCP',
                'src_ip': '192.168.3.4',
                'src_port': '1234',
                'dst_ip': '172.16.1.1',
                'dst_port': '25',
                'description': 'Remote user connecting to local SMTP server'
            },
            {
                'packet_id': 2,
                'protocol': 'TCP',
                'src_ip': '172.16.1.1',
                'src_port': '25',
                'dst_ip': '192.168.3.4',
                'dst_port': '1234',
                'description': 'Local SMTP server responding to remote user'
            },
            {
                'packet_id': 3,
                'protocol': 'TCP',
                'src_ip': '172.16.1.1',
                'src_port': '2345',
                'dst_ip': '192.168.3.4',
                'dst_port': '25',
                'description': 'Local user connecting to remote SMTP server'
            },
            {
                'packet_id': 4,
                'protocol': 'TCP',
                'src_ip': '192.168.3.4',
                'src_port': '25',
                'dst_ip': '172.16.1.1',
                'dst_port': '2345',
                'description': 'Remote SMTP server responding to local user'
            }
        ]
        
        # Attack packets for Problem 9.5 part (c)
        self.attack_packets = [
            {
                'packet_id': 5,
                'protocol': 'TCP',
                'src_ip': '10.1.2.3',
                'src_port': '5150',
                'dst_ip': '172.16.3.4',
                'dst_port': '8080',
                'description': 'External attacker to web proxy server'
            },
            {
                'packet_id': 6,
                'protocol': 'TCP',
                'src_ip': '172.16.3.4',
                'src_port': '8080',
                'dst_ip': '10.1.2.3',
                'dst_port': '5150',
                'description': 'Web proxy server responding to external attacker'
            }
        ]
    
    def analyze_problem_9_5(self) -> Dict:
        """Analyze Problem 9.5 - Basic SMTP Filtering Rules"""
        print("\n📧 Problem 9.5: SMTP Packet Filtering Rules Analysis")
        print("=" * 55)
        
        analysis = {
            'problem': '9.5',
            'problem_type': 'smtp_filtering_basic',
            'timestamp': datetime.datetime.now().isoformat(),
            'scenario': {
                'local_host': '172.16.1.1',
                'remote_host': '192.168.3.4',
                'smtp_port': 25,
                'high_ports': '>1023'
            },
            'rule_analysis': {},
            'packet_analysis': {},
            'attack_analysis': {}
        }
        
        print("📋 Scenario:")
        print(f"   - Local Host: {analysis['scenario']['local_host']}")
        print(f"   - Remote Host: {analysis['scenario']['remote_host']}")
        print(f"   - SMTP Port: {analysis['scenario']['smtp_port']}")
        print(f"   - User Ports: {analysis['scenario']['high_ports']}")
        
        # Part (a): Analyze each rule
        self.analyze_rule_effects(analysis)
        
        # Part (b): Analyze test packets
        self.analyze_test_packets(analysis)
        
        # Part (c): Analyze attack scenario
        self.analyze_attack_scenario(analysis)
        
        return analysis
    
    def analyze_rule_effects(self, analysis: Dict):
        """Analyze the effect of each filtering rule"""
        print(f"\n📜 Part (a): Rule Effect Analysis")
        
        for rule in self.standard_rules:
            print(f"\n🔍 Rule {rule['rule_id']}:")
            print(f"   {rule['action']} {rule['protocol']} from {rule['src_ip']}:{rule['src_port']} to {rule['dst_ip']}:{rule['dst_port']}")
            print(f"   Description: {rule['description']}")
            
            effect_analysis = {
                'rule': rule,
                'purpose': input(f"What is the purpose of Rule {rule['rule_id']}? "),
                'traffic_allowed': input(f"What traffic does Rule {rule['rule_id']} allow/deny? "),
                'security_impact': input(f"What is the security impact of Rule {rule['rule_id']}? ")
            }
            
            analysis['rule_analysis'][f'rule_{rule["rule_id"]}'] = effect_analysis
    
    def analyze_test_packets(self, analysis: Dict):
        """Analyze test packets against the rule set"""
        print(f"\n📦 Part (b): Test Packet Analysis")
        
        for packet in self.test_packets:
            print(f"\n📨 Packet {packet['packet_id']}:")
            print(f"   {packet['protocol']} from {packet['src_ip']}:{packet['src_port']} to {packet['dst_ip']}:{packet['dst_port']}")
            print(f"   Description: {packet['description']}")
            
            # Determine which rule applies
            matching_rule = self.find_matching_rule(packet, self.standard_rules)
            
            packet_analysis = {
                'packet': packet,
                'matching_rule': matching_rule['rule_id'] if matching_rule else None,
                'action': matching_rule['action'] if matching_rule else 'DENY',
                'user_analysis': {}
            }
            
            # Get user analysis
            user_action = input(f"Is Packet {packet['packet_id']} PERMITTED or DENIED? ").upper()
            user_rule = input(f"Which rule applies to Packet {packet['packet_id']}? ")
            reasoning = input(f"Explain your reasoning: ")
            
            packet_analysis['user_analysis'] = {
                'action': user_action,
                'rule_used': user_rule,
                'reasoning': reasoning,
                'matches_calculated': user_action == packet_analysis['action']
            }
            
            analysis['packet_analysis'][f'packet_{packet["packet_id"]}'] = packet_analysis
            
            # Show calculated result
            if matching_rule:
                print(f"   ✅ Calculated: {packet_analysis['action']} by Rule {matching_rule['rule_id']}")
            else:
                print(f"   ❌ Calculated: DENY (no matching rule)")
    
    def analyze_attack_scenario(self, analysis: Dict):
        """Analyze attack packets against the rule set"""
        print(f"\n🚨 Part (c): Attack Scenario Analysis")
        print("   External attacker (10.1.2.3) attempting to connect to web proxy (172.16.3.4:8080)")
        
        for packet in self.attack_packets:
            print(f"\n🎯 Attack Packet {packet['packet_id']}:")
            print(f"   {packet['protocol']} from {packet['src_ip']}:{packet['src_port']} to {packet['dst_ip']}:{packet['dst_port']}")
            print(f"   Description: {packet['description']}")
            
            # Determine which rule applies
            matching_rule = self.find_matching_rule(packet, self.standard_rules)
            
            attack_analysis = {
                'packet': packet,
                'matching_rule': matching_rule['rule_id'] if matching_rule else None,
                'action': matching_rule['action'] if matching_rule else 'DENY',
                'user_analysis': {}
            }
            
            # Get user analysis
            user_action = input(f"Is Attack Packet {packet['packet_id']} PERMITTED or DENIED? ").upper()
            user_rule = input(f"Which rule applies? ")
            
            attack_analysis['user_analysis'] = {
                'action': user_action,
                'rule_used': user_rule,
                'matches_calculated': user_action == attack_analysis['action']
            }
            
            analysis['attack_analysis'][f'attack_packet_{packet["packet_id"]}'] = attack_analysis
        
        # Overall attack success analysis
        print(f"\n🔍 Attack Success Analysis:")
        analysis['attack_analysis']['attack_success'] = input("Will the attack succeed? (YES/NO) ").upper()
        analysis['attack_analysis']['success_reasoning'] = input("Explain why the attack will/won't succeed: ")
        analysis['attack_analysis']['security_implications'] = input("What are the security implications? ")
    
    def analyze_problem_9_6(self, basic_analysis: Dict) -> Dict:
        """Analyze Problem 9.6 - Enhanced SMTP Filtering Rules"""
        print("\n🔒 Problem 9.6: Enhanced SMTP Filtering Rules Analysis")
        print("=" * 55)
        
        analysis = {
            'problem': '9.6',
            'problem_type': 'smtp_filtering_enhanced',
            'timestamp': datetime.datetime.now().isoformat(),
            'scenario': basic_analysis['scenario'].copy(),
            'rule_changes': {},
            'enhanced_packet_analysis': {},
            'security_improvements': {}
        }
        
        print("📋 Enhanced Rule Set Analysis:")
        print("The rule set from Problem 9.5 has been modified for better protection.")
        
        # Part (a): Describe the changes
        self.analyze_rule_changes(analysis)
        
        # Part (b): Apply new rules to same packets
        self.analyze_enhanced_packet_filtering(analysis, basic_analysis)
        
        return analysis
    
    def analyze_rule_changes(self, analysis: Dict):
        """Analyze changes made to enhance security"""
        print(f"\n🔄 Part (a): Rule Set Changes Analysis")
        
        print("What changes were made to the rule set?")
        
        changes = {
            'modifications_made': input("Describe the specific modifications: "),
            'rules_added': input("Were any rules added? Describe: "),
            'rules_removed': input("Were any rules removed? Describe: "),
            'rules_modified': input("Were any existing rules modified? Describe: "),
            'security_rationale': input("What is the security rationale for these changes? ")
        }
        
        analysis['rule_changes'] = changes
        
        # Get the enhanced rule set
        print(f"\n📜 Enhanced Rule Set:")
        rule_count = int(input("How many rules are in the enhanced set? "))
        
        enhanced_rules = []
        for i in range(rule_count):
            print(f"\nEnhanced Rule {i+1}:")
            rule = {
                'rule_id': i+1,
                'action': input("Action (ALLOW/DENY): ").upper(),
                'protocol': input("Protocol: "),
                'src_ip': input("Source IP: "),
                'src_port': input("Source Port: "),
                'dst_ip': input("Destination IP: "),
                'dst_port': input("Destination Port: "),
                'description': input("Description: ")
            }
            enhanced_rules.append(rule)
        
        analysis['enhanced_rules'] = enhanced_rules
    
    def analyze_enhanced_packet_filtering(self, analysis: Dict, basic_analysis: Dict):
        """Apply enhanced rules to the same test packets"""
        print(f"\n📦 Part (b): Enhanced Packet Analysis")
        print("Applying the enhanced rule set to the same six packets from Problem 9.5")
        
        # Combine test packets and attack packets
        all_packets = self.test_packets + self.attack_packets
        
        for packet in all_packets:
            print(f"\n📨 Packet {packet['packet_id']} (Enhanced Analysis):")
            print(f"   {packet['protocol']} from {packet['src_ip']}:{packet['src_port']} to {packet['dst_ip']}:{packet['dst_port']}")
            
            # Get original result for comparison
            original_key = f'packet_{packet["packet_id"]}' if packet['packet_id'] <= 4 else f'attack_packet_{packet["packet_id"]}'
            if packet['packet_id'] <= 4:
                original_result = basic_analysis['packet_analysis'].get(original_key, {})
            else:
                original_result = basic_analysis['attack_analysis'].get(original_key, {})
            
            original_action = original_result.get('action', 'UNKNOWN')
            print(f"   Original Result: {original_action}")
            
            # Analyze with enhanced rules
            enhanced_action = input(f"With enhanced rules, is Packet {packet['packet_id']} PERMITTED or DENIED? ").upper()
            enhanced_rule = input(f"Which enhanced rule applies? ")
            reasoning = input(f"Explain the reasoning: ")
            
            enhanced_analysis = {
                'packet': packet,
                'original_action': original_action,
                'enhanced_action': enhanced_action,
                'rule_used': enhanced_rule,
                'reasoning': reasoning,
                'action_changed': enhanced_action != original_action
            }
            
            analysis['enhanced_packet_analysis'][f'packet_{packet["packet_id"]}'] = enhanced_analysis
            
            if enhanced_analysis['action_changed']:
                print(f"   🔄 Action Changed: {original_action} → {enhanced_action}")
            else:
                print(f"   ✅ Action Unchanged: {enhanced_action}")
    
    def find_matching_rule(self, packet: Dict, rules: List[Dict]) -> Dict:
        """Find the first matching rule for a packet"""
        for rule in rules:
            if self.packet_matches_rule(packet, rule):
                return rule
        return None
    
    def packet_matches_rule(self, packet: Dict, rule: Dict) -> bool:
        """Check if a packet matches a rule"""
        # Protocol check
        if rule['protocol'] != 'ANY' and packet['protocol'] != rule['protocol']:
            return False
        
        # Source IP check
        if rule['src_ip'] != 'ANY' and packet['src_ip'] != rule['src_ip']:
            return False
        
        # Destination IP check
        if rule['dst_ip'] != 'ANY' and packet['dst_ip'] != rule['dst_ip']:
            return False
        
        # Source port check
        if rule['src_port'] != 'ANY':
            if rule['src_port'].startswith('>'):
                threshold = int(rule['src_port'][1:])
                if int(packet['src_port']) <= threshold:
                    return False
            elif packet['src_port'] != rule['src_port']:
                return False
        
        # Destination port check
        if rule['dst_port'] != 'ANY':
            if rule['dst_port'].startswith('>'):
                threshold = int(rule['dst_port'][1:])
                if int(packet['dst_port']) <= threshold:
                    return False
            elif packet['dst_port'] != rule['dst_port']:
                return False
        
        return True
    
    def compare_rule_sets(self, basic_analysis: Dict, enhanced_analysis: Dict) -> Dict:
        """Compare basic vs enhanced rule sets"""
        print("\n⚖️ Rule Set Comparison Analysis")
        print("=" * 35)
        
        comparison = {
            'analysis_type': 'rule_set_comparison',
            'timestamp': datetime.datetime.now().isoformat(),
            'security_improvements': {},
            'functionality_impact': {},
            'overall_assessment': {}
        }
        
        print("📊 Comparative Analysis:")
        
        # Security improvements
        print(f"\n🔒 Security Improvements:")
        comparison['security_improvements'] = {
            'attack_prevention': input("How do the enhanced rules better prevent attacks? "),
            'vulnerability_reduction': input("What vulnerabilities are reduced? "),
            'false_positive_impact': input("Do enhanced rules increase false positives? "),
            'detection_capability': input("How is attack detection improved? ")
        }
        
        # Functionality impact
        print(f"\n⚙️ Functionality Impact:")
        comparison['functionality_impact'] = {
            'legitimate_traffic': input("How do enhanced rules affect legitimate SMTP traffic? "),
            'usability_changes': input("Are there any usability impacts? "),
            'performance_considerations': input("What are the performance implications? "),
            'maintenance_complexity': input("How does rule complexity change? ")
        }
        
        # Overall assessment
        print(f"\n📈 Overall Assessment:")
        comparison['overall_assessment'] = {
            'security_vs_usability': input("How do you balance security vs usability? "),
            'recommendation': input("Would you recommend the enhanced rule set? Why? "),
            'further_improvements': input("What further improvements could be made? ")
        }
        
        return comparison
    
    def save_analysis(self, analysis: Dict, filename: str):
        """Save analysis to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {filename}")
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate formatted report"""
        problem = analysis.get('problem', 'Unknown')
        problem_type = analysis.get('problem_type', analysis.get('analysis_type', 'Unknown'))
        
        report = f"""
# SMTP Filtering Analysis Report
Generated: {analysis['timestamp']}
Problem: {problem}
Type: {problem_type}

## Analysis Results

"""
        
        if problem == '9.5':
            report += self.generate_problem_9_5_report(analysis)
        elif problem == '9.6':
            report += self.generate_problem_9_6_report(analysis)
        elif problem_type == 'rule_set_comparison':
            report += self.generate_comparison_report(analysis)
        
        return report
    
    def generate_problem_9_5_report(self, analysis: Dict) -> str:
        """Generate Problem 9.5 report"""
        report = "### Problem 9.5: Basic SMTP Filtering Rules\n\n"
        
        report += "**Rule Analysis**:\n"
        for rule_key, rule_data in analysis['rule_analysis'].items():
            rule_id = rule_data['rule']['rule_id']
            report += f"- **Rule {rule_id}**: {rule_data['purpose']}\n"
        
        report += "\n**Packet Analysis**:\n"
        for packet_key, packet_data in analysis['packet_analysis'].items():
            packet_id = packet_data['packet']['packet_id']
            action = packet_data['user_analysis']['action']
            rule = packet_data['user_analysis']['rule_used']
            report += f"- **Packet {packet_id}**: {action} (Rule {rule})\n"
        
        report += "\n**Attack Analysis**:\n"
        attack_success = analysis['attack_analysis'].get('attack_success', 'UNKNOWN')
        report += f"- **Attack Success**: {attack_success}\n"
        report += f"- **Reasoning**: {analysis['attack_analysis'].get('success_reasoning', 'N/A')}\n"
        
        return report
    
    def generate_problem_9_6_report(self, analysis: Dict) -> str:
        """Generate Problem 9.6 report"""
        report = "### Problem 9.6: Enhanced SMTP Filtering Rules\n\n"
        
        report += "**Rule Changes**:\n"
        report += f"- Modifications: {analysis['rule_changes']['modifications_made']}\n"
        report += f"- Security Rationale: {analysis['rule_changes']['security_rationale']}\n\n"
        
        report += "**Enhanced Packet Analysis**:\n"
        for packet_key, packet_data in analysis['enhanced_packet_analysis'].items():
            packet_id = packet_data['packet']['packet_id']
            original = packet_data['original_action']
            enhanced = packet_data['enhanced_action']
            changed = " (CHANGED)" if packet_data['action_changed'] else ""
            report += f"- **Packet {packet_id}**: {original} → {enhanced}{changed}\n"
        
        return report
    
    def generate_comparison_report(self, analysis: Dict) -> str:
        """Generate rule set comparison report"""
        report = "### SMTP Rule Set Comparison\n\n"
        
        report += "**Security Improvements**:\n"
        report += f"- Attack Prevention: {analysis['security_improvements']['attack_prevention']}\n"
        report += f"- Vulnerability Reduction: {analysis['security_improvements']['vulnerability_reduction']}\n\n"
        
        report += "**Overall Assessment**:\n"
        report += f"- Recommendation: {analysis['overall_assessment']['recommendation']}\n"
        
        return report

def main():
    analyzer = SMTPFilteringAnalyzer()
    
    print("📧 CS4910 Lab 4: SMTP Packet Filtering Analysis Tool")
    print("=" * 55)
    print("This tool helps with Lab 4 Textbook Problems 9.5 and 9.6")
    
    options = [
        "Analyze Problem 9.5 (Basic SMTP Filtering)",
        "Analyze Problem 9.6 (Enhanced SMTP Filtering)",
        "Complete Analysis (9.5 + 9.6 + Comparison)",
        "Exit"
    ]
    
    basic_analysis = None
    enhanced_analysis = None
    
    while True:
        print("\nAnalysis Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            if choice == 1:
                basic_analysis = analyzer.analyze_problem_9_5()
                filename = f"problem_9_5_smtp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(basic_analysis, filename)
                
                # Generate report
                report = analyzer.generate_report(basic_analysis)
                report_filename = f"problem_9_5_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 2:
                if basic_analysis is None:
                    print("📧 First, let's analyze Problem 9.5 for baseline:")
                    basic_analysis = analyzer.analyze_problem_9_5()
                
                enhanced_analysis = analyzer.analyze_problem_9_6(basic_analysis)
                filename = f"problem_9_6_smtp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(enhanced_analysis, filename)
                
                # Generate report
                report = analyzer.generate_report(enhanced_analysis)
                report_filename = f"problem_9_6_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 3:
                # Complete analysis workflow
                if basic_analysis is None:
                    print("📧 Step 1: Analyzing Problem 9.5...")
                    basic_analysis = analyzer.analyze_problem_9_5()
                
                if enhanced_analysis is None:
                    print("🔒 Step 2: Analyzing Problem 9.6...")
                    enhanced_analysis = analyzer.analyze_problem_9_6(basic_analysis)
                
                print("⚖️ Step 3: Comparing rule sets...")
                comparison = analyzer.compare_rule_sets(basic_analysis, enhanced_analysis)
                
                # Save all analyses
                basic_filename = f"complete_9_5_smtp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                enhanced_filename = f"complete_9_6_smtp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                comparison_filename = f"smtp_comparison_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                analyzer.save_analysis(basic_analysis, basic_filename)
                analyzer.save_analysis(enhanced_analysis, enhanced_filename)
                analyzer.save_analysis(comparison, comparison_filename)
                
                # Generate combined report
                combined_report = (analyzer.generate_report(basic_analysis) + 
                                 "\n" + analyzer.generate_report(enhanced_analysis) + 
                                 "\n" + analyzer.generate_report(comparison))
                
                report_filename = f"complete_smtp_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(combined_report)
                print(f"📄 Complete analysis report generated: {report_filename}")
                
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