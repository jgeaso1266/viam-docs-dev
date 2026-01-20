# Stationary Vision Tutorial

**Status:** 🟡 Draft

**Time:** ~75 minutes
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
| Configure automation | Set up data capture, triggers, and alerts | Production monitoring |
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

## Tutorial Parts

| Part | Time | What You'll Do |
|------|------|----------------|
| [Part 1: Vision Pipeline](./part1.md) | ~15 min | Set up camera, ML model, and vision service |
| [Part 2: Data Capture](./part2.md) | ~15 min | Configure automatic data sync and alerts |
| [Part 3: Control Logic](./part3.md) | ~25 min | Write inspection module, deploy to machine |
| [Part 4: Scale](./part4.md) | ~10 min | Create fragment, add second machine |
| [Part 5: Productize](./part5.md) | ~10 min | Build dashboard, white-label auth |

<details>
<summary><strong>Full Section Outline</strong></summary>

**[Part 1: Vision Pipeline](./part1.md)** (~15 min)
- [1.1 Launch the Simulation](./part1.md#11-launch-the-simulation)
- [1.2 Create a Machine in Viam](./part1.md#12-create-a-machine-in-viam)
- [1.3 Install viam-server](./part1.md#13-install-viam-server)
- [1.4 Configure the Camera](./part1.md#14-configure-the-camera)
- [1.5 Test the Camera](./part1.md#15-test-the-camera)
- [1.6 Add a Vision Service](./part1.md#16-add-a-vision-service)

**[Part 2: Data Capture](./part2.md)** (~15 min)
- [2.1 Configure Data Capture](./part2.md#21-configure-data-capture)
- [2.2 Add Machine Health Alert](./part2.md#22-add-machine-health-alert)
- [2.3 View and Query Data](./part2.md#23-view-and-query-data)
- [2.4 Summary](./part2.md#24-summary)

**[Part 3: Control Logic](./part3.md)** (~30 min)
- [3.1 Set Up Your Project](./part3.md#31-set-up-your-project)
- [3.2 Build the Inspector](./part3.md#32-build-the-inspector)
- [3.3 Write the Development CLI](./part3.md#33-write-the-development-cli)
- [3.4 Configure the Rejector](./part3.md#34-configure-the-rejector)
- [3.5 Test the Inspector](./part3.md#35-test-the-inspector)
- [3.6 Deploy as a Module](./part3.md#36-deploy-as-a-module)
- [3.7 Summary](./part3.md#37-summary)

**[Part 4: Scale](./part4.md)** (~10 min)
- [4.1 Create a Fragment](./part4.md#41-create-a-fragment)
- [4.2 Parameterize Machine-Specific Values](./part4.md#42-parameterize-machine-specific-values)
- [4.3 Add a Second Machine](./part4.md#43-add-a-second-machine)
- [4.4 Fleet Management Capabilities](./part4.md#44-fleet-management-capabilities)

**[Part 5: Productize](./part5.md)** (~15 min)
- [5.1 Create a Dashboard](./part5.md#51-create-a-dashboard)
- [5.2 Set Up White-Label Auth](./part5.md#52-set-up-white-label-auth)
- [5.3 (Optional) Configure Billing](./part5.md#53-optional-configure-billing)

</details>

---

## Get Started

**[Begin Part 1: Vision Pipeline →](./part1.md)**

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
- [Mobile Base](../mobile-base.md) — Add navigation and movement
- [Arm + Vision](../arm-vision.md) — Add manipulation

**Go deeper with blocks:**
- [Track Objects Across Frames](../../build/perception/track-objects.md) — Add persistence to detections
- [Capture and Sync Data](../../build/foundation/capture-sync.md) — Build datasets from your cameras
- [Monitor Over Time](../../build/stationary-vision/monitor-over-time.md) — Detect anomalies and trends

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
| `part-classifier` | mlmodel | TFLite model for PASS/FAIL classification |
| `part-detector` | vision | ML model service connected to camera |
| `rejector` | motor | Pneumatic pusher for rejecting parts |
| `inspector` | generic (module) | Control logic service |
| `offline-alert` | trigger | Email notification when machine goes offline |

### Simulated Events

| Event | Trigger | Purpose |
|-------|---------|---------|
| Part appears | Timer or user action | New item to inspect |

---

## Blocks Used

From [block-definitions.md](../../planning/block-definitions.md):

**Foundation:**
- Connect to Cloud
- Add a Camera
- Capture and Sync Data
- Start Writing Code

**Perception:**
- Add Computer Vision
- Detect Objects (2D)

**Stationary Vision:**
- Trigger on Detection
- Inspect for Defects

**Fleet/Deployment:**
- Configure Multiple Machines

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
- [ ] Data capture configuration UI
- [ ] Trigger configuration UI
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

3. ~~**Alert mechanism:** What works without user setup?~~ **Resolved:** Using machine health trigger (offline alert) with email notification. Detection-based alerts deferred to Part 5.

4. **Second station:** Identical or slightly different? Identical is simpler; different shows fragment flexibility.

5. **Dashboard complexity:** How much web dev do we include? Keep minimal—point is Viam APIs, not teaching React.

6. **Mobile app control:** Consider introducing mobile SDK / remote control from phone somewhere in the tutorials. Could demonstrate controlling machines from anywhere.
