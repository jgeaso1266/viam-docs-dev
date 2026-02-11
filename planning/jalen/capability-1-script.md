# Capability #1: Get Hardware Running in Minutes
## 60-Second Video Script

**Learning Outcome:** "I can add hardware without writing drivers or dealing with dependencies"

**Demo Setup:** Chess robot (xArm 7, gripper, Intel RealSense D435 camera)

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera, chess robot visible in background
- Hardware on desk (camera, arm, gripper - unplugged)

*Presenter:*
"Getting robot hardware running usually means hunting for drivers, installing SDKs, dealing with dependencies. Let me show you a different way."

---

### [00:08-00:28] Demo: Configuration (20 seconds)

*Visual:*
- Quick cuts, tight editing:
  - Plug in camera
  - Add camera config, save
  - Camera feed appears
  - Plug in arm
  - Add arm config, save
  - Arm moves in UI
  - Attach gripper
  - Add gripper config, save
  - Gripper works in UI

*Presenter (voiceover over the montage):*
"Three pieces of hardware. Three config blocks. Camera, arm, gripper."

---

### [00:28-00:45] Demo: Robot Working (17 seconds)

*Visual:*
- Chess robot in action:
  - Camera viewing board
  - Arm moves to piece
  - Gripper grabs
  - Arm moves piece
  - Gripper releases
  - Piece is now in new position

*No narration - let the robot working speak for itself*

---

### [00:45-00:60] Payoff (15 seconds)

*Visual:*
- Back to presenter on camera
- Robot still visible in background

*Presenter:*
"No driver installation. No compilation. Just configuration. The same pattern you use for databases and APIs works for hardware."

*Final beat - presenter gestures to robot:*
"That's it."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Presenter should be enthusiastic but not over-the-top
- Demo section (08-28s) should be fast-paced montage - we don't need to see every keystroke
- Robot working section (28-45s) is the proof point - no narration needed
- Closing drives home the familiarity angle

**The narrative arc:**
Setup seems complex → Actually it's just config → Proof it works → This is just like what you already do

**Key message:**
Hardware configuration uses the same config-driven pattern software engineers already know and trust. No special tooling, no driver hunting, just configuration.

---

## B-Roll Needed

- Clean shots of xArm 7 in action
- RealSense camera closeup
- Gripper grabbing chess piece
- Wide shot of full Chess setup
- Tight shots of USB cables being plugged in

## Screen Recordings Needed

- Viam app UI (component list, camera feed, control panel)
- Config file editing (clean, well-formatted JSON)
- Components appearing in UI after config save
- Testing components from browser UI

## Graphics/Overlays

- Config blocks should be clearly visible and readable
- Smooth transitions between shots
- Minimal, clean aesthetic
