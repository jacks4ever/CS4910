# CS 4910: Introduction to Computer Security
## Lab Assignment 2: Information Theory, Cryptography, and Security Analysis (AI-Enhanced)

**Fall 2025 Semester**  
**University of Colorado Colorado Springs**  
**Instructor:** Rhett Saunders  

---

## 📋 Lab Overview

This is the second lab assignment in CS 4910. Building on the foundational concepts from Lab 1, you will:

- 🔢 Explore information theory and entropy calculations in security contexts
- 🔐 Analyze cryptographic systems including digital envelopes and authentication
- 🔑 Investigate password security and brute force attack resistance
- ⚖️ Compare symmetric encryption algorithms (DES vs AES)
- 🛠️ Implement practical security analysis tools
- 🤖 **Leverage AI tools to enhance understanding of complex cryptographic concepts**
- ✅ **Use AI to validate mathematical calculations and explore theoretical implications**

**⏱️ Estimated Time:** 5-7 hours  
**📅 Due Date:** [To be announced by instructor]

---

## 🎯 Learning Objectives

By the end of this lab, you will be able to:

1. ✅ Calculate and interpret information entropy in security contexts
2. ✅ Design and analyze digital envelope systems for confidentiality and authentication
3. ✅ Evaluate password strength using entropy and brute force analysis
4. ✅ Compare the security properties of different symmetric encryption algorithms
5. ✅ Implement practical tools for cryptographic analysis
6. ✅ Apply information theory principles to network security scenarios
7. 🤖 **Use AI tools to verify complex mathematical calculations and explore edge cases**
8. 🤖 **Leverage AI to understand the theoretical foundations of cryptographic security**
9. 📝 **Document AI-assisted learning and demonstrate enhanced comprehension**

---

## 📚 Prerequisites

- ✅ Completion of Lab 1 (AWS environment setup and basic security concepts)
- ✅ Basic understanding of probability and mathematics
- ✅ Familiarity with cryptographic hash functions and digital certificates
- 🤖 **Access to AI tools (ChatGPT, Claude, Gemini, or similar) for mathematical verification and concept exploration**

---

## 🤖 AI Integration Philosophy

This lab extends AI integration to **mathematical verification and theoretical exploration**. You are encouraged to:

- 🔍 **Use AI to verify entropy calculations and mathematical derivations**
- 🧠 **Explore theoretical implications of cryptographic design choices**
- 🎯 **Generate additional test cases for security analysis**
- ✅ **Validate your understanding of complex cryptographic concepts**
- 📝 **Document mathematical reasoning with AI assistance**

> **⚠️ Note:** While AI assistance is encouraged for verification and exploration, your final calculations and analysis must demonstrate your own mathematical understanding.

### 🎯 Enhanced AI Usage Principles
- **🔢 Mathematical Verification**: Use AI to check calculations and explore mathematical concepts
- **🧠 Theoretical Exploration**: Leverage AI to understand deeper implications of security principles
- **🎲 Scenario Generation**: Use AI to create additional test cases and edge scenarios
- **✅ Concept Validation**: Verify your understanding through AI-guided discussions
- **📝 Documentation Enhancement**: Use AI to help articulate complex technical concepts clearly

---

## 📊 Part 1: Information Theory and Entropy Analysis (25 points)

### 1.1 📖 Theory: Information Entropy in Security

**Information Entropy** measures the uncertainty or randomness in a system:
- **Formula**: `H(X) = -Σ p(x) log₂ p(x)`
- **Security Relevance**: Higher entropy indicates better unpredictability
- **Applications**: Password strength, cryptographic key quality, random number generation

**🔑 Key Concepts:**
- **Uniform Distribution**: Maximum entropy for given number of outcomes
- **Entropy and Security**: Relationship between randomness and cryptographic strength
- **Practical Applications**: Key generation, password policies, secure communications

### 1.2 🤖 Entropy Calculation with AI Verification

**AI-Enhanced Learning Process:**
1. **🔍 Concept Exploration**: Use AI to understand entropy's role in security
2. **🔢 Mathematical Verification**: Have AI check your entropy calculations
3. **🛡️ Security Implications**: Explore with AI how entropy affects system security
4. **🎯 Edge Case Analysis**: Use AI to generate and analyze additional scenarios

