#!/bin/bash
# CS4910 Lab 1 - Virtual Environment Activation Script
# This script activates the Python virtual environment for the lab

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "================================================================================"
echo "CS4910 Lab 1 - Virtual Environment Activation"
echo "================================================================================"

# Check if virtual environment exists
VENV_PATH="$HOME/CS4910-Lab1/lab_venv"

if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}❌ Virtual environment not found at $VENV_PATH${NC}"
    echo -e "${YELLOW}Please run the AWS setup script first:${NC}"
    echo "  ./aws_setup.sh"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source "$VENV_PATH/bin/activate"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Virtual environment activated successfully!${NC}"
    echo -e "${GREEN}✓ Python path: $(which python3)${NC}"
    echo -e "${GREEN}✓ Pip path: $(which pip)${NC}"
    
    echo -e "\n${BLUE}Available packages:${NC}"
    pip list | grep -E "(requests|beautifulsoup4|lxml|cryptography)"
    
    echo -e "\n${YELLOW}You can now run the lab analysis scripts:${NC}"
    echo "  python3 cia_analysis.py"
    echo "  python3 incident_analysis.py"
    echo "  python3 hash_analysis.py"
    echo "  ./certificate_analysis.sh"
    
    echo -e "\n${YELLOW}To deactivate the virtual environment later, run:${NC}"
    echo "  deactivate"
    
    # Start a new shell with the virtual environment activated
    echo -e "\n${BLUE}Starting new shell with virtual environment activated...${NC}"
    exec bash
else
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi