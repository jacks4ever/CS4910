# CS 4910: Introduction to Computer Security
## Lab Assignment 1: Security Fundamentals and AWS Environment Setup
**Fall 2025 Semester**  
**University of Colorado Colorado Springs**  
**Instructor: Rhett Saunders**

---

## Lab Overview

This is the first of several lab assignments in CS 4910. In this lab, you will:
1. Set up a secure AWS virtual machine environment
2. Explore fundamental security concepts including the CIA Triad
3. Analyze real-world security incidents
4. Investigate cryptographic hash functions and their properties
5. Examine public-key certificates and digital signatures
6. Use automated scripts to validate your understanding

**Estimated Time:** 4-6 hours  
**Due Date:** [To be announced by instructor]

---

## Learning Objectives

By the end of this lab, you will be able to:
- Set up and configure a secure AWS EC2 instance for security research
- Apply the CIA Triad (Confidentiality, Integrity, Availability) to real-world systems
- Analyze security incidents using established security frameworks
- Understand hash function properties and collision resistance
- Examine and validate digital certificates
- Use command-line tools for security analysis

---

## Prerequisites

- Basic understanding of computer networks and operating systems
- AWS account with educational credits (provided by instructor)
- SSH client (PuTTY for Windows, Terminal for Mac/Linux)
- Web browser with developer tools
- Access to AI tools (ChatGPT, Claude, Gemini, or similar) for research and analysis assistance

## AI Integration Philosophy

This lab integrates AI tools as research assistants and analysis partners. You are encouraged to:
- Use AI to research security concepts and current threats
- Validate your analysis with AI-powered insights
- Generate additional test cases and scenarios
- Enhance your understanding through AI-guided exploration
- Document your AI interactions as part of your learning process

**Note**: While AI assistance is encouraged, your final analysis and conclusions must demonstrate your own understanding and critical thinking.

---

## Part 1: AWS Environment Setup (20 points)

### 1.1 Theory: Cloud Security Fundamentals

Before setting up your AWS environment, it's important to understand the shared responsibility model in cloud computing:

- **AWS Responsibility**: Physical security, infrastructure, hypervisor security
- **Your Responsibility**: Operating system security, application security, data encryption, network configuration

### 1.2 Setting Up Your AWS EC2 Instance

1. **Launch EC2 Instance**:
   - AMI: Ubuntu 24.04 LTS
   - Instance Type: t3.micro (free tier eligible)
   - Security Group: Create a new security group named "CS4910-Lab1-SG"
   - Key Pair: Create and download a new key pair named "CS4910-Lab1-Key"

2. **Security Group Configuration**:
   ```
   Inbound Rules:
   - SSH (22): Your IP only
   - HTTP (80): Anywhere (for web server testing)
   - HTTPS (443): Anywhere (for certificate analysis)
   
   Outbound Rules:
   - All traffic: Anywhere (default)
   ```

3. **Connect to Your Instance**:
   ```bash
   chmod 400 CS4910-Lab1-Key.pem
   ssh -i CS4910-Lab1-Key.pem ubuntu@[YOUR-INSTANCE-IP]
   ```

### 1.3 Install Required Tools

Run the setup script to install necessary tools:

```bash
#!/bin/bash
# CS4910 Lab 1 Setup Script for Ubuntu 24.04
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget openssl python3 python3-pip python3-venv git vim
python3 -m pip install --user requests beautifulsoup4 cryptography
```

**Deliverable 1.1**: Screenshot of successful SSH connection to your EC2 instance showing the Ubuntu welcome message and your instance's IP address.

---

## Part 2: CIA Triad Analysis (25 points)

### 2.1 Theory: The CIA Triad

The CIA Triad forms the foundation of information security:

- **Confidentiality**: Ensuring information is accessible only to authorized individuals
- **Integrity**: Maintaining accuracy and completeness of data
- **Availability**: Ensuring information and resources are accessible when needed

Additional concepts:
- **Authenticity**: Verifying the identity of users and data sources
- **Accountability**: Ensuring actions can be traced to responsible parties

### 2.2 Practical Analysis with AI Assistance

For each scenario below, analyze the CIA requirements and use the provided script to validate your understanding.

