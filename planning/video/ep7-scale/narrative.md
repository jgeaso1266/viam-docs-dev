# Viam Essentials: Scale Your Fleet

**Duration target:** 90 seconds

---

## Pre-shoot checklist

- [ ] Machine 1 from previous episodes running (arm + camera + detector +
      wrench-finder module)
- [ ] Machine 2 set up with a different compute board and camera. Hardware
      options:
  - **Option A (preferred):** Mobile base with mounted camera. Visually
    distinct from the arm workstation.
  - **Option B (backup):** Second workstation with different compute board
    (RPi vs Jetson) and different camera (webcam or Orbbec vs RealSense).
- [ ] Machine 2 has `viam-server` installed and is online but NOT configured
      (or minimally configured with just its local hardware)
- [ ] Objects (wrench, bolt) visible to both cameras
- [ ] `test_fleet.py` ready with both machine credentials

**NOTE on Option B:** If using a different camera model (e.g., webcam
instead of RealSense), the fragment's camera config won't match. To make
this work, either:
1. Use a fragment that specifies `webcam` instead of `realsense`, or
2. Use fragment overwrites to change the camera model on Machine 2.
Option 2 is actually better for the demo — it shows the overwrite
capability. But it adds complexity to the 90-second slot. Decide during
rehearsal.

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> One machine works. Now you need fifty of them running the same
> configuration. With Viam, you turn your working config into a fragment
> and apply it everywhere.

SHOT: Presenter. Two machines visible (or implied — one in frame, the
other referenced).

---

### DEMO — screen [0:10–1:15]

**Create a fragment [0:10–0:30]**

> Here's my working machine. It has a camera, an ML model, a detector,
> and the wrench-finder module. I want this exact setup on every machine
> in my fleet.

SHOT: Screen — CONFIGURE tab of Machine 1. Show the full config: camera,
ML model service, vision service, wrench-finder service.

> I create a fragment from this configuration. I give it a name and save.

SHOT: Screen — create fragment flow. Name it "wrench-detection-setup".
Save.

**Apply to a second machine [0:30–0:50]**

> Here's a second machine — different hardware, no configuration yet.
> I add the fragment.

SHOT: Screen — navigate to Machine 2 in the Viam app. CONFIGURE tab.
Add fragment "wrench-detection-setup". Save.

> viam-server on that machine downloads the modules, loads the model,
> and starts the services. Same behavior, different machine.

SHOT: Screen — Machine 2's LOGS tab. Modules downloading. Services
starting. The "Configured:" log line from the wrench-finder module.

CUT TO: Machine 2 — camera feed showing detections. (If mobile base:
the rover with a detection overlay on its camera feed.)

**Fleet-wide update [0:50–1:10]**

> Now I update the fragment — change the confidence threshold from 0.7
> to 0.5.

SHOT: Screen — edit the fragment. Change `confidence_threshold` from
`0.7` to `0.5`. Save.

> Both machines pull the update.

SHOT: Screen — FLEET view. Both machines online. Show logs from one
machine showing the reconfigure.

CUT TO: Brief CONTROL tab views of both machines showing detections.

---

### PAYOFF — face to camera [1:10–1:30]

> One fragment, any number of machines. Update once, deploy everywhere.
> That's how you go from prototype to production.

SHOT: Presenter. Both machines visible if possible.

---

## Validation notes

### Config accuracy (fragment-config.json)
- Fragment structure matches standard machine config — fragments are
  partial configs that merge into the machine's full config. Confirmed
  from docs and `config-xref.md` (fragments use the same component/
  service config schema).
- All service and component configs reuse validated configs from
  previous episodes.
- `depends_on` in the wrench-finder service — correct; viam-server
  resolves these before starting the service.

### Code accuracy (test_fleet.py)
- `asyncio.gather()` to check both machines concurrently — valid Python
  pattern
- All SDK calls verified in previous episodes
- Each machine gets its own `RobotClient` connection — correct; each
  machine has separate credentials

### Behavioral claims
- "create a fragment from configuration" — confirmed: fragments are
  partial configs stored in the Viam cloud and applied to machines
  via `fragment_ids` in the machine config
- "viam-server downloads modules, loads model" — confirmed from Flow 3:
  module lifecycle handles download and start on config change
- "both machines pull the update" — confirmed: when a fragment is
  modified, all machines using it receive the updated config on their
  next config check (typically within 15 seconds)
- Fragment config merge behavior — confirmed from flows.md: fragments
  merge into the machine config, with machine-level config taking
  precedence for overwrites

### UI references
- Fragment creation flow — exists in CONFIGURE tab
- FLEET view — confirmed route `/fleet`
- Fragment editing — exists in fleet management UI
