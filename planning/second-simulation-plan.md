# Draft Plan: Second Inspection Station Simulation

**Status:** Draft
**Purpose:** Enable Part 5 of the stationary-vision tutorial to demonstrate fragments and fleet management with two visually distinct simulation environments.

## Problem

Part 5 of the tutorial teaches fragments and fleet scaling, but currently lacks:
1. A second simulation environment for users to deploy
2. A meaningful configuration difference that requires fragment parameterization
3. Visual differentiation so users can tell which station they're viewing

## Proposal

Create a second Gazebo world file that is functionally identical but visually distinct, with a different camera topic name to create a real parameterization need.

---

## Plan: Second Inspection Station World

**Source file:** `poc/gazebo-camera/worlds/cylinder_inspection.sdf`
**New file:** `poc/gazebo-camera/worlds/cylinder_inspection_2.sdf`

### Key Changes

**1. Camera topic (creates fragment variable need)**

Current:
```xml
<topic>inspection_camera</topic>
```

Change to:
```xml
<topic>station_2_camera</topic>
```

This means the fragment needs a `camera_topic` variable. Users will set:
- Station 1: `{"camera_topic": "/inspection_camera"}`
- Station 2: `{"camera_topic": "/station_2_camera"}`

**2. Visual differentiation (easy color changes)**

| Element | Station 1 (current) | Station 2 (proposed) |
|---------|---------------------|----------------------|
| Belt surface | Dark gray (`0.1, 0.1, 0.12`) | Dark blue (`0.1, 0.12, 0.18`) |
| Side rails | Light gray (`0.6, 0.6, 0.6`) | Yellow/gold (`0.7, 0.6, 0.2`) |
| Reject bin | Red (`0.6, 0.2, 0.2`) | Orange (`0.7, 0.4, 0.1`) |
| Output chute | Green (`0.2, 0.5, 0.2`) | Blue (`0.2, 0.4, 0.6`) |
| Frame legs | Gray (`0.5, 0.5, 0.5`) | Darker gray (`0.35, 0.35, 0.4`) |

**3. World name**

Change from `cylinder_inspection` to `cylinder_inspection_2` so Gazebo services use a different namespace.

**4. Overview camera topic** (if used)

Current: `/overview_camera`
Change to: `/station_2_overview`

### What stays the same

- Conveyor dimensions and positions (functional compatibility)
- Can spawn/delete positions
- Camera position and field of view
- Physics settings
- Can models (good/dented)

### Supporting changes needed

1. **New entrypoint script** (`entrypoint_station2.sh`) or parameterized entrypoint that accepts the world file
2. **Updated Docker run instructions** for launching station 2 on different ports (e.g., 8082, 8083, 8445)
3. **Updated `can_spawner.py`** to accept world name as parameter (currently hardcoded to `cylinder_inspection`)
4. **Viam config for station 2** with the different camera topic

### Educational payoff

- **Real parameterization**: Camera topic isn't arbitrary—it's required for the config to work
- **Visual confirmation**: Users can instantly see which station they're controlling
- **Fleet realism**: Mirrors real deployments where hardware varies but logic is shared
- **Debugging practice**: If they mix up topics, the camera won't work—teachable moment

---

## Open Questions

- Should the second station use a different can spawner rate or defect probability to show data differences across fleet?
- Do we need a combined web viewer that shows both stations side by side?
- How will Docker networking work for two containers? Same network with different ports, or separate networks?

## Next Steps

1. Review and approve plan
2. Create `cylinder_inspection_2.sdf` with proposed changes
3. Create/update entrypoint script for station 2
4. Update `can_spawner.py` to accept world name parameter
5. Create Viam config for station 2
6. Update Part 5 tutorial with concrete instructions
7. Test end-to-end flow
