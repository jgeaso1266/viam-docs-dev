# Start Writing Code

**Status:** 🟡 Draft

**Time:** ~20 minutes
**Prerequisites:** Connect to Cloud, Add a Camera
**Works with:** Simulation | Real Hardware

---

## What You'll Learn

- Connect to your machine from your laptop
- Access configured components (camera, sensors, actuators) by name
- Write and test code locally against remote hardware
- Iterate rapidly without deploying anything

## The Development Pattern

Your machine runs `viam-server` with configured components. Your code runs on your laptop and connects over the network. When you call `camera.get_image()`, that call goes to the real camera on the machine. You get the image back on your laptop.

```
┌─────────────────┐         ┌─────────────────┐
│   Your Laptop   │  WebRTC │    Machine      │
│                 │◄───────►│                 │
│  Python/Go code │         │  viam-server    │
│  runs here      │         │  + components   │
└─────────────────┘         └─────────────────┘
```

No SSH. No file copying. No deploy step. Viam handles NAT traversal automatically.

---

## Step 1: Get Your Connection Credentials

In the Viam app, go to your machine's **CONNECT** tab. Copy the connection code for your language.

You'll get something like:

```python
# Python
robot = await connect()

async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='your-api-key',
        api_key_id='your-api-key-id'
    )
    return await RobotClient.at_address('your-machine.viam.cloud', opts)
```

```go
// Go
machine, err := client.New(
    context.Background(),
    "your-machine.viam.cloud",
    logger,
    client.WithDialOptions(rpc.WithEntityCredentials(
        "your-api-key-id",
        rpc.Credentials{
            Type:    rpc.CredentialsTypeAPIKey,
            Payload: "your-api-key",
        })),
)
```

---

## Step 2: Access Components by Name

Components you configured in the Viam app are available by name:

```python
# Python
from viam.components.camera import Camera

# Get the camera you configured
camera = Camera.from_robot(robot, "my-camera")

# Use it
image = await camera.get_image()
```

```go
// Go
import "go.viam.com/rdk/components/camera"

// Get the camera you configured
cam, err := camera.FromRobot(machine, "my-camera")

// Use it
img, err := cam.Image(ctx, nil, nil)
```

The name (`"my-camera"`) matches what you configured. You're not instantiating hardware—you're getting a reference to hardware that's already running on the machine.

---

## Step 3: Write Your Logic

Now write code that does something useful. This runs on your laptop:

```python
# inspection_test.py
import asyncio
from viam.robot.client import RobotClient
from viam.components.camera import Camera
from viam.services.vision import VisionClient

async def main():
    robot = await connect()

    # Get components by name (these are configured on the machine)
    camera = Camera.from_robot(robot, "inspection-cam")
    detector = VisionClient.from_robot(robot, "part-detector")

    # Your logic runs locally, but operates on remote hardware
    image = await camera.get_image()
    detections = await detector.get_detections(image)

    for d in detections:
        print(f"Found {d.class_name} with confidence {d.confidence}")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python inspection_test.py
```

The camera captures an image on the machine. The image comes to your laptop. The detector runs inference (on the machine). Results come back to your laptop. Your `print()` shows them locally.

---

## Step 4: Iterate

Change your code. Run it again. No deploy cycle.

```python
# Add filtering logic
for d in detections:
    if d.confidence > 0.8:
        print(f"HIGH CONFIDENCE: {d.class_name}")
```

Run again immediately. This is your development loop.

---

## Step 5: Build a CLI Tool (Optional)

For more complex projects, structure your code as a CLI tool with commands:

```python
# inspection_cli.py
import argparse
import asyncio

async def cmd_detect(robot):
    """Run detection and print results."""
    camera = Camera.from_robot(robot, "inspection-cam")
    detector = VisionClient.from_robot(robot, "part-detector")

    image = await camera.get_image()
    detections = await detector.get_detections(image)

    for d in detections:
        print(f"{d.class_name}: {d.confidence:.2f}")

async def cmd_capture(robot, output_path):
    """Capture and save an image."""
    camera = Camera.from_robot(robot, "inspection-cam")
    image = await camera.get_image()
    image.save(output_path)
    print(f"Saved to {output_path}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["detect", "capture"])
    parser.add_argument("--output", default="capture.png")
    args = parser.parse_args()

    robot = await connect()

    try:
        if args.command == "detect":
            await cmd_detect(robot)
        elif args.command == "capture":
            await cmd_capture(robot, args.output)
    finally:
        await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Usage:

```bash
python inspection_cli.py detect
python inspection_cli.py capture --output test.png
```

This pattern scales to complex applications. Add commands as you need them.

---

## When to Deploy Code to the Machine

For most development and testing, keep code on your laptop. Deploy to the machine only when you need:

- **Autonomous operation** — Code that runs without your laptop connected
- **Low latency** — Operations where network round-trip matters
- **Offline operation** — Code that must run when internet is unavailable

When you're ready for that, see [Building Modules](../../reference/modules.md).

---

## Try It

1. Copy the connection code from your machine's CONNECT tab
2. Write a script that gets an image from your camera
3. Run it from your laptop
4. Verify you see the image (save it locally and open it)

---

## What's Next

- [Add Computer Vision](../perception/add-computer-vision.md) — Add ML detection to your script
- [Trigger on Detection](../stationary-vision/trigger-on-detection.md) — React when you detect something
- [Configure Data Pipelines](./configure-data-pipelines.md) — Process data at scale

---

## Key Takeaway

**Your code runs on your laptop. The robot runs viam-server with configured components. You connect, access components by name, and iterate locally. No deployment during development.**
