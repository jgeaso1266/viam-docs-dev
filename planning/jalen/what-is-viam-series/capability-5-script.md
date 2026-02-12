# Capability #5: Develop Code Remotely
## 60-Second Video Script

**Learning Outcome:** "I can develop against robot hardware like it's a cloud API"

**Demo Setup:** Chess robot (xArm 7, gripper, camera), laptop with code editor (VS Code or similar), Python script using Viam SDK to control chess

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera with laptop in foreground, chess robot visible in background (different location/room)
- IDE visible on laptop screen showing code

*Presenter:*
"Test your robot code as fast as you test web code. Write it, run it, see results instantly. Let me show you."

---

### [00:08-00:20] Demo: Write and Run Code (12 seconds)

*Visual:*
- Close-up of IDE showing simple Python code:
  ```python
  chess = Generic.from_robot(robot, "chess")
  await chess.do_command({"move": {"from": "e2", "to": "e4"}})
  ```
- Show command: `python test_move.py` in terminal
- Split screen or cut to: Robot executes move (e2 to e4)
- Show it happens immediately

*Presenter (voiceover):*
"Write code on your laptop. Run it. Robot responds. No deployment, no file copying, just run."

---

### [00:20-00:35] Demo: Edit and Iterate (15 seconds)

*Visual:*
- Back to IDE
- Edit the code live - change to:
  ```python
  chess = Generic.from_robot(robot, "chess")
  await chess.do_command({"move": {"from": "d2", "to": "d4"}})
  ```
- Run again: `python test_move.py`
- Robot immediately executes the different move (d2 to d4)
- Emphasize the speed - instant iteration

*Presenter (voiceover):*
"Change the move. Run again. Instant feedback. Iterate in seconds, not minutes."

---

### [00:35-00:48] Demo: Add Complexity (13 seconds)

*Visual:*
- Back to IDE
- Add more code - multiple moves:
  ```python
  chess = Generic.from_robot(robot, "chess")
  await chess.do_command({"move": {"from": "e2", "to": "e4"}})
  await chess.do_command({"move": {"from": "g1", "to": "f3"}})
  ```
- Run: `python test_move.py`
- Robot executes both moves in sequence
- Shows building complexity with same workflow

*Presenter (voiceover):*
"Add complexity. Your code controls hardware over the network like it's calling an API."

---

### [00:48-00:60] Payoff (12 seconds)

*Visual:*
- Back to presenter on camera
- Chess robot still visible in background
- Optional: Show IDE and robot side-by-side

*Presenter:*
"Write, run, iterate. From your IDE. Against real hardware. The development workflow you already know."

*Final beat:*
"That's Viam."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Hook emphasizes speed and familiarity (testing web code)
- First demo shows basic write → run → respond cycle
- Second demo emphasizes iteration speed (the key differentiator)
- Third demo shows building complexity with same workflow
- Payoff reinforces "familiar workflow" message

**The narrative arc:**
Fast iteration like web dev → Write simple robot code → Run, robot responds → Edit and run again instantly → Build complexity with same speed → This is the development workflow you know

**Key message:**
Develop against robot hardware with the same fast iteration cycle as web development. Write, run, see results instantly from your local IDE.

**Critical moment:**
The second iteration (edit → run → robot responds with different move). This shows the speed of the feedback loop and proves you can iterate rapidly without deployment overhead.

---

## B-Roll Needed

- Chess robot executing moves (e2-e4, d2-d4, g1-f3)
- Multiple angles of arm moving pieces
- Close-up of gripper picking up and placing pieces
- Wide shot showing laptop and robot in same frame (or different locations)
- Robot executing sequence of moves

## Screen Recordings Needed

- Code editor (VS Code or similar) with clean Python script
- Code showing `Generic.from_robot(robot, "chess")`
- Code showing `await chess.do_command({"move": {...}})` with move dictionary
- Code being edited (changing move parameters - from/to squares)
- Terminal showing run command (`python test_move.py`)
- Code with multiple moves/sequence
- Clean, readable code - large font, good contrast

## Graphics/Overlays

- Code should be large and very readable
- Highlight the changed line when editing (optional subtle highlight)
- Chess notation (e2, e4, d2, d4) should be clear in code
- Split screen or smooth transitions between IDE and robot
- Optional: "No deployment" text overlay during first execution
- Optional: Timer showing < 1 second response time
- Minimal aesthetic - let the speed speak for itself

## Technical Considerations

**Making the Demo Clear:**
- Code should be minimal - just connection and move command
- Show the full edit → run → respond cycle at least twice
- Terminal output can show connection status or move confirmation
- Robot and laptop in different locations emphasizes "remote"
- Chess moves should be simple and different enough to be obvious

**Code Accuracy:**
- Uses actual Viam SDK: `Generic.from_robot(robot, "chess")`
- Uses actual chess module API: `await chess.do_command({"move": {"from": "e2", "to": "e4"}})`
- Chess notation is lowercase (e2, not E2)
- Focus visible code on robot control, not boilerplate
