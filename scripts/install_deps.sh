#!/bin/bash
# Dependency installation script for Mars-Rover-Control-OS

echo "🚀 Installing dependencies for Mars-Rover-Control-OS..."

# Python dependencies
pip install numpy opencv-python pyyaml

# ROS2 dependencies (mock)
sudo apt update
# sudo apt install -y ros-humble-ros-base ros-humble-cv-bridge

echo "✅ Dependencies installed successfully!"