**💬 AI Verification Prompts:**
```
"I'm calculating information entropy for a security scenario. Can you help me:
1. Verify my entropy calculation: H(X) = -Σ p(x) log₂ p(x)
2. Explain why higher entropy means better security
3. What are the security implications of low entropy in cryptographic systems?
4. Generate similar scenarios to test my understanding"
```

### 1.3 🛠️ Practical Entropy Analysis

Use the interactive entropy analysis script (`entropy_analysis.py`) to solve:

**🎲 Scenario A: Balls in a Bin (Security Token Selection)**
Simulate a security token system with colored tokens:
- 4 red tokens, 2 yellow tokens, 3 green tokens
- Calculate entropy for single selection and multiple selections
- Analyze how adding/removing tokens affects security

**📡 Scenario B: Network Communication Entropy**
Analyze entropy in communication systems:
- Uniform letter distribution vs. English language patterns
- Impact of headers and multiple senders on information entropy
- Security implications of predictable vs. random communication patterns

### 1.4 📝 Assignment Tasks

**📋 Task 1.1: Token System Analysis**
- **a.** Calculate entropy for initial token distribution (4 red, 2 yellow, 3 green)
- **b.** Calculate entropy for five independent selections
- **c.** Analyze entropy change when adding 2 yellow tokens
- **d.** Determine optimal action to maximize entropy (security)
- **e.** Determine optimal action to minimize entropy (predictability)

**📋 Task 1.2: Communication Security Analysis**
- **a.** Calculate entropy for uniform English letter distribution
- **b.** Determine optimal bit encoding for efficient transmission
- **c.** Analyze entropy for 10-letter sequences vs. individual letters
- **d.** Compare English language entropy with uniform distribution
- **e.** Calculate entropy impact of sender identification headers
- **f.** Analyze multi-sender network entropy implications

**📤 Deliverable 1.1:**
- ✅ Complete entropy calculations with step-by-step work
- 📸 Screenshots of script output validating calculations
- 🔍 Analysis of security implications for each scenario
- 🤖 AI interaction log showing verification process

---

## 🔐 Part 2: Digital Envelope Systems and Authentication (25 points)

### 2.1 📖 Theory: Digital Envelopes and Hybrid Cryptography

**🔧 Digital Envelope Components:**
- **🔒 Symmetric Encryption**: Fast encryption of message content
- **🔑 Asymmetric Encryption**: Secure key exchange
- **✍️ Digital Signatures**: Authentication and non-repudiation
- **#️⃣ Hash Functions**: Message integrity verification

**🛡️ Security Properties Achieved:**
- **🔒 Confidentiality**: Through symmetric encryption
- **✅ Authentication**: Through digital signatures
- **🔍 Integrity**: Through cryptographic hashing
- **📝 Non-repudiation**: Through public key signatures

### 2.2 🤖 Digital Envelope Design with AI Assistance

**AI-Guided Design Process:**
1. **🏗️ Architecture Planning**: Use AI to explore different digital envelope designs
2. **🔍 Security Analysis**: Have AI help identify potential vulnerabilities
3. **✅ Protocol Verification**: Use AI to verify your protocol design
4. **⚔️ Attack Scenario Generation**: Explore potential attack vectors with AI

**💬 AI Design Prompts:**
```
"I'm designing a digital envelope system that provides both confidentiality and authentication. Can you help me:
1. What components are essential for a secure digital envelope?
2. How should the sender and receiver processes be structured?
3. What are potential vulnerabilities in digital envelope systems?
4. How can I verify that my design achieves all security goals?"
```

### 2.3 🛠️ Implementation and Analysis

Use the digital envelope simulation script (`digital_envelope.py`) to:

**📋 Design Requirements:**
- Implement both sender and receiver processes
- Achieve message confidentiality and sender authentication
- Include proper key management and verification
- Handle error cases and security failures

**🔍 Analysis Tasks:**
- Document the complete protocol flow
- Identify all cryptographic operations
- Analyze security properties achieved
- Evaluate potential attack vectors

**📤 Deliverable 2.1:**
- ✅ Complete digital envelope protocol design
- 💻 Implementation using provided script framework
- 🔍 Security analysis documenting achieved properties
- ⚔️ Attack vector analysis and mitigation strategies
- 📸 Screenshots of successful protocol execution

---

## 🔑 Part 3: Password Security and Brute Force Analysis (25 points)

### 3.1 📖 Theory: Password Security Metrics

