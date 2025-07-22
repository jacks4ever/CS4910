# CS 4910: Introduction to Computer Security
## Lab Assignment 1: Instructor Guide
**Fall 2025 Semester**  
**University of Colorado Colorado Springs**  
**Instructor: Rhett Saunders**

---

## Overview

This instructor guide provides comprehensive information for administering Lab 1 of CS4910. The lab combines theoretical security concepts with practical AWS cloud computing experience, giving students hands-on exposure to security analysis tools and methodologies.

---

## Learning Objectives Assessment

### Primary Objectives
1. **Cloud Security Setup** - Students demonstrate ability to securely configure AWS infrastructure
2. **CIA Triad Application** - Students apply fundamental security concepts to real-world scenarios
3. **Incident Analysis** - Students analyze actual security breaches using established frameworks
4. **Cryptographic Understanding** - Students explore hash function properties and collision resistance
5. **PKI Comprehension** - Students examine digital certificates and trust chains
6. **AI-Enhanced Learning** - Students effectively integrate AI tools to deepen understanding and accelerate learning

### Skills Developed
- AWS EC2 instance management and security configuration
- Command-line security tool usage (OpenSSL, Python scripts)
- Security framework application (CIA Triad, incident analysis)
- Technical writing and documentation
- Critical thinking about security trade-offs
- AI tool integration for enhanced learning and research
- Documentation of AI-assisted learning processes

---

## Pre-Lab Preparation

### AWS Account Setup
1. **Educational Credits**: Ensure students have AWS Educate accounts with sufficient credits
2. **Account Limits**: Verify students can launch t3.micro instances in their preferred region
3. **Support**: Prepare troubleshooting guide for common AWS issues

### Infrastructure Requirements
- **Instance Type**: t3.micro (free tier eligible)
- **AMI**: Ubuntu 22.04 LTS
- **Security Groups**: SSH (22), HTTP (80), HTTPS (443)
- **Key Pairs**: Students must create and securely store their key pairs

### Tool Verification
Ensure the following tools work in the lab environment:
- OpenSSL (certificate analysis)
- Python 3.8+ with required packages
- Network connectivity for certificate retrieval
- Git for potential script updates

---

## Unified Grading Rubric (100 Points Total)

This lab uses a comprehensive, unified rubric that evaluates both technical competency and AI-enhanced learning outcomes.

### Technical Implementation (40 points)

#### AWS Environment Setup (10 points)
- **Excellent (9-10)**: Instance properly configured, security groups correct, all tools installed, professional setup
- **Good (7-8)**: Minor configuration issues, mostly functional, good security practices
- **Satisfactory (5-6)**: Basic setup complete, some functionality missing, adequate security
- **Needs Improvement (0-4)**: Major setup problems, non-functional environment, security concerns

#### Script Execution and Results (15 points)
- **Excellent (14-15)**: All scripts run successfully, outputs captured and analyzed, comprehensive results
- **Good (11-13)**: Most scripts work, minor issues with outputs, good analysis
- **Satisfactory (8-10)**: Scripts run with some errors, basic outputs obtained, adequate analysis
- **Needs Improvement (0-7)**: Scripts fail to run or produce meaningful results, poor analysis

#### Tool Usage and Screenshots (15 points)
- **Excellent (14-15)**: Professional screenshots, proper tool usage demonstrated, excellent documentation
- **Good (11-13)**: Good screenshots, tools used correctly, solid documentation
- **Satisfactory (8-10)**: Basic screenshots, adequate tool usage, meets requirements
- **Needs Improvement (0-7)**: Poor screenshots, incorrect tool usage, inadequate documentation

### Analysis and Understanding (35 points)

#### CIA Triad Analysis (15 points)
- **Excellent (14-15)**: Thorough analysis, clear justifications, demonstrates deep understanding, excellent critical thinking
- **Good (11-13)**: Good analysis, mostly correct justifications, solid understanding
- **Satisfactory (8-10)**: Basic analysis, adequate understanding shown, meets requirements
- **Needs Improvement (0-7)**: Poor analysis, misunderstanding of concepts, weak reasoning

