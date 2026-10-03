#!/bin/bash
set -e

echo "🚀 Initializing SkyPrognos Environment..."

VENV_PATH="/mnt/sda5/Projects/QT/.venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Error: The required virtual environment does not exist at $VENV_PATH"
    echo "Please ensure the QT project is properly initialized."
    exit 1
fi

echo "🔄 Using existing virtual environment from QT project..."
source "$VENV_PATH/bin/activate"

echo "📥 Installing/Updating SkyPrognos dependencies..."
pip install -e .[dev]

echo "✅ Environment setup complete."
echo "👉 You can activate it manually via: source '$VENV_PATH/bin/activate'"
