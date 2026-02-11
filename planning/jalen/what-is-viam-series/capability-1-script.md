# Capability #1: Get Hardware Running in Minutes
## 60-Second Video Script

**Learning Outcome:** "I can add hardware without writing drivers or dealing with dependencies"

**Demo Setup:** Chess robot (xArm 7, gripper, Intel RealSense D435 camera + Orbbec Astra camera for swap)

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera, chess robot visible in background
- Hardware on desk (camera, arm, gripper - unplugged)

*Presenter:*
"Getting robot hardware running usually means hunting for drivers, installing SDKs, dealing with dependencies. Let me show you a different way."

---

### [00:08-00:23] Demo: Initial Configuration (15 seconds)

*Visual:*
- Quick cuts, tight editing:
  - Plug in Intel RealSense camera → add config → camera feed appears
  - Plug in arm → add config → arm moves in UI
  - Attach gripper → add config → gripper works in UI

*Presenter (voiceover over the montage):*
"Three pieces of hardware. Three config blocks. Camera, arm, gripper."

---

### [00:23-00:30] Demo: Robot Working (7 seconds)

*Visual:*
- Chess robot in action with RealSense camera:
  - Camera viewing board
  - Arm moves to piece, gripper grabs
  - Arm moves piece to new position

*No narration - let the robot working speak for itself*

---

### [00:30-00:42] Demo: Camera Swap (12 seconds)

*Visual:*
- Unplug Intel RealSense camera
- Plug in Orbbec Astra camera
- Update config (change model from "intel-realsense" to "orbbec-astra")
- Camera feed appears immediately with new camera

*Presenter (voiceover):*
"Swap the camera. Update the config. Same code, different hardware."

---

### [00:42-00:48] Demo: Robot Still Working (6 seconds)

*Visual:*
- Chess robot in action with Orbbec camera:
  - Same chess-playing behavior
  - Different camera, same result

*No narration - the point is clear*

---

### [00:48-00:60] Payoff (12 seconds)

*Visual:*
- Back to presenter on camera
- Robot with Orbbec camera still visible in background

*Presenter:*
"No driver installation. No code changes. Just configuration. Your code works with any hardware that speaks the same API."

*Final beat - presenter gestures to robot:*
"That's hardware abstraction."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Presenter should be enthusiastic but not over-the-top
- Initial config demo (08-23s) should be fast-paced montage - we don't need to see every keystroke
- First robot working (23-30s) proves the initial setup works
- Camera swap (30-42s) should be quick and smooth - the ease is the point
- Second robot working (42-48s) proves hardware abstraction - same behavior, different camera
- Closing drives home the abstraction benefit

**The narrative arc:**
Setup seems complex → Actually it's just config → Proof it works → Swap hardware with just config change → Still works → This is hardware abstraction

**Key message:**
Hardware abstraction through configuration. Change hardware without changing code. No driver hunting, no code rewrites, just configuration updates.

---

## B-Roll Needed

- Clean shots of xArm 7 in action
- Intel RealSense D435 camera closeup
- Orbbec Astra camera closeup
- Camera swap moment (unplugging RealSense, plugging in Orbbec)
- Gripper grabbing chess piece
- Wide shot of full Chess setup
- Tight shots of USB cables being plugged in/out
- Side-by-side shots showing both cameras work identically

## Screen Recordings Needed

- Viam app UI (component list, camera feed, control panel)
- Initial config editing - adding Intel RealSense camera (clean, well-formatted JSON)
- Components appearing in UI after config save
- Camera swap config change - changing model from "intel-realsense" to "orbbec-astra"
- Camera feed updating immediately after config change
- Testing components from browser UI (with both cameras)

## Graphics/Overlays

- Config blocks should be clearly visible and readable
- Highlight the model change in config: "intel-realsense" → "orbbec-astra"
- Smooth transitions between shots
- Minimal, clean aesthetic
- Optional: Small label showing which camera is active during each demo
