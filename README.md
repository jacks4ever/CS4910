# CS 4910: Introduction to Computer Security - Lab 1

## Security Fundamentals and AWS Environment Setup

**University of Colorado Colorado Springs**  
**Fall 2025 Semester**  
**Instructor: Rhett Saunders**

---

## 📋 Overview

This repository contains the complete Lab Assignment 1 for CS4910: Introduction to Computer Security. The lab combines theoretical security concepts with practical hands-on experience using AWS cloud infrastructure and security analysis tools.

## 🎯 Learning Objectives

Students will:
- Set up and configure a secure AWS EC2 environment
- Apply the CIA Triad to real-world security scenarios
- Analyze actual security incidents using established frameworks
- Explore cryptographic hash functions and collision resistance
- Examine digital certificates and public key infrastructure
- Develop practical security analysis skills

## 📁 Repository Structure

```
CS4910-Lab1/
├── CS4910_Lab1_Security_Fundamentals.md    # Main lab assignment
├── CS4910_Lab1_Instructor_Guide.md         # Comprehensive instructor guide
├── CS4910_Lab1_Report_Template.md          # Student report template
├── scripts/                                # Analysis tools and scripts
│   ├── aws_setup.sh                       # AWS environment setup script
│   ├── cia_analysis.py                    # CIA Triad analysis tool
│   ├── incident_analysis.py               # Security incident analysis tool
│   ├── hash_analysis.py                   # Hash function analysis tool
│   └── certificate_analysis.sh            # SSL/TLS certificate analysis tool
└── README.md                              # This file
```

## 🚀 Quick Start

### For Students

1. **Read the Lab Assignment**: Start with `CS4910_Lab1_Security_Fundamentals.md`
2. **Set up AWS Environment**: Follow Part 1 of the lab assignment
3. **Run Setup Script**: Execute `bash aws_setup.sh` on your EC2 instance (no editing required)
4. **Customize Analysis Scripts**: Edit each template script with your own analysis data:
   - Replace placeholder values (0 ratings, "STUDENT:" text) with your analysis
   - Use AI assistance to help determine ratings and justifications
5. **Run Customized Scripts**: Execute your completed scripts to generate outputs
6. **Write Report**: Use `CS4910_Lab1_Report_Template.md` as your starting point

### For Instructors

1. **Review Instructor Guide**: Read `CS4910_Lab1_Instructor_Guide.md` thoroughly
2. **Prepare AWS Accounts**: Ensure students have access to AWS Educate credits
3. **Test Scripts**: Verify all analysis scripts work in your environment
4. **Customize as Needed**: Adapt the lab for your specific class requirements

## 🛠️ Technical Requirements

### AWS Infrastructure
- **Instance Type**: t3.micro (free tier eligible)
- **Operating System**: Ubuntu 22.04 LTS
- **Security Groups**: SSH (22), HTTP (80), HTTPS (443)
- **Network**: Public subnet with internet gateway access

### Software Dependencies
- Python 3.8+
- OpenSSL
- Required Python packages: `requests`, `cryptography`, `beautifulsoup4`
- Standard Linux utilities: `curl`, `wget`, `git`

## 📊 Lab Components

### Part 1: AWS Environment Setup (20 points)
- EC2 instance configuration
- Security group setup
- SSH key management
- Tool installation and verification

### Part 2: CIA Triad Analysis (25 points)
- Analysis of 5 security scenarios
- Application of Confidentiality, Integrity, Availability concepts
- Use of automated analysis script
- Critical thinking about security trade-offs

### Part 3: Security Incident Analysis (20 points)
- Research of recent security incident
- Application of security framework
- Analysis of affected security properties
- Written analysis and documentation

### Part 4: Hash Function Investigation (25 points)
- Theoretical understanding of collision resistance
- Practical demonstration of hash properties
- Birthday attack simulation
- Mathematical concept application

### Part 5: Public-Key Certificate Analysis (10 points)
- SSL/TLS certificate examination
- Digital signature verification
- Certificate chain analysis
- PKI concept application

## 📝 Script Workflow for Students

### Understanding the Two Types of Scripts

**1. Setup Script (No Editing Required)**
- `aws_setup.sh` - Run once to set up your environment
- Fully automated - just execute with `bash aws_setup.sh`

**2. Analysis Scripts (Customization Required)**
- These are **template scripts** that you must edit with your own analysis
- Each script contains placeholder values and "STUDENT:" comments
- You replace these with your actual analysis data
- Then run the customized script to generate outputs

### Student Workflow Example

```bash
# 1. Initial setup (run once, no editing)
bash aws_setup.sh

# 2. Navigate to lab directory
cd ~/CS4910-Lab1

# 3. Edit analysis scripts with your data
nano scripts/cia_analysis.py
# Replace all "STUDENT:" placeholders with your analysis

# 4. Run your customized script
python3 scripts/cia_analysis.py

# 5. Take screenshots of output for your report
```

