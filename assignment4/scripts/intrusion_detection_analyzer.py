#!/usr/bin/env python3
"""
CS4910 Lab 4: Tripwire Intrusion Detection Analysis Tool
Specifically for Lab 4 Textbook Problem 8.6 - Tripwire HIDS Analysis
"""

import json
import datetime
import hashlib
import os
from typing import Dict, List, Tuple

class IntrusionDetectionAnalyzer:
    def __init__(self):
        self.ids_types = {
            'hids': 'Host-based Intrusion Detection System',
            'nids': 'Network-based Intrusion Detection System',
            'hybrid': 'Hybrid Intrusion Detection System'
        }
        
        self.file_categories = {
            'static': 'Files that rarely change',
            'dynamic': 'Files that change frequently',
            'log': 'Log files (append-only)',
            'config': 'Configuration files',
            'executable': 'Executable files'
        }
        
    def analyze_tripwire_system(self) -> Dict:
        """Analyze Tripwire IDS system"""
        print("\n🔍 Tripwire IDS Analysis")
        print("=" * 30)
        
        analysis = {
            'system_type': 'tripwire_hids',
            'timestamp': datetime.datetime.now().isoformat(),
            'advantages': [],
            'disadvantages': [],
            'configuration_challenges': {},
            'file_categories': {},
            'hash_function_analysis': {},
            'operational_considerations': {}
        }
        
        # Analyze advantages
        print("📈 Tripwire Advantages Analysis:")
        print("Common advantages of file integrity monitoring:")
        advantages_list = [
            "Detects unauthorized file modifications",
            "Provides audit trail for compliance",
            "Helps with forensic investigation",
            "Monitors critical system files",
            "Detects insider threats",
            "Provides real-time alerting"
        ]
        
        for i, advantage in enumerate(advantages_list, 1):
            print(f"{i}. {advantage}")
        
        selected_advantages = input("\nSelect advantages (comma-separated numbers): ")
        try:
            indices = [int(x.strip()) - 1 for x in selected_advantages.split(',')]
            analysis['advantages'] = [advantages_list[i] for i in indices if 0 <= i < len(advantages_list)]
        except ValueError:
            analysis['advantages'] = advantages_list[:3]  # Default selection
        
        additional_advantages = input("Any additional advantages? ")
        if additional_advantages:
            analysis['advantages'].append(additional_advantages)
        
        # Analyze disadvantages
        print(f"\n📉 Tripwire Disadvantages Analysis:")
        disadvantages_list = [
            "High configuration complexity",
            "Significant administrative overhead",
            "Performance impact on system",
            "False positive management challenges",
            "Scalability limitations",
            "Storage requirements for checksums"
        ]
        
        for i, disadvantage in enumerate(disadvantages_list, 1):
            print(f"{i}. {disadvantage}")
        
        selected_disadvantages = input("\nSelect disadvantages (comma-separated numbers): ")
        try:
            indices = [int(x.strip()) - 1 for x in selected_disadvantages.split(',')]
            analysis['disadvantages'] = [disadvantages_list[i] for i in indices if 0 <= i < len(disadvantages_list)]
        except ValueError:
            analysis['disadvantages'] = disadvantages_list[:3]  # Default selection
        
        additional_disadvantages = input("Any additional disadvantages? ")
        if additional_disadvantages:
            analysis['disadvantages'].append(additional_disadvantages)
        
        # Configuration challenges
        print(f"\n⚙️ Configuration Challenges Analysis:")
        
        for category, description in self.file_categories.items():
            print(f"\n{category.upper()} FILES ({description}):")
            
            challenge = {
                'monitoring_frequency': input(f"  How often should {category} files be monitored? "),
                'change_policy': input(f"  What changes are acceptable for {category} files? "),
                'alert_threshold': input(f"  What should trigger alerts for {category} files? "),
                'examples': input(f"  Give examples of {category} files: ").split(',')
            }
            
            analysis['configuration_challenges'][category] = challenge
        
        # Hash function analysis
        print(f"\n🔐 Cryptographic Hash Function Analysis:")
        analysis['hash_function_analysis']['purpose'] = input("Why are hash functions used in Tripwire? ")
        analysis['hash_function_analysis']['security_properties'] = input("What security properties must the hash function have? ").split(',')
        analysis['hash_function_analysis']['attack_resistance'] = input("What attacks must the hash function resist? ").split(',')
        analysis['hash_function_analysis']['performance_considerations'] = input("What are the performance considerations? ")
        
        # Operational considerations
        print(f"\n🔧 Operational Considerations:")
        analysis['operational_considerations']['admin_workload'] = input("Describe the administrative workload: ")
        analysis['operational_considerations']['response_procedures'] = input("What procedures are needed for alert response? ")
        analysis['operational_considerations']['maintenance_requirements'] = input("What ongoing maintenance is required? ")
        analysis['operational_considerations']['integration_challenges'] = input("How does Tripwire integrate with other security tools? ")
        
        return analysis
    
    def simulate_file_integrity_monitoring(self) -> Dict:
        """Simulate file integrity monitoring process"""
        print("\n📁 File Integrity Monitoring Simulation")
        print("=" * 40)
        
        simulation = {
            'type': 'file_integrity_simulation',
            'timestamp': datetime.datetime.now().isoformat(),
            'monitored_files': {},
            'baseline_hashes': {},
            'monitoring_results': {},
            'alerts_generated': []
        }
        
        # Define files to monitor
        print("Define files to monitor:")
        file_count = int(input("How many files to simulate monitoring? "))
        
        for i in range(file_count):
            print(f"\nFile {i+1}:")
            file_info = {
                'path': input("File path: "),
                'category': input("File category (static/dynamic/log/config/executable): "),
                'criticality': input("Criticality level (1-5): "),
                'change_policy': input("Acceptable changes (none/append/modify): ")
            }
            
            file_id = f"file_{i+1}"
            simulation['monitored_files'][file_id] = file_info
            
            # Generate simulated baseline hash
            baseline_content = input(f"Simulated initial content for {file_info['path']}: ")
            baseline_hash = hashlib.sha256(baseline_content.encode()).hexdigest()
            simulation['baseline_hashes'][file_id] = {
                'hash': baseline_hash,
                'timestamp': datetime.datetime.now().isoformat(),
                'content': baseline_content
            }
        
        # Simulate monitoring checks
        print(f"\n🔍 Simulating Monitoring Checks:")
        
        for file_id, file_info in simulation['monitored_files'].items():
            print(f"\nChecking {file_info['path']}:")
            
            current_content = input(f"Current content (or press Enter for no change): ")
            if not current_content:
                current_content = simulation['baseline_hashes'][file_id]['content']
            
            current_hash = hashlib.sha256(current_content.encode()).hexdigest()
            baseline_hash = simulation['baseline_hashes'][file_id]['hash']
            
            monitoring_result = {
                'current_hash': current_hash,
                'baseline_hash': baseline_hash,
                'content_changed': current_hash != baseline_hash,
                'timestamp': datetime.datetime.now().isoformat()
            }
            
            simulation['monitoring_results'][file_id] = monitoring_result
            
            if monitoring_result['content_changed']:
                # Generate alert
                alert = {
                    'file_id': file_id,
                    'file_path': file_info['path'],
                    'alert_type': 'FILE_MODIFIED',
                    'severity': self.calculate_alert_severity(file_info),
                    'timestamp': datetime.datetime.now().isoformat(),
                    'details': {
                        'old_hash': baseline_hash,
                        'new_hash': current_hash,
                        'change_authorized': input(f"Is this change authorized for {file_info['path']}? (y/n): ").lower() == 'y'
                    }
                }
                
                simulation['alerts_generated'].append(alert)
                print(f"  🚨 ALERT: File modified - Severity: {alert['severity']}")
            else:
                print(f"  ✅ No changes detected")
        
        return simulation
    
    def calculate_alert_severity(self, file_info: Dict) -> str:
        """Calculate alert severity based on file characteristics"""
        criticality = int(file_info.get('criticality', 3))
        category = file_info.get('category', 'static')
        
        if criticality >= 4 and category in ['executable', 'config']:
            return 'HIGH'
        elif criticality >= 3:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def analyze_ids_deployment(self) -> Dict:
        """Analyze IDS deployment considerations"""
        print("\n🚀 IDS Deployment Analysis")
        print("=" * 30)
        
        deployment = {
            'type': 'ids_deployment',
            'timestamp': datetime.datetime.now().isoformat(),
            'environment_analysis': {},
            'deployment_strategy': {},
            'resource_requirements': {},
            'integration_plan': {}
        }
        
        # Environment analysis
        print("🏢 Environment Analysis:")
        deployment['environment_analysis']['organization_size'] = input("Organization size (small/medium/large): ")
        deployment['environment_analysis']['network_complexity'] = input("Network complexity (simple/moderate/complex): ")
        deployment['environment_analysis']['compliance_requirements'] = input("Compliance requirements: ").split(',')
        deployment['environment_analysis']['threat_level'] = input("Threat level (low/medium/high): ")
        
        # Deployment strategy
        print(f"\n📋 Deployment Strategy:")
        deployment['deployment_strategy']['ids_type'] = input("Primary IDS type (HIDS/NIDS/Hybrid): ")
        deployment['deployment_strategy']['coverage_scope'] = input("Coverage scope (critical systems/all systems): ")
        deployment['deployment_strategy']['monitoring_approach'] = input("Monitoring approach (real-time/batch/hybrid): ")
        deployment['deployment_strategy']['alert_management'] = input("Alert management strategy: ")
        
        # Resource requirements
        print(f"\n💰 Resource Requirements:")
        deployment['resource_requirements']['personnel'] = input("Personnel requirements: ")
        deployment['resource_requirements']['hardware'] = input("Hardware requirements: ")
        deployment['resource_requirements']['software'] = input("Software licensing needs: ")
        deployment['resource_requirements']['training'] = input("Training requirements: ")
        
        # Integration plan
        print(f"\n🔗 Integration Plan:")
        deployment['integration_plan']['siem_integration'] = input("SIEM integration approach: ")
        deployment['integration_plan']['incident_response'] = input("Incident response integration: ")
        deployment['integration_plan']['existing_tools'] = input("Integration with existing security tools: ")
        
        return deployment
    
    def save_analysis(self, analysis: Dict, filename: str):
        """Save analysis to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {filename}")
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a formatted report"""
        report_type = analysis.get('type', analysis.get('system_type', 'Unknown'))
        
        report = f"""
# Intrusion Detection System Analysis Report
Generated: {analysis['timestamp']}
Analysis Type: {report_type}

## Analysis Results

"""
        
        if analysis.get('system_type') == 'tripwire_hids':
            report += self.generate_tripwire_report(analysis)
        elif analysis.get('type') == 'file_integrity_simulation':
            report += self.generate_simulation_report(analysis)
        elif analysis.get('type') == 'ids_deployment':
            report += self.generate_deployment_report(analysis)
        
        return report
    
    def generate_tripwire_report(self, analysis: Dict) -> str:
        """Generate Tripwire analysis report"""
        report = "### Tripwire HIDS Analysis\n\n"
        
        report += "**Advantages**:\n"
        for advantage in analysis['advantages']:
            report += f"- {advantage}\n"
        
        report += "\n**Disadvantages**:\n"
        for disadvantage in analysis['disadvantages']:
            report += f"- {disadvantage}\n"
        
        report += "\n**Configuration Challenges**:\n"
        for category, challenge in analysis['configuration_challenges'].items():
            report += f"- **{category.upper()} files**: {challenge['change_policy']}\n"
        
        report += f"\n**Hash Function Role**: {analysis['hash_function_analysis']['purpose']}\n"
        
        return report
    
    def generate_simulation_report(self, analysis: Dict) -> str:
        """Generate file integrity simulation report"""
        report = "### File Integrity Monitoring Simulation\n\n"
        
        report += f"**Files Monitored**: {len(analysis['monitored_files'])}\n"
        report += f"**Alerts Generated**: {len(analysis['alerts_generated'])}\n\n"
        
        report += "**Alert Summary**:\n"
        for alert in analysis['alerts_generated']:
            report += f"- {alert['file_path']}: {alert['alert_type']} (Severity: {alert['severity']})\n"
        
        return report
    
    def generate_deployment_report(self, analysis: Dict) -> str:
        """Generate IDS deployment report"""
        report = "### IDS Deployment Analysis\n\n"
        
        report += f"**Organization Size**: {analysis['environment_analysis']['organization_size']}\n"
        report += f"**IDS Type**: {analysis['deployment_strategy']['ids_type']}\n"
        report += f"**Coverage Scope**: {analysis['deployment_strategy']['coverage_scope']}\n"
        
        return report

def main():
    analyzer = IntrusionDetectionAnalyzer()
    
    print("🔍 CS4910 Lab 4: Intrusion Detection System Analysis Tool")
    print("=" * 60)
    
    options = [
        "Tripwire HIDS Analysis",
        "File Integrity Monitoring Simulation",
        "IDS Deployment Analysis",
        "Exit"
    ]
    
    while True:
        print("\nAnalysis Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            if choice == 1:
                analysis = analyzer.analyze_tripwire_system()
                filename = f"tripwire_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(analysis, filename)
                
                # Generate report
                report = analyzer.generate_report(analysis)
                report_filename = f"tripwire_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 2:
                simulation = analyzer.simulate_file_integrity_monitoring()
                filename = f"file_integrity_sim_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(simulation, filename)
                
                # Generate report
                report = analyzer.generate_report(simulation)
                report_filename = f"file_integrity_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(report_filename, 'w') as f:
                    f.write(report)
                print(f"📄 Report generated: {report_filename}")
                
            elif choice == 3:
                deployment = analyzer.analyze_ids_deployment()
                filename = f"ids_deployment_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(deployment, filename)
                
                # Generate report
                report = analyzer.generate_report(deployment)
                report_filename = f"ids_deployment_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
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