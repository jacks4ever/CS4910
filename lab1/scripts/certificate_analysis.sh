#!/bin/bash
# certificate_analysis.sh - Interactive SSL/TLS Certificate Analysis Tool

echo "=== CS4910 Lab 1 - Interactive Certificate Analysis ==="
echo "This tool will analyze SSL/TLS certificates for websites you specify."
echo

# Function to get user input for domain
get_domain() {
    while true; do
        echo "Enter the domain name to analyze (e.g., www.uccs.edu, google.com):" >&2
        read -r domain
        
        if [[ -z "$domain" ]]; then
            echo "Please enter a domain name." >&2
            continue
        fi
        
        # Remove protocol if user included it
        domain=$(echo "$domain" | sed 's|^https\?://||' | sed 's|/.*||')
        
        echo "You entered: $domain" >&2
        echo "Is this correct? (y/n)" >&2
        read -r confirm
        
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            echo "$domain"
            return
        fi
    done
}

# Function to get port (with default)
get_port() {
    echo "Enter the port number (default: 443 for HTTPS):" >&2
    read -r port
    
    if [[ -z "$port" ]]; then
        port="443"
    fi
    
    # Validate port number
    if ! [[ "$port" =~ ^[0-9]+$ ]] || [ "$port" -lt 1 ] || [ "$port" -gt 65535 ]; then
        echo "Invalid port number. Using default port 443." >&2
        port="443"
    fi
    
    echo "$port"
}

# Function to check if domain is reachable
check_connectivity() {
    local domain=$1
    local port=$2
    
    echo "Checking connectivity to $domain:$port..."
    
    if timeout 10 bash -c "</dev/tcp/$domain/$port" 2>/dev/null; then
        echo "✓ Successfully connected to $domain:$port"
        return 0
    else
        echo "✗ Failed to connect to $domain:$port"
        echo "This could be due to:"
        echo "  - Domain doesn't exist or is unreachable"
        echo "  - Port is not open or filtered"
        echo "  - Network connectivity issues"
        return 1
    fi
}

# Function to analyze certificate
analyze_certificate() {
    local domain=$1
    local port=$2
    
    echo
    echo "============================================================"
    echo "CERTIFICATE ANALYSIS FOR: $domain:$port"
    echo "============================================================"
    
    # Get certificate
    echo "Retrieving certificate..."
    CERT=$(openssl s_client -connect "$domain:$port" -servername "$domain" </dev/null 2>/dev/null | openssl x509)
    
    if [[ -z "$CERT" ]]; then
        echo "✗ Failed to retrieve certificate"
        return 1
    fi
    
    echo "✓ Certificate retrieved successfully"
    
    # Certificate fingerprints
    echo
    echo "=== CERTIFICATE FINGERPRINTS ==="
    echo "SHA-1 Fingerprint:"
    echo "$CERT" | openssl x509 -noout -fingerprint -sha1
    echo
    echo "SHA-256 Fingerprint:"
    echo "$CERT" | openssl x509 -noout -fingerprint -sha256
    
    # Certificate validity dates
    echo
    echo "=== CERTIFICATE VALIDITY ==="
    echo "$CERT" | openssl x509 -noout -dates
    
    # Calculate days until expiration
    expiry_date=$(echo "$CERT" | openssl x509 -noout -enddate | cut -d= -f2)
    expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null)
    current_epoch=$(date +%s)
    
    if [[ -n "$expiry_epoch" ]]; then
        days_until_expiry=$(( (expiry_epoch - current_epoch) / 86400 ))
        echo "Days until expiration: $days_until_expiry"
        
        if [ "$days_until_expiry" -lt 30 ]; then
            echo "⚠️  WARNING: Certificate expires in less than 30 days!"
        elif [ "$days_until_expiry" -lt 0 ]; then
            echo "🚨 CRITICAL: Certificate has expired!"
        fi
    fi
    
    # Certificate subject and issuer
    echo
    echo "=== CERTIFICATE IDENTITY ==="
    echo "Subject (who the certificate is issued to):"
    echo "$CERT" | openssl x509 -noout -subject
    echo
    echo "Issuer (Certificate Authority that issued it):"
    echo "$CERT" | openssl x509 -noout -issuer
    
    # Certificate details
    echo
    echo "=== CERTIFICATE TECHNICAL DETAILS ==="
    echo "Serial Number:"
    echo "$CERT" | openssl x509 -noout -serial
    echo
    echo "Signature Algorithm:"
    echo "$CERT" | openssl x509 -noout -text | grep "Signature Algorithm" | head -1
    echo
    echo "Public Key Algorithm and Size:"
    echo "$CERT" | openssl x509 -noout -text | grep -A1 "Public Key Algorithm"
    
    # Extract and display public key details (modulus and exponent for RSA)
    echo
    echo "=== PUBLIC KEY DETAILS ==="
    
    # Check if it's an RSA key
    key_type=$(echo "$CERT" | openssl x509 -noout -text | grep "Public Key Algorithm" | head -1)
    
    if echo "$key_type" | grep -q "rsaEncryption"; then
        echo "RSA Public Key Details:"
        
        # Extract modulus
        echo "Modulus (Hexadecimal):"
        hex_modulus=$(echo "$CERT" | openssl x509 -noout -modulus | sed 's/Modulus=//')
        echo "$hex_modulus"
        
        echo
        echo "Modulus (Decimal):"
        # Convert hex to decimal using Python (more reliable than bc for large numbers)
        if command -v python3 >/dev/null 2>&1; then
            decimal_modulus=$(echo "$hex_modulus" | python3 -c "import sys; print(int(sys.stdin.read().strip(), 16))")
            echo "$decimal_modulus"
            
            # Calculate and display the number of decimal digits
            digit_count=$(echo "$decimal_modulus" | wc -c)
            digit_count=$((digit_count - 1))  # Subtract 1 for newline
            echo
            echo "Modulus Length: $digit_count decimal digits"
            
        elif command -v python >/dev/null 2>&1; then
            decimal_modulus=$(echo "$hex_modulus" | python -c "import sys; print(int(sys.stdin.read().strip(), 16))")
            echo "$decimal_modulus"
            
            # Calculate and display the number of decimal digits
            digit_count=$(echo "$decimal_modulus" | wc -c)
            digit_count=$((digit_count - 1))  # Subtract 1 for newline
            echo
            echo "Modulus Length: $digit_count decimal digits"
            
        else
            echo "Python not available - cannot convert to decimal format"
            echo "Hex value: $hex_modulus"
        fi
        
        # Extract public exponent
        echo
        echo "Public Exponent:"
        exponent=$(echo "$CERT" | openssl x509 -noout -text | grep -A20 "RSA Public-Key" | grep "Exponent:" | sed 's/.*Exponent: //')
        if [[ -n "$exponent" ]]; then
            echo "$exponent"
        else
            # Alternative method to get exponent
            echo "$CERT" | openssl x509 -noout -text | grep -A30 "Public-Key:" | grep "Exponent:" | head -1 | sed 's/.*Exponent: //'
        fi
        
        # Also show the full public key in PEM format
        echo
        echo "Public Key (PEM format):"
        echo "$CERT" | openssl x509 -noout -pubkey
        
    elif echo "$key_type" | grep -q "id-ecPublicKey"; then
        echo "Elliptic Curve Public Key Details:"
        
        # For EC keys, show the curve and public key
        echo "Curve Information:"
        echo "$CERT" | openssl x509 -noout -text | grep -A5 "Public-Key:" | grep -E "(Public-Key|ASN1 OID|NIST CURVE)"
        
        echo
        echo "Public Key (PEM format):"
        echo "$CERT" | openssl x509 -noout -pubkey
        
        echo
        echo "Public Key (hex format):"
        echo "$CERT" | openssl x509 -noout -text | grep -A10 "pub:" | grep -E "^\s*[0-9a-f]{2}:" | sed 's/^\s*//'
        
    else
        echo "Public Key Type: $(echo "$key_type" | sed 's/.*Algorithm: //')"
        echo "Public Key (PEM format):"
        echo "$CERT" | openssl x509 -noout -pubkey
    fi
    
    # Subject Alternative Names (SAN)
    echo
    echo "=== SUBJECT ALTERNATIVE NAMES ==="
    san=$(echo "$CERT" | openssl x509 -noout -text | grep -A1 "Subject Alternative Name" | tail -1)
    if [[ -n "$san" ]]; then
        echo "$san"
    else
        echo "No Subject Alternative Names found"
    fi
    
    # Certificate chain analysis
    echo
    echo "=== CERTIFICATE CHAIN ANALYSIS ==="
    echo "Analyzing certificate chain..."
    
    chain_info=$(openssl s_client -connect "$domain:$port" -servername "$domain" -showcerts </dev/null 2>/dev/null | grep -E "(subject=|issuer=)")
    
    if [[ -n "$chain_info" ]]; then
        echo "$chain_info"
    else
        echo "Unable to retrieve certificate chain information"
    fi
    
    # SSL/TLS connection details
    echo
    echo "=== SSL/TLS CONNECTION DETAILS ==="
    connection_info=$(openssl s_client -connect "$domain:$port" -servername "$domain" </dev/null 2>&1 | grep -E "(Protocol|Cipher|Server public key)")
    
    if [[ -n "$connection_info" ]]; then
        echo "$connection_info"
    else
        echo "Unable to retrieve connection details"
    fi
}

