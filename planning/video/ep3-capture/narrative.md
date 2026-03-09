# Viam Essentials: Capture Data

**Duration target:** 90 seconds

---

## Pre-shoot checklist

- [ ] Machine from Ep 1-2 running (arm + camera online)
- [ ] Small objects on workbench: wrench, bolt, screwdriver (or similar)
- [ ] Viam app open, machine selected, CONFIGURE tab visible
- [ ] Data manager service NOT yet configured (will add on camera during demo)
- [ ] DATA tab in Viam app will be checked after capture starts

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> You need training data from your robot's camera. Normally that means
> building a capture pipeline, managing local storage, handling network
> dropouts. With Viam, it's a config change.

SHOT: Presenter at workbench. Objects (wrench, bolt) visible on the table
in front of the camera.

---

### DEMO — screen + workbench [0:10–1:15]

**Enable data capture [0:10–0:30]**

> In the CONFIGURE tab, I go to my camera and add a data capture method.
> I select GetImages, set the frequency to one image per second, and save.

SHOT: Screen capture — CONFIGURE tab. Click on "my-camera" component.
Find the data capture configuration section. Add method: `GetImages`.
Set `capture_frequency_hz` to `1`. Save.

> That's it. The camera is now capturing images to local storage, and
> syncing them to the cloud automatically.

NOTE: The data manager service is also needed. If not already configured,
the app may prompt to add it, or we add it explicitly. Show this briefly
if needed — "I'll add the data management service too" — then save.

**See data in the cloud [0:30–0:50]**

> Let me put some objects in front of the camera.

SHOT: Hands placing a wrench and bolt on the workbench in the camera's
field of view.

> After a few seconds, I switch to the DATA tab.

SHOT: Screen — DATA tab. Images are appearing in the gallery view.
Each image shows the workbench with the objects. Timestamps visible.

> Every image is tagged with the machine name, component, and timestamp.
> I can filter by time range, by component, or search by tags.

SHOT: Screen — show a quick filter action (filter by component name
"my-camera"). Gallery updates.

**Filtered capture [0:50–1:15]**

> But I don't want every frame. I only want images where something
> interesting is happening. I can add a vision service and use a filtered
> camera to capture only images with detections.

SHOT: Screen — CONFIGURE tab. Add a vision service (use `color_detector`
for simplicity — it's built-in and doesn't require an ML model).
Configure it to detect a specific color (the wrench color).

> Then I swap my data capture to use a filtered camera that only passes
> images when the detector fires.

SHOT: Screen — add the `filtered-camera` component
(`viam:filtered-camera`). Set the source to "my-camera", the vision
service, and the label+confidence. Enable data capture on the filtered
camera instead of the raw camera. Save.

> Now, only images with detected objects get captured and synced.

SHOT: Screen — DATA tab. Show that new images only appear when the wrench
is in frame. Move the wrench away — no new captures. Move it back —
captures resume.

---

### PAYOFF — face to camera [1:15–1:30]

> Configuration, not code. Capture what matters, filter out what doesn't,
> and it all syncs automatically.

SHOT: Presenter, objects on workbench behind them.

---

## Validation notes

### Config accuracy (machine-config.json)
- `service_configs` on component with `type: "data_manager"` and
  `capture_methods` array — confirmed from existing docs
  (`data/trigger-on-data.md:96-109`)
- `method: "GetImages"` for camera capture — confirmed from flows.md
  (data capture methods are component API method names)
- `capture_frequency_hz` field — confirmed from flows.md:18
- Data manager service config:
  - `api: "rdk:service:data_manager"` — confirmed
  - `model: "rdk:builtin:builtin"` — confirmed (built-in model)
  - `sync_interval_mins: 0.1` (6 seconds) — confirmed default from
    flows.md:28

### Behavioral claims
- "captures images to local storage, syncing to cloud automatically" —
  confirmed from Flow 1 in flows.md: collector writes to local capture
  files, sync goroutine uploads when connectivity allows
- "tagged with machine name, component, timestamp" — confirmed:
  `DataCaptureMetadata` proto includes component name, method, timestamp
- Local storage path defaults to `~/.viam/capture` — confirmed from
  flows.md:23
- Filtered camera behavior — confirmed from alert-on-detections.md:
  the `filtered-camera` module only passes images to data management
  when detection criteria are met

### UI references
- **CONFIGURE tab** — confirmed route
- **DATA tab** — confirmed route `/data`
- Data capture configuration on components — this is configured in the
  component's config panel in the CONFIGURE tab
- Gallery view in DATA tab — confirmed from route structure

### Filtered camera
- Module: `viam:filtered-camera` (confirmed: `viam/filtered-camera` in
  registry, corrected from old `erh/filtered-camera` namespace in
  previous docs work)
- Config attributes: `camera`, `vision_services` array with `vision`,
  `objects`/`classifications` label-to-confidence maps — confirmed from
  alert-on-detections.md
