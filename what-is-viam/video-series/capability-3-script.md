# Capability #3: Capture Data from Edge to Cloud
## 60-Second Video Script

**Learning Outcome:** "Data collection is configuration, not code I have to write"

**Demo Setup:** Robot with camera (Pi + camera or Chess/Vino), laptop with Viam app, ethernet cable that can be unplugged for network disconnect demo

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera with robot setup in background
- Maybe show code editor or whiteboard with typical data pipeline architecture

*Presenter:*
"Building a data pipeline usually means writing collection code, sync logic, error handling, retry mechanisms. Let me show you what happens when you skip all that."

---

### [00:08-00:20] Demo: Configure Data Capture (12 seconds)

*Visual:*
- Screen recording: Viam app config interface
- Add data capture configuration block (JSON or UI)
- Show key parameters: component (camera), frequency (1Hz or similar), sync to cloud
- Simple, clean, just a few lines/fields

*Presenter (voiceover):*
"Configure data capture. Which component, how often. That's it. No collection code, no sync logic."

---

### [00:20-00:28] Demo: Data Flowing (8 seconds)

*Visual:*
- Split screen or quick cuts:
  - Camera capturing images (robot's view)
  - Data appearing in cloud dashboard (thumbnails or list)
- Show it's automatic and continuous

*Presenter (voiceover):*
"Data starts flowing. Edge to cloud. Automatically."

---

### [00:28-00:48] Demo: Resilience Test (20 seconds)

*Visual:*
- THIS IS THE KEY MOMENT - needs clear visual storytelling:
  - Hand unplugs ethernet cable from robot (or disconnect WiFi)
  - Overlay: "Network disconnected" or red indicator
  - Data still capturing locally (show local files accumulating or counter)
  - Wait a beat (show time passing - maybe 2-3 more images captured)
  - Hand plugs ethernet cable back in (or reconnect WiFi)
  - Overlay: "Network reconnected" or green indicator
  - Data automatically syncs to cloud (show files appearing in dashboard)

*Presenter (voiceover):*
"Unplug the network. Data keeps capturing locally. Reconnect. Everything syncs automatically. No code for retries, queuing, or error handling."

---

### [00:48-00:60] Payoff (12 seconds)

*Visual:*
- Back to presenter on camera
- Robot still visible in background
- Optional: Show cloud dashboard with all captured data

*Presenter:*
"Resilient data pipeline with zero custom code. Network interruptions, restarts, bandwidth constraints—all handled automatically."

*Final beat:*
"That's Viam."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Hook establishes the typical complexity of data pipelines
- Configuration demo should be quick and simple - the point is minimal setup
- Initial data flow shows it works automatically
- Resilience test is the heart of the video - needs clear visual indicators and enough time to show the full cycle
- Payoff reinforces the "zero code" message and resilience benefits

**The narrative arc:**
Data pipelines are complex → Configure in a few lines → Data flows automatically → Test resilience with network disconnect → Auto-sync on reconnect → Built-in resilience with no code

**Key message:**
Data collection is configuration, not code. Resilience is built-in - handles network interruptions, queuing, and sync automatically.

**Critical moment:**
The network disconnect/reconnect cycle showing data continues to capture offline and automatically syncs when connection returns. This proves the resilience story.

---

## Showing Local Data Accumulation During Network Disconnect

**Challenge:** If the machine is offline, we can't view it remotely. How do we prove data is still being captured locally?

### Option 1: Inference from Cloud Sync (Recommended)
- Show cloud dashboard with data flowing in real-time
- Disconnect network → cloud data stops appearing, show "disconnected" status
- Show timestamp/clock advancing (3-5 seconds pass)
- Reconnect network
- **Batch of images suddenly appears in cloud** (proves they were captured while offline)
- The quantity of synced images (e.g., 5 images from the offline period) proves local capture continued

**Pros:** Clean, elegant, no extra hardware needed
**Cons:** Requires trust in the timing/narration

### Option 2: Physical Local Display
- Have a monitor/screen connected to the robot showing local filesystem or capture counter
- Camera frames both the robot and its monitor
- When network disconnects, monitor visibly shows files/counter still increasing
- Provides direct visual proof even while network is down

**Pros:** Explicit visual proof, no trust required
**Cons:** Requires extra hardware setup, potentially cluttered frame

### Option 3: Trust + Timing Cues
- Don't show local files directly
- Visual sequence: disconnect → (show clock/timestamp advancing) → reconnect → data appears in cloud
- Narration explains "data keeps capturing locally"
- Rely on timing and narration to convey what's happening

**Pros:** Simple production, clean visuals
**Cons:** Weakest proof, requires audience trust

### Option 4: Split Recording
- Record robot's local view separately (SSH terminal or local UI showing files)
- Edit together: cloud dashboard + local terminal view side by side
- Show both perspectives simultaneously during disconnect

**Pros:** Comprehensive proof, shows both edge and cloud
**Cons:** More production/editing work, split screen may be busy

**Recommendation:** Use **Option 1** for elegance, or **Option 2** if explicit visual proof is important. Option 1 works well if narration clearly states "X images captured while offline" as they appear in batch.

---

## B-Roll Needed

- Robot with camera capturing data
- Close-up of ethernet cable being unplugged and plugged back in
- Hands disconnecting/reconnecting network
- Camera view showing continuous capture
- Wide shot of setup showing robot and network equipment

## Screen Recordings Needed

- Viam app config interface showing data capture configuration
- Data capture config being added/saved
- Cloud dashboard showing data appearing in real-time
- Local data accumulating during network disconnect (file list or counter)
- Data syncing to cloud after reconnect (files appearing)
- Final view of complete dataset in cloud

## Graphics/Overlays

- Network status indicators ("Connected" / "Disconnected")
- Visual cues for network state changes (green/red, icons)
- Timestamp or counter showing data capture continues during disconnect
- Clean transitions between local and cloud views
- Optional: Simple diagram showing edge device → cloud sync flow