# Function to save results
save_results() {
    local domain=$1
    local port=$2
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local filename="certificate_analysis_${domain}_${timestamp}.txt"
    
    echo
    echo "Would you like to save the analysis results to a file? (y/n)"
    read -r save_choice
    
    if [[ "$save_choice" =~ ^[Yy]$ ]]; then
        # Create outputs directory if it doesn't exist
        mkdir -p ../outputs/certificate
        
        # Re-run analysis and save to file
        {
            echo "================================================================================"
            echo "CS4910 Lab 1 - Certificate Analysis Report"
            echo "================================================================================"
            echo "Analysis Date: $(date '+%B %d, %Y at %I:%M %p')"
            echo "Target Domain: $domain:$port"
            echo ""
            analyze_certificate "$domain" "$port"
            echo ""
            echo "================================================================================"
            echo "End of Certificate Analysis Report"
            echo "================================================================================"
        } > "../outputs/certificate/$filename" 2>&1
        
        echo "✓ Results saved to ../outputs/certificate/$filename"
        echo "You can copy and paste this content directly into your Word document."
    fi
}

# Main execution
main() {
    echo "This tool will help you analyze SSL/TLS certificates."
    echo "You can analyze any HTTPS website's certificate."
    echo
    
    while true; do
        # Get domain from user
        domain=$(get_domain)
        
        # Get port from user
        port=$(get_port)
        
        echo
        echo "Analyzing certificate for: $domain:$port"
        echo
        
        # Check connectivity
        if check_connectivity "$domain" "$port"; then
            # Analyze certificate
            analyze_certificate "$domain" "$port"
            
            # Offer to save results
            save_results "$domain" "$port"
        else
            echo "Cannot proceed with certificate analysis due to connectivity issues."
        fi
        
        echo
        echo "============================================================"
        echo "Would you like to analyze another certificate? (y/n)"
        read -r continue_choice
        
        if [[ ! "$continue_choice" =~ ^[Yy]$ ]]; then
            break
        fi
        
        echo
    done
    
    echo
    echo "Certificate analysis complete!"
    echo "Your results are ready for your lab report."
    echo "If you saved the results, you can copy and paste them directly into your Word document."
    
    # AI-Enhanced Learning Suggestions
    echo
    echo "======================================================================"
    echo "🤖 AI-ENHANCED LEARNING SUGGESTIONS"
    echo "======================================================================"
    echo "Use AI to deepen your PKI and certificate understanding with these prompts:"
    echo
    echo "1. PKI FUNDAMENTALS:"
    echo '   "Explain Public Key Infrastructure (PKI) using simple analogies"'
    echo '   "How does certificate-based authentication work step by step?"'
    echo
    echo "2. CERTIFICATE DETAILS:"
    echo '   "What is the purpose of each field in an X.509 certificate?"'
    echo '   "Explain the difference between self-signed and CA-signed certificates"'
    echo
    echo "3. TRUST AND VALIDATION:"
    echo '   "How does a browser validate a certificate chain?"'
    echo '   "What happens when a certificate expires or is revoked?"'
    echo
    echo "4. SECURITY IMPLICATIONS:"
    echo '   "What are the security risks of certificate pinning?"'
    echo '   "How do certificate transparency logs improve security?"'
    echo
    echo "5. PRACTICAL APPLICATIONS:"
    echo '   "Where else besides HTTPS are certificates used?"'
    echo '   "How do certificate authorities prevent fraudulent certificates?"'
    echo
    echo "6. VERIFICATION:"
    echo '   "Review my certificate analysis: [paste results]. What additional"'
    echo '   "security considerations or insights should I explore?"'
    echo
    echo "💡 Remember: Use AI to enhance understanding, not replace analysis!"
    echo "   Document all AI interactions in your lab report."
    echo "======================================================================"
}

# Run main function
main