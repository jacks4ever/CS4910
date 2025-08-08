# CS 4910 Lab 2 Scripts

This directory contains interactive Python scripts for CS 4910 Lab 2: Information Theory, Cryptography, and Security Analysis.

## Prerequisites

Before running these scripts, ensure you have the required Python packages installed:

```bash
pip install cryptography matplotlib numpy
```

## Script Descriptions

### 1. entropy_analysis.py
**Purpose**: Calculate and analyze information entropy in security contexts

**Features**:
- Balls in bin entropy calculations (from HW2 Problem 1)
- Communication entropy analysis (from HW2 Problem 2)
- Interactive entropy calculator
- Password entropy analysis
- Visualization tools

**Usage**:
```bash
python3 entropy_analysis.py
```

### 2. digital_envelope.py
**Purpose**: Implement and analyze digital envelope systems

**Features**:
- Complete digital envelope implementation
- Confidentiality and authentication demonstration
- Security property analysis
- Attack scenario simulations
- Interactive protocol demonstration

**Usage**:
```bash
python3 digital_envelope.py
```

### 3. password_security.py
**Purpose**: Analyze password security and brute force resistance

**Features**:
- Traditional password entropy analysis
- CVCN password generation analysis (from HW2 Problem 3.5)
- Brute force time estimation
- Password method comparison
- Interactive security calculator

**Usage**:
```bash
python3 password_security.py
```

### 4. cipher_comparison.py
**Purpose**: Compare symmetric encryption algorithms (DES vs AES)

**Features**:
- Key space analysis
- Brute force resistance comparison (from HW2 Problem 3.7)
- Performance benchmarking
- Security evolution analysis
- Quantum computing impact assessment

**Usage**:
```bash
python3 cipher_comparison.py
```

### 5. advanced_analysis.py
**Purpose**: Explore advanced cryptographic concepts

**Features**:
- Post-quantum cryptography analysis
- Zero-knowledge proofs overview
- Blockchain security mechanisms
- IoT device security challenges
- Homomorphic encryption concepts
- Secure multi-party computation

**Usage**:
```bash
python3 advanced_analysis.py
```

## Lab Integration

These scripts are designed to support the lab exercises and textbook problems:

- **Problem 2.9**: Use `digital_envelope.py` for digital envelope design
- **Problem 3.2**: Use `password_security.py` for brute force time estimation
- **Problem 3.5**: Use `password_security.py` for CVCN password analysis
- **Problem 3.7**: Use `cipher_comparison.py` for DES vs AES comparison

## AI Integration

All scripts are designed to work with AI tools for:
- Mathematical verification
- Concept exploration
- Additional scenario generation
- Security analysis validation

## Output and Documentation

Each script generates:
- Interactive analysis results
- Calculation verification
- Security assessments
- Educational explanations

Save outputs to the appropriate directories in your lab submission structure.

## Troubleshooting

### Common Issues

1. **Missing cryptography library**:
   ```bash
   pip install cryptography
   ```

2. **Missing matplotlib**:
   ```bash
   pip install matplotlib
   ```

3. **Permission errors**:
   ```bash
   chmod +x *.py
   ```

4. **Python version compatibility**:
   - Scripts require Python 3.6 or higher
   - Tested with Python 3.8+

### Getting Help

- Use the interactive help within each script
- Refer to the lab instructions for context
- Use AI tools to understand complex concepts
- Check the CS 4910 course materials

## Security Note

These scripts are for educational purposes only. Do not use the cryptographic implementations in production systems. Always use well-tested, standardized cryptographic libraries for real applications.