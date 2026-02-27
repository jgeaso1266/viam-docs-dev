# Add a Camera

**Time:** ~15 minutes
**Prerequisites:** [Connect to Cloud](connect-to-cloud.md) (machine created, `viam-server` running, machine online)
**Works with:** Simulation ✓ | Real Hardware ✓

## What You'll Learn

- How Viam abstracts hardware into components with uniform APIs
- How to add and configure a camera component through the Viam app
- How to verify the camera feed using the built-in test panel
- How to capture an image programmatically in Python and Go

## What Problem This Solves

You have a camera -- USB webcam, Raspberry Pi camera module, IP camera, or even a simulated one -- and you need your machine to use it.
In Viam, all cameras expose the same API regardless of the underlying hardware.
Once you configure a camera here, every other block that needs images (data capture, computer vision, visual servoing) works without changes to your code.

## Concepts

### Components and hardware abstraction

In Viam, a **component** is any piece of hardware your machine can control or read from: cameras, motors, arms, sensors, encoders, and more.
Every component of the same type shares a common API.
A USB webcam and a Raspberry Pi camera module both implement the *camera* API, so the code you write to get images from one works identically with the other.

This means you can:

- Develop against a simulated camera and swap in real hardware later.
- Switch camera hardware without changing application code.
- Use the same code across different machines with different physical setups.

### Camera models

When you add a camera, you choose a **model** that tells `viam-server` how to communicate with the hardware.
Common models include:

| Model | Hardware | When to use |
|-------|----------|-------------|
| `webcam` | USB webcams, built-in laptop cameras | Most common starting point |
| `ffmpeg` | RTSP/IP cameras, video streams | Network cameras, video files |
| `image_file` | Static image on disk | Testing without any camera hardware |
| `fake` | Simulated camera (built into Viam) | Development and CI environments |

## Components Needed

- A machine running `viam-server` (from [Connect to Cloud](connect-to-cloud.md))
- One of the following:
  - A USB webcam connected to the machine
  - A Raspberry Pi camera module
  - No camera at all (use the `fake` model for simulation)

## Steps

### 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.
If it shows as offline, verify that `viam-server` is running on your machine.

### 2. Add a camera component

1. Click the **+** button in the left sidebar.
2. Select **Component**.
3. For the type, select **camera**.
4. Choose the model that matches your hardware:
   - **webcam** for a USB webcam or built-in laptop camera.
   - **fake** if you have no camera and want a simulated feed.
5. Name your camera. This guide uses `my-camera`. The name is how you reference this camera in code, so keep it short and descriptive.
6. Click **Create**.

### 3. Configure camera attributes

After creating the component, you'll see its configuration panel.

**For a USB webcam (`webcam` model):**

Most USB webcams work with no additional configuration.
If you have multiple cameras connected, specify which one to use:

```json
{
  "video_path": "video0"
}
```

To find available video devices on Linux:

```bash
ls /dev/video*
```

You can also set resolution and frame rate:

```json
{
  "width_px": 640,
  "height_px": 480,
  "frame_rate": 30
}
```

**For a simulated camera (`fake` model):**

No attributes needed. The fake camera generates color images automatically.
Leave the attributes section empty or use:

```json
{}
```

### 4. Save the configuration

Click **Save** in the upper right of the configuration panel.

When you save, `viam-server` automatically reloads the configuration and initializes the new component.
You do not need to restart anything.

### 5. Test the camera

Every component in Viam has a built-in **test panel** in the Configure tab.
The test panel uses the exact same APIs your code will use, so if the camera works here, it will work in your programs.

1. Find your camera component in the configuration view.
2. Expand the **TEST** section at the bottom of the component panel.
3. Click **Toggle stream** to see a live video feed from the camera.
4. Click **Get image** to capture a single frame.

You should see a live feed (or a colored pattern if using the `fake` model).

## Try It

Capture an image from your camera programmatically.
Make sure you have the Viam SDK installed for your language.

