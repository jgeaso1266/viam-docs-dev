# Capability #6: Manage Software Deployments
## 60-Second Video Script

**Learning Outcome:** "Code deployment has version control and lifecycle management built-in"

**Demo Setup:** Chess robot running chess module, Viam app showing registry and robot configuration, ability to push module updates and change config parameters

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera with chess robot in background
- Optional: Screen showing Viam registry with versioned modules

*Presenter:*
"Deploy to your robot like it's a server in the cloud. Let me show you."

---

### [00:08-00:20] Demo: Module v1.0 Running (12 seconds)

*Visual:*
- Show Viam Registry with chess module v1.0
- Show robot configuration using chess module v1.0
- Chess robot playing (executing a move)
- Show it's running and working

*Presenter (voiceover):*
"Chess module v1.0 deployed from registry. Robot pulls it, runs it. Lifecycle managed automatically."

---

### [00:20-00:35] Demo: Version Update (15 seconds)

*Visual:*
- Terminal showing: Push v1.1 to registry (or show registry UI with v1.1 appearing)
- Robot status showing update pulling/installing
- Robot now running v1.1
- Show improved behavior (maybe different chess strategy, faster move, or visible improvement)

*Presenter (voiceover):*
"Push v1.1 to registry. Robot pulls the update automatically. New version, improved behavior. OTA updates like you're used to."

---

### [00:35-00:50] Demo: Live Reconfiguration (15 seconds)

*Visual:*
- Open robot configuration in Viam app
- Show config parameter (e.g., "engine-millis": 10)
- Change it (e.g., to "engine-millis": 1000)
- Save configuration
- Robot immediately adjusts behavior (longer thinking time for chess move)
- Emphasize: No restart, instant change

*Presenter (voiceover):*
"Change a config parameter. Saves in seconds. Robot adjusts immediately. No restart, no redeployment."

---

### [00:50-00:60] Payoff (10 seconds)

*Visual:*
- Back to presenter on camera
- Chess robot still playing in background

*Presenter:*
"Version control for robot modules. OTA updates. Live reconfiguration. Production-grade deployment from day one."

*Final beat:*
"That's Viam."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Hook establishes familiarity with version control (npm/pip)
- Module v1.0 shows deployment and lifecycle management
- Version update shows OTA updates and version control
- Live reconfiguration is the unique capability - emphasize the speed
- Payoff ties together all three capabilities

**The narrative arc:**
Familiar version control → Module deployed and running → Push update, robot pulls it → Better behavior → Change config, instant adjustment → Production-ready deployment built-in

**Key message:**
Robot code deployment works like software deployment you already know: version control, OTA updates, and live reconfiguration without restarts.

**Critical moments:**
1. Robot auto-updating to v1.1 (proves version control/OTA)
2. Config change → behavior adjusts in 2 seconds (proves live reconfiguration)

---

## B-Roll Needed

- Chess robot playing (showing it's working)
- Chess robot making different moves (v1.0 vs v1.1 behavior)
- Close-ups of robot executing moves at different speeds/strategies
- Robot continuing to work during updates (if safe to show)

## Screen Recordings Needed

- Viam Registry showing chess module with version number (v1.0)
- Robot configuration showing module in use
- Terminal/CLI pushing v1.1 to registry (or registry UI showing new version)
- Robot status showing update in progress
- Robot configuration showing v1.1 now in use
- Configuration editor showing parameter (engine-millis or similar)
- Changing parameter value
- Save button/action
- Timestamp showing quick update (< 2 seconds)

## Graphics/Overlays

- Version labels (v1.0, v1.1) clearly visible
- "No restart required" text during live reconfiguration
- Optional: Timeline showing update speed
- Optional: Comparison between v1.0 and v1.1 behavior
- Clean, professional aesthetic

## Technical Considerations

**Module Version Update:**
- Use chess module with actual version numbers
- If showing CLI: `viam module upload --version 1.1.0`
- Show robot status/logs indicating update pulling
- Behavior difference should be visible (timing, strategy, or other observable change)

**Live Reconfiguration:**
- Use actual chess module config parameter (engine-millis, skill, or similar)
- Show before value and after value
- Timing should prove it's instant (< 2-3 seconds)
- Robot should visibly change behavior without restart
- Emphasize no restart/redeployment needed

**Making Both Clear:**
- Version update and live reconfiguration are different capabilities
- Version update = new code
- Live reconfiguration = same code, different parameters
- Both should be clearly labeled/distinguished in video
