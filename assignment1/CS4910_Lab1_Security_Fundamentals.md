# CS 4910: Introduction to Computer Security
## Lab Assignment 1: Security Fundamentals and AWS Environment Setup (AI-Enhanced)

**Fall 2025 Semester**
**University of Colorado Colorado Springs**
**Instructor:** Rhett Saunders

---

## 📋 Lab Overview

This is the first lab assignment in CS 4910. You will establish foundational security knowledge and practical skills while setting up a secure cloud environment for future labs:

- 🌐 **AWS Cloud Security**: Set up and secure an EC2 instance for security analysis
- 🔐 **CIA Triad**: Deep dive into Confidentiality, Integrity, and Availability principles
- 🚨 **Security Incident Analysis**: Research and analyze real-world security breaches
- 🔑 **Hash Functions**: Understand cryptographic hash properties and applications
- 📜 **Digital Certificates**: Analyze X.509 certificates and PKI infrastructure
- 📚 **Textbook Problems**: Analyze ECB mode vulnerabilities and DS vs MAC security
- 🤖 **Leverage AI tools to enhance understanding of fundamental security concepts**
- ✅ **Use AI to validate analysis and explore security implications**

**⏱️ Estimated Time:** 4-6 hours
**📅 Due Date:** [To be announced by instructor]

---

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. ✅ Set up and configure a secure AWS EC2 instance for security research
2. ✅ Apply the CIA Triad (Confidentiality, Integrity, Availability) to real-world systems
3. ✅ Analyze security incidents using established security frameworks
4. ✅ Understand hash function properties and collision resistance
5. ✅ Examine and analyze X.509 digital certificates and PKI infrastructure
6. ✅ Evaluate ECB mode vulnerabilities and cryptographic security properties
7. ✅ Compare digital signatures and message authentication codes
8. 🤖 **Use AI tools to verify security analysis and explore edge cases**
9. 🤖 **Leverage AI to understand theoretical foundations of security concepts**
10. 📝 **Document AI-assisted learning and demonstrate enhanced comprehension**

---

## 📚 Prerequisites

- ✅ Basic understanding of computer networks and operating systems
- ✅ Familiarity with command-line interfaces (Linux/Unix)
- ✅ AWS account with appropriate permissions for EC2 instance creation
- 🤖 **Access to AI tools (ChatGPT, Claude, Gemini, or similar) for concept exploration and verification**

---

## 🤖 AI Integration Philosophy

This lab introduces AI integration for **security concept exploration and analysis verification**. You are encouraged to:

- 🔍 **Use AI to explore security concepts and theoretical foundations**
- 🧠 **Verify your understanding of CIA Triad applications and security frameworks**
- 🎯 **Generate additional scenarios for security analysis practice**
- ✅ **Validate your incident analysis and certificate examination findings**
- 📝 **Document security reasoning with AI assistance**

> **⚠️ Note:** While AI assistance is encouraged for exploration and verification, your final analysis must demonstrate your own understanding of security principles.

---

## 🛠️ Required Tools and Setup

### AWS Environment
- EC2 instance (t3.micro recommended for free tier)
- Ubuntu 24.04 LTS AMI
- Security groups configured for SSH, HTTP, and HTTPS
- Key pair for secure access

### Security Analysis Tools
- OpenSSL for certificate analysis
- Python 3 with hashlib library
- curl and wget for web requests
- Text editors (nano, vim, or VS Code)

---

## 📋 Part 1: AWS Environment Setup and Security Configuration

### 1.1 EC2 Instance Creation and Security Hardening

**Objective**: Create a secure AWS EC2 instance that will serve as your security analysis environment.

**Steps**:
1. **Launch EC2 Instance**:
   - Choose Ubuntu 24.04 LTS AMI
   - Select t3.micro instance type
   - Configure security group with minimal required access
   - Generate and download key pair

2. **Security Group Configuration**:
   ```
   Inbound Rules:
   - SSH (22): Your IP address only
   - HTTP (80): 0.0.0.0/0 (for web server testing)
   - HTTPS (443): 0.0.0.0/0 (for secure web testing)
   
   Outbound Rules:
   - All traffic: 0.0.0.0/0 (default)
   ```

