# Capability #1: Get Hardware Running in Minutes
## 90-Second Video Script

**Learning Outcome:** "I can add hardware without writing drivers or dealing with dependencies"

**Demo Setup:** xArm 6 on workbench (ethernet connected), EMEET SmartCam (external), Intel RealSense D435 (arm-mounted), Raspberry Pi with viam-server pre-installed, Viam app open in browser

---

## Script

### [00:00-00:10] Hook (10 seconds)

*Visual:*
- Presenter at workbench. xArm 6 visible but powered off. External camera nearby.

*Presenter:*
"Setting up a new robot arm usually means hunting down vendor SDKs, installing driver dependencies, and spending half a day on configuration before anything moves. With Viam, it takes about two minutes."

---

### [00:10-00:25] Demo: Create the Machine (15 seconds)

*Visual:*
- Screen capture — Viam app
- Click **+ Add machine**, type "demo-machine", click **Add machine**
- Copy setup command, cut to terminal on Raspberry Pi, paste and run
- Show viam-server starting (2-3 seconds of log output, then cut)

*Presenter (voiceover):*
"I'll start in the Viam app. I create a new machine — just give it a name. Viam gives me a setup command. I run it on my machine's terminal and viam-server starts."

---

### [00:25-00:45] Demo: Add the Arm (20 seconds)

*Visual:*
- Screen capture — CONFIGURE tab
- Click **+**, select **Component**, search "xArm6", select `viam:ufactory:xArm6`
- Name it "my-arm", set `host` to arm's IP address
- Click **Save** — show module downloading in logs (can be sped up in post)

*CUT TO:* Wide shot of arm — status LEDs come on as it initializes. Arm makes a small settling movement. Hold for a beat.

*Presenter (voiceover):*
"In the CONFIGURE tab, I search for xArm6 and add it. The only thing I need to set is the arm's IP address. I save, and viam-server pulls the driver from the Registry."

---

### [00:45-01:10] Demo: Add Remaining Components (25 seconds)

*Visual:*
- Fast montage, no narration — establish the pattern repeats:
  - Add EMEET SmartCam → Save → component appears in CONFIGURE tab
  - Add RealSense (arm-mounted) → Save → component appears in CONFIGURE tab
  - Add gripper → Save → component appears in CONFIGURE tab
- All four components now visible in CONFIGURE tab

*No narration — the pattern is self-evident*

---

### [01:10-01:22] Demo: Test Components (12 seconds)

*Visual:*
- Fast cuts through each component in CONTROL tab:
  - Arm: jog a joint — arm moves
  - External camera (EMEET): live feed appears showing workbench scene
  - Arm camera (RealSense): live feed appears showing arm's-eye perspective
  - Gripper: open/close — gripper responds

*Presenter (voiceover):*
"In the CONTROL tab, you can test each component to verify it works."

---

### [01:22-01:30] Payoff (8 seconds)

*Visual:*
- Back to presenter, arm visible in background in its jogged position

*Presenter:*
"Four components. Zero driver code. And because every arm, every camera, and every gripper in Viam speaks the same API, if I swap any of them for a different model or brand, my code doesn't change. Just update the config."

---