### Python

Install the SDK if you haven't already:

```bash
pip install viam-sdk
```

Save this as `camera_test.py`:

```python
import asyncio
from viam.robot.client import RobotClient
from viam.components.camera import Camera


async def main():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR-API-KEY",
        api_key_id="YOUR-API-KEY-ID"
    )
    robot = await RobotClient.at_address("YOUR-MACHINE-ADDRESS", opts)

    camera = Camera.from_robot(robot, "my-camera")
    image = await camera.get_image()
    image.save("test-capture.png")
    print(f"Captured {image.size[0]}x{image.size[1]} image")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Replace the placeholder values:

1. In the Viam app, go to your machine's **CONNECT** tab.
2. Select **API keys** and copy your API key and API key ID.
3. Copy the machine address from the same tab.

Run it:

```bash
python camera_test.py
```

You should see output like:

```
Captured 640x480 image
```

And a file called `test-capture.png` in your current directory.

### Go

Initialize a Go module and install the SDK if you haven't already:

```bash
mkdir camera-test && cd camera-test
go mod init camera-test
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
	"context"
	"fmt"
	"image/png"
	"os"

	"go.viam.com/rdk/components/camera"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/utils"
)

func main() {
	ctx := context.Background()
	logger := logging.NewLogger("camera-test")

	robot, err := client.New(ctx, "YOUR-MACHINE-ADDRESS", logger,
		client.WithCredentials(utils.Credentials{
			Type:    utils.CredentialsTypeAPIKey,
			Payload: "YOUR-API-KEY",
		}),
		client.WithAPIKeyID("YOUR-API-KEY-ID"),
	)
	if err != nil {
		logger.Fatal(err)
	}
	defer robot.Close(ctx)

	cam, err := camera.FromRobot(robot, "my-camera")
	if err != nil {
		logger.Fatal(err)
	}

	img, _, err := cam.Images(ctx)
	if err != nil {
		logger.Fatal(err)
	}

	f, err := os.Create("test-capture.png")
	if err != nil {
		logger.Fatal(err)
	}
	defer f.Close()

	if err := png.Encode(f, img[0].Image); err != nil {
		logger.Fatal(err)
	}

	fmt.Printf("Captured image and saved to test-capture.png\n")
}
```

Replace the placeholder values with your machine address, API key, and API key ID from the Viam app's **CONNECT** tab.

Run it:

```bash
go run main.go
```

## Troubleshooting

### Camera not appearing as a component option

- Confirm your machine is **Live** in the Viam app.
- Refresh the page and try again.

### Test panel shows no image or a black frame

- **USB webcam:** Check the physical connection. Unplug and replug the camera. On Linux, verify the device exists with `ls /dev/video*`.
- **Raspberry Pi camera module:** Ensure the ribbon cable is fully seated and the camera is enabled in `raspi-config`.
- **`video_path` wrong:** If you have multiple cameras, the default device may not be the one you expect. Try different `video_path` values (`video0`, `video1`, etc.).

### "Failed to find the best driver" or driver errors

- On Linux, install required video drivers: `sudo apt install v4l-utils`.
- On macOS, grant camera permissions to the terminal application running `viam-server`.

### Code connects but `get_image` fails

- Verify the camera name in your code matches the name in the Viam app exactly (names are case-sensitive).
- Check that the camera test panel works in the Viam app first. If it doesn't work there, the issue is with the camera configuration, not your code.
- Ensure `viam-server` is still running and the machine is online.

### Image is very dark or overexposed

- Some cameras need a few seconds to adjust exposure after starting. Try adding a short delay before capturing, or capture and discard a few frames first.
- Check if the camera has a physical lens cap or privacy shutter.

## What's Next

- [Capture and Sync Data](capture-and-sync-data.md) -- configure your camera to automatically capture images and sync them to the cloud.
- [Add Computer Vision](../vision-detection/add-computer-vision.md) -- run ML models on your camera feed to detect or classify objects.
