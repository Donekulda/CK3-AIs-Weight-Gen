#!/bin/bash

# CK3 AI Weight Check Script
# This script runs the weight calculator to show current AI model weights

echo "🔍 Running CK3 AI Weight Check..."
echo "=================================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
fi

# Add src directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Run the weight check
python src/quick_weight_check.py

echo ""
echo "✅ Weight check completed!" 