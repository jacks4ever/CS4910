# CS 4910 Lab 4 Scripts

This directory contains interactive Python scripts for CS 4910 Lab 4: Network Security and Intrusion Detection Systems.

## Prerequisites

These scripts use standard Python libraries and require no additional installations for basic functionality.

## Script Descriptions

### 1. syn_cookie_analyzer.py
**Purpose**: Analyze TCP SYN Cookie defense mechanisms (Problem 1)

**Features**:
- SYN cookie defense mechanism analysis
- True/False statement evaluation
- Unix system implementation guidance
- OS-specific configuration support

**Usage**:
```bash
python3 syn_cookie_analyzer.py
```

### 2. firewall_analyzer.py
**Purpose**: IP address discovery and firewall blocking implementation (Problem 2)

**Features**:
- Multi-method IP address discovery
- Firewall rule implementation
- IP blocking verification
- Cross-platform support (Linux, macOS, Unix)

**Usage**:
```bash
python3 firewall_analyzer.py
```

### 3. dos_calculator.py
**Purpose**: DoS and DDoS attack calculations (Problems 7.1 & 7.3)

**Features**:
- Classic DoS flood attack calculations
- Distributed DoS scaling analysis
- Botnet capacity analysis
- Attack comparison and assessment

**Usage**:
```bash
python3 dos_calculator.py
```

### 4. malware_analyzer.py
**Purpose**: Malware code fragment analysis (Problems 6.5 & 6.6)

**Features**:
- Document infection malware classification
- Web-based malicious code analysis
- Behavior analysis and impact assessment
- Malware type comparison

**Usage**:
```bash
python3 malware_analyzer.py
```

### 5. smtp_analyzer.py
**Purpose**: SMTP packet filtering rule analysis (Problems 9.5 & 9.6)

**Features**:
- Basic SMTP filtering rule analysis
- Enhanced filtering rule comparison
- Packet analysis against rule sets
- Security improvement assessment

**Usage**:
```bash
python3 smtp_analyzer.py
```

### 6. intrusion_detection_analyzer.py
**Purpose**: Tripwire intrusion detection system analysis (Problem 8.6)

**Features**:
- Tripwire HIDS advantages/disadvantages analysis
- File integrity monitoring simulation
- IDS deployment planning
- Hash function security analysis

**Usage**:
```bash
python3 intrusion_detection_analyzer.py
```

## Lab Integration

These scripts are designed to support the lab exercises and textbook problems:

- **Problem 1**: Use `syn_cookie_analyzer.py` for TCP SYN Cookie analysis
- **Problem 2**: Use `firewall_analyzer.py` for IP discovery and blocking
- **Problems 6.5 & 6.6**: Use `malware_analyzer.py` for malware code analysis
- **Problems 7.1 & 7.3**: Use `dos_calculator.py` for DoS attack calculations
- **Problem 8.6**: Use `intrusion_detection_analyzer.py` for Tripwire analysis
- **Problems 9.5 & 9.6**: Use `smtp_analyzer.py` for SMTP filtering analysis

## AI Integration

All scripts are designed to work with AI tools for:
- Network security implementation guidance
- Attack analysis and verification
- System configuration validation
- Security assessment and comparison

## Output and Documentation

Each script generates:
- Interactive analysis results
- JSON data files for detailed analysis
- Markdown reports for documentation
- Implementation guidance and verification

Save outputs to the appropriate directories in your lab submission structure.

## Troubleshooting

### Common Issues

1. **Permission errors**:
   ```bash
   chmod +x *.py
   ```

2. **Python version compatibility**:
   - Scripts require Python 3.6 or higher
   - Tested with Python 3.8+

3. **Network configuration issues**:
   - Some scripts require network access for IP discovery
   - Firewall scripts may require administrative privileges

### Getting Help

- Use the interactive help within each script
- Refer to the lab instructions for context
- Use AI tools to understand complex network security concepts
- Check the CS 4910 course materials

## Security Note

These scripts are for educational purposes only. The network security implementations and configurations should only be used in controlled lab environments. Always follow proper security practices and obtain appropriate permissions before implementing security measures on production systems.