## 🔧 Script Descriptions

### `aws_setup.sh` - Environment Setup (No Student Editing Required)
Automated setup script for AWS EC2 instances that:
- Updates Ubuntu 24.04 system packages
- Installs required tools and dependencies (Python 3.12+, OpenSSL, etc.)
- Creates standardized lab directory structure
- Configures security settings and firewall
- Verifies installation and functionality
- **Usage**: Students run once with `bash aws_setup.sh`

### `cia_analysis.py` - Template Script (Student Customization Required)
CIA Triad analysis framework that students must customize:
- **Template Structure**: Provides analysis functions and framework
- **Student Task**: Replace placeholder values with their own CIA ratings and justifications
- **Functionality**: Calculates risk scores, generates formatted output, saves results to JSON
- **Usage**: Students edit the script with their analysis, then run `python3 cia_analysis.py`

### `incident_analysis.py` - Template Script (Student Customization Required)
Security incident analysis framework that students must customize:
- **Template Structure**: Provides incident analysis framework and reporting functions
- **Student Task**: Add their chosen security incident details and analysis
- **Functionality**: Structures incident research, applies security property analysis
- **Usage**: Students edit with their incident data, then run to generate reports

### `hash_analysis.py` - Template Script (Student Customization Required)
Hash function analysis tool that students must customize:
- **Template Structure**: Provides hash analysis functions and birthday attack simulation
- **Student Task**: Configure hash experiments and analysis parameters
- **Functionality**: Demonstrates avalanche effect, simulates birthday attacks, compares algorithms
- **Usage**: Students customize experiments, then run to generate analysis results

### `certificate_analysis.sh` - Template Script (Student Customization Required)
SSL/TLS certificate analysis tool that students must customize:
- **Template Structure**: Provides certificate retrieval and analysis functions
- **Student Task**: Specify target domains and analysis parameters
- **Functionality**: Retrieves certificates, extracts key information, analyzes certificate chains
- **Usage**: Students edit target domains, then run `bash certificate_analysis.sh`

## 📈 Assessment and Grading

The lab uses a comprehensive rubric evaluating:
- **Technical Implementation** (40%): AWS setup, script execution, tool usage
- **Conceptual Understanding** (35%): Security concept application, analysis quality
- **Documentation and Communication** (25%): Report quality, screenshots, explanations

See the Instructor Guide for detailed grading rubrics and assessment guidelines.

## 🔒 Security Considerations

This lab emphasizes security best practices:
- Proper AWS security group configuration
- SSH key management and permissions
- Principle of least privilege
- Secure communication protocols
- Data protection and privacy

## 🆘 Troubleshooting

### Common Issues

**AWS Connection Problems**
- Verify security group allows SSH from your IP
- Check SSH key permissions (`chmod 400 keyfile.pem`)
- Ensure instance is running and accessible

**Script Execution Issues**
- Verify Python 3.8+ is installed
- Install missing dependencies with `pip3 install`
- Check file permissions for shell scripts

**Certificate Analysis Failures**
- Test network connectivity to target domains
- Verify OpenSSL installation
- Try alternative domains if target is unavailable

## 📚 Educational Resources

### Required Reading
- Lab assignment document
- Instructor-provided security frameworks
- AWS documentation for EC2 setup

### Supplementary Materials
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [RFC 5280 - Internet X.509 PKI Certificate](https://tools.ietf.org/html/rfc5280)
- [OWASP Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

## 🤝 Contributing

This lab is designed for educational use. Instructors are welcome to:
- Adapt scripts for their specific environments
- Modify scenarios for current relevance
- Extend analysis tools with additional features
- Share improvements with the community

## 📄 License

This educational material is provided for academic use. Please respect academic integrity policies when using these materials.

## 📞 Support

For technical issues or questions:
- **Students**: Contact your instructor during office hours
- **Instructors**: Refer to the comprehensive Instructor Guide
- **Technical Issues**: Check the troubleshooting section above

## 🔄 Version History

- **v1.0** (July 2025): Initial release for Fall 2025 semester
- Comprehensive lab with AWS integration
- Full script suite and documentation
- Instructor guide and assessment rubrics

---

## 🎓 Academic Integrity

This lab is designed to be completed individually unless otherwise specified by your instructor. While you may discuss concepts with classmates, all submitted work must be your own. Sharing scripts, outputs, or written analysis constitutes academic dishonesty.

---

**Happy Learning! 🚀**

*CS4910: Introduction to Computer Security*  
*University of Colorado Colorado Springs*  
*Fall 2025*