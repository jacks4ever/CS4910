# CS 4910: Introduction to Computer Security
## Lab Assignment 1 Report: Security Fundamentals and AWS Environment Setup
**Fall 2025 Semester**  
**University of Colorado Colorado Springs**  
**Instructor: Rhett Saunders**

---

**Student Name**: [Your Name]  
**Student ID**: [Your Student ID]  
**Date Submitted**: [Submission Date]  
**AI Tools Used**: [List AI tools used, e.g., "ChatGPT-4, Claude 3.5"]

---

## Executive Summary

[Write a 2-3 paragraph summary of what you accomplished in this lab, key findings, and lessons learned. This should be written last but appear first in your report.]

---

## Part 1: AWS Environment Setup

### 1.1 Instance Configuration

**AWS Instance Details:**
- Instance ID: [Your instance ID]
- Instance Type: [e.g., t3.micro]
- AMI: [e.g., Ubuntu 24.04 LTS]
- Region: [e.g., us-east-1]
- Public IP: [Your instance public IP]

**Security Group Configuration:**
```
[Paste your security group rules here]
Inbound Rules:
- SSH (22): [Your IP]/32
- HTTP (80): 0.0.0.0/0
- HTTPS (443): 0.0.0.0/0

Outbound Rules:
- All traffic: 0.0.0.0/0
```

### 1.2 Connection Verification

