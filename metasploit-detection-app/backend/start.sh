#!/bin/bash

# Metasploit Attack Detection System - Backend Auto-Start Script
# Automatically sets up venv, installs dependencies, and runs the application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}Metasploit Attack Detection System - Backend Startup${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}ERROR: This script must be run with sudo (root privileges required for packet capture)${NC}"
    echo -e "${YELLOW}Usage: sudo ./start.sh${NC}"
    exit 1
fi

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python ${PYTHON_VERSION} found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

# Activate virtual environment
echo ""
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓${NC} Virtual environment activated"

# Upgrade pip
echo ""
echo -e "${YELLOW}Upgrading pip...${NC}"
pip install --upgrade pip --quiet
echo -e "${GREEN}✓${NC} pip upgraded"

# Install/update requirements
echo ""
echo -e "${YELLOW}Installing dependencies from requirements.txt...${NC}"
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓${NC} Dependencies installed"
else
    echo -e "${RED}ERROR: requirements.txt not found${NC}"
    exit 1
fi

# Check for libpcap (needed for scapy)
echo ""
echo -e "${YELLOW}Checking system dependencies...${NC}"
if ldconfig -p 2>/dev/null | grep -q libpcap; then
    echo -e "${GREEN}✓${NC} libpcap found"
else
    echo -e "${YELLOW}!${NC} libpcap not found, attempting to install..."
    if command -v apt-get &> /dev/null; then
        apt-get update -qq
        apt-get install -y libpcap-dev python3-dev -qq
        echo -e "${GREEN}✓${NC} libpcap installed"
    elif command -v yum &> /dev/null; then
        yum install -y libpcap-devel python3-devel -qq
        echo -e "${GREEN}✓${NC} libpcap installed"
    else
        echo -e "${YELLOW}!${NC} Could not auto-install libpcap, manual installation may be required"
    fi
fi

# Run the application
echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}Starting Metasploit Attack Detection Backend...${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "${YELLOW}Press CTRL+C to stop the server${NC}"
echo ""

# Run with the virtual environment's Python
exec venv/bin/python3 app.py
