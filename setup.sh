#!/bin/bash

# Quick setup script for Property Collection Bot

echo "🏠 Property Collection Bot - Quick Setup"
echo "========================================"
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create virtual environment (optional but recommended)
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
echo "   To activate: source venv/bin/activate"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt

# Setup .env file
echo ""
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "   ⚠️  Please edit .env and add your credentials!"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials:"
echo "   - TELEGRAM_BOT_TOKEN (from @BotFather)"
echo "   - GEMINI_API_KEY (from https://aistudio.google.com)"
echo "   - DATABASE_URL (your PostgreSQL connection)"
echo ""
echo "2. Setup database:"
echo "   psql -d your_database -f schema.sql"
echo ""
echo "3. Run the bot:"
echo "   python3 bot.py"
echo ""
