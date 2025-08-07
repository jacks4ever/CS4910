#!/usr/bin/env python3
"""
CS4910 Lab 4: DoS Attack Calculator
Specifically for Lab 4 Textbook Problems 7.1 and 7.3 - DoS and DDoS Attack Calculations
"""

import json
import datetime
import math
from typing import Dict, List, Tuple

class DoSCalculator:
    def __init__(self):
        self.bits_per_byte = 8
        self.mbps_to_bps = 1_000_000
        self.kbps_to_bps = 1_000
        
    def calculate_problem_7_1(self) -> Dict:
        """Calculate Problem 7.1 - Classic DoS Flood Attack"""
        print("\n📊 Problem 7.1: Classic DoS Flood Attack Calculation")
        print("=" * 55)
        
        calculation = {
            'problem': '7.1',
            'problem_type': 'classic_dos_flood',
            'timestamp': datetime.datetime.now().isoformat(),
            'scenario': {
                'attack_type': 'ICMP echo request (ping) packets',
                'target_link': '8-Mbps',
                'packet_sizes': [100, 1000, 1460],  # bytes
                'overhead_ignored': True
            },
            'calculations': {},
            'analysis': {}
        }
        
        print("📋 Scenario:")
        print("   - Attack Type: ICMP echo request (ping) packets")
        print("   - Target Link: 8-Mbps")
        print("   - Packet Sizes: 100, 1000, 1460 bytes")
        print("   - Overhead: Ignored (as specified)")
        
        # Convert target bandwidth to bits per second
        target_bandwidth_mbps = 8
        target_bandwidth_bps = target_bandwidth_mbps * self.mbps_to_bps
        
        print(f"\n🧮 Calculations:")
        print(f"   Target bandwidth: {target_bandwidth_mbps} Mbps = {target_bandwidth_bps:,} bps")
        
        for packet_size_bytes in calculation['scenario']['packet_sizes']:
            print(f"\n   📦 {packet_size_bytes}-byte packets:")
            
            # Convert packet size to bits
            packet_size_bits = packet_size_bytes * self.bits_per_byte
            print(f"      Packet size: {packet_size_bytes} bytes = {packet_size_bits} bits")
            
            # Calculate packets per second needed
            packets_per_second = target_bandwidth_bps / packet_size_bits
            packets_per_second_rounded = math.ceil(packets_per_second)
            
            print(f"      Packets needed: {target_bandwidth_bps:,} bps ÷ {packet_size_bits} bits = {packets_per_second:.2f} packets/second")
            print(f"      Rounded up: {packets_per_second_rounded:,} packets/second")
            
            calculation['calculations'][f'{packet_size_bytes}_bytes'] = {
                'packet_size_bytes': packet_size_bytes,
                'packet_size_bits': packet_size_bits,
                'packets_per_second_exact': packets_per_second,
                'packets_per_second_rounded': packets_per_second_rounded,
                'calculation_formula': f"{target_bandwidth_bps} bps ÷ {packet_size_bits} bits/packet"
            }
        
        # Analysis questions
        print(f"\n📈 Analysis Questions:")
        calculation['analysis']['most_efficient_packet_size'] = input("Which packet size is most efficient for the attacker? ")
        calculation['analysis']['efficiency_reasoning'] = input("Why is this packet size most efficient? ")
        calculation['analysis']['practical_considerations'] = input("What practical considerations affect attack implementation? ")
        calculation['analysis']['defense_implications'] = input("How can defenders use this information? ")
        
        return calculation
    
    def calculate_problem_7_3(self) -> Dict:
        """Calculate Problem 7.3 - Distributed DoS Attack"""
        print("\n🌐 Problem 7.3: Distributed DoS Attack Calculation")
        print("=" * 50)
        
        calculation = {
            'problem': '7.3',
            'problem_type': 'distributed_dos',
            'timestamp': datetime.datetime.now().isoformat(),
            'scenario': {
                'zombie_bandwidth': '256 kbps uplink',
                'target_link': '8-Mbps',
                'packet_sizes': [100, 1000, 1500],  # bytes
                'attack_type': 'ICMP echo request packets'
            },
            'zombie_calculations': {},
            'attack_requirements': {},
            'botnet_analysis': {}
        }
        
        print("📋 Scenario:")
        print("   - Zombie Systems: Compromised residential PCs")
        print("   - Zombie Bandwidth: 256 kbps uplink each")
        print("   - Target Link: 8-Mbps")
        print("   - Packet Sizes: 100, 1000, 1500 bytes")
        
        # Convert bandwidths
        zombie_bandwidth_kbps = 256
        zombie_bandwidth_bps = zombie_bandwidth_kbps * self.kbps_to_bps
        target_bandwidth_mbps = 8
        target_bandwidth_bps = target_bandwidth_mbps * self.mbps_to_bps
        
        print(f"\n🧮 Bandwidth Conversions:")
        print(f"   Zombie bandwidth: {zombie_bandwidth_kbps} kbps = {zombie_bandwidth_bps:,} bps")
        print(f"   Target bandwidth: {target_bandwidth_mbps} Mbps = {target_bandwidth_bps:,} bps")
        
        # Calculate for each packet size
        for packet_size_bytes in calculation['scenario']['packet_sizes']:
            print(f"\n   📦 {packet_size_bytes}-byte packets:")
            
            # Convert packet size to bits
            packet_size_bits = packet_size_bytes * self.bits_per_byte
            
            # Calculate maximum packets per second per zombie
            zombie_packets_per_second = zombie_bandwidth_bps / packet_size_bits
            zombie_packets_per_second_rounded = math.floor(zombie_packets_per_second)
            
            print(f"      Single zombie capacity: {zombie_bandwidth_bps:,} bps ÷ {packet_size_bits} bits = {zombie_packets_per_second:.2f} packets/second")
            print(f"      Rounded down: {zombie_packets_per_second_rounded:,} packets/second per zombie")
            
            # Calculate total packets needed to flood target
            total_packets_needed = target_bandwidth_bps / packet_size_bits
            
            # Calculate number of zombies needed
            zombies_needed = math.ceil(total_packets_needed / zombie_packets_per_second)
            
            print(f"      Total packets needed: {target_bandwidth_bps:,} bps ÷ {packet_size_bits} bits = {total_packets_needed:.2f} packets/second")
            print(f"      Zombies needed: {total_packets_needed:.2f} ÷ {zombie_packets_per_second:.2f} = {zombies_needed:,} zombies")
            
            calculation['zombie_calculations'][f'{packet_size_bytes}_bytes'] = {
                'packet_size_bytes': packet_size_bytes,
                'packet_size_bits': packet_size_bits,
                'zombie_packets_per_second': zombie_packets_per_second,
                'zombie_packets_per_second_rounded': zombie_packets_per_second_rounded
            }
            
            calculation['attack_requirements'][f'{packet_size_bytes}_bytes'] = {
                'total_packets_needed': total_packets_needed,
                'zombies_needed': zombies_needed,
                'calculation_formula': f"ceil({total_packets_needed:.2f} ÷ {zombie_packets_per_second:.2f})"
            }
        
        # Botnet scaling analysis
        self.analyze_botnet_scaling(calculation)
        
        return calculation
    
    def analyze_botnet_scaling(self, calculation: Dict):
        """Analyze botnet scaling implications"""
        print(f"\n🔍 Botnet Scaling Analysis:")
        
        # Get botnet size input
        typical_botnet_size = input("Enter a typical botnet size (e.g., 10000): ")
        try:
            botnet_size = int(typical_botnet_size)
        except ValueError:
            botnet_size = 10000  # Default
        
        calculation['botnet_analysis']['botnet_size'] = botnet_size
        calculation['botnet_analysis']['multiple_targets'] = {}
        
        print(f"   Analyzing botnet with {botnet_size:,} zombies:")
        
        for packet_size in [100, 1000, 1500]:
            zombies_needed = calculation['attack_requirements'][f'{packet_size}_bytes']['zombies_needed']
            
            # Calculate how many simultaneous targets
            simultaneous_targets = botnet_size // zombies_needed
            remaining_zombies = botnet_size % zombies_needed
            
            print(f"      {packet_size}-byte packets: Can attack {simultaneous_targets} targets simultaneously")
            print(f"         ({remaining_zombies} zombies remaining)")
            
            calculation['botnet_analysis']['multiple_targets'][f'{packet_size}_bytes'] = {
                'simultaneous_targets': simultaneous_targets,
                'remaining_zombies': remaining_zombies,
                'utilization_percentage': (simultaneous_targets * zombies_needed / botnet_size) * 100
            }
        
        # Analysis questions
        print(f"\n📈 Strategic Analysis:")
        calculation['botnet_analysis']['multiple_orgs_capability'] = input("Can this botnet attack multiple organizations simultaneously? How? ")
        calculation['botnet_analysis']['large_org_threat'] = input("What about major organizations with larger network links? ")
        calculation['botnet_analysis']['scaling_implications'] = input("What are the implications of botnet scaling? ")
    
    def compare_dos_vs_ddos(self, dos_calc: Dict, ddos_calc: Dict) -> Dict:
        """Compare DoS vs DDoS attack requirements"""
        print("\n⚖️ DoS vs DDoS Comparison Analysis")
        print("=" * 35)
        
        comparison = {
            'analysis_type': 'dos_vs_ddos_comparison',
            'timestamp': datetime.datetime.now().isoformat(),
            'dos_requirements': {},
            'ddos_requirements': {},
            'comparison_analysis': {}
        }
        
        # Extract key data for comparison
        for packet_size in [100, 1000]:  # Common sizes in both problems
            if packet_size == 1460:  # 7.1 has 1460, 7.3 has 1500
                packet_size_ddos = 1500
            else:
                packet_size_ddos = packet_size
            
            dos_key = f'{packet_size}_bytes'
            ddos_key = f'{packet_size_ddos}_bytes'
            
            if dos_key in dos_calc['calculations'] and ddos_key in ddos_calc['attack_requirements']:
                dos_packets = dos_calc['calculations'][dos_key]['packets_per_second_rounded']
                ddos_zombies = ddos_calc['attack_requirements'][ddos_key]['zombies_needed']
                
                comparison['dos_requirements'][dos_key] = {
                    'single_attacker_packets_needed': dos_packets,
                    'feasibility': 'High bandwidth requirement for single attacker'
                }
                
                comparison['ddos_requirements'][ddos_key] = {
                    'zombies_needed': ddos_zombies,
                    'distributed_advantage': 'Lower bandwidth per zombie, harder to block'
                }
                
                print(f"📊 {packet_size}-byte packets:")
                print(f"   DoS: Single attacker needs {dos_packets:,} packets/second")
                print(f"   DDoS: Needs {ddos_zombies:,} zombies at 256 kbps each")
                print(f"   DDoS total bandwidth: {ddos_zombies * 256:,} kbps = {(ddos_zombies * 256)/1000:.1f} Mbps")
        
        # Analysis questions
        print(f"\n🤔 Comparison Analysis:")
        comparison['comparison_analysis']['attack_feasibility'] = input("Which attack type is more feasible and why? ")
        comparison['comparison_analysis']['defense_difficulty'] = input("Which is harder to defend against and why? ")
        comparison['comparison_analysis']['detection_differences'] = input("How do detection methods differ between DoS and DDoS? ")
        
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
# DoS Attack Calculation Report
Generated: {analysis['timestamp']}
Problem: {problem}
Type: {problem_type}

