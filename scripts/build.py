#!/bin/bash
set -e

echo "Building DeskPet for Windows..."

pyinstaller deskpet.spec --clean

echo "Build complete! Output: dist/DeskPet"
echo ""
echo "To run on Windows, copy the 'dist/DeskPet' folder to your Windows machine."
