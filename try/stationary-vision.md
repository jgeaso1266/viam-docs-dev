# Stationary Vision Tutorial

**Status:** 🔴 Outline

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
- Open the browser-based simulation
- See the work cell: conveyor, camera, sample parts
- Understand what you're working with—this is a Linux machine with hardware attached

> **Author note:** Provide clear visual of what the simulation looks like. Users need to orient themselves. Emphasize this is a real (simulated) machine, not a sandbox.

#### 1.2 Create a Machine in Viam
- Create a Viam account (if needed)
- Create a new machine in the Viam app
- Copy the install command from the Setup tab
- **Transferable skill:** This is the starting point for *any* Viam machine—real or simulated

> **Author note:** Walk through the app UI carefully. Screenshots essential. The Setup tab and install command are the key moments.

#### 1.3 Install viam-server
- Open the web terminal (or SSH into the simulation machine)
- Paste and run the install command
- Watch viam-server install and start
- See the machine come online in the Viam app
- **Transferable skill:** This is exactly how you'd set up a Raspberry Pi, Jetson, or any Linux machine

> **Author note:** This is the "aha" moment—the machine they're looking at in the browser connects to the cloud. Make this connection explicit. Troubleshoot common issues (permissions, network).

#### 1.4 Configure the Camera
- Machine is online but has no components yet
- Add a camera component in the Viam app
- Select the appropriate model for the simulated camera
- Save config—viam-server automatically applies it
- **Transferable skill:** This is how you add *any* component—cameras, motors, arms, sensors

> **Author note:** Emphasize the declarative config model: you declare what's connected, Viam handles the drivers.

#### 1.5 View the Camera Feed
- Find the camera component in the Control tab
- Open the live stream
- Take a snapshot
- **Transferable skill:** This is how you view *any* camera in Viam—webcam, industrial camera, depth camera

> **Author note:** The Control tab may not be obvious. Provide explicit guidance.

#### 1.6 Add a Vision Service
- Configure an ML model (pre-trained, provided for this tutorial)
- Run detection on your camera feed
- See bounding boxes and classifications
- **Transferable skill:** This is how you add ML to *any* Viam machine

> **Author note:** Vision service configuration has multiple steps. Break down carefully. Note that users can train their own models later (link to ML docs), but we're using pre-trained here to stay focused.

#### 1.7 Write Detection Logic
- Connect to your machine via Python or Go SDK
- Get camera images programmatically
- Run detections and print results
- Filter for "FAIL" classifications
- **Transferable skill:** This is how you write control logic for *any* Viam component

> **Author note:** Provide complete, working code. Both Python and Go. Users should be able to copy-paste and run. Explain what each section does.

**Checkpoint:** You've installed viam-server, connected a machine to Viam, configured a camera, added ML, and written SDK code. This is the complete prototype workflow for any Viam project.

---

### Part 2: Deploy (~10 min)

**Goal:** Make your detection logic run continuously on the machine.

**Skills:** Deploying code to run on machines, event-driven actions.

#### 2.1 Create a Process
- Wrap your detection script as a Viam process
- Configure it to run on machine startup
- See it running in the Viam app
- **Transferable skill:** This is how you deploy *any* code to run on a Viam machine

> **Author note:** Process configuration can be confusing. Show exactly where this lives in the config. Explain the difference between running code on your laptop vs. on the machine.

#### 2.2 Add Alerting
- Trigger an action when a FAIL is detected
- See the alert arrive
- **Transferable skill:** Event-driven actions work the same way across all Viam applications

> **Author note:** Need to decide on alert mechanism that works without user setup (in-app notification? logged event?). Whatever we choose, explain how this pattern extends to webhooks, emails, etc. in production.

**Checkpoint:** Detection runs automatically. Your code is deployed to the machine, not just running on your laptop.

---

### Part 3: Scale (~10 min)

**Goal:** Add a second inspection station.

**Skills:** Configuration reuse with fragments, fleet basics.

#### 3.1 Create a Fragment
- Extract your camera + vision + process config into a fragment
- Understand what a fragment is: reusable configuration
- **Transferable skill:** Fragments are how you manage configuration across *any* fleet

> **Author note:** Fragments are a key Viam concept but can be abstract. Use concrete analogy: "A fragment is like a template. Instead of configuring each machine from scratch, you apply the template."

#### 3.2 Add a Second Machine
- Launch a second simulated station
- Apply the fragment
- See both machines in your organization
- **Transferable skill:** This is how you scale from 1 to 1,000 machines

**Checkpoint:** Two stations running identical inspection logic. You didn't copy-paste configuration—you used a fragment.

---

### Part 4: Fleet (~10 min)

**Goal:** Manage both stations as a fleet.

**Skills:** Fleet monitoring, pushing updates.

#### 4.1 View Your Fleet
- See both machines' status in the Viam app
- View aggregated data across machines
- Compare pass/fail rates between stations
- **Transferable skill:** Fleet monitoring works the same whether you have 2 machines or 200

> **Author note:** Show the fleet view clearly. If there are UI rough edges here, document workarounds.

#### 4.2 Push a Configuration Update
- Modify the fragment (e.g., adjust detection threshold)
- See it propagate to both machines
- **Transferable skill:** This is how you update *any* fleet—change the fragment, machines sync automatically

**Checkpoint:** You can manage multiple machines from one place. Configuration changes propagate automatically.

---

### Part 5: Maintain (~10 min)

**Goal:** Debug and fix an issue.

**Skills:** Remote diagnostics, log analysis, incident response.

#### 5.1 Simulate a Problem
- One camera "degrades" (simulated noise/blur)
- Detection accuracy drops
- Notice the anomaly in your fleet view or alerts

#### 5.2 Diagnose Remotely
- Check logs for the affected machine
- View the camera feed to see the degradation
- Identify root cause—without physical access to the machine
- **Transferable skill:** Remote diagnostics work the same for any Viam machine, anywhere in the world

#### 5.3 Fix and Verify
- "Replace" the camera (reset simulation)
- Verify detection accuracy recovers
- **Transferable skill:** The debug cycle is the same in production

**Checkpoint:** You've diagnosed and fixed a production issue remotely.

---

### Part 6: Productize (~15 min)

**Goal:** Build a customer-facing product.

**Skills:** Building apps with Viam SDKs, white-label deployment.

#### 6.1 Create a Customer Dashboard
- Use the TypeScript SDK to build a simple web page
- Display live pass/fail counts from your fleet
- Show recent inspection images
- **Transferable skill:** The SDKs let you build *any* customer-facing application

> **Author note:** Provide working starter code. Keep the dashboard simple—the point is showing that Viam provides the APIs, not teaching web development.

#### 6.2 Set Up White-Label Auth
- Configure authentication with your branding
- Your customer logs in without seeing Viam
- **Transferable skill:** This is how you ship products to *your* customers, not Viam's

#### 6.3 (Optional) Configure Billing
- Set up per-machine or per-inspection pricing
- See how Viam handles metering and invoicing

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
