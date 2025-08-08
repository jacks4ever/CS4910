#!/usr/bin/env python3
"""
CS4910 Lab 3: Database Security Analysis Tool
Interactive script for analyzing database security and normalization
"""

import json
import datetime
from typing import Dict, List, Tuple

class DatabaseSecurityAnalyzer:
    def __init__(self):
        self.normalization_problems = [
            "Data redundancy",
            "Update anomalies", 
            "Insert anomalies",
            "Delete anomalies",
            "Storage inefficiency",
            "Data inconsistency"
        ]
        
    def analyze_table_problems(self) -> Dict:
        """Analyze problems in an unnormalized table"""
        print("\n📊 Database Table Problem Analysis")
        print("=" * 40)
        
        analysis = {
            'type': 'table_analysis',
            'timestamp': datetime.datetime.now().isoformat(),
            'table_description': '',
            'identified_problems': [],
            'normalization_solution': {},
            'security_implications': {}
        }
        
        # Get table description
        print("Describe the table structure and data:")
        analysis['table_description'] = input("Table description: ")
        
        # Identify problems
        print(f"\n🔍 Problem Identification")
        print("Common database problems:")
        for i, problem in enumerate(self.normalization_problems, 1):
            print(f"{i}. {problem}")
        
        problem_indices = input("\nWhich problems exist? (enter numbers, comma-separated): ")
        try:
            indices = [int(x.strip()) - 1 for x in problem_indices.split(',')]
            analysis['identified_problems'] = [self.normalization_problems[i] for i in indices if 0 <= i < len(self.normalization_problems)]
        except ValueError:
            print("Invalid input, no problems recorded.")
        
        # Additional problems
        additional = input("Any additional problems not listed? ")
        if additional:
            analysis['identified_problems'].append(additional)
        
        # Normalization solution
        print(f"\n🛠️ Normalization Solution")
        table_count = int(input("How many tables in your normalized solution? "))
        
        for i in range(table_count):
            table_name = input(f"Table {i+1} name: ")
            columns = input(f"Columns in {table_name} (comma-separated): ")
            primary_key = input(f"Primary key for {table_name}: ")
            
            analysis['normalization_solution'][table_name] = {
                'columns': [c.strip() for c in columns.split(',')],
                'primary_key': primary_key,
                'relationships': input(f"Relationships for {table_name}: ")
            }
        
        # Security implications
        print(f"\n🔐 Security Analysis")
        analysis['security_implications']['access_control'] = input("How does normalization affect access control? ")
        analysis['security_implications']['data_integrity'] = input("How does it improve data integrity? ")
        analysis['security_implications']['confidentiality'] = input("Impact on data confidentiality? ")
        
        return analysis
    
    def analyze_privilege_scenario(self) -> Dict:
        """Analyze complex privilege granting/revocation scenarios"""
        print("\n🔑 Privilege Scenario Analysis")
        print("=" * 35)
        
        scenario = {
            'type': 'privilege_scenario',
            'timestamp': datetime.datetime.now().isoformat(),
            'users': [],
            'privileges': [],
            'grant_graph': {},
            'revocation_events': [],
            'cascade_analysis': {}
        }
        
        # Define users and privileges
        users = input("Enter all users (comma-separated): ").split(',')
        privileges = input("Enter all privileges (comma-separated): ").split(',')
        
        scenario['users'] = [u.strip() for u in users]
        scenario['privileges'] = [p.strip() for p in privileges]
        
        # Build grant graph
        print(f"\n📈 Grant Relationship Mapping")
        for user in scenario['users']:
            scenario['grant_graph'][user] = {}
            for privilege in scenario['privileges']:
                grantor = input(f"Who granted {privilege} to {user}? (or 'none'): ")
                if grantor.lower() != 'none':
                    grant_time = input(f"When was {privilege} granted to {user}? (t=X): ")
                    grant_option = input(f"Was {privilege} granted to {user} with grant option? (y/n): ").lower() == 'y'
                    
                    scenario['grant_graph'][user][privilege] = {
                        'grantor': grantor,
                        'time': grant_time,
                        'grant_option': grant_option
                    }
        
        # Revocation events
        print(f"\n🔄 Revocation Events")
        revocation_count = int(input("How many revocation events to analyze? "))
        
        for i in range(revocation_count):
            print(f"\nRevocation Event {i+1}:")
            event = {
                'revoker': input("Who is revoking? "),
                'revokee': input("From whom? "),
                'privilege': input("Which privilege? "),
                'time': input("When? (t=X): "),
                'cascade': input("Cascade or restrict? ").lower()
            }
            scenario['revocation_events'].append(event)
        
        # Cascade analysis
        print(f"\n📊 Cascade Effect Analysis")
        scenario['cascade_analysis']['affected_users'] = input("Which users are affected by cascading? ").split(',')
        scenario['cascade_analysis']['affected_privileges'] = input("Which privileges are revoked due to cascading? ").split(',')
        scenario['cascade_analysis']['reasoning'] = input("Explain the cascade reasoning: ")
        
        return scenario
    
    def generate_privilege_diagram(self, scenario: Dict) -> str:
        """Generate text-based privilege relationship diagram"""
        diagram = "# Privilege Relationship Diagram\n\n"
        diagram += "## Grant Relationships\n\n"
        
        for user, privileges in scenario['grant_graph'].items():
            if privileges:
                diagram += f"### {user}\n"
                for privilege, details in privileges.items():
                    grant_option_text = " (with grant option)" if details['grant_option'] else ""
                    diagram += f"- {privilege}: granted by {details['grantor']} at {details['time']}{grant_option_text}\n"
                diagram += "\n"
        
        diagram += "## Revocation Events\n\n"
        for i, event in enumerate(scenario['revocation_events'], 1):
            diagram += f"{i}. {event['revoker']} revokes {event['privilege']} from {event['revokee']} at {event['time']} ({event['cascade']})\n"
        
        diagram += "\n## Cascade Effects\n\n"
        if scenario['cascade_analysis']['affected_users']:
            diagram += f"Affected users: {', '.join(scenario['cascade_analysis']['affected_users'])}\n"
            diagram += f"Revoked privileges: {', '.join(scenario['cascade_analysis']['affected_privileges'])}\n"
            diagram += f"Reasoning: {scenario['cascade_analysis']['reasoning']}\n"
        
        return diagram
    
    def save_analysis(self, analysis: Dict, filename: str):
        """Save analysis to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {filename}")

def main():
    analyzer = DatabaseSecurityAnalyzer()
    
    print("📊 CS4910 Lab 3: Database Security Analysis Tool")
    print("=" * 50)
    
    options = [
        "Analyze Table Normalization Problems",
        "Analyze Privilege Scenarios",
        "Exit"
    ]
    
    while True:
        print("\nAnalysis Options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("\nSelect an option (1-3): "))
            
            if choice == 1:
                analysis = analyzer.analyze_table_problems()
                filename = f"table_analysis_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(analysis, filename)
                
                # Generate summary report
                print(f"\n📋 Analysis Summary:")
                print(f"Problems identified: {len(analysis['identified_problems'])}")
                print(f"Normalized tables: {len(analysis['normalization_solution'])}")
                
            elif choice == 2:
                scenario = analyzer.analyze_privilege_scenario()
                filename = f"privilege_scenario_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                analyzer.save_analysis(scenario, filename)
                
                # Generate privilege diagram
                diagram = analyzer.generate_privilege_diagram(scenario)
                diagram_filename = f"privilege_diagram_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(diagram_filename, 'w') as f:
                    f.write(diagram)
                print(f"📊 Privilege diagram saved to {diagram_filename}")
                
            elif choice == 3:
                print("👋 Goodbye!")
                break
                
            else:
                print("Please enter a number between 1 and 3.")
                
        except ValueError:
            print("Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()