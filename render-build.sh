#!/bin/bash
set -o errexit

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Configure pytesseract fallback
echo "Configuring pytesseract fallback..."
if ! command -v tesseract &> /dev/null; then
    echo "WARNING: Tesseract OCR not found - image text extraction will be disabled"
    # Create a local dummy script that will be used by pytesseract
    mkdir -p ./.tesseract_fallback
    echo 'echo "Tesseract OCR is not available in this environment" >&2' > ./.tesseract_fallback/tesseract
    echo 'exit 1' >> ./.tesseract_fallback/tesseract
    chmod +x ./.tesseract_fallback/tesseract
    export TESSERACT_CMD=$PWD/.tesseract_fallback/tesseract
fi
