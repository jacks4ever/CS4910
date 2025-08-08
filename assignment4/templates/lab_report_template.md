# CS 4910 Lab 2: Information Theory, Cryptography, and Security Analysis
## Lab Report

**Student Name**: [Your Name]  
**Student ID**: [Your ID]  
**Date Submitted**: [Date]  
**Instructor**: Rhett Saunders  
**Semester**: Fall 2025  

---

## Executive Summary

[Provide a 2-3 paragraph summary of the lab, key findings, and learning outcomes]

---

## Part 1: Information Theory and Entropy Analysis (25 points)

### 1.1 Balls in Bin Analysis

**Problem Setup**:
- Initial configuration: 4 red, 2 yellow, 3 green balls
- Analysis of entropy changes with modifications

**Calculations and Results**:

**Part a: Initial Entropy**
- Probabilities: P(red) = [value], P(yellow) = [value], P(green) = [value]
- Entropy calculation: H(X) = -Σ p(x) log₂ p(x) = [value] bits
- [Show detailed calculation steps]

**Part b: Five Events Entropy**
- For independent events: H(5 events) = 5 × H(1 event) = [value] bits
- [Explain reasoning]

**Part c: Modified System (Adding 2 Yellow Balls)**
- New configuration: 4 red, 4 yellow, 3 green balls
- New probabilities: [values]
- New entropy: [value] bits
- [Show calculations]

**Part d: Maximizing Entropy**
- Analysis of all possible actions (add/remove each color)
- Optimal action: [action and color]
- Resulting entropy: [value] bits
- [Explain why this maximizes entropy]

**Part e: Minimizing Entropy**
- Optimal action: [action and color]
- Resulting entropy: [value] bits
- [Explain reasoning]

**AI Verification**:
- [Describe how you used AI to verify calculations]
- [Include key insights from AI interactions]

### 1.2 Communication Entropy Analysis

**Part a: Uniform English Letters**
- Character set size: 26
- Entropy per letter: log₂(26) = [value] bits
- [Show calculation]

**Part b: Efficient Bit Encoding**
- Bits needed per letter: ⌈log₂(26)⌉ = [value] bits
- [Explain efficient encoding]

**Part c: Ten-Letter Sequence Analysis**
- Total combinations: 26¹⁰ = [value]
- Bits for sequence: [value] bits
- Bits per letter in sequence: [value] bits
- [Compare with individual letter encoding]

**Part d: English Language Entropy Comparison**
- English language entropy (X): approximately [value] bits
- Comparison with uniform distribution: [analysis]
- Reasons for difference: [explain language structure effects]

**Part e: Single Sender with Header**
- Header entropy: 0 bits (no uncertainty)
- Message entropy: 10 × X = [value] bits
- Total entropy: [value] bits

**Part f: Multiple Senders (1024)**
- Header entropy: log₂(1024) = [value] bits
- Total entropy: [value] bits
- [Compare with single sender case]

**Security Implications**:
- [Discuss how entropy relates to security]
- [Analyze predictability vs. randomness trade-offs]

---

## Part 2: Digital Envelope Systems and Authentication (25 points)

### 2.1 Digital Envelope Design

**System Architecture**:
[Describe your digital envelope system design]

**Transmitter Process**:
1. [Step-by-step description of sender operations]
2. [Include cryptographic operations used]
3. [Explain key management]

**Receiver Process**:
1. [Step-by-step description of receiver operations]
2. [Include verification procedures]
3. [Explain error handling]

**Security Properties Achieved**:
- **Confidentiality**: [Explain how achieved]
- **Authentication**: [Explain how achieved]
- **Integrity**: [Explain how achieved]
- **Non-repudiation**: [Explain how achieved]

### 2.2 Implementation Results

**Script Output**:
[Include screenshots of successful digital envelope creation and opening]

**Performance Analysis**:
- Envelope size: [value] bytes
- Processing time: [measurements]
- [Compare with alternatives]

### 2.3 Security Analysis

**Attack Resistance**:
- Eavesdropping: [Analysis of resistance]
- Message tampering: [Analysis of detection]
- Signature forgery: [Analysis of prevention]
- Replay attacks: [Analysis and mitigation]

**AI-Enhanced Analysis**:
- [Describe AI assistance in security analysis]
- [Include additional attack scenarios explored with AI]

---

## Part 3: Password Security and Brute Force Analysis (25 points)

### 3.1 Traditional Password Analysis

**8-Character Mixed Password Analysis**:
- Character set size: [value]
- Total combinations: [value]
- Entropy: [value] bits
- Average brute force time: [value]
- [Show detailed calculations]

### 3.2 CVCN Password Analysis

**CVCN Format Analysis**:
- Consonants: [count] characters
- Vowels: [count] characters
- Digits: [count] characters

**Single CVCN Segment**:
- Combinations: [calculation] = [value]
- Entropy: [value] bits

**Two CVCN Segments (8 characters)**:
- Total combinations: [value]
- Entropy: [value] bits
- Brute force time: [value]

**Sample CVCN Passwords**:
- [List 5 generated passwords]

### 3.3 Comparative Analysis

**Security Comparison**:
[Create comparison table of different password methods]

| Method | Entropy (bits) | Combinations | Brute Force Time | Usability |
|--------|---------------|--------------|------------------|-----------|
| Traditional | [value] | [value] | [value] | [rating] |
| CVCN | [value] | [value] | [value] | [rating] |

