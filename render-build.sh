#!/bin/bash
set -o errexit

# Use Render's package cache instead of trying to update
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Tesseract OCR if needed (using Render's available packages)
if ! command -v tesseract &> /dev/null; then
    echo "Installing Tesseract OCR..."
    curl -L https://github.com/tesseract-ocr/tesseract/archive/refs/tags/5.3.2.tar.gz | tar xz
    cd tesseract-5.3.2
    ./autogen.sh
    ./configure
    make
    make install
    ldconfig
    cd ..
fi
