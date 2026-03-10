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
- Presenter gestures to laptop screen

*Presenter:*
"This arm is in my home office in New Jersey. I'm in Manhattan. Thirty miles, two networks, a firewall I didn't configure."

---

### [00:30-00:45] Demo: Connection + Camera Feed (15 seconds)

*Visual:*
- Open Viam app in browser
- Robot appears in dashboard — online
- Click into robot
- Overhead camera feed from NJ home office streams immediately — arm visible

*Presenter (voiceover):*
"Open the app. Robot's there. Live camera feed from my home office. No VPN, no port forwarding, no separate video server. One connection."

---

### [00:45-00:58] Demo: Control + Code (13 seconds)

*Visual:*
- Send command from UI — arm moves in the overhead feed
- Switch to terminal/IDE, show:
  ```python
  arm = Arm.from_robot(robot, "my-arm")
  await arm.move_to_position(pose)
  ```
- Run it. Arm moves to new position in the feed. Live.

*Presenter (voiceover):*
"Move the arm from the UI. Or run code from my laptop. Same APIs, same connection. The robot is thirty miles away. Viam handles the entire network layer — your code just talks to the robot."

---

### [00:58-01:15] Payoff (17 seconds)

*Visual:*
- Back to presenter on camera
- Overhead feed still visible on laptop screen behind them

*Presenter:*
"No networking infrastructure to build. No VPN to maintain. Commands, camera feeds, logs — all one connection."

---

## Production Notes

**Total time:** 75 seconds

**Pacing:**
- Hook is dense — three specific pain points delivered with authority. This is a real problem the presenter has encountered.
- Setup establishment should feel casual and factual — "thirty miles, two networks, a firewall I didn't configure" is understated confidence.
- Connection demo should feel instant and effortless — that's the point. Don't linger.
- Control + code demo should breathe — the arm moving in the overhead feed 30 miles away is the proof. Let the viewer watch it happen.
- Payoff is short and direct. No taglines.

**The narrative arc:**
Remote access requires networking infrastructure you have to build (hook) → This robot is 30 miles away (setup) → Open the app, it's there, camera feed is live (connection) → Control it from UI or code, same connection (control) → No infrastructure to build or maintain (payoff)

**Key messages:**
1. Every robotics team ends up building networking infrastructure before they can do their actual work
2. Viam handles the entire network layer — commands, camera feeds, and logs over one connection, no VPN or port forwarding
3. Your code talks to the robot the same way whether it's on your bench or 30 miles away

**Tone:**
- The hook is empathetic — "your robot is deployed, something's not working" puts the viewer in a moment they've lived (roboticists) or can imagine (software engineers)
- The "networking infrastructure tax" framing connects to software engineers — they recognize the pattern from cloud infrastructure
- The demo is understated — no dramatic reveal, just casual control of hardware 30 miles away. The casualness IS the point.

**Critical moment:**
The arm moving in the overhead camera feed after running code from Manhattan. Live, unedited, 30 miles away. This is the proof that makes everything else credible.

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
- Arm moving in response to code execution (captured by overhead cam)
- Close-up of laptop screen showing Viam app and camera feed

## Screen Recordings Needed

- Viam app dashboard showing robot online
- Clicking into robot, camera feed appearing
- Overhead camera feed streaming live from NJ
- UI control panel — sending arm command
- Terminal/IDE showing Python code (2 lines — Arm.from_robot, move_to_position)
- Code execution and arm responding in camera feed
- Clean, readable code — large font

## Graphics/Overlays

- Location labels: "Viam HQ — Manhattan" / "Home Office — New Jersey" (brief, at setup)
- Optional: "~30 miles" text or simple map showing distance
- Camera feed should be raw/unpolished — the authenticity is the point
- Code should be large and readable
- Minimal aesthetic — let the live demo speak for itself

## Technical Requirements

- xArm 6 must be set up and running in NJ home office before filming day
- Overhead camera configured and streaming via Viam
- Reliable internet at both locations
- Test the full demo (UI control + code execution) before filming
- Have backup commands ready in case arm needs repositioning between takes
- Ensure overhead camera angle clearly shows arm movement
