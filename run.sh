#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "🚀 Initializing SkyPrognos Training Pipeline..."

# 1. Activate the virtual environment
VENV_PATH="/mnt/sda5/Projects/QT/.venv"
if [ ! -d "$VENV_PATH" ]; then
    echo "📦 Virtual environment not found at $VENV_PATH. Please run ./scripts/setup.sh first."
    exit 1
fi

echo "🔄 Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# 2. Run the ML Training Engine
echo "⚡ Running ML Pipeline..."
echo "==============================================="
echo "⏳ Loading Libraries (PyTorch, XGBoost)..."
mkdir -p runs
export PYTHONUNBUFFERED=1

python3 -m prognos.train --dataset FD001 --epochs 50 --max-ram 6.0 2>&1 | tee runs/training_log.txt
