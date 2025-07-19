#!/bin/bash

# CK3 AI Weight Generator - Test Runner Script
# This script sets up the Python virtual environment, installs dependencies,
# and runs the test suite.

# Don't exit on error, let us handle it manually

echo "CK3 AI Weight Generator - Test Runner Script"
echo "==========================================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -d "tests" ] || [ ! -d "models" ]; then
    echo "Error: Please run this script from the CK3-AIs-Weight-Gen directory"
    echo "Expected directories: tests/, models/"
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

# Check if tests directory exists and contains test files
if [ ! -d "tests" ]; then
    echo "Error: tests directory not found"
    exit 1
fi

# Find all test files
test_files=$(find tests -name "test_*.py" -type f)
if [ -z "$test_files" ]; then
    echo "Error: No test files found in tests directory"
    exit 1
fi

echo ""
echo "Environment setup complete!"
echo "Running test suite..."
echo ""

# Add src directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run all test files
total_tests=0
passed_tests=0
failed_tests=0

for test_file in $test_files; do
    echo "Running $(basename "$test_file")..."
    echo "----------------------------------------"
    
    if python3 "$test_file"; then
        echo "✅ $(basename "$test_file") passed"
        ((passed_tests++))
    else
        echo "❌ $(basename "$test_file") failed"
        ((failed_tests++))
    fi
    
    ((total_tests++))
    echo ""
done

echo "Test Results Summary"
echo "==================="
echo "Total tests run: $total_tests"
echo "Passed: $passed_tests"
echo "Failed: $failed_tests"

if [ $failed_tests -eq 0 ]; then
    echo "🎉 All tests passed!"
    exit 0
else
    echo "⚠️  Some tests failed. Please check the output above."
    exit 1
fi 