3. **Connect and Update System**:
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3 python3-pip openssl curl wget -y
   ```

### 1.2 🤖 Security Configuration with AI Verification

**AI-Enhanced Learning Process:**
1. **🔍 Security Best Practices**: Use AI to understand AWS security best practices
2. **🛡️ Configuration Verification**: Have AI review your security group settings
3. **🎯 Threat Analysis**: Explore with AI potential threats to your configuration
4. **📝 Documentation**: Use AI to help document your security decisions

**💬 AI Verification Prompts:**
```
"I'm setting up an AWS EC2 instance for security research. Can you help me:
1. Review my security group configuration for potential vulnerabilities
2. Suggest additional hardening measures for Ubuntu 24.04
3. Explain the security implications of allowing HTTP/HTTPS from 0.0.0.0/0
4. What are the risks of SSH access and how can I mitigate them?"
```

**📝 Deliverable**: Document your instance configuration, security group settings, and AI-verified security measures.

---

## 🔐 Part 2: CIA Triad Analysis and Real-World Applications

### 2.1 Fundamental CIA Triad Concepts

**Objective**: Develop deep understanding of Confidentiality, Integrity, and Availability principles through practical analysis.

**Core Concepts**:
- **Confidentiality**: Ensuring information is accessible only to authorized entities
- **Integrity**: Maintaining accuracy and completeness of information
- **Availability**: Ensuring information and resources are accessible when needed

### 2.2 🤖 CIA Triad Analysis with AI Enhancement

**AI-Enhanced Learning Process:**
1. **🔍 Concept Exploration**: Use AI to explore nuanced aspects of CIA principles
2. **🏢 Real-World Applications**: Have AI help identify CIA applications in different industries
3. **⚖️ Trade-off Analysis**: Explore with AI the tensions between CIA components
4. **🎯 Scenario Generation**: Use AI to create additional analysis scenarios

**💬 AI Analysis Prompts:**
```
"I'm analyzing the CIA Triad in cybersecurity. Can you help me:
1. Provide real-world examples where confidentiality conflicts with availability
2. Explain how integrity can be maintained in distributed systems
3. Generate scenarios where I need to prioritize one CIA component over others
4. What are modern challenges to each CIA component in cloud environments?"
```

**Analysis Tasks**:

1. **Healthcare System Analysis**:
   - Analyze how a hospital's electronic health record (EHR) system implements each CIA component
   - Identify potential conflicts between CIA requirements
   - Propose solutions for balancing competing needs

2. **E-commerce Platform Analysis**:
   - Evaluate CIA requirements for an online shopping platform
   - Consider customer data, payment processing, and service availability
   - Analyze the impact of CIA failures on business operations

3. **Government Database Analysis**:
   - Examine CIA requirements for a classified government database
   - Consider different security clearance levels and access controls
   - Analyze the consequences of CIA breaches in this context

### 2.3 🤖 AI-Assisted Scenario Development

**Create Your Own Scenario**:
Use AI to help develop and analyze a unique CIA scenario:

**💬 AI Scenario Prompts:**
```
"Help me create a unique CIA Triad analysis scenario involving [your chosen domain: 
IoT devices, autonomous vehicles, smart city infrastructure, etc.]. 
1. What are the specific CIA requirements for this domain?
2. What are the unique challenges and threats?
3. How would you prioritize CIA components in this context?
4. What would be the consequences of failures in each area?"
```

**📝 Deliverable**: Comprehensive CIA analysis document with AI-verified scenarios and solutions.

---

## 🚨 Part 3: Security Incident Analysis and Framework Application

### 3.1 Current Security Incident Research

**Objective**: Analyze a recent security incident using established security frameworks and AI-enhanced research.

**Requirements**:
- Select a security incident from the past 12 months
- Use multiple reliable sources (security blogs, official reports, news articles)
- Apply security analysis frameworks to understand the incident

### 3.2 🤖 AI-Enhanced Incident Analysis

**AI-Enhanced Research Process:**
1. **🔍 Incident Discovery**: Use AI to help identify significant recent security incidents
2. **📊 Framework Application**: Have AI explain different security analysis frameworks
3. **🎯 Root Cause Analysis**: Explore with AI the underlying causes and contributing factors
4. **🛡️ Prevention Strategies**: Use AI to develop comprehensive prevention recommendations

**💬 AI Research Prompts:**
```
"I'm analyzing the [incident name] security breach. Can you help me:
1. Explain the technical details of how this attack was executed
2. Apply the NIST Cybersecurity Framework to analyze this incident
3. Identify the key vulnerabilities that were exploited
4. Suggest specific prevention and detection measures
5. What lessons can other organizations learn from this incident?"
```

**Analysis Framework Options**:
1. **NIST Cybersecurity Framework**: Identify, Protect, Detect, Respond, Recover
2. **MITRE ATT&CK Framework**: Map attack techniques and tactics
3. **Cyber Kill Chain**: Analyze attack progression stages
4. **Diamond Model**: Examine adversary, capability, infrastructure, and victim

### 3.3 Incident Analysis Requirements

**Your analysis must include**:
1. **Incident Overview**: What happened, when, and to whom
2. **Technical Analysis**: How the attack was executed
3. **Impact Assessment**: Consequences for the organization and stakeholders
4. **Framework Application**: Use at least one security framework for analysis
5. **Lessons Learned**: Key takeaways and prevention strategies
6. **AI Insights**: Document how AI enhanced your understanding

### 3.4 🤖 AI-Verified Prevention Strategies

**💬 AI Prevention Prompts:**
```
"Based on the [incident name] analysis, help me develop:
1. Specific technical controls that could have prevented this attack
2. Process improvements for better security posture
3. Detection mechanisms that could have identified the attack earlier
4. Response procedures for similar future incidents
5. How can AI and machine learning help prevent similar attacks?"
```

**📝 Deliverable**: Comprehensive incident analysis report with framework application and AI-enhanced insights.

---

## 🔑 Part 4: Hash Functions and Cryptographic Properties

### 4.1 Hash Function Fundamentals

**Objective**: Understand cryptographic hash functions and their security properties through practical analysis.

**Key Properties**:
- **Deterministic**: Same input always produces same output
- **Fixed Output Size**: Regardless of input size
- **Avalanche Effect**: Small input changes cause large output changes
- **One-way Function**: Computationally infeasible to reverse
- **Collision Resistant**: Hard to find two inputs with same output

### 4.2 🤖 Hash Function Analysis with AI Verification

**AI-Enhanced Learning Process:**
1. **🔍 Property Exploration**: Use AI to understand hash function properties deeply
2. **🧮 Calculation Verification**: Have AI verify your hash calculations and analysis
3. **🎯 Attack Scenario Analysis**: Explore with AI different hash function attacks
4. **🛡️ Security Applications**: Use AI to understand hash function uses in security

**💬 AI Analysis Prompts:**
```
"I'm studying cryptographic hash functions. Can you help me:
1. Explain why the avalanche effect is crucial for security
2. Describe different types of hash collision attacks
3. Compare the security properties of MD5, SHA-1, and SHA-256
4. Provide examples of how hash functions are used in digital signatures
5. What are rainbow tables and how do salts prevent their use?"
```

### 4.3 Practical Hash Analysis

**Analysis Tasks**:

1. **Hash Property Demonstration**:
   ```bash
   # Demonstrate avalanche effect
   echo "Hello World" | sha256sum
   echo "Hello World!" | sha256sum
   echo "hello world" | sha256sum
   ```

2. **Hash Collision Research**:
   - Research known MD5 and SHA-1 collisions
   - Understand the practical implications
   - Analyze why these algorithms are deprecated

3. **Password Hashing Analysis**:
   - Compare simple hashing vs. salted hashing
   - Understand bcrypt, scrypt, and Argon2
   - Analyze password storage best practices

### 4.4 🤖 AI-Enhanced Security Applications

**💬 AI Application Prompts:**
```
"Help me understand hash function applications in cybersecurity:
1. How are hash functions used in blockchain technology?
2. Explain the role of hashing in digital forensics
3. How do hash functions provide data integrity in network protocols?
4. What is the difference between cryptographic and non-cryptographic hash functions?
5. How can AI be used to analyze hash function security?"
```

**📝 Deliverable**: Hash function analysis report with practical demonstrations and AI-verified security applications.

---

## 📜 Part 5: Digital Certificate Analysis and PKI Infrastructure

### 5.1 X.509 Certificate Structure and Analysis

**Objective**: Examine digital certificates and understand Public Key Infrastructure (PKI) components.

**Certificate Components**:
- **Subject**: Entity the certificate identifies
- **Issuer**: Certificate Authority that signed the certificate
- **Public Key**: Subject's public key for cryptographic operations
- **Validity Period**: Certificate's valid date range
- **Digital Signature**: CA's signature ensuring certificate integrity

### 5.2 🤖 Certificate Analysis with AI Enhancement

**AI-Enhanced Learning Process:**
1. **🔍 PKI Concepts**: Use AI to understand PKI infrastructure and trust models
2. **📜 Certificate Parsing**: Have AI help interpret certificate fields and extensions
3. **🔐 Trust Chain Analysis**: Explore with AI how certificate trust chains work
4. **🛡️ Security Implications**: Use AI to understand certificate-based attacks

**💬 AI Analysis Prompts:**
```
"I'm analyzing X.509 digital certificates. Can you help me:
1. Explain the difference between root, intermediate, and end-entity certificates
2. Describe how certificate revocation works (CRL vs OCSP)
3. What are the security implications of certificate pinning?
4. How do wildcard certificates work and what are their risks?
5. Explain common certificate-based attacks and their prevention"
```

### 5.3 Practical Certificate Analysis

**Analysis Tasks**:

1. **Website Certificate Examination**:
   ```bash
   # Examine a website's certificate
   openssl s_client -connect google.com:443 -servername google.com < /dev/null 2>/dev/null | openssl x509 -text -noout
   ```

2. **Certificate Chain Analysis**:
   ```bash
   # Get full certificate chain
   openssl s_client -connect github.com:443 -showcerts < /dev/null 2>/dev/null
   ```

3. **Certificate Validation**:
   - Verify certificate signatures
   - Check validity periods
   - Analyze certificate extensions
   - Understand Subject Alternative Names (SAN)

### 5.4 🤖 AI-Enhanced PKI Security Analysis

**💬 AI PKI Prompts:**
```
"Help me understand PKI security in modern environments:
1. How does certificate transparency help prevent certificate mis-issuance?
2. What are the challenges of PKI in IoT and mobile environments?
3. How do certificate authorities maintain security and trust?
4. What is the role of Hardware Security Modules (HSMs) in PKI?
5. How can AI help with certificate lifecycle management?"
```

**📝 Deliverable**: Certificate analysis report with practical examinations and AI-enhanced PKI understanding.

---

## 📚 Part 6: Textbook Problems Analysis

### 6.1 Problem 2.1: Electronic Codebook (ECB) Mode Analysis

**Problem Statement**: 
*"Electronic Codebook (ECB) mode is the simplest encryption mode for block ciphers, where each block of plaintext is encrypted independently. However, ECB mode has significant security weaknesses. Analyze a scenario where ECB mode cannot be safely applied and explain why this mode is not secure."*

#### 6.1.1 🤖 ECB Mode Understanding with AI

**AI-Enhanced Learning Process:**
1. **🔍 Mode Operation**: Use AI to understand how ECB mode processes data blocks
2. **🛡️ Security Analysis**: Have AI explain ECB's fundamental security weaknesses
3. **🎯 Attack Scenarios**: Explore with AI specific attacks against ECB mode
4. **📊 Pattern Analysis**: Use AI to understand how ECB preserves data patterns

**💬 AI ECB Analysis Prompts:**
```
"I'm analyzing ECB mode vulnerabilities. Can you help me:
1. Explain step-by-step how ECB mode encrypts data blocks
2. Why is the independence of block encryption a security weakness?
3. Provide concrete examples of ECB mode attacks (like image encryption)
4. Compare ECB with other block cipher modes (CBC, CTR, GCM)
5. In what scenarios might ECB mode be acceptable, if any?"
```

#### 6.1.2 Vulnerable Scenario Analysis

**Your Analysis Must Include**:
1. **Specific Scenario**: Describe a concrete situation where ECB fails
2. **Technical Explanation**: Why ECB is vulnerable in this scenario
3. **Attack Demonstration**: How an attacker could exploit the weakness
4. **Pattern Preservation**: How ECB reveals information through patterns
5. **Alternative Solutions**: What encryption modes would be secure

#### 6.1.3 🤖 AI-Verified Security Analysis

**💬 AI Verification Prompts:**
```
"Please verify my ECB mode analysis:
1. Is my understanding of ECB's block-by-block encryption correct?
2. Are the attack scenarios I described technically accurate?
3. What additional vulnerabilities should I consider?
4. How would you improve my security recommendations?
5. Are there any edge cases or special considerations I missed?"
```

### 6.2 Problem 2.5: Digital Signatures vs. Message Authentication Codes

**Problem Statement**: 
*"Compare digital signatures (DS) and message authentication codes (MAC) in terms of their security properties. Analyze how each mechanism responds to different attack scenarios: message modification, replay attacks, sender authentication disputes, and receiver authentication disputes."*

#### 6.2.1 🤖 DS vs MAC Fundamentals with AI

**AI-Enhanced Learning Process:**
1. **🔍 Mechanism Comparison**: Use AI to understand fundamental differences between DS and MAC
2. **🔐 Security Properties**: Have AI explain the security guarantees of each approach
3. **🔑 Key Management**: Explore with AI how key management differs between DS and MAC
4. **⚖️ Trade-off Analysis**: Use AI to understand when to use each mechanism

**💬 AI Comparison Prompts:**
```
"I'm comparing digital signatures and MACs. Can you help me:
1. Explain the fundamental cryptographic differences between DS and MAC
2. What are the key management implications of each approach?
3. How do DS and MAC provide different types of authentication?
4. What are the performance trade-offs between DS and MAC?
5. In what scenarios would you choose one over the other?"
```

#### 6.2.2 Attack Scenario Analysis

**Analyze Each Scenario**:

1. **Message Modification Attack**:
   - Alice sends "Transfer $1000 to Mark" + auth(x)
   - Oscar intercepts and changes "Mark" to "Oscar"
   - Compare DS vs MAC detection capabilities

2. **Replay Attack**:
   - Alice sends "Transfer $1000 to Oscar" + auth(x)
   - Oscar captures and replays the message 100 times
   - Analyze DS vs MAC replay protection

3. **Sender Authentication Dispute**:
   - Oscar claims he sent message x with valid auth(x)
   - Alice claims she sent it
   - Compare DS vs MAC dispute resolution

4. **Receiver Authentication Dispute**:
   - Bob claims Alice sent "Transfer $1000 to Bob" + auth(x)
   - Alice denies sending it
   - Analyze DS vs MAC non-repudiation properties

#### 6.2.3 🤖 AI-Enhanced Security Property Analysis

**💬 AI Security Analysis Prompts:**
```
"Help me analyze DS vs MAC security properties:
1. How does non-repudiation differ between DS and MAC?
2. What are the implications of shared vs. asymmetric keys for authentication?
3. How do DS and MAC handle multi-party communication scenarios?
4. What additional security measures are needed for replay protection?
5. How do modern protocols combine DS and MAC for enhanced security?"
```

**📝 Deliverable**: Comprehensive comparison analysis with AI-verified security property evaluation.

---

## 📊 Unified Grading Rubric (100 Points Total)

### 1. 🛠️ Technical Implementation and Environment Setup (25 points)
*Includes AWS configuration, tool installation, script execution, and practical demonstrations*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 23-25 | Perfect AWS setup, all tools configured correctly, comprehensive security hardening, excellent script execution with detailed outputs |
| **Good** | 18-22 | Good AWS setup, most tools working, adequate security measures, scripts run with minor issues |
| **Satisfactory** | 13-17 | Basic AWS setup functional, some tool issues, minimal security configuration, scripts run with some problems |
| **Needs Improvement** | 0-12 | Poor AWS setup, major tool failures, inadequate security, scripts fail to execute properly |

### 2. 🔐 Security Analysis and Understanding (35 points)
*Includes CIA Triad analysis, incident analysis, hash functions, certificates, and textbook problems*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 32-35 | Sophisticated security analysis, excellent understanding of all concepts, comprehensive textbook problem solutions, insightful incident analysis |
| **Good** | 25-31 | Good security analysis, solid understanding of most concepts, adequate textbook solutions, reasonable incident analysis |
| **Satisfactory** | 18-24 | Basic security analysis, adequate understanding, minimal textbook solutions, superficial incident analysis |
| **Needs Improvement** | 0-17 | Poor security analysis, misunderstanding of concepts, inadequate textbook solutions, weak incident analysis |

### 3. 🤖 AI Integration and Enhanced Learning (25 points)
*Includes AI usage for verification, exploration, and enhanced understanding*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 23-25 | Sophisticated AI usage for concept exploration and verification, detailed interaction logs, demonstrates critical evaluation of AI responses, novel insights generated through AI collaboration |
| **Good** | 18-22 | Effective AI usage with good documentation, evidence of enhanced understanding through AI interaction, appropriate verification of AI-provided information |
| **Satisfactory** | 13-17 | Basic AI usage documented, some evidence of enhanced learning, minimal but acceptable AI integration |
| **Needs Improvement** | 0-12 | Poor or minimal AI usage, inadequate documentation, no evidence of enhanced learning through AI |

### 4. 📝 Technical Documentation and Communication (15 points)
*Includes lab report, analysis documentation, and clear explanation of concepts*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 14-15 | Professional documentation, clear technical communication, comprehensive explanations, excellent organization |
| **Good** | 11-13 | Good documentation quality, mostly clear explanations, minor communication issues |
| **Satisfactory** | 8-10 | Adequate documentation, basic explanations, some clarity issues |
| **Needs Improvement** | 0-7 | Poor documentation, unclear explanations, major communication problems |

---

## 📁 File Structure and Organization

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
├── textbook_problems/
│   ├── problem_2_1_ecb_analysis.md
│   └── problem_2_5_ds_vs_mac.md
├── ai_interactions/
│   ├── cia_ai_session.md
│   ├── incident_ai_research.md
│   ├── hash_ai_exploration.md
│   ├── certificate_ai_analysis.md
│   ├── ecb_ai_research.md
│   └── ds_mac_ai_analysis.md
└── lab_report.md
```

---

## ✅ Submission Checklist

- [ ] AWS EC2 instance properly configured and accessible
- [ ] All scripts executed successfully with output saved
- [ ] Screenshots captured for each major section
- [ ] CIA Triad analysis completed with real-world scenarios
- [ ] Security incident research and analysis completed
- [ ] Hash function analysis with practical demonstrations
- [ ] Certificate analysis completed with proper documentation
- [ ] **Textbook Problem 2.1 (ECB Mode) analysis completed**
- [ ] **Textbook Problem 2.5 (DS vs MAC) analysis completed**
- [ ] AI interaction logs and insights documented for all sections
- [ ] All files organized in required directory structure
- [ ] Comprehensive lab report summarizing findings and lessons learned

---

## 📚 Additional Resources

### 📖 Recommended Reading
- Textbook Chapter 1: Introduction to Computer Security
- Textbook Chapter 2: Cryptographic Tools (Problems 2.1 and 2.5)
- AWS EC2 Security Best Practices
- NIST Cybersecurity Framework
- OWASP Security Guidelines

### 🔗 Useful Links
- [AWS EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [OpenSSL Documentation](https://www.openssl.org/docs/)
- [NIST Hash Function Standards](https://csrc.nist.gov/projects/hash-functions)
- [Certificate Transparency Logs](https://crt.sh/)

### 🤖 AI Tool Recommendations
- **ChatGPT**: Excellent for concept explanation and verification
- **Claude**: Strong analytical capabilities for security analysis
- **Gemini**: Good for research and information synthesis
- **Perplexity**: Useful for current security incident research

---

## 📞 Support and Office Hours

If you encounter technical difficulties or have questions about the lab content:

- **Office Hours**: [To be announced by instructor]
- **Email**: [Instructor email]
- **Discussion Forum**: [Course management system]

Remember to document any issues you encounter and the solutions you implement - this demonstrates problem-solving skills and can be valuable for your lab report.

---

*This lab assignment is designed to build foundational security knowledge while introducing AI-enhanced learning techniques that will be valuable throughout your cybersecurity career.*