#!/usr/bin/env python3
# incident_analysis.py - Interactive Security Incident Analysis Tool

import json
from datetime import datetime

class SecurityIncidentAnalyzer:
    def __init__(self):
        self.incident_data = {}
        self.security_properties = [
            "Confidentiality",
            "Integrity", 
            "Availability",
            "Authenticity",
            "Accountability"
        ]
    
    def get_incident_details(self):
        """Interactively collect incident details from user"""
        print("=" * 60)
        print("SECURITY INCIDENT DATA COLLECTION")
        print("=" * 60)
        
        # Get basic incident information
        title = input("Enter the incident title/name: ").strip()
        while not title:
            print("Please provide an incident title.")
            title = input("Enter the incident title/name: ").strip()
        
        date = input("Enter the incident date (YYYY-MM-DD or description): ").strip()
        while not date:
            print("Please provide the incident date.")
            date = input("Enter the incident date (YYYY-MM-DD or description): ").strip()
        
        print("\nProvide a brief description of what happened:")
        description = input("Description: ").strip()
        while not description:
            print("Please provide a description.")
            description = input("Description: ").strip()
        
        # Get news source
        source = input("Enter the news source URL or publication name: ").strip()
        while not source:
            print("Please provide a news source.")
            source = input("Enter the news source URL or publication name: ").strip()
        
        return title, date, description, source
    
    def get_affected_properties(self):
        """Interactively determine which security properties were affected"""
        print("\n" + "=" * 60)
        print("SECURITY PROPERTIES IMPACT ASSESSMENT")
        print("=" * 60)
        print("For each security property, indicate if it was affected by this incident:")
        print("Enter 'y' for yes, 'n' for no")
        
        affected_properties = []
        property_impacts = {}
        
        for prop in self.security_properties:
            while True:
                response = input(f"\nWas {prop} affected? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    affected_properties.append(prop)
                    # Get impact level for affected properties
                    impact = self.get_impact_level(prop)
                    property_impacts[prop] = impact
                    break
                elif response in ['n', 'no']:
                    property_impacts[prop] = 0
                    break
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
        
        return affected_properties, property_impacts
    
    def get_impact_level(self, property_name):
        """Get impact level for a specific security property"""
        print(f"\nRate the impact on {property_name} (1-5 scale):")
        print("1 = Minimal impact")
        print("2 = Low impact") 
        print("3 = Moderate impact")
        print("4 = High impact")
        print("5 = Severe impact")
        
        while True:
            try:
                impact = int(input(f"Impact level for {property_name}: "))
                if 1 <= impact <= 5:
                    return impact
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")
    
    def get_overall_impact(self):
        """Get overall incident impact assessment"""
        print("\n" + "=" * 60)
        print("OVERALL IMPACT ASSESSMENT")
        print("=" * 60)
        print("Rate the overall impact of this incident (1-5 scale):")
        print("1 = Minimal overall impact")
        print("2 = Low overall impact")
        print("3 = Moderate overall impact") 
        print("4 = High overall impact")
        print("5 = Severe overall impact")
        
        while True:
            try:
                impact = int(input("Overall impact level: "))
                if 1 <= impact <= 5:
                    return impact
                else:
                    print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")
    
    def analyze_incident_interactive(self):
        """Interactively analyze a security incident"""
        print("CS4910 Lab 1 - Interactive Security Incident Analysis Tool")
        print("=" * 60)
        print("This tool will help you analyze a security incident you've researched.")
        print("Make sure you have already researched an incident before starting.")
        
        # Collect incident details
        title, date, description, source = self.get_incident_details()
        
        # Assess affected properties
        affected_properties, property_impacts = self.get_affected_properties()
        
        # Get overall impact
        overall_impact = self.get_overall_impact()
        
        # Store analysis data
        self.incident_data = {
            'title': title,
            'date': date,
            'description': description,
            'source': source,
            'affected_properties': affected_properties,
            'property_impacts': property_impacts,
            'overall_impact': overall_impact,
            'analysis_date': datetime.now().isoformat()
        }
        
        # Display results
        self.display_analysis_results()
        
        return self.incident_data
    
    def display_analysis_results(self):
        """Display the analysis results"""
        data = self.incident_data
        
        print("\n" + "=" * 60)
        print("SECURITY INCIDENT ANALYSIS RESULTS")
        print("=" * 60)
        print(f"Incident: {data['title']}")
        print(f"Date: {data['date']}")
        print(f"Source: {data['source']}")
        print(f"Overall Impact: {data['overall_impact']}/5")
        print(f"\nDescription: {data['description']}")
        
        print(f"\nAffected Security Properties:")
        if data['affected_properties']:
            for prop in data['affected_properties']:
                impact_level = data['property_impacts'][prop]
                print(f"  - {prop}: Impact Level {impact_level}/5")
        else:
            print("  - No security properties were identified as affected")
        
        print(f"\nUnaffected Security Properties:")
        unaffected = [prop for prop in self.security_properties 
                     if prop not in data['affected_properties']]
        if unaffected:
            for prop in unaffected:
                print(f"  - {prop}")
        else:
            print("  - All security properties were affected")
        
        # Calculate statistics
        total_properties = len(self.security_properties)
        affected_count = len(data['affected_properties'])
        coverage = (affected_count / total_properties) * 100
        
        print(f"\nAnalysis Statistics:")
        print(f"Security Property Coverage: {coverage:.1f}% ({affected_count}/{total_properties})")
        
        # Calculate average impact for affected properties
        if data['affected_properties']:
            avg_impact = sum(data['property_impacts'][prop] for prop in data['affected_properties']) / len(data['affected_properties'])
            print(f"Average Impact Level (affected properties): {avg_impact:.1f}/5")
    
    def save_analysis(self, filename="incident_analysis_results.txt"):
        """Save analysis results to formatted plaintext file"""
        if not self.incident_data:
            print("No incident data to save")
            return
        
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs("../outputs/incident", exist_ok=True)
        output_file = f"../outputs/incident/{filename}"
        
        # Create formatted plaintext content
        content = []
        content.append("=" * 80)
        content.append("CS4910 Lab 1 - Security Incident Analysis Results")
        content.append("=" * 80)
        content.append(f"Analysis Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
        content.append("")
        
        # Incident Overview
        content.append("INCIDENT OVERVIEW")
        content.append("-" * 40)
        content.append(f"Title: {self.incident_data.get('title', 'N/A')}")
        content.append(f"Date: {self.incident_data.get('date', 'N/A')}")
        content.append(f"Source: {self.incident_data.get('source', 'N/A')}")
        content.append("")
        
        content.append("INCIDENT DESCRIPTION:")
        content.append(self.incident_data.get('description', 'N/A'))
        content.append("")
        
        # CIA Impact Analysis
        content.append("CIA TRIAD IMPACT ANALYSIS")
        content.append("-" * 40)
        
        cia_analysis = self.incident_data.get('cia_analysis', {})
        
        content.append("CONFIDENTIALITY IMPACT:")
        conf = cia_analysis.get('confidentiality', {})
        content.append(f"  Impact Level: {conf.get('impact', 'N/A')}")
        content.append(f"  Explanation: {conf.get('explanation', 'N/A')}")
        content.append("")
        
        content.append("INTEGRITY IMPACT:")
        integ = cia_analysis.get('integrity', {})
        content.append(f"  Impact Level: {integ.get('impact', 'N/A')}")
        content.append(f"  Explanation: {integ.get('explanation', 'N/A')}")
        content.append("")
        
        content.append("AVAILABILITY IMPACT:")
        avail = cia_analysis.get('availability', {})
        content.append(f"  Impact Level: {avail.get('impact', 'N/A')}")
        content.append(f"  Explanation: {avail.get('explanation', 'N/A')}")
        content.append("")
        
        # Additional Security Properties
        content.append("ADDITIONAL SECURITY PROPERTIES")
        content.append("-" * 40)
        
        content.append("AUTHENTICITY IMPACT:")
        auth = cia_analysis.get('authenticity', {})
        content.append(f"  Impact Level: {auth.get('impact', 'N/A')}")
        content.append(f"  Explanation: {auth.get('explanation', 'N/A')}")
        content.append("")
        
        content.append("ACCOUNTABILITY IMPACT:")
        acc = cia_analysis.get('accountability', {})
        content.append(f"  Impact Level: {acc.get('impact', 'N/A')}")
        content.append(f"  Explanation: {acc.get('explanation', 'N/A')}")
        content.append("")
        
        # Overall Assessment
        content.append("OVERALL ASSESSMENT")
        content.append("-" * 40)
        content.append(f"Primary Security Properties Affected: {', '.join(self.incident_data.get('primary_impacts', []))}")
        content.append(f"Overall Severity: {self.incident_data.get('overall_severity', 'N/A')}")
        content.append("")
        
        content.append("KEY LESSONS LEARNED:")
        lessons = self.incident_data.get('lessons_learned', 'N/A')
        content.append(lessons)
        content.append("")
        
        content.append("=" * 80)
        content.append("End of Security Incident Analysis")
        content.append("=" * 80)
        
        # Save to file
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(content))
            print(f"\nAnalysis results saved to {output_file}")
            print("You can copy and paste this content directly into your Word document.")
        except FileNotFoundError:
            # Fallback to current directory
            with open(filename, 'w') as f:
                f.write('\n'.join(content))
            print(f"\nAnalysis results saved to {filename}")
            print("You can copy and paste this content directly into your Word document.")

def main():
    analyzer = SecurityIncidentAnalyzer()
    
    # Run interactive analysis
    analyzer.analyze_incident_interactive()
    
    # Save results
    analyzer.save_analysis()
    
    print("\n" + "=" * 60)
    print("Analysis complete! Your results are ready for your lab report.")
    print("Your detailed analysis has been saved to incident_analysis_results.txt")
    print("You can copy and paste the content directly into your Word document.")
    print("=" * 60)
    
    # AI-Enhanced Learning Suggestions
    print("\n" + "=" * 70)
    print("🤖 AI-ENHANCED LEARNING SUGGESTIONS")
    print("=" * 70)
    print("Use AI to deepen your incident analysis with these prompts:")
    print("\n1. ROOT CAUSE ANALYSIS:")
    print('   "What are the typical root causes of [type of incident]?"')
    print('   "How could this incident have been prevented?"')
    print("\n2. BROADER IMPLICATIONS:")
    print('   "What are the long-term impacts of this type of security incident"')
    print('   "on organizations and society?"')
    print("\n3. COMPARATIVE ANALYSIS:")
    print('   "Compare this incident to similar ones. What patterns emerge?"')
    print('   "How has the industry response to these incidents evolved?"')
    print("\n4. TECHNICAL DEEP DIVE:")
    print('   "Explain the technical details of how [attack method] works"')
    print('   "What security controls could have detected this attack?"')
    print("\n5. VERIFICATION:")
    print('   "Review my incident analysis: [paste summary]. What additional"')
    print('   "security properties or impacts should I consider?"')
    print("\n💡 Remember: Use AI to enhance understanding, not replace analysis!")
    print("   Document all AI interactions in your lab report.")
    print("=" * 70)

if __name__ == "__main__":
    main()