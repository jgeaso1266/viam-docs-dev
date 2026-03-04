# Block Definitions

**Status:** 🟡 Draft

Blocks are modular tutorials that can be composed into larger workflows. Each block should:
- Be self-contained (~15-30 minutes)
- Work in simulation AND real hardware
- Have clear prerequisites and outcomes
- Map to specific problems from the lifecycle analysis

All block categories are top-level sections in viam-docs.

See [Content Guidelines](./content-guidelines.md) for detailed authoring guidance.

---

## Get Started Blocks

*Universal prerequisite. Everyone starts here.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Initialize a Viam Machine | Compute board | Platform basics, remote access, WebRTC | 1.1, 1.6, 2.9 |

---

## Hardware Blocks

*Configure physical components.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Add a Camera | Camera + compute | Component configuration, viewing feeds | 1.1, 1.2, 1.9 |

---

## Data Blocks

*Work with captured data.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Capture and Sync Data | Camera + compute + cloud | Data pipeline, storage, sync | 1.12, 2.13, 2.14 |
| Query Data | Cloud + data | SQL/MQL queries, navigating nested JSON, filtering and aggregation | 1.12, 2.13 |
| Filter at the Edge | Camera + compute | Time-based sampling, sensor thresholds, filtered camera modules, conditional sync | 2.13, 2.14 |
| Visualize Data | Cloud + third-party tools | Connect Grafana, Tableau, or custom dashboards to Viam data | 2.13, 3.10 |
| Configure Data Pipelines | Cloud + data | Windowed roll-ups, aggregations, derived metrics, cost-efficient querying | 2.13, 2.14, 3.10 |
| Sync Data to Your Database | Cloud + external MongoDB | Direct capture to your cluster, egress patterns, "Viam as ingestion layer" architecture | 2.13, 3.10 |

---

## Train Blocks

*Go from raw data to trained models.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Create a Dataset | Cloud + captured data | Tag images, draw bounding boxes, manage dataset versions | 1.13, 2.13 |
| Train a Model | Cloud + dataset | Select model architecture, start training, evaluate results, deploy to machines | 1.13 |

---

## Development Blocks

*Write and ship code.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Write an Inline Module | Browser + machine | Browser-based module editing, cloud builds, validate/new/do_command pattern, scheduled jobs | 1.3, 1.21 |
| Write a Module | Laptop + robot | Module scaffolding, dependency injection, DoCommand, remote testing | 1.3, 1.21 |
| Deploy a Module | Module registry | Cross-compile, package, upload, versioning | 1.21, 3.10 |

---

## Work Cell Layout Blocks

*Configure the 3D space your robot operates in.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Define Your Frame System | Robot + compute | World frame, parent-child hierarchy, static transforms, spatial visualization | 1.4, 1.17 |
| Configure Robot Kinematics | Arm/gantry + compute | URDF import, joint limits, tool center point, kinematic model | 1.3, 1.17 |
| Calibrate Camera to Robot | Camera + arm + calibration target | Camera intrinsics, eye-in-hand vs eye-to-hand, verifying 3D accuracy | 1.9, 1.19 |
| Define Obstacles | Robot + workspace fixtures | Static geometry (box/sphere/capsule), keep-out zones, world state store, collision avoidance | 1.7, 1.20 |

---

## Vision & Detection Blocks

*Building understanding of the environment.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Add Computer Vision | Camera + compute + model | Vision service, ML models, inference basics | 1.13 |
| Detect Objects (2D) | Camera + ML model | Bounding boxes, confidence scores | 1.13, 1.19 |
| Classify Objects | Camera + ML model | Single-label vs. multi-label classification | 1.13, 1.19 |
| Track Objects Across Frames | Camera + ML model | Persistence, IDs, trajectories | 1.19 |
| Measure Depth | Depth camera | Point clouds, distance estimation | 1.19 |
| Localize Objects in 3D | Camera + depth | Transforming 2D detections to 3D coordinates | 1.19 |

---

## Stationary Vision Blocks

*Vision systems that don't move.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Trigger on Detection | Camera + ML + triggers | Event-driven actions, alerts | 2.12 |
| Count Objects | Camera + ML + data | Accumulation, logging, dashboards | 1.12 |
| Inspect for Defects | Camera + ML | Binary classification, pass/fail | 1.13 |
| Monitor Over Time | Camera + data capture | Baseline establishment, anomaly detection | 2.6 |

---

## Mobile Base Blocks

*Robots that move.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Drive the Base | Base + motors | Velocity commands, encoders | 1.3 |
| Estimate Position | Base + encoders | Position estimation, drift | 1.3, 1.4 |
| Build a Map | Base + lidar + SLAM | Mapping service, localization | 1.17, 1.18 |
| Navigate to Waypoint | Base + lidar + nav service | Motion planning, goal-seeking | 1.17, 1.18 |
| Avoid Obstacles | Base + sensors | Reactive control, safety | 1.7, 1.20 |
| Follow a Patrol Route | Base + nav + waypoints | Multi-point missions, state machines | 1.16 |
| Detect While Moving | Base + camera + ML | Perception during motion | 1.5, 1.19 |
| Navigate to Detected Object | Base + camera + nav | Perception-driven goals | 1.16, 1.19 |
| Mobile Pick-and-Place | Base + arm + camera | Mobile manipulation | 1.5, 1.16 |

