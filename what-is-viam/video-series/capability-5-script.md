# Capability #5: Develop Code Remotely
## 60-Second Video Script

**Learning Outcome:** "I can develop against robot hardware like it's a cloud API"

**Demo Setup:** Robot arm with depth camera and gripper, object on workbench for pick test, laptop with terminal open, `hand-eye-test` binary ready

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter at laptop, robot visible in background (different room or location)
- Terminal open on laptop

*Presenter:*
"You're writing code that controls hardware. How do you test it? The same way you test any other code — you run it and see what happens."

---

### [00:08-00:25] Demo: Run the Script (17 seconds)

*Visual:*
- Screen — terminal on laptop, briefly show key lines from the script:
  - `camera.NextPointCloud()` to detect the object
  - `arm.MoveToPosition(pose)` to approach
  - `gripper.Grab()` to pick up
- Run: `./bin/hand-eye-test pick`

*Presenter (voiceover):*
"I'm building a hand-eye calibration test. The script calls the Viam SDK — it captures a point cloud from the camera, moves the arm to the detected object, and closes the gripper. I run it from my laptop."

*Visual:*
- CUT TO: Robot arm moves to object on workbench, gripper closes, arm lifts object
- CUT BACK: Terminal output:
  ```
  approach offset: 3.2mm
  world frame offset: 4.1mm
  grasp: success
  ```

*Presenter (voiceover):*
"From my laptop, I'm controlling an arm, a camera, and a gripper — all running on a machine in another room."

---

### [00:25-00:45] Demo: Iterate (20 seconds)

*Visual:*
- Screen — terminal, change a flag: `--approach-offset 50` (down from 100)
- Run again: `./bin/hand-eye-test pick`
- CUT TO: Robot executes the pick again, slightly different approach
- CUT BACK: Terminal output shows updated offsets

*Presenter (voiceover):*
"I adjust a parameter and run it again. The robot responds immediately. I'm iterating on hardware in seconds, not hours."

---

### [00:45-01:00] Payoff (15 seconds)

*Visual:*
- Back to presenter on camera, robot visible in background

*Presenter:*
"No deployment pipeline, no file copying, no waiting. Your laptop is your development environment, and the robot is your test environment. You write code, you run it, and the hardware responds."
