#!/bin/bash
set -o errexit

# Install Python dependencies only (no system packages)
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Configure pytesseract to use system tesseract if available
echo "Configuring pytesseract..."
if ! command -v tesseract &> /dev/null; then
    echo "Tesseract OCR not found - image text extraction will be disabled"
    # Create a dummy tesseract command to prevent errors
    echo 'echo "Tesseract not installed" >&2; exit 1' > /usr/local/bin/tesseract
    chmod +x /usr/local/bin/tesseract
fi
