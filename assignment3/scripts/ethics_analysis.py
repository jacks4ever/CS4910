#!/usr/bin/env python3
"""
CS4910 Lab 3: Ethics Analysis Tool
Interactive script for analyzing ethical scenarios using DFEI principles
"""

import json
import datetime
from typing import Dict, List

class EthicsAnalyzer:
    def __init__(self):
        self.dfei_principles = {
            'integrity': 'Intellectual honesty and authentic behavior',
            'trust': 'Building and maintaining trust relationships',
            'fairness': 'Equitable treatment and justice',
            'responsibility': 'Duty to prevent harm and act responsibly',
            'social_impact': 'Broader societal implications and consequences'
        }
        
    def analyze_scenario(self, scenario_name: str) -> Dict:
        """Interactive analysis of an ethical scenario"""
        print(f"\n🤝 Ethics Analysis: {scenario_name}")
        print("=" * 50)
        
        analysis = {
            'scenario': scenario_name,
            'timestamp': datetime.datetime.now().isoformat(),
            'principles': {}
        }
        
        for principle, description in self.dfei_principles.items():
            print(f"\n🔍 Analyzing: {principle.upper()}")
            print(f"Definition: {description}")
            
            # Get user analysis
            user_analysis = input(f"\nHow does {principle} apply to this scenario? ")
            arguments = input(f"What are the key arguments regarding {principle}? ")
            rating = self.get_rating(f"Rate the importance of {principle} in this scenario (1-5): ")
            
            analysis['principles'][principle] = {
                'analysis': user_analysis,
                'arguments': arguments,
                'importance_rating': rating
            }
            
        return analysis
    
    def get_rating(self, prompt: str) -> int:
        """Get a valid rating from 1-5"""
        while True:
            try:
                rating = int(input(prompt))
                if 1 <= rating <= 5:
                    return rating
                else:
                    print("Please enter a rating between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")
    
    def save_analysis(self, analysis: Dict, filename: str):
        """Save analysis to JSON file"""
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"\n✅ Analysis saved to {filename}")
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate a formatted report"""
        report = f"""
# Ethics Analysis Report: {analysis['scenario']}
Generated: {analysis['timestamp']}

## DFEI Principles Analysis

"""
        for principle, data in analysis['principles'].items():
            report += f"""
### {principle.upper()} (Importance: {data['importance_rating']}/5)

**Analysis**: {data['analysis']}

**Key Arguments**: {data['arguments']}

---
"""
        return report

def main():
    analyzer = EthicsAnalyzer()
    
    print("🤝 CS4910 Lab 3: Ethics Analysis Tool")
    print("=====================================")
    
    scenarios = [
        "Dr. Stefan Savage's Car Hacking Disclosure",
        "Personal Ethical Dilemma",
        "Course Project Ethics",
        "Custom Scenario"
    ]
    
    print("\nAvailable scenarios:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario}")
    
    while True:
        try:
            choice = int(input("\nSelect a scenario to analyze (1-4): "))
            if 1 <= choice <= 4:
                if choice == 4:
                    scenario_name = input("Enter your custom scenario name: ")
                else:
                    scenario_name = scenarios[choice - 1]
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Perform analysis
    analysis = analyzer.analyze_scenario(scenario_name)
    
    # Save results
    filename = f"ethics_analysis_{scenario_name.lower().replace(' ', '_')}.json"
    analyzer.save_analysis(analysis, filename)
    
    # Generate report
    report = analyzer.generate_report(analysis)
    report_filename = f"ethics_report_{scenario_name.lower().replace(' ', '_')}.md"
    with open(report_filename, 'w') as f:
        f.write(report)
    
    print(f"📄 Report generated: {report_filename}")
    
    # Summary
    print(f"\n📊 Analysis Summary for {scenario_name}:")
    for principle, data in analysis['principles'].items():
        print(f"  {principle.upper()}: {data['importance_rating']}/5")

if __name__ == "__main__":
    main()