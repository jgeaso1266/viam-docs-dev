#!/usr/bin/env python3
"""
Web viewer for Gazebo cameras.
Serves MJPEG streams for the can inspection camera.
"""

import io
import time
import threading
from flask import Flask, Response, render_template_string

from gz.transport13 import Node
from gz.msgs10.image_pb2 import Image as GzImage
from PIL import Image

app = Flask(__name__)

# Camera streams - each has its own frame buffer
cameras = {
    "inspection": {
        "topic": "/inspection_camera",
        "frame": None,
        "lock": threading.Lock(),
        "label": "Inspection Camera (RGB)"
    }
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Can Inspection Viewer</title>
    <style>
        body {
            background: #1a1a1a;
            color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
        }
        h1 {
            text-align: center;
            margin-bottom: 5px;
            font-weight: 400;
        }
        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
        }
        .camera-container {
            max-width: 800px;
            margin: 0 auto;
        }
        .camera-card {
            background: #252525;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .camera-header {
            padding: 12px 16px;
            background: #333;
            font-size: 14px;
            font-weight: 500;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .camera-header .topic {
            color: #888;
            font-family: monospace;
            font-size: 11px;
        }
        .camera-feed {
            position: relative;
            background: #000;
        }
        .camera-feed img {
            display: block;
            width: 100%;
            height: auto;
        }
        .camera-feed .no-signal {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: #666;
            font-size: 14px;
        }
        .info-bar {
            max-width: 800px;
            margin: 30px auto 0;
            padding: 15px 20px;
            background: #252525;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            color: #888;
        }
        .info-bar h3 {
            margin: 0 0 10px 0;
            color: #fff;
            font-size: 13px;
        }
    </style>
</head>
<body>
    <h1>Can Inspection Station</h1>
    <p class="subtitle">Simulated conveyor belt inspection system</p>

    <div class="camera-container">
        <div class="camera-card">
            <div class="camera-header">
                <span>Inspection Camera (RGB)</span>
                <span class="topic">/inspection_camera</span>
            </div>
            <div class="camera-feed">
                <img src="/stream/inspection" alt="Inspection Camera">
            </div>
        </div>
    </div>

    <div class="info-bar">
        <h3>Inspection Station Components</h3>
        <p>• Overhead inspection camera (640x480 @ 30fps)</p>
        <p>• Conveyor belt with side rails</p>
        <p>• Air jet rejector for defective cans</p>
        <p>• Reject bin (red) for dented cans</p>
        <p>• Output chute (green) for good cans</p>
        <p>• Cans spawned automatically (~10% defect rate)</p>
    </div>
</body>
</html>
"""


def make_rgb_callback(camera_key):
    """Create a callback for RGB camera topics."""
    def callback(msg: GzImage):
        try:
            # Convert raw RGB to PIL Image
            img = Image.frombytes("RGB", (msg.width, msg.height), msg.data)

            # Convert to JPEG
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=80)
            jpeg_bytes = buffer.getvalue()

            with cameras[camera_key]["lock"]:
                cameras[camera_key]["frame"] = jpeg_bytes
        except Exception as e:
            print(f"Error processing {camera_key} frame: {e}")
    return callback


def generate_stream(camera_key):
    """Generator that yields MJPEG frames for a specific camera."""
    while True:
        with cameras[camera_key]["lock"]:
            frame = cameras[camera_key]["frame"]

        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        time.sleep(0.033)  # ~30fps


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/stream/<camera>')
def stream(camera):
    if camera not in cameras:
        return "Camera not found", 404
    return Response(
        generate_stream(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/snapshot/<camera>')
def snapshot(camera):
    if camera not in cameras:
        return "Camera not found", 404
    with cameras[camera]["lock"]:
        frame = cameras[camera]["frame"]
    if frame is None:
        return "No frame available", 503
    return Response(frame, mimetype='image/jpeg')


def main():
    node = Node()

    print("Subscribing to camera topics...")

    # Inspection camera
    success = node.subscribe(GzImage, "/inspection_camera", make_rgb_callback("inspection"))
    print(f"  /inspection_camera: {'OK' if success else 'FAILED'}")

    print(f"\nStarting web server on http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, threaded=True)


if __name__ == "__main__":
    main()