**AI Integration Steps:**
1. **Research Phase**: Use AI to research each system type and understand its security requirements
2. **Analysis Phase**: Discuss your initial CIA assessment with AI to identify potential gaps
3. **Validation Phase**: Use AI to generate additional scenarios or edge cases to test your understanding
4. **Documentation Phase**: Have AI help you articulate your reasoning clearly

**AI Prompt Example:**
```
"I'm analyzing an ATM system for CIA Triad requirements. Can you help me understand:
1. What are the primary confidentiality concerns for ATM systems?
2. What integrity failures could occur and their impact?
3. How critical is availability for ATM operations?
4. Are there any security aspects I might be overlooking?"
```

Create and run the CIA analysis script:

```python
#!/usr/bin/env python3
# cia_analysis.py - CIA Triad Analysis Tool

import json
import sys

def analyze_scenario(scenario_name, confidentiality, integrity, availability, justification):
    """
    Analyze a scenario for CIA requirements
    
    Args:
        scenario_name: Name of the scenario
        confidentiality: Importance level (1-5, 5 being highest)
        integrity: Importance level (1-5, 5 being highest)  
        availability: Importance level (1-5, 5 being highest)
        justification: Dictionary with explanations for each rating
    """
    
    print(f"\n=== CIA Analysis: {scenario_name} ===")
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
        'risk_level': risk_level
    }

# Example usage and template
if __name__ == "__main__":
    # Template for student analysis
    scenarios = [
        "ATM System",
        "DNS System", 
        "Implanted Defibrillator",
        "Online Voting System",
        "Automated Metro Train"
    ]
    
    print("CS4910 Lab 1 - CIA Triad Analysis Tool")
    print("Complete your analysis for each scenario:")
    
    for scenario in scenarios:
        print(f"\n--- Analyze: {scenario} ---")
        print("Rate each aspect from 1-5 (5 = highest importance)")
        # Students will modify this section with their analysis
```

### 2.3 Scenario Analysis

**Complete the following analyses using the script above:**

a. **Automated Teller Machine (ATM)**
b. **Domain Name System (DNS)**
c. **Implanted Defibrillator**
d. **Online Voting System**
e. **Automated Metro Train System**

**Deliverable 2.1**: For each scenario, provide:
- CIA importance ratings (1-5 scale)
- Detailed justification for each rating
- Screenshot of script output
- Discussion of which aspect is most critical and why

---

## Part 3: Security Incident Analysis (20 points)

### 3.1 Theory: Security Incident Framework

When analyzing security incidents, consider:
- **Attack Vector**: How the attack was carried out
- **Impact Assessment**: Which security properties were violated
- **Root Cause**: Underlying vulnerabilities that enabled the attack
- **Mitigation**: Steps taken to address the incident

### 3.2 Incident Research and Analysis with AI

**AI-Enhanced Research Process:**
1. **Incident Discovery**: Use AI to find recent, relevant security incidents
2. **Technical Analysis**: Have AI explain technical details and attack vectors
3. **Impact Assessment**: Discuss with AI how the incident affects CIA+AA properties
4. **Lessons Learned**: Use AI to identify broader security implications

**AI Research Prompts:**
```
"Find me a recent security incident involving [specific technology/industry]. 
I need details about:
1. What happened and when?
2. What attack vectors were used?
3. Which security properties (CIA, authenticity, accountability) were compromised?
4. What were the business and technical impacts?
5. What lessons can be learned for prevention?"
```

**AI Analysis Prompts:**
```
"I'm analyzing the [incident name]. Can you help me understand:
1. The technical details of how this attack worked?
2. Which CIA Triad elements were most severely impacted?
3. How could this have been prevented?
4. What are the broader implications for the industry?"
```

Use the provided script to structure your incident analysis:

