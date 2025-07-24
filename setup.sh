#!/bin/bash

# Dark Web Checker Setup Script
# This script helps set up the Dark Web Checker tool

echo "🔍 Dark Web Checker Setup"
echo "========================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Found: $python_version"
else
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3.7 or higher from https://python.org"
    exit 1
fi

# Check pip
echo "Checking pip..."
pip_version=$(pip3 --version 2>&1)
if [[ $? -eq 0 ]]; then
    echo "✅ Found: $pip_version"
else
    echo "❌ pip is required but not found."
    echo "Please install pip or use your system's package manager."
    exit 1
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip3 install -r requirements.txt

if [[ $? -eq 0 ]]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check for API key
echo ""
echo "Checking for API key..."
if [[ -n "$HIBP_API_KEY" ]]; then
    echo "✅ HIBP_API_KEY environment variable is set"
else
    echo "⚠️  HIBP_API_KEY environment variable is not set"
    echo ""
    echo "To get your API key:"
    echo "1. Visit: https://haveibeenpwned.com/API/Key"
    echo "2. Purchase an API key"
    echo "3. Set it as an environment variable:"
    echo "   export HIBP_API_KEY='your_key_here'"
    echo ""
    echo "Or you can provide it when running the tool with --api-key parameter"
fi

# Make the script executable
chmod +x dark_web_checker.py

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Usage examples:"
echo "  python3 dark_web_checker.py -e user@example.com -o results.json"
echo "  python3 dark_web_checker.py -f examples/sample_emails.txt -o results.csv"
echo "  python3 dark_web_checker.py  # Interactive mode"
echo ""
echo "For more information, see the documentation in the docs/ directory."