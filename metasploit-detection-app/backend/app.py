#!/usr/bin/env python3
"""
Metasploit Attack Detection System - Backend
Real-time monitoring and detection of common Metasploit attacks
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from scapy.all import sniff, IP, TCP, UDP, Raw, ICMP
from collections import defaultdict, deque
from datetime import datetime
import threading
import json
import re
import time
import socket
import netifaces

app = Flask(__name__)
app.config['SECRET_KEY'] = 'metasploit-detection-secret'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=False, engineio_logger=False)

# Store attack events (increased limit and allow unlimited storage)
attack_events = deque(maxlen=1000)  # Increased from 100 to 1000
connection_tracker = defaultdict(lambda: {'count': 0, 'last_seen': time.time()})
port_scan_tracker = defaultdict(lambda: {'ports': set(), 'first_seen': time.time()})

# Common Metasploit exploit patterns
EXPLOIT_SIGNATURES = {
    'ms17_010': {
        'name': 'EternalBlue (MS17-010)',
        'description': 'SMB exploit targeting Windows systems',
        'ports': [445, 139],
        'patterns': [  # Multiple patterns to detect various stages
            b'\xffSMB',  # SMB protocol identifier
            b'SMB',      # Generic SMB
            b'\x00\x00\x00\x31\xff\x53\x4d\x42',  # Original pattern
            b'NT LM 0.12',  # SMB negotiation
            b'\xfe\x53\x4d\x42',  # SMB2 header
        ],
        'severity': 'CRITICAL'
    },
    'ms08_067': {
        'name': 'MS08-067 Netapi',
        'description': 'Windows Server Service RPC exploit',
        'ports': [445],
        'pattern': b'\\x5c\\x00\\x5c\\x00',
        'severity': 'CRITICAL'
    },
    'vsftpd_backdoor': {
        'name': 'VSFTPD Backdoor',
        'description': 'VSFTPD 2.3.4 backdoor exploitation',
        'ports': [21],
        'pattern': b':)',
        'severity': 'HIGH'
    },
    'tomcat_mgr': {
        'name': 'Tomcat Manager Deploy',
        'description': 'Apache Tomcat Manager application deployment',
        'ports': [8080, 8180],
        'pattern': b'/manager/html',
        'severity': 'MEDIUM'
    },
    'shellshock': {
        'name': 'Shellshock (CVE-2014-6271)',
        'description': 'Bash environment variable injection',
        'ports': [80, 443],
        'pattern': b'() { :; };',
        'severity': 'CRITICAL'
    },
    'sql_injection': {
        'name': 'SQL Injection Attempt',
        'description': 'Database exploitation attempt',
        'ports': [3306, 1433, 5432],
        'pattern': b"' OR '1'='1",
        'severity': 'HIGH'
    },
    'reverse_shell': {
        'name': 'Reverse Shell Connection',
        'description': 'Meterpreter or reverse shell callback',
        'ports': [4444, 4445, 8080],
        'pattern': b'meterpreter',
        'severity': 'CRITICAL'
    }
}

class AttackDetector:
    def __init__(self):
        self.running = False
        self.sniffer_thread = None
        self.local_ips = self.get_local_ips()
        self.smb_tracker = defaultdict(lambda: {'count': 0, 'last_seen': 0, 'first_seen': 0})
        print(f"Local IPs detected: {self.local_ips}")
    
    def get_local_ips(self):
        """Get all local IP addresses of this machine"""
        local_ips = set()
        try:
            # Get hostname IPs
            hostname = socket.gethostname()
            local_ips.add(socket.gethostbyname(hostname))
            
            # Get all interface IPs
            for interface in netifaces.interfaces():
                addrs = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addrs:
                    for addr in addrs[netifaces.AF_INET]:
                        local_ips.add(addr['addr'])
        except Exception as e:
            print(f"Error getting local IPs: {e}")
            # Fallback to basic method
            local_ips.add('127.0.0.1')
            local_ips.add(socket.gethostbyname(socket.gethostname()))
        
        return local_ips
    
    def is_inbound_traffic(self, src_ip, dst_ip):
        """Check if traffic is inbound (external source to local destination)"""
        # Inbound = source is NOT local AND destination IS local
        return src_ip not in self.local_ips and dst_ip in self.local_ips
    
    def is_outbound_traffic(self, src_ip, dst_ip):
        """Check if traffic is outbound (local source to external destination)"""
        # Outbound = source IS local AND destination is NOT local
        return src_ip in self.local_ips and dst_ip not in self.local_ips
    
    def detect_reverse_shell(self, src_ip, dst_ip, dst_port):
        """Detect outbound reverse shell connections"""
        reverse_shell_ports = {4444, 4445, 8080}
        
        if dst_port in reverse_shell_ports and self.is_outbound_traffic(src_ip, dst_ip):
            # Track active connections for heartbeat
            connection_key = f"{src_ip}:{dst_ip}:{dst_port}"
            if not hasattr(self, 'reverse_shell_connections'):
                self.reverse_shell_connections = {}
            
            # Update or create connection tracking
            current_time = time.time()
            if connection_key not in self.reverse_shell_connections:
                # New connection detected
                port_names = {4444: 'Meterpreter default', 4445: 'Meterpreter alternate', 8080: 'HTTP/Meterpreter'}
                self.reverse_shell_connections[connection_key] = current_time
                return {
                    'type': 'reverse_shell',
                    'name': 'Reverse Shell Connection',
                    'description': f'Outbound connection to suspected C2 server',
                    'severity': 'CRITICAL',
                    'details': f'Connection to {dst_ip}:{dst_port} ({port_names.get(dst_port, "common reverse shell port")})'
                }
            else:
                # Existing connection - just update timestamp (heartbeat)
                self.reverse_shell_connections[connection_key] = current_time
        return None
        
    def detect_port_scan(self, src_ip, dst_port):
        """Detect port scanning activities"""
        current_time = time.time()
        tracker = port_scan_tracker[src_ip]
        tracker['ports'].add(dst_port)
        
        # Check for SQL database port scanning (SQLi reconnaissance)
        sql_ports = {3306, 1433, 5432}  # MySQL, MSSQL, PostgreSQL
        sql_ports_scanned = tracker['ports'].intersection(sql_ports)
        
        # Immediate detection for database port probing
        if dst_port in sql_ports:
            db_names = {3306: 'MySQL', 1433: 'MSSQL', 5432: 'PostgreSQL'}
            if len(sql_ports_scanned) >= 2:
                # Multiple database ports = definite SQLi reconnaissance
                return {
                    'type': 'sql_injection',
                    'name': 'SQL Injection Attempt',
                    'description': 'Multiple database port reconnaissance detected',
                    'severity': 'HIGH',
                    'details': f'Probing database ports: {", ".join(map(str, sorted(sql_ports_scanned)))}'
                }
            else:
                # Single database port = likely SQLi attempt
                return {
                    'type': 'sql_injection',
                    'name': 'SQL Injection Attempt',
                    'description': f'{db_names[dst_port]} database reconnaissance',
                    'severity': 'HIGH',
                    'details': f'Connection attempt to {db_names[dst_port]} port {dst_port}'
                }
        
        # If scanning multiple ports in short time
        if len(tracker['ports']) > 10 and (current_time - tracker['first_seen']) < 60:
            return {
                'type': 'port_scan',
                'name': 'Port Scan Detected',
                'description': f'Multiple ports scanned from {src_ip}',
                'severity': 'MEDIUM',
                'details': f'Scanned {len(tracker["ports"])} ports in last 60 seconds'
            }
        return None
    
    def detect_syn_flood(self, src_ip):
        """Detect SYN flood attacks"""
        current_time = time.time()
        tracker = connection_tracker[src_ip]
        tracker['count'] += 1
        tracker['last_seen'] = current_time
        
        # Higher threshold to avoid false positives during legitimate exploits
        # Increased from 100 to 200 connections in 10 seconds
        if tracker['count'] > 200 and (current_time - tracker['last_seen']) < 10:
            return {
                'type': 'syn_flood',
                'name': 'SYN Flood Attack',
                'description': f'High volume of SYN packets from {src_ip}',
                'severity': 'HIGH',
                'details': f'{tracker["count"]} connections in 10 seconds'
            }
        return None
    
    def detect_exploit(self, packet):
        """Detect known exploit patterns"""
        # Check port-based detection first (for exploits targeting specific ports)
        if packet.haslayer(TCP):
            src_port = packet[TCP].sport
            dst_port = packet[TCP].dport
            
            # Special handling for SMB/EternalBlue on ports 445/139
            # Check traffic in BOTH directions (dst or src)
            is_smb_traffic = dst_port in [445, 139] or src_port in [445, 139]
            
            if is_smb_traffic:
                # Count ALL SMB packets (connections, scans, data)
                src_ip = packet[IP].src
                if not hasattr(self, 'smb_tracker'):
                    self.smb_tracker = defaultdict(lambda: {'count': 0, 'last_seen': 0, 'first_seen': 0})
                
                current_time = time.time()
                tracker = self.smb_tracker[src_ip]
                
                # Reset counter if more than 30 seconds since last packet
                if current_time - tracker['last_seen'] > 30:
                    tracker['count'] = 0
                    tracker['first_seen'] = current_time
                elif tracker['count'] == 0:
                    tracker['first_seen'] = current_time
                
                tracker['count'] += 1
                tracker['last_seen'] = current_time
                
                # Detect SMB scanning or exploit attempt with LOW threshold
                if tracker['count'] >= 3:  # Just 3 SMB packets = likely scanning/exploit
                    elapsed = current_time - tracker['first_seen']
                    target_port = dst_port if dst_port in [445, 139] else src_port
                    return {
                        'type': 'ms17_010',
                        'name': 'EternalBlue (MS17-010)',
                        'description': 'SMB scanning/exploitation attempt detected',
                        'severity': 'CRITICAL',
                        'details': f'SMB activity on port {target_port} ({tracker["count"]} packets in {elapsed:.1f}s)'
                    }
        
        # Check payload patterns
        if not packet.haslayer(Raw):
            return None
            
        payload = bytes(packet[Raw].load)
        
        for exploit_id, exploit_info in EXPLOIT_SIGNATURES.items():
            # Handle both single pattern and multiple patterns
            patterns = exploit_info.get('patterns', [exploit_info.get('pattern')])
            if not isinstance(patterns, list):
                patterns = [patterns]
            
            for pattern in patterns:
                if pattern and pattern in payload:
                    dst_port = packet[TCP].dport if packet.haslayer(TCP) else (packet[UDP].dport if packet.haslayer(UDP) else 0)
                    
                    if dst_port in exploit_info['ports'] or not exploit_info['ports']:
                        return {
                            'type': exploit_id,
                            'name': exploit_info['name'],
                            'description': exploit_info['description'],
                            'severity': exploit_info['severity'],
                            'details': f'Exploit signature detected in payload to port {dst_port}'
                        }
        return None
    
    def packet_handler(self, packet):
        """Process each captured packet"""
        try:
            if not packet.haslayer(IP):
                return
            
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            timestamp = datetime.now().isoformat()
            
            attack_detected = None
            
            # Check for OUTBOUND reverse shell connections first
            if packet.haslayer(TCP):
                dst_port = packet[TCP].dport
                reverse_shell_detected = self.detect_reverse_shell(src_ip, dst_ip, dst_port)
                if reverse_shell_detected:
                    attack_detected = reverse_shell_detected
            
            # Skip remaining checks if not inbound traffic (but allow reverse shell through)
            if not attack_detected and not self.is_inbound_traffic(src_ip, dst_ip):
                return  # Skip outbound and local-to-local traffic
            
            # PRIORITY 1: Check for known exploits FIRST (most specific)
            if not attack_detected:
                attack_detected = self.detect_exploit(packet)
            
            # PRIORITY 2: Check for port scanning (if no exploit found)
            if not attack_detected and packet.haslayer(TCP):
                dst_port = packet[TCP].dport
                attack_detected = self.detect_port_scan(src_ip, dst_port)
            
            # PRIORITY 3: Check for SYN flood (if no exploit or port scan found)
            # Only report SYN floods if we haven't detected a more specific attack
            if not attack_detected and packet.haslayer(TCP) and packet[TCP].flags == 'S':
                syn_attack = self.detect_syn_flood(src_ip)
                if syn_attack:
                    attack_detected = syn_attack
            
            # If attack detected, emit event
            if attack_detected:
                event = {
                    'timestamp': timestamp,
                    'src_ip': src_ip,
                    'dst_ip': dst_ip,
                    'attack_type': attack_detected['type'],
                    'attack_name': attack_detected['name'],
                    'description': attack_detected['description'],
                    'severity': attack_detected['severity'],
                    'details': attack_detected['details']
                }
                
                attack_events.append(event)
                socketio.emit('attack_detected', event)
                print(f"[ALERT] {attack_detected['severity']} - {attack_detected['name']} from {src_ip}")
                
        except Exception as e:
            print(f"Error processing packet: {e}")
    
    def start_sniffing(self, interface=None):
        """Start packet capture"""
        self.running = True
        print(f"Starting packet capture on interface: {interface or 'default'}")
        
        try:
            # Sniff packets - requires root/admin privileges
            sniff(prn=self.packet_handler, store=False, iface=interface)
        except PermissionError:
            print("ERROR: Root privileges required for packet capture")
            print("Please run with sudo: sudo python3 app.py")
            self.running = False
        except Exception as e:
            print(f"Error starting packet capture: {e}")
            self.running = False
    
    def start(self, interface=None):
        """Start detector in background thread"""
        if not self.running:
            self.sniffer_thread = threading.Thread(
                target=self.start_sniffing,
                args=(interface,),
                daemon=True
            )
            self.sniffer_thread.start()
    
    def stop(self):
        """Stop detector"""
        self.running = False

# Initialize detector
detector = AttackDetector()

@app.route('/')
def index():
    """Serve frontend"""
    return """
    <html>
    <head><title>Metasploit Attack Detection System</title></head>
    <body>
        <h1>Metasploit Attack Detection System</h1>
        <p>Backend is running. Access the frontend at /frontend/index.html</p>
        <p>WebSocket endpoint: ws://localhost:5000</p>
    </body>
    </html>
    """

@app.route('/api/status')
def status():
    """Get system status"""
    return jsonify({
        'status': 'running' if detector.running else 'stopped',
        'total_events': len(attack_events),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/events')
def get_events():
    """Get recent attack events"""
    return jsonify({
        'events': list(attack_events),
        'count': len(attack_events)
    })

@app.route('/api/exploits')
def get_exploits():
    """Get list of detectable exploits"""
    exploits = []
    for exploit_id, info in EXPLOIT_SIGNATURES.items():
        exploits.append({
            'id': exploit_id,
            'name': info['name'],
            'description': info['description'],
            'severity': info['severity'],
            'ports': info['ports']
        })
    return jsonify({'exploits': exploits})

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('status', {'message': 'Connected to attack detection system'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('start_monitoring')
def handle_start_monitoring(data):
    """Start monitoring"""
    interface = data.get('interface') if data else None
    if not detector.running:
        detector.start(interface)
        emit('status', {'message': 'Monitoring started'})
    else:
        emit('status', {'message': 'Monitoring already running'})

@socketio.on('stop_monitoring')
def handle_stop_monitoring():
    """Stop monitoring"""
    detector.stop()
    emit('status', {'message': 'Monitoring stopped'})

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("Metasploit Attack Detection System - Backend")
    print("=" * 60)
    print("\nNOTE: This application requires ROOT privileges to capture packets")
    print("Run with: sudo python3 app.py")
    print("\nStarting Flask-SocketIO server on http://0.0.0.0:5000")
    print("=" * 60)
    
    # Auto-start detector
    detector.start()
    
    # Run Flask-SocketIO server with proper threading mode
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