```python
#!/usr/bin/env python3
# incident_analysis.py - Security Incident Analysis Tool

import requests
import json
from datetime import datetime

class SecurityIncidentAnalyzer:
    def __init__(self):
        self.incident_data = {}
    
    def analyze_incident(self, title, date, description, affected_properties, impact_level):
        """
        Analyze a security incident
        
        Args:
            title: Incident title
            date: Date of incident
            description: Brief description
            affected_properties: List of affected security properties
            impact_level: Scale 1-5 (5 = highest impact)
        """
        
        self.incident_data = {
            'title': title,
            'date': date,
            'description': description,
            'affected_properties': affected_properties,
            'impact_level': impact_level,
            'analysis_date': datetime.now().isoformat()
        }
        
        print(f"\n=== Security Incident Analysis ===")
        print(f"Incident: {title}")
        print(f"Date: {date}")
        print(f"Impact Level: {impact_level}/5")
        print(f"\nDescription: {description}")
        print(f"\nAffected Security Properties:")
        
        for prop in affected_properties:
            print(f"  - {prop}")
        
        return self.incident_data
    
    def generate_report(self):
        """Generate a formatted analysis report"""
        if not self.incident_data:
            print("No incident data to report")
            return
            
        print(f"\n=== INCIDENT ANALYSIS REPORT ===")
        print(f"Generated: {self.incident_data['analysis_date']}")
        print(f"Incident: {self.incident_data['title']}")
        print(f"Overall Impact: {self.incident_data['impact_level']}/5")
        
        # Calculate affected property percentages
        total_properties = 5  # CIA + Authenticity + Accountability
        affected_count = len(self.incident_data['affected_properties'])
        coverage = (affected_count / total_properties) * 100
        
        print(f"Security Property Coverage: {coverage:.1f}% ({affected_count}/{total_properties})")

# Example usage
if __name__ == "__main__":
    analyzer = SecurityIncidentAnalyzer()
    
    print("CS4910 Lab 1 - Security Incident Analysis Tool")
    print("Research a recent security incident and analyze it using this framework")
```

### 3.3 Assignment Requirements

1. **Research**: Find a recent security incident (within the last 2 years) from a reputable news source
2. **Analysis**: Use the script to analyze which security properties were affected
3. **Report**: Write 2-3 paragraphs explaining the incident and its security implications

**Deliverable 3.1**: 
- Link to news source
- Completed incident analysis using the script
- Written analysis (2-3 paragraphs) explaining the incident and affected security properties
- Screenshot of script output

---

## Part 4: Hash Function Investigation (25 points)

### 4.1 Theory: Cryptographic Hash Functions

Hash functions are fundamental to modern cryptography. Key properties include:

- **Deterministic**: Same input always produces same output
- **Fixed Output Size**: Regardless of input size
- **Avalanche Effect**: Small input changes cause large output changes
- **One-way Function**: Computationally infeasible to reverse

**Collision Resistance Types**:
- **Weak Collision Resistance (Second Preimage Resistance)**: Given x, hard to find x' where H(x) = H(x')
- **Strong Collision Resistance**: Hard to find any x, x' where H(x) = H(x')

### 4.2 Hash Function Analysis with AI Exploration

**AI-Guided Learning Process:**
1. **Concept Exploration**: Use AI to deepen understanding of hash function properties
2. **Mathematical Analysis**: Have AI explain the mathematics behind collision resistance
3. **Real-world Applications**: Explore with AI how hash functions are used in practice
4. **Attack Scenarios**: Discuss potential vulnerabilities and attack methods

**AI Learning Prompts:**
```
"I'm studying cryptographic hash functions. Can you help me understand:
1. Why is the avalanche effect important for security?
2. What's the mathematical basis for the birthday paradox?
3. How do MD5 vulnerabilities demonstrate weak collision resistance?
4. What are practical applications where hash function security is critical?"
```

**AI Experiment Prompts:**
```
"I want to understand hash collisions better. Can you:
1. Explain why finding collisions becomes easier as we test more inputs?
2. Help me design experiments to demonstrate the avalanche effect?
3. Suggest ways to visualize the birthday paradox?
4. Explain the security implications of different hash algorithms?"
```

### 4.3 Hash Function Analysis Script

