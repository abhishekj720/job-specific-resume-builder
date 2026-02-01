#!/bin/bash

# Quick setup script for Reddit Stock Sentiment Analyzer

echo "========================================="
echo "Stock Sentiment Analyzer - Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Setup .env file
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: You need to add your Reddit API credentials to the .env file"
    echo ""
    echo "To get Reddit API credentials:"
    echo "1. Go to https://www.reddit.com/prefs/apps"
    echo "2. Click 'Create App' or 'Create Another App'"
    echo "3. Choose 'script' as the app type"
    echo "4. Fill in the fields (redirect uri can be http://localhost:8080)"
    echo "5. Copy the client ID and secret to your .env file"
    echo ""
    echo "Edit the .env file now? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        ${EDITOR:-nano} .env
    fi
else
    echo ".env file already exists"
fi

echo ""
echo "========================================="
echo "Setup complete!"
echo "========================================="
echo ""
echo "To run the analyzer:"
echo "  python agent.py"
echo ""
echo "To see examples:"
echo "  python example.py"
echo ""
