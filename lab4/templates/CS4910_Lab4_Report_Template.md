# CS 4910: Introduction to Computer Security
## Lab 4 Report: Network Security and Intrusion Detection Systems

**Student Name**: [Your Name]  
**Student ID**: [Your Student ID]  
**Date**: [Submission Date]  
**Instructor**: Rhett Saunders  
**Semester**: Fall 2025  
**Due Date**: December 10, 2025

---

## 📋 Executive Summary

[Provide a 2-3 paragraph summary of your lab work, key findings, and insights gained about network security and intrusion detection systems]

---

## 🛡️ Part 1: TCP SYN Cookies and DoS Defense

### 1.1 SYN Cookie Defense Mechanism Analysis

#### Background and Context
[Describe SYN flooding attacks and the need for defense mechanisms]

#### Part (a) - Defense Mechanism Explanation
**How SYN Cookies Defend Against SYN Flooding**:
[Your detailed explanation of the SYN cookie mechanism]

**Types of DoS Attacks SYN Cookies Are Effective Against**:
[Specific DoS attack types and effectiveness analysis]

**AI Insights**: [Key insights gained from AI interaction about SYN cookie mechanisms]

#### Part (b) - Statement Analysis

##### Statement 1: "SYN cookies disallow an attacker from completing the TCP handshake"
**Analysis**: [Your true/false determination and explanation]
**Reasoning**: [Detailed technical reasoning]
**AI Verification**: [AI insights on this statement]

##### Statement 2: "SYN cookies cause major degradation of service"
**Analysis**: [Your true/false determination and explanation]
**Reasoning**: [Performance impact analysis]
**AI Verification**: [AI insights on performance implications]

##### Statement 3: "SYN cookies cause TCP resets"
**Analysis**: [Your true/false determination and explanation]
**Reasoning**: [Technical explanation of TCP behavior]
**AI Verification**: [AI insights on TCP reset behavior]

#### Part (c) - Practical Implementation
**Operating System**: [Your OS version and type]
**Implementation Method**: [Commands/methods used]
**Configuration Details**: [Specific configuration changes made]
**Verification**: [How you verified the implementation]
**Screenshots**: [Reference to included screenshots]
**AI Guidance**: [How AI assisted in implementation]

---

## 🔥 Part 2: Firewall Configuration and IP Blocking

### 2.1 Network Address Discovery

#### Part (a) - IP Address Identification
**Discovery Methods Used**: [Commands/GUI methods employed]
**My_address**: [Your discovered IP address]
**Discovery Process**: [Step-by-step process description]
**Screenshots**: [Reference to included screenshots]
**AI Assistance**: [How AI helped with network discovery]

### 2.2 IP Address Blocking Implementation

#### Part (b) - Firewall Rule Configuration
**Target IP Address**: [My_address + 1]
**Firewall Tool Used**: [iptables, ufw, etc.]
**Blocking Commands**: [Exact commands used]
**Rule Verification**: [How you verified the blocking]
**Screenshots**: [Reference to included screenshots]
**AI Guidance**: [AI assistance in firewall configuration]

#### Security Analysis
**Effectiveness**: [Analysis of IP blocking effectiveness]
**Limitations**: [Limitations of IP-based filtering]
**Bypass Methods**: [Potential ways to circumvent blocking]

---

## 🦠 Part 3: Malware Analysis and Attack Vector Identification

### 3.1 Document Infection Malware Analysis

#### Code Fragment Analysis
```
legitimate code
if an infected document is opened;    
  trigger_code_to_infect_other_documents();
legitimate code
```

**Malware Type**: [Your identification of the malware type]
**Infection Mechanism**: [Detailed explanation of how it works]
**Propagation Method**: [How the malware spreads]
**Impact Assessment**: [Potential damage and effects]
**Detection Strategies**: [Methods for detection and prevention]
**AI Analysis**: [AI insights on malware classification]

### 3.2 Web-Based Attack Vector Analysis

#### Code Fragment Analysis
```
username = read_username();
password = read_password();
if username and password are valid
  return ALLOW_LOGIN;    
  executable_start_download();
else return 
  DENY_LOGIN    
  executable_start_download();
```

**Attack Type**: [Your identification of the attack type]
**Attack Mechanism**: [How the attack works]
**Stealth Characteristics**: [Why it's difficult to detect]
**Delivery Methods**: [How this attack might be deployed]
**Defense Strategies**: [Prevention and detection methods]
**AI Analysis**: [AI insights on web-based attacks]

---

## 📊 Part 4: Quantitative Network Attack Analysis

### 4.1 DoS Flood Attack Calculations

#### Attack Scenario Parameters
**Target Link Capacity**: 8 Mbps
**Attack Protocol**: ICMP echo request (ping)
**Packet Sizes Analyzed**: 100 bytes, 1000 bytes, 1460 bytes

#### Calculations

##### 100-byte Packets
**Mathematical Work**: [Step-by-step calculations]
**Result**: [Packets per second required]
**AI Verification**: [AI confirmation of calculations]

##### 1000-byte Packets
**Mathematical Work**: [Step-by-step calculations]
**Result**: [Packets per second required]
**AI Verification**: [AI confirmation of calculations]

##### 1460-byte Packets
**Mathematical Work**: [Step-by-step calculations]
**Result**: [Packets per second required]
**AI Verification**: [AI confirmation of calculations]

#### Analysis
**Packet Size vs. Attack Efficiency**: [Relationship analysis]
**Practical Implications**: [Real-world attack considerations]
**Defense Implications**: [How defenders can use this information]

### 4.2 Distributed DoS Attack Scaling Analysis

#### Scenario Parameters
**Zombie System Capacity**: 256 kbps uplink
**Packet Sizes**: 100 bytes, 1000 bytes, 1500 bytes
**Target**: Same 8-Mbps link

#### Individual Zombie Calculations

##### 100-byte Packets
**Maximum Packets per Second**: [Your calculation]
**AI Verification**: [AI confirmation]

##### 1000-byte Packets
**Maximum Packets per Second**: [Your calculation]
**AI Verification**: [AI confirmation]

##### 1500-byte Packets
**Maximum Packets per Second**: [Your calculation]
**AI Verification**: [AI confirmation]

#### Distributed Attack Analysis
**Zombies Required for 8-Mbps Link**: [Calculations for each packet size]
**Botnet Scaling Implications**: [Analysis of large-scale botnets]
**Multiple Target Capability**: [Ability to attack multiple organizations]
**Large Organization Threats**: [Implications for major organizations]
**AI Insights**: [AI analysis of distributed attack implications]

---

## 🔍 Part 5: Intrusion Detection System Analysis

### 5.1 Tripwire System Analysis

#### System Overview
[Your understanding of Tripwire functionality and purpose]

#### Advantages Analysis
**Security Benefits**: [List and explain advantages]
**Detection Capabilities**: [What Tripwire can detect]
**Forensic Value**: [Incident investigation benefits]
**AI Insights**: [AI analysis of advantages]

#### Disadvantages Analysis
**Configuration Complexity**: [Challenges in setup and maintenance]
**Performance Impact**: [System resource implications]
**False Positive Management**: [Alert management challenges]
**Scalability Issues**: [Limitations for large systems]
**AI Insights**: [AI analysis of disadvantages]

#### Implementation Challenges
**File Classification**: [Strategies for different file types]
**Configuration Workload**: [Administrative overhead]
**Alert Management**: [Response and monitoring requirements]
**AI Guidance**: [AI assistance in understanding challenges]

#### Cryptographic Hash Function Role
**Integrity Verification**: [How hash functions ensure security]
**Security Properties**: [Required cryptographic properties]
**Attack Resistance**: [Protection against various attacks]
**Performance Considerations**: [Efficiency in large-scale monitoring]
**AI Analysis**: [AI insights on cryptographic implementation]

---

## 📧 Part 6: Network Protocol Security and Packet Filtering

### 6.1 SMTP Protocol Security Analysis

#### Protocol Understanding
[Your understanding of SMTP mechanics and security considerations]

#### Basic SMTP Filtering Rule Analysis

##### Part (a) - Rule Effect Description
**Rule 1**: [Description of effect and purpose]
**Rule 2**: [Description of effect and purpose]
**Rule 3**: [Description of effect and purpose]
**Rule 4**: [Description of effect and purpose]
**Rule 5**: [Description of effect and purpose]
**AI Analysis**: [AI insights on rule effectiveness]

##### Part (b) - Packet Analysis
**Packet 1**: [Permit/Deny decision and rule used]
**Packet 2**: [Permit/Deny decision and rule used]
**Packet 3**: [Permit/Deny decision and rule used]
**Packet 4**: [Permit/Deny decision and rule used]
**AI Verification**: [AI confirmation of analysis]

##### Part (c) - Attack Scenario Evaluation
**Attack Success**: [Will the attack succeed?]
**Analysis**: [Detailed evaluation of attack packets]
**Rule Weaknesses**: [Identified vulnerabilities]
**AI Assessment**: [AI analysis of attack scenario]

### 6.2 Enhanced SMTP Filtering Analysis

#### Part (a) - Change Analysis
**Modifications Made**: [Description of rule changes]
**Security Improvements**: [How changes enhance security]
**AI Insights**: [AI analysis of improvements]

#### Part (b) - Comparative Packet Analysis
**Packet 1**: [New permit/deny decision and rule]
**Packet 2**: [New permit/deny decision and rule]
**Packet 3**: [New permit/deny decision and rule]
**Packet 4**: [New permit/deny decision and rule]
**Packet 5**: [New permit/deny decision and rule]
**Packet 6**: [New permit/deny decision and rule]

#### Security Enhancement Assessment
**Improvements Achieved**: [Analysis of enhanced security]
**Trade-offs**: [Impact on legitimate traffic]
**Overall Effectiveness**: [Evaluation of rule set improvements]
**AI Analysis**: [AI assessment of enhanced filtering]

---

## 📚 Part 7: Textbook Problems Solutions

### Problem 6.5: Malware Type Identification

#### Problem Analysis
[Your understanding of the code fragment and requirements]

#### Solution
**Malware Type**: [Your identification]
**Explanation**: [Detailed analysis of malware characteristics]
**Infection Mechanism**: [How the malware operates]
**AI Verification**: [AI confirmation of analysis]

### Problem 6.6: Web-Based Malicious Code Analysis

#### Problem Analysis
[Your understanding of the web code fragment]

#### Solution
**Attack Type**: [Your identification]
**Explanation**: [Detailed analysis of the attack mechanism]
**Security Implications**: [Impact and risks]
**AI Verification**: [AI confirmation of analysis]

### Problem 7.1: DoS Flood Attack Calculations

#### Problem Analysis
[Your understanding of the attack scenario]

#### Solutions
**100-byte packets**: [Calculation and result]
**1000-byte packets**: [Calculation and result]
**1460-byte packets**: [Calculation and result]
**AI Verification**: [AI confirmation of all calculations]

### Problem 7.3: Distributed DoS Attack Analysis

#### Problem Analysis
[Your understanding of the distributed attack scenario]

#### Solutions
**Single zombie capacity**: [Calculations for each packet size]
**Zombie requirements**: [Number needed for target link]
**Botnet implications**: [Analysis of large-scale attacks]
**AI Verification**: [AI confirmation of analysis]

### Problem 8.6: Tripwire Intrusion Detection Analysis

#### Problem Analysis
[Your understanding of Tripwire system requirements]

#### Solution
**Advantages**: [Detailed list and explanation]
**Disadvantages**: [Detailed list and explanation]
**Configuration challenges**: [Analysis of operational issues]
**Cryptographic hash function role**: [Explanation of security implementation]
**AI Verification**: [AI confirmation of analysis]

### Problem 9.5: SMTP Packet Filtering Rules

#### Problem Analysis
[Your understanding of SMTP filtering requirements]

#### Solutions
**Part (a)**: [Rule effect descriptions]
**Part (b)**: [Packet analysis results]
**Part (c)**: [Attack scenario evaluation]
**AI Verification**: [AI confirmation of analysis]

### Problem 9.6: Enhanced SMTP Filtering Rules

#### Problem Analysis
[Your understanding of the enhanced rule set]

#### Solutions
**Part (a)**: [Change description]
**Part (b)**: [Comparative packet analysis]
**AI Verification**: [AI confirmation of analysis]

---

## 🤖 Part 8: AI Integration and Learning Enhancement

### 8.1 AI Tools and Techniques Used

#### Tools Utilized
[List of AI tools used and their specific applications]

#### Interaction Methodology
[Your approach to using AI effectively]

### 8.2 Key AI-Enhanced Insights

#### Network Security Implementation
[Major insights gained through AI assistance]

#### Attack Analysis and Calculations
[Key insights from AI interaction in quantitative analysis]

#### Security System Analysis
[How AI enhanced your understanding of security systems]

### 8.3 AI Interaction Logs Summary

#### Most Valuable AI Interactions
[Highlight the most helpful AI conversations]

#### Critical Evaluation of AI Responses
[Your assessment of AI accuracy and usefulness]

#### Novel Insights Generated
[New understanding developed through AI collaboration]

---

## 📈 Part 9: Synthesis and Conclusions

### 9.1 Key Learning Outcomes

#### Network Security Implementation
[What you learned about practical network security]

#### Attack Analysis and Defense
[Understanding gained about attack mechanisms and defenses]

#### Intrusion Detection Systems
[Key insights about IDS capabilities and limitations]

### 9.2 Practical Applications

#### Professional Relevance
[How this knowledge applies to cybersecurity careers]

#### Real-World Scenarios
[Examples of how you might apply these concepts]

### 9.3 Future Learning Directions

#### Areas for Further Study
[Topics you want to explore further]

#### Skill Development
[Technical skills to continue developing]

---

## 📊 Part 10: Self-Assessment and Reflection

### 10.1 Challenges Encountered

#### Technical Implementation Challenges
[Difficult technical concepts and how you overcame them]

#### Calculation and Analysis Challenges
[Mathematical and analytical difficulties]

### 10.2 AI Integration Effectiveness

#### Successful AI Usage
[Where AI was most helpful in your learning]

#### AI Limitations
[Where AI was less helpful or required critical evaluation]

### 10.3 Overall Learning Assessment

#### Knowledge Gained
[Assessment of your learning progress]

#### Skills Developed
[New technical and analytical skills acquired]

#### Professional Growth
[How this lab contributes to your cybersecurity development]

---

## 📚 References and Resources

### Academic Sources
[List any academic papers or textbook sections referenced]

### AI Interactions
[Reference to your detailed AI interaction logs]

### Additional Resources
[Any supplementary materials used]

---

## 📎 Appendices

### Appendix A: Detailed AI Interaction Logs
[Include comprehensive logs of your AI conversations]

### Appendix B: Screenshots and System Configurations
[Include all system screenshots and configuration files]

### Appendix C: Mathematical Calculations
[Include detailed mathematical work and verification]

### Appendix D: Implementation Scripts and Configurations
[Include any scripts or configuration files created]

---

**Total Word Count**: [Approximate word count]  
**Submission Date**: [Date submitted]  
**Academic Integrity Statement**: I certify that this work is my own and that I have properly documented all AI assistance used in completing this assignment.