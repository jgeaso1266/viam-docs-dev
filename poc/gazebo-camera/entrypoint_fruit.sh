#!/bin/bash
set -e

# Fruit Inspection POC Entrypoint
# Launches Gazebo with the fruit inspection world and web viewer

# Export protobuf compatibility setting
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Start virtual display for headless rendering
echo "Starting Xvfb virtual display..."
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1
sleep 2

echo "Starting Gazebo Sim with can inspection world..."
gz sim -s /opt/worlds/fruit_inspection.sdf &
GZ_PID=$!

# Wait for Gazebo to initialize
echo "Waiting for Gazebo to initialize..."
sleep 10

echo ""
echo "Checking Gazebo topics..."
gz topic -l

# Unpause simulation
echo ""
echo "Unpausing simulation..."
gz service -s /world/fruit_inspection/control --reqtype gz.msgs.WorldControl --reptype gz.msgs.Boolean --timeout 2000 --req 'pause: false'
sleep 1

# Start web viewer
echo ""
echo "Starting web viewer..."
python3 /opt/web_viewer_fruit.py &
VIEWER_PID=$!

echo ""
echo "=========================================="
echo "Can Inspection POC Running!"
echo "=========================================="
echo ""
echo "  Web Viewer:  http://localhost:8080"
echo ""
echo "  Camera topic: /inspection_camera"
echo ""
echo "  World: fruit_inspection (can inspection)"
echo "  - Good cans: silver aluminum, undamaged"
echo "  - Dented cans: visible dent marks"
echo ""
echo "=========================================="
echo ""

# Keep container running
wait $GZ_PID