---

## Arm + Manipulation Blocks

*Robots that grab things.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Move the Arm | Arm | Joint positions, velocity control | 1.3 |
| Control Gripper | Gripper | Open/close, force sensing | 1.3 |
| Move to Pose | Arm + motion service | Inverse kinematics, motion planning | 1.17 |
| Pick an Object | Arm + gripper + camera | Grasp planning, coordination | 1.5, 1.19 |
| Place an Object | Arm + gripper | Precision, release | 1.5 |
| Pick from Bin | Arm + camera + ML | Full pick-and-place cycle | 1.5, 1.19 |
| Visual Servoing | Arm + camera | Closed-loop control, alignment | 1.19 |

---

## Productize Blocks

*Ship a product to your customers.*

| Block | Components | What You Learn | Problems Addressed |
|-------|------------|----------------|-------------------|
| Build a Teleop Dashboard | Cloud + data | Workspaces, widgets, MQL pipelines, internal monitoring | 4.9 |
| Build a Customer-Facing Web App | TypeScript SDK | Custom interfaces, customer-facing web apps | 4.9 |
| Branded Customer Login | Auth config | Customer login with your branding | 4.9 |
| Configure Billing | Billing config | Per-machine/per-data pricing, metering | 4.8 |

---

## Block Composition: Work Cells

### Stationary Vision Work Cell

```
Get Started
└── Initialize a Viam Machine
        ↓
Hardware
└── Add a Camera
        ↓
Data
├── Capture and Sync Data
├── Query Data
└── Filter at the Edge
        ↓
Development
├── Write an Inline Module
├── Write a Module
└── Deploy a Module
        ↓
Vision & Detection
├── Add Computer Vision
├── Detect Objects (2D)
└── Classify Objects
        ↓
Stationary Vision
├── Trigger on Detection
├── Count Objects
└── Inspect for Defects
        ↓
Productize
├── Build a Teleop Dashboard
├── Build a Customer-Facing Web App
├── Branded Customer Login
└── Configure Billing
```

### Mobile Base Work Cell

```
Get Started
└── Initialize a Viam Machine
        ↓
Hardware
└── Add a Camera
        ↓
Data
├── Capture and Sync Data
├── Query Data
└── Filter at the Edge
        ↓
Development
├── Write an Inline Module
├── Write a Module
└── Deploy a Module
        ↓
Vision & Detection
├── Add Computer Vision
├── Detect Objects (2D)
└── Track Objects Across Frames
        ↓
Mobile Base
├── Drive the Base
├── Estimate Position
├── Build a Map
├── Navigate to Waypoint
├── Avoid Obstacles
├── Follow a Patrol Route
├── Detect While Moving
└── Navigate to Detected Object
        ↓
Productize
├── Build a Teleop Dashboard
├── Build a Customer-Facing Web App
├── Branded Customer Login
└── Configure Billing
```

### Arm + Vision Work Cell

```
Get Started
└── Initialize a Viam Machine
        ↓
Hardware
└── Add a Camera
        ↓
Data
├── Capture and Sync Data
├── Query Data
└── Filter at the Edge
        ↓
Development
├── Write an Inline Module
├── Write a Module
└── Deploy a Module
        ↓
Work Cell Layout
├── Define Your Frame System
├── Configure Robot Kinematics
├── Calibrate Camera to Robot
└── Define Obstacles
        ↓
Vision & Detection
├── Add Computer Vision
├── Detect Objects (2D)
├── Measure Depth
└── Localize Objects in 3D
        ↓
Arm + Manipulation
├── Move the Arm
├── Control Gripper
├── Move to Pose
├── Pick an Object
├── Place an Object
└── Pick from Bin
        ↓
Productize
├── Build a Teleop Dashboard
├── Build a Customer-Facing Web App
├── Branded Customer Login
└── Configure Billing
```

---

## Block Template

Each block should follow this structure:

```markdown
# [Block Name]

## What Problem This Solves

2-3 sentences describing the real-world problem this addresses.

## Steps

1. Step one
2. Step two
3. ...

Use Python/Go code in tabbed blocks for all code samples.

## Try It

Verification step that confirms the block works as expected.

## Troubleshooting

Collapsible sections for common issues.

## Next Steps

- Link to next block
- Link to related blocks
```

---

## Open Questions

1. **Block size:** Is 15-30 minutes the right target?
2. **Prerequisites:** How strict? Can users skip ahead?
3. **Simulation parity:** Can all blocks work identically in sim and real?
4. **Code samples:** What languages? Python first, then others?
5. **Versioning:** How do we update blocks without breaking paths?
