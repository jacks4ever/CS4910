// Metasploit Attack Detection Dashboard - JavaScript

// Configuration - Auto-detect backend URL
function getBackendURL() {
    // If frontend is served from a web server, use that host
    const currentHost = window.location.hostname;
    
    // If localhost or file://, try localhost first
    if (!currentHost || currentHost === '' || window.location.protocol === 'file:') {
        return 'http://localhost:5000';
    }
    
    // Use the same host as the frontend is served from
    return `http://${currentHost}:5000`;
}

const BACKEND_URL = getBackendURL();
console.log(`Backend URL: ${BACKEND_URL}`);
let socket;
let totalDetections = 0;
let severityCounts = {
    CRITICAL: 0,
    HIGH: 0,
    MEDIUM: 0,
    LOW: 0
};
let attackTypeCounts = {};
let whitelistedIPs = new Set();

// Traffic tracking for intensity meter and graph
let trafficHistory = [];
let recentPackets = [];
let intensityLevel = 0;
let trafficChart = null;

// Active connection tracking
let activeConnections = new Map(); // key: "src_ip:dst_ip:port", value: {timestamp, line_element}

// Load whitelist from localStorage
function loadWhitelist() {
    const saved = localStorage.getItem('whitelistedIPs');
    if (saved) {
        whitelistedIPs = new Set(JSON.parse(saved));
    }
}

// Save whitelist to localStorage
function saveWhitelist() {
    localStorage.setItem('whitelistedIPs', JSON.stringify([...whitelistedIPs]));
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('Initializing Metasploit Attack Detection Dashboard...');
    
    // Load whitelist
    loadWhitelist();
    
    // Setup event listeners
    document.getElementById('clearBtn').addEventListener('click', clearEvents);
    document.getElementById('whitelistBtn').addEventListener('click', openWhitelistModal);
    document.getElementById('closeModal').addEventListener('click', closeWhitelistModal);
    document.getElementById('addIPBtn').addEventListener('click', addWhitelistIP);
    document.getElementById('clearProgressBtn').addEventListener('click', clearExploitProgress);
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('whitelistModal');
        if (e.target === modal) {
            closeWhitelistModal();
        }
    });
    
    // Add IP on Enter key
    document.getElementById('whitelistIP').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addWhitelistIP();
        }
    });
    
    // Connect to WebSocket
    connectWebSocket();
    
    // Load initial data
    loadExploits();
    loadEvents();
    
    // Initialize traffic chart
    initTrafficChart();
    
    // Update timestamp every second
    setInterval(updateTimestamp, 1000);
    
    // Update traffic metrics every second
    setInterval(updateTrafficMetrics, 1000);
    
    // Check for stale connections every 2 seconds
    setInterval(checkStaleConnections, 2000);
});

// WebSocket Connection
function connectWebSocket() {
    console.log('Connecting to WebSocket server...');
    updateWSStatus('Connecting...', 'ws-connecting');
    
    socket = io(BACKEND_URL, {
        transports: ['websocket', 'polling'],
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionAttempts: 10
    });
    
    socket.on('connect', () => {
        console.log('✓ Connected to backend');
        updateWSStatus('Connected', 'ws-connected');
        updateSystemStatus('Running', 'status-running');
    });
    
    socket.on('disconnect', () => {
        console.log('✗ Disconnected from backend');
        updateWSStatus('Disconnected', 'ws-disconnected');
        updateSystemStatus('Disconnected', 'status-stopped');
    });
    
    socket.on('connect_error', (error) => {
        console.error('Connection error:', error);
        updateWSStatus('Connection Failed', 'ws-disconnected');
    });
    
    socket.on('attack_detected', (data) => {
        console.log('🚨 Attack detected:', data);
        handleAttackDetected(data);
    });
    
    socket.on('status', (data) => {
        console.log('Status update:', data.message);
    });
}

// Update WebSocket status
function updateWSStatus(message, statusClass) {
    const wsStatus = document.getElementById('wsStatus');
    const statusIcons = {
        'ws-connecting': '⚪',
        'ws-connected': '🟢',
        'ws-disconnected': '🔴'
    };
    
    wsStatus.textContent = `${statusIcons[statusClass] || '⚪'} ${message}`;
    wsStatus.className = statusClass;
}

