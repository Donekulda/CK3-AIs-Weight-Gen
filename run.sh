#!/bin/bash

# CK3 AI Weight Generator - Setup and Run Script
# This script sets up the Python virtual environment, installs dependencies,
# and runs the CK3 AI weight generator.

set -e  # Exit on any error

echo "CK3 AI Weight Generator - Setup and Run Script"
echo "=============================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -d "events" ] || [ ! -d "models" ]; then
    echo "Error: Please run this script from the CK3-AIs-Weight-Gen directory"
    echo "Expected directories: events/, models/"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "Warning: requirements.txt not found, installing basic dependencies..."
    pip install pathlib typing-extensions
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found in current directory"
    exit 1
fi

# Make main.py executable
chmod +x main.py

# Add src directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

echo ""
echo "Environment setup complete!"
echo "Running CK3 AI Weight Generator..."
echo ""

# Run the main program
python3 main.py

echo ""
echo "Script execution completed."
echo "You can deactivate the virtual environment with: deactivate" 