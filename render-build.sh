#!/bin/bash
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    tesseract-ocr \
    libtesseract-dev \
    python3.11-dev

# Ensure we're using Python 3.11
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
update-alternatives --set python3 /usr/bin/python3.11

# Install Python dependencies
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt
