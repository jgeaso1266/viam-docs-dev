# Viam Essentials: Get Hardware Running

**Duration target:** 90 seconds

---

## Pre-shoot checklist

- [ ] xArm 6 powered off, on workbench, ethernet connected to network
- [ ] Intel RealSense D435 in box or loosely mounted
- [ ] Compute board (Jetson or RPi) on workbench, powered, networked,
      `viam-server` pre-installed (don't show the install during the video)
- [ ] Viam app open in browser, logged in, no machines configured
- [ ] Terminal open on compute board (SSH session or direct)
- [ ] `test_hardware.py` ready on laptop (not shown until end)

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> Setting up a new robot arm usually means hunting down vendor SDKs,
> installing driver dependencies, and spending half a day on configuration
> before anything moves. With Viam, it takes about two minutes.

SHOT: Presenter at workbench. Arm visible but powered off. Camera in box.
Tone: direct, confident, slight smile. Not rushed.

---

### DEMO — screen + hardware [0:10–1:15]

**Create the machine [0:10–0:25]**

> I'll start in the Viam app. I create a new machine — just give it a name.

SHOT: Screen capture — Viam app, click **+ Add machine**, type
"demo-machine", click **Add machine**.

> Viam gives me a setup command. I run it on my machine's terminal and
> viam-server starts.

SHOT: Copy the setup command. Cut to terminal on the compute board. Paste
and run. Show `viam-server` starting (brief — 2-3 seconds of log output,
then cut).

**Add the arm [0:25–0:45]**

> Now I add hardware. In the CONFIGURE tab, I click the plus button, search
> for xArm6, and add it. The only thing I need to set is the arm's IP
> address. I save, and viam-server pulls the driver module from the
> Registry.

SHOT: Screen capture — CONFIGURE tab. Click **+**, select **Component**,
search "xArm6", select `viam:ufactory:xArm6`. Name it "my-arm". Set
`host` to `10.0.0.50`. Click **Save**. Brief pause — show the module
downloading in the logs (can be sped up in post).

CUT TO: Wide shot of arm — status LEDs come on as it initializes. The arm
may make a small settling movement. This is a satisfying physical moment —
hold it for a beat.

**Add the camera [0:45–0:55]**

> Same thing for a camera. Add a RealSense, save, and I've got a live feed.

SHOT: Screen capture — click **+**, search "realsense", select
`viam:camera:realsense`. Name it "my-camera". Click **Save**.

CUT TO: CONTROL tab. Click on "my-camera". Live color feed appears.

**Test the arm [0:55–1:15]**

> In the CONTROL tab, I can test everything right here. I'll jog the arm —

SHOT: CONTROL tab — click on "my-arm". Use the joint position sliders to
move Joint 1 (base rotation) about 30 degrees.

CUT TO: Wide shot — arm rotates smoothly. Camera feed (visible on screen in
background or in a split) shows the arm moving from the camera's
perspective.

> — and the camera is capturing the arm's movement live.

SHOT: Screen — camera feed showing the arm in its new position.

---

### PAYOFF — face to camera [1:15–1:30]

> Two components. Zero driver code. And because every arm and every camera
> in Viam speaks the same API, if I swap this arm for a different model or
> this camera for a different brand, my code doesn't change. Just update
> the config.

SHOT: Presenter, same framing as the open. Arm visible in background,
now powered and in its jogged position.

---

## Validation notes

### Config accuracy
- Model triplet `viam:ufactory:xArm6` confirmed from claw-game tutorial
  (`docs/tutorials/projects/claw-game.md:237`)
- Model triplet `viam:camera:realsense` confirmed from module-configuration
  reference (`docs/reference/module-configuration.md:229`)
- Module IDs (`viam:ufactory-xarm`, `viam:realsense`) — these are
  auto-resolved by the app when you add a registry component, so they
  won't be visible on screen. The JSON in `machine-config.json` represents
  the full config for reference only.
- `host` attribute for xArm confirmed from claw-game tutorial
  (`docs/tutorials/projects/claw-game.md:237-248`)

### Code accuracy (test_hardware.py)
- `RobotClient.Options.with_api_key(api_key, api_key_id)` — confirmed
  from SDK source (`viam/robot/client.py:142`)
- `RobotClient.at_address(address, options)` — confirmed (`client.py:175`)
- `Arm.from_robot(robot, name)` — inherited from ComponentBase
  (`component_base.py:33`)
- `arm.get_joint_positions()` returns `JointPositions` with `.values`
  (repeated double) — confirmed from proto and SDK (`arm.py:125`)
- `arm.get_end_position()` returns `Pose` with `.x`, `.y`, `.z` —
  confirmed from proto `GetEndPositionResponse.pose`
- `Camera.from_robot(robot, name)` — inherited from ComponentBase
- `camera.get_image()` returns `ViamImage` with `.width`, `.height`,
  `.mime_type` properties — confirmed from SDK (`video.py:120-154`)
- `camera.get_images()` returns `Tuple[Sequence[NamedImage], ResponseMetadata]`
  — confirmed from SDK (`camera.py:66`). `NamedImage` has `.name` attribute
  (not `.source_name`) — confirmed from SDK (`video.py:178-185`)

### Behavioral claims
- "viam-server pulls the driver module from the Registry" — confirmed from
  Flow 3 (Module Lifecycle) in `flows.md`: viam-server downloads modules
  on config change, extracts, and starts them.
- "consistent API across hardware" — confirmed: all arms implement the
  same proto interface (`component/arm/v1/arm.proto`), all cameras
  implement `component/camera/v1/camera.proto`.
- "swap hardware without changing code" — accurate: changing the model
  triplet in config switches the driver; the API interface is identical.

### UI references
- **+ Add machine** button — exists in app UI
- **CONFIGURE tab** — confirmed route `/machine/{id}/configure`
- **CONTROL tab** — confirmed route `/machine/{id}/control`
- **Save** button — standard CONFIGURE tab action
- Component search and add flow — uses the add-resource-menu-new component