**🔢 Password Strength Factors:**
- **📝 Character Set Size**: Number of possible characters
- **📏 Password Length**: Exponential impact on search space
- **📊 Entropy Calculation**: `H = log₂(N^L)` where N=charset size, L=length
- **⏱️ Time Complexity**: Expected brute force time analysis

**⚔️ Attack Models:**
- **🔨 Brute Force**: Systematic enumeration of all possibilities
- **📚 Dictionary Attacks**: Using common password lists
- **🔀 Hybrid Attacks**: Combining dictionary and brute force methods

### 3.2 🤖 Password Analysis with AI Enhancement

**AI-Enhanced Security Analysis:**
1. **💪 Strength Calculation**: Use AI to verify password entropy calculations
2. **⚔️ Attack Modeling**: Explore different attack scenarios with AI
3. **📋 Policy Development**: Use AI to design effective password policies
4. **🌍 Real-world Analysis**: Analyze actual password breach data with AI

**💬 AI Analysis Prompts:**
```
"I'm analyzing password security for different generation methods. Can you help me:
1. Calculate the entropy for passwords with specific character sets and lengths
2. Estimate brute force attack times for different computational capabilities
3. Compare the security of different password generation strategies
4. What are the trade-offs between usability and security in password policies?"
```

### 3.3 🧪 Password Security Laboratory

Use the password analysis script (`password_security.py`) to analyze:

**🎯 Scenario A: Traditional Password Analysis**
- 8-character passwords with mixed case, numbers, symbols
- Calculate search space and entropy
- Estimate brute force time with current technology

**🎯 Scenario B: Structured Password Generation**
- CVCN format (Consonant-Vowel-Consonant-Number) segments
- Two random segments for 8-symbol passwords
- Compare security with traditional approaches

**🎯 Scenario C: Advanced Encryption Impact**
- Compare DES vs AES-256 for password-based encryption
- Analyze how cipher strength affects overall security
- Evaluate the security improvement from algorithm upgrades

### 3.4 📝 Assignment Tasks

**📋 Task 3.1: Password Entropy Analysis**
- **a.** Calculate entropy for 8-character mixed-case alphanumeric passwords
- **b.** Estimate expected brute force search time
- **c.** Analyze CVCN-based password generation security
- **d.** Compare structured vs. random password approaches

**📋 Task 3.2: Encryption Algorithm Comparison**
- **a.** Analyze security implications of DES vs AES-256
- **b.** Calculate effective security improvement from algorithm upgrade
- **c.** Evaluate impact on password-based encryption systems

**📤 Deliverable 3.1:**
- ✅ Complete password entropy calculations
- ⏱️ Brute force time estimates with methodology
- 📊 Comparative analysis of password generation methods
- 🔐 Encryption algorithm security comparison
- 📸 Screenshots of analysis tool output

---

## ⚖️ Part 4: Symmetric Encryption Security Analysis (15 points)

### 4.1 📖 Theory: Symmetric Cipher Security

**🔑 Key Security Metrics:**
- **📏 Key Length**: Direct impact on brute force resistance
- **🏗️ Algorithm Design**: Resistance to cryptanalytic attacks
- **💻 Implementation Security**: Side-channel attack resistance
- **⚡ Performance vs. Security Trade-offs**

**🆚 DES vs AES Comparison:**
- **DES**: 56-bit effective key length, known vulnerabilities
- **AES-256**: 256-bit key length, current standard
- **📈 Security Margin**: Quantitative security improvement

### 4.2 🤖 Cipher Analysis with AI Exploration

**AI-Guided Cipher Analysis:**
1. **📚 Historical Context**: Use AI to understand cipher evolution
2. **🔢 Mathematical Analysis**: Explore the mathematics behind cipher security
3. **🛡️ Attack Resistance**: Analyze different types of cryptanalytic attacks
4. **🔮 Future Considerations**: Discuss quantum computing implications

**💬 AI Cipher Prompts:**
```
"I'm comparing DES and AES encryption algorithms. Can you help me understand:
1. What are the fundamental security differences between DES and AES?
2. How do key length differences translate to practical security improvements?
3. What types of attacks are these algorithms resistant to?
4. How do implementation considerations affect real-world security?"
```

### 4.3 🛠️ Practical Cipher Comparison

Use the cipher analysis script (`cipher_comparison.py`) to:
- Implement basic DES and AES operations
- Compare encryption/decryption performance
- Analyze key space and brute force resistance
- Evaluate security margins and practical implications

