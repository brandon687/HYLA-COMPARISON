#!/bin/bash
# Hyla Stock Comparison Dashboard Startup Script

echo "========================================"
echo "Hyla Stock Comparison Dashboard"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 from https://www.python.org/"
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed."
    echo "Please install pip3 first."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "Dependencies installed."
echo ""

# Start the Flask application
echo "========================================"
echo "Starting dashboard..."
echo "========================================"
echo ""
echo "The dashboard will open at:"
echo "    http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 web_app.py
