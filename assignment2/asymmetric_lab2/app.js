// RSA Lab Application Logic
class RSALab {
    constructor() {
        this.currentTab = 'theory';
        this.practiceProgress = 0;
        this.challengeProgress = 0;
        this.init();
    }

    init() {
        // Add a small delay to ensure DOM is fully loaded
        setTimeout(() => {
            this.setupTabSwitching();
            this.setupAIPrompts();
            this.setupTheoryTab();
            this.setupPracticeTab();
            this.setupApplicationTab();
            this.setupChallengeTab();
        }, 100);
    }

    // Tab Switching
    setupTabSwitching() {
        const tabButtons = document.querySelectorAll('.tab-button');
        const tabContents = document.querySelectorAll('.tab-content');



        tabButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const targetTab = button.getAttribute('data-tab');
                
                // Remove active class from all tabs and contents
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));
                
                // Add active class to clicked tab and corresponding content
                button.classList.add('active');
                const targetContent = document.getElementById(targetTab);
                if (targetContent) {
                    targetContent.classList.add('active');
                }
                
                this.currentTab = targetTab;
                
                // Initialize tab-specific functionality when tab becomes active
                if (targetTab === 'practice') {
                    this.initializePracticeTab();
                }
            });
        });
    }

    // AI Prompts Toggle
    setupAIPrompts() {
        const toggles = document.querySelectorAll('.ai-prompt-toggle');
        toggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                const content = toggle.nextElementSibling;
                if (content) {
                    content.classList.toggle('hidden');
                }
            });
        });
    }

    // Theory Tab Setup
    setupTheoryTab() {
        // Variable definition validation
        const definitionSelects = document.querySelectorAll('.definition-select');
        console.log('Found', definitionSelects.length, 'definition selects');
        
        definitionSelects.forEach(select => {
            select.addEventListener('change', (e) => {
                this.validateDefinition(select);
            });
            
            // Also validate on input for immediate feedback
            select.addEventListener('input', (e) => {
                this.validateDefinition(select);
            });
        });

        // Fill-in-the-blank validation
        const fillBlanks = document.querySelectorAll('.fill-blank');
        fillBlanks.forEach(input => {
            input.addEventListener('input', (e) => {
                this.validateFillBlank(input);
            });
            
            input.addEventListener('blur', (e) => {
                this.validateFillBlank(input);
            });
        });
    }

    validateDefinition(select) {
        const correctAnswer = select.getAttribute('data-correct');
        const selectedValue = select.value;
        const feedback = select.parentElement.querySelector('.feedback');
        
        console.log('Validating definition:', selectedValue, 'vs', correctAnswer);
        
        if (selectedValue === correctAnswer) {
            select.classList.remove('incorrect');
            select.classList.add('correct');
            if (feedback) {
                feedback.textContent = 'Correct! ✓';
                feedback.classList.remove('incorrect');
                feedback.classList.add('correct');
            }
        } else if (selectedValue !== '' && selectedValue !== null) {
            select.classList.remove('correct');
            select.classList.add('incorrect');
            if (feedback) {
                const variable = select.closest('.variable-card')?.getAttribute('data-variable') || 'unknown';
                feedback.textContent = 'Try again - ' + this.getHintForVariable(variable);
                feedback.classList.remove('correct');
                feedback.classList.add('incorrect');
            }
        } else {
            select.classList.remove('correct', 'incorrect');
            if (feedback) {
                feedback.textContent = '';
                feedback.classList.remove('correct', 'incorrect');
            }
        }
    }

    getHintForVariable(variable) {
        const hints = {
            'p': 'This is the first secret prime number used in RSA',
            'q': 'This is the second secret prime number used in RSA',  
            'n': 'This is calculated by multiplying p and q',
            'phi': 'This function counts integers less than n that are coprime to n',
            'e': 'This is chosen to be coprime with φ(n) and is used for encryption',
            'd': 'This is calculated as the multiplicative inverse of e modulo φ(n)',
            'M': 'This represents the original, unencrypted data',
            'C': 'This represents the encrypted data after applying RSA'
        };
        return hints[variable] || 'Check the definitions carefully';
    }

    validateFillBlank(input) {
        const correctAnswer = parseInt(input.getAttribute('data-correct'));
        const userAnswer = parseInt(input.value);
        const feedback = input.parentElement.querySelector('.feedback');
        
        if (!isNaN(userAnswer) && userAnswer === correctAnswer) {
            input.classList.remove('incorrect');
            input.classList.add('correct');
            if (feedback) {
                feedback.textContent = 'Correct! ✓';
                feedback.classList.remove('incorrect');
                feedback.classList.add('correct');
            }
        } else if (input.value !== '' && input.value !== null) {
            input.classList.remove('correct');
            input.classList.add('incorrect');
            if (feedback) {
                feedback.textContent = 'Try again';
                feedback.classList.remove('correct');
                feedback.classList.add('incorrect');
            }
        } else {
            input.classList.remove('correct', 'incorrect');
            if (feedback) {
                feedback.textContent = '';
                feedback.classList.remove('correct', 'incorrect');
            }
        }
    }

    // Practice Tab Setup
    setupPracticeTab() {
        const answerInputs = document.querySelectorAll('.answer-input');
        answerInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                this.validatePracticeAnswer(input);
            });
            
            input.addEventListener('blur', (e) => {
                this.validatePracticeAnswer(input);
            });
        });


    }

    initializePracticeTab() {
        const showStepsButtons = document.querySelectorAll('.show-steps');
        console.log('Initializing Practice tab - Found', showStepsButtons.length, 'show steps buttons');
        showStepsButtons.forEach(button => {
            // Remove any existing event listeners to avoid duplicates
            button.replaceWith(button.cloneNode(true));
        });
        
        // Re-query after cloning to get fresh elements
        const freshShowStepsButtons = document.querySelectorAll('.show-steps');
        freshShowStepsButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Show steps button clicked');
                const stepsContent = button.nextElementSibling;
                console.log('Steps content:', stepsContent);
                if (stepsContent) {
                    stepsContent.classList.toggle('hidden');
                    button.textContent = stepsContent.classList.contains('hidden') ? 'Show Steps' : 'Hide Steps';
                    console.log('Toggled steps, now hidden:', stepsContent.classList.contains('hidden'));
                } else {
                    console.log('No steps content found');
                }
            });
        });
    }

    validatePracticeAnswer(input) {
        const correctAnswer = parseInt(input.getAttribute('data-correct'));
        const userAnswer = parseInt(input.value);
        const feedback = input.parentElement.querySelector('.problem-feedback');
        const hint = input.getAttribute('data-hint');
        
        if (!isNaN(userAnswer) && userAnswer === correctAnswer) {
            input.classList.remove('incorrect');
            input.classList.add('correct');
            if (feedback) {
                feedback.textContent = 'Excellent! ✓';
                feedback.classList.remove('incorrect');
                feedback.classList.add('correct');
            }
            
            if (!input.hasAttribute('data-solved')) {
                input.setAttribute('data-solved', 'true');
                this.practiceProgress++;
                this.updatePracticeProgress();
            }
        } else if (input.value !== '' && input.value !== null) {
            input.classList.remove('correct');
            input.classList.add('incorrect');
            if (feedback) {
                feedback.textContent = 'Try again - ' + (hint || 'Check your calculation');
                feedback.classList.remove('correct');
                feedback.classList.add('incorrect');
            }
        } else {
            input.classList.remove('correct', 'incorrect');
            if (feedback) {
                feedback.textContent = '';
                feedback.classList.remove('correct', 'incorrect');
            }
        }
    }

    updatePracticeProgress() {
        const progressFill = document.querySelector('#practice .progress-fill');
        const progressText = document.querySelector('#practice .progress-text');
        const percentage = (this.practiceProgress / 5) * 100;
        
        if (progressFill) {
            progressFill.style.width = percentage + '%';
        }
        if (progressText) {
            progressText.textContent = `${this.practiceProgress}/5 Problems Completed`;
        }
    }

    // Application Tab Setup
    setupApplicationTab() {
        const convertButton = document.getElementById('convert-message');
        const plaintextInput = document.getElementById('plaintext-input');
        
        if (convertButton) {
            convertButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.convertMessage();
            });
        }
        
        if (plaintextInput) {
            plaintextInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.convertMessage();
                }
            });
            
            // Only allow A-Z letters and spaces
            plaintextInput.addEventListener('input', (e) => {
                e.target.value = e.target.value.toUpperCase().replace(/[^A-Z\s]/g, '');
            });
        }
    }

    convertMessage() {
        const plaintextInput = document.getElementById('plaintext-input');
        if (!plaintextInput) return;
        
        const message = plaintextInput.value.trim().replace(/\s/g, '');
        
        if (message === '') {
            alert('Please enter a message');
            return;
        }
        
        if (message.length > 10) {
            alert('Please limit message to 10 characters for this demo');
            return;
        }
        
        this.showASCIIConversion(message);
        this.setupEncryptionSteps(message);
    }

    showASCIIConversion(message) {
        const conversionDiv = document.getElementById('ascii-conversion');
        const lettersDisplay = document.getElementById('letters-display');
        const numbersDisplay = document.getElementById('numbers-display');
        
        if (!conversionDiv || !lettersDisplay || !numbersDisplay) return;
        
        const letters = message.split('');
        const numbers = letters.map(letter => letter.charCodeAt(0) - 64); // A=1, B=2, etc.
        
        lettersDisplay.textContent = letters.join(' ');
        numbersDisplay.textContent = numbers.join(' ');
        
        conversionDiv.classList.remove('hidden');
    }

    setupEncryptionSteps(message) {
        const encryptionSteps = document.getElementById('encryption-steps');
        const calculationsDiv = document.getElementById('encryption-calculations');
        const finalCiphertext = document.getElementById('final-ciphertext');
        
        if (!encryptionSteps || !calculationsDiv || !finalCiphertext) return;
        
        calculationsDiv.innerHTML = '';
        
        const letters = message.split('');
        const numbers = letters.map(letter => letter.charCodeAt(0) - 64);
        const ciphertext = [];
        
        numbers.forEach((num, index) => {
            const calculationDiv = document.createElement('div');
            calculationDiv.className = 'encryption-calculation';
            
            // Calculate correct answer: num^7 mod 77
            const correctAnswer = this.modularExponentiation(num, 7, 77);
            ciphertext.push(correctAnswer);
            
            calculationDiv.innerHTML = `
                <span class="formula">${letters[index]} = ${num}: ${num}⁷ mod 77 = </span>
                <input type="number" class="calculation-input" data-correct="${correctAnswer}" placeholder="?">
                <div class="feedback"></div>
            `;
            
            calculationsDiv.appendChild(calculationDiv);
            
            const input = calculationDiv.querySelector('.calculation-input');
            if (input) {
                input.addEventListener('input', () => {
                    this.validateEncryptionCalculation(input);
                });
            }
        });
        
        encryptionSteps.classList.remove('hidden');
        this.showFinalCiphertext(ciphertext);
    }

    validateEncryptionCalculation(input) {
        const correctAnswer = parseInt(input.getAttribute('data-correct'));
        const userAnswer = parseInt(input.value);
        const feedback = input.parentElement.querySelector('.feedback');
        
        if (!isNaN(userAnswer) && userAnswer === correctAnswer) {
            input.classList.remove('incorrect');
            input.classList.add('correct');
            if (feedback) {
                feedback.textContent = 'Correct! ✓';
                feedback.classList.remove('incorrect');
                feedback.classList.add('correct');
            }
        } else if (input.value !== '' && input.value !== null) {
            input.classList.remove('correct');
            input.classList.add('incorrect');
            if (feedback) {
                feedback.textContent = 'Try again';
                feedback.classList.remove('correct');
                feedback.classList.add('incorrect');
            }
        } else {
            input.classList.remove('correct', 'incorrect');
            if (feedback) {
                feedback.textContent = '';
                feedback.classList.remove('correct', 'incorrect');
            }
        }
    }

    showFinalCiphertext(ciphertext) {
        const finalDiv = document.getElementById('final-ciphertext');
        const ciphertextDisplay = finalDiv?.querySelector('.ciphertext-display');
        
        if (finalDiv && ciphertextDisplay) {
            ciphertextDisplay.textContent = '[' + ciphertext.join(', ') + ']';
            finalDiv.classList.remove('hidden');
        }
    }

    modularExponentiation(base, exponent, modulus) {
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

    // Challenge Tab Setup
    setupChallengeTab() {
        const decryptInputs = document.querySelectorAll('.decrypt-input');
        decryptInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                this.validateDecryption(input);
            });
            
            input.addEventListener('blur', (e) => {
                this.validateDecryption(input);
            });
        });
    }

    validateDecryption(input) {
        const correctAnswer = parseInt(input.getAttribute('data-correct'));
        const userAnswer = parseInt(input.value);
        const feedback = input.parentElement.querySelector('.decrypt-feedback');
        const revealedLetter = input.parentElement.querySelector('.revealed-letter');
        
        if (!isNaN(userAnswer) && userAnswer === correctAnswer) {
            input.classList.remove('incorrect');
            input.classList.add('correct');
            if (feedback) {
                feedback.textContent = '✓';
                feedback.classList.remove('incorrect');
                feedback.classList.add('correct');
            }
            
            // Reveal the letter
            if (revealedLetter) {
                revealedLetter.classList.remove('hidden');
            }
            
            if (!input.hasAttribute('data-solved')) {
                input.setAttribute('data-solved', 'true');
                this.challengeProgress++;
                this.updateChallengeProgress();
            }
        } else if (input.value !== '' && input.value !== null) {
            input.classList.remove('correct');
            input.classList.add('incorrect');
            if (feedback) {
                feedback.textContent = '✗';
                feedback.classList.remove('correct');
                feedback.classList.add('incorrect');
            }
            if (revealedLetter) {
                revealedLetter.classList.add('hidden');
            }
        } else {
            input.classList.remove('correct', 'incorrect');
            if (feedback) {
                feedback.textContent = '';
                feedback.classList.remove('correct', 'incorrect');
            }
            if (revealedLetter) {
                revealedLetter.classList.add('hidden');
            }
        }
    }

    updateChallengeProgress() {
        const progressFill = document.querySelector('#challenge .progress-fill');
        const statusText = document.querySelector('.status-text');
        const percentage = (this.challengeProgress / 11) * 100;
        
        if (progressFill) {
            progressFill.style.width = percentage + '%';
        }
        if (statusText) {
            statusText.textContent = `Mission Progress: ${this.challengeProgress}/11 Numbers Decrypted`;
        }
        
        if (this.challengeProgress === 11) {
            setTimeout(() => {
                this.showMissionComplete();
            }, 500);
        }
    }

    showMissionComplete() {
        const missionComplete = document.getElementById('mission-complete');
        if (missionComplete) {
            missionComplete.classList.remove('hidden');
            
            // Scroll to the mission complete section
            missionComplete.scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Initialize the RSA Lab when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing RSA Lab...');
    new RSALab();
});

// Fallback initialization in case DOMContentLoaded already fired
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Fallback: DOM loaded, initializing RSA Lab...');
        new RSALab();
    });
} else {
    console.log('Document already loaded, initializing RSA Lab immediately...');
    new RSALab();
}