#!/bin/bash
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    tesseract-ocr \
    libtesseract-dev \
    python3.11-dev \
    libxml2-dev \
    libxslt-dev \
    libffi-dev

# Install Python dependencies
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt
