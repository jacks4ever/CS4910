#!/usr/bin/env python3
"""
CS4910 Lab 3: Access Control Analysis Tool
Interactive script for analyzing DAC, RBAC, and ABAC systems
"""

import json
import datetime
from typing import Dict, List, Tuple

class AccessControlAnalyzer:
    def __init__(self):
        self.models = {
            'DAC': 'Discretionary Access Control',
            'RBAC': 'Role-Based Access Control', 
            'ABAC': 'Attribute-Based Access Control'
        }
        
    def analyze_dac_system(self) -> Dict:
        """Analyze a DAC system"""
        print("\n🔐 DAC System Analysis")
        print("=" * 30)
        
        analysis = {
            'model': 'DAC',
            'timestamp': datetime.datetime.now().isoformat(),
            'subjects': [],
            'objects': [],
            'access_matrix': {},
            'security_analysis': {}
        }
        
        # Get subjects and objects
        subjects = input("Enter subjects (comma-separated): ").split(',')
        objects = input("Enter objects (comma-separated): ").split(',')
        
        analysis['subjects'] = [s.strip() for s in subjects]
        analysis['objects'] = [o.strip() for o in objects]
        
        # Build access matrix
        print("\n📊 Building Access Matrix")
        for subject in analysis['subjects']:
            analysis['access_matrix'][subject] = {}
            for obj in analysis['objects']:
                rights = input(f"Access rights for {subject} on {obj} (r/w/x, comma-separated): ")
                analysis['access_matrix'][subject][obj] = [r.strip() for r in rights.split(',') if r.strip()]
        
        # Security analysis
        print("\n🛡️ Security Analysis")
        analysis['security_analysis']['strengths'] = input("DAC strengths in this scenario: ")
        analysis['security_analysis']['weaknesses'] = input("DAC weaknesses in this scenario: ")
        analysis['security_analysis']['vulnerabilities'] = input("Potential vulnerabilities: ")
        
        return analysis
    
    def design_abac_policy(self) -> Dict:
        """Design ABAC policies"""
        print("\n🎯 ABAC Policy Design")
        print("=" * 25)
        
        policy = {
            'model': 'ABAC',
            'timestamp': datetime.datetime.now().isoformat(),
            'attributes': {
                'subject': [],
                'object': [],
                'environment': [],
                'action': []
            },
            'rules': [],
            'advantages': []
        }
        
        # Define attributes
        print("\n📋 Define Attributes")
        for attr_type in policy['attributes'].keys():
            attrs = input(f"Enter {attr_type} attributes (comma-separated): ")
            policy['attributes'][attr_type] = [a.strip() for a in attrs.split(',') if a.strip()]
        
        # Define policy rules
        print("\n📜 Define Policy Rules")
        rule_count = int(input("How many policy rules to define? "))
        
        for i in range(rule_count):
            print(f"\nRule {i+1}:")
            rule = {
                'id': i+1,
                'condition': input("Rule condition: "),
                'action': input("Allowed action: "),
                'effect': input("Effect (permit/deny): ")
            }
            policy['rules'].append(rule)
        
        # ABAC advantages
        print("\n✅ ABAC Advantages")
        advantages = input("List ABAC advantages (comma-separated): ")
        policy['advantages'] = [a.strip() for a in advantages.split(',') if a.strip()]
        
        return policy
    
    def analyze_database_privileges(self) -> Dict:
        """Analyze database privilege scenarios"""
        print("\n📊 Database Privilege Analysis")
        print("=" * 35)
        
        analysis = {
            'type': 'database_privileges',
            'timestamp': datetime.datetime.now().isoformat(),
            'users': [],
            'privileges': [],
            'grant_events': [],
            'revocation_analysis': {}
        }
        
        # Define users and privileges
        users = input("Enter users (comma-separated): ").split(',')
        privileges = input("Enter privileges (comma-separated): ").split(',')
        
        analysis['users'] = [u.strip() for u in users]
        analysis['privileges'] = [p.strip() for p in privileges]
        
        # Grant events
        print("\n📅 Grant Events")
        event_count = int(input("How many grant events to record? "))
        
        for i in range(event_count):
            print(f"\nGrant Event {i+1}:")
            event = {
                'grantor': input("Grantor: "),
                'grantee': input("Grantee: "),
                'privilege': input("Privilege: "),
                'timestamp': input("Time (t=X): "),
                'grant_option': input("With grant option? (y/n): ").lower() == 'y'
            }
            analysis['grant_events'].append(event)
        
        # Revocation analysis
        print("\n🔄 Revocation Analysis")
        analysis['revocation_analysis']['revoked_by'] = input("Who issued revocation? ")
        analysis['revocation_analysis']['revoked_from'] = input("Revoked from whom? ")
        analysis['revocation_analysis']['cascade_effects'] = input("Describe cascade effects: ")
        
        return analysis
    
    def save_analysis(self, analysis: Dict, filename: str):
        """Save analysis to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {filename}")
    
    def generate_visualization_data(self, analysis: Dict) -> str:
        """Generate data for creating visualizations"""
        if analysis.get('model') == 'DAC':
            viz_data = "# DAC Directed Graph Data\n\n"
            viz_data += "## Nodes\n"
            for subject in analysis['subjects']:
                viz_data += f"- {subject} (subject)\n"
            for obj in analysis['objects']:
                viz_data += f"- {obj} (object)\n"
            
            viz_data += "\n## Edges\n"
            for subject, objects in analysis['access_matrix'].items():
                for obj, rights in objects.items():
                    if rights:
                        viz_data += f"- {subject} -> {obj} [{', '.join(rights)}]\n"
            
            return viz_data
        
        return "Visualization data not available for this analysis type."

def main():
    analyzer = AccessControlAnalyzer()
    
    print("🔐 CS4910 Lab 3: Access Control Analysis Tool")
    print("=" * 45)
    
    options = [
        "DAC System Analysis",
        "ABAC Policy Design", 
        "Database Privilege Analysis",
        "Exit"
    ]
    
    while True:
        print("\nAnalysis Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nSelect an option (1-4): "))
            
            if choice == 1:
                analysis = analyzer.analyze_dac_system()
                filename = f"dac_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(analysis, filename)
                
                # Generate visualization data
                viz_data = analyzer.generate_visualization_data(analysis)
                viz_filename = f"dac_visualization_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(viz_filename, 'w') as f:
                    f.write(viz_data)
                print(f"📊 Visualization data saved to {viz_filename}")
                
            elif choice == 2:
                policy = analyzer.design_abac_policy()
                filename = f"abac_policy_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(policy, filename)
                
            elif choice == 3:
                analysis = analyzer.analyze_database_privileges()
                filename = f"db_privileges_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(analysis, filename)
                
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