// Update system status
function updateSystemStatus(message, statusClass) {
    const systemStatus = document.getElementById('systemStatus');
    const icon = statusClass === 'status-running' ? '●  ' : '●  ';
    systemStatus.textContent = icon + message;
    systemStatus.className = `status-value ${statusClass}`;
}

// Handle attack detection
function handleAttackDetected(attack) {
    // Check if source IP is whitelisted
    if (whitelistedIPs.has(attack.src_ip)) {
        console.log(`Suppressed: ${attack.attack_name} from whitelisted IP ${attack.src_ip}`);
        return; // Suppress this detection
    }
    
    // Update counts
    totalDetections++;
    document.getElementById('totalDetections').textContent = totalDetections;
    
    // Update severity counts
    if (attack.severity in severityCounts) {
        severityCounts[attack.severity]++;
        updateSeverityCounts();
    }
    
    // Update attack type counts
    if (!attackTypeCounts[attack.attack_name]) {
        attackTypeCounts[attack.attack_name] = 0;
    }
    attackTypeCounts[attack.attack_name]++;
    updateAttackTypes();
    
    // Mark exploit as detected in the checklist
    markExploitDetected(attack.attack_type);
    
    // Track packet for metrics
    trackPacket(attack);
    
    // Animate attack in network diagram
    animateAttack(attack);
    
    // Add to feed
    addAttackToFeed(attack);
    
    // Update active badge
    updateActiveBadge();
}

// Add attack to feed
function addAttackToFeed(attack) {
    const attackFeed = document.getElementById('attackFeed');
    
    // Remove "no attacks" message if present
    const noAttacks = attackFeed.querySelector('.no-attacks');
    if (noAttacks) {
        noAttacks.remove();
    }
    
    // Create attack card
    const card = document.createElement('div');
    card.className = `attack-card severity-${attack.severity} new`;
    
    const timestamp = new Date(attack.timestamp).toLocaleString();
    
    card.innerHTML = `
        <div class="attack-header">
            <div class="attack-name">${escapeHtml(attack.attack_name)}</div>
            <div class="attack-severity ${attack.severity}">${attack.severity}</div>
        </div>
        <div class="attack-description">${escapeHtml(attack.description)}</div>
        <div class="attack-details">
            <div class="attack-detail"><strong>Source IP:</strong> ${escapeHtml(attack.src_ip)}</div>
            <div class="attack-detail"><strong>Target IP:</strong> ${escapeHtml(attack.dst_ip)}</div>
            <div class="attack-detail"><strong>Type:</strong> ${escapeHtml(attack.attack_type)}</div>
        </div>
        <div class="attack-description" style="margin-top: 10px;">
            <strong>Details:</strong> ${escapeHtml(attack.details)}
        </div>
        <div class="attack-timestamp">⏰ ${timestamp}</div>
    `;
    
    // Add to top of feed
    attackFeed.insertBefore(card, attackFeed.firstChild);
    
    // Remove 'new' class after animation
    setTimeout(() => {
        card.classList.remove('new');
    }, 500);
    
    // Limit feed to 50 cards
    const cards = attackFeed.querySelectorAll('.attack-card');
    if (cards.length > 50) {
        cards[cards.length - 1].remove();
    }
}

// Update severity counts
function updateSeverityCounts() {
    document.getElementById('criticalCount').textContent = severityCounts.CRITICAL;
    document.getElementById('highCount').textContent = severityCounts.HIGH;
    document.getElementById('mediumCount').textContent = severityCounts.MEDIUM;
    document.getElementById('lowCount').textContent = severityCounts.LOW;
}

// Update attack types breakdown
function updateAttackTypes() {
    const attackTypesDiv = document.getElementById('attackTypes');
    
    // Sort by count
    const sortedTypes = Object.entries(attackTypeCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10); // Top 10
    
    if (sortedTypes.length === 0) {
        attackTypesDiv.innerHTML = '<p class="no-data">No attacks detected yet</p>';
        return;
    }
    
    attackTypesDiv.innerHTML = sortedTypes.map(([name, count]) => `
        <div class="attack-type-item">
            <div class="attack-type-name">${escapeHtml(name)}</div>
            <div class="attack-type-count">${count}</div>
        </div>
    `).join('');
}

