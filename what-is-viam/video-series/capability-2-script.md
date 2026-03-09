# Capability #2: Operate from Anywhere
## 75-Second Video Script

**Learning Outcome:** "I can access and control my robot remotely without networking configuration"

**Demo Setup:** Machine from Ep 1 running (xArm 6 + cameras configured and online), presenter at a different location (different room, staged as home office or coffee shop), laptop with browser and terminal open, `demo_remote_connect.py` ready

---

## Script

### [00:00-00:10] Hook (10 seconds)

*Visual:*
- Presenter at laptop, clearly not next to the robot. Setting feels remote — different room, different lighting.

*Presenter:*
"Your robot is running in the lab. You're at your desk. Normally, remote access means VPN configs, SSH tunnels, and firewall rules. With Viam, you just connect."

---

### [00:10-00:30] Demo: Web App Control (20 seconds)

*Visual:*
- Screen capture — Viam app, CONTROL tab
- Live camera feed visible — the workbench from Ep 1, streaming in real time

*Presenter (voiceover):*
"I open the Viam app and navigate to my machine. Here's the CONTROL tab. I can see the live camera feed — that's the workbench, streaming right now from the machine in the other room."

- Screen — presenter jogs a joint using the arm control panel

*Presenter (voiceover):*
"I can move the arm from right here."

*CUT TO:* Wide shot of machine in other room — arm moves.

*CUT BACK:* Screen — camera feed shows arm in its new position.

---

### [00:30-00:50] Demo: Code Control (20 seconds)

*Visual:*
- Screen — terminal on laptop, `demo_remote_connect.py` briefly visible (connection lines and arm move command)
- Run the script

*Presenter (voiceover):*
"And it's not just the web UI. I can run code from my laptop too. Five lines to connect, read the camera, and move the arm. Same API whether I'm sitting next to it or across the country."

*Visual:*
- Terminal output appears:
  ```
  Got image: 640x480
  Current joints: [0.0, -45.0, -30.0, 0.0, 60.0, 0.0]
  Arm moved.
  ```

*CUT TO:* Wide shot — arm moves again.

### [00:50-00:55] Demo: Logs (5 seconds)

*Visual:*
- Screen — LOGS tab in Viam app, logs streaming, quick filter by "my-arm"

*Presenter (voiceover):*
"I can also stream logs in real time, filtered by component."

---

### [00:55-01:15] Payoff (20 seconds)

*Visual:*
- Back to presenter at laptop, brief and confident

*Presenter:*
"No VPN. No port forwarding. Viam handles the connection. Same app, same SDK, same APIs — from anywhere."

---

