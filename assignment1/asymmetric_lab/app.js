// RSA Cryptography Lab - Interactive JavaScript Implementation
// Educational purposes only - not for production use

document.addEventListener('DOMContentLoaded', function() {
    console.log('RSA Lab script loaded...');
    console.log('DOMContentLoaded event fired!');

    // Tab navigation
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    console.log('Found', tabButtons.length, 'tab buttons');
    console.log('Found', tabContents.length, 'tab contents');
    
    tabButtons.forEach(button => {
        console.log('Adding event listener to button:', button.getAttribute('data-tab'));
        button.addEventListener('click', () => {
            console.log('Button clicked:', button.getAttribute('data-tab'));
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabContents.forEach(content => content.classList.remove('active'));
            
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
            console.log('Activated tab:', tabId);
        });
    });

    // RSA Theory Tab - Variable definitions validation
    const variableSelects = document.querySelectorAll('#theory select');
    variableSelects.forEach(select => {
        select.addEventListener('change', function() {
            const variable = this.parentElement.querySelector('label').textContent;
            const selectedValue = this.value;
            const feedback = this.parentElement.querySelector('.feedback');
            
            // Define correct answers
            const correctAnswers = {
                'p': 'First prime number (kept secret)',
                'q': 'Second prime number (kept secret)',
                'n': 'Public modulus (n = p × q)',
                'φ(n)': "Euler's totient function φ(n) = (p-1)(q-1)",
                'e': 'Public encryption exponent (coprime to φ(n))',
                'd': 'Private decryption exponent (modular inverse of e)',
                'M': 'Original message (plaintext)',
                'C': 'Encrypted message (ciphertext)'
            };
            
            if (selectedValue === correctAnswers[variable]) {
                feedback.textContent = '✓ Correct!';
                feedback.className = 'feedback correct';
            } else if (selectedValue !== 'Select definition...') {
                feedback.textContent = '✗ Try again';
                feedback.className = 'feedback incorrect';
            } else {
                feedback.textContent = '';
                feedback.className = 'feedback';
            }
        });
    });

    // RSA Key Generation Practice
    const keyGenInputs = document.querySelectorAll('#theory input[type="number"]');
    keyGenInputs.forEach(input => {
        input.addEventListener('input', function() {
            const step = this.getAttribute('data-step');
            const value = parseInt(this.value);
            const feedback = this.parentElement.querySelector('.step-feedback');
            
            let correct = false;
            switch(step) {
                case 'n':
                    correct = (value === 77); // 7 * 11
                    break;
                case 'phi':
                    correct = (value === 60); // (7-1) * (11-1)
                    break;
                case 'e':
                    correct = (value === 7); // Common choice, coprime to 60
                    break;
                case 'd':
                    correct = (value === 43); // Modular inverse of 7 mod 60
                    break;
            }
            
            if (correct) {
                feedback.textContent = '✓ Correct!';
                feedback.className = 'step-feedback correct';
            } else if (value) {
                feedback.textContent = '✗ Try again';
                feedback.className = 'step-feedback incorrect';
            } else {
                feedback.textContent = '';
                feedback.className = 'step-feedback';
            }
        });
    });

    // Modular Arithmetic Practice
    function generateModularProblem() {
        const base = Math.floor(Math.random() * 20) + 2;
        const exponent = Math.floor(Math.random() * 10) + 2;
        const modulus = Math.floor(Math.random() * 20) + 5;
        
        const result = Math.pow(base, exponent) % modulus;
        
        document.getElementById('mod-base').textContent = base;
        document.getElementById('mod-exp').textContent = exponent;
        document.getElementById('mod-mod').textContent = modulus;
        document.getElementById('mod-answer').value = '';
        document.getElementById('mod-feedback').textContent = '';
        
        // Store correct answer
        document.getElementById('mod-answer').setAttribute('data-correct', result);
    }

    // Initialize modular arithmetic practice
    if (document.getElementById('generate-mod-problem')) {
        document.getElementById('generate-mod-problem').addEventListener('click', generateModularProblem);
        document.getElementById('check-mod-answer').addEventListener('click', function() {
            const userAnswer = parseInt(document.getElementById('mod-answer').value);
            const correctAnswer = parseInt(document.getElementById('mod-answer').getAttribute('data-correct'));
            const feedback = document.getElementById('mod-feedback');
            
            if (userAnswer === correctAnswer) {
                feedback.textContent = '✓ Correct! Well done.';
                feedback.className = 'feedback correct';
            } else {
                feedback.textContent = `✗ Incorrect. The answer is ${correctAnswer}`;
                feedback.className = 'feedback incorrect';
            }
        });
        
        // Generate initial problem
        generateModularProblem();
    }

    // RSA Encryption/Decryption Application
    function performRSAOperation(operation) {
        const message = parseInt(document.getElementById('rsa-message').value);
        const key = parseInt(document.getElementById('rsa-key').value);
        const modulus = parseInt(document.getElementById('rsa-modulus').value);
        
        if (!message || !key || !modulus) {
            document.getElementById('rsa-result').textContent = 'Please fill in all fields';
            return;
        }
        
        const result = modPow(message, key, modulus);
        document.getElementById('rsa-result').textContent = `Result: ${result}`;
    }

    // Modular exponentiation function
    function modPow(base, exponent, modulus) {
        let result = 1;
        base = base % modulus;
        while (exponent > 0) {
            if (exponent % 2 === 1) {
                result = (result * base) % modulus;
            }
            exponent = Math.floor(exponent / 2);
            base = (base * base) % modulus;
        }
        return result;
    }

    // RSA Application buttons
    if (document.getElementById('encrypt-btn')) {
        document.getElementById('encrypt-btn').addEventListener('click', () => performRSAOperation('encrypt'));
    }
    if (document.getElementById('decrypt-btn')) {
        document.getElementById('decrypt-btn').addEventListener('click', () => performRSAOperation('decrypt'));
    }

    // Challenge Tab - CIA Decryption
    let challengeAttempts = 0;
    const maxAttempts = 3;
    
    if (document.getElementById('submit-flag')) {
        document.getElementById('submit-flag').addEventListener('click', function() {
            const userFlag = document.getElementById('flag-input').value.trim();
            const correctFlag = 'FLAG{RSA_CRACKED}';
            const feedback = document.getElementById('challenge-feedback');
            
            challengeAttempts++;
            
            if (userFlag === correctFlag) {
                feedback.innerHTML = `
                    <div class="success">
                        🎉 <strong>MISSION ACCOMPLISHED!</strong><br>
                        You've successfully cracked the RSA encryption!<br>
                        The intercepted message has been decoded.
                    </div>
                `;
                document.getElementById('flag-input').disabled = true;
                this.disabled = true;
            } else {
                const remaining = maxAttempts - challengeAttempts;
                if (remaining > 0) {
                    feedback.innerHTML = `
                        <div class="error">
                            ❌ Incorrect flag. ${remaining} attempts remaining.<br>
                            <em>Hint: Use the factorization n = p × q to find the private key</em>
                        </div>
                    `;
                } else {
                    feedback.innerHTML = `
                        <div class="error">
                            🚫 <strong>MISSION FAILED</strong><br>
                            Maximum attempts exceeded. The correct flag was: <code>${correctFlag}</code><br>
                            <em>Study the RSA algorithm and try again!</em>
                        </div>
                    `;
                    document.getElementById('flag-input').disabled = true;
                    this.disabled = true;
                }
            }
        });
    }

    console.log('RSA Lab initialization complete');
});