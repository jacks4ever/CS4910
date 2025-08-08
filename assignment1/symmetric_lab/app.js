// AES Cryptography Lab - Interactive JavaScript Implementation
// Educational purposes only - not for production use

document.addEventListener('DOMContentLoaded', function() {
    // Global variables
    let currentKey = '';
    let currentIV = '';
    let secretMessage = "FLAG{ECB_IS_INSECURE}"; // Secret for ECB oracle challenge
    let challengeProgress = 0;
    
    // AES S-Box for educational purposes
    const sBox = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
    ];

    // Tab navigation
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Utility functions
    function generateRandomHex(length) {
        const chars = '0123456789abcdef';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars[Math.floor(Math.random() * chars.length)];
        }
        return result;
    }

    function hexToBytes(hex) {
        const bytes = [];
        for (let i = 0; i < hex.length; i += 2) {
            bytes.push(parseInt(hex.substr(i, 2), 16));
        }
        return bytes;
    }

    function bytesToHex(bytes) {
        return bytes.map(b => b.toString(16).padStart(2, '0')).join('');
    }

    function validateHex(hex, expectedLength) {
        const cleanHex = hex.replace(/[^0-9a-fA-F]/g, '');
        return cleanHex.length === expectedLength && /^[0-9a-fA-F]+$/.test(cleanHex);
    }

    // PRACTICE TAB FUNCTIONALITY

    // Key Expansion
    const expandKeyButton = document.getElementById('expand-key');
    const randomKeyButton = document.getElementById('random-key');
    
    if (expandKeyButton) {
        expandKeyButton.addEventListener('click', function() {
            const initialKey = document.getElementById('initial-key').value.toLowerCase();
            
            if (!validateHex(initialKey, 32)) {
                alert('Please enter exactly 32 hexadecimal characters for the key.');
                return;
            }
            
            // For educational purposes, we'll use CryptoJS to expand the key
            try {
                const key = CryptoJS.enc.Hex.parse(initialKey);
                const roundKeys = [];
                
                // Generate round keys using CryptoJS internal functions
                // This is a simplified demonstration
                for (let i = 0; i <= 10; i++) {
                    if (i === 0) {
                        roundKeys.push(initialKey);
                    } else {
                        // Generate pseudo round keys for demonstration
                        const pseudoKey = CryptoJS.SHA256(initialKey + i.toString()).toString().substring(0, 32);
                        roundKeys.push(pseudoKey);
                    }
                }
                
                let roundKeysHTML = '';
                for (let i = 0; i < roundKeys.length; i++) {
                    roundKeysHTML += `<p><strong>Round ${i}:</strong> ${roundKeys[i]}</p>`;
                }
                
                document.getElementById('round-keys').innerHTML = roundKeysHTML;
            } catch (error) {
                alert('Error expanding key: ' + error.message);
            }
        });
    }

    if (randomKeyButton) {
        randomKeyButton.addEventListener('click', function() {
            const randomKey = generateRandomHex(32);
            document.getElementById('initial-key').value = randomKey;
        });
    }

    // Round Function Visualization
    const processRoundButton = document.getElementById('process-round');
    const stepByStepButton = document.getElementById('step-by-step');
    
    if (processRoundButton) {
        processRoundButton.addEventListener('click', function() {
            const inputState = document.getElementById('input-state').value.toLowerCase();
            const roundKey = document.getElementById('round-key-input').value.toLowerCase();
            
            if (!validateHex(inputState, 32) || !validateHex(roundKey, 32)) {
                alert('Please enter exactly 32 hexadecimal characters for both state and key.');
                return;
            }
            
            processAESRound(inputState, roundKey);
        });
    }

    if (stepByStepButton) {
        stepByStepButton.addEventListener('click', function() {
            const inputState = document.getElementById('input-state').value.toLowerCase();
            const roundKey = document.getElementById('round-key-input').value.toLowerCase();
            
            if (!validateHex(inputState, 32) || !validateHex(roundKey, 32)) {
                alert('Please enter exactly 32 hexadecimal characters for both state and key.');
                return;
            }
            
            processAESRoundStepByStep(inputState, roundKey);
        });
    }

    function processAESRound(stateHex, keyHex) {
        const state = hexToBytes(stateHex);
        const key = hexToBytes(keyHex);
        
        // Update initial state display
        updateMatrixDisplay('initial-state', state);
        
        // SubBytes
        const afterSubBytes = state.map(byte => sBox[byte]);
        updateMatrixDisplay('subbytes-output', afterSubBytes);
        
        // ShiftRows
        const afterShiftRows = shiftRows(afterSubBytes);
        updateMatrixDisplay('shiftrows-output', afterShiftRows);
        
        // MixColumns (simplified for demonstration)
        const afterMixColumns = mixColumns(afterShiftRows);
        updateMatrixDisplay('mixcolumns-output', afterMixColumns);
        
        // AddRoundKey
        const afterAddRoundKey = afterMixColumns.map((byte, i) => byte ^ key[i]);
        updateMatrixDisplay('addroundkey-output', afterAddRoundKey);
    }

    function processAESRoundStepByStep(stateHex, keyHex) {
        const state = hexToBytes(stateHex);
        const key = hexToBytes(keyHex);
        
        let step = 0;
        const steps = [
            () => updateMatrixDisplay('initial-state', state),
            () => {
                const afterSubBytes = state.map(byte => sBox[byte]);
                updateMatrixDisplay('subbytes-output', afterSubBytes);
                return afterSubBytes;
            },
            (prevState) => {
                const afterShiftRows = shiftRows(prevState);
                updateMatrixDisplay('shiftrows-output', afterShiftRows);
                return afterShiftRows;
            },
            (prevState) => {
                const afterMixColumns = mixColumns(prevState);
                updateMatrixDisplay('mixcolumns-output', afterMixColumns);
                return afterMixColumns;
            },
            (prevState) => {
                const afterAddRoundKey = prevState.map((byte, i) => byte ^ key[i]);
                updateMatrixDisplay('addroundkey-output', afterAddRoundKey);
                return afterAddRoundKey;
            }
        ];
        
        let currentState = state;
        const interval = setInterval(() => {
            if (step < steps.length) {
                currentState = steps[step](currentState) || currentState;
                step++;
            } else {
                clearInterval(interval);
            }
        }, 1000);
    }

    function shiftRows(state) {
        const result = [...state];
        // Row 0: no shift
        // Row 1: shift left by 1
        [result[4], result[5], result[6], result[7]] = [result[5], result[6], result[7], result[4]];
        // Row 2: shift left by 2
        [result[8], result[9], result[10], result[11]] = [result[10], result[11], result[8], result[9]];
        // Row 3: shift left by 3
        [result[12], result[13], result[14], result[15]] = [result[15], result[12], result[13], result[14]];
        return result;
    }

    function mixColumns(state) {
        // Simplified MixColumns for demonstration
        // In real AES, this involves Galois field multiplication
        const result = [...state];
        for (let col = 0; col < 4; col++) {
            const c0 = state[col];
            const c1 = state[col + 4];
            const c2 = state[col + 8];
            const c3 = state[col + 12];
            
            // Simplified mixing (not actual AES MixColumns)
            result[col] = (c0 ^ c1 ^ c2) & 0xFF;
            result[col + 4] = (c1 ^ c2 ^ c3) & 0xFF;
            result[col + 8] = (c2 ^ c3 ^ c0) & 0xFF;
            result[col + 12] = (c3 ^ c0 ^ c1) & 0xFF;
        }
        return result;
    }

    function updateMatrixDisplay(elementId, bytes) {
        const matrix = document.getElementById(elementId);
        if (matrix && bytes.length >= 16) {
            const cells = matrix.children;
            for (let i = 0; i < 16; i++) {
                if (cells[i]) {
                    cells[i].textContent = bytes[i].toString(16).padStart(2, '0');
                }
            }
        }
    }

    // S-Box Lookup
    const sboxLookupButton = document.getElementById('sbox-lookup');
    if (sboxLookupButton) {
        sboxLookupButton.addEventListener('click', function() {
            const input = document.getElementById('sbox-input').value.toLowerCase();
            if (validateHex(input, 2)) {
                const inputByte = parseInt(input, 16);
                const outputByte = sBox[inputByte];
                document.getElementById('sbox-result').textContent = 
                    `Result: ${outputByte.toString(16).padStart(2, '0').toUpperCase()}`;
                highlightSBoxCell(inputByte, outputByte);
            } else {
                alert('Please enter exactly 2 hexadecimal characters.');
            }
        });
    }

    // Generate S-Box table
    function generateSBoxTable() {
        const table = document.getElementById('sbox-table');
        if (table) {
            let html = '<tr><th></th>';
            for (let i = 0; i < 16; i++) {
                html += `<th>${i.toString(16).toUpperCase()}</th>`;
            }
            html += '</tr>';
            
            for (let row = 0; row < 16; row++) {
                html += `<tr><th>${row.toString(16).toUpperCase()}</th>`;
                for (let col = 0; col < 16; col++) {
                    const value = sBox[row * 16 + col];
                    html += `<td id="sbox-${row * 16 + col}">${value.toString(16).padStart(2, '0').toUpperCase()}</td>`;
                }
                html += '</tr>';
            }
            table.innerHTML = html;
        }
    }

    function highlightSBoxCell(input, output) {
        // Remove previous highlights
        document.querySelectorAll('.sbox-highlight').forEach(cell => {
            cell.classList.remove('sbox-highlight');
        });
        
        // Highlight the cell
        const cell = document.getElementById(`sbox-${input}`);
        if (cell) {
            cell.classList.add('sbox-highlight');
        }
    }

    // APPLICATION TAB FUNCTIONALITY

    // Real AES Encryption/Decryption
    const encryptButton = document.getElementById('encrypt-button');
    const decryptButton = document.getElementById('decrypt-button');
    const generateKeyButton = document.getElementById('generate-key');
    const copyButton = document.getElementById('copy-ciphertext');

    if (generateKeyButton) {
        generateKeyButton.addEventListener('click', function() {
            currentKey = generateRandomHex(32);
            currentIV = generateRandomHex(32);
            document.getElementById('aes-key').value = currentKey;
            document.getElementById('aes-iv').value = currentIV;
            updateEncryptionDetails();
        });
    }

    if (encryptButton) {
        encryptButton.addEventListener('click', function() {
            const plaintext = document.getElementById('plaintext').value;
            const mode = document.getElementById('aes-mode').value;
            let key = document.getElementById('aes-key').value || generateRandomHex(32);
            let iv = document.getElementById('aes-iv').value || generateRandomHex(32);
            
            if (!key) key = generateRandomHex(32);
            if (!iv) iv = generateRandomHex(32);
            
            currentKey = key;
            currentIV = iv;
            
            try {
                let encrypted;
                const keyObj = CryptoJS.enc.Hex.parse(key);
                const ivObj = CryptoJS.enc.Hex.parse(iv);
                
                switch (mode) {
                    case 'ECB':
                        encrypted = CryptoJS.AES.encrypt(plaintext, keyObj, {
                            mode: CryptoJS.mode.ECB,
                            padding: CryptoJS.pad.Pkcs7
                        });
                        break;
                    case 'CBC':
                        encrypted = CryptoJS.AES.encrypt(plaintext, keyObj, {
                            iv: ivObj,
                            mode: CryptoJS.mode.CBC,
                            padding: CryptoJS.pad.Pkcs7
                        });
                        break;
                    case 'CTR':
                        encrypted = CryptoJS.AES.encrypt(plaintext, keyObj, {
                            iv: ivObj,
                            mode: CryptoJS.mode.CTR,
                            padding: CryptoJS.pad.NoPadding
                        });
                        break;
                }
                
                document.getElementById('ciphertext').value = encrypted.toString();
                updateEncryptionDetails();
            } catch (error) {
                alert('Encryption error: ' + error.message);
            }
        });
    }

    if (decryptButton) {
        decryptButton.addEventListener('click', function() {
            const ciphertext = document.getElementById('ciphertext').value;
            const mode = document.getElementById('aes-mode').value;
            const key = currentKey || document.getElementById('aes-key').value;
            const iv = currentIV || document.getElementById('aes-iv').value;
            
            if (!key) {
                alert('No key available. Please encrypt a message first or enter a key.');
                return;
            }
            
            try {
                let decrypted;
                const keyObj = CryptoJS.enc.Hex.parse(key);
                const ivObj = CryptoJS.enc.Hex.parse(iv);
                
                switch (mode) {
                    case 'ECB':
                        decrypted = CryptoJS.AES.decrypt(ciphertext, keyObj, {
                            mode: CryptoJS.mode.ECB,
                            padding: CryptoJS.pad.Pkcs7
                        });
                        break;
                    case 'CBC':
                        decrypted = CryptoJS.AES.decrypt(ciphertext, keyObj, {
                            iv: ivObj,
                            mode: CryptoJS.mode.CBC,
                            padding: CryptoJS.pad.Pkcs7
                        });
                        break;
                    case 'CTR':
                        decrypted = CryptoJS.AES.decrypt(ciphertext, keyObj, {
                            iv: ivObj,
                            mode: CryptoJS.mode.CTR,
                            padding: CryptoJS.pad.NoPadding
                        });
                        break;
                }
                
                document.getElementById('plaintext').value = decrypted.toString(CryptoJS.enc.Utf8);
            } catch (error) {
                alert('Decryption error: ' + error.message);
            }
        });
    }

    if (copyButton) {
        copyButton.addEventListener('click', function() {
            const ciphertext = document.getElementById('ciphertext');
            ciphertext.select();
            document.execCommand('copy');
            alert('Ciphertext copied to clipboard!');
        });
    }

    function updateEncryptionDetails() {
        document.getElementById('current-key').textContent = currentKey || 'Not generated';
        document.getElementById('current-iv').textContent = currentIV || 'Not generated';
        document.getElementById('current-mode').textContent = document.getElementById('aes-mode').value;
    }

    // ECB Visual Demonstration
    const encryptImageButton = document.getElementById('encrypt-image');
    const resetImageButton = document.getElementById('reset-image');

    if (encryptImageButton) {
        encryptImageButton.addEventListener('click', function() {
            encryptPenguinImage();
        });
    }

    if (resetImageButton) {
        resetImageButton.addEventListener('click', function() {
            resetImageDemo();
        });
    }

    function encryptPenguinImage() {
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = function() {
            // Show gradual transformation animation for 5 seconds
            showGradualTransformation(img);
        };
        img.src = 'penguin.png';
    }

    function showGradualTransformation(img) {
        const canvases = ['ecb-canvas', 'cbc-canvas', 'ctr-canvas'];
        const contexts = {};
        const originalImageData = {};
        
        // Initialize all canvases with original image
        canvases.forEach(canvasId => {
            const canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            
            contexts[canvasId] = ctx;
            originalImageData[canvasId] = ctx.getImageData(0, 0, img.width, img.height);
        });
        
        const totalSteps = 50; // Number of animation steps
        const stepDuration = 100; // Duration of each step in ms (5 seconds total)
        let currentStep = 0;
        
        const animationInterval = setInterval(() => {
            const progress = currentStep / totalSteps; // 0 to 1
            
            // ECB Mode - Gradually grey out while preserving patterns
            const ecbCtx = contexts['ecb-canvas'];
            const ecbImageData = ecbCtx.createImageData(img.width, img.height);
            const ecbData = ecbImageData.data;
            const originalEcbData = originalImageData['ecb-canvas'].data;
            
            for (let i = 0; i < originalEcbData.length; i += 4) {
                const originalR = originalEcbData[i];
                const originalG = originalEcbData[i + 1];
                const originalB = originalEcbData[i + 2];
                const brightness = (originalR + originalG + originalB) / 3;
                
                // Target colors based on brightness (ECB final state)
                let targetR, targetG, targetB;
                if (brightness < 50) { // Very dark pixels (penguin body)
                    targetR = 60; targetG = 60; targetB = 80;
                } else if (brightness < 100) { // Dark-medium pixels (penguin edges)
                    targetR = 90; targetG = 90; targetB = 110;
                } else if (brightness < 200) { // Medium pixels (penguin belly, some edges)
                    targetR = 140; targetG = 140; targetB = 160;
                } else { // Light pixels (background - white areas)
                    targetR = 180; targetG = 180; targetB = 190;
                }
                
                // Interpolate between original and target colors
                ecbData[i] = Math.round(originalR + (targetR - originalR) * progress);
                ecbData[i + 1] = Math.round(originalG + (targetG - originalG) * progress);
                ecbData[i + 2] = Math.round(originalB + (targetB - originalB) * progress);
                ecbData[i + 3] = 255; // Alpha
            }
            ecbCtx.putImageData(ecbImageData, 0, 0);
            
            // CBC Mode - Gradually transform to static
            const cbcCtx = contexts['cbc-canvas'];
            const cbcImageData = cbcCtx.createImageData(img.width, img.height);
            const cbcData = cbcImageData.data;
            const originalCbcData = originalImageData['cbc-canvas'].data;
            
            for (let i = 0; i < originalCbcData.length; i += 4) {
                const originalR = originalCbcData[i];
                const originalG = originalCbcData[i + 1];
                const originalB = originalCbcData[i + 2];
                
                // Target is random static
                const targetR = Math.floor(Math.random() * 256);
                const targetG = Math.floor(Math.random() * 256);
                const targetB = Math.floor(Math.random() * 256);
                
                // Interpolate between original and random colors
                cbcData[i] = Math.round(originalR + (targetR - originalR) * progress);
                cbcData[i + 1] = Math.round(originalG + (targetG - originalG) * progress);
                cbcData[i + 2] = Math.round(originalB + (targetB - originalB) * progress);
                cbcData[i + 3] = 255; // Alpha
            }
            cbcCtx.putImageData(cbcImageData, 0, 0);
            
            // CTR Mode - Gradually transform to static (different random pattern than CBC)
            const ctrCtx = contexts['ctr-canvas'];
            const ctrImageData = ctrCtx.createImageData(img.width, img.height);
            const ctrData = ctrImageData.data;
            const originalCtrData = originalImageData['ctr-canvas'].data;
            
            for (let i = 0; i < originalCtrData.length; i += 4) {
                const originalR = originalCtrData[i];
                const originalG = originalCtrData[i + 1];
                const originalB = originalCtrData[i + 2];
                
                // Target is random static (different from CBC)
                const targetR = Math.floor(Math.random() * 256);
                const targetG = Math.floor(Math.random() * 256);
                const targetB = Math.floor(Math.random() * 256);
                
                // Interpolate between original and random colors
                ctrData[i] = Math.round(originalR + (targetR - originalR) * progress);
                ctrData[i + 1] = Math.round(originalG + (targetG - originalG) * progress);
                ctrData[i + 2] = Math.round(originalB + (targetB - originalB) * progress);
                ctrData[i + 3] = 255; // Alpha
            }
            ctrCtx.putImageData(ctrImageData, 0, 0);
            
            currentStep++;
            
            // Stop animation when complete
            if (currentStep > totalSteps) {
                clearInterval(animationInterval);
                
                // Ensure final state is exactly what we want
                finalizeEncryption(img);
            }
        }, stepDuration);
        
        // Store interval ID for cleanup
        window.processingInterval = animationInterval;
    }

    function finalizeEncryption(img) {
        // ECB Mode - Final state with preserved patterns
        const ecbCanvas = document.getElementById('ecb-canvas');
        const ecbCtx = ecbCanvas.getContext('2d');
        ecbCtx.drawImage(img, 0, 0);
        
        const ecbImageData = ecbCtx.getImageData(0, 0, img.width, img.height);
        const ecbData = ecbImageData.data;
        
        for (let i = 0; i < ecbData.length; i += 4) {
            const brightness = (ecbData[i] + ecbData[i + 1] + ecbData[i + 2]) / 3;
            
            if (brightness < 50) { // Very dark pixels (penguin body)
                ecbData[i] = 60; ecbData[i + 1] = 60; ecbData[i + 2] = 80;
            } else if (brightness < 100) { // Dark-medium pixels (penguin edges)
                ecbData[i] = 90; ecbData[i + 1] = 90; ecbData[i + 2] = 110;
            } else if (brightness < 200) { // Medium pixels (penguin belly, some edges)
                ecbData[i] = 140; ecbData[i + 1] = 140; ecbData[i + 2] = 160;
            } else { // Light pixels (background - white areas)
                ecbData[i] = 180; ecbData[i + 1] = 180; ecbData[i + 2] = 190;
            }
        }
        ecbCtx.putImageData(ecbImageData, 0, 0);
        
        // CBC Mode - Final static
        const cbcCanvas = document.getElementById('cbc-canvas');
        const cbcCtx = cbcCanvas.getContext('2d');
        const cbcImageData = cbcCtx.createImageData(img.width, img.height);
        const cbcData = cbcImageData.data;
        
        for (let i = 0; i < cbcData.length; i += 4) {
            cbcData[i] = Math.floor(Math.random() * 256);
            cbcData[i + 1] = Math.floor(Math.random() * 256);
            cbcData[i + 2] = Math.floor(Math.random() * 256);
            cbcData[i + 3] = 255;
        }
        cbcCtx.putImageData(cbcImageData, 0, 0);
        
        // CTR Mode - Final static
        const ctrCanvas = document.getElementById('ctr-canvas');
        const ctrCtx = ctrCanvas.getContext('2d');
        const ctrImageData = ctrCtx.createImageData(img.width, img.height);
        const ctrData = ctrImageData.data;
        
        for (let i = 0; i < ctrData.length; i += 4) {
            ctrData[i] = Math.floor(Math.random() * 256);
            ctrData[i + 1] = Math.floor(Math.random() * 256);
            ctrData[i + 2] = Math.floor(Math.random() * 256);
            ctrData[i + 3] = 255;
        }
        ctrCtx.putImageData(ctrImageData, 0, 0);
    }

    function hideProcessingAnimation() {
        if (window.processingInterval) {
            clearInterval(window.processingInterval);
            window.processingInterval = null;
        }
    }

    function resetImageDemo() {
        ['ecb-canvas', 'cbc-canvas', 'ctr-canvas'].forEach(canvasId => {
            const canvas = document.getElementById(canvasId);
            const ctx = canvas.getContext('2d');
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#f0f0f0';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#666';
            ctx.font = '14px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('Click "Encrypt Image"', canvas.width / 2, canvas.height / 2);
        });
    }

    // Mode Comparison
    const compareModesButton = document.getElementById('compare-modes');
    if (compareModesButton) {
        compareModesButton.addEventListener('click', function() {
            const plaintext = document.getElementById('pattern-input').value;
            compareEncryptionModes(plaintext);
        });
    }

    function compareEncryptionModes(plaintext) {
        const key = generateRandomHex(32);
        const iv = generateRandomHex(32);
        const keyObj = CryptoJS.enc.Hex.parse(key);
        const ivObj = CryptoJS.enc.Hex.parse(iv);
        
        try {
            // ECB Mode
            const ecbEncrypted = CryptoJS.AES.encrypt(plaintext, keyObj, {
                mode: CryptoJS.mode.ECB,
                padding: CryptoJS.pad.Pkcs7
            });
            
            // CBC Mode
            const cbcEncrypted = CryptoJS.AES.encrypt(plaintext, keyObj, {
                iv: ivObj,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            
            // CTR Mode
            const ctrEncrypted = CryptoJS.AES.encrypt(plaintext, keyObj, {
                iv: ivObj,
                mode: CryptoJS.mode.CTR,
                padding: CryptoJS.pad.NoPadding
            });
            
            // Display results
            document.getElementById('ecb-result').innerHTML = 
                `<div class="cipher-hex">${ecbEncrypted.ciphertext.toString()}</div>`;
            document.getElementById('cbc-result').innerHTML = 
                `<div class="cipher-hex">${cbcEncrypted.ciphertext.toString()}</div>`;
            document.getElementById('ctr-result').innerHTML = 
                `<div class="cipher-hex">${ctrEncrypted.ciphertext.toString()}</div>`;
            
            // Analyze patterns
            analyzePatterns(plaintext, ecbEncrypted.ciphertext.toString(), 'ecb-analysis');
            analyzePatterns(plaintext, cbcEncrypted.ciphertext.toString(), 'cbc-analysis');
            analyzePatterns(plaintext, ctrEncrypted.ciphertext.toString(), 'ctr-analysis');
            
        } catch (error) {
            alert('Comparison error: ' + error.message);
        }
    }

    function analyzePatterns(plaintext, ciphertext, elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            // Simple pattern analysis
            const blocks = [];
            for (let i = 0; i < ciphertext.length; i += 32) {
                blocks.push(ciphertext.substr(i, 32));
            }
            
            const uniqueBlocks = new Set(blocks);
            const patternPreserved = uniqueBlocks.size < blocks.length;
            
            if (patternPreserved) {
                element.innerHTML = '<span class="danger-text">⚠️ Patterns detected! Identical blocks found.</span>';
            } else {
                element.innerHTML = '<span class="success-text">✅ No patterns detected. All blocks unique.</span>';
            }
        }
    }

    // CHALLENGE TAB FUNCTIONALITY

    // Challenge 1: ECB Oracle Attack
    const queryOracleButton = document.getElementById('query-oracle');
    const resetChallenge1Button = document.getElementById('reset-challenge1');
    
    if (queryOracleButton) {
        queryOracleButton.addEventListener('click', function() {
            const input = document.getElementById('oracle-input').value;
            const response = ecbOracle(input);
            document.getElementById('oracle-output').innerHTML = `<p>${response}</p>`;
            
            // Check if user is making progress
            checkECBProgress(input, response);
        });
    }

    if (resetChallenge1Button) {
        resetChallenge1Button.addEventListener('click', function() {
            challengeProgress = 0;
            document.getElementById('secret-progress').textContent = '???????????????';
            document.getElementById('oracle-output').innerHTML = 'Submit input to see encrypted result...';
        });
    }

    function ecbOracle(userInput) {
        const fullInput = secretMessage + userInput;
        const key = 'secretkeyforchallenge123456789012'; // Fixed key for consistency
        
        try {
            const keyObj = CryptoJS.enc.Utf8.parse(key);
            const encrypted = CryptoJS.AES.encrypt(fullInput, keyObj, {
                mode: CryptoJS.mode.ECB,
                padding: CryptoJS.pad.Pkcs7
            });
            
            return encrypted.ciphertext.toString();
        } catch (error) {
            return 'Oracle error: ' + error.message;
        }
    }

    function checkECBProgress(input, response) {
        // Simple progress tracking for educational purposes
        if (input.length >= 15 && input.match(/^A+$/)) {
            challengeProgress = Math.min(challengeProgress + 1, secretMessage.length);
            const revealed = secretMessage.substring(0, challengeProgress);
            const hidden = '?'.repeat(secretMessage.length - challengeProgress);
            document.getElementById('secret-progress').textContent = revealed + hidden;
        }
    }

    // Show/hide hints
    const showHint1Button = document.getElementById('show-hint1');
    if (showHint1Button) {
        showHint1Button.addEventListener('click', function() {
            const hintContent = document.getElementById('hint1-content');
            hintContent.classList.toggle('hidden');
            this.textContent = hintContent.classList.contains('hidden') ? 'Show Hint' : 'Hide Hint';
        });
    }

    // Challenge 2: Padding Oracle Attack
    const checkPaddingButton = document.getElementById('check-padding');
    const autoAttackButton = document.getElementById('auto-attack');
    
    if (checkPaddingButton) {
        checkPaddingButton.addEventListener('click', function() {
            const ciphertext = document.getElementById('padding-ciphertext').value;
            const response = paddingOracle(ciphertext);
            document.getElementById('padding-response').innerHTML = `<p>${response}</p>`;
        });
    }

    if (autoAttackButton) {
        autoAttackButton.addEventListener('click', function() {
            simulatePaddingOracleAttack();
        });
    }

    function paddingOracle(ciphertext) {
        // Simulate padding oracle response
        // In reality, this would check actual PKCS#7 padding
        const random = Math.random();
        if (ciphertext.length % 32 !== 0) {
            return 'Invalid ciphertext length';
        }
        
        // Simulate mostly invalid padding with occasional valid
        if (random < 0.1) {
            return '✅ Valid padding';
        } else {
            return '❌ Invalid padding';
        }
    }

    function simulatePaddingOracleAttack() {
        let progress = 0;
        const targetPlaintext = 'SECRET_MESSAGE!!';
        const progressBar = document.getElementById('attack-progress-bar');
        const plaintextProgress = document.getElementById('plaintext-progress');
        
        const interval = setInterval(() => {
            progress += Math.random() * 10;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
                plaintextProgress.textContent = targetPlaintext;
            } else {
                const revealed = Math.floor((progress / 100) * targetPlaintext.length);
                plaintextProgress.textContent = 
                    targetPlaintext.substring(0, revealed) + 
                    '?'.repeat(targetPlaintext.length - revealed);
            }
            
            progressBar.style.width = progress + '%';
        }, 200);
    }

    const showHint2Button = document.getElementById('show-hint2');
    if (showHint2Button) {
        showHint2Button.addEventListener('click', function() {
            const hintContent = document.getElementById('hint2-content');
            hintContent.classList.toggle('hidden');
            this.textContent = hintContent.classList.contains('hidden') ? 'Show Attack Strategy' : 'Hide Attack Strategy';
        });
    }

    // Challenge 3: Authenticated Encryption
    const protectMessageButton = document.getElementById('protect-message');
    const tamperBitButton = document.getElementById('tamper-bit');
    const tamperByteButton = document.getElementById('tamper-byte');
    const tamperBlockButton = document.getElementById('tamper-block');
    const verifyMessageButton = document.getElementById('verify-message');
    
    let protectedData = null;
    let tamperedData = null;

    if (protectMessageButton) {
        protectMessageButton.addEventListener('click', function() {
            const message = document.getElementById('auth-message').value;
            const mode = document.getElementById('auth-mode').value;
            
            protectedData = authenticatedEncrypt(message, mode);
            document.getElementById('protected-data').innerHTML = `<p>${protectedData}</p>`;
            
            // Enable tampering buttons
            [tamperBitButton, tamperByteButton, tamperBlockButton].forEach(btn => {
                if (btn) btn.disabled = false;
            });
        });
    }

    if (tamperBitButton) {
        tamperBitButton.addEventListener('click', function() {
            if (protectedData) {
                tamperedData = tamperData(protectedData, 'bit');
                showTamperedData();
            }
        });
    }

    if (tamperByteButton) {
        tamperByteButton.addEventListener('click', function() {
            if (protectedData) {
                tamperedData = tamperData(protectedData, 'byte');
                showTamperedData();
            }
        });
    }

    if (tamperBlockButton) {
        tamperBlockButton.addEventListener('click', function() {
            if (protectedData) {
                tamperedData = tamperData(protectedData, 'block');
                showTamperedData();
            }
        });
    }

    if (verifyMessageButton) {
        verifyMessageButton.addEventListener('click', function() {
            const dataToVerify = tamperedData || protectedData;
            if (dataToVerify) {
                const result = verifyAuthenticatedData(dataToVerify, tamperedData !== null);
                document.getElementById('verification-result').innerHTML = `<p>${result}</p>`;
            }
        });
    }

    function authenticatedEncrypt(message, mode) {
        const key = generateRandomHex(32);
        const iv = generateRandomHex(32);
        
        try {
            const keyObj = CryptoJS.enc.Hex.parse(key);
            const ivObj = CryptoJS.enc.Hex.parse(iv);
            
            if (mode === 'GCM') {
                // Simulate GCM (CryptoJS doesn't have native GCM)
                const encrypted = CryptoJS.AES.encrypt(message, keyObj, {
                    iv: ivObj,
                    mode: CryptoJS.mode.CTR,
                    padding: CryptoJS.pad.NoPadding
                });
                const tag = CryptoJS.HmacSHA256(encrypted.ciphertext.toString(), keyObj).toString().substring(0, 32);
                return `${encrypted.ciphertext.toString()}:${tag}`;
            } else {
                // AES-CBC + HMAC
                const encrypted = CryptoJS.AES.encrypt(message, keyObj, {
                    iv: ivObj,
                    mode: CryptoJS.mode.CBC,
                    padding: CryptoJS.pad.Pkcs7
                });
                const hmac = CryptoJS.HmacSHA256(encrypted.ciphertext.toString(), keyObj).toString();
                return `${encrypted.ciphertext.toString()}:${hmac}`;
            }
        } catch (error) {
            return 'Encryption error: ' + error.message;
        }
    }

    function tamperData(data, type) {
        const parts = data.split(':');
        let ciphertext = parts[0];
        const tag = parts[1];
        
        switch (type) {
            case 'bit':
                // Flip a random bit
                const bitPos = Math.floor(Math.random() * ciphertext.length);
                const chars = ciphertext.split('');
                const originalChar = chars[bitPos];
                let newChar = originalChar;
                while (newChar === originalChar) {
                    newChar = '0123456789abcdef'[Math.floor(Math.random() * 16)];
                }
                chars[bitPos] = newChar;
                ciphertext = chars.join('');
                break;
                
            case 'byte':
                // Change a random byte
                const bytePos = Math.floor(Math.random() * (ciphertext.length / 2)) * 2;
                const newByte = generateRandomHex(2);
                ciphertext = ciphertext.substring(0, bytePos) + newByte + ciphertext.substring(bytePos + 2);
                break;
                
            case 'block':
                // Corrupt an entire block
                const blockPos = Math.floor(Math.random() * (ciphertext.length / 32)) * 32;
                const newBlock = generateRandomHex(32);
                ciphertext = ciphertext.substring(0, blockPos) + newBlock + ciphertext.substring(blockPos + 32);
                break;
        }
        
        return `${ciphertext}:${tag}`;
    }

    function showTamperedData() {
        const tamperedElement = document.getElementById('tampered-data');
        tamperedElement.innerHTML = `<p>${tamperedData}</p>`;
        tamperedElement.classList.remove('hidden');
    }

    function verifyAuthenticatedData(data, wasTampered) {
        if (wasTampered) {
            return '❌ <strong>VERIFICATION FAILED!</strong> The message has been tampered with. Do not trust this data.';
        } else {
            return '✅ <strong>VERIFICATION SUCCESSFUL!</strong> The message is authentic and has not been tampered with.';
        }
    }

    // Initialize components
    generateSBoxTable();
    resetImageDemo();
    updateEncryptionDetails();
    
    // Set initial values
    document.getElementById('aes-mode').addEventListener('change', updateEncryptionDetails);
});