#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "🚀 Starting SkyPrognos Platform..."

# 1. Activate the virtual environment
VENV_PATH="/mnt/sda5/Projects/QT/.venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 Virtual environment not found at $VENV_PATH. Please run ./scripts/setup.sh first."
    exit 1
fi

echo "🔄 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# 2. Start the Streamlit Web App
echo "📱 Preparing the Streamlit Frontend..."
export PYTHONUNBUFFERED=1

echo "🌐 Starting Frontend Web Server on http://127.0.0.1:8501"
echo "👉 Open your browser to use SkyPrognos"
echo "Press Ctrl+C to stop the server."

streamlit run app/Home.py
