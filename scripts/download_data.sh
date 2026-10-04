#!/bin/bash
set -e

echo "🚀 Downloading NASA C-MAPSS dataset..."
mkdir -p data/raw

# We attempt to download from a public repository mirror.
# If unavailable, a Python script will generate synthetic data matching the schema.

FILE_TRAIN="data/raw/train_FD001.txt"
FILE_TEST="data/raw/test_FD001.txt"
FILE_RUL="data/raw/RUL_FD001.txt"

if [ ! -f "$FILE_TRAIN" ]; then
    echo "Downloading train_FD001.txt..."
    curl -sSL "https://raw.githubusercontent.com/umbertogriffo/Predictive-Maintenance-using-LSTM/master/Dataset/train_FD001.txt" -o "$FILE_TRAIN" || true
fi

if [ ! -f "$FILE_TEST" ]; then
    echo "Downloading test_FD001.txt..."
    curl -sSL "https://raw.githubusercontent.com/umbertogriffo/Predictive-Maintenance-using-LSTM/master/Dataset/test_FD001.txt" -o "$FILE_TEST" || true
fi

if [ ! -f "$FILE_RUL" ]; then
    echo "Downloading RUL_FD001.txt..."
    curl -sSL "https://raw.githubusercontent.com/umbertogriffo/Predictive-Maintenance-using-LSTM/master/Dataset/RUL_FD001.txt" -o "$FILE_RUL" || true
fi

# Fallback: Generate synthetic data if the download failed (file size is too small or missing)
if [ ! -s "$FILE_TRAIN" ] || [ $(wc -c < "$FILE_TRAIN") -lt 1000 ]; then
    echo "⚠️ Download mirror failed or blocked. Generating synthetic C-MAPSS data for FD001..."
    
    # We will use the VENV python to run a quick generation script
    VENV_PATH="/mnt/sda5/Projects/QT/.venv"
    source "$VENV_PATH/bin/activate"
    python3 scripts/generate_mock_cmapss.py
else
    echo "✅ C-MAPSS data downloaded successfully."
fi
