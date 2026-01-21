#!/usr/bin/env python3
"""
Web viewer for Fruit Inspection simulation.
Serves MJPEG stream from the overhead inspection camera.
"""

import io
import time
import threading
from flask import Flask, Response, render_template_string

from gz.transport13 import Node
from gz.msgs10.image_pb2 import Image as GzImage
from PIL import Image

app = Flask(__name__)

# Camera stream
camera = {
    "topic": "/inspection_camera",
    "frame": None,
    "lock": threading.Lock(),
    "width": 640,
    "height": 480
}

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Fruit Inspection Station</title>
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
        .main-container {
            max-width: 900px;
            margin: 0 auto;
        }
        .camera-card {
            background: #252525;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            margin-bottom: 20px;
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
        .camera-header .status {
            color: #4a4;
            font-size: 12px;
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
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .info-card {
            background: #252525;
            border-radius: 8px;
            padding: 15px 20px;
        }
        .info-card h3 {
            margin: 0 0 10px 0;
            font-size: 13px;
            color: #fff;
            font-weight: 500;
        }
        .info-card p {
            margin: 5px 0;
            font-size: 12px;
            color: #888;
        }
        .info-card .good {
            color: #4a4;
        }
        .info-card .bad {
            color: #a44;
        }
        .legend {
            display: flex;
            gap: 20px;
            margin-top: 10px;
        }
        .legend-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
        }
        .legend-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        .legend-dot.good {
            background: #c41e1e;
        }
        .legend-dot.bad {
            background: linear-gradient(135deg, #c41e1e 60%, #3a2010 60%);
        }
    </style>
</head>
<body>
    <h1>Fruit Inspection Station</h1>
    <p class="subtitle">Quality grading simulation - detecting bruised apples</p>

    <div class="main-container">
        <div class="camera-card">
            <div class="camera-header">
                <span>Overhead Inspection Camera</span>
                <span class="status">● LIVE</span>
                <span class="topic">/inspection_camera</span>
            </div>
            <div class="camera-feed">
                <img src="/stream" alt="Inspection Camera">
            </div>
        </div>

        <div class="info-grid">
            <div class="info-card">
                <h3>Inspection Criteria</h3>
                <p class="good">✓ PASS: Uniform red color, no visible damage</p>
                <p class="bad">✗ FAIL: Dark bruise spots, discoloration</p>
                <div class="legend">
                    <div class="legend-item">
                        <div class="legend-dot good"></div>
                        <span>Good apple</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-dot bad"></div>
                        <span>Bruised apple</span>
                    </div>
                </div>
            </div>

            <div class="info-card">
                <h3>Station Components</h3>
                <p>• Conveyor belt with side rails</p>
                <p>• Overhead RGB camera (640x480, 30fps)</p>
                <p>• Air jet rejector (pneumatic)</p>
                <p>• Reject bin (red) / Output chute (green)</p>
            </div>
        </div>
    </div>
</body>
</html>
"""


def camera_callback(msg: GzImage):
    """Process incoming camera images from Gazebo."""
    try:
        # Convert raw RGB to PIL Image
        img = Image.frombytes("RGB", (msg.width, msg.height), msg.data)

        # Convert to JPEG
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        jpeg_bytes = buffer.getvalue()

        with camera["lock"]:
            camera["frame"] = jpeg_bytes
            camera["width"] = msg.width
            camera["height"] = msg.height
    except Exception as e:
        print(f"Error processing frame: {e}")


def generate_stream():
    """Generator that yields MJPEG frames."""
    while True:
        with camera["lock"]:
            frame = camera["frame"]

        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        time.sleep(0.033)  # ~30fps


@app.route('/')
def index():
    return render_template_string(HTML_PAGE)


@app.route('/stream')
def stream():
    return Response(
        generate_stream(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


@app.route('/snapshot')
def snapshot():
    with camera["lock"]:
        frame = camera["frame"]
    if frame is None:
        return "No frame available", 503
    return Response(frame, mimetype='image/jpeg')


def main():
    node = Node()

    print("Subscribing to inspection camera...")
    success = node.subscribe(GzImage, "/inspection_camera", camera_callback)
    print(f"  /inspection_camera: {'OK' if success else 'FAILED'}")

    print(f"\nStarting web server on http://0.0.0.0:8080")
    app.run(host='0.0.0.0', port=8080, threaded=True)


if __name__ == "__main__":
    main()
