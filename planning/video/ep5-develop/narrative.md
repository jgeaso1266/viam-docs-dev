# Viam Essentials: Develop Remotely

**Duration target:** 75 seconds

---

## Pre-shoot checklist

- [ ] Machine from previous episodes running (arm + camera + detector)
- [ ] Wrench on workbench in camera's field of view
- [ ] Presenter at laptop with VS Code or similar IDE open
- [ ] `detect_and_move.py` loaded in IDE with credentials filled in
- [ ] Camera angle on the arm to show it moving during the demo

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> In traditional robotics, you develop on the robot. Your IDE is SSH.
> Your debugger is print. With Viam, you write code on your laptop and
> run it against your robot over the network.

SHOT: Presenter at laptop, not next to the robot.

---

### DEMO — screen + hardware [0:10–0:55]

**Show the code [0:10–0:25]**

> Here's a Python script in my IDE. It connects to the machine, gets
> detections from the camera, finds the wrench, and moves the arm
> toward it.

SHOT: Screen — VS Code with `detect_and_move.py` open. Briefly highlight
the key parts:
1. `RobotClient.at_address(...)` — the connection
2. `detector.get_detections_from_camera(...)` — vision call
3. `arm.move_to_joint_positions(...)` — arm movement

Don't read the code line by line. Let the viewer scan it visually while
the presenter summarizes.

**Run it [0:25–0:40]**

> I run it from right here.

SHOT: Terminal in VS Code. Run the script. Output appears:
```
Found wrench: 0.92 at (120, 80, 340, 290)
Detection center: (230, 185)
Moving arm joint 1 by -2.8 degrees...
Arm moved toward wrench.
```

CUT TO: Wide shot — arm rotates slightly toward the wrench.

**Iterate [0:40–0:55]**

> Now I change a parameter — make the movement bigger.

SHOT: Screen — change `offset * 10` to `offset * 20` in the script.
Save. Run again.

CUT TO: Arm makes a larger movement.

> That's the development loop. Edit, run, see the result. No deploy step,
> no file copying, no restarting services.

---

### PAYOFF — face to camera [0:55–1:15]

> Your laptop, your IDE, your workflow. The robot is just another
> endpoint.

SHOT: Presenter at laptop. Arm visible in background.

---

## Validation notes

### Code accuracy (detect_and_move.py)
- All imports verified against SDK source:
  - `viam.robot.client.RobotClient` — confirmed
  - `viam.components.arm.Arm` — confirmed
  - `viam.components.camera.Camera` — confirmed (imported but not used
    directly; detector reads from camera by name)
  - `viam.services.vision.VisionClient` — confirmed
  - `viam.proto.component.arm.JointPositions` — confirmed
    (`proto/component/arm/__init__.py:14`)
- `Arm.from_robot(robot, name)` — confirmed (`component_base.py:33`)
- `VisionClient.from_robot(robot, name)` — confirmed (`service_base.py:28`)
- `detector.get_detections_from_camera("my-camera")` — confirmed
  (`client.py:87`): `camera_name: str` positional arg
- Detection attributes `class_name`, `confidence`, `x_min`, `y_min`,
  `x_max`, `y_max` — confirmed from proto Detection message
- `arm.get_joint_positions()` returns `JointPositions` with `.values`
  (`repeated double`) — confirmed
- `arm.move_to_joint_positions(JointPositions(values=...))` — confirmed
  (`arm.py:92`)
- Note: `Camera` import is unused in this script. It's included for
  clarity (the viewer sees all the resource types involved) but could
  be removed. Keep it for the video — it helps the viewer understand
  what's available.

### Behavioral claims
- "run it against your robot over the network" — confirmed: SDK uses
  WebRTC/gRPC for remote connection
- "No deploy step, no file copying" — accurate: the script runs locally
  on the laptop, API calls go over the network
- "no restarting services" — accurate: the SDK client connects to the
  existing viam-server instance; running a script doesn't require any
  server restart
