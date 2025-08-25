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

echo "Starting RSA Cryptography Lab server..."
echo "Press Ctrl+C to stop the server when you're done."

# Function to cleanup server process on exit
cleanup() {
    echo ""
    echo "Shutting down server..."
    if [ ! -z "$SERVER_PID" ]; then
        kill $SERVER_PID 2>/dev/null
        wait $SERVER_PID 2>/dev/null
    fi
    echo "Server stopped."
    exit 0
}

# Set trap to catch Ctrl+C (SIGINT) and cleanup
trap cleanup SIGINT

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

echo "RSA Cryptography Lab is now running at http://localhost:$PORT"
echo ""
echo "⚠️  IMPORTANT: Use Incognito/Private browsing mode!"
echo "   Since this server runs on port 12000, your browser may cache"
echo "   old content. Use Incognito/Private mode to ensure you see"
echo "   the latest version of the lab."
echo ""
echo "Keep this terminal window open while using the lab."
echo "Press Ctrl+C to stop the server when you're done."

# Wait for user to press Ctrl+C
wait $SERVER_PID