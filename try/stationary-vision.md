# Stationary Vision Tutorial

**Status:** 🟡 Draft

**Time:** ~1.5 hours
**Components:** Camera + Compute
**Physics required:** None (rendered images only)

---

## Before You Begin

### What is Viam?

Viam lets you build robotics applications the way you build other software. Viam abstracts away hardware concerns and services for common tasks to enable you to focus on your core robotics application. Declare your hardware in a config, write control logic against well-defined APIs for everything, push updates through a CLI. Viam is the development workflow you're used to, applied to physical machines.

Viam works with any hardware:

| Category | Examples |
|----------|----------|
| Cameras | Webcams, depth cameras, thermal, CSI |
| Arms | 6-DOF robot arms, collaborative arms |
| Bases | Wheeled, tracked, holonomic, drones |
| Motors | DC, stepper, servo, brushless |
| Sensors | IMU, GPS, ultrasonic, temperature, humidity |
| Grippers | Parallel jaw, vacuum, custom end effectors |
| Boards | Raspberry Pi, Jetson, Orange Pi, ESP32 |
| LiDAR | 2D and 3D scanning |
| Encoders | Rotary, absolute, incremental |
| Gantries | Linear actuators, multi-axis systems |

If your hardware isn't on the list, you can add support with a custom module by implementing the appropriate API.

This tutorial uses the simplest work cell (camera + compute) to teach patterns that apply to *all* Viam applications.

### What You'll Learn

By the end of this tutorial, you'll understand how to:

| Skill | What It Means | Applies To |
|-------|---------------|------------|
| Configure components | Add hardware to a Viam machine | Any sensor, actuator, or peripheral |
| Add services | Attach capabilities like ML inference | Vision, navigation, motion planning |
| Write control logic | Code that reads sensors and makes decisions | Any automation task |
| Deploy code to machines | Run your logic on the machine itself | All production deployments |
| Scale with fragments | Reuse configurations across machines | Any fleet, any size |
| Manage fleets | Monitor, update, and debug remotely | Production operations |
| Build customer apps | Create products on top of Viam | Shipping to your customers |

**These patterns are the same whether you're working with a camera, a robot arm, or a warehouse full of mobile robots.**

## Scenario

You're building a **quality inspection station** for a manufacturing line. Parts move past a camera on a conveyor. Your system must:

1. Detect when a part is present
2. Classify it as PASS or FAIL
3. Log results and trigger alerts on failures
4. Scale to multiple inspection stations
5. Ship as a product your customers can use

---

## What You'll Build

A working inspection system with:

- A camera streaming live images
- An ML model classifying parts as pass/fail
- Business logic that triggers alerts on failures
- A second station added to your fleet
- A dashboard showing inspection results across stations
- A customer-facing web app with your branding

---

## Tutorial Flow

### Part 1: Prototype (~25 min)

**Goal:** Get a working detection pipeline on one simulated camera.

**Skills:** Installing viam-server, connecting a machine to Viam, component configuration, adding services, writing SDK code.

#### 1.1 Launch the Simulation

Click the button below to launch your simulation environment:

[BUTTON: Launch Simulation]

After a few seconds, you'll see a split-screen view:

[SCREENSHOT: Simulation interface showing work cell on left, terminal on right]

**Left panel:** A 3D view of your work cell—a conveyor belt with an overhead camera. Parts will appear here during the tutorial.

**Right panel:** A terminal connected to the Linux machine running this simulation. This is the same terminal you'd use if you SSH'd into a Raspberry Pi or any other device.

> **What you're looking at:** This isn't a sandbox or a toy. It's an actual Linux machine running in the cloud with simulated hardware attached. Everything you do here—installing software, configuring components, writing code—works exactly the same way on real hardware.

#### 1.2 Create a Machine in Viam

Before the simulated machine can talk to Viam, you need to create a machine entry in the Viam app. This is where you'll configure components, view data, and manage your machine.

