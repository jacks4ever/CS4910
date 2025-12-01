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

// Track active animations
let activeAnimations = 0;
let allExploitsDetectedPending = false;

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
    
    // Check if all exploits are detected
    checkAllExploitsDetected();
}

// Check if all exploits have been detected and trigger confetti
function checkAllExploitsDetected() {
    const allExploits = document.querySelectorAll('.exploit-item');
    const totalExploits = allExploits.length;
    const detectedCount = detectedExploits.size;
    
    if (totalExploits > 0 && detectedCount === totalExploits) {
        // Mark as pending, wait for animations to finish
        allExploitsDetectedPending = true;
        checkAndLaunchConfetti();
    }
}

// Launch confetti only when all animations complete
function checkAndLaunchConfetti() {
    if (allExploitsDetectedPending && activeAnimations === 0) {
        allExploitsDetectedPending = false;
        // Wait 5 seconds after last exploit before showing celebration
        setTimeout(() => {
            launchConfetti();
        }, 5000);
    }
}

// Confetti animation
function launchConfetti() {
    const colors = [
        '#FFD700', '#FF6B9D', '#C724B1', '#4169E1', '#00CED1', 
        '#FF4500', '#32CD32', '#FFD700', '#FF1493', '#1E90FF'
    ];
    const confettiCount = 150;
    
    for (let i = 0; i < confettiCount; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            
            // Random shapes: square, rectangle, or circle
            const shapes = ['square', 'rectangle', 'circle'];
            const shape = shapes[Math.floor(Math.random() * shapes.length)];
            
            if (shape === 'square') {
                confetti.style.width = '8px';
                confetti.style.height = '8px';
            } else if (shape === 'rectangle') {
                confetti.style.width = Math.random() > 0.5 ? '12px' : '6px';
                confetti.style.height = Math.random() > 0.5 ? '6px' : '12px';
            } else {
                confetti.style.width = '8px';
                confetti.style.height = '8px';
                confetti.style.borderRadius = '50%';
            }
            
            // Position and color
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            
            // Add metallic shine
            if (Math.random() > 0.5) {
                confetti.style.background = `linear-gradient(135deg, ${colors[Math.floor(Math.random() * colors.length)]} 0%, ${colors[Math.floor(Math.random() * colors.length)]} 100%)`;
            }
            
            // Random physics
            const drift = (Math.random() - 0.5) * 200; // horizontal drift
            const rotation = Math.random() * 1440 - 720; // -720 to 720 degrees
            const duration = Math.random() * 2 + 2.5;
            
            confetti.style.setProperty('--drift', drift + 'px');
            confetti.style.setProperty('--rotation', rotation + 'deg');
            confetti.style.animationDuration = duration + 's';
            confetti.style.animationDelay = Math.random() * 0.3 + 's';
            
            document.body.appendChild(confetti);
            
            // Remove confetti after animation
            setTimeout(() => confetti.remove(), (duration + 0.3) * 1000);
        }, i * 8);
    }
    
    // Show celebration message
    showCelebrationMessage();
}

