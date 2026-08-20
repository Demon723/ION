#!/bin/bash
# Deployment Script for Intent-Deterministic Development Platform
# Developer: ADITYA KAMBLE

set -e

echo "=========================================="
echo "ION Platform Deployment Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 is required"; exit 1; }

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create artifact directory
echo "Creating artifact directory..."
mkdir -p artifacts

# Run quick test
echo "Running quick test..."
python3 quick_test.py

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "To run the platform:"
echo "  source venv/bin/activate"
echo "  python3 main.py --demo"
echo ""
echo "To run real-time demo:"
echo "  python3 main.py --realtime"
echo ""
echo "To compile ION source:"
echo "  python3 main.py --compile your_file.ion"
echo ""
echo "To run examples:"
echo "  python3 main.py --example 1"
echo "  python3 main.py --example 8  # Enhanced examples"
echo ""
echo "Developer: ADITYA KAMBLE"