**📤 Deliverable 4.1:**
- 📊 Comparative analysis of DES vs AES security properties
- ⚡ Performance benchmarking results
- 📈 Security improvement quantification
- 💡 Practical implementation recommendations

---

## 🚀 Part 5: Advanced Cryptographic Concepts (10 points)

### 5.1 📖 Theory: Advanced Security Protocols

**🔧 Protocol Security Analysis:**
- **👥 Multi-party Communication**: Scaling security to multiple participants
- **🔑 Key Distribution**: Secure key sharing mechanisms
- **✅ Protocol Verification**: Formal methods for security validation
- **🌍 Real-world Implementation**: Practical security considerations

### 5.2 🤖 Advanced Analysis with AI

**AI-Enhanced Protocol Analysis:**
1. **🏗️ Protocol Design**: Use AI to explore advanced protocol structures
2. **📝 Security Proofs**: Understand formal security verification methods
3. **⚠️ Implementation Challenges**: Analyze real-world deployment issues
4. **🔮 Future Directions**: Explore emerging cryptographic techniques

### 5.3 🔬 Research and Analysis

Complete analysis of one advanced topic:
- 🔮 Post-quantum cryptography implications
- 🕵️ Zero-knowledge proof applications
- ⛓️ Blockchain security mechanisms
- 🌐 IoT device security protocols

**📤 Deliverable 5.1:**
- 📄 Research report on chosen advanced topic
- 🔍 Security analysis using established frameworks
- 🤖 AI-assisted exploration documentation
- 💡 Practical implementation considerations

---

## 📚 Textbook Problems Integration

*Problems from Computer Security: Principles and Practice, 4th Edition (Pages 84, 124-126)*

### 📖 Problem 2.9: Digital Envelope with Confidentiality and Authentication

**Problem Statement**: 
*"Build on the digital envelope in Figure 2.9. Provide a solution which achieves both message confidentiality and authentication. In addition to the textbook parts show and explain both the transmitter's and receiver's sides."*

#### 2.9.1 🤖 Digital Envelope Design with AI Enhancement

**AI-Enhanced Learning Process:**
1. **🔍 Concept Exploration**: Use AI to understand digital envelope components and security properties
2. **🔐 Protocol Design**: Have AI help design comprehensive transmitter/receiver protocols
3. **🛡️ Security Analysis**: Explore with AI how to achieve both confidentiality and authentication
4. **📊 Implementation Details**: Use AI to verify cryptographic operation sequences

**💬 AI Design Prompts:**
```
"I'm designing a digital envelope system that provides both confidentiality and authentication. Can you help me:
1. Explain the components needed for both security properties
2. Design the step-by-step transmitter protocol
3. Design the corresponding receiver protocol
4. Analyze potential vulnerabilities and countermeasures
5. Compare this approach with other hybrid cryptographic systems"
```

**Your Analysis Must Include**:
1. **Complete Transmitter Protocol**: Step-by-step process with all cryptographic operations
2. **Complete Receiver Protocol**: Corresponding decryption and verification steps
3. **Security Property Analysis**: How confidentiality and authentication are achieved
4. **Implementation Considerations**: Key management, algorithm choices, performance
5. **Vulnerability Assessment**: Potential attacks and mitigation strategies

### 📖 Problem 3.2: Pseudorandom Password Generator Analysis

**Problem Statement**: 
*"An early attempt to force users to use less predictable passwords involved computer-supplied passwords. These passwords were generated using a pseudorandom number generator. Suppose the passwords were nine-character long and were taken from the character set consisting of uppercase letters and digits so that the adversary has to search through all character strings of length 9 from a 36-character alphabet. Would a pseudorandom number generator with 2^16 possible starting values suffice? If yes, how? If not, then what should be the appropriate range for this pseudorandom number generator? In addition to the textbook parts, what is the estimated expected brute force search time using the same technology?"*

#### 3.2.1 🤖 Password Security Analysis with AI Verification

**AI-Enhanced Learning Process:**
1. **🔢 Mathematical Analysis**: Use AI to verify password space calculations
2. **🎯 Attack Modeling**: Have AI help model brute force attack scenarios
3. **⏱️ Time Estimation**: Explore with AI realistic attack timeframes
4. **🔐 Security Recommendations**: Use AI to develop appropriate security parameters