**Create an account** (if you don't have one):

1. Open [app.viam.com](https://app.viam.com) in a new browser tab
2. Click **Sign Up** and create an account with your email or Google/GitHub

[SCREENSHOT: Viam app sign-up page]

**Create a new machine:**

1. From the Viam app home screen, click **+ Add machine**
2. Give your machine a name like `inspection-station-1`
3. Click **Add machine**

[SCREENSHOT: Add machine dialog with name field]

You'll land on your machine's page. Notice the status indicator shows **Offline**—that's expected. The machine exists in Viam's cloud, but nothing is running on your simulated hardware yet.

**Get the install command:**

1. Click the **Setup** tab
2. You'll see a `curl` command that looks like this:

```bash
curl -fsSL https://app.viam.com/install | sh -s -- --apisecret <your-secret>
```

3. Click the **Copy** button to copy this command

[SCREENSHOT: Setup tab showing the install command with copy button highlighted]

> **Keep this tab open.** You'll paste this command into the simulation terminal in the next step.

This command downloads and installs `viam-server`, then configures it with credentials that link it to this specific machine in your Viam account. Every Viam machine—whether it's a Raspberry Pi in your garage or an industrial robot in a factory—starts the same way.

#### 1.3 Install viam-server

Now you'll install `viam-server` on the simulation machine. This is the software that runs on every Viam-managed device—it connects to the cloud, loads your configuration, and provides APIs for controlling components.

**Run the install command:**

1. Click in the terminal panel on the right side of your simulation
2. Paste the install command you copied from the Viam app (Ctrl+V or Cmd+V)
3. Press Enter

You'll see output as the installer runs:

```
Downloading viam-server...
Installing to /usr/local/bin/viam-server...
Creating configuration directory...
Starting viam-server...
```

[SCREENSHOT: Terminal showing successful viam-server installation]

The installation takes about 30 seconds. When it completes, `viam-server` starts automatically as a background service.

**Verify the connection:**

Switch back to your Viam app browser tab. The status indicator should now show **Online** with a green dot.

[SCREENSHOT: Machine page showing Online status]

This is the moment: the Linux machine you're looking at in the simulation is now connected to Viam's cloud. You can configure it, monitor it, and control it from anywhere in the world.

> **Troubleshooting:**
> - **Still showing Offline?** Wait 10-15 seconds and refresh the page. The connection can take a moment to establish.
> - **Installation failed?** Make sure you copied the entire command, including the `--apisecret` flag and its value.
> - **Permission denied?** The install script should handle this, but if you see permission errors, prefix the command with `sudo`.

This is the same process you'd follow on real hardware. SSH into a Raspberry Pi, run the install command, and it connects to Viam. The only difference here is that your "SSH" is a browser-based terminal.

#### 1.4 Configure the Camera

Your machine is online but empty—it doesn't know about any hardware yet. You'll now add the camera as a *component*.

In Viam, a component is any piece of hardware: cameras, motors, arms, sensors, grippers. You configure components by declaring what they are, and Viam handles the drivers and communication.

**Add a camera component:**

1. In the Viam app, click the **Config** tab
2. Click **+ Add component**
3. For **Type**, select `camera`
4. For **Model**, select `webcam`

   > The simulated camera presents itself as a standard webcam to the operating system—just like a USB camera would on a real machine.

5. Name it `inspection-cam`
6. Click **Create**

[SCREENSHOT: Add component dialog with camera settings]

**Configure the camera source:**

After creating the component, you'll see a configuration panel. The `webcam` model needs to know which video device to use.

1. In the **Attributes** section, click the **video_path** dropdown
2. Select the available video device (typically `/dev/video0` or similar)
3. Click **Save config** in the top right

[SCREENSHOT: Camera configuration panel with video_path selected]

When you save, viam-server automatically reloads and applies the new configuration. You don't need to restart anything—the system picks up changes within seconds.

> **What just happened:** You declared "this machine has a camera called `inspection-cam`" by editing configuration in a web UI. Behind the scenes, viam-server loaded the appropriate driver, connected to the video device, and made the camera available through Viam's camera API. You'd do exactly the same thing for a motor, an arm, or any other component—just select a different type and model.

#### 1.5 View the Camera Feed

Let's verify the camera is working by viewing its live feed.

**Open the Control tab:**

1. Click the **Control** tab at the top of the machine page

The Control tab shows interactive panels for each component. You should see your `inspection-cam` listed.

[SCREENSHOT: Control tab showing inspection-cam component]

**View the live stream:**

1. Find the `inspection-cam` panel
2. Click the **Toggle stream** button (or the expand icon)

You should see a live video feed from the simulated camera—an overhead view of the conveyor/staging area.

[SCREENSHOT: Live camera feed showing the work cell]

**Test the camera:**

Click **Get image** to capture a single frame. The image appears in the panel and can be downloaded.

> **What you're seeing:** This isn't a special debugging view. The Control tab uses the exact same APIs that your code will use. When you click "Get image," Viam calls the camera's `GetImage` method—the same method you'll call from Python or Go in a few minutes.

This pattern applies to all components. Motors have controls for setting velocity. Arms have controls for moving joints. The Control tab lets you interact with hardware before writing any code.

#### 1.6 Add a Vision Service

Now you'll add machine learning to your camera. In Viam, ML capabilities are provided by *services*—higher-level functionality that operates on components.

**Components vs. Services:**
- **Components** are hardware: cameras, motors, arms
- **Services** are capabilities: vision (ML inference), navigation (path planning), motion (arm kinematics)

Services often *use* components. The vision service will use your camera to get images, then run ML inference on them.

**Add the ML model:**

First, you need an ML model. We've provided a pre-trained model for this tutorial that classifies parts as PASS or FAIL.

1. In the Viam app, click the **Config** tab
2. Click **+ Add service**
3. For **Type**, select `mlmodel`
4. For **Model**, select `tflite_cpu`
5. Name it `part-classifier`
6. Click **Create**

[SCREENSHOT: Add service dialog for ML model]

**Configure the model location:**

1. In the `part-classifier` configuration panel, find the **model_path** field
2. Enter: `/path/to/part-classifier.tflite`

   > This model file is pre-installed in the simulation. On real hardware, you'd deploy your own trained model.

3. Click **Save config**

[SCREENSHOT: ML model configuration with model_path]

**Add the vision service:**

Now create a vision service that uses this model to analyze images.

1. Click **+ Add service** again
2. For **Type**, select `vision`
3. For **Model**, select `mlmodel`
4. Name it `part-detector`
5. Click **Create**

**Link the vision service to your model:**

1. In the `part-detector` configuration panel, find the **mlmodel_name** field
2. Enter: `part-classifier` (the name of the ML model service you just created)
3. Click **Save config**

[SCREENSHOT: Vision service configuration linked to ML model]

**Test the vision service:**

1. Go to the **Control** tab
2. Find the `part-detector` panel
3. Select `inspection-cam` as the camera source
4. Click **Get detections**

You should see the camera image with detection results—bounding boxes around detected parts with labels (PASS or FAIL) and confidence scores.

[SCREENSHOT: Vision service showing detection results with bounding boxes]

> **What you've built:** A complete ML inference pipeline. The vision service grabs an image from the camera, runs it through the TensorFlow Lite model, and returns structured detection results. This same pattern works for any ML task—object detection, classification, segmentation—you just swap the model.

#### 1.7 Write Detection Logic

So far you've configured everything through the Viam app. Now you'll write code that connects to your machine and runs detections programmatically.

Viam provides SDKs for Python, Go, TypeScript, C++, and Flutter. We'll use Python and Go here—choose whichever you're more comfortable with.

**Get your connection credentials:**

1. In the Viam app, click the **Code sample** tab
2. Select your language (Python or Go)
3. Copy the connection code snippet

This snippet contains your machine's address and API key. Keep these credentials secure—they grant full access to your machine.

[SCREENSHOT: Code sample tab showing connection snippet]

**Set up your development environment:**

{{< tabs >}}
{{% tab name="Python" %}}

Create a new directory and set up a virtual environment:

```bash
mkdir inspection-logic && cd inspection-logic
python3 -m venv venv
source venv/bin/activate
pip install viam-sdk
```

{{% /tab %}}
{{% tab name="Go" %}}

Create a new Go module:

```bash
mkdir inspection-logic && cd inspection-logic
go mod init inspection-logic
go get go.viam.com/rdk/robot/client
```

{{% /tab %}}
{{< /tabs >}}

**Write the detection script:**

Create a file called `inspector.py` (or `inspector.go`) with the following code:

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.services.vision import VisionClient

async def connect():
    opts = RobotClient.Options.with_api_key(
        # Replace with your credentials from the Code sample tab
        api_key='YOUR_API_KEY',
        api_key_id='YOUR_API_KEY_ID'
    )
    return await RobotClient.at_address('YOUR_MACHINE_ADDRESS', opts)

async def main():
    robot = await connect()
    print("Connected to machine")

    # Get the vision service
    detector = VisionClient.from_robot(robot, "part-detector")

    # Run detection on the camera
    detections = await detector.get_detections_from_camera("inspection-cam")

    # Process results
    for d in detections:
        label = d.class_name
        confidence = d.confidence
        print(f"Detected: {label} ({confidence:.1%})")

        if label == "FAIL":
            print("⚠️  DEFECTIVE PART DETECTED")

    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:

```bash
python inspector.py
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"
    "fmt"

    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/services/vision"
    "go.viam.com/utils/rpc"
)

func main() {
    logger := logging.NewLogger("inspector")
    ctx := context.Background()

    // Replace with your credentials from the Code sample tab
    robot, err := client.New(
        ctx,
        "YOUR_MACHINE_ADDRESS",
        logger,
        client.WithDialOptions(rpc.WithEntityCredentials(
            "YOUR_API_KEY_ID",
            rpc.Credentials{
                Type:    rpc.CredentialsTypeAPIKey,
                Payload: "YOUR_API_KEY",
            },
        )),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(ctx)
    fmt.Println("Connected to machine")

    // Get the vision service
    detector, err := vision.FromRobot(robot, "part-detector")
    if err != nil {
        logger.Fatal(err)
    }

    // Run detection on the camera
    detections, err := detector.DetectionsFromCamera(ctx, "inspection-cam", nil)
    if err != nil {
        logger.Fatal(err)
    }

    // Process results
    for _, d := range detections {
        label := d.Label()
        confidence := d.Score()
        fmt.Printf("Detected: %s (%.1f%%)\n", label, confidence*100)

        if label == "FAIL" {
            fmt.Println("⚠️  DEFECTIVE PART DETECTED")
        }
    }
}
```

Run it:

```bash
go run inspector.go
```

{{% /tab %}}
{{< /tabs >}}

**What the code does:**

1. **Connects to your machine** using the API credentials. This works from anywhere—your laptop, a server, another machine.
2. **Gets the vision service** by name (`part-detector`).
3. **Runs detection** using `get_detections_from_camera`, which captures an image and runs inference in one call.
4. **Processes results** by iterating through detections, each with a label and confidence score.

> **This is the pattern.** Whether you're reading a temperature sensor, moving a robot arm, or running ML inference, the flow is the same: connect to the machine, get the component or service by name, call its methods. The APIs are consistent across all hardware.

**Checkpoint:** You've installed viam-server, connected a machine to Viam, configured a camera, added ML, and written SDK code. This is the complete prototype workflow for any Viam project.

---

### Part 2: Deploy (~10 min)

**Goal:** Make your detection logic run continuously on the machine.

**Skills:** Deploying code to run on machines, event-driven actions.

#### 2.1 Create a Process

Right now, your detection script runs on your laptop. When you close the terminal, it stops. For production, you want the code running *on the machine itself*—so it keeps working even when you're not connected.

In Viam, a *process* is code that runs on the machine as part of its configuration. When viam-server starts, it starts your processes. When the machine reboots, your code automatically restarts.

**Modify your script for continuous operation:**

First, update your script to run in a loop:

{{< tabs >}}
{{% tab name="Python" %}}

```python
import asyncio
import time
from viam.robot.client import RobotClient
from viam.services.vision import VisionClient

async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key='YOUR_API_KEY',
        api_key_id='YOUR_API_KEY_ID'
    )
    return await RobotClient.at_address('YOUR_MACHINE_ADDRESS', opts)

async def main():
    robot = await connect()
    print("Inspector started")

    detector = VisionClient.from_robot(robot, "part-detector")

    while True:
        detections = await detector.get_detections_from_camera("inspection-cam")

        for d in detections:
            if d.class_name == "FAIL":
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] FAIL detected (confidence: {d.confidence:.1%})")
                # Alert logic will go here

        await asyncio.sleep(1)  # Check every second

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
package main

import (
    "context"
    "fmt"
    "time"

    "go.viam.com/rdk/robot/client"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/services/vision"
    "go.viam.com/utils/rpc"
)

func main() {
    logger := logging.NewLogger("inspector")
    ctx := context.Background()

    robot, err := client.New(
        ctx,
        "YOUR_MACHINE_ADDRESS",
        logger,
        client.WithDialOptions(rpc.WithEntityCredentials(
            "YOUR_API_KEY_ID",
            rpc.Credentials{
                Type:    rpc.CredentialsTypeAPIKey,
                Payload: "YOUR_API_KEY",
            },
        )),
    )
    if err != nil {
        logger.Fatal(err)
    }
    defer robot.Close(ctx)
    fmt.Println("Inspector started")

    detector, err := vision.FromRobot(robot, "part-detector")
    if err != nil {
        logger.Fatal(err)
    }

    for {
        detections, err := detector.DetectionsFromCamera(ctx, "inspection-cam", nil)
        if err != nil {
            logger.Error(err)
            time.Sleep(time.Second)
            continue
        }

        for _, d := range detections {
            if d.Label() == "FAIL" {
                timestamp := time.Now().Format("2006-01-02 15:04:05")
                fmt.Printf("[%s] FAIL detected (confidence: %.1f%%)\n",
                    timestamp, d.Score()*100)
                // Alert logic will go here
            }
        }

        time.Sleep(time.Second) // Check every second
    }
}
```

{{% /tab %}}
{{< /tabs >}}

**Deploy the script to the machine:**

1. In the simulation terminal, create a directory for your code:
   ```bash
   mkdir -p /home/viam/inspector
   ```

2. Copy your script to the machine. In this simulation, you can paste the code directly:
   ```bash
   nano /home/viam/inspector/inspector.py
   ```
   Paste your code, save (Ctrl+O, Enter, Ctrl+X).

   > On real hardware, you'd use `scp`, `rsync`, or a deployment tool to copy files.

**Configure the process in Viam:**

1. In the Viam app, go to **Config** → **Processes**
2. Click **+ Add process**
3. Configure:
   - **Name:** `inspector`
   - **Executable:** `python3` (or `go run` for Go)
   - **Arguments:** `/home/viam/inspector/inspector.py`
   - **Working directory:** `/home/viam/inspector`
4. Click **Save config**

[SCREENSHOT: Process configuration panel]

The process starts immediately. Check the **Logs** tab to see your inspector's output.

[SCREENSHOT: Logs showing inspector output]

> **What changed:** Your code now runs on the machine, managed by viam-server. Close your browser, turn off your laptop—the inspector keeps running. This is how you deploy code to any Viam machine, from a single sensor node to a factory full of robots.

#### 2.2 Add Alerting

Detection is useful, but you need to know when failures happen. Let's add alerting so you're notified immediately when a defective part is detected.

**Add logging with the data service:**

The simplest form of alerting is logging events to Viam's cloud, where you can query them later or set up notifications.

Update your script to log failures:

{{< tabs >}}
{{% tab name="Python" %}}

```python
# Add to your imports
from viam.services.data import DataClient

# In your detection loop, after detecting a FAIL:
if d.class_name == "FAIL":
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] FAIL detected")

    # Log to Viam's data service
    data_client = DataClient.from_robot(robot)
    await data_client.tabular_data_capture(
        component_name="inspector",
        method_name="detection",
        data={"result": "FAIL", "confidence": d.confidence}
    )
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
// After detecting a FAIL:
if d.Label() == "FAIL" {
    timestamp := time.Now().Format("2006-01-02 15:04:05")
    fmt.Printf("[%s] FAIL detected\n", timestamp)

    // Log the detection - events appear in Viam's data tab
    logger.Infow("Defective part detected",
        "result", "FAIL",
        "confidence", d.Score(),
        "timestamp", timestamp,
    )
}
```

{{% /tab %}}
{{< /tabs >}}

**View alerts in the Viam app:**

1. Go to the **Data** tab in your organization
2. Filter by your machine
3. See logged detection events

[SCREENSHOT: Data tab showing logged FAIL events]

> **Going further:** In production, you'd extend this pattern to send webhooks, trigger emails, or integrate with monitoring systems like PagerDuty or Slack. The logged data can also feed dashboards—which you'll build in Part 6.

**Checkpoint:** Detection runs automatically. Your code is deployed to the machine, not just running on your laptop.

---

### Part 3: Scale (~10 min)

**Goal:** Add a second inspection station.

**Skills:** Configuration reuse with fragments, fleet basics.

#### 3.1 Create a Fragment

You have one working inspection station. Now imagine you need 10 more—or 100. Manually copying configuration to each machine would be tedious and error-prone.

Viam solves this with *fragments*: reusable configuration blocks that can be applied to any machine. Think of a fragment as a template. Define your camera, vision service, and inspector process once, then apply that template to as many machines as you need.

**Create a fragment from your configuration:**

1. In the Viam app, click **Fragments** in the left sidebar
2. Click **+ Create fragment**
3. Name it `inspection-station`
4. Click **Create**

[SCREENSHOT: Create fragment dialog]

**Add your configuration to the fragment:**

Now you'll copy the configuration from your machine into the fragment.

1. Go back to your `inspection-station-1` machine
2. Click the **Config** tab, then click the **JSON** toggle (top right) to see the raw configuration
3. Copy the entire JSON configuration

[SCREENSHOT: JSON config view with copy button]

4. Return to your fragment
5. Paste the configuration into the fragment editor
6. Click **Save**

[SCREENSHOT: Fragment editor with pasted configuration]

Your fragment now contains everything: the camera component, ML model service, vision service, and inspector process. Any machine with this fragment applied will have this exact setup.

> **Fragments are powerful.** When you update a fragment, every machine using it receives the update automatically. Change a detection threshold once, and 100 stations update. This is how you manage configuration at scale.

#### 3.2 Add a Second Machine

Let's spin up a second inspection station and apply the fragment.

**Launch a second simulation:**

Click the button below to launch a second work cell:

[BUTTON: Launch Second Station]

This opens another browser tab with an identical simulation environment—conveyor, camera, the works. But this machine doesn't have any Viam configuration yet.

[SCREENSHOT: Second simulation tab]

**Create the machine and install viam-server:**

Follow the same steps from Part 1:

1. In the Viam app, click **+ Add machine**
2. Name it `inspection-station-2`
3. Copy the install command from the **Setup** tab
4. Paste and run it in the second simulation's terminal
5. Wait for the machine to come online

**Apply the fragment:**

Instead of manually configuring everything, you'll apply your fragment.

1. On `inspection-station-2`, go to the **Config** tab
2. Click **+ Add fragment**
3. Select `inspection-station` from the dropdown
4. Click **Add**
5. Click **Save config**

[SCREENSHOT: Adding fragment to machine]

Within seconds, the machine reloads its configuration. It now has the camera, vision service, and inspector process—all from the fragment.

**Verify it works:**

1. Go to the **Control** tab
2. Check the camera feed
3. Run a detection

Both stations are now running identical inspection logic.

[SCREENSHOT: Fleet view showing both machines online]

**Checkpoint:** Two stations running identical inspection logic. You didn't copy-paste configuration—you used a fragment.

---

### Part 4: Fleet (~10 min)

**Goal:** Manage both stations as a fleet.

**Skills:** Fleet monitoring, pushing updates.

#### 4.1 View Your Fleet

With multiple machines running, you need a way to monitor them together—not clicking through each one individually.

**Open the fleet view:**

1. In the Viam app, click **Fleet** in the left sidebar (or **Machines** in some views)
2. You'll see a list of all machines in your organization

[SCREENSHOT: Fleet view showing both inspection stations]

The fleet view shows:
- **Status:** Online/offline for each machine
- **Last seen:** When each machine last connected
- **Location:** If you've tagged machines by location

**Check machine health:**

Click on either machine to see its details:
- Component status (is the camera responding?)
- Recent logs
- Resource usage (CPU, memory)

[SCREENSHOT: Machine detail view with status indicators]

**View aggregated data:**

1. Click the **Data** tab at the organization level
2. You'll see data from *all* machines combined
3. Filter by machine, time range, or data type

You can query: "How many FAIL detections across all stations in the last hour?" This is the foundation for dashboards and analytics.

[SCREENSHOT: Data tab showing aggregated events from both machines]

> **Two machines or two hundred:** This same view works regardless of fleet size. As you add machines, they appear here automatically. The fleet view is your single pane of glass for operations.

#### 4.2 Push a Configuration Update

One of the most powerful aspects of fragments is pushing updates. Let's change a setting and watch it propagate.

**Modify the fragment:**

Suppose you want to adjust how often the inspector runs. Instead of checking every 1 second, you want every 2 seconds.

1. Go to **Fragments** in the left sidebar
2. Open your `inspection-station` fragment
3. Find the inspector process configuration
4. Change the relevant setting (or modify the script's sleep interval)
5. Click **Save**

[SCREENSHOT: Editing fragment configuration]

**Watch the update propagate:**

1. Go back to the **Fleet** view
2. Watch both machines briefly show as "Configuring" or "Restarting"
3. Within 30 seconds, both machines are running the updated configuration

[SCREENSHOT: Machines showing configuration update in progress]

You didn't SSH into either machine. You didn't run any deployment commands. You changed the fragment, and Viam pushed the update automatically.

**Verify the change:**

1. Click into `inspection-station-1`
2. Check the **Logs** tab
3. Confirm the inspector is now running at the new interval

[SCREENSHOT: Logs showing updated inspection interval]

> **This is fleet management.** Need to update an ML model across 50 machines? Update the fragment. Need to roll back a bad change? Revert the fragment. The machines sync automatically. This same pattern scales from 2 machines to 2,000.

**Checkpoint:** You can manage multiple machines from one place. Configuration changes propagate automatically.

---

### Part 5: Maintain (~10 min)

**Goal:** Debug and fix an issue.

**Skills:** Remote diagnostics, log analysis, incident response.

#### 5.1 Simulate a Problem

In production, things break. Cameras get dirty, cables loosen, lighting changes. Let's simulate a problem and practice debugging.

**Trigger the issue:**

Click the button below to simulate camera degradation on `inspection-station-1`:

[BUTTON: Degrade Camera]

This simulates what happens when a camera lens gets dirty or lighting conditions change—the image becomes noisy and blurry, making ML detection unreliable.

[SCREENSHOT: Simulation showing degraded camera view]

**Notice the anomaly:**

Within a few seconds, you should see signs of trouble:

1. **Logs:** The inspector might report unusual confidence scores or errors
2. **Data:** Detection results become inconsistent
3. **Alerts:** If you configured alerting, you might see unexpected patterns

In a real deployment, this is how you'd first learn about a problem—through monitoring data, not a phone call from the factory floor.

#### 5.2 Diagnose Remotely

Now let's investigate without physical access to the machine.

**Check the logs:**

1. In the Viam app, go to `inspection-station-1`
2. Click the **Logs** tab
3. Look for error messages or unusual output

[SCREENSHOT: Logs showing detection anomalies]

You might see:
- Lower confidence scores than usual
- Failed detections (no objects found when there should be)
- Timeout errors if the camera is struggling

**View the camera feed:**

1. Go to the **Control** tab
2. Open the `inspection-cam` stream
3. Look at the image quality

[SCREENSHOT: Degraded camera feed in Control tab]

The issue is immediately visible: the camera feed is noisy or blurred. You've identified the root cause without leaving your desk.

**Compare to the healthy station:**

1. Open `inspection-station-2` in another tab
2. View its camera feed
3. Confirm the image quality is normal

This comparison confirms the problem is isolated to station 1, not a systemic issue.

> **Remote diagnostics in practice:** You just debugged a hardware issue without physical access. In a real deployment, the machine could be in another building, another city, or another country. Viam gives you the same visibility regardless of location.

#### 5.3 Fix and Verify

Let's fix the issue and confirm the system recovers.

**Reset the camera:**

In a real scenario, you'd dispatch maintenance to clean or replace the camera. For this simulation, click the reset button:

[BUTTON: Reset Camera]

This restores the camera to normal operation.

**Verify the fix:**

1. Go back to `inspection-station-1`
2. Check the **Control** tab—the camera feed should be clear
3. Check the **Logs** tab—detection should be working normally
4. Wait for a few inspection cycles to confirm consistent results

[SCREENSHOT: Restored camera feed and normal logs]

**Document the incident:**

In production, you'd want to track this:
- When the issue started
- How it was detected
- What caused it
- How it was resolved

The data captured during the incident (the anomalous detections, the degraded images) is already in Viam's data service—you can query it later for incident reports or trend analysis.

**Checkpoint:** You've diagnosed and fixed a production issue remotely.

---

### Part 6: Productize (~15 min)

**Goal:** Build a customer-facing product.

**Skills:** Building apps with Viam SDKs, white-label deployment.

#### 6.1 Create a Customer Dashboard

You've built a working system—but right now, only you can see it through the Viam app. Your customers need their own interface, with your branding, showing only what they need to see.

Viam's SDKs let you build custom applications that connect to machines and query data. Let's create a simple dashboard that shows inspection results.

**Set up a TypeScript project:**

```bash
mkdir inspection-dashboard && cd inspection-dashboard
npm init -y
npm install @viamrobotics/sdk
```

**Create the dashboard:**

Create a file called `dashboard.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Inspection Dashboard</title>
    <style>
        body { font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-card { background: #f5f5f5; padding: 20px; border-radius: 8px; flex: 1; }
        .stat-value { font-size: 48px; font-weight: bold; }
        .pass { color: #22c55e; }
        .fail { color: #ef4444; }
        .station { background: #fff; border: 1px solid #e5e5e5; padding: 15px; margin: 10px 0; border-radius: 8px; }
        .online { color: #22c55e; }
        .offline { color: #ef4444; }
    </style>
</head>
<body>
    <h1>Quality Inspection Dashboard</h1>

    <div class="stats">
        <div class="stat-card">
            <div>Today's Inspections</div>
            <div class="stat-value" id="total-count">--</div>
        </div>
        <div class="stat-card">
            <div>Pass Rate</div>
            <div class="stat-value pass" id="pass-rate">--%</div>
        </div>
        <div class="stat-card">
            <div>Failures</div>
            <div class="stat-value fail" id="fail-count">--</div>
        </div>
    </div>

    <h2>Stations</h2>
    <div id="stations"></div>

    <script type="module">
        import { createRobotClient, DataClient } from '@viamrobotics/sdk';

        // Replace with your credentials
        const API_KEY = 'YOUR_API_KEY';
        const API_KEY_ID = 'YOUR_API_KEY_ID';

        async function updateDashboard() {
            // Connect to Viam's data service
            const dataClient = await DataClient.createFromCredentials(
                API_KEY_ID,
                API_KEY
            );

            // Query inspection results from the last 24 hours
            const results = await dataClient.tabularDataByFilter({
                filter: {
                    componentName: 'inspector',
                    interval: {
                        start: new Date(Date.now() - 24 * 60 * 60 * 1000),
                        end: new Date()
                    }
                }
            });

            // Calculate stats
            const total = results.length;
            const fails = results.filter(r => r.data.result === 'FAIL').length;
            const passRate = total > 0 ? ((total - fails) / total * 100).toFixed(1) : 0;

            // Update UI
            document.getElementById('total-count').textContent = total;
            document.getElementById('fail-count').textContent = fails;
            document.getElementById('pass-rate').textContent = `${passRate}%`;
        }

        // Update every 5 seconds
        updateDashboard();
        setInterval(updateDashboard, 5000);
    </script>
</body>
</html>
```

**Run the dashboard:**

Open `dashboard.html` in your browser (or serve it with a local web server). You'll see live inspection statistics pulled from Viam's data service.

[SCREENSHOT: Customer dashboard showing inspection stats]

> **This is your product.** The dashboard has no Viam branding—it's your interface, powered by Viam's APIs. You can add your logo, customize the design, add features. The same APIs that power this simple page can power a full React application, a mobile app, or an enterprise dashboard.

#### 6.2 Set Up White-Label Auth

Your customers shouldn't log into Viam—they should log into *your* product. Viam supports white-label authentication so you can use your own identity provider.

**Configure custom authentication:**

1. In the Viam app, go to **Organization Settings**
2. Find the **Custom Authentication** section
3. Configure your identity provider (OAuth/OIDC)

[SCREENSHOT: Custom auth configuration]

With this configured:
- Your customers log in through your login page
- They see only the machines you've given them access to
- Your branding, your domain, your experience

> **Note:** Full OAuth configuration is beyond the scope of this tutorial. See the [Authentication documentation](../reference/authentication.md) for detailed setup instructions.

**Create customer accounts:**

You can also create customer accounts directly:

1. Go to **Organization Settings** → **Members**
2. Invite your customer with limited permissions
3. They see only their machines, not your entire fleet

This lets you ship a product where each customer sees only their own inspection stations.

#### 6.3 (Optional) Configure Billing

If you're selling inspection-as-a-service, you need to bill customers. Viam can meter usage and integrate with your billing system.

**Usage metering:**

Viam tracks:
- Number of machines
- Data captured and stored
- API calls
- ML inference operations

You can query this data to build usage-based billing:

```typescript
// Example: Get machine usage for billing
const usage = await dataClient.getUsageByOrganization({
    organizationId: 'YOUR_ORG_ID',
    startTime: billingPeriodStart,
    endTime: billingPeriodEnd
});

// Calculate charges based on your pricing model
const machineCharges = usage.machineCount * PRICE_PER_MACHINE;
const dataCharges = usage.dataGB * PRICE_PER_GB;
```

**Billing integration:**

For production billing, you'd integrate Viam's usage data with your billing system (Stripe, your own invoicing, etc.). The data is available through APIs, so you have full flexibility in how you present and charge for usage.

> **Business model flexibility:** Charge per machine, per inspection, per GB of data, or a flat subscription. Viam provides the metering data; you decide the pricing.

**Checkpoint:** You have a customer-ready product. You've gone from prototype to shippable product in one tutorial.

---

## What's Next

### You Can Now Build

With the skills from this tutorial, you could build:

- **Inventory monitoring** — Camera watches shelves, alerts when stock is low
- **Security system** — Detect people or vehicles, log events, send alerts
- **Wildlife camera** — Classify animals, sync photos to cloud, monitor remotely
- **Equipment monitoring** — Watch gauges or indicator lights, alert on anomalies

These all use the same patterns: configure components, add services, write logic, deploy, scale with fragments.

### Continue Learning

**Try another tutorial:**
- [Mobile Base](./mobile-base.md) — Add navigation and movement
- [Arm + Vision](./arm-vision.md) — Add manipulation

**Go deeper with blocks:**
- [Track Objects Across Frames](../build/perception/track-objects.md) — Add persistence to detections
- [Capture and Sync Data](../build/foundation/capture-sync.md) — Build datasets from your cameras
- [Monitor Over Time](../build/stationary-vision/monitor-over-time.md) — Detect anomalies and trends

**Build your own project:**
- You have all the foundational skills
- Pick hardware (or stay in simulation)
- Use the blocks as reference when you get stuck

---

## Simulation Requirements

### Work Cell Elements

| Element | Description |
|---------|-------------|
| Conveyor/staging area | Surface where parts appear |
| Camera | Overhead RGB camera (640x480, 30fps) |
| Sample parts | Mix of "good" and "defective" items |
| Lighting | Consistent industrial lighting |

### Viam Components

| Component | Type | Notes |
|-----------|------|-------|
| `inspection-cam` | camera | Gazebo RGB camera |
| `part-detector` | vision | ML model service |
| `inspector` | process | Detection + alerting script |

### Simulated Events

| Event | Trigger | Purpose |
|-------|---------|---------|
| Part appears | Timer or user action | New item to inspect |
| Camera degradation | Part 5 trigger | Create debugging scenario |

---

## Blocks Used

From [block-definitions.md](../planning/block-definitions.md):

**Foundation:**
- Connect to Cloud
- Add a Camera
- Start Writing Code

**Perception:**
- Add Computer Vision
- Detect Objects (2D)

**Stationary Vision:**
- Trigger on Detection
- Inspect for Defects

**Fleet/Deployment:**
- Configure Multiple Machines
- Monitor a Fleet
- Push Updates

**Productize:**
- Build a Customer Dashboard (TypeScript SDK)
- Set Up White-Label Auth
- Configure Billing

---

## Author Guidance

### UI Rough Edges to Address

Document and provide explicit guidance for:

- [ ] Account creation flow
- [ ] Finding the camera panel in the app
- [ ] Vision service configuration steps
- [ ] Process configuration location
- [ ] Fragment creation UI
- [ ] Fleet view navigation

### Key Teaching Moments

At each step, explicitly connect to transferable skills:

- "This is how you configure *any* component"
- "This pattern works for *any* sensor"
- "You'd do the same thing with a robot arm"

### Anti-Patterns to Avoid

- Don't let users think Viam is "just for cameras"
- Don't let steps feel like magic—explain what's happening
- Don't assume users will read linked docs—include essential context inline

---

## Open Questions

1. **Part appearance:** Timer vs. manual trigger? Timer feels realistic; manual gives control.

2. **ML model:** Pre-trained (provided) vs. walk through training? Pre-trained keeps focus on platform skills.

3. **Alert mechanism:** What works without user setup? In-app notification? Logged event?

4. **Second station:** Identical or slightly different? Identical is simpler; different shows fragment flexibility.

5. **Dashboard complexity:** How much web dev do we include? Keep minimal—point is Viam APIs, not teaching React.
