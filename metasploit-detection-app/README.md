# Metasploit Attack Detection System 🛡️

A real-time web-based application that detects and visualizes Metasploit attacks for educational purposes. This tool helps cybersecurity students understand defensive security from the blue team perspective by showing live attack patterns, exploit signatures, and network anomalies.

## 🎯 Purpose

This application is designed for **CS4910 Security Course** to demonstrate:
- Real-time detection of common Metasploit exploits
- Network traffic analysis and anomaly detection
- Blue team defensive monitoring techniques
- Visual representation of attack patterns
- Understanding of various exploit signatures

## ✨ Features

### Attack Detection
- **EternalBlue (MS17-010)** - SMB exploit detection
- **MS08-067 Netapi** - Windows RPC vulnerability
- **VSFTPD Backdoor** - FTP backdoor exploitation
- **Tomcat Manager Deploy** - Application deployment attacks
- **Shellshock** - Bash environment variable injection
- **SQL Injection** - Database exploitation attempts
- **Reverse Shell** - Meterpreter callbacks
- **Port Scanning** - Network reconnaissance detection
- **SYN Flood** - Denial of service attacks

### Real-Time Dashboard
- Live attack feed with detailed information
- Severity classification (Critical, High, Medium, Low)
- Attack type statistics and breakdown
- Source/destination IP tracking
- WebSocket-based real-time updates
- Clean, professional UI for classroom projection

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **Root/Administrator privileges** (required for packet capture)
- Modern web browser (Chrome, Firefox, Edge)
- Network interface to monitor

### Installation

1. **Navigate to the project directory:**
```bash
cd /home/rhettsaunders/GitHub/CS4910/metasploit-detection-app
```

2. **Install Python dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

Alternatively, use a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Running the Application

#### 1. Start the Backend (Detection System)

**Important:** The backend requires root privileges to capture network packets.

```bash
cd backend
sudo python3 app.py
```

Or with virtual environment:
```bash
sudo /path/to/venv/bin/python3 app.py
```

You should see:
```
============================================================
Metasploit Attack Detection System - Backend
============================================================

NOTE: This application requires ROOT privileges to capture packets
Run with: sudo python3 app.py

Starting Flask-SocketIO server on http://0.0.0.0:5000
============================================================
Starting packet capture on interface: default
```

#### 2. Open the Frontend Dashboard

**Important:** Serve the frontend via HTTP to avoid CORS issues.

Open a new terminal and run:
```bash
cd frontend
python3 -m http.server 8080
```

Then open your browser and visit:
- **http://localhost:8080** (if on same machine)
- **http://YOUR_IP:8080** (from other devices on network)

**Note:** Do not open as `file://` - this will cause WebSocket connection failures due to browser security restrictions.

## 📊 Using the Dashboard

### Dashboard Components

1. **Status Bar**
   - System status indicator
   - Total detection count
   - Last update timestamp
   - Clear events button

2. **Live Attack Feed** (Left Panel)
   - Real-time attack alerts
   - Attack name and severity
   - Source/destination IPs
   - Detailed attack information
   - Timestamp for each event

3. **Severity Distribution** (Right Panel - Top)
   - Critical, High, Medium, Low counts
   - Color-coded severity levels

4. **Detectable Exploits** (Right Panel - Middle)
   - List of all monitored exploit signatures
   - Target ports for each exploit

5. **Attack Type Breakdown** (Right Panel - Bottom)
   - Top 10 most frequent attack types
   - Attack frequency counts

### Color Coding

- 🔴 **CRITICAL** - Red (Immediate threat, requires urgent response)
- 🟠 **HIGH** - Orange (Serious threat, needs attention)
- 🟡 **MEDIUM** - Yellow (Moderate risk, should be investigated)
- 🔵 **LOW** - Blue (Minor concern, informational)

## 🧪 Testing the System

### Simulated Attacks (For Testing)

⚠️ **Warning:** Only perform these tests in a controlled lab environment on systems you own or have permission to test.

#### 1. Port Scan Detection
```bash
# Using nmap (install if needed: sudo apt install nmap)
nmap -sS localhost -p 1-1000
```

#### 2. SYN Flood Simulation
```bash
# Using hping3 (install if needed: sudo apt install hping3)
sudo hping3 -S -p 80 --flood localhost
```

#### 3. Metasploit Exploits

If you have Metasploit installed:
```bash
msfconsole
use exploit/unix/ftp/vsftpd_234_backdoor
set RHOST <target-ip>
run
```

### Generate Test Traffic

Create a simple Python script to generate detectable patterns:

```python
#!/usr/bin/env python3
import socket
import time

# Test port scanning detection
def test_port_scan():
    print("Testing port scan detection...")
    for port in range(20, 100):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            sock.connect(('localhost', port))
            sock.close()
        except:
            pass
        time.sleep(0.01)

if __name__ == '__main__':
    test_port_scan()
```

## 🛠️ Configuration

### Network Interface

To specify a specific network interface to monitor:

Edit `backend/app.py` and modify the start call:
```python
detector.start(interface='eth0')  # Replace 'eth0' with your interface
```

List available interfaces:
```bash
ip link show  # Linux
ifconfig      # Linux/Mac
ipconfig      # Windows
```

### Adding Custom Exploit Signatures

Edit the `EXPLOIT_SIGNATURES` dictionary in `backend/app.py`:

```python
EXPLOIT_SIGNATURES = {
    'custom_exploit': {
        'name': 'Custom Exploit Name',
        'description': 'Description of the exploit',
        'ports': [80, 443],  # Target ports
        'pattern': b'\\x00\\x00',  # Byte pattern to detect
        'severity': 'HIGH'  # CRITICAL, HIGH, MEDIUM, LOW
    }
}
```

## 📁 Project Structure

```
metasploit-detection-app/
├── backend/
│   ├── app.py              # Flask server with attack detection
│   └── requirements.txt     # Python dependencies
└── frontend/
    ├── index.html          # Dashboard UI
    ├── style.css           # Styling
    └── app.js              # WebSocket client & UI logic
```

## 🔧 Troubleshooting

### "Permission denied" error
**Problem:** Packet capture requires root privileges.
**Solution:** Run with `sudo python3 app.py`

### Backend won't start
**Problem:** Port 5000 already in use.
**Solution:** Change the port in `app.py`:
```python
socketio.run(app, host='0.0.0.0', port=5001, debug=True)
```
And update `BACKEND_URL` in `frontend/app.js`.

### Frontend not connecting
**Problem:** WebSocket connection fails.
**Solution:** 
1. Verify backend is running: `curl http://localhost:5000/api/status`
2. Check browser console for errors
3. Ensure firewall allows connections on port 5000

### No attacks detected
**Problem:** No traffic being captured.
**Solution:**
1. Verify correct network interface
2. Check if running with root privileges
3. Generate test traffic (see Testing section)

### Scapy installation issues
**Problem:** Scapy fails to install.
**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev libpcap-dev

# macOS
brew install libpcap

# Then reinstall
pip install scapy
```

## 🎓 Educational Use

### Classroom Demonstration

1. **Project the dashboard** on a screen for students to see
2. **Run controlled attacks** from a Kali Linux VM
3. **Explain each detection** as it appears in real-time
4. **Discuss mitigation strategies** for each attack type

### Lab Exercise Ideas

- Have students identify attack patterns
- Compare blue team vs red team perspectives
- Analyze attack severity classifications
- Research CVEs for detected exploits
- Propose defensive countermeasures

### Learning Objectives

Students will learn:
- Network packet analysis fundamentals
- Common Metasploit exploit signatures
- Real-time threat detection techniques
- Blue team defensive strategies
- Security monitoring best practices

## ⚠️ Security Considerations

- **Lab Use Only:** This tool is for educational purposes in controlled environments
- **Root Access:** Requires elevated privileges - use caution
- **Network Impact:** Packet capture can affect network performance
- **Privacy:** Monitors all network traffic - use only on networks you control
- **False Positives:** Not all detections indicate actual attacks
- **Legal Compliance:** Ensure you have authorization to monitor network traffic

## 📝 Dependencies

### Backend
- **Flask 3.0.0** - Web framework
- **Flask-SocketIO 5.3.5** - WebSocket support
- **Flask-CORS 4.0.0** - Cross-origin resource sharing
- **Scapy 2.5.0** - Packet manipulation and capture
- **python-socketio 5.10.0** - Socket.IO protocol
- **eventlet 0.33.3** - Concurrent networking

### Frontend
- **Socket.IO Client 4.5.4** - WebSocket client (CDN)
- Vanilla JavaScript (no framework required)
- Modern CSS3

## 🤝 Contributing

For course improvements or bug fixes:
1. Test changes in a lab environment
2. Document any new exploit signatures
3. Update README with new features
4. Submit changes for review

## 📄 License

This project is created for CS4910 Security Course educational purposes.

## 👥 Credits

Developed for CS4910 - Computer Security Course
Blue Team Training & Defensive Security Education

## 📞 Support

For issues or questions:
- Check the Troubleshooting section
- Review course materials
- Contact course instructor
- Check system logs: `journalctl -xe`

## 🔄 Version History

**v1.0.0** (November 2025)
- Initial release
- 7 exploit signatures
- Port scan detection
- SYN flood detection
- Real-time WebSocket dashboard
- Severity classification

---

**Remember:** Always use this tool responsibly and only in authorized lab environments. Unauthorized network monitoring may violate laws and regulations.

🛡️ **Stay Safe. Stay Secure. Keep Learning.** 🛡️
