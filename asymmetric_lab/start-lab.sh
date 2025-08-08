#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if command -v docker-compose &> /dev/null; then
    echo "Starting Asymmetric Lab using Docker Compose..."
    docker-compose up -d
    echo "Asymmetric Lab is now running at http://localhost:12000"
else
    echo "Docker Compose not found. Using Docker directly..."
    
    # Build the Docker image
    echo "Building Docker image..."
    docker build -t asymmetric-lab .
    
    # Run the container
    echo "Starting container..."
    docker run -d -p 12000:12000 --name asymmetric-lab-container asymmetric-lab
    
    echo "Asymmetric Lab is now running at http://localhost:12000"
fi