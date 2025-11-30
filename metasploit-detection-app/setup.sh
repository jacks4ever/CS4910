#!/bin/bash

# Metasploit Attack Detection System - Setup Script
# Automated installation and configuration

set -e

echo "=============================================="
echo "Metasploit Attack Detection System - Setup"
echo "=============================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "⚠️  Note: This script doesn't need root, but running the app will require sudo"
fi

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
else
    echo -e "${RED}✗${NC} Python 3 is not installed"
    exit 1
fi

# Navigate to backend directory
cd "$(dirname "$0")/backend"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${YELLOW}!${NC} Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓${NC} pip upgraded"

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✓${NC} Dependencies installed"

# Check for libpcap (needed for scapy)
echo ""
echo "Checking for libpcap..."
if ldconfig -p | grep -q libpcap; then
    echo -e "${GREEN}✓${NC} libpcap found"
else
    echo -e "${YELLOW}!${NC} libpcap not found. Installing..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update > /dev/null 2>&1
        sudo apt-get install -y libpcap-dev python3-dev > /dev/null 2>&1
        echo -e "${GREEN}✓${NC} libpcap installed"
    elif command -v yum &> /dev/null; then
        sudo yum install -y libpcap-devel python3-devel > /dev/null 2>&1
        echo -e "${GREEN}✓${NC} libpcap installed"
    else
        echo -e "${RED}✗${NC} Please install libpcap manually"
    fi
fi

# Get network interfaces
echo ""
echo "Available network interfaces:"
if command -v ip &> /dev/null; then
    ip -o link show | awk -F': ' '{print "  - " $2}'
elif command -v ifconfig &> /dev/null; then
    ifconfig | grep "^[a-z]" | awk '{print "  - " $1}' | sed 's/:$//'
fi

# Create startup script
echo ""
echo "Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/backend"
source venv/bin/activate
sudo venv/bin/python3 app.py
EOF
chmod +x start.sh
echo -e "${GREEN}✓${NC} Startup script created"

# Summary
echo ""
echo "=============================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=============================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start the backend (in one terminal):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   sudo python3 app.py"
echo ""
echo "2. Start the frontend (in another terminal):"
echo "   cd frontend"
echo "   python3 -m http.server 8080"
echo ""
echo "3. Open browser and visit:"
echo "   http://localhost:8080"
echo ""
echo "=============================================="
echo -e "${YELLOW}IMPORTANT: Always serve frontend via HTTP!${NC}"
echo -e "${YELLOW}Do NOT open as file:// - causes connection issues${NC}"
echo "=============================================="