#### Security Incident Analysis (10 points)
- **Excellent (9-10)**: Current incident, comprehensive analysis, clear security implications, excellent framework application
- **Good (7-8)**: Good incident choice, solid analysis, proper framework usage
- **Satisfactory (5-6)**: Adequate incident analysis, basic understanding, meets requirements
- **Needs Improvement (0-4)**: Poor incident choice or analysis, weak framework application

#### Hash Function and Certificate Analysis (10 points)
- **Excellent (9-10)**: Clear understanding of concepts, thorough analysis, excellent mathematical reasoning
- **Good (7-8)**: Good grasp of concepts, adequate analysis, solid reasoning
- **Satisfactory (5-6)**: Basic understanding, minimal analysis, meets requirements
- **Needs Improvement (0-4)**: Poor understanding, inadequate analysis, weak reasoning

### AI Integration and Learning (15 points)

#### AI Usage Documentation (8 points)
- **Excellent (7-8)**: Detailed AI interaction logs, shows effective use of AI for learning, comprehensive documentation
- **Good (5-6)**: Good AI usage documentation, some learning enhancement shown, adequate records
- **Satisfactory (3-4)**: Basic AI usage documented, minimal enhancement shown
- **Needs Improvement (0-2)**: Minimal or no AI usage documentation, no clear learning benefit

#### AI-Enhanced Insights (7 points)
- **Excellent (6-7)**: AI interactions led to deeper understanding, novel insights generated, clear learning acceleration
- **Good (4-5)**: AI helped improve analysis quality, some insights gained
- **Satisfactory (2-3)**: Basic AI assistance utilized, minimal insights
- **Needs Improvement (0-1)**: AI usage did not enhance learning, no clear benefits

### Communication and Documentation (10 points)

#### Lab Report Quality (10 points)
- **Excellent (9-10)**: Clear, professional writing, comprehensive coverage, excellent organization, outstanding presentation
- **Good (7-8)**: Good writing quality, covers most requirements, well organized
- **Satisfactory (5-6)**: Adequate writing, meets basic requirements, acceptable organization
- **Needs Improvement (0-4)**: Poor writing quality, incomplete coverage, poor organization

**Total: 100 Points**

### AI Integration Assessment Guidelines

When evaluating AI integration, look for:
- **Documentation Quality**: Are AI interactions well-documented with clear prompts and responses?
- **Learning Enhancement**: Did AI usage lead to deeper understanding beyond traditional methods?
- **Critical Thinking**: Did students critically evaluate AI responses rather than blindly accepting them?
- **Insight Generation**: Did AI interactions produce novel insights or understanding?
- **Tool Effectiveness**: Did students use appropriate AI tools for different tasks?

---

## Common Student Issues and Solutions

### AWS-Related Issues

**Issue**: Students cannot connect to EC2 instance
- **Cause**: Incorrect security group configuration, wrong key pair, or network issues
- **Solution**: Verify security group allows SSH from student's IP, check key pair permissions (chmod 400)

**Issue**: "Permission denied" when using SSH key
- **Cause**: Incorrect file permissions on private key
- **Solution**: `chmod 400 keyfile.pem`

**Issue**: Instance not accessible after setup
- **Cause**: Firewall misconfiguration or service issues
- **Solution**: Check security groups, verify instance is running, check system logs

### Script-Related Issues

**Issue**: Python scripts fail to run
- **Cause**: Missing dependencies, Python version issues
- **Solution**: Verify Python 3.8+, install required packages with pip3

**Issue**: Certificate analysis fails
- **Cause**: Network connectivity, OpenSSL configuration, or target site issues
- **Solution**: Test with different domains, check network connectivity, verify OpenSSL installation

**Issue**: Hash analysis script runs slowly
- **Cause**: Large hash space for birthday attack simulation
- **Solution**: Reduce hash bits for demonstration (16-bit recommended)

### Conceptual Issues

**Issue**: Students struggle with CIA Triad application
- **Solution**: Provide additional examples, emphasize real-world consequences

**Issue**: Confusion about collision resistance types
- **Solution**: Use birthday paradox analogy, provide visual examples

**Issue**: Certificate chain understanding
- **Solution**: Draw trust hierarchy diagrams, explain CA role

---

## Assessment Guidelines

### Grading Philosophy
- **Process over Product**: Reward good methodology even if results aren't perfect
- **Learning Evidence**: Look for evidence of understanding, not just correct answers
- **Security Mindset**: Reward security-conscious thinking and practices

### Red Flags for Academic Integrity
- Identical script outputs across multiple students
- Unrealistic analysis completion times
- Copy-pasted text without understanding
- Missing intermediate files or screenshots

### Partial Credit Guidelines
- **AWS Setup**: Give partial credit for attempted configuration even if not perfect
- **Analysis Scripts**: Credit for script execution attempts and partial results
- **Written Analysis**: Credit for effort and partial understanding
- **Screenshots**: Accept alternative evidence if screenshots are problematic

---

## Extension Activities

For advanced students or those finishing early:

### Advanced AWS Security
- Configure AWS CloudTrail for audit logging
- Set up AWS Config for compliance monitoring
- Implement AWS Systems Manager for patch management

### Extended Cryptographic Analysis
- Compare hash function performance benchmarks
- Implement simple hash collision detection
- Analyze certificate revocation mechanisms

### Security Research
- Research recent PKI vulnerabilities
- Analyze certificate transparency logs
- Investigate DNS security extensions (DNSSEC)

---

## Lab Variations

### For Different Class Sizes

**Small Classes (< 20 students)**
- Individual AWS accounts and instances
- Detailed one-on-one troubleshooting
- Extended discussion of results

**Large Classes (> 50 students)**
- Shared AWS accounts with student sub-accounts
- Group troubleshooting sessions
- Automated grading for script outputs

### For Different Skill Levels

**Beginner-Friendly Modifications**
- Pre-configured AWS instances
- Simplified script interfaces
- Additional guided examples

**Advanced Modifications**
- Custom security group configurations
- Extended cryptographic analysis
- Research component on recent vulnerabilities

---

## Time Management

### Recommended Schedule
- **Week 1**: Lab assignment, AWS account setup
- **Week 2**: AWS instance configuration, begin analysis
- **Week 3**: Complete analysis scripts, documentation
- **Week 4**: Final report submission, peer review

### In-Class Time Allocation
- **30 minutes**: AWS setup troubleshooting
- **45 minutes**: Script execution and analysis
- **30 minutes**: Discussion of results and concepts
- **15 minutes**: Questions and wrap-up

---

## Resources for Students

### Official Documentation
- [AWS EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [OpenSSL Documentation](https://www.openssl.org/docs/)
- [Python Cryptography Library](https://cryptography.io/)

### Additional Learning Materials
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [RFC 5280 - Internet X.509 PKI Certificate](https://tools.ietf.org/html/rfc5280)
- [OWASP Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Video Tutorials
- AWS EC2 Getting Started
- OpenSSL Certificate Analysis
- Python Security Scripting

---

## Continuous Improvement

### Student Feedback Collection
- Post-lab survey on difficulty and clarity
- Technical issue tracking
- Suggestion collection for improvements

### Lab Evolution
- Update scripts based on student feedback
- Refresh security incidents for current relevance
- Adapt to new AWS features and pricing

### Assessment Refinement
- Analyze grade distributions
- Identify common misconceptions
- Adjust rubric based on student performance

---

## Appendix: Sample Solutions

### CIA Triad Analysis - ATM System
- **Confidentiality: 5/5** - PIN and financial data must be absolutely protected
- **Integrity: 5/5** - Transaction accuracy is critical for financial operations
- **Availability: 3/5** - Important for customer service but not life-critical

### Security Incident Example Analysis
**Incident**: SolarWinds Supply Chain Attack (2020)
- **Affected Properties**: Confidentiality, Integrity, Authenticity, Accountability
- **Impact Level**: 5/5 (Critical)
- **Analysis**: Nation-state attack compromising software supply chain affecting thousands of organizations

### Hash Function Theoretical Answers
**Question**: Is H(x) ≠ H(x') always true for x ≠ x'?
**Answer**: No, due to the pigeonhole principle. Infinite input space maps to finite output space, guaranteeing collisions exist mathematically.

---

**Document Version**: 1.0  
**Last Updated**: July 2025  
**Next Review**: December 2025