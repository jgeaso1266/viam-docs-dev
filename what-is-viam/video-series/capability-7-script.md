# Capability #7: Scale Easily
## 60-Second Video Script

**Learning Outcome:** "One robot's config becomes 100 robots' config with zero scripting"

**Demo Setup:** 3 identical sensor stations (Raspberry Pis with cameras) physically located in different parts of the office, framed as "Quality Control Stations". Each station views a desk/area with multiple objects (cups, bottles, keyboards, mice, laptops). Initially detecting only cups and bottles. Viam app showing fragment management and fleet dashboard.

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter at laptop, one QC station visible in background

*Presenter:*
"You've configured one quality control station. Now you need to roll it out across your entire facility."

---

### [00:08-00:18] Explain Fragments (10 seconds)

*Visual:*
- Show one working QC station (camera viewing desk with objects)
- ML detection boxes visible on screen around cups and bottles only
- Screen showing its configuration in Viam app
- Station labeled "Zone A - Quality Control"

*Presenter (voiceover):*
"This is Zone A — one configured station, detecting cups and bottles. In Viam, that configuration can be saved as a fragment, which is a reusable template you can apply across your entire fleet."

---

### [00:18-00:32] Demo: Create and Apply Fragment (14 seconds)

*Visual:*
- Quick montage:
  - Screen — save Zone A config as a fragment in Viam app
  - Fragment appears in fragments list
  - Apply fragment to Zone B machine → provisions and starts detecting
  - Apply fragment to Zone C machine → provisions and starts detecting
  - All three stations now detecting cups and bottles

*Presenter (voiceover):*
"I apply that fragment to Zones B and C — two stations in different parts of the office. They provision automatically with the same configuration."

---

### [00:32-00:50] Demo: Update Propagation (The "Wow") (18 seconds)

*Visual:*
- Focus on Viam app showing fragment configuration
- Edit fragment: Change detected object classes from ["cup", "bottle"] to ["cup", "bottle", "keyboard", "mouse", "laptop"]
- Save fragment update
- Show fleet dashboard with all 3 stations:
  - Status indicators: "Updating..." on all stations
  - All stations pull new config simultaneously
  - **Visual change:** Detection boxes suddenly appear on keyboards, mice, and laptops across ALL stations
  - Each station keeps its zone label (A, B, C)
  - Dramatic and obvious - new object types now detected everywhere
- Timestamp showing update takes seconds

*Presenter (voiceover):*
"Now I update the fragment to detect more object types. Every station pulls the change automatically — and within seconds, detection boxes are appearing on new objects across all three locations."

---

### [00:50-00:60] Payoff (10 seconds)

*Visual:*
- Back to presenter on camera
- Screen — fleet dashboard showing all three stations in sync

*Presenter:*
"We used simple sensor stations here, but this same workflow applies to any system — robot arms, mobile robots, full production lines. Configure once, deploy everywhere, and update the entire fleet from one place."

