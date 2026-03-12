# Capability #6: Manage Software Deployments
## ~90-Second Video Script

**Learning Outcome:** "Code deployment has version control and lifecycle management built-in"

**Demo Setup:** Beanjamin barista robot, Viam app open in browser, two versions of the beanjamin module ready (v1.0 — silent during grind, v1.1 — speaks during grind)

---

## Script

### [00:00–00:16] Hook (16 seconds)

*Visual:*
- Presenter on camera, Beanjamin robot visible in background

*Presenter:*
"Updating your robot's software means SSH-ing in, pulling the latest code, and restarting — which can silently break other parts of your stack. And there's no standard way to push updates to a fleet. Viam replaces all of this."

---

### [00:16–00:53] Demo: Module v1.0 Running (37 seconds)

*Visual:*
- Wide shot of Beanjamin robot setup

*Presenter (voiceover):*
"This is Beanjamin — a robot barista."

*Visual:*
- Screen — Viam Registry showing beanjamin module v1.0

*Presenter (voiceover):*
"In Viam, code is packaged as a module and published to the registry. A module isn't just a script — viam-server manages its entire lifecycle: starts on boot, restarts on failure, updates automatically."

*Visual:*
- Screen — add module to robot configuration in CONFIGURE tab → Save
- Logs show module loading and starting

*Presenter (voiceover):*
"I add the beanjamin module to the robot's configuration, and the robot pulls it down automatically."

*Visual:*
- Screen — terminal showing:
  ```python
  coffee = Generic.from_robot(robot, "coffee")
  await coffee.do_command({"prepare_order": {"drink": "espresso", "customer_name": "Alice"}})
  ```
- Run it
- CUT TO: robot greets customer by name, runs brew sequence (grind, tamp, lock porta filter), announces order ready

*Presenter (voiceover):*
"Now when I call `prepare_order` via `do_command`, it greets the customer by name, runs the brew sequence — grinding, tamping, locking the porta filter — then announces when the espresso is ready. That's v1.0."

---

### [00:53–01:09] Demo: Version Update (v1.1) (16 seconds)

*Visual:*
- Screen — code editor showing `grindCoffee` in `espresso.go`, two `say` calls added at start and end of the method
- Terminal — `viam module upload --version 1.1.0`
- Screen — Viam Registry showing v1.1 available
- Screen — robot configuration updates to v1.1 automatically
- Logs show module reloading
- CUT TO: robot runs `prepare_order` again — speaks during grinding: "Grinding away..." → brews → "The grind is over."

*Presenter (voiceover):*
"I add two lines to the grind step — a spoken message at the start and end of the grind. I push v1.1 to the registry. The robot pulls the update automatically, no SSH, no restart. Same `do_command`, new behavior."

---

### [01:09–01:25] Payoff (16 seconds)

*Visual:*
- Back to presenter on camera, Beanjamin robot in background

*Presenter:*
"One command to publish. The robot updated itself. In Viam, robot software deploys the same way any other software does — versioned, distributed through a registry, applied without touching the machine. Every version is tracked, so you can pin or roll back."

---

## Production Notes

**Pacing:**
- Hook is specific and backed by real failure modes — deliver with authority, not speed
- v1.0 deployment section should feel methodical — registry, config, run. Each step is deliberate.
- v1.1 update should feel effortless by contrast — the point is that the robot updates itself
- Payoff is short and direct. No taglines.

**The narrative arc:**
Deploying robot software is a manual, fragile process (hook) → In Viam, code is a module — viam-server manages its lifecycle (v1.0) → Push a new version, robot pulls it automatically (v1.1) → Versioned, trackable, rollback-able (payoff)

**Key messages:**
1. A Viam module is not a script — viam-server owns its lifecycle (boot, failure recovery, updates)
2. Updates are pushed to the registry, not SSH'd to the robot
3. Every version is tracked — you can pin or roll back

**Critical moment:**
The robot pulling v1.1 automatically after `viam module upload`. No SSH, no restart command, no manual step — the behavior change is visible and audible.

**Tone:**
- Hook comes from genuine experience — DDS discovery failures and ad-hoc deployment scripts are real problems.
- Demo should feel calm and confident — the contrast with the hook is the point.

---

## Research Backing for Hook Claims

### Deployment pain points (validated 2021 - 2026):
- Restarting one ROS2 node silently breaks DDS discovery across the entire stack — other nodes stop communicating with no error message (GitHub ros2/rmw_fastrtps #509, February 2021)
- `apt upgrade` on a robot causes segfault at runtime in `ros2_control` — no warning before launch, failure only surfaces at runtime (GitHub ros-controls/ros2_control #1819, October 2024)
- No standard deployment approach exists — teams use 6+ incompatible toolchains (SSH/git, Ansible, RAUC, Mender, Docker, Balena) with no reference implementation (ROS Discourse — "The landscape of software deployment in robotics", March 2023)
- NSF 2024 workshop on Software Engineering for Robotics explicitly identified "upgrades management" as an unsolved problem for robot fleets (arXiv:2401.12317, January 2024)
- Manual SSH/git-pull deploy workflow does not scale past ~10 robots; described as "error prone" by practitioners (ROS Discourse #33884, October 2023)

---

## B-Roll Needed

- Wide shot of Beanjamin robot setup on bench
- Beanjamin running full `prepare_order` — greeting, brew sequence, order callout (v1.0)
- Beanjamin running `prepare_order` with grinding speech added (v1.1) — audible difference
- Close-up of arm during grind step (v1.0 silent vs v1.1 speaking)

## Screen Recordings Needed

- Viam Registry showing beanjamin module v1.0
- CONFIGURE tab — adding beanjamin module to robot configuration
- Logs showing module loading and starting after config save
- Terminal showing `do_command` call with `prepare_order`
- Code editor showing `grindCoffee` in `espresso.go` with two `say` calls added
- Terminal — `viam module upload --version 1.1.0`
- Viam Registry showing v1.1 available
- Robot configuration showing version updating automatically
- Logs showing module reloading to v1.1

## Graphics/Overlays

- Version labels (v1.0, v1.1) clearly visible during registry and config shots
- Minimal aesthetic — let the robot's audible behavior change speak for itself

## Technical Requirements

- beanjamin module v1.0 published to Viam Registry before filming
- beanjamin module v1.1 (with `say` calls in `grindCoffee`) built and ready to upload during demo
- `viam module upload --version 1.1.0` command tested and confirmed working before filming
- Robot must have speaker/audio output configured for TTS
- Confirm `prepare_order` do_command works end-to-end on the actual machine before filming day
