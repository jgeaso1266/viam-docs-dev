# Viam Essentials: Operate from Anywhere

**Duration target:** 75 seconds

---

## Pre-shoot checklist

- [ ] Machine from Ep 1 running (arm + camera configured and online)
- [ ] Presenter at a different location from the machine (different room,
      or staged to look like a different location — home office, coffee shop)
- [ ] Laptop with browser open to Viam app, logged in
- [ ] Laptop with terminal/IDE open, `demo_remote_connect.py` ready
- [ ] Camera angle on the machine (second film camera) to show arm moving
      when controlled remotely

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> Your robot is on a factory floor. You're at your desk. Normally, remote
> access means VPN configs, SSH tunnels, and firewall rules. With Viam, you
> just connect.

SHOT: Presenter at a laptop, clearly not next to the robot. The setting
should feel "remote" — a different room, different lighting.

---

### DEMO — screen + intercut hardware [0:10–0:55]

**Web app control [0:10–0:30]**

> I open the Viam app and navigate to my machine. Here's the CONTROL tab.
> I can see the live camera feed — that's the workbench, streaming right
> now from the machine in the other room.

SHOT: Screen capture — Viam app, CONTROL tab. Camera feed is live.

> I can move the arm from right here.

SHOT: Screen — presenter uses arm control panel to jog a joint.

CUT TO: Wide shot of the machine in the other room. Arm moves.

CUT BACK: Screen — camera feed shows the arm in its new position.

**Code control [0:30–0:50]**

> And it's not just the web UI. I can run code from my laptop too.

SHOT: Screen — terminal on laptop. Show `demo_remote_connect.py` briefly
(the connection lines and the arm move command). Run it.

> Five lines to connect, read the camera, and move the arm. Same API
> whether I'm sitting next to it or across the country.

SHOT: Terminal output appears:
```
Got image: 640x480
Current joints: [0.0, -45.0, -30.0, 0.0, 60.0, 0.0]
Arm moved.
```

CUT TO: Wide shot — arm moves again (the 15-degree jog from the script).

**Logs [0:50–0:55]**

> I can also stream logs in real time, filtered by component.

SHOT: Screen — LOGS tab in Viam app. Logs streaming. Quick filter by
"my-arm". Brief — just enough to establish the capability.

---

### PAYOFF — face to camera [0:55–1:15]

> No VPN. No port forwarding. Viam handles the connection. Same app, same
> SDK, same APIs — from anywhere.

SHOT: Presenter at laptop. Brief, confident.

---

## Validation notes

### Code accuracy (demo_remote_connect.py)
- Connection pattern (`Options.with_api_key` + `at_address`) — same as
  Ep 1, confirmed from SDK source
- `camera.get_image()` returns `ViamImage` with `.width`, `.height` —
  confirmed (`video.py:147-153`)
- `arm.get_joint_positions()` returns `JointPositions` with `.values` —
  confirmed from proto (`repeated double values`)
- `JointPositions` import from `viam.proto.component.arm` — confirmed
  from SDK (`proto/component/arm/__init__.py:14`)
- `arm.move_to_joint_positions(JointPositions(values=...))` — correct
  signature per SDK (`arm.py:92`): takes `JointPositions` positional,
  optional `extra`, `timeout` kwargs
- Modifying `positions.values` via `list()` copy then passing new
  `JointPositions` — safe pattern, avoids mutating the protobuf in place

### Behavioral claims
- "No VPN, no port forwarding" — confirmed: Viam uses WebRTC with cloud
  signaling for NAT traversal. The SDK connects through
  `robot/client.py` which uses `viam.rpc.dial` with cloud auth.
- "Same API whether next to it or remote" — correct: the SDK client
  classes use gRPC/WebRTC; the API is identical regardless of network path.

### UI references
- **CONTROL tab** — confirmed route `/machine/{id}/control`
- **LOGS tab** — confirmed route `/machine/{id}/logs`
- Arm control panel — rendered by `@viamrobotics/test-cards` (external
  package, can't verify exact UI from local source, but functionality
  confirmed from existing docs and tutorials)
- Log filtering — exists in the logs UI component
