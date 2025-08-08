#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3 first."
    exit 1
fi

# Determine which Python command to use
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Starting AES Cryptography Lab server..."
echo "Press Ctrl+C to stop the server when you're done."

# Start the Python HTTP server
PORT=12000
$PYTHON_CMD -m http.server $PORT &
SERVER_PID=$!

# Wait a moment for the server to start
sleep 1

# Open the browser (platform-specific)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "http://localhost:$PORT" 2>/dev/null
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open "http://localhost:$PORT"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start "http://localhost:$PORT"
else
    echo "Please open your browser and navigate to: http://localhost:$PORT"
fi

echo "AES Cryptography Lab is now running at http://localhost:$PORT"
echo "Keep this terminal window open while using the lab."
echo "Press Ctrl+C to stop the server when you're done."

# Wait for user to press Ctrl+C
wait $SERVER_PID