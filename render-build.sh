#!/bin/bash
set -o errexit

# Reset environment
pip uninstall -y numpy pandas

# Upgrade pip and install fresh requirements
pip install --upgrade pip
pip install -r requirements.txt
