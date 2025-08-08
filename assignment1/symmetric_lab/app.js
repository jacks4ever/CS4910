document.addEventListener('DOMContentLoaded', function() {
    // Tab navigation
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and contents
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Add active class to clicked button and corresponding content
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Practice Tab - Key Expansion
    const expandKeyButton = document.getElementById('expand-key');
    if (expandKeyButton) {
        expandKeyButton.addEventListener('click', function() {
            const initialKey = document.getElementById('initial-key').value;
            // In a real implementation, this would calculate the round keys
            // For this demo, we're using pre-calculated values
            const roundKeys = [
                "000102030405060708090a0b0c0d0e0f", // Initial key
                "d6aa74fdd2af72fadaa678f1d6ab76fe", // Round 1
                "b692cf0b643dbdf1be9bc5006830b3fe", // Round 2
                "b6ff744ed2c2c9bf6c590cbf0469bf41", // Round 3
                "47f7f7bc95353e03f96c32bcfd058dfd", // Round 4
                "3caaa3e8a99f9deb50f3af57adf622aa", // Round 5
                "5e390f7df7a69296a7553dc10aa31f6b", // Round 6
                "14f9701ae35fe28c440adf4d4ea9c026", // Round 7
                "47438735a41c65b9e016baf4aebf7ad2", // Round 8
                "549932d1f08557681093ed9cbe2c974e", // Round 9
                "13111d7fe3944a17f307a78b4d2b30c5"  // Round 10
            ];
            
            let roundKeysHTML = '';
            for (let i = 0; i < roundKeys.length; i++) {
                roundKeysHTML += `<p>Round ${i}: ${roundKeys[i]}</p>`;
            }
            
            document.getElementById('round-keys').innerHTML = roundKeysHTML;
        });
    }
    
    // Practice Tab - Round Function Visualization
    const processRoundButton = document.getElementById('process-round');
    if (processRoundButton) {
        processRoundButton.addEventListener('click', function() {
            // In a real implementation, this would perform the actual AES operations
            // For this demo, we're using pre-calculated values for visualization
            
            // Update the visualization with pre-calculated values
            // These would normally be calculated based on the input state and round key
            
            // No changes needed for initial state as it's hardcoded in the HTML
            
            // SubBytes output would be calculated
            const subBytesOutput = [
                "63", "1a", "cd", "b4",
                "82", "f3", "ee", "8a",
                "93", "33", "ac", "6f",
                "c7", "5b", "ea", "16"
            ];
            updateMatrix('subbytes-output', subBytesOutput);
            
            // ShiftRows output would be calculated
            const shiftRowsOutput = [
                "63", "1a", "cd", "b4",
                "f3", "ee", "8a", "82",
                "ac", "6f", "93", "33",
                "16", "c7", "5b", "ea"
            ];
            updateMatrix('shiftrows-output', shiftRowsOutput);
            
            // MixColumns output would be calculated
            const mixColumnsOutput = [
                "ba", "84", "e8", "1b",
                "75", "a4", "8d", "40",
                "f4", "8d", "06", "7d",
                "7a", "32", "0e", "5d"
            ];
            updateMatrix('mixcolumns-output', mixColumnsOutput);
            
            // AddRoundKey output would be calculated
            const addRoundKeyOutput = [
                "ba", "80", "e0", "17",
                "74", "a1", "85", "4c",
                "f6", "88", "0c", "71",
                "77", "3f", "04", "53"
            ];
            updateMatrix('addroundkey-output', addRoundKeyOutput);
        });
    }
    
    // Helper function to update a matrix visualization
    function updateMatrix(id, values) {
        const matrix = document.getElementById(id);
        if (matrix) {
            const cells = matrix.children;
            for (let i = 0; i < Math.min(cells.length, values.length); i++) {
                cells[i].textContent = values[i];
            }
        }
    }
    
    // Application Tab - Encryption/Decryption Tool
    const encryptButton = document.getElementById('encrypt-button');
    const decryptButton = document.getElementById('decrypt-button');
    
    if (encryptButton) {
        encryptButton.addEventListener('click', function() {
            const plaintext = document.getElementById('plaintext').value;
            const key = document.getElementById('aes-key').value;
            const iv = document.getElementById('aes-iv').value;
            const mode = document.getElementById('aes-mode').value;
            
            // In a real implementation, this would perform actual AES encryption
            // For this demo, we're just showing a simulated ciphertext
            const ciphertext = simulateEncryption(plaintext, key, iv, mode);
            document.getElementById('ciphertext').value = ciphertext;
        });
    }
    
    if (decryptButton) {
        decryptButton.addEventListener('click', function() {
            const ciphertext = document.getElementById('ciphertext').value;
            const key = document.getElementById('aes-key').value;
            const iv = document.getElementById('aes-iv').value;
            const mode = document.getElementById('aes-mode').value;
            
            // In a real implementation, this would perform actual AES decryption
            // For this demo, we're just showing the original plaintext
            const plaintext = simulateDecryption(ciphertext, key, iv, mode);
            document.getElementById('plaintext').value = plaintext;
        });
    }
    
    // Simulate AES encryption (for demo purposes only)
    function simulateEncryption(plaintext, key, iv, mode) {
        // This is a simplified simulation for educational purposes
        // In a real implementation, this would use a proper AES library
        
        // Convert plaintext to a hex representation for display
        let result = '';
        for (let i = 0; i < plaintext.length; i++) {
            result += plaintext.charCodeAt(i).toString(16).padStart(2, '0');
        }
        
        // Add some randomness to make each encryption look different
        const randomSuffix = Math.floor(Math.random() * 1000000).toString(16).padStart(6, '0');
        return result + randomSuffix;
    }
    
    // Simulate AES decryption (for demo purposes only)
    function simulateDecryption(ciphertext, key, iv, mode) {
        // This is a simplified simulation for educational purposes
        // In a real implementation, this would use a proper AES library
        
        // For the demo, we'll just return a fixed message
        return "This is a secret message that needs to be encrypted securely.";
    }
    
    // Application Tab - Mode Comparison
    const compareModes = document.getElementById('compare-modes');
    if (compareModes) {
        compareModes.addEventListener('click', function() {
            // In a real implementation, this would show actual encryption results
            // For this demo, we're just updating the visualizations
            
            // ECB visualization - identical blocks encrypt to identical ciphertext
            const ecbVisualization = document.getElementById('ecb-visualization');
            if (ecbVisualization) {
                ecbVisualization.innerHTML = `
                    <div class="block identical">Block 1 (A...A)</div>
                    <div class="block different">Block 2 (B...B)</div>
                    <div class="block identical">Block 3 (A...A)</div>
                    <div class="block different">Block 4 (B...B)</div>
                `;
            }
            
            // CBC visualization - all blocks are different
            const cbcVisualization = document.getElementById('cbc-visualization');
            if (cbcVisualization) {
                cbcVisualization.innerHTML = `
                    <div class="block unique">Block 1 (A...A)</div>
                    <div class="block unique">Block 2 (B...B)</div>
                    <div class="block unique">Block 3 (A...A)</div>
                    <div class="block unique">Block 4 (B...B)</div>
                `;
            }
            
            // CTR visualization - all blocks are different
            const ctrVisualization = document.getElementById('ctr-visualization');
            if (ctrVisualization) {
                ctrVisualization.innerHTML = `
                    <div class="block unique">Block 1 (A...A)</div>
                    <div class="block unique">Block 2 (B...B)</div>
                    <div class="block unique">Block 3 (A...A)</div>
                    <div class="block unique">Block 4 (B...B)</div>
                `;
            }
        });
    }
    
    // Challenge Tab - Padding Oracle
    const checkPadding = document.getElementById('check-padding');
    if (checkPadding) {
        checkPadding.addEventListener('click', function() {
            const ciphertext = document.getElementById('challenge1-ciphertext').value;
            
            // In a real implementation, this would send the ciphertext to a server
            // For this demo, we're simulating server responses
            const response = simulatePaddingOracleResponse(ciphertext);
            document.getElementById('padding-response').innerHTML = `<p>${response}</p>`;
        });
    }
    
    // Simulate padding oracle responses
    function simulatePaddingOracleResponse(ciphertext) {
        // This is a simplified simulation for educational purposes
        // In a real implementation, this would check actual padding
        
        // For the demo, we'll randomly return valid or invalid
        // with a bias toward invalid (more realistic)
        const random = Math.random();
        if (random < 0.2) {
            return "Valid padding";
        } else {
            return "Invalid padding";
        }
    }
    
    // Challenge Tab - ECB Oracle
    const encryptInput = document.getElementById('encrypt-input');
    if (encryptInput) {
        encryptInput.addEventListener('click', function() {
            const input = document.getElementById('challenge2-input').value;
            
            // In a real implementation, this would perform actual encryption
            // For this demo, we're simulating oracle responses
            const response = simulateECBOracleResponse(input);
            document.getElementById('oracle-response').innerHTML = `<p>${response}</p>`;
        });
    }
    
    // Simulate ECB oracle responses
    function simulateECBOracleResponse(input) {
        // This is a simplified simulation for educational purposes
        // In a real implementation, this would perform actual AES-ECB encryption
        
        // For the demo, we'll generate a random-looking hex string
        // with some structure to simulate ECB patterns
        let result = '';
        const secretPrefix = "supersecretvalue"; // This is what the attacker is trying to discover
        
        // Prepend the secret to the input (as the oracle would)
        const fullInput = secretPrefix + input;
        
        // Generate blocks of 16 bytes (32 hex chars)
        for (let i = 0; i < fullInput.length; i += 16) {
            const block = fullInput.substring(i, i + 16);
            
            // If this is a block of all the same character, simulate ECB's pattern-preserving property
            if (block.length === 16 && new Set(block.split('')).size === 1) {
                result += "d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4d4";
            } else {
                // Otherwise generate a random-looking block
                for (let j = 0; j < 32; j++) {
                    result += "0123456789abcdef"[Math.floor(Math.random() * 16)];
                }
            }
            
            result += " ";
        }
        
        return result.trim();
    }
    
    // Challenge Tab - Authenticated Encryption
    const protectMessage = document.getElementById('protect-message');
    const tamperButton = document.getElementById('tamper-button');
    const verifyButton = document.getElementById('verify-button');
    
    if (protectMessage) {
        protectMessage.addEventListener('click', function() {
            const message = document.getElementById('auth-message').value;
            const key = document.getElementById('auth-key').value;
            const mode = document.getElementById('auth-mode').value;
            
            // In a real implementation, this would perform actual authenticated encryption
            // For this demo, we're simulating the output
            const protectedOutput = simulateAuthenticatedEncryption(message, key, mode);
            document.getElementById('protected-output').innerHTML = `<p>${protectedOutput}</p>`;
            
            // Enable the tamper button
            tamperButton.disabled = false;
        });
    }
    
    if (tamperButton) {
        tamperButton.addEventListener('click', function() {
            const protectedOutput = document.getElementById('protected-output').textContent;
            
            // Simulate tampering by changing a character in the middle
            const tamperedOutput = simulateTampering(protectedOutput);
            
            document.getElementById('tampered-output').innerHTML = `<p>${tamperedOutput}</p>`;
            document.getElementById('tampered-output').classList.remove('hidden');
        });
    }
    
    if (verifyButton) {
        verifyButton.addEventListener('click', function() {
            const tamperedOutput = document.getElementById('tampered-output');
            const protectedOutput = document.getElementById('protected-output').textContent;
            
            // Check if we're verifying the original or tampered message
            const messageToVerify = !tamperedOutput.classList.contains('hidden') 
                ? tamperedOutput.textContent 
                : protectedOutput;
            
            // In a real implementation, this would perform actual verification
            // For this demo, we're simulating the result
            const verificationResult = simulateVerification(messageToVerify, tamperedOutput.classList.contains('hidden'));
            document.getElementById('verification-result').innerHTML = `<p>${verificationResult}</p>`;
        });
    }
    
    // Simulate authenticated encryption
    function simulateAuthenticatedEncryption(message, key, mode) {
        // This is a simplified simulation for educational purposes
        // In a real implementation, this would use a proper AES-GCM or HMAC library
        
        // Generate a random-looking ciphertext
        let ciphertext = '';
        for (let i = 0; i < message.length * 2; i++) {
            ciphertext += "0123456789abcdef"[Math.floor(Math.random() * 16)];
        }
        
        // Add an authentication tag
        const tag = "aabbccddeeff00112233445566778899";
        
        return `Ciphertext: ${ciphertext}\nAuth Tag: ${tag}`;
    }
    
    // Simulate tampering
    function simulateTampering(protectedOutput) {
        // Change a character in the middle of the ciphertext
        const parts = protectedOutput.split('\n');
        const ciphertext = parts[0].substring(12); // Remove "Ciphertext: "
        
        // Change a character in the middle
        const middleIndex = Math.floor(ciphertext.length / 2);
        const tamperedCiphertext = 
            ciphertext.substring(0, middleIndex) + 
            "ff" + 
            ciphertext.substring(middleIndex + 2);
        
        return `Ciphertext: ${tamperedCiphertext}\n${parts[1]}`;
    }
    
    // Simulate verification
    function simulateVerification(messageToVerify, isOriginal) {
        // For the demo, original messages pass verification, tampered ones fail
        if (isOriginal) {
            return "✅ Verification successful! Message is authentic and has not been tampered with.";
        } else {
            return "❌ Verification failed! Message has been tampered with or is corrupted.";
        }
    }
    
    // Show/hide solution buttons
    const showSolution1 = document.getElementById('show-solution1');
    const showSolution2 = document.getElementById('show-solution2');
    
    if (showSolution1) {
        showSolution1.addEventListener('click', function() {
            const solution = document.getElementById('solution1');
            solution.classList.toggle('hidden');
            showSolution1.textContent = solution.classList.contains('hidden') 
                ? 'Show Solution Approach' 
                : 'Hide Solution Approach';
        });
    }
    
    if (showSolution2) {
        showSolution2.addEventListener('click', function() {
            const solution = document.getElementById('solution2');
            solution.classList.toggle('hidden');
            showSolution2.textContent = solution.classList.contains('hidden') 
                ? 'Show Solution Approach' 
                : 'Hide Solution Approach';
        });
    }
});