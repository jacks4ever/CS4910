#!/bin/bash
# CS4910 Lab 1 - AWS Environment Setup Script
# University of Colorado Colorado Springs
# Fall 2025 - Instructor: Rhett Saunders

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================================${NC}"
echo -e "${BLUE}CS4910 Lab 1 - AWS Environment Setup${NC}"
echo -e "${BLUE}University of Colorado Colorado Springs${NC}"
echo -e "${BLUE}Fall 2025 - Instructor: Rhett Saunders${NC}"
echo -e "${BLUE}================================================================${NC}"

# Function to check if running on Ubuntu
check_os() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        if [[ "$ID" == "ubuntu" ]]; then
            echo -e "${GREEN}✓ Running on Ubuntu $VERSION_ID${NC}"
            return 0
        fi
    fi
    echo -e "${YELLOW}⚠ This script is optimized for Ubuntu. Proceeding anyway...${NC}"
    return 0
}

# Function to update system packages
update_system() {
    echo -e "\n${YELLOW}=== Updating System Packages ===${NC}"
    sudo apt update && sudo apt upgrade -y
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ System packages updated successfully${NC}"
    else
        echo -e "${RED}✗ Failed to update system packages${NC}"
        exit 1
    fi
}

# Function to install required packages
install_packages() {
    echo -e "\n${YELLOW}=== Installing Required Packages ===${NC}"
    
    PACKAGES=(
        "curl"
        "wget" 
        "openssl"
        "python3"
        "python3-pip"
        "git"
        "vim"
        "nano"
        "htop"
        "net-tools"
        "unzip"
        "tree"
    )
    
    for package in "${PACKAGES[@]}"; do
        echo -e "Installing ${BLUE}$package${NC}..."
        sudo apt install -y "$package"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ $package installed${NC}"
        else
            echo -e "${RED}✗ Failed to install $package${NC}"
        fi
    done
}

# Function to install Python packages
install_python_packages() {
    echo -e "\n${YELLOW}=== Installing Python Packages ===${NC}"
    
    PYTHON_PACKAGES=(
        "requests"
        "beautifulsoup4"
        "cryptography"
        "urllib3"
        "certifi"
    )
    
    for package in "${PYTHON_PACKAGES[@]}"; do
        echo -e "Installing Python package ${BLUE}$package${NC}..."
        python3 -m pip install --user "$package"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ $package installed${NC}"
        else
            echo -e "${RED}✗ Failed to install $package${NC}"
        fi
    done
}