```python
#!/usr/bin/env python3
# hash_analysis.py - Hash Function Analysis Tool

import hashlib
import random
import string
import time
from collections import defaultdict

class HashAnalyzer:
    def __init__(self):
        self.algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    
    def hash_string(self, data, algorithm='sha256'):
        """Hash a string using specified algorithm"""
        hasher = hashlib.new(algorithm)
        hasher.update(data.encode('utf-8'))
        return hasher.hexdigest()
    
    def demonstrate_avalanche_effect(self, base_string="Hello World"):
        """Demonstrate how small changes affect hash output"""
        print(f"\n=== Avalanche Effect Demonstration ===")
        print(f"Base string: '{base_string}'")
        
        base_hash = self.hash_string(base_string)
        print(f"SHA256 Hash: {base_hash}")
        
        # Small modifications
        modifications = [
            base_string + "!",  # Add character
            base_string.replace("H", "h"),  # Change case
            base_string.replace(" ", "_"),  # Replace character
            base_string[:-1]  # Remove character
        ]
        
        for i, modified in enumerate(modifications):
            mod_hash = self.hash_string(modified)
            print(f"\nModification {i+1}: '{modified}'")
            print(f"SHA256 Hash: {mod_hash}")
            
            # Calculate bit differences
            diff_bits = bin(int(base_hash, 16) ^ int(mod_hash, 16)).count('1')
            total_bits = len(base_hash) * 4  # Each hex digit = 4 bits
            diff_percentage = (diff_bits / total_bits) * 100
            
            print(f"Bit differences: {diff_bits}/{total_bits} ({diff_percentage:.1f}%)")
    
    def birthday_attack_simulation(self, hash_bits=16):
        """Simulate birthday attack on truncated hash"""
        print(f"\n=== Birthday Attack Simulation ===")
        print(f"Using {hash_bits}-bit truncated SHA256")
        
        hash_map = {}
        attempts = 0
        max_attempts = 2 ** (hash_bits + 2)  # Reasonable upper limit
        
        start_time = time.time()
        
        while attempts < max_attempts:
            # Generate random string
            random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            
            # Get truncated hash
            full_hash = self.hash_string(random_string)
            truncated_hash = full_hash[:hash_bits//4]  # Convert bits to hex digits
            
            if truncated_hash in hash_map:
                end_time = time.time()
                print(f"Collision found after {attempts} attempts!")
                print(f"String 1: '{hash_map[truncated_hash]}'")
                print(f"String 2: '{random_string}'")
                print(f"Truncated hash: {truncated_hash}")
                print(f"Time taken: {end_time - start_time:.2f} seconds")
                
                # Theoretical vs actual
                theoretical = 2 ** (hash_bits / 2)
                print(f"Theoretical attempts needed: ~{theoretical:.0f}")
                print(f"Actual attempts: {attempts}")
                return attempts
            
            hash_map[truncated_hash] = random_string
            attempts += 1
            
            if attempts % 1000 == 0:
                print(f"Attempts: {attempts}")
        
        print(f"No collision found after {attempts} attempts")
        return attempts

    def compare_algorithms(self, test_string="CS4910 Security Lab"):
        """Compare different hash algorithms"""
        print(f"\n=== Hash Algorithm Comparison ===")
        print(f"Input: '{test_string}'")
        
        for algo in self.algorithms:
            try:
                hash_value = self.hash_string(test_string, algo)
                print(f"{algo.upper()}: {hash_value}")
            except ValueError:
                print(f"{algo.upper()}: Not available")

# Example usage
if __name__ == "__main__":
    analyzer = HashAnalyzer()
    
    print("CS4910 Lab 1 - Hash Function Analysis")
    
    # Run demonstrations
    analyzer.demonstrate_avalanche_effect()
    analyzer.compare_algorithms()
    analyzer.birthday_attack_simulation(16)  # 16-bit for quick demo
```

### 4.3 Theoretical Questions

Answer the following questions and use the script to support your explanations:

