#!/bin/bash
# Build script for Render
set -e

echo "Installing dependencies..."
pip install --upgrade pip setuptools wheel
pip install --no-cache-dir -r requirements.txt

echo "Build complete!"
