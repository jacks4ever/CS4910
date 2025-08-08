# Asymmetric Lab - RSA Cryptography

This is an interactive lab for learning about RSA cryptography. The lab includes:
- Interactive HTML/CSS/JS interface for learning RSA concepts
- Python scripts demonstrating RSA encryption/decryption
- Practice problems and challenges

## Running with Docker

### Prerequisites
- Docker installed on your system
- Docker Compose (optional, but recommended)

### Option 1: Using Docker Compose (Recommended)

To start the lab server with a single command:

```bash
docker-compose up
```

This will build the Docker image if it doesn't exist and start the container.

### Option 2: Using Docker directly

Build the Docker image:

```bash
docker build -t asymmetric-lab .
```

Run the container:

```bash
docker run -p 12000:12000 asymmetric-lab
```

### Accessing the Lab

Once the container is running, open your web browser and navigate to:

```
http://localhost:12000
```

The interactive RSA lab will be available at this URL.

## Running Python Scripts

The lab includes several Python scripts demonstrating RSA concepts. To run these scripts inside the Docker container:

```bash
docker exec -it asymmetric_lab-asymmetric-lab-1 python script.py
```

Or to run them locally:

```bash
python script.py
```

## Contents

- `index.html` - Main lab interface
- `style.css` - Styling for the lab
- `app.js` - JavaScript for interactive elements
- `script.py` - Basic RSA implementation
- `script_1.py` - Extended RSA examples
- `script_2.py` - RSA challenge problems
- `rsa-crypto-lab.zip` - Additional resources