a. **Collision Resistance**: Is it true that for all messages x, x' with x ≠ x', we have H(x) ≠ H(x')? Explain using the pigeonhole principle.

b. **Resistance Types**: Define and differentiate weak vs. strong collision resistance.

c. **Birthday Paradox**: Explain the birthday paradox and how it applies to hash function attacks.

d. **Attack Comparison**: Compare the difficulty of finding someone with Alice's birthday vs. finding any two people with the same birthday.

**Deliverable 4.1**:
- Answers to theoretical questions (a-d)
- Screenshots of script output for avalanche effect demonstration
- Results from birthday attack simulation
- Analysis of hash algorithm comparison

---

## Part 5: Public-Key Certificate Analysis (10 points)

### 5.1 Theory: Digital Certificates and PKI

Public Key Infrastructure (PKI) enables secure communication through:
- **Digital Certificates**: Bind public keys to identities
- **Certificate Authorities (CA)**: Trusted third parties that issue certificates
- **Certificate Chain**: Hierarchy of trust from root CA to end-entity certificates

### 5.2 Certificate Analysis with AI Understanding

**AI-Enhanced PKI Learning:**
1. **Concept Clarification**: Use AI to understand PKI concepts and certificate structures
2. **Trust Chain Analysis**: Have AI explain how certificate chains establish trust
3. **Security Implications**: Explore with AI what certificate vulnerabilities mean
4. **Real-world Context**: Discuss current PKI challenges and solutions

**AI PKI Prompts:**
```
"I'm analyzing SSL/TLS certificates. Can you help me understand:
1. How does the certificate chain of trust work?
2. What information is contained in an X.509 certificate?
3. Why are certificate fingerprints important for security?
4. What are the implications of certificate expiration or revocation?"
```

**AI Analysis Prompts:**
```
"I'm examining a certificate for [domain]. Can you explain:
1. What each field in the certificate means?
2. How to verify the certificate is legitimate?
3. What security risks exist if this certificate were compromised?
4. How browsers validate certificates during HTTPS connections?"
```

### 5.3 Certificate Analysis Script

```bash
#!/bin/bash
# certificate_analysis.sh - SSL/TLS Certificate Analysis Tool

DOMAIN="www.uccs.edu"
PORT="443"

echo "=== CS4910 Lab 1 - Certificate Analysis ==="
echo "Analyzing certificate for: $DOMAIN"

# Get certificate information
echo -e "\n=== Certificate Details ==="
openssl s_client -connect $DOMAIN:$PORT -servername $DOMAIN </dev/null 2>/dev/null | \
openssl x509 -noout -text

# Get certificate fingerprints
echo -e "\n=== Certificate Fingerprints ==="
CERT=$(openssl s_client -connect $DOMAIN:$PORT -servername $DOMAIN </dev/null 2>/dev/null | \
openssl x509)

echo "SHA-1 Fingerprint:"
echo "$CERT" | openssl x509 -noout -fingerprint -sha1

echo "SHA-256 Fingerprint:"
echo "$CERT" | openssl x509 -noout -fingerprint -sha256

# Get certificate dates
echo -e "\n=== Certificate Validity ==="
echo "$CERT" | openssl x509 -noout -dates

# Get certificate subject and issuer
echo -e "\n=== Certificate Identity ==="
echo "Subject:"
echo "$CERT" | openssl x509 -noout -subject

echo "Issuer:"
echo "$CERT" | openssl x509 -noout -issuer

# Certificate chain
echo -e "\n=== Certificate Chain ==="
openssl s_client -connect $DOMAIN:$PORT -servername $DOMAIN -showcerts </dev/null 2>/dev/null | \
grep -E "(subject=|issuer=)"
```

### 5.3 Certificate Investigation

Use the script above to analyze the UCCS website certificate and answer:

a. **Objective**: What is the purpose of the digital certificate?
b. **Fingerprint**: Find the SHA-1 fingerprint and identify the issuing CA
c. **Validity**: When was the certificate issued and when does it expire?
d. **Methodology**: Explain your analysis process and tools used

**Deliverable 5.1**:
- Screenshots of certificate analysis output
- Answers to questions (a-d)
- Discussion of certificate chain validation

---

## Submission Requirements

### File Structure
Create the following directory structure on your AWS instance:

```
~/CS4910-Lab1/
├── scripts/
│   ├── cia_analysis.py
│   ├── incident_analysis.py
│   ├── hash_analysis.py
│   └── certificate_analysis.sh
├── outputs/
│   ├── cia_results.txt
│   ├── incident_report.txt
│   ├── hash_analysis.txt
│   └── certificate_analysis.txt
├── screenshots/
│   ├── aws_connection.png
│   ├── cia_analysis.png
│   ├── incident_analysis.png
│   ├── hash_demo.png
│   └── certificate_analysis.png
├── ai_interactions/
│   ├── cia_ai_session.md
│   ├── incident_ai_research.md
│   ├── hash_ai_exploration.md
│   └── certificate_ai_analysis.md
└── lab_report.md
```

### Submission Checklist

- [ ] AWS EC2 instance properly configured and accessible
- [ ] All scripts executed successfully with output saved
- [ ] Screenshots captured for each major section
- [ ] Written analysis completed for all theoretical questions
- [ ] Security incident research and analysis completed
- [ ] Certificate analysis completed with proper documentation
- [ ] AI interaction logs and insights documented
- [ ] All files organized in required directory structure
- [ ] Comprehensive lab report summarizing findings and lessons learned

### Unified Grading Rubric (100 Points Total)

#### Technical Implementation (40 points)
- **AWS Environment Setup (10 points)**
  - Excellent (9-10): Instance properly configured, security groups correct, all tools installed
  - Good (7-8): Minor configuration issues, mostly functional
  - Satisfactory (5-6): Basic setup complete, some functionality missing
  - Needs Improvement (0-4): Major setup problems, non-functional environment

- **Script Execution and Results (15 points)**
  - Excellent (14-15): All scripts run successfully, outputs captured and analyzed
  - Good (11-13): Most scripts work, minor issues with outputs
  - Satisfactory (8-10): Scripts run with some errors, basic outputs obtained
  - Needs Improvement (0-7): Scripts fail to run or produce meaningful results

- **Tool Usage and Screenshots (15 points)**
  - Excellent (14-15): Professional screenshots, proper tool usage demonstrated
  - Good (11-13): Good screenshots, tools used correctly
  - Satisfactory (8-10): Basic screenshots, adequate tool usage
  - Needs Improvement (0-7): Poor screenshots, incorrect tool usage

#### Analysis and Understanding (35 points)
- **CIA Triad Analysis (15 points)**
  - Excellent (14-15): Thorough analysis, clear justifications, demonstrates deep understanding
  - Good (11-13): Good analysis, mostly correct justifications
  - Satisfactory (8-10): Basic analysis, adequate understanding shown
  - Needs Improvement (0-7): Poor analysis, misunderstanding of concepts

- **Security Incident Analysis (10 points)**
  - Excellent (9-10): Current incident, comprehensive analysis, clear security implications
  - Good (7-8): Good incident choice, solid analysis
  - Satisfactory (5-6): Adequate incident analysis, basic understanding
  - Needs Improvement (0-4): Poor incident choice or analysis

- **Hash Function and Certificate Analysis (10 points)**
  - Excellent (9-10): Clear understanding of concepts, thorough analysis
  - Good (7-8): Good grasp of concepts, adequate analysis
  - Satisfactory (5-6): Basic understanding, minimal analysis
  - Needs Improvement (0-4): Poor understanding, inadequate analysis

#### AI Integration and Learning (15 points)
- **AI Usage Documentation (8 points)**
  - Excellent (7-8): Detailed AI interaction logs, shows effective use of AI for learning
  - Good (5-6): Good AI usage documentation, some learning enhancement shown
  - Satisfactory (3-4): Basic AI usage documented
  - Needs Improvement (0-2): Minimal or no AI usage documentation

- **AI-Enhanced Insights (7 points)**
  - Excellent (6-7): AI interactions led to deeper understanding, novel insights generated
  - Good (4-5): AI helped improve analysis quality
  - Satisfactory (2-3): Basic AI assistance utilized
  - Needs Improvement (0-1): AI usage did not enhance learning

#### Communication and Documentation (10 points)
- **Lab Report Quality (10 points)**
  - Excellent (9-10): Clear, professional writing, comprehensive coverage, excellent organization
  - Good (7-8): Good writing quality, covers most requirements
  - Satisfactory (5-6): Adequate writing, meets basic requirements
  - Needs Improvement (0-4): Poor writing quality, incomplete coverage

**Total: 100 Points**

### Late Submission Policy
- 10% deduction per day late
- No submissions accepted after 1 week past due date

---

## Additional Resources

- [AWS EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [OpenSSL Documentation](https://www.openssl.org/docs/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [RFC 5280 - Internet X.509 PKI Certificate](https://tools.ietf.org/html/rfc5280)

---

## Academic Integrity

This is an individual assignment. While you may discuss concepts with classmates, all work submitted must be your own. Sharing scripts, outputs, or written analysis constitutes academic dishonesty.

---

**Questions?** Contact Instructor Rhett Saunders during office hours or via email.

*Last Updated: July 2025*