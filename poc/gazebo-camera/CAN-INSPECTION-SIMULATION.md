# Can Inspection Simulation

Technical reference for the Gazebo-based can inspection simulation.

---

## Overview

This simulation models an industrial quality inspection station where cans move along a conveyor belt past an overhead camera. Approximately 10% of cans have visible defects (dents). The simulation supports the **Stationary Vision** tutorial scenario, demonstrating how computer vision can detect defects in manufacturing.

**Purpose:** Provide a realistic test environment for vision-based defect detection without requiring physical hardware.

**Key capabilities:**
- Continuous stream of objects moving through inspection zone
- Mix of good and defective items with visually distinguishable differences
- Live camera feed accessible via web browser
- Configurable spawn rate, belt speed, and defect probability

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Docker Container                            │
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   gz-sim     │    │ can_spawner  │    │  web_viewer_     │  │
│  │              │    │    .py       │    │    fruit.py      │  │
│  │  - Physics   │    │              │    │                  │  │
│  │  - Rendering │    │  - Spawns    │    │  - Subscribes    │  │
│  │  - Sensors   │    │    cans      │    │    to camera     │  │
│  │              │    │  - Moves     │    │  - Serves HTTP   │  │
│  │              │    │    cans      │    │    on :8080      │  │
│  │              │    │  - Deletes   │    │                  │  │
│  │              │    │    cans      │    │                  │  │
│  └──────┬───────┘    └──────┬───────┘    └────────┬─────────┘  │
│         │                   │                      │            │
│         └───────── gz-transport ──────────────────┘            │
│                    (topics & services)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼ Port 8080
                    ┌──────────────────┐
                    │  User's Browser  │
                    │  (live camera)   │
                    └──────────────────┘
```

**Data flow:**

1. `gz-sim` runs the physics simulation and renders camera images
2. `can_spawner.py` creates/moves/deletes cans via gz service calls
3. `web_viewer_fruit.py` subscribes to the camera topic and streams JPEG frames
4. Browser displays MJPEG stream at `http://localhost:8080`

---

## Camera Specification

| Property | Value |
|----------|-------|
| **Sensor type** | RGB camera (no depth) |
| **Resolution** | 640 x 480 pixels |
| **Frame rate** | 30 fps |
| **Pixel format** | R8G8B8 |
| **Horizontal FOV** | 1.047 radians (~60°) |
| **Clip range** | 0.1m to 100m |
| **Mounting** | Overhead, pointing straight down |
| **Height above belt** | ~0.5m |
| **Topic name** | `/inspection_camera` |

The camera is mounted on a static frame above the conveyor belt, providing a top-down view of cans as they pass through the inspection zone.

---

## Conveyor Belt System

The conveyor belt uses **kinematic positioning** rather than physics-based movement. Cans are spawned as kinematic objects (no physics simulation) and their positions are updated directly via Gazebo's `set_pose` service.

**Why kinematic?** Physics-based conveyor belts require complex joint configurations or contact friction tuning. Kinematic positioning provides smooth, predictable motion without fighting the physics engine.

| Parameter | Value | Description |
|-----------|-------|-------------|
| Belt length | ~0.92m | From x=-0.42 to x=0.50 |
| Belt speed | 0.18 m/s | Time to cross: ~5 seconds |
| Belt width | ~0.20m | Centered at y=0 |
| Belt height | 0.50m | Surface height above ground |
| Update interval | 0.3 seconds | Position update frequency |

**Movement sequence:**

1. Can spawns at x=-0.42 (input end)
2. Position incremented by `BELT_SPEED * CHECK_INTERVAL` each cycle
3. Can deleted when x > 0.50 (output end)

---

## Object Models

### Good Can (`models/can_good/`)

Standard aluminum beverage can, undamaged.

| Property | Value |
|----------|-------|
| Dimensions | 6.6cm diameter, 12cm height |
| Material | Metallic PBR (metalness: 0.9, roughness: 0.3) |
| Color | Silver/aluminum with blue label band |
| Physics | Kinematic (no mass/inertia) |

### Dented Can (`models/can_dented/`)

Damaged can with visible defects on top surface (designed for overhead camera visibility).

| Property | Value |
|----------|-------|
| Base model | Same as good can |
| Defect type | Dark discolored patches on top lid |
| Defect count | 2 ellipsoid damage marks |
| Defect color | Brown/rust tones (contrast with silver) |
| Defect size | ~12mm and ~8mm diameter |

**Design decision:** Defects are placed on the TOP of the can because the camera views from above. Side dents would not be visible from the overhead perspective.

---

## Configuration Parameters

All configurable values are defined at the top of `can_spawner.py`:

