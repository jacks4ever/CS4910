#!/usr/bin/env python3
# cia_analysis.py - Interactive CIA Triad Analysis Tool

import json
import sys
from datetime import datetime

def get_rating_input(aspect, scenario):
    """Get a valid rating (1-5) from user input"""
    while True:
        try:
            rating = int(input(f"Rate {aspect} importance for {scenario} (1-5, 5=highest): "))
            if 1 <= rating <= 5:
                return rating
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")

def get_justification_input(aspect, scenario):
    """Get justification text from user input"""
    print(f"\nExplain your {aspect} rating for {scenario}:")
    justification = input("Justification: ").strip()
    while not justification:
        print("Please provide a justification.")
        justification = input("Justification: ").strip()
    return justification

def analyze_scenario_interactive(scenario_name):
    """
    Interactively analyze a scenario for CIA requirements
    """
    print(f"\n{'='*60}")
    print(f"ANALYZING: {scenario_name}")
    print(f"{'='*60}")
    
    # Get ratings
    confidentiality = get_rating_input("Confidentiality", scenario_name)
    integrity = get_rating_input("Integrity", scenario_name)
    availability = get_rating_input("Availability", scenario_name)
    
    # Get justifications
    print(f"\nNow provide justifications for your ratings:")
    conf_justification = get_justification_input("confidentiality", scenario_name)
    int_justification = get_justification_input("integrity", scenario_name)
    avail_justification = get_justification_input("availability", scenario_name)
    
    justification = {
        'confidentiality': conf_justification,
        'integrity': int_justification,
        'availability': avail_justification
    }
    
    # Display analysis results
    print(f"\n=== CIA Analysis Results: {scenario_name} ===")
    print(f"Confidentiality: {confidentiality}/5 - {justification['confidentiality']}")
    print(f"Integrity: {integrity}/5 - {justification['integrity']}")
    print(f"Availability: {availability}/5 - {justification['availability']}")
    
    # Calculate risk score
    total_score = confidentiality + integrity + availability
    risk_level = "Low" if total_score <= 8 else "Medium" if total_score <= 12 else "High"
    print(f"Overall Risk Level: {risk_level} (Score: {total_score}/15)")
    
    return {
        'scenario': scenario_name,
        'scores': {
            'confidentiality': confidentiality,
            'integrity': integrity,
            'availability': availability
        },
        'justification': justification,
        'risk_level': risk_level,
        'total_score': total_score
    }

def save_analysis_results(results, filename="cia_analysis_results.txt"):
    """Save analysis results to formatted plaintext file"""
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs("../outputs/cia", exist_ok=True)
    output_file = f"../outputs/cia/{filename}"
    
    # Create formatted plaintext content
    content = []
    content.append("=" * 80)
    content.append("CS4910 Lab 1 - CIA Triad Analysis Results")
    content.append("=" * 80)
    content.append(f"Analysis Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    content.append("")
    
    for i, result in enumerate(results, 1):
        content.append(f"SCENARIO {i}: {result['scenario'].upper()}")
        content.append("-" * 60)
        content.append("")
        
        # CIA Analysis
        content.append("CONFIDENTIALITY ANALYSIS:")
        content.append(f"  Rating: {result['scores']['confidentiality']}/5")
        content.append("")
        
        content.append("INTEGRITY ANALYSIS:")
        content.append(f"  Rating: {result['scores']['integrity']}/5")
        content.append("")
        
        content.append("AVAILABILITY ANALYSIS:")
        content.append(f"  Rating: {result['scores']['availability']}/5")
        content.append("")
        
        content.append("STUDENT JUSTIFICATION:")
        content.append(f"  {result['justification']}")
        content.append("")
        
        content.append(f"OVERALL RISK ASSESSMENT:")
        content.append(f"  Total Score: {result['total_score']}/15")
        content.append(f"  Risk Level: {result['risk_level']}")
        content.append("")
        content.append("=" * 60)
        content.append("")
    
    # Summary section
    content.append("ANALYSIS SUMMARY")
    content.append("=" * 40)
    for result in results:
        content.append(f"• {result['scenario']}: {result['risk_level']} Risk (Score: {result['total_score']}/15)")
    
    content.append("")
    content.append("=" * 80)
    content.append("End of CIA Triad Analysis")
    content.append("=" * 80)
    
    # Save to file
    try:
        with open(output_file, 'w') as f:
            f.write('\n'.join(content))
        print(f"\nResults saved to {output_file}")
        print("You can copy and paste this content directly into your Word document.")
    except FileNotFoundError:
        # Fallback to current directory if outputs/cia doesn't exist
        with open(filename, 'w') as f:
            f.write('\n'.join(content))
        print(f"\nResults saved to {filename}")
        print("You can copy and paste this content directly into your Word document.")

def main():
    print("CS4910 Lab 1 - Interactive CIA Triad Analysis Tool")
    print("=" * 60)
    print("You will analyze 5 scenarios for CIA Triad requirements.")
    print("For each scenario, rate the importance of Confidentiality, Integrity, and Availability.")
    print("Use the scale: 1=Very Low, 2=Low, 3=Medium, 4=High, 5=Very High")
    
    scenarios = [
        "ATM System",
        "DNS System", 
        "Implanted Defibrillator",
        "Online Voting System",
        "Automated Metro Train System"
    ]
    
    results = []
    
    for scenario in scenarios:
        analysis = analyze_scenario_interactive(scenario)
        results.append(analysis)
        
        # Ask if user wants to continue
        if scenario != scenarios[-1]:  # Not the last scenario
            print(f"\nCompleted analysis for {scenario}")
            continue_input = input("Press Enter to continue to the next scenario, or 'q' to quit: ").strip().lower()
            if continue_input == 'q':
                print("Analysis incomplete. Exiting...")
                return
    
    # Save results
    save_analysis_results(results)
    
    # Summary
    print(f"\n{'='*60}")
    print("ANALYSIS SUMMARY")
    print(f"{'='*60}")
    for result in results:
        print(f"{result['scenario']}: {result['risk_level']} Risk (Score: {result['total_score']}/15)")
    
    print(f"\n{'='*60}")
    print("Analysis complete! Your results are ready for your lab report.")
    print("Your detailed results have been saved to cia_analysis_results.txt")
    print("You can copy and paste the content directly into your Word document.")
    print(f"{'='*60}")
    
    # AI-Enhanced Learning Suggestions
    print("\n" + "=" * 70)
    print("🤖 AI-ENHANCED LEARNING SUGGESTIONS")
    print("=" * 70)
    print("Use AI to deepen your understanding with these prompts:")
    print("\n1. CONCEPT CLARIFICATION:")
    print('   "Explain the CIA Triad in cybersecurity using simple analogies"')
    print('   "What are real-world examples of confidentiality vs privacy?"')
    print("\n2. SCENARIO EXPANSION:")
    print('   "Generate 3 more examples of systems where availability is more"')
    print('   "important than confidentiality, and explain why"')
    print("\n3. CRITICAL THINKING:")
    print('   "What are the trade-offs between the three CIA principles?"')
    print('   "How do modern cloud systems balance CIA requirements?"')
    print("\n4. VERIFICATION:")
    print('   "Review my CIA analysis: [paste your results]. Are my"')
    print('   "priority rankings reasonable? What did I miss?"')
    print("\n💡 Remember: Use AI to enhance understanding, not replace analysis!")
    print("   Document all AI interactions in your lab report.")
    print("=" * 70)

if __name__ == "__main__":
    main()