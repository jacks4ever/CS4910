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
    
    // Update timestamp every second
    setInterval(updateTimestamp, 1000);
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

// Load detectable exploits
async function loadExploits() {
    try {
        const response = await fetch(`${BACKEND_URL}/api/exploits`);
        const data = await response.json();
        
        const exploitList = document.getElementById('exploitList');
        
        if (data.exploits && data.exploits.length > 0) {
            exploitList.innerHTML = data.exploits.map(exploit => `
                <div class="exploit-item">
                    <div class="exploit-name">${escapeHtml(exploit.name)}</div>
                    <div class="exploit-description">${escapeHtml(exploit.description)}</div>
                    <div class="exploit-ports">Ports: ${exploit.ports.join(', ') || 'Any'}</div>
                </div>
            `).join('');
        } else {
            exploitList.innerHTML = '<p class="no-data">No exploit signatures loaded</p>';
        }
    } catch (error) {
        console.error('Error loading exploits:', error);
        document.getElementById('exploitList').innerHTML = 
            '<p class="no-data" style="color: var(--accent-red);">Error loading exploits</p>';
    }
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
    // Update IPs in diagram
    document.getElementById('attackerIP').textContent = attack.src_ip;
    document.getElementById('targetIP').textContent = attack.dst_ip;
    document.getElementById('attackLabel').textContent = attack.attack_name;
    
    // Get severity color class
    const severityClass = `packet-${attack.severity.toLowerCase()}`;
    
    // Create animated packet
    const packetsGroup = document.getElementById('attackPackets');
    const packet = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    const packetId = `packet-${Date.now()}-${Math.random()}`;
    
    packet.setAttribute('id', packetId);
    packet.setAttribute('cx', '150');
    packet.setAttribute('cy', '150');
    packet.setAttribute('r', '8');
    packet.setAttribute('class', `attack-packet ${severityClass}`);
    
    packetsGroup.appendChild(packet);
    
    // Add pulse effect to nodes
    const attackerNode = document.getElementById('attackerNode');
    const targetNode = document.getElementById('targetNode');
    attackerNode.classList.add('attacker-active');
    targetNode.classList.add('target-active');
    
    // Animate packet
    let position = 150;
    const endPosition = 650;
    const duration = 2000; // 2 seconds
    const startTime = Date.now();
    
        const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease-in-out function
        const easeProgress = progress < 0.5
            ? 2 * progress * progress
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        
        position = 150 + (endPosition - 150) * easeProgress;
        packet.setAttribute('cx', position);
        packet.setAttribute('cy', 145);  // Match the updated attack path y-coordinate
        packet.setAttribute('opacity', 1 - progress);        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            // Remove packet after animation
            packet.remove();
            
            // Remove pulse after short delay
            setTimeout(() => {
                attackerNode.classList.remove('attacker-active');
                targetNode.classList.remove('target-active');
            }, 500);
        }
    };
    
    requestAnimationFrame(animate);
    
    // Also create multiple smaller packets for dramatic effect
    for (let i = 1; i <= 3; i++) {
        setTimeout(() => {
            createSmallPacket(severityClass);
        }, i * 300);
    }
}

function createSmallPacket(severityClass) {
    const packetsGroup = document.getElementById('attackPackets');
    const packet = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    
    packet.setAttribute('cx', '150');
    packet.setAttribute('cy', 145 + (Math.random() - 0.5) * 40);  // Centered on new y-coordinate
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

// Log initialization
console.log(`
╔══════════════════════════════════════════════════════╗
║   Metasploit Attack Detection Dashboard v1.0        ║
║   Blue Team Security Monitoring System              ║
╚══════════════════════════════════════════════════════╝

Connected to: ${BACKEND_URL}
WebSocket Status: Initializing...
`);