```python
SPAWN_INTERVAL = 4.0    # seconds between spawns
SPAWN_X = -0.42         # X position where cans spawn (input end)
DELETE_X = 0.50         # X position where cans are deleted (output end)
BELT_Y = 0.0            # Y position (center of belt)
BELT_Z = 0.60           # Z position (spawn height, drops to belt)
DENT_PROBABILITY = 0.1  # 10% chance of dented can
CHECK_INTERVAL = 0.3    # seconds between position updates
BELT_SPEED = 0.18       # meters per second
```

**Derived values:**

- Transit time: `(DELETE_X - SPAWN_X) / BELT_SPEED` ≈ 5.1 seconds
- Max cans on belt: `transit_time / SPAWN_INTERVAL` ≈ 1-2 cans
- Position updates per transit: `transit_time / CHECK_INTERVAL` ≈ 17 updates

---

## File Inventory

| File | Purpose |
|------|---------|
| `worlds/fruit_inspection.sdf` | Gazebo world file defining scene geometry, lighting, camera sensor |
| `models/can_good/model.sdf` | Good can model definition |
| `models/can_good/model.config` | Model metadata |
| `models/can_dented/model.sdf` | Dented can model definition |
| `models/can_dented/model.config` | Model metadata |
| `can_spawner.py` | Python script that spawns, moves, and deletes cans |
| `web_viewer_fruit.py` | Flask app that streams camera feed to browser |
| `entrypoint_fruit.sh` | Container startup script |
| `viam-config-fruit.json` | Viam configuration for this scenario |
| `Dockerfile` | Container build definition |

---

## Running the Simulation

```bash
# Build the container
cd poc/gazebo-camera
docker build -t gazebo-camera-poc .

# Run the can inspection simulation
docker run -d --name can-inspection -p 8080:8080 \
  --entrypoint /entrypoint_fruit.sh \
  gazebo-camera-poc

# View in browser
open http://localhost:8080

# Watch logs
docker logs -f can-inspection

# Stop simulation
docker stop can-inspection && docker rm can-inspection
```

**Startup sequence:**

1. Xvfb starts (virtual display for headless rendering)
2. Gazebo loads world file
3. Simulation unpaused
4. Can spawner starts (waits 5s for Gazebo)
5. Web viewer starts
6. Ready message displayed

---

## World File Structure

The world file (`worlds/fruit_inspection.sdf`) contains:

| Element | Description |
|---------|-------------|
| Physics | Default ODE physics engine |
| Lighting | Directional sun + point lights for even illumination |
| Ground plane | Gray surface beneath conveyor |
| Conveyor structure | Static model with belt surface, frame, legs |
| Camera mount | Static frame holding inspection camera |
| Inspection camera | Sensor attached to camera mount |
| Reject bin | Red bin (visual only, not functional) |
| Output chute | Green chute (visual only, not functional) |
| Air jet | Rejector nozzle (visual only, not functional) |

**Note:** The reject bin, output chute, and air jet are visual props. The rejection mechanism is not implemented—all cans currently pass through to deletion regardless of defect status.

---

## Gazebo Services Used

The spawner interacts with Gazebo via these services:

| Service | Purpose |
|---------|---------|
| `/world/fruit_inspection/create` | Spawn new can model |
| `/world/fruit_inspection/remove` | Delete can model |
| `/world/fruit_inspection/set_pose/blocking` | Update can position |
| `/world/fruit_inspection/control` | Unpause simulation |

**Example spawn request:**
```
sdf_filename: "model://can_good", name: "can_0001",
pose: {position: {x: -0.42, y: 0.0, z: 0.60}}
```

---

## Limitations

| Limitation | Description |
|------------|-------------|
| **No depth camera** | Only RGB images; no 3D point cloud data |
| **No physics-based belt** | Cans move via position updates, not friction |
| **No rejection mechanism** | All cans pass through; air jet is visual only |
| **Single camera angle** | Overhead only; no side inspection |
| **Simplified defects** | Color patches, not geometric deformation |
| **No lighting variation** | Consistent lighting; no shadows/glare challenges |

---

## Future Enhancements

Potential improvements for more realistic simulation:

1. **Depth camera** — Add RGBD sensor for 3D inspection
2. **Working rejector** — Implement air jet that pushes defective cans into reject bin
3. **Physics-based belt** — Use joint velocity control for realistic belt movement
4. **Geometric defects** — Model actual dents as mesh deformations
5. **Lighting variation** — Add configurable lighting conditions
6. **Multiple camera angles** — Side cameras for comprehensive inspection
7. **More defect types** — Rust, label damage, crushed cans
8. **Variable can orientations** — Rotation variation as cans spawn