## Analysis Results

"""
        
        if problem == '7.1':
            report += self.generate_problem_7_1_report(analysis)
        elif problem == '7.3':
            report += self.generate_problem_7_3_report(analysis)
        elif problem_type == 'dos_vs_ddos_comparison':
            report += self.generate_comparison_report(analysis)
        
        return report
    
    def generate_problem_7_1_report(self, analysis: Dict) -> str:
        """Generate Problem 7.1 report"""
        report = "### Problem 7.1: Classic DoS Flood Attack\n\n"
        report += f"**Scenario**: {analysis['scenario']['attack_type']} against {analysis['scenario']['target_link']} link\n\n"
        
        report += "**Calculations**:\n"
        for packet_key, calc in analysis['calculations'].items():
            report += f"- **{calc['packet_size_bytes']}-byte packets**: {calc['packets_per_second_rounded']:,} packets/second\n"
            report += f"  - Formula: {calc['calculation_formula']}\n"
            report += f"  - Exact: {calc['packets_per_second_exact']:.2f} packets/second\n\n"
        
        if 'analysis' in analysis:
            report += "**Analysis**:\n"
            report += f"- Most efficient packet size: {analysis['analysis'].get('most_efficient_packet_size', 'N/A')}\n"
            report += f"- Reasoning: {analysis['analysis'].get('efficiency_reasoning', 'N/A')}\n"
        
        return report
    
    def generate_problem_7_3_report(self, analysis: Dict) -> str:
        """Generate Problem 7.3 report"""
        report = "### Problem 7.3: Distributed DoS Attack\n\n"
        report += f"**Scenario**: Zombie systems with {analysis['scenario']['zombie_bandwidth']} attacking {analysis['scenario']['target_link']} link\n\n"
        
        report += "**Single Zombie Capacity**:\n"
        for packet_key, calc in analysis['zombie_calculations'].items():
            report += f"- **{calc['packet_size_bytes']}-byte packets**: {calc['zombie_packets_per_second_rounded']:,} packets/second per zombie\n"
        
        report += "\n**Attack Requirements**:\n"
        for packet_key, req in analysis['attack_requirements'].items():
            packet_size = packet_key.split('_')[0]
            report += f"- **{packet_size}-byte packets**: {req['zombies_needed']:,} zombies needed\n"
        
        if 'botnet_analysis' in analysis:
            report += f"\n**Botnet Analysis** (with {analysis['botnet_analysis']['botnet_size']:,} zombies):\n"
            for packet_key, targets in analysis['botnet_analysis']['multiple_targets'].items():
                packet_size = packet_key.split('_')[0]
                report += f"- **{packet_size}-byte packets**: Can attack {targets['simultaneous_targets']} targets simultaneously\n"
        
        return report
    
    def generate_comparison_report(self, analysis: Dict) -> str:
        """Generate DoS vs DDoS comparison report"""
        report = "### DoS vs DDoS Comparison\n\n"
        
        report += "**Single DoS Requirements**:\n"
        for packet_key, req in analysis['dos_requirements'].items():
            packet_size = packet_key.split('_')[0]
            report += f"- **{packet_size}-byte packets**: {req['single_attacker_packets_needed']:,} packets/second\n"
        
        report += "\n**Distributed DDoS Requirements**:\n"
        for packet_key, req in analysis['ddos_requirements'].items():
            packet_size = packet_key.split('_')[0]
            report += f"- **{packet_size}-byte packets**: {req['zombies_needed']:,} zombies needed\n"
        
        return report

def main():
    calculator = DoSCalculator()
    
    print("📊 CS4910 Lab 4: DoS Attack Calculator")
    print("=" * 40)
    print("This tool helps with Lab 4 Textbook Problems 7.1 and 7.3")
    
    options = [
        "Calculate Problem 7.1 (Classic DoS Flood)",
        "Calculate Problem 7.3 (Distributed DoS)",
        "Compare DoS vs DDoS (Both Problems)",
        "Exit"
    ]
    
    dos_calc = None
    ddos_calc = None
    
    while True:
        print("\nCalculation Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            if choice == 1:
                dos_calc = calculator.calculate_problem_7_1()
                filename = f"problem_7_1_calculation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                calculator.save_analysis(dos_calc, filename)
                
                # Generate report
                report = calculator.generate_report(dos_calc)
                report_filename = f"problem_7_1_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 2:
                ddos_calc = calculator.calculate_problem_7_3()
                filename = f"problem_7_3_calculation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                calculator.save_analysis(ddos_calc, filename)
                
                # Generate report
                report = calculator.generate_report(ddos_calc)
                report_filename = f"problem_7_3_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 3:
                if dos_calc is None:
                    print("📊 First, let's calculate Problem 7.1:")
                    dos_calc = calculator.calculate_problem_7_1()
                
                if ddos_calc is None:
                    print("📊 Now, let's calculate Problem 7.3:")
                    ddos_calc = calculator.calculate_problem_7_3()
                
                # Generate comparison
                comparison = calculator.compare_dos_vs_ddos(dos_calc, ddos_calc)
                filename = f"dos_vs_ddos_comparison_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                calculator.save_analysis(comparison, filename)
                
                # Generate combined report
                combined_report = (calculator.generate_report(dos_calc) + 
                                 "\n" + calculator.generate_report(ddos_calc) + 
                                 "\n" + calculator.generate_report(comparison))
                
                report_filename = f"complete_dos_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
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