**💬 AI Analysis Prompts:**
```
"I'm analyzing pseudorandom password generator security. Can you help me:
1. Calculate the total password space for 9-character passwords from 36-character alphabet
2. Determine if 2^16 starting values provide adequate security
3. Calculate the appropriate range for secure password generation
4. Estimate brute force search times using current technology
5. What are the implications of predictable pseudorandom generators?"
```

**Your Analysis Must Include**:
1. **Password Space Calculation**: Total possible passwords (36^9)
2. **PRNG Analysis**: Whether 2^16 starting values suffice and why
3. **Appropriate Range Determination**: Recommended PRNG range for security
4. **Brute Force Time Estimation**: Expected search time with current technology
5. **Security Recommendations**: Best practices for password generation

### 📖 Problem 3.5: Phonetic Password Generator Analysis

**Problem Statement**: 
*"A phonetic password generator picks two segments randomly for each six-letter password. The form of each segment is CVC (consonant, vowel, consonant), where V = {a, e, i, o, u} and C = V̄.*
*a. What is the total password population?*
*b. What is the probability of an adversary guessing a password correctly?*
*In addition to the textbook parts, solve the following.*
*c. Repeat the two parts in the textbook with another password generator picking two segments randomly for an eight-symbol password. The form of each segment is CVCN (consonant, vowel, consonant, number) where the number is a decimal digit."*

#### 3.5.1 🤖 Phonetic Password Analysis with AI Enhancement

**AI-Enhanced Learning Process:**
1. **🔤 Character Set Analysis**: Use AI to understand consonant/vowel distributions
2. **🧮 Combinatorial Calculations**: Have AI verify password population calculations
3. **📊 Probability Analysis**: Explore with AI attack probability scenarios
4. **🔄 Pattern Comparison**: Use AI to compare CVC vs CVCN security

**💬 AI Calculation Prompts:**
```
"I'm analyzing phonetic password generators. Can you help me:
1. Calculate consonant and vowel counts in English alphabet
2. Determine total password population for CVC-CVC (6 characters)
3. Calculate guessing probability for the 6-character system
4. Analyze CVCN-CVCN system (8 symbols) password population
5. Compare security between CVC and CVCN approaches"
```

**Your Analysis Must Include**:
1. **Part (a) - CVC System**: Total password population calculation
2. **Part (b) - Attack Probability**: Probability of correct guess
3. **Part (c) - CVCN System**: Extended analysis for 8-symbol passwords
4. **Security Comparison**: CVC vs CVCN security properties
5. **Practical Implications**: Usability vs security trade-offs

### 📖 Problem 3.7: GPU-Based Password Cracking Analysis

**Problem Statement**: 
*"The NVIDIA Tesla K-20X GPU has 2688 cores, each operating at a 732-MHz frequency. Further, the GPU has 6 GB of DRAM with a bandwidth of 250 GB/sec that is shared among all the cores. If a password hashing scheme (PHS) takes 2 ms to compute a password:*
*a. How many passwords can be tested by the GPU in one hour if the PHS consumes no memory?*
*b. How many cores can work simultaneously if each hash computation requires 20 MB of DRAM? How many passwords can now be tested by the GPU in one hour?*
*In addition to the textbook parts, solve the following.*
*c. AES-256 is used instead of DES. Repeat the previous part b. Also, how does the security improve from the change in the symmetric cipher?"*

#### 3.7.1 🤖 GPU Performance Analysis with AI Verification

**AI-Enhanced Learning Process:**
1. **⚡ Performance Modeling**: Use AI to understand GPU parallel processing capabilities
2. **💾 Memory Constraint Analysis**: Have AI help analyze DRAM limitations
3. **🔐 Cipher Comparison**: Explore with AI security differences between DES and AES-256
4. **📈 Scalability Analysis**: Use AI to model attack scaling scenarios

**💬 AI Performance Prompts:**
```
"I'm analyzing GPU-based password cracking performance. Can you help me:
1. Calculate maximum passwords/hour with unlimited memory
2. Determine memory-constrained core utilization
3. Compare DES vs AES-256 computational requirements
4. Analyze the security improvement from cipher upgrade
5. What are the implications for password policy?"
```

**Your Analysis Must Include**:
1. **Part (a) - Unlimited Memory**: Maximum password testing rate
2. **Part (b) - Memory Constrained**: Active cores and reduced testing rate
3. **Part (c) - AES-256 Analysis**: Performance with stronger cipher
4. **Security Improvement Quantification**: DES to AES-256 security gain
5. **Practical Defense Recommendations**: Countermeasures against GPU attacks

### 📖 Problem 3.11: Biometric Authentication Protocol Analysis

**Problem Statement**: 
*"For the biometric authentication protocols illustrated in Figure 3.13, note the biometric capture device is authenticated in the case of a static biometric but not authenticated for a dynamic biometric. Explain why authentication is useful in the case of a stable biometric, but not needed in the case of a dynamic biometric."*

#### 3.11.1 🤖 Biometric Security Analysis with AI Enhancement

**AI-Enhanced Learning Process:**
1. **🔍 Protocol Comparison**: Use AI to understand static vs dynamic biometric differences
2. **🛡️ Threat Modeling**: Have AI help analyze attack vectors for each approach
3. **🔐 Authentication Requirements**: Explore with AI when device authentication is necessary
4. **📊 Security Trade-offs**: Use AI to evaluate security vs usability implications

**💬 AI Biometric Analysis Prompts:**
```
"I'm analyzing biometric authentication protocols. Can you help me:
1. Explain the difference between static and dynamic biometric systems
2. Identify why device authentication matters for static biometrics
3. Analyze why dynamic biometrics don't require device authentication
4. What are the security implications of each approach?
5. How do replay attacks affect static vs dynamic biometric systems?"
```

**Your Analysis Must Include**:
1. **Static Biometric Analysis**: Why device authentication is essential
2. **Dynamic Biometric Analysis**: Why device authentication is unnecessary
3. **Threat Model Comparison**: Different attack vectors for each system
4. **Security Property Analysis**: How each approach achieves authentication goals
5. **Implementation Recommendations**: Best practices for each biometric type

---

### 🤖 AI-Enhanced Textbook Problem Solving

**For all textbook problems, use this comprehensive AI integration approach:**

#### 📋 **AI Verification Process**
1. **Initial Understanding**: Use AI to clarify problem requirements
2. **Mathematical Verification**: Have AI check all calculations
3. **Concept Exploration**: Explore deeper implications with AI assistance
4. **Alternative Approaches**: Use AI to suggest different solution methods
5. **Practical Applications**: Discuss real-world relevance with AI

#### 💬 **Standard AI Prompts for Each Problem**
```
"I'm solving textbook problem [X.Y]. Can you help me:
1. Verify my understanding of the problem requirements
2. Check my mathematical calculations and methodology
3. Suggest alternative approaches or considerations
4. Explain the practical security implications
5. Identify any edge cases or special considerations"
```

#### 📝 **Documentation Requirements**
- **Problem Restatement**: Clear articulation of what you're solving
- **Solution Methodology**: Step-by-step approach with AI verification
- **Mathematical Work**: All calculations with AI cross-checking
- **AI Interaction Logs**: Document your AI conversations and insights
- **Security Analysis**: Practical implications and recommendations
- **Alternative Approaches**: AI-suggested alternative solutions or considerations

---

## 📤 Submission Requirements

### 📁 File Structure
Create the following directory structure on your AWS instance:

```
~/CS4910-Lab2/
├── scripts/
│   ├── entropy_analysis.py
│   ├── digital_envelope.py
│   ├── password_security.py
│   ├── cipher_comparison.py
│   └── advanced_analysis.py
├── outputs/
│   ├── entropy/
│   │   └── entropy_calculations.txt
│   ├── digital_envelope/
│   │   └── protocol_analysis.txt
│   ├── password/
│   │   └── password_security_analysis.txt
│   ├── cipher/
│   │   └── cipher_comparison_results.txt
│   └── advanced/
│       └── advanced_topic_analysis.txt
├── screenshots/
│   ├── entropy_analysis.png
│   ├── digital_envelope_demo.png
│   ├── password_analysis.png
│   ├── cipher_comparison.png
│   └── advanced_analysis.png
├── ai_interactions/
│   ├── entropy_ai_verification.md
│   ├── digital_envelope_ai_design.md
│   ├── password_ai_analysis.md
│   ├── cipher_ai_exploration.md
│   └── advanced_ai_research.md
├── textbook_problems/
│   ├── problem_2_9_solution.md
│   ├── problem_3_2_solution.md
│   ├── problem_3_5_solution.md
│   ├── problem_3_7_solution.md
│   └── problem_3_11_solution.md
└── lab_report.md
```

### ✅ Submission Checklist
- [ ] All entropy calculations completed with verification
- [ ] Digital envelope system designed and implemented
- [ ] Password security analysis completed with multiple methods
- [ ] Cipher comparison analysis with quantitative results
- [ ] Advanced topic research and analysis completed
- [ ] All textbook problems solved with detailed explanations
- [ ] AI interaction logs comprehensive and insightful
- [ ] Screenshots captured for all major analyses
- [ ] All files organized in required directory structure
- [ ] Comprehensive lab report with findings and recommendations

---

## 📊 Unified Grading Rubric (100 Points Total)

### 1. 🔢 Mathematical Analysis and Calculations (35 points)
*Includes entropy calculations, password analysis, cipher comparisons, and textbook problems*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 32-35 | All calculations correct with clear methodology, comprehensive analysis, excellent problem-solving approach |
| **Good** | 25-31 | Most calculations correct, good analytical approach, minor errors in methodology |
| **Satisfactory** | 18-24 | Basic calculations completed, adequate analysis, some mathematical errors |
| **Needs Improvement** | 0-17 | Major calculation errors, poor analytical approach, incomplete problem solutions |

### 2. 🔐 Cryptographic System Design and Analysis (30 points)
*Includes digital envelope design, security protocol analysis, and system implementation*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 27-30 | Sophisticated system design, thorough security analysis, excellent implementation with proper error handling |
| **Good** | 21-26 | Good system design, solid security analysis, functional implementation with minor issues |
| **Satisfactory** | 15-20 | Basic system design, adequate security analysis, working implementation with some problems |
| **Needs Improvement** | 0-14 | Poor system design, inadequate security analysis, non-functional or severely flawed implementation |

### 3. 🤖 AI Integration and Enhanced Learning (25 points)
*Includes AI usage for verification, exploration, and enhanced understanding*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 23-25 | Sophisticated AI usage for mathematical verification and concept exploration, detailed interaction logs, demonstrates critical evaluation of AI responses, novel insights generated through AI collaboration |
| **Good** | 18-22 | Effective AI usage with good documentation, evidence of enhanced understanding through AI interaction, appropriate verification of AI-provided information |
| **Satisfactory** | 13-17 | Basic AI usage documented, some evidence of enhanced learning, minimal but acceptable AI integration |
| **Needs Improvement** | 0-12 | Poor or minimal AI usage, inadequate documentation, no evidence of enhanced learning through AI |

### 4. 📝 Technical Documentation and Communication (10 points)
*Includes lab report, code documentation, and clear explanation of concepts*

| Grade | Points | Description |
|-------|--------|-------------|
| **Excellent** | 9-10 | Professional documentation, clear technical communication, comprehensive explanations |
| **Good** | 7-8 | Good documentation quality, mostly clear explanations, minor communication issues |
| **Satisfactory** | 5-6 | Adequate documentation, basic explanations, some clarity issues |
| **Needs Improvement** | 0-4 | Poor documentation, unclear explanations, major communication problems |

---

## 📚 Additional Resources

### 📖 Recommended Reading
- Textbook Chapter 2: Cryptographic Tools
- Textbook Chapter 3: User Authentication
- NIST Guidelines on Password Security
- Information Theory and Cryptography research papers

### 🌐 Online Tools and References
- Online entropy calculators for verification
- Cryptographic algorithm comparison tools
- Password strength testing utilities
- Academic papers on information theory applications in security

### 🤖 AI Learning Enhancement
- Use AI to explore mathematical proofs and derivations
- Generate additional practice problems and scenarios
- Verify complex calculations and explore edge cases
- Research current developments in cryptographic security

---

## 🎓 Academic Integrity and AI Usage

### ✅ Acceptable AI Usage
- 🔢 Mathematical verification and calculation checking
- 🧠 Concept exploration and theoretical understanding
- 🎯 Additional scenario generation for practice
- 📝 Documentation and explanation enhancement
- 🔬 Research assistance for advanced topics

### 📝 Required Documentation
- All AI interactions must be logged and included in submission
- Specific prompts and responses should be documented
- Analysis of AI-provided information and your verification process
- Reflection on how AI enhanced your learning experience

### 🎯 Academic Integrity
- Your final analysis and conclusions must be your own work
- AI assistance must be clearly documented and attributed
- Mathematical calculations must show your understanding
- Critical thinking and analysis cannot be outsourced to AI

---

> **📝 Note:** This lab builds upon concepts from Lab 1 and prepares you for advanced topics in computer security. The integration of AI tools is designed to enhance your learning experience while maintaining academic rigor and personal understanding development.