# Symmetric Lab - AES Cryptography

This is an interactive lab for learning about AES (Advanced Encryption Standard) cryptography. The lab includes:
- Interactive HTML/CSS/JS interface for learning AES concepts
- Visualizations of AES operations and modes
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
docker build -t symmetric-lab .
```

Run the container:

```bash
docker run -p 12000:12000 symmetric-lab
```

### Accessing the Lab

Once the server is running, open your web browser and navigate to:

```
http://localhost:12000
```

The interactive AES lab will be available at this URL.

## Lab Content

The lab is divided into four main sections:

### 1. Theory
- Overview of AES encryption algorithm
- Key concepts and terminology
- AES round operations (SubBytes, ShiftRows, MixColumns, AddRoundKey)
- Different modes of operation (ECB, CBC, CTR, GCM)

### 2. Practice
- Key expansion exercise
- AES round function visualization
- Step-by-step walkthrough of the encryption process

### 3. Application
- Interactive encryption/decryption tool
- Comparison of different AES modes
- Practical examples of AES usage

### 4. Challenge
- Padding oracle attack simulation
- Known-plaintext attack on ECB mode
- Authenticated encryption implementation

## Educational Purpose

This lab is designed for educational purposes only. The implementations and examples are simplified for learning and should not be used in production systems.

## Contents

- `index.html` - Main lab interface
- `style.css` - Styling for the lab
- `app.js` - JavaScript for interactive elements
- `uccs-logo.svg` - UCCS logo for branding
- `start-lab.sh` - Script to start the lab server