# Asymmetric Lab - RSA Cryptography

This is an interactive lab for learning about RSA (Rivest-Shamir-Adleman) cryptography. The lab includes:
- Interactive HTML/CSS/JS interface for learning RSA concepts
- Visualizations of RSA operations and key generation
- Practice exercises and challenges

## Running the Lab

### Option 1: Using the start-lab.sh Script (Recommended)

The easiest way to run the lab is using the provided start-lab.sh script:

```bash
# Make sure the script is executable
chmod +x start-lab.sh

# Run the script
./start-lab.sh
```

This script will:
1. Check if Python is installed
2. Start a local web server on port 12000
3. Open your default web browser to the lab interface

### Option 2: Running with Docker

#### Prerequisites
- Docker installed on your system
- Docker Compose (optional, but recommended)

#### Option 2A: Using Docker Compose

To start the lab server with Docker Compose:

```bash
docker-compose up
```

This will build the Docker image if it doesn't exist and start the container.

#### Option 2B: Using Docker directly

Build the Docker image:

```bash
docker build -t asymmetric-lab .
```

Run the container:

```bash
docker run -p 12000:12000 asymmetric-lab
```

### Accessing the Lab

Once the server is running, open your web browser and navigate to:

```
http://localhost:12000
```

The interactive RSA lab will be available at this URL.

## Lab Content

The lab is divided into four main sections:

### 1. Theory
- Overview of RSA encryption algorithm
- Key concepts and terminology
- Prime number generation and modular arithmetic
- Public and private key generation

### 2. Practice
- Key generation exercise
- Step-by-step walkthrough of the encryption/decryption process
- Modular exponentiation calculations

### 3. Application
- Interactive encryption/decryption tool
- Digital signature demonstration
- Practical examples of RSA usage

### 4. Challenge
- Breaking weak RSA implementations
- Timing attack simulation
- Implementing proper padding schemes

## Educational Purpose

This lab is designed for educational purposes only. The implementations and examples are simplified for learning and should not be used in production systems.

## Contents

- `index.html` - Main lab interface
- `style.css` - Styling for the lab
- `app.js` - JavaScript for interactive elements
- `script.py` - Main Python helper script for RSA operations
- `practice_problems.py` - Python script for generating practice problems
- `challenge_decryption.py` - Python script for the decryption challenge
- `uccs-logo.svg` - UCCS logo for branding
- `start-lab.sh` - Script to start the lab server