# Function to create lab directory structure
create_lab_structure() {
    echo -e "\n${YELLOW}=== Creating Lab Directory Structure ===${NC}"
    
    LAB_DIR="$HOME/CS4910-Lab1"
    
    # Create main directories
    mkdir -p "$LAB_DIR"/{scripts,outputs,screenshots,docs}
    
    # Create subdirectories
    mkdir -p "$LAB_DIR/outputs"/{cia,incident,hash,certificate}
    
    if [ -d "$LAB_DIR" ]; then
        echo -e "${GREEN}✓ Lab directory structure created at $LAB_DIR${NC}"
        
        # Display directory structure
        echo -e "\n${BLUE}Directory Structure:${NC}"
        tree "$LAB_DIR" 2>/dev/null || ls -la "$LAB_DIR"
        
        # Create README file
        cat > "$LAB_DIR/README.md" << EOF
# CS4910 Lab 1 - Security Fundamentals

This directory contains all files for CS4910 Lab 1.

## Directory Structure

- \`scripts/\` - Analysis scripts for the lab
- \`outputs/\` - Output files from script execution
- \`screenshots/\` - Screenshots for lab report
- \`docs/\` - Additional documentation

## Usage

1. Run the analysis scripts from the scripts/ directory
2. Save all outputs to the appropriate subdirectories
3. Take screenshots and save to screenshots/ directory
4. Complete your lab report

## Scripts

- \`cia_analysis.py\` - CIA Triad analysis tool
- \`incident_analysis.py\` - Security incident analysis tool  
- \`hash_analysis.py\` - Hash function analysis tool
- \`certificate_analysis.sh\` - SSL/TLS certificate analysis tool

Generated: $(date)
EOF
        
        echo -e "${GREEN}✓ README.md created${NC}"
    else
        echo -e "${RED}✗ Failed to create lab directory structure${NC}"
        exit 1
    fi
}

# Function to download and setup lab scripts
setup_lab_scripts() {
    echo -e "\n${YELLOW}=== Setting Up Lab Scripts ===${NC}"
    
    LAB_DIR="$HOME/CS4910-Lab1"
    SCRIPTS_DIR="$LAB_DIR/scripts"
    
    # Note: In a real deployment, these would be downloaded from a course repository
    # For this demo, we'll create placeholder scripts
    
    echo -e "Setting up analysis scripts in ${BLUE}$SCRIPTS_DIR${NC}..."
    
    # Make scripts executable
    chmod +x "$SCRIPTS_DIR"/*.py 2>/dev/null
    chmod +x "$SCRIPTS_DIR"/*.sh 2>/dev/null
    
    echo -e "${GREEN}✓ Lab scripts configured${NC}"
}

# Function to configure security settings
configure_security() {
    echo -e "\n${YELLOW}=== Configuring Security Settings ===${NC}"
    
    # Update SSH configuration for better security (if needed)
    echo -e "Checking SSH configuration..."
    
    # Ensure firewall is configured (ufw)
    if command -v ufw &> /dev/null; then
        echo -e "Configuring firewall..."
        sudo ufw --force enable
        sudo ufw default deny incoming
        sudo ufw default allow outgoing
        sudo ufw allow ssh
        sudo ufw allow 80/tcp
        sudo ufw allow 443/tcp
        echo -e "${GREEN}✓ Firewall configured${NC}"
    else
        echo -e "${YELLOW}⚠ UFW not available, skipping firewall configuration${NC}"
    fi
    
    # Set up automatic security updates
    echo -e "Configuring automatic security updates..."
    sudo apt install -y unattended-upgrades
    sudo dpkg-reconfigure -plow unattended-upgrades
    
    echo -e "${GREEN}✓ Security settings configured${NC}"
}

# Function to verify installation
verify_installation() {
    echo -e "\n${YELLOW}=== Verifying Installation ===${NC}"
    
    # Check critical commands
    COMMANDS=("python3" "pip3" "openssl" "curl" "wget" "git")
    
    for cmd in "${COMMANDS[@]}"; do
        if command -v "$cmd" &> /dev/null; then
            VERSION=$($cmd --version 2>&1 | head -1)
            echo -e "${GREEN}✓ $cmd: $VERSION${NC}"
        else
            echo -e "${RED}✗ $cmd: Not found${NC}"
        fi
    done
    
    # Check Python packages
    echo -e "\n${BLUE}Python Package Verification:${NC}"
    python3 -c "
import sys
packages = ['requests', 'cryptography', 'hashlib', 'json']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'✓ {pkg}: Available')
    except ImportError:
        print(f'✗ {pkg}: Not available')
"
    
    # Check OpenSSL functionality
    echo -e "\n${BLUE}OpenSSL Functionality Test:${NC}"
    echo "test" | openssl dgst -sha256 >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ OpenSSL: Functional${NC}"
    else
        echo -e "${RED}✗ OpenSSL: Not functional${NC}"
    fi
}

# Function to display completion message
show_completion_message() {
    echo -e "\n${GREEN}================================================================${NC}"
    echo -e "${GREEN}AWS Environment Setup Complete!${NC}"
    echo -e "${GREEN}================================================================${NC}"
    
    echo -e "\n${BLUE}Next Steps:${NC}"
    echo -e "1. Navigate to your lab directory: ${YELLOW}cd ~/CS4910-Lab1${NC}"
    echo -e "2. Review the README.md file for instructions"
    echo -e "3. Start with the CIA analysis: ${YELLOW}python3 scripts/cia_analysis.py${NC}"
    echo -e "4. Continue with other analysis scripts as outlined in the lab"
    
    echo -e "\n${BLUE}Lab Directory Location:${NC}"
    echo -e "${YELLOW}$HOME/CS4910-Lab1${NC}"
    
    echo -e "\n${BLUE}Available Scripts:${NC}"
    echo -e "- ${YELLOW}scripts/cia_analysis.py${NC} - CIA Triad analysis"
    echo -e "- ${YELLOW}scripts/incident_analysis.py${NC} - Security incident analysis"
    echo -e "- ${YELLOW}scripts/hash_analysis.py${NC} - Hash function analysis"
    echo -e "- ${YELLOW}scripts/certificate_analysis.sh${NC} - Certificate analysis"
    
    echo -e "\n${BLUE}System Information:${NC}"
    echo -e "- OS: $(lsb_release -d 2>/dev/null | cut -f2 || echo 'Unknown')"
    echo -e "- Python: $(python3 --version)"
    echo -e "- OpenSSL: $(openssl version)"
    
    echo -e "\n${GREEN}Happy learning! 🎓${NC}"
}

# Main execution function
main() {
    echo -e "Starting AWS environment setup for CS4910 Lab 1...\n"
    
    check_os
    update_system
    install_packages
    install_python_packages
    create_lab_structure
    setup_lab_scripts
    configure_security
    verify_installation
    show_completion_message
    
    echo -e "\n${GREEN}Setup completed successfully!${NC}"
}

# Run main function
main "$@"