#!/bin/bash
set -e

# Fruit Inspection POC Entrypoint
# Launches Gazebo with the fruit inspection world and web viewer

# Export protobuf compatibility setting
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Start SSH server
echo "Starting SSH server..."
/usr/sbin/sshd

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

# Start can spawner (moves cans along conveyor)
echo ""
echo "Starting can spawner..."
python3 /opt/can_spawner.py &
SPAWNER_PID=$!

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
echo "  SSH:         ssh -p 2222 viam@localhost"
echo "               Password: viam"
echo ""
echo "  Camera topic: /inspection_camera"
echo ""
echo "  World: fruit_inspection (can inspection)"
echo "  - Cans spawn continuously at input end"
echo "  - ~10% of cans are dented (defective)"
echo "  - Belt moves cans past inspection camera"
echo ""
echo "  To set up viam-server after SSH:"
echo "    curl https://storage.googleapis.com/packages.viam.com/apps/viam-server/viam-server-stable-x86_64.AppImage -o viam-server"
echo "    chmod +x viam-server"
echo "    ./viam-server -config /path/to/your-config.json"
echo ""
echo "=========================================="
echo ""

# Keep container running
wait $GZ_PID