**Recommendations**:
- [Provide security vs. usability analysis]
- [Recommend best practices]

### 3.4 Advanced Attack Analysis

**Brute Force Time Estimation (Problem 3.2)**:
- Current technology assumptions: [describe]
- Expected search time: [calculation and result]
- [Show methodology]

**AI Verification**:
- [Describe AI assistance in calculations]
- [Include additional scenarios explored]

---

## Part 4: Symmetric Encryption Security Analysis (15 points)

### 4.1 DES vs AES Comparison (Problem 3.7)

**Key Space Analysis**:
- DES effective key length: 56 bits
- AES-256 key length: 256 bits
- Security improvement factor: 2^(256-56) = 2^200

**Brute Force Resistance**:
[Create comparison table]

| Algorithm | Key Length | Key Space | Brute Force Time |
|-----------|------------|-----------|------------------|
| DES | 56 bits | 2^56 | [value] |
| AES-256 | 256 bits | 2^256 | [value] |

**Security Improvement Analysis**:
- Quantitative improvement: [analysis]
- Practical implications: [discussion]
- Implementation considerations: [analysis]

### 4.2 Performance vs Security Trade-offs

**Benchmark Results**:
[Include performance measurements from script]

**Analysis**:
- Performance impact of key length increase
- Security margin gained
- Practical deployment considerations

---

## Part 5: Advanced Cryptographic Concepts (10 points)

### 5.1 Chosen Advanced Topic: [Topic Name]

**Background and Motivation**:
- [Explain the problem this technology addresses]
- [Describe current limitations it overcomes]

**Technical Analysis**:
- [Core concepts and mechanisms]
- [Security properties provided]
- [Implementation challenges]

**Security Implications**:
- [Threat model analysis]
- [Attack resistance evaluation]
- [Comparison with alternatives]

**Future Prospects**:
- [Current adoption status]
- [Research directions]
- [Long-term viability]

**AI-Enhanced Research**:
- [Describe AI assistance in research]
- [Include novel insights discovered]
- [Verification of technical details]

---

## Textbook Problems Solutions

### Problem 2.9: Digital Envelope Enhancement

**Problem Statement**: [Copy from textbook]

**Solution**:
[Detailed solution with diagrams and explanations]

**Transmitter Side**:
[Step-by-step process]

**Receiver Side**:
[Step-by-step process]

**Security Analysis**:
[Verification of confidentiality and authentication]

### Problem 3.2: Brute Force Time Estimation

**Problem Statement**: [Copy from textbook]

**Solution**:
[Detailed calculations and methodology]

**Technology Assumptions**:
[Describe computational capabilities assumed]

**Results**:
[Present time estimates with justification]

### Problem 3.5: CVCN Password Analysis

**Problem Statement**: [Copy from textbook]

**Solution**:
[Complete analysis of CVCN password generation]

**Part c Solution**:
[Specific solution to additional part]

### Problem 3.7: AES vs DES Analysis

**Problem Statement**: [Copy from textbook]

**Solution**:
[Detailed comparison and security improvement analysis]

**Part c Solution**:
[AES-256 analysis and security improvement quantification]

### Problem 3.11: [Insert Problem Title from Textbook]

**Problem Statement**: [Copy complete problem statement from textbook]

**Solution**:
[Detailed solution following the same analytical approach as other problems]

**Analysis**:
[Include security implications and practical considerations]

**AI Assistance**:
[Document how AI helped with concept clarification and verification]

---

## AI Integration and Learning Enhancement

### AI Usage Summary

**Tools Used**:
- [List AI tools and their specific applications]

**Verification Methods**:
- [Describe how AI information was verified]
- [Cross-references with authoritative sources]

**Enhanced Learning Outcomes**:
- [Concepts better understood through AI assistance]
- [Mathematical verifications performed]
- [Additional insights gained]

### Critical Evaluation of AI Assistance

**Strengths**:
- [What AI did well in supporting learning]
- [Areas where AI provided valuable insights]

**Limitations**:
- [Areas where AI was insufficient or incorrect]
- [Concepts requiring human expertise]

**Learning Reflection**:
- [How AI changed your learning process]
- [Balance between AI assistance and independent thinking]

---

## Conclusions and Recommendations

### Key Findings

1. **Information Theory Applications**:
   - [Summarize entropy analysis insights]
   - [Security implications of randomness]

2. **Cryptographic System Design**:
   - [Digital envelope effectiveness]
   - [Trade-offs in security mechanisms]

3. **Password Security**:
   - [Comparative analysis results]
   - [Practical recommendations]

4. **Encryption Algorithm Evolution**:
   - [DES to AES transition analysis]
   - [Future-proofing considerations]

### Security Recommendations

1. [Practical security recommendations based on analysis]
2. [Best practices for implementation]
3. [Future considerations and emerging threats]

### Learning Outcomes

- [Personal learning achievements]
- [Skills developed through lab exercises]
- [Understanding of AI as a learning tool]

---

## References

1. [Textbook citations]
2. [Academic papers referenced]
3. [Online resources used for verification]
4. [AI tools and their versions]
5. [Course materials and lecture notes]

---

## Appendices

### Appendix A: Script Outputs
[Include relevant screenshots and output files]

### Appendix B: Detailed Calculations
[Include step-by-step mathematical work]

### Appendix C: AI Interaction Logs
[Reference to separate AI interaction documentation]

### Appendix D: Code Implementations
[Any custom code written for analysis]