function showCelebrationMessage() {
    const message = document.createElement('div');
    message.className = 'celebration-message';
    message.innerHTML = '🎉 All Exploits Detected! 🎉';
    document.body.appendChild(message);
    
    setTimeout(() => {
        message.style.opacity = '0';
        setTimeout(() => message.remove(), 500);
    }, 3000);
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
    
    // Get exploit-specific visuals
    const exploitVisuals = getExploitVisuals(attack.attack_type);
    const attackIcon = getAttackIcon(attack.attack_type);
    
    // Determine animation direction
    // Normal attacks: LEFT (180) to RIGHT (620) - attacker to victim
    // Reverse shell: RIGHT (620) to LEFT (180) - victim to attacker
    const startX = isReverseShell ? 620 : 180;
    const endX = isReverseShell ? 180 : 620;
    
    // Create packet group (packet + icon + trail)
    const packetsGroup = document.getElementById('attackPackets');
    const packetGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    const packetId = `packet-${Date.now()}-${Math.random()}`;
    packetGroup.setAttribute('id', packetId);
    
    // Create trail path with exploit-specific styling
    const trail = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    trail.setAttribute('class', 'packet-trail');
    trail.setAttribute('x1', startX);
    trail.setAttribute('y1', '135');
    trail.setAttribute('x2', startX);
    trail.setAttribute('y2', '135');
    trail.setAttribute('stroke', exploitVisuals.glowColor);
    trail.setAttribute('stroke-width', exploitVisuals.trailEffect === 'solid-thick' ? '8' : '5');
    
    // Apply trail effect styling
    if (exploitVisuals.trailEffect === 'dashed') {
        trail.setAttribute('stroke-dasharray', '8,4');
    } else if (exploitVisuals.trailEffect === 'dotted') {
        trail.setAttribute('stroke-dasharray', '2,4');
    } else if (exploitVisuals.trailEffect === 'electric') {
        trail.setAttribute('stroke-dasharray', '3,3');
        trail.style.filter = 'drop-shadow(0 0 3px ' + exploitVisuals.glowColor + ')';
    }
    
    trail.style.animation = 'trailFade 0.5s ease-out forwards';
    packetGroup.appendChild(trail);
    
    // Create animated packet circle with glow effect
    const packet = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    packet.setAttribute('cx', startX);
    packet.setAttribute('cy', '135');
    packet.setAttribute('r', exploitVisuals.size);
    packet.setAttribute('fill', exploitVisuals.color);
    packet.setAttribute('stroke', exploitVisuals.glowColor);
    packet.setAttribute('stroke-width', '4');
    packet.style.filter = `drop-shadow(0 0 20px ${exploitVisuals.glowColor}) drop-shadow(0 0 10px ${exploitVisuals.glowColor})`;
    
    // Add pulsing animation based on speed
    const pulseClass = `pulse-${exploitVisuals.pulseSpeed}`;
    packet.classList.add(pulseClass);
    
    packetGroup.appendChild(packet);
    
    // Create icon on packet
    const icon = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    icon.setAttribute('x', startX);
    icon.setAttribute('y', '140');
    icon.setAttribute('text-anchor', 'middle');
    icon.setAttribute('font-size', '20');
    icon.textContent = attackIcon;
    packetGroup.appendChild(icon);
    
    packetsGroup.appendChild(packetGroup);
    
    // Track active animation
    activeAnimations++;
    
    // Add pulse effect to nodes
    const attackerNode = document.getElementById('attackerNode');
    const targetNode = document.getElementById('targetNode');
    attackerNode.classList.add('attacker-active');
    targetNode.classList.add('target-active');
    
    // For reverse shells, show persistent connection line
    if (isReverseShell) {
        showConnectionLine(attack.src_ip, attack.dst_ip);
    }
    
    // Make animation more pronounced with larger packet
    packet.setAttribute('r', exploitVisuals.size * 2.2);
    packet.setAttribute('stroke-width', '5');
    
    // Animate packet
    let position = startX;
    const duration = 3000; // 3 seconds for more dramatic effect
    const startTime = Date.now();
    
    const animate = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Ease-in-out function
        const easeProgress = progress < 0.5
            ? 2 * progress * progress
            : 1 - Math.pow(-2 * progress + 2, 2) / 2;
        
        position = startX + (endX - startX) * easeProgress;
        
        // Update packet position with pronounced wave motion
        const wave = Math.sin(progress * Math.PI * 3) * 15;
        packet.setAttribute('cx', position);
        packet.setAttribute('cy', 135 + wave);
        packet.setAttribute('opacity', 1 - progress * 0.3);
        
        // Update icon position
        icon.setAttribute('x', position);
        icon.setAttribute('y', 140 + wave);
        icon.setAttribute('opacity', 1 - progress * 0.3);
        
        // Update trail
        trail.setAttribute('x2', position);
        trail.setAttribute('y2', 135 + wave);
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        } else {
            // Impact: shake victim computer and add crack
            shakeAndCrackVictim();
            
            // Remove packet after animation
            packetGroup.remove();
            
            // Remove pulse after short delay
            setTimeout(() => {
                attackerNode.classList.remove('attacker-active');
                targetNode.classList.remove('target-active');
                
                // Animation complete
                activeAnimations--;
                checkAndLaunchConfetti();
            }, 800);
        }
    };
    
    requestAnimationFrame(animate);
}

// Shake and crack victim computer on exploit impact
function shakeAndCrackVictim() {
    const targetNode = document.getElementById('targetNode');
    const victimMonitor = targetNode.querySelector('.victim-monitor');
    
    // Add shake effect
    targetNode.classList.add('computer-shake');
    setTimeout(() => targetNode.classList.remove('computer-shake'), 600);
    
    // Add progressive crack effect
    const crackCount = detectedExploits.size;
    const cracksGroup = document.getElementById('computerCracks') || createCracksGroup();
    
    // Add new crack based on exploit count
    addCrack(cracksGroup, crackCount);
    
    // On 7th (final) exploit, make it dramatic
    if (crackCount === 7) {
        setTimeout(() => {
            targetNode.classList.add('computer-destroyed');
        }, 600);
    }
}

// Create SVG group for cracks
function createCracksGroup() {
    const targetNode = document.getElementById('targetNode');
    const cracksGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    cracksGroup.setAttribute('id', 'computerCracks');
    targetNode.appendChild(cracksGroup);
    return cracksGroup;
}

// Add a crack line to the victim computer (glass-breaking effect)
function addCrack(cracksGroup, crackNumber) {
    // Glass shatter patterns - realistic branching cracks with spider-web effect (adjusted for 2x larger screen)
    const crackPatterns = [
        // Crack 1: Top-left impact with branches (adjusted for new screen coords)
        'M 640 90 L 650 105 M 645 95 L 635 88 M 650 105 L 655 115 M 650 105 L 648 118',
        
        // Crack 2: Top-right with multiple branches
        'M 760 85 L 755 100 M 760 85 L 765 80 M 755 100 L 750 115 M 755 100 L 760 112 L 765 125',
        
        // Crack 3: Left side spider-web
        'M 630 110 L 645 120 M 638 118 L 628 125 M 645 120 L 655 130 M 645 120 L 648 108',
        
        // Crack 4: Right side radiating cracks
        'M 770 105 L 762 120 M 766 115 L 773 108 M 762 120 L 758 132 M 762 120 L 768 130 M 762 120 L 765 140',
        
        // Crack 5: Center impact with star pattern
        'M 700 105 L 700 120 M 700 115 L 692 107 M 700 115 L 708 107 M 700 120 L 695 132 M 700 120 L 705 132 M 700 120 L 700 140',
        
        // Crack 6: Bottom diagonal with spreading
        'M 635 140 L 650 128 M 642 137 L 635 150 M 650 128 L 700 120 M 650 128 L 655 140 M 700 120 L 710 128 M 710 128 L 720 137 M 710 128 L 715 140',
        
        // Crack 7: Final devastating full shatter (adjusted for larger screen)
        'M 625 80 L 700 135 M 625 80 L 632 70 M 625 80 L 620 90 M 700 135 L 775 180 M 700 135 L 770 165 M 775 180 L 778 185 M 640 85 L 700 120 M 760 88 L 750 110 M 645 160 L 655 140 M 755 160 L 745 140 M 630 105 L 650 125 M 770 110 L 750 125'
    ];
    
    if (crackNumber <= crackPatterns.length) {
        const crack = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        crack.setAttribute('d', crackPatterns[crackNumber - 1]);
        crack.setAttribute('stroke', '#ffffff');  // White cracks like broken glass
        crack.setAttribute('stroke-width', crackNumber === 7 ? '2.5' : '1.5');
        crack.setAttribute('fill', 'none');
        crack.setAttribute('opacity', '0');
        crack.setAttribute('stroke-linecap', 'round');
        crack.setAttribute('stroke-linejoin', 'round');
        
        // Glass-like effect with blue-white shimmer
        crack.style.filter = 'drop-shadow(0 0 2px rgba(100, 200, 255, 0.8)) drop-shadow(0 0 4px rgba(255, 255, 255, 0.6))';
        
        cracksGroup.appendChild(crack);
        
        // Animate crack appearing with glass-breaking effect
        setTimeout(() => {
            crack.setAttribute('opacity', '0.85');
            crack.style.transition = 'opacity 0.2s ease-out';
        }, 50);
        
        // Add glass fragment highlights
        if (crackNumber >= 3) {
            addGlassFragments(cracksGroup, crackNumber);
        }
    }
}

// Add glass fragment highlights for more realistic shattering
function addGlassFragments(cracksGroup, crackNumber) {
    const fragmentPositions = [
        { x: 685, y: 145 },
        { x: 710, y: 140 },
        { x: 695, y: 155 }
    ];
    
    fragmentPositions.forEach((pos, index) => {
        if (index < crackNumber - 2) {
            const fragment = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            fragment.setAttribute('cx', pos.x);
            fragment.setAttribute('cy', pos.y);
            fragment.setAttribute('r', '1.5');
            fragment.setAttribute('fill', '#ffffff');
            fragment.setAttribute('opacity', '0');
            fragment.style.filter = 'blur(0.5px)';
            
            cracksGroup.appendChild(fragment);
            
            setTimeout(() => {
                fragment.setAttribute('opacity', '0.7');
                fragment.style.transition = 'opacity 0.3s';
            }, 100 + index * 50);
        }
    });
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
    line.setAttribute('x1', '620');  // From victim (right)
    line.setAttribute('y1', '135');
    line.setAttribute('x2', '180');  // To attacker (left)
    line.setAttribute('y2', '135');
    line.setAttribute('class', 'connection-line');
    line.setAttribute('id', `conn-${connectionKey.replace(/[.:]/g, '-')}`);
    
    // Calculate line length for animation (distance from right to left)
    const lineLength = 440; // 620 - 180 = 440
    
    // Set up stroke-dasharray for drawing animation
    line.style.strokeDasharray = lineLength;
    line.style.strokeDashoffset = lineLength;
    
    connectionGroup.appendChild(line);
    
    // Animate line drawing from right to left over 2 seconds
    setTimeout(() => {
        line.style.transition = 'stroke-dashoffset 2s ease-out';
        line.style.strokeDashoffset = '0';
    }, 10);
    
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
        'struts2_rce': '☕',      // Apache Struts2
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

// Get exploit-specific visual properties
function getExploitVisuals(attackType) {
    const exploitStyles = {
        // EternalBlue: Devastating worm-like spread, blue glow (NSA tool leaked)
        'ms17_010': {
            color: '#3b82f6',
            glowColor: '#60a5fa',
            size: 18,
            pulseSpeed: 'fast',
            trailEffect: 'electric'
        },
        // Apache Struts2: Java web framework RCE, coffee brown (CVE-2017-5638)
        'struts2_rce': {
            color: '#92400e',
            glowColor: '#d97706',
            size: 16,
            pulseSpeed: 'medium',
            trailEffect: 'solid'
        },
        // VSFTPD Backdoor: Stealthy backdoor, purple/magenta (hidden smiley face trigger)
        'vsftpd_backdoor': {
            color: '#7c3aed',
            glowColor: '#a78bfa',
            size: 15,
            pulseSpeed: 'slow',
            trailEffect: 'dashed'
        },
        // Tomcat Manager: Web-based deployment, orange (manager console abuse)
        'tomcat_mgr': {
            color: '#ea580c',
            glowColor: '#fb923c',
            size: 16,
            pulseSpeed: 'medium',
            trailEffect: 'dotted'
        },
        // Shellshock: Bash exploit, green terminal (environment variable injection)
        'shellshock': {
            color: '#16a34a',
            glowColor: '#4ade80',
            size: 17,
            pulseSpeed: 'fast',
            trailEffect: 'electric'
        },
        // SQL Injection: Database attack, cyan/teal (query manipulation)
        'sql_injection': {
            color: '#0891b2',
            glowColor: '#22d3ee',
            size: 16,
            pulseSpeed: 'medium',
            trailEffect: 'wavy'
        },
        // Reverse Shell: Callback connection, bright red (attacker control)
        'reverse_shell': {
            color: '#dc2626',
            glowColor: '#ef4444',
            size: 18,
            pulseSpeed: 'fast',
            trailEffect: 'solid-thick'
        }
    };
    
    return exploitStyles[attackType] || {
        color: '#9aa0a6',
        glowColor: '#6b7280',
        size: 8,
        pulseSpeed: 'medium',
        trailEffect: 'solid'
    };
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

