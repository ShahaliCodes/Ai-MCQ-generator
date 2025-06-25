#!/bin/bash
set -o errexit

# Update package lists and install system dependencies
apt-get update
apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    tesseract-ocr \
    libtesseract-dev

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
