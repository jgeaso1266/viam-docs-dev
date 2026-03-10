# Capability #5: Develop Code Remotely
## 70-Second Video Script

**Learning Outcome:** "I can develop against robot hardware like it's a cloud API — my laptop is my IDE, the robot is my test environment."

**Demo Setup:** Robot arm with depth camera and gripper, object on workbench for pick test, laptop with terminal open in a different room from the robot.

---

## Script

### [00:00-00:18] Hook (18 seconds)

*Visual:*
- Presenter at laptop, robot visible in background (different room or location)
- Terminal open on laptop

*Presenter:*
"In robotics, the development loop is broken. Write code, cross-compile, copy it to the robot, restart the service, walk over and watch. A one-line change can take minutes to test.

With Viam, your laptop is your IDE and the robot is your test environment. Write code, run it, hardware responds."

*Presenter guidance:*
- "The development loop is broken" — software engineers are used to: write code, run it, see results. In robotics, every iteration requires multiple extra steps. This isn't a minor inconvenience — Docker builds for robotics take up to 40 minutes, colcon build (the ROS 2 build system) takes 2+ minutes for a single package change, and can hang entirely. Three separate teams built ROS alternatives in 14 months (Basis, Copper, HORUS), all motivated by developer experience problems.
- "Cross-compile" — you develop on x86 (Mac or Linux), the robot runs ARM64. Cross-compilation adds a build step that frequently breaks. NVIDIA Isaac ROS 3 broke its own cross-compilation for Jetson (GitHub #86). Carnegie Mellon's AirLab built an entire Docker toolchain just to make it work.
- "Copy it to the robot" — scp, rsync, or a custom deploy script. Airbotics describes this as the baseline for most teams: "laborious, prone to operator error, not particularly secure."
- "Restart the service" — after copying code, you restart the robot's control process. In ROS 2, this means rebuilding with colcon build and relaunching nodes.
- "Walk over and watch" — without remote visualization, you physically observe the robot. Foxglove raised $40M in 2025 specifically to solve this visibility gap. Their pitch: "The gap between a robot failing and a developer understanding why is often measured in hours, if not days."
- "Your laptop is your IDE and the robot is your test environment" — Viam SDK connects to the robot over the network. Your code calls camera, arm, gripper APIs from your laptop. The robot executes. Same APIs whether the robot is on your bench or across the building.

---

### [00:18-00:28] Establish Setup (10 seconds)

*Visual:*
- Presenter gestures toward where the robot is (another room)
- Terminal visible on laptop

*Presenter:*
"I'm building a hand-eye calibration test — the script captures a point cloud from the camera, moves the arm to the detected object, and closes the gripper. The robot is in another room. I'm running the code from my laptop."

*Presenter guidance:*
- "Hand-eye calibration" — calibrating the relationship between where the camera sees an object and where the arm needs to move to reach it. This is a fundamental robotics task that requires many iterations to get right — exactly the kind of work where a fast development loop matters.
- "Point cloud" — a 3D representation of the scene captured by a depth camera. Each point has x, y, z coordinates. The script uses this to locate the object in 3D space.
- "The robot is in another room" — understated proof that this is remote. No SSH, no file copying. The Viam SDK connects over the network automatically.

---

### [00:28-00:43] Demo: Run the Script (15 seconds)

*Visual:*
- Screen — terminal on laptop, briefly show key lines:
  ```python
  camera.get_point_cloud()
  arm.move_to_position(pose)
  gripper.grab()
  ```
- Run the script
- CUT TO: Robot arm moves to object on workbench, gripper closes, arm lifts object
- CUT BACK: Terminal output showing results

*Presenter (voiceover):*
"Three SDK calls — point cloud, move, grab. Run it from my laptop. The arm moves, the gripper closes, the object lifts. No deploy step, no build step. Just run."

*Presenter guidance:*
- "Three SDK calls" — this is the key contrast with the hook. The development loop in Viam is: write Python, run Python. The SDK handles the network connection to the robot. These are the same APIs from capability 1 — camera, arm, gripper — now being called remotely as part of application logic.
- "No deploy step, no build step" — in the traditional workflow, you'd cross-compile, scp the binary to the robot, SSH in, restart the service. Here you just run a Python script on your laptop. The SDK connects to the robot's viam-server over WebRTC (same connection infrastructure from capability 2).
- The visual should linger on the robot responding — the arm moving in response to code run from a laptop in another room is the proof.

---

### [00:43-00:58] Demo: Iterate (15 seconds)

*Visual:*
- Screen — terminal, change a parameter: `--approach-offset 50`
- Run again
- CUT TO: Robot executes the pick again, slightly different approach angle
- CUT BACK: Terminal output showing updated offset measurements

*Presenter (voiceover):*
"I adjust a parameter and run it again. The robot responds immediately. This is the development loop — write, run, observe, adjust. Same as any other code, except the runtime is a robot."

*Presenter guidance:*
- "Adjust a parameter and run it again" — this is the iteration speed that matters. In the traditional workflow, changing one parameter means: edit, rebuild (2+ minutes in ROS 2), copy to robot, restart, observe. Here it's: edit, run. Seconds, not minutes.
- "Same as any other code, except the runtime is a robot" — this is the core message for software engineers. The development workflow they already know (IDE, run, observe, iterate) works unchanged. The robot is just another service their code talks to.

---

### [00:58-01:10] Payoff (12 seconds)

*Visual:*
- Back to presenter on camera
- Robot visible in background

*Presenter:*
"No cross-compilation, no file copying, no deploy step. Your laptop is your development environment. The robot is your test environment. Write code, run it, hardware responds."

*Presenter guidance:*
- "No cross-compilation, no file copying, no deploy step" — echoes the hook's pain points, now resolved. Each item was a step in the broken development loop. All three are gone.
- "Your laptop is your development environment. The robot is your test environment." — this reframes how software engineers should think about robotics development. It's the same separation they already have between their IDE and a staging server.
- "Write code, run it, hardware responds" — bookends with the hook. The repetition is deliberate — it's the thesis statement, stated at the start and proved by the demo.

---

## Production Notes

**Total time:** 70 seconds

**Pacing:**
- Hook is dense — catalogs the broken loop quickly, then immediately states Viam's answer. Two beats: the problem, the solution.
- Setup is brief — explain what the script does and that the robot is remote, then move on.
- Run demo should feel effortless — three lines of code, run, robot moves. The simplicity is the point.
- Iterate demo should feel fast — change a number, run again, robot responds. This is the development loop working the way software engineers expect.
- Payoff is short and bookends the hook. No taglines.

**The narrative arc:**
The robotics development loop is broken (hook) → I'm building a hand-eye calibration test, robot is in another room (setup) → Three SDK calls, run from laptop, robot responds (run) → Change a parameter, run again, iterate in seconds (iterate) → No cross-compilation, no deploy step, just write and run (payoff)

**Key messages:**
1. Traditional robotics development requires multiple steps between writing code and seeing results — cross-compile, copy, restart, observe
2. With Viam, your laptop is your IDE and the robot is your test environment
3. The Viam SDK connects to the robot over the network — same APIs regardless of where the robot is
4. Iteration speed is the same as any other software project

**Tone:**
- The hook should feel like a diagnosis — naming a problem software engineers will immediately recognize as the opposite of how they work.
- The demo should feel casual and fast — the speed is the point.
- The iterate section should feel like a normal development session — nothing special happening, which IS what's special.
- The payoff mirrors the hook. Clean closure.

**Connection to Capability 2:**
The network connection used here is the same WebRTC infrastructure from capability 2. The difference is framing: capability 2 is about operating and monitoring, capability 5 is about developing and iterating.

**Connection to Capability 6:**
When the code is ready for production, capability 6 shows how to package it as a module and deploy through the Registry — the next step after remote development.

---

## Research Backing for Hook Claims

### Development loop pain (validated March 2025 - March 2026):
- Docker builds for robotics: 40 minutes for full rebuild (Medium, Oct 2025)
- colcon build (ROS 2) on Raspberry Pi: ~45 minutes for full workspace
- colcon build for a single package change: 2+ minutes; bypassing colcon directly: ~7 seconds
- colcon build hanging entirely — freezing system or hanging after "completion" (GitHub ros2/examples #402, colcon/colcon-ros #122)
- Baseline workflow is SSH + scp: "laborious, prone to operator error" (Airbotics)
- Foxglove raised $40M in 2025 for remote robot visualization: "The gap between a robot failing and a developer understanding why is often measured in hours, if not days"
- NVIDIA Isaac ROS 3 broke cross-compilation for Jetson (GitHub NVIDIA-ISAAC-ROS/isaac_ros_common #86)
- Carnegie Mellon AirLab built Jetson-Robotics-Docker specifically to solve cross-compilation
- "Stop Fighting Your ROS 2 Environment" hit Hacker News front page (May 2025) — environment mismatch between dev machines and robots
- Three ROS alternatives built in 14 months (Basis Oct 2024, Copper Dec 2024, HORUS Nov 2025) — all motivated by developer experience problems

### How Viam solves it:
- SDK connects to robot over WebRTC — same connection infrastructure as capability 2
- Write Python/Go/TypeScript/Flutter on your laptop, run against remote hardware
- No cross-compilation — SDK runs natively on your dev machine, calls robot APIs over the network
- No file copying — code stays on your laptop, only API calls go to the robot
- No service restart — viam-server is already running, SDK connects to it
- Same APIs regardless of robot location — on your bench, across the building, or 30 miles away (capability 2)
- When ready for production, package as a module (capability 6)

---

## B-Roll Needed

- Robot arm with depth camera and gripper in one room
- Presenter at laptop in a different room
- Robot arm moving to object, gripper closing, lifting
- Robot executing pick with slightly different approach (second run)
- Terminal on laptop showing code and output

## Screen Recordings Needed

- Terminal: Python code showing three SDK calls (get_point_cloud, move_to_position, grab)
- Terminal: running the script, output appearing
- Terminal: changing approach-offset parameter
- Terminal: running again, updated output
- Clean, readable code — large font

## Graphics/Overlays

- Optional: room/location labels to emphasize the robot is elsewhere
- Code should be large and readable
- Minimal aesthetic — the speed and simplicity of the loop is the story
