# Capability #1: Get Hardware Running in Minutes
## 90-Second Video Script

**Learning Outcome:** "Hardware is configured, not coded — and because it's behind a consistent API, my code never has to change when my hardware does."

**Demo Setup:** xArm 6 with gripper attached, Intel RealSense D435 camera, Orbbec Astra camera (for swap), bench setup (no application — bare hardware)

---

## Script

### [00:00-00:18] Hook (18 seconds)

*Visual:*
- Presenter on camera, arm with gripper attached, camera, all on bench — unplugged

*Presenter:*
"Getting a depth camera running on a robot means kernel patches, vendor-specific SDKs, and platform builds that may or may not support your OS.

Getting an arm moving means configuring a dedicated Ethernet connection, enabling motors through a web interface, and writing initialization code you'll paste into every script. If anything goes wrong such as a collision or an overload, the arm locks up, and sometimes the only fix is walking over and power cycling it.

Here's what setting up an arm and wrist-mounted cam looks like with Viam."

---

### [00:18-00:38] Demo: Configuration (20 seconds)

*Visual:*
- Quick cuts, tight editing:
  - Attach gripper to arm
  - Plug in Intel RealSense camera → show config in Viam app UI → camera feed appears
  - Plug in arm (with gripper already attached) → show config in UI → arm responds
  - Show gripper config in UI → gripper opens and closes

*Presenter (voiceover over the montage):*
"Three components. Three config blocks. No kernel patches. No SDKs. No initialization ritual. Just tell Viam what's connected to your robot, and it handles the rest."

---

### [00:38-00:58] Demo: Code (20 seconds)

*Visual:*
- Show on screen (see `examples/cap1_camera_demo.py`):
  ```python
  camera = Camera.from_robot(robot, "my-camera")
  images, _ = await camera.get_images()
  pcd_bytes, _ = await camera.get_point_cloud()
  ```
- Run it. Image pops up on screen. Point cloud visualizer opens.
- Show the same image and point cloud in the Viam app UI CONTROL tab.

*Presenter (voiceover):*
"Getting your hardware set up in Viam is quick and usually painless, but the real power is that Viam SDKs provide well-defined APIs for every type of hardware. Your code talks to a camera. Not a RealSense. Not an Orbbec. A camera. Get images. Get point clouds. The API is the same regardless of what hardware is behind it. And you can see the same outputs in the Viam app."

---

### [00:58-01:10] Demo: The Swap (12 seconds)

*Visual:*
- Unplug Intel RealSense camera
- Plug in Orbbec Astra camera
- Show config change in Viam app UI — one field changes
- Run the same code. Image pops up — visibly different (different camera characteristics) but same code produced it.

*Presenter (voiceover):*
"Swap the hardware. Change one field in the config. Run the same code. Different camera, same API. Your application doesn't know the difference."

---

### [01:10-01:30] Payoff (20 seconds)

*Visual:*
- Back to presenter on camera
- Arm with Orbbec camera still visible in background

*Presenter:*
"In Viam, hardware is configured, not coded. Every camera speaks the same API. Every arm speaks the same API. You write your application once, and it works with whatever hardware you connect.

---

## Production Notes

**Total time:** ~90 seconds

**Pacing:**
- Hook is dense and specific — delivered with authority, not speed. These are real problems the presenter has encountered.
- Config montage (18-38s) should be fast-paced — the ease and speed is the point. Don't linger on keystrokes.
- Code section (38-58s) should breathe — let the viewer read the three lines, see the image and point cloud, and absorb the point. Show outputs both from the script and in the Viam app UI.
- Swap section (58-70s) should feel effortless — unplug, plug, change one field, run same code, visibly different image output. Point cloud not shown for Orbbec — presenter will finesse this in the demo.
- Payoff (70-90s) is delivered directly to camera, with conviction. This is the thesis statement.

**The narrative arc:**
Hardware setup is real engineering work (hook) → With Viam it's just configuration (config montage) → Your code uses generic APIs, not vendor SDKs (code) → Swap hardware, code doesn't change (swap) → This is hardware abstraction (payoff)

**Key messages:**
1. Setup is configuration, not engineering work — no kernel patches, no vendor SDKs, no initialization code
2. Hardware abstraction means your code is hardware-independent — swap vendors, change devices, your application doesn't care

**Tone:**
- Expert, not salesperson. The hook comes from genuine experience with these problems.
- The pain points in the hook are specific and validated — kernel patches, vendor SDKs, dedicated Ethernet, motor enable sequences, power cycling after errors. These are real.
- No "the old way vs. the new way" framing. Just: here's the problem, here's what it looks like with Viam.

---

## Research Backing for Hook Claims

### Camera pain points (validated March 2025 - March 2026):
- RealSense DKMS kernel patching fails on kernel 6.8+ (GitHub issue #14156, July 2025)
- RealSense USB 3.0 misdetection across multiple laptops (GitHub issue #13903, April 2025)
- Orbbec has 4 competing SDKs; same camera model ships with different firmware requiring different SDKs
- Orbbec Windows pip wheel ships macOS binaries (GitHub issue #194, December 2025)
- Orbbec "no device found" with no diagnostic (multiple issues, through March 2026)

### Arm pain points (validated March 2025 - March 2026):
- xArm mode switch silently resets, undocumented (GitHub issue #141, May 2025)
- xArm SDK bug leaves motion state broken (GitHub issue #149, December 2025)
- Firmware updates break working code (GitHub xarm_ros2 issue #155, December 2025; SDK issue #153, March 2026)
- F/T sensor errors unrecoverable via SDK, require power cycle (GitHub issue #151, January 2026)

---

## B-Roll Needed

- xArm 6 on bench (no application, clean setup)
- Intel RealSense D435 camera closeup
- Orbbec Astra camera closeup
- Gripper being attached to arm
- Camera swap moment (unplugging RealSense, plugging in Orbbec)
- Gripper opening and closing from UI command
- Arm moving from UI command
- Tight shots of USB cables being plugged in
- Wide shot of bench setup with all components

## Screen Recordings Needed

- Viam app UI showing camera config and live feed appearing
- Viam app UI showing arm config and arm responding
- Viam app UI showing gripper config and gripper operating
- Camera swap: config field changing in UI
- Python code on screen (3 lines — Camera.from_robot, get_image, get_point_cloud)
- Code execution showing 2D image and Open3D point cloud visualization
- Viam app UI CONTROL tab showing same camera feed and point cloud viewer
- Same code execution after camera swap showing visibly different image and point cloud
- Viam app UI after swap showing updated feed and point cloud

## Graphics/Overlays

- Config fields should be clearly visible and readable in UI
- Highlight the model change during camera swap
- Code should be large, readable, clean font
- Smooth transitions between shots
- Minimal, clean aesthetic
- Optional: small label showing which camera is active during each demo