// Update active badge
function updateActiveBadge() {
    const badge = document.getElementById('activeBadge');
    const activeCount = document.querySelectorAll('.attack-card').length;
    badge.textContent = `${activeCount} Active`;
}

// Track detected exploits
let detectedExploits = new Set();

// Load detectable exploits
async function loadExploits() {
    try {
        const response = await fetch(`${BACKEND_URL}/api/exploits`);
        const data = await response.json();
        
        const exploitList = document.getElementById('exploitList');
        
        if (data.exploits && data.exploits.length > 0) {
            exploitList.innerHTML = data.exploits.map(exploit => {
                const exploitId = exploit.id || exploit.name.toLowerCase().replace(/\s+/g, '_');
                const isDetected = detectedExploits.has(exploitId);
                return `
                    <div class="exploit-item ${isDetected ? 'exploit-detected' : ''}" data-exploit-id="${exploitId}">
                        <div class="exploit-checkbox">
                            <span class="checkbox-icon">${isDetected ? '✅' : '⬜'}</span>
                        </div>
                        <div class="exploit-details">
                            <div class="exploit-name">${escapeHtml(exploit.name)}</div>
                            <div class="exploit-description">${escapeHtml(exploit.description)}</div>
                            <div class="exploit-ports">Ports: ${exploit.ports.join(', ') || 'Any'}</div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            exploitList.innerHTML = '<p class="no-data">No exploit signatures loaded</p>';
        }
    } catch (error) {
        console.error('Error loading exploits:', error);
        document.getElementById('exploitList').innerHTML = 
            '<p class="no-data" style="color: var(--accent-red);">Error loading exploits</p>';
    }
}

// Mark exploit as detected
function markExploitDetected(attackType) {
    // Add to detected set
    detectedExploits.add(attackType);
    
    // Update the UI
    const exploitItem = document.querySelector(`[data-exploit-id="${attackType}"]`);
    if (exploitItem && !exploitItem.classList.contains('exploit-detected')) {
        exploitItem.classList.add('exploit-detected');
        const checkbox = exploitItem.querySelector('.checkbox-icon');
        if (checkbox) {
            checkbox.textContent = '✅';
            
            // Animate the check
            exploitItem.style.animation = 'exploitCheckAnimation 0.5s ease-out';
            setTimeout(() => {
                exploitItem.style.animation = '';
            }, 500);
        }
    }
}

// Clear exploit progress
function clearExploitProgress() {
    if (!confirm('Reset all exploit detection progress?')) {
        return;
    }
    
    // Clear the detected set
    detectedExploits.clear();
    
    // Reload the exploit list to reset checkboxes
    loadExploits();
    
    console.log('Exploit detection progress reset');
}

// Load existing events
async function loadEvents() {
    try {
        const response = await fetch(`${BACKEND_URL}/api/events`);
        const data = await response.json();
        
        if (data.events && data.events.length > 0) {
            // Process events in reverse (oldest first) so newest appears on top
            data.events.reverse().forEach(event => {
                handleAttackDetected(event);
            });
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// Clear all events
function clearEvents() {
    if (!confirm('Clear all attack events from the dashboard?')) {
        return;
    }
    
    // Clear feed
    const attackFeed = document.getElementById('attackFeed');
    attackFeed.innerHTML = `
        <div class="no-attacks">
            <p>🟢 No attacks detected</p>
            <p class="subtitle-small">System is monitoring network traffic...</p>
        </div>
    `;
    
    // Reset counts
    totalDetections = 0;
    severityCounts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
    attackTypeCounts = {};
    
    document.getElementById('totalDetections').textContent = '0';
    updateSeverityCounts();
    updateAttackTypes();
    updateActiveBadge();
}

// Update timestamp
function updateTimestamp() {
    const now = new Date().toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = now;
}

// Escape HTML to prevent XSS
function escapeHtml(unsafe) {
    if (typeof unsafe !== 'string') return unsafe;
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Network Diagram Animation Functions
function animateAttack(attack) {
    // Determine if this is a reverse shell (outbound from victim)
    const isReverseShell = attack.attack_type === 'reverse_shell';
    
    // For reverse shells: attacker IP goes on LEFT, victim IP goes on RIGHT
    // For normal attacks: attacker IP goes on LEFT, victim IP goes on RIGHT
    document.getElementById('attackerIP').textContent = isReverseShell ? attack.dst_ip : attack.src_ip;
    document.getElementById('targetIP').textContent = isReverseShell ? attack.src_ip : attack.dst_ip;
    document.getElementById('attackLabel').textContent = attack.attack_name;
    
    // Get severity color and icon
    const severityClass = `packet-${attack.severity.toLowerCase()}`;
    const attackIcon = getAttackIcon(attack.attack_type);
    const trailColor = getSeverityColor(attack.severity);
    
    // Determine animation direction
    // Normal attacks: LEFT (150) to RIGHT (650) - attacker to victim
    // Reverse shell: RIGHT (650) to LEFT (150) - victim to attacker
    const startX = isReverseShell ? 650 : 150;
    const endX = isReverseShell ? 150 : 650;
    
    // Create packet group (packet + icon + trail)
    const packetsGroup = document.getElementById('attackPackets');
    const packetGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const packetId = `packet-${Date.now()}-${Math.random()}`;
    packetGroup.setAttribute('id', packetId);
    
    // Create trail path
    const trail = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    trail.setAttribute('class', 'packet-trail');
    trail.setAttribute('x1', startX);
    trail.setAttribute('y1', '145');
    trail.setAttribute('x2', startX);
    trail.setAttribute('y2', '145');
    trail.setAttribute('stroke', trailColor);
    trail.style.animation = 'trailFade 0.5s ease-out forwards';
    packetGroup.appendChild(trail);
    
    // Create animated packet circle
    const packet = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    packet.setAttribute('cx', startX);
    packet.setAttribute('cy', '145');
    packet.setAttribute('r', '8');
    packet.setAttribute('class', `attack-packet ${severityClass}`);
    packetGroup.appendChild(packet);
    
    // Create icon on packet
    const icon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    icon.setAttribute('x', startX);
    icon.setAttribute('y', '150');
    icon.setAttribute('text-anchor', 'middle');
    icon.setAttribute('font-size', '12');
    icon.textContent = attackIcon;
    packetGroup.appendChild(icon);
    
    packetsGroup.appendChild(packetGroup);
    
    // Add pulse effect to nodes
    const attackerNode = document.getElementById('attackerNode');
    const targetNode = document.getElementById('targetNode');
    attackerNode.classList.add('attacker-active');
    targetNode.classList.add('target-active');
    
    // For reverse shells, show persistent connection line
    if (isReverseShell) {
        showConnectionLine(attack.src_ip, attack.dst_ip);
    }
    
    // Animate packet
    let position = startX;
    const duration = 2000; // 2 seconds
    const startTime = Date.now();
    
    const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease-in-out function
        const easeProgress = progress < 0.5
            ? 2 * progress * progress
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        
        position = startX + (endX - startX) * easeProgress;
        
        // Update packet position
        packet.setAttribute('cx', position);
        packet.setAttribute('cy', 145);
        packet.setAttribute('opacity', 1 - progress);
        
        // Update icon position
        icon.setAttribute('x', position);
        icon.setAttribute('y', 150);
        icon.setAttribute('opacity', 1 - progress);
        
        // Update trail
        trail.setAttribute('x2', position);
        trail.setAttribute('y2', 145);
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            // Remove packet after animation
            packetGroup.remove();
            
            // Remove pulse after short delay
            setTimeout(() => {
                attackerNode.classList.remove('attacker-active');
                targetNode.classList.remove('target-active');
            }, 500);
        }
    };
    
    requestAnimationFrame(animate);
}

function createSmallPacket(severityClass, startX) {
    const packetsGroup = document.getElementById('attackPackets');
    const packet = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    
    packet.setAttribute('cx', startX);  // Use the same startX as main packet
    packet.setAttribute('cy', 145 + (Math.random() - 0.5) * 40);
    packet.setAttribute('r', '4');
    packet.setAttribute('class', `attack-packet ${severityClass}`);
    
    packetsGroup.appendChild(packet);
    
    setTimeout(() => packet.remove(), 2000);
}

// Whitelist Modal Functions
function openWhitelistModal() {
    document.getElementById('whitelistModal').style.display = 'block';
    renderWhitelistedIPs();
}

function closeWhitelistModal() {
    document.getElementById('whitelistModal').style.display = 'none';
}

function addWhitelistIP() {
    const input = document.getElementById('whitelistIP');
    const ip = input.value.trim();
    
    // Validate IP address format
    const ipPattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    if (!ipPattern.test(ip)) {
        alert('Please enter a valid IP address (e.g., 192.168.1.100)');
        return;
    }
    
    // Check each octet is 0-255
    const octets = ip.split('.');
    if (octets.some(octet => parseInt(octet) > 255)) {
        alert('Invalid IP address: octets must be between 0-255');
        return;
    }
    
    if (whitelistedIPs.has(ip)) {
        alert('This IP is already whitelisted');
        return;
    }
    
    whitelistedIPs.add(ip);
    saveWhitelist();
    renderWhitelistedIPs();
    input.value = '';
    
    console.log(`Whitelisted IP: ${ip}`);
}

function removeWhitelistIP(ip) {
    if (confirm(`Remove ${ip} from whitelist?`)) {
        whitelistedIPs.delete(ip);
        saveWhitelist();
        renderWhitelistedIPs();
        console.log(`Removed from whitelist: ${ip}`);
    }
}

function renderWhitelistedIPs() {
    const container = document.getElementById('whitelistedIPs');
    
    if (whitelistedIPs.size === 0) {
        container.innerHTML = '<p class="no-data">No IPs whitelisted</p>';
        return;
    }
    
    const sortedIPs = [...whitelistedIPs].sort();
    container.innerHTML = sortedIPs.map(ip => `
        <div class="whitelist-item">
            <span class="whitelist-ip">${escapeHtml(ip)}</span>
            <button class="whitelist-remove" onclick="removeWhitelistIP('${escapeHtml(ip)}')">Remove</button>
        </div>
    `).join('');
}

// ============================================
// VISUAL ENHANCEMENTS
// ============================================

// Show persistent connection line
function showConnectionLine(srcIP, dstIP) {
    const connectionKey = `${srcIP}:${dstIP}`;
    
    // Check if connection already exists
    if (activeConnections.has(connectionKey)) {
        // Update timestamp
        activeConnections.get(connectionKey).timestamp = Date.now();
        return;
    }
    
    // Create connection line (victim to attacker for reverse shell)
    const connectionGroup = document.getElementById('connectionLines');
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', '650');  // From victim
    line.setAttribute('y1', '145');
    line.setAttribute('x2', '150');  // To attacker
    line.setAttribute('y2', '145');
    line.setAttribute('class', 'connection-line');
    line.setAttribute('id', `conn-${connectionKey.replace(/[.:]/g, '-')}`);
    
    connectionGroup.appendChild(line);
    
    // Track connection
    activeConnections.set(connectionKey, {
        timestamp: Date.now(),
        line: line,
        srcIP: srcIP,
        dstIP: dstIP
    });
    
    console.log(`Connection established: ${srcIP} → ${dstIP}`);
}

// Remove connection line
function removeConnectionLine(connectionKey) {
    if (activeConnections.has(connectionKey)) {
        const conn = activeConnections.get(connectionKey);
        conn.line.remove();
        activeConnections.delete(connectionKey);
        console.log(`Connection closed: ${connectionKey}`);
    }
}

// Check for stale connections (no activity in 5 seconds = connection closed)
function checkStaleConnections() {
    const now = Date.now();
    const timeout = 5000; // 5 seconds
    
    for (const [key, conn] of activeConnections.entries()) {
        if (now - conn.timestamp > timeout) {
            console.log(`Connection timeout: ${key}`);
            removeConnectionLine(key);
        }
    }
}

// Get Attack Icon based on type
function getAttackIcon(attackType) {
    const icons = {
        'ms17_010': '💀',        // EternalBlue
        'ms08_067': '💀',        // MS08-067
        'port_scan': '🔍',       // Port scan
        'syn_flood': '🌊',       // SYN flood
        'vsftpd_backdoor': '🚪', // Backdoor
        'shellshock': '💣',      // Shellshock
        'sql_injection': '💉',   // SQL Injection
        'reverse_shell': '🔙',   // Reverse shell
        'tomcat_mgr': '🐱'       // Tomcat
    };
    return icons[attackType] || '⚠️';
}

// Get Severity Color
function getSeverityColor(severity) {
    const colors = {
        'CRITICAL': '#dc2626',
        'HIGH': '#f97316',
        'MEDIUM': '#eab308',
        'LOW': '#3b82f6'
    };
    return colors[severity] || '#9aa0a6';
}

// Traffic Chart Initialization
function initTrafficChart() {
    const canvas = document.getElementById('trafficChart');
    const ctx = canvas.getContext('2d');
    
    // Initialize traffic history with 60 seconds of data
    for (let i = 0; i < 60; i++) {
        trafficHistory.push(0);
    }
    
    // Store context for later use
    trafficChart = { canvas, ctx };
    
    // Start drawing loop
    drawTrafficChart();
    setInterval(drawTrafficChart, 1000);
}

// Draw Traffic Chart
function drawTrafficChart() {
    if (!trafficChart) return;
    
    const { canvas, ctx } = trafficChart;
    const width = canvas.width;
    const height = canvas.height;
    const padding = 20;
    const graphWidth = width - padding * 2;
    const graphHeight = height - padding * 2;
    
    // Clear canvas
    ctx.fillStyle = '#1e2139';
    ctx.fillRect(0, 0, width, height);
    
    // Find max value for scaling
    const maxValue = Math.max(...trafficHistory, 10);
    
    // Draw grid lines
    ctx.strokeStyle = '#2d3250';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 5; i++) {
        const y = padding + (graphHeight / 5) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }
    
    // Draw line graph
    ctx.strokeStyle = '#4285f4';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    trafficHistory.forEach((value, index) => {
        const x = padding + (graphWidth / (trafficHistory.length - 1)) * index;
        const y = padding + graphHeight - (value / maxValue) * graphHeight;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    
    ctx.stroke();
    
    // Fill area under line
    ctx.lineTo(width - padding, padding + graphHeight);
    ctx.lineTo(padding, padding + graphHeight);
    ctx.closePath();
    ctx.fillStyle = 'rgba(66, 133, 244, 0.1)';
    ctx.fill();
    
    // Draw labels
    ctx.fillStyle = '#9aa0a6';
    ctx.font = '10px monospace';
    ctx.fillText('60s', padding, height - 5);
    ctx.fillText('0s', width - padding - 15, height - 5);
    ctx.fillText(Math.round(maxValue) + ' pkt/s', padding + 5, padding + 10);
}

// Track Packet for Metrics
function trackPacket(attack) {
    const now = Date.now();
    recentPackets.push(now);
    
    // Remove packets older than 60 seconds
    recentPackets = recentPackets.filter(time => now - time < 60000);
}

// Update Traffic Metrics
function updateTrafficMetrics() {
    const now = Date.now();
    
    // Count packets in last second
    const packetsLastSecond = recentPackets.filter(time => now - time < 1000).length;
    
    // Add to history
    trafficHistory.push(packetsLastSecond);
    if (trafficHistory.length > 60) {
        trafficHistory.shift();
    }
}

// Log initialization
console.log(`
╔══════════════════════════════════════════════════════╗
║   Metasploit Attack Detection Dashboard v1.0        ║
║   Blue Team Security Monitoring System              ║
╚══════════════════════════════════════════════════════╝

Connected to: ${BACKEND_URL}
WebSocket Status: Initializing...
`);

