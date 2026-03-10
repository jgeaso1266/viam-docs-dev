# Capability #3: Capture Data from Edge to Cloud
## 90-Second Video Script

**Learning Outcome:** "Data collection is configuration, not code — and resilience is built in."

**Demo Setup:** Vino wine-pouring robot with two arms, each with a camera for glass detection. Not demonstrating pouring — using the setup to capture glass images for building a training dataset. Ethernet cable for network disconnect demo.

---

## Script

### [00:00-00:18] Hook (18 seconds)

*Visual:*
- Presenter on camera, Vino robot visible in background

*Presenter:*
"Capturing data from a robot is a few lines of code. Making it reliable is the real project. You need sync logic for intermittent connectivity, retry handling, disk management so you don't fill up an SD card and crash the OS.

And the failures are silent. Standard recording tools drop image data when they hit a throughput ceiling — no error, no warning. You find out the data is missing when you go to train a model.

Here's what it looks like with Viam."

---

### [00:18-00:35] Establish Setup + Config (17 seconds)

*Visual:*
- Presenter gestures to Vino robot
- Show both camera feeds briefly
- Show data capture config in Viam app — two cameras, frequency, method

*Presenter:*
"This is a wine-pouring robot with two arms. Each arm has a camera for glass detection. We're capturing images from both cameras to build a training dataset for the detection model.

Two cameras, two config blocks — capture frequency, capture method. That's it."

---

### [00:35-00:48] Demo: Data Flowing (13 seconds)

*Visual:*
- Cloud dashboard: images from both cameras appearing — glasses from two angles
- Data flowing automatically, thumbnails populating

*Presenter (voiceover):*
"Images from both cameras, flowing to the cloud. No collection code, no sync logic, no upload management. Just configuration running in the background."

---

### [00:48-00:58] Edge Filtering (10 seconds)

*Visual:*
- Stay on cloud dashboard showing glass images

*Presenter (voiceover):*
"If I wanted to filter out frames where a hand obscures the glass, I'd train a simple model on a small number of images and use it to filter at the edge. Unusable frames never leave the robot."

---

### [00:58-01:18] Demo: Resilience (20 seconds)

*Visual:*
- Cloud dashboard with data flowing from both cameras
- Disconnect network — visible action (unplug ethernet or toggle WiFi)
- Dashboard stops updating
- Beat. Let the viewer sit with it.
- Reconnect network
- Batch of images from both cameras appears in the dashboard

*Presenter (voiceover):*
"Disconnect the network. Data keeps capturing locally. Reconnect. Everything syncs. No retry code, no queue management, no error handling. Two cameras, both resilient, all from configuration."

---

### [01:18-01:30] Payoff (12 seconds)

*Visual:*
- Back to presenter on camera
- Vino robot visible in background

*Presenter:*
"No collection code. No sync logic. No storage management. Data capture is configuration in Viam. And it stays on in production — you keep capturing to improve the model over time. Configuration controls let you sync only in key situations, like failures."

---

## Production Notes

**Total time:** 90 seconds

**Pacing:**
- Hook is specific about the infrastructure tax — not "data pipelines are hard" but the exact things you have to build (sync logic, retry, disk management) and the exact way they fail (silent data loss).
- Setup establishment is brief — explain what the robot is and why we're capturing, then move on.
- Data flowing demo should feel effortless — thumbnails populating automatically.
- Edge filtering is mentioned, not demonstrated — keep it quick and practical.
- Resilience demo is the centerpiece. The network disconnect needs room to breathe. Let the viewer sit with "it's offline" before the reconnect.
- Payoff is short and direct. No taglines.

**The narrative arc:**
Data collection infrastructure is the real project, not the capture itself (hook) → This robot needs training data from two cameras (setup) → Configuration, data flows (demo) → Edge filtering is possible too (mention) → Network goes down, data survives (resilience) → All configuration, no code (payoff)

**Key messages:**
1. Data collection looks simple but the reliability engineering is months of work
2. Silent failures (dropped data, disk full, corrupt storage) are the worst kind
3. Viam makes data capture configuration — frequency, method, done
4. Resilience is built in — offline capture, automatic sync, no custom retry logic

**Tone:**
- The hook should feel like a warning from someone who's been burned — "you find out the data is missing when you go to train a model" is a specific, lived moment.
- The demo should feel casual — the ease is the point.
- The resilience demo should have a deliberate pause after the disconnect. Don't rush it.

**Connection to Capability 4:**
This video explicitly sets up capability 4 (Train and Deploy Models). We're capturing training data here. The next video shows what you do with it.

---

## Research Backing for Hook Claims

### Data pipeline infrastructure tax (validated March 2025 - March 2026):
- rosbag2 silently stops recording image and pointcloud2 topics after 10-60 seconds — SQLite backend hits throughput ceiling, drops large messages without error (GitHub rosbag2 #498)
- rosbag2 loses initial messages with ~20 publishers at 1000 msgs/sec due to non-deterministic topic discovery (GitHub rosbag2 #1430)
- rosbag2 corrupted chunks — "database image malformed," chunks fail to decompress (GitHub rosbag2 #1348)
- Azure IoT Edge documentation warns message queue "could easily exceed the available storage capacity and cause the OS crash"
- Neuracore (funded Nov 2025) built because teams spend months building "Frankenstein stacks" of disconnected data tools
- ARES project (a16z, 2025) exists because academic teams repeatedly rebuild ingestion/annotation infrastructure
- SD card corruption from power loss is the leading cause of data loss on Raspberry Pi (Hackaday, RPi Forums)

### How Viam solves it:
- Data capture config: component, method, frequency — no collection code
- Capture and sync decoupled: capture writes to local disk regardless of network
- Sync with exponential backoff: 200ms initial, 2x factor, max 1 hour. Offline detection backs off to 60 seconds.
- Automatic disk management: when disk hits 90% and capture dir >50% of usage, auto-deletes every Nth file
- Edge filtering: ML-filtered camera captures only useful frames; conditional sync via custom sensor
- Multiple sources independent: each component/method gets its own collector

---

## B-Roll Needed

- Vino robot on bench (not pouring — static but impressive)
- Both camera feeds showing glasses from different angles
- Close-up of ethernet cable being unplugged and plugged back in
- Presenter with robot in background

## Screen Recordings Needed

- Viam app: data capture config for both cameras (frequency, method)
- Cloud dashboard: image thumbnails appearing from both cameras
- Cloud dashboard: images including some with hands visible
- Cloud dashboard: data flow stopping after network disconnect
- Cloud dashboard: batch of images appearing after reconnect
- Clean, readable config

## Graphics/Overlays

- Camera labels if needed ("Camera 1 — Left Arm" / "Camera 2 — Right Arm")
- Network status indicator during resilience demo (optional — the cable unplug may be enough)
- Minimal aesthetic — let the data flow and the disconnect/reconnect tell the story
