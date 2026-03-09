# Viam Capabilities Video Series

## Series concept

Eight short videos (60-120 seconds each), one per capability from the
"What is Viam?" page. Each video follows the same structure:

1. **The problem** (10-15s) — A concrete pain point developers recognize.
2. **The Viam way** (40-60s) — Live demo showing the capability in action.
3. **The payoff** (10-15s) — What just happened, reframed as a principle.

The videos work standalone (embedded on docs pages, shared individually) and
as a playlist that builds a cumulative picture of the platform.

## Production approach

- Polished but developer-authentic. Real hardware on a real workbench, real
  terminal output, real UI. Not stock footage, not slides.
- Film crew handles camera work, lighting, audio. Screenflow captures are
  composited in post for terminal/UI shots.
- Presenter on camera for problem setup and payoff moments. Demo sections
  mix face-to-camera, hands-on-hardware, and screen capture. The presenter
  drives the narrative — this is someone showing you something they built,
  not a disembodied voiceover.
- Each video should feel like watching a skilled developer work, with the
  tedious parts cut away.

## Playlist order and narrative arc

The order tells a story: start a machine, connect to it, capture data, train
on that data, write code against it, package that code, scale it out, then
productize. Each video assumes you've seen the previous ones but doesn't
require it.

| # | Capability | Duration | Core demo |
|---|-----------|----------|-----------|
| 1 | Get hardware running in minutes | 90s | Cold-start an arm + camera from zero config |
| 2 | Operate from anywhere | 75s | Control the arm from a laptop across the network |
| 3 | Capture data from edge to cloud | 90s | Set up vision-based data capture, see it in the cloud |
| 4 | Train and deploy models | 90s | Train a classifier on captured data, deploy to the machine |
| 5 | Develop code remotely | 75s | Write and run a pick script from a laptop IDE |
| 6 | Manage software deployments | 90s | Package the script as a module, push an OTA update |
| 7 | Scale easily | 90s | Apply a fragment to a second machine, roll out a config change |
| 8 | Productize with Viam apps | 75s | Show a white-labeled customer dashboard |

---

## Episode breakdowns

### 1. Get hardware running in minutes

**Problem** (10s): "Setting up a robot arm usually means vendor SDKs, driver
dependencies, and half a day of debugging. What if it took two minutes?"

**Demo** (65s):
- Start on an empty workbench. An xArm 6 sits unpowered, a RealSense camera
  is in its box.
- Terminal: `viam-server` is already installed. Show the one-line install
  for context (don't wait for it).
- Viam app: Create a new machine. Copy the config command. Run it on the
  machine's terminal — `viam-server` starts.
- App CONFIGURE tab: Add a component. Select `xArm6`. Fill in IP address.
  Save. The arm initializes — cut to the arm's status LEDs lighting up.
- Add a second component: `realsense` camera. Save. Cut to the CONTROL tab
  showing a live camera feed.
- CONTROL tab: Use the arm control panel to jog the arm. It moves. The
  camera feed shows the arm moving from the camera's perspective.

**Payoff** (15s): "Two components, zero driver code, consistent APIs.
Hardware just works."

**Key shots**:
- Close-up: empty config, then populated config (fast cut)
- Wide: arm moving for the first time
- Screen capture: CONTROL tab with camera feed + arm controls side by side

**Hardware**: xArm 6, Intel RealSense D435, compute board (Jetson or RPi)

---

### 2. Operate from anywhere

**Problem** (10s): "Your robot is on the factory floor. You're at your desk.
Normally that means VPN configs, SSH tunnels, and prayer."

**Demo** (50s):
- Establish the distance: show the machine on a workbench in one room.
  Cut to a developer at a laptop somewhere else (different room, or
  emphasize "anywhere" with a coffee-shop or home-office setting).
- Laptop browser: Open the Viam app. Navigate to the machine. Show the
  CONTROL tab — live camera feed is streaming.
- Teleoperate: Use the arm control panel to move the arm. Cut between
  the laptop screen and a wide shot of the arm moving in the other room.
- Logs tab: Show live logs streaming. Filter by component name.
- Terminal on laptop: Run a 5-line Python script that connects to the
  machine, reads the camera, and prints the image dimensions. Show the
  output.

**Payoff** (15s): "No VPN. No port forwarding. Just connect and work."

**Key shots**:
- Split screen or cut: laptop in one location, robot in another
- Screen capture: CONTROL tab with live feed
- Terminal: Python script connecting and returning data

**Hardware**: Same arm + camera setup from Ep 1, plus a laptop

---

### 3. Capture data from edge to cloud

**Problem** (10s): "You need training data. Normally that means writing a
capture pipeline, managing local storage, handling network failures..."

**Demo** (65s):
- Viam app CONFIGURE tab: On the camera component, enable data capture.
  Set frequency to 1 image/second. Save.
- Show objects in front of the camera — a few colored blocks or tools on
  the workbench. The camera is capturing.
- App DATA tab: Images start appearing. Show the gallery view populating.
  Scroll through — timestamps, metadata, component name all visible.
- Show the filtering: filter by label, by time range.
- Back to CONFIGURE: Add a vision service (color detector or ML model).
  On the camera, change data capture to use the `filtered-camera` so only
  images with detections are captured. Save.
- DATA tab: Now only images with detected objects appear.

**Payoff** (15s): "Configuration, not code. Capture what matters, skip
what doesn't."

**Key shots**:
- Close-up: toggling data capture on in the UI
- Screen capture: DATA tab populating in near-real-time
- Close-up: objects on the workbench being captured

**Hardware**: Camera + objects to detect (colored blocks, tools, parts)

---

### 4. Train and deploy models

**Problem** (10s): "You have data. Now you need a model that runs on
your robot, not in the cloud."

**Demo** (65s):
- App DATA tab: Select a set of captured images. Add bounding box labels
  — draw boxes around objects, assign class names ("wrench", "bolt",
  "empty"). Show this going fast (speed up in post, or pre-label most
  and show the last few live).
- App TRAIN tab: Create a training job. Select the labeled dataset,
  choose a model type (object detection). Start training.
  (Cut — don't wait for training. Show a "training complete" state.)
- App MODELS section: The trained model appears with a version number.
- App CONFIGURE tab: Add an ML model service pointing to the new model.
  Add a vision service (mlmodel detector) that uses it. Save.
- CONTROL tab on the vision service: TEST panel shows live detections.
  Hold up a wrench — bounding box appears with "wrench: 0.92".

**Payoff** (15s): "From raw images to on-device inference. No GPU
provisioning, no export pipeline, no deploy scripts."

**Key shots**:
- Screen capture: Drawing bounding boxes (satisfying, precise)
- Screen capture: Training job completing
- Live shot: Holding up an object, detection appearing in real-time
- Split: camera feed on screen + real object in hand

**Hardware**: Camera, assorted small objects for detection

---

### 5. Develop code remotely

**Problem** (10s): "In traditional robotics, you develop on the robot or
you don't develop at all. Your IDE is SSH. Your debugger is `print`."

**Demo** (50s):
- Laptop with VS Code (or similar IDE) open. A Python file is visible.
- Show the connection setup: `RobotClient.at_address(...)` with API key.
  Run the script. It connects to the remote machine.
- The script reads the camera, runs the detector from Ep 4, and prints
  detections. Show terminal output: `wrench: 0.92 at (120, 80, 340, 290)`.
- Modify the script live: add logic to move the arm toward the detected
  object. Run again. Cut to the arm moving toward the wrench on the
  workbench.
- Show the iteration loop: tweak a parameter, re-run, watch the result.
  Fast, no deploy step.

**Payoff** (15s): "Your laptop, your IDE, your workflow. The robot is
just another endpoint."

**Key shots**:
- Screen capture: IDE with code, terminal with output
- Wide: arm responding to the script in real-time
- Close-up: developer's hands on keyboard, arm moving in background

**Hardware**: xArm 6, camera, laptop with IDE, small objects

---

### 6. Manage software deployments

**Problem** (10s): "Your script works. Now you need it to run on boot,
restart on failure, and update without SSH."

**Demo** (65s):
- Terminal: Package the script from Ep 5 as a module.
  Show `meta.json` briefly — model name, version, entrypoint.
- Terminal: `viam module upload` — the module goes to the Registry.
  Show the Registry page with the new module listed.
- App CONFIGURE tab: Remove the local script. Add the module from the
  Registry. Configure it with the same attributes. Save.
- Show the machine running the module — same behavior as the script,
  but now managed by `viam-server`.
- Terminal: Make a small change to the module code (adjust a threshold).
  Bump the version. `viam module upload` again.
- App: The machine pulls the update. Show logs indicating the new
  version loaded. Show the changed behavior.

**Payoff** (15s): "Version control, OTA updates, managed lifecycle.
Production-grade deployment without the infrastructure."

**Key shots**:
- Terminal: upload command completing
- Screen capture: Registry showing the module
- Screen capture: Logs showing version update
- Wide: machine continuing to operate through the update

**Hardware**: Same setup as Ep 5

---

### 7. Scale easily

**Problem** (10s): "One machine works. Now you need fifty of them running
the same configuration."

**Demo** (65s):
- App: Show the working machine from previous episodes.
  Open the config — it has an arm, camera, ML model, vision service,
  and the custom module.
- Create a fragment from this configuration. Name it. Save.
- Show a second machine. Add the fragment to it. Save.
- The second machine pulls modules and configures itself. Show it
  running the same detection behavior as the first.
- Update the fragment: change the confidence threshold.
  Show both machines pulling the update. Both now use the new threshold.
- App FLEET view: Show both machines listed, both online, both running
  the same fragment version.

**Payoff** (15s): "One fragment, any number of machines. Update once,
deploy everywhere."

**Key shots**:
- Screen capture: Creating the fragment
- Wide: Two machines side by side, both running
- Screen capture: Fleet view showing both machines

**Hardware options** (pick one):

*Option A — Mobile base (preferred):* The second machine is a rover with
a mounted camera. Strong visual contrast with the arm workstation. Same
fragment configures the camera and vision pipeline on both. The base
doesn't need to drive — the point is that the same detection behavior
runs on completely different hardware.

*Option B — Second workstation (backup):* A visibly different compute
board (e.g., RPi if the first is a Jetson, or vice versa) with a
different camera model (e.g., Orbbec if the first is RealSense). Set it
up at a separate workstation. The visual point: different hardware, same
config, same behavior. This also reinforces the Ep 1 message about
hardware-agnostic APIs — the fragment works even though the camera
model changed.

---

### 8. Productize with Viam apps

**Problem** (10s): "You've built a robotics product. Now your customers
need dashboards, auth, and billing. Do you really want to build all that?"

**Demo** (50s):
- Show a customer-facing web app built with the TypeScript SDK.
  It has a company logo (not Viam's), a login screen, and a dashboard
  showing machine status and camera feeds.
- Log in. Show the dashboard: machine online/offline status, recent
  data, camera feeds. Click into a machine — show controls.
- Show the Flutter mobile app on a phone: same data, native mobile UI.
- Back to the Viam app: Show the billing configuration — pricing tiers,
  per-machine fees. (Brief — just enough to establish the capability.)

**Payoff** (15s): "Auth, dashboards, billing — built in. Ship your
product, not your infrastructure."

**Key shots**:
- Screen capture: White-labeled login page
- Screen capture: Customer dashboard with live data
- Phone screen: Flutter app with machine controls
- Brief: Billing configuration screen

**Hardware**: Laptop, phone, any running machine for live data

**Pre-production requirement**: Build demo versions of both apps before
the shoot. These need to be functional against live machines — not
mockups. Scope:
- **TypeScript web dashboard**: White-labeled login page (custom logo,
  custom colors), fleet overview (machines online/offline), single-machine
  view with live camera feed and recent data. Does not need to be
  production-quality code — just visually clean and functional on camera.
- **Flutter mobile app**: Same fleet overview and single-machine camera
  view. Running on a real phone, not an emulator.
- Both apps authenticate via Viam's OAuth flow and connect to the
  machines used in earlier episodes.

---

## Cross-cutting production notes

### Visual consistency
- Same workbench and lighting setup across all episodes
- Consistent terminal theme and font size for screen captures
- Viam app always shown in the same browser, same zoom level
- Color-coded terminal prompts to distinguish local laptop vs. robot

### Continuity
- Episodes 1-6 build on the same machine. The arm and camera set up in
  Ep 1 are the same ones used through Ep 6. This creates a cumulative
  "we built this" feeling.
- Ep 7 introduces a second machine to demonstrate scaling.
- Ep 8 shifts context to the customer/product side.

### Screen capture approach
- Film the real screens during the live shoot for timing and natural
  interaction.
- Re-capture clean screenflows in post for clarity (no typos, no loading
  spinners, crisp resolution).
- Composite the clean captures over the live footage in post.

### Presenter and narration
- Presenter speaks directly to camera for the problem setup and payoff.
  During the demo section, they narrate over their own actions — talking
  while working, not voiceover added in post.
- Tone is knowledgeable and direct. The presenter is a developer showing
  another developer something useful, not a salesperson pitching.
- Scripts finalized after demo rehearsal — narration should describe what
  the viewer is actually seeing, not what we wish they were seeing.
- Record room tone and backup voiceover takes for flexibility in post.

### Music and pacing
- Subtle background music. Not corporate-inspirational. Something with
  forward momentum.
- Cuts should be brisk. Dead time (loading, typing) is either cut or
  sped up. The viewer should never wait.

## Decisions made

- **Presenter**: Face-to-camera for problem/payoff beats. Hands-on
  during demos. Not pure voiceover.
- **Objects**: Wrench and bolt (simple, recognizable, reads well on
  camera).
- **Ep 7 second machine**: Mobile base preferred, second workstation
  as backup. Both options scripted.
- **Ep 8 apps**: Build demo versions (TypeScript web + Flutter mobile)
  before the shoot. See Ep 8 notes for scope.

## Series name

**Viam Essentials**

Individual episode titles follow the pattern:
"Viam Essentials: [Capability]"

| # | Title |
|---|-------|
| 1 | Viam Essentials: Get Hardware Running |
| 2 | Viam Essentials: Operate from Anywhere |
| 3 | Viam Essentials: Capture Data |
| 4 | Viam Essentials: Train and Deploy Models |
| 5 | Viam Essentials: Develop Remotely |
| 6 | Viam Essentials: Manage Deployments |
| 7 | Viam Essentials: Scale Your Fleet |
| 8 | Viam Essentials: Productize with Apps |
