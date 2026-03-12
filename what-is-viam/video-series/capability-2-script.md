# Capability #2: Operate from Anywhere
## 75-Second Video Script

**Learning Outcome:** "Viam handles the entire network layer — my code just talks to the robot, regardless of where it is."

**Demo Setup:** xArm 6 with overhead camera in Shannon's home office (NJ). Presenter filming from Viam offices (NYC). ~30 miles, two networks, home firewall. Live demo — no faking the distance.

---

## Script

### [00:00-00:20] Hook (20 seconds)

*Visual:*
- Presenter on camera in Viam NYC office

*Presenter:*
"Your robot is deployed. Something's not working. You need to see the camera feed, check sensor readings, send a test command. But the robot is behind a firewall on a network you don't control. So before you can debug, you're setting up a VPN or configuring port forwarding — if your network even allows inbound connections.

This is so common that every robotics team ends up building networking infrastructure. It's a problem you have to solve before you can solve your actual problem. And even after you solve remote access, getting live video from the robot is a separate pipeline.

Here's what it looks like with Viam."

---

### [00:20-00:30] Establish the Setup (10 seconds)

*Visual:*
- Presenter gestures to laptop screen showing the overhead camera feed from NJ — arm visible in the feed
- The feed is already live, establishing that the connection exists before we explain it

*Presenter:*
"This arm is in my home office in New Jersey. I'm in Manhattan. Thirty miles, two networks, a firewall I didn't configure."

---

### [00:30-00:42] Demo: UI Control (12 seconds)

*Visual:*
- Viam app CONTROL tab — move the arm to a saved pose
- Overhead camera feed shows the arm moving in NJ

*Presenter (voiceover):*
"Move the arm to a saved pose from the UI. That's happening thirty miles away."

---

### [00:42-00:52] Demo: Camera + 3D View (10 seconds)

*Visual:*
- Switch to the arm-mounted camera feed — live view from the arm's perspective
- Switch to the 3D view — point clouds appearing in the scene

*Presenter (voiceover):*
"Switch to the arm camera. Live feed from the wrist, thirty miles away. And the 3D view — point clouds, live in the scene."

---

### [00:52-01:08] Demo: Remote Code (16 seconds)

*Visual:*
- Switch to terminal, show the code:
  ```python
  camera = Camera.from_robot(robot, "cam")
  images, _ = await camera.get_images()
  ```
- Run it. Image from the arm's camera pops up on the presenter's laptop screen — captured from 30 miles away.

*Presenter (voiceover):*
"Now run code from my laptop. Three lines — connect to the robot, grab an image from the camera. That image was captured thirty miles away. Same connection. No VPN, no port forwarding. Viam handles the entire network layer — my code just talks to the robot."

---

### [01:08-01:20] Payoff (12 seconds)

*Visual:*
- Back to presenter on camera
- Overhead feed still visible on laptop screen behind them

*Presenter:*
"No networking infrastructure to build. No VPN to maintain. UI control, camera feeds, point clouds, remote code — all one connection."

---

## Production Notes

**Total time:** ~80 seconds

**Pacing:**
- Hook is dense — three specific pain points delivered with authority. This is a real problem the presenter has encountered.
- Setup establishment should feel casual and factual — "thirty miles, two networks, a firewall I didn't configure" is understated confidence.
- UI control demo should feel instant — move to saved pose, arm responds in the feed. Don't linger.
- Camera + 3D view should feel like natural exploration — switching views, point clouds appearing. The viewer should feel the richness of the remote connection.
- Code demo should breathe — an image captured from thirty miles away, popping up on the presenter's laptop, is the proof. Let the viewer see it appear.
- Payoff is short and direct. No taglines.

**The narrative arc:**
Remote access requires networking infrastructure you have to build (hook) → This robot is 30 miles away, feed already live (setup) → Move the arm from UI (control) → Arm camera, point clouds, live 3D view (camera + 3D) → Run code remotely, grab an image from 30 miles away (code) → No infrastructure to build or maintain (payoff)

**Key messages:**
1. Every robotics team ends up building networking infrastructure before they can do their actual work
2. Viam handles the entire network layer — commands, camera feeds, and logs over one connection, no VPN or port forwarding
3. Your code talks to the robot the same way whether it's on your bench or 30 miles away

**Tone:**
- The hook is empathetic — "your robot is deployed, something's not working" puts the viewer in a moment they've lived (roboticists) or can imagine (software engineers)
- The "networking infrastructure tax" framing connects to software engineers — they recognize the pattern from cloud infrastructure
- The demo is understated — no dramatic reveal, just casual control of hardware 30 miles away. The casualness IS the point.

**Critical moment:**
The image popping up on the presenter's laptop after running three lines of Python from Manhattan — captured by a camera 30 miles away. Live, unedited. This is the proof that makes everything else credible.

---

## Research Backing for Hook Claims

### Networking infrastructure tax (validated March 2025 - March 2026):
- TurtleBot4 DDS UDP traffic detected as "UDP Flood/DDoS attack" by university firewall (GitHub turtlebot4 #673, Feb 2026)
- ROS 2 DDS Discovery Server becomes unresponsive at >75 participants (GitHub Fast-DDS #5767, Apr 2025)
- Tailscale exit node fails over 4G on Raspberry Pi 5 (GitHub tailscale #16877, Aug 2025)
- Tailscale gets stuck on weak WiFi: "need to find someone to power-cycle the device" (GitHub tailscale #12332, Jun 2024)
- Starlink uses CGNAT, making port forwarding impossible (2025)
- balena explicitly states SSH-over-cloud is "not designed for high availability"

### Camera streaming as separate problem (validated March 2025 - March 2026):
- Clearpath: single 720p camera at 30fps requires 660 Mbps uncompressed over ROS (Clearpath blog, Apr 2025)
- Polymath Robotics: prior tools caused "laggy videos, unbounded memory usage on robots" (LiveKit case study, recent)
- Transitive Robotics: WebRTC is "a hell of a task to implement on an end device" (blog, Oct 2023)

### How Viam solves it:
- WebRTC with STUN for NAT traversal. Viam Cloud is signaling server only — brokers handshake, then drops out. All traffic is peer-to-peer.
- Works through any firewall that allows outbound HTTPS. No inbound ports needed.
- Camera streaming: RTP/H264 over WebRTC data channels — not a separate video server
- SDK connection is 2 lines of Python
- Session safety: 20-second heartbeat, auto-stop on disconnect

---

## B-Roll Needed

- Presenter in Viam NYC office with laptop
- xArm 6 in NJ home office (overhead camera angle showing full workspace)
- Establishing shot of NYC office (optional — to emphasize location)
- Arm moving in response to UI commands (captured by overhead cam)
- Image from remote camera appearing on presenter's laptop after running code
- Close-up of laptop screen showing Viam app and camera feed

## Screen Recordings Needed

- Overhead camera feed streaming live from NJ (visible during setup)
- Viam app CONTROL tab — moving arm to saved pose
- Arm-mounted camera feed (live from wrist)
- 3D view with point clouds appearing in scene
- Terminal showing Python code (Camera.from_robot, get_images) and execution
- Image from remote camera appearing on presenter's laptop
- Clean, readable command — large font

## Graphics/Overlays

- Location labels: "Viam HQ — Manhattan" / "Home Office — New Jersey" (brief, at setup)
- Optional: "~30 miles" text or simple map showing distance
- Camera feed should be raw/unpolished — the authenticity is the point
- Python code should be large and readable
- Minimal aesthetic — let the live demo speak for itself

## Technical Requirements

- xArm 6 must be set up and running in NJ home office before filming day
- Overhead camera configured and streaming via Viam
- Reliable internet at both locations
- Test the full demo (UI control + code execution) before filming
- Have backup commands ready in case arm needs repositioning between takes
- Ensure overhead camera angle clearly shows arm movement