**Screenshot 1.1**: SSH Connection Success
[Insert screenshot showing successful SSH connection to your EC2 instance, including the Ubuntu welcome message and your instance's IP address]

**Tools Verification:**
```bash
# Paste output of tool verification commands
python3 --version
openssl version
pip3 list | grep -E "(requests|cryptography)"
```

### 1.3 Security Considerations

[Discuss the security measures you implemented during AWS setup. Consider:]
- Key pair management and permissions
- Security group configuration rationale
- Network access restrictions
- Any additional security measures taken

---

## Part 2: CIA Triad Analysis

### 2.1 Methodology

[Explain how you approached the CIA Triad analysis, including use of the provided script]

### 2.2 AI Integration Summary

**AI Tools Used**: [List specific AI tools used for this section]

**Key AI Interactions**:
- [Summarize how AI helped you understand CIA concepts]
- [Describe any insights gained through AI discussions]
- [Note any AI-generated scenarios or examples that enhanced your learning]

**AI-Enhanced Learning Outcomes**:
[Describe how AI usage improved your understanding of the CIA Triad beyond what you would have achieved independently]

### 2.3 Scenario Analyses

#### 2.3.1 Automated Teller Machine (ATM)

**CIA Ratings:**
- Confidentiality: [X]/5
- Integrity: [X]/5  
- Availability: [X]/5

**Justification:**
- **Confidentiality**: [Your detailed explanation of why you rated confidentiality at this level]
- **Integrity**: [Your detailed explanation of why you rated integrity at this level]
- **Availability**: [Your detailed explanation of why you rated availability at this level]

**Primary Security Concern**: [Which aspect is most critical and why]

#### 2.3.2 Domain Name System (DNS)

**CIA Ratings:**
- Confidentiality: [X]/5
- Integrity: [X]/5  
- Availability: [X]/5

**Justification:**
[Provide detailed justifications for each rating]

#### 2.3.3 Implanted Defibrillator

**CIA Ratings:**
- Confidentiality: [X]/5
- Integrity: [X]/5  
- Availability: [X]/5

**Justification:**
[Provide detailed justifications for each rating]

#### 2.3.4 Online Voting System

**CIA Ratings:**
- Confidentiality: [X]/5
- Integrity: [X]/5  
- Availability: [X]/5

**Justification:**
[Provide detailed justifications for each rating]

#### 2.3.5 Automated Metro Train System

**CIA Ratings:**
- Confidentiality: [X]/5
- Integrity: [X]/5  
- Availability: [X]/5

**Justification:**
[Provide detailed justifications for each rating]

### 2.3 Analysis Summary

**Screenshot 2.1**: CIA Analysis Script Output
[Insert screenshot of your CIA analysis script execution and results]

**Key Insights:**
[Summarize your key findings from the CIA analysis, including which scenarios had the highest security requirements and why]

---

## Part 3: Security Incident Analysis

### 3.1 AI-Assisted Research Process

**AI Research Strategy**: [Describe how you used AI to find and research security incidents]

**AI Tools Used**: [List AI tools used for incident research]

**Research Refinement**: [Explain how AI helped you refine your incident selection and analysis]

### 3.2 Incident Selection

**Incident Title**: [Title of the security incident you researched]  
**Date**: [Date of the incident]  
**Source**: [URL of your news source]  
**Source Credibility**: [Brief assessment of why this is a credible source]

### 3.3 Incident Description

[Write 1-2 paragraphs describing the security incident. Include:]
- What happened?
- Who was affected?
- How was the attack carried out?
- What was the impact?

### 3.4 Security Framework Analysis

**Affected Security Properties:**
- [ ] Confidentiality - [Explain if/how this was affected]
- [ ] Integrity - [Explain if/how this was affected]
- [ ] Availability - [Explain if/how this was affected]
- [ ] Authenticity - [Explain if/how this was affected]
- [ ] Accountability - [Explain if/how this was affected]

**Impact Assessment**: [X]/5 - [Justify your impact rating]

**Attack Vector**: [Describe how the attack was carried out]

### 3.4 Analysis Discussion

[Write 1-2 paragraphs discussing the security implications of this incident. Consider:]
- Which security properties were most severely affected?
- What could have been done to prevent this incident?
- What lessons can be learned for future security practices?

**Screenshot 3.1**: Incident Analysis Script Output
[Insert screenshot of your incident analysis script execution]

---

## Part 4: Hash Function Investigation

### 4.1 AI-Enhanced Cryptographic Learning

**AI Learning Approach**: [Describe how you used AI to understand hash function concepts]

**Mathematical Insights**: [Explain how AI helped you understand the mathematical foundations]

**Conceptual Breakthroughs**: [Describe any "aha moments" facilitated by AI discussions]

### 4.2 Theoretical Analysis

#### 4.2.1 Collision Resistance Question

**Question**: Is it true that for all messages x, x' with x ≠ x', we have H(x) ≠ H(x')?

**Answer**: [Your answer - should be "No"]

**Explanation**: [Explain using the pigeonhole principle. Your explanation should cover:]
- The pigeonhole principle concept
- How it applies to hash functions
- Why collisions must exist mathematically
- The difference between mathematical existence and computational feasibility

#### 4.2.2 Collision Resistance Types

**Weak Collision Resistance (Second Preimage Resistance):**
[Define weak collision resistance and explain what it means]

**Strong Collision Resistance:**
[Define strong collision resistance and explain what it means]

**Key Differences:**
[Explain how weak and strong collision resistance differ, including computational requirements]

#### 4.2.3 Birthday Paradox

**Birthday Paradox Explanation:**
[Explain the birthday paradox concept and the mathematics behind it]

**Birthday Attack Against Hash Functions:**
[Explain how the birthday paradox applies to attacking hash functions]

#### 4.2.4 Attack Comparison

**Finding Alice's Specific Birthday vs. Any Matching Birthdays:**
[Compare the difficulty of these two scenarios]

**Relationship to Collision Resistance:**
[Explain how this relates to weak vs. strong collision resistance]

### 4.2 Practical Analysis

**Screenshot 4.1**: Avalanche Effect Demonstration
[Insert screenshot showing the avalanche effect analysis from your script]

**Screenshot 4.2**: Birthday Attack Simulation
[Insert screenshot showing the birthday attack simulation results]

**Screenshot 4.3**: Hash Algorithm Comparison
[Insert screenshot showing comparison of different hash algorithms]

### 4.3 Analysis Results

**Avalanche Effect Findings:**
[Summarize your findings about how small input changes affect hash outputs]

**Birthday Attack Results:**
[Discuss the results of your birthday attack simulation, including how actual results compared to theoretical expectations]

**Algorithm Comparison Insights:**
[Compare the different hash algorithms you tested]

---

## Part 5: Public-Key Certificate Analysis

### 5.1 AI-Guided PKI Understanding

**PKI Concept Exploration**: [Describe how AI helped you understand PKI concepts]

**Certificate Analysis Strategy**: [Explain how AI guided your certificate analysis approach]

**Trust Chain Insights**: [Describe AI-facilitated understanding of certificate trust chains]

### 5.2 Certificate Investigation

**Target Domain**: www.uccs.edu  
**Analysis Date**: [Date you performed the analysis]

#### 5.2.1 Certificate Objective

**Question**: What is the objective of the digital certificate?

**Answer**: [Explain the purpose of digital certificates, including authentication, encryption, integrity, and non-repudiation]

#### 5.2.2 Certificate Details

**SHA-1 Fingerprint**: [Insert the SHA-1 fingerprint you found]

**Certificate Authority**: [Name of the CA that issued the certificate]

**Certificate Subject**: [The subject/owner of the certificate]

**Screenshot 5.1**: Certificate Fingerprint and CA Information
[Insert screenshot showing the certificate fingerprint, CA, and subject information]

#### 5.2.3 Certificate Validity

**Issue Date (Not Before)**: [Certificate issue date]  
**Expiration Date (Not After)**: [Certificate expiration date]

**Screenshot 5.2**: Certificate Validity Dates
[Insert screenshot showing the certificate validity period]

**Question**: Does the UCCS website need to present this certificate every time a client accesses it?

**Answer**: [Explain when and how certificates are presented during TLS handshake]

#### 5.2.4 Methodology

**Tools Used**: [List the tools you used - OpenSSL, browser developer tools, etc.]

**Commands Executed**:
```bash
# List the specific commands you used
openssl s_client -connect www.uccs.edu:443 -servername www.uccs.edu
# Add other commands you used
```

**Process Steps**:
1. [Step 1 of your analysis process]
2. [Step 2 of your analysis process]
3. [Continue with all steps]

**Reproducibility**: [Explain how someone else could reproduce your analysis]

### 5.2 Additional Analysis

**Certificate Chain**: [Describe the certificate chain you observed]

**Security Assessment**: [Discuss any security observations about the certificate]

**Screenshot 5.3**: Complete Certificate Analysis Output
[Insert screenshot of your complete certificate analysis script output]

---

## Part 6: Textbook Problems Analysis

### 7.1 Problem 2.1: Electronic Codebook (ECB) Mode Analysis

**Problem Statement**: [Copy the complete problem statement from the lab instructions]

#### 7.1.1 ECB Mode Explanation

**How ECB Mode Works:**
[Provide a detailed explanation of how ECB mode processes message blocks, including:]
- Block-by-block encryption process
- Relationship between plaintext and ciphertext blocks
- Why it's considered the "simplest" approach

#### 7.1.2 Vulnerable Scenario Analysis

**Identified Scenario**: [Describe a specific scenario where ECB cannot be safely applied]

**Why This Scenario is Problematic**:
[Explain why your chosen scenario is vulnerable when using ECB mode]

**Concrete Examples**:
[Provide specific examples such as image encryption, database records, etc.]

#### 7.1.3 Security Analysis

**Why ECB is Not Secure**:
[Explain the fundamental security weaknesses of ECB mode]

**Fundamental Flaw**:
[Identify and explain the core flaw in the ECB scheme]

**Pattern Preservation and Information Leakage**:
[Discuss how ECB preserves patterns and what information this reveals]

#### 7.1.4 Attack Exploitation

**Attack Methods**:
[Describe specific ways attackers can exploit ECB mode weaknesses]

**Attack Scenarios**:
[Provide concrete attack scenarios such as:]
- Pattern analysis attacks
- Block rearrangement attacks
- Known plaintext attacks

**Practical Implications**:
[Explain the real-world impact of these attacks]

#### 7.1.5 AI-Enhanced Analysis

**AI Research Process**:
[Document your AI interactions for ECB mode research]

**Key Insights from AI**:
[List important insights gained through AI assistance]

**Verification Process**:
[Describe how you verified AI-provided information]

### 7.2 Problem 2.5: Digital Signatures vs. Message Authentication Codes

**Problem Statement**: [Copy the complete problem statement from the lab instructions]

#### 7.2.1 Fundamental Differences

**Digital Signatures (DS)**:
[Explain key characteristics of digital signatures]

**Message Authentication Codes (MAC)**:
[Explain key characteristics of MACs]

**Key Management Differences**:
[Compare how keys are managed in DS vs MAC systems]

#### 7.2.2 Attack Scenario Analysis

**Scenario A: Message Integrity Attack**

*Attack Description*: Alice sends "Transfer $1000 to Mark" + auth(x). Oscar intercepts and replaces "Mark" with "Oscar."

**Digital Signatures Protection**:
- Will DS detect this modification? [Yes/No and detailed explanation]
- Detection mechanism: [Explain how DS detects the modification]
- Effectiveness: [Rate and justify the effectiveness]

**MAC Protection**:
- Will MAC detect this modification? [Yes/No and detailed explanation]
- Detection mechanism: [Explain how MAC detects the modification]
- Effectiveness: [Rate and justify the effectiveness]

**Comparison**: [Compare DS vs MAC effectiveness for integrity protection]

**Scenario B: Replay Attack**

*Attack Description*: Alice sends "Transfer $1000 to Oscar" + auth(x). Oscar observes and resends the message 100 times.

**Digital Signatures Protection**:
- Will DS detect replay attacks? [Yes/No and detailed explanation]
- Inherent replay protection: [Explain DS replay resistance]
- Additional mechanisms needed: [Describe what else is required]

**MAC Protection**:
- Will MAC detect replay attacks? [Yes/No and detailed explanation]
- Inherent replay protection: [Explain MAC replay resistance]
- Additional mechanisms needed: [Describe what else is required]

**Comparison**: [Compare DS vs MAC replay attack resistance]

**Scenario C: Sender Authentication with Cheating Third Party**

*Attack Description*: Oscar claims he sent message x with valid auth(x), but Alice claims she sent it.

**Digital Signatures Resolution**:
- Can Bob determine the true sender? [Yes/No and detailed explanation]
- Resolution mechanism: [Explain how DS enables sender identification]
- Non-repudiation properties: [Discuss DS non-repudiation capabilities]

**MAC Resolution**:
- Can Bob determine the true sender? [Yes/No and detailed explanation]
- Resolution mechanism: [Explain MAC limitations for sender identification]
- Non-repudiation properties: [Discuss MAC non-repudiation limitations]

**Comparison**: [Compare DS vs MAC for sender authentication and non-repudiation]

**Scenario D: Authentication with Receiver Cheating**

*Attack Description*: Bob claims Alice sent "Transfer $1000 from Alice to Bob" + auth(x), but Alice denies sending it.

**Digital Signatures Protection**:
- Can Alice prove she didn't send it? [Yes/No and detailed explanation]
- Proof mechanism: [Explain how DS enables Alice to prove innocence]
- Non-repudiation implications: [Discuss the implications]

**MAC Protection**:
- Can Alice prove she didn't send it? [Yes/No and detailed explanation]
- Proof mechanism: [Explain MAC limitations for proving innocence]
- Non-repudiation implications: [Discuss the implications]

**Comparison**: [Compare DS vs MAC dispute resolution capabilities]

#### 7.2.3 Comprehensive Comparison Table

| Security Property | Digital Signatures (DS) | Message Authentication Codes (MAC) |
|-------------------|-------------------------|-------------------------------------|
| **Message Integrity** | [Your detailed analysis] | [Your detailed analysis] |
| **Sender Authentication** | [Your detailed analysis] | [Your detailed analysis] |
| **Non-repudiation** | [Your detailed analysis] | [Your detailed analysis] |
| **Replay Protection** | [Your detailed analysis] | [Your detailed analysis] |
| **Key Management** | [Your detailed analysis] | [Your detailed analysis] |
| **Performance** | [Your detailed analysis] | [Your detailed analysis] |
| **Use Cases** | [Your detailed analysis] | [Your detailed analysis] |

#### 7.2.4 Practical Recommendations

**When to Use Digital Signatures**:
[Provide specific scenarios and justifications]

**When to Use MACs**:
[Provide specific scenarios and justifications]

**Hybrid Approaches**:
[Discuss when and how to combine both approaches]

#### 7.2.5 AI-Enhanced Analysis

**AI Research Process**:
[Document your AI interactions for DS vs MAC analysis]

**Key Insights from AI**:
[List important insights gained through AI assistance]

**Verification Process**:
[Describe how you verified AI-provided information]

**Novel Insights Generated**:
[Describe any new understanding gained through AI collaboration]

---

## Part 7: Lessons Learned and Reflection

### 7.1 Technical Skills Gained

[Discuss the technical skills you developed during this lab, such as:]
- AWS EC2 management
- Command-line security tools
- Certificate analysis
- Hash function analysis

### 7.2 AI Integration Impact Assessment

**Overall AI Usage Summary**:
[Provide a comprehensive summary of how you used AI throughout the lab]

**Learning Enhancement**:
[Describe specific ways AI enhanced your learning beyond traditional methods]

**AI-Facilitated Insights**:
[List key insights or understanding that emerged from AI interactions]

**AI Tool Effectiveness**:
[Evaluate which AI tools were most helpful and why]

**Limitations Encountered**:
[Discuss any limitations or challenges with AI assistance]

### 7.3 Security Concepts Reinforced

[Discuss how this lab reinforced your understanding of security concepts:]
- CIA Triad application
- Real-world security incidents
- Cryptographic principles
- Public key infrastructure

### 7.4 Challenges Encountered

[Describe any challenges you faced and how you overcame them:]
- Technical difficulties
- Conceptual challenges
- Time management issues

### 7.4 Future Applications

[Discuss how you might apply what you learned in future coursework or career:]
- Security analysis skills
- Cloud computing experience
- Incident response knowledge

---

## Part 8: Conclusion

[Write a concluding paragraph that summarizes your overall experience with the lab and key takeaways]

---

## Appendix

### A.1 Script Outputs

[Include any additional script outputs that support your analysis]

### A.2 Configuration Files

[Include any configuration files or additional technical details]

### A.3 References

[List any additional sources you consulted beyond those provided in the lab assignment]

---

## Academic Integrity Statement

I certify that this work is my own and that I have not received unauthorized assistance from any person or source. All sources used have been properly cited.

**Signature**: [Your name]  
**Date**: [Date]

---

**Report Statistics:**
- Total Pages: [X]
- Word Count: [Approximate word count]
- Screenshots Included: [Number]
- Scripts Executed: [Number]