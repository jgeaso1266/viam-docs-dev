# Capability #7: Scale Easily
## ~70-Second Video Script

**Learning Outcome:** "One robot's config becomes 100 robots' config with zero scripting"

**Demo Setup:** 3 identical sensor stations (Raspberry Pis with cameras) physically located in different parts of the office, framed as "Quality Control Stations". Each station views a desk/area with multiple objects (cups, bottles, keyboards, mice, laptops). Initially detecting only cups and bottles. Viam app showing fragment management and fleet dashboard.

---

## Script

### [00:00-00:18] Hook (18 seconds)

*Visual:*
- Presenter at laptop, one QC station visible in background

*Presenter:*
"Configuring one robot is a solved problem. Scaling to fifty means touching each machine individually — and after enough field edits and ad-hoc patches, every robot ends up slightly different with no visibility into the gaps. In Viam, one configuration becomes a reusable template applied across your entire fleet. Update it once, every machine gets the change. Here's what that looks like."

---

### [00:18-00:28] Explain Fragments (10 seconds)

*Visual:*
- Show one working QC station (camera viewing desk with objects)
- ML detection boxes visible on screen around cups and bottles only
- Screen showing its configuration in Viam app
- Station labeled "Zone A - Quality Control"

*Presenter (voiceover):*
"This is Zone A — one configured station, detecting cups and bottles. That configuration is saved as a fragment."

---

### [00:28-00:42] Demo: Create and Apply Fragment (14 seconds)

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

### [00:42-01:00] Demo: Update Propagation (The "Wow") (18 seconds)

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

### [01:00-01:10] Payoff (10 seconds)

*Visual:*
- Back to presenter on camera
- Screen — fleet dashboard showing all three stations in sync

*Presenter:*
"We used simple sensor stations here, but this same workflow applies to any system — robot arms, mobile robots, full production lines. Configure once, deploy everywhere, and update the entire fleet from one place."

---

## Production Notes

**Pacing:**
- Hook is on camera — deliver with conviction, not speed. The "snowflake robot" problem is real and familiar to any engineer who has managed servers.
- Explain Fragments is brief by design — the hook already introduced the concept. This section just makes it concrete.
- Create and Apply Fragment should feel fast and effortless — the point is that B and C provision with zero manual config work.
- Update Propagation is the critical moment — let the visual breathe. The detection boxes appearing on new objects across all three locations simultaneously is the payoff of the whole demo.
- Payoff is short and direct. No taglines.

**The narrative arc:**
Scaling robot config is a manual, drift-prone process (hook) → In Viam, one config becomes a fragment (explain) → Apply it to a fleet, they provision automatically (apply) → Update the fragment, every machine gets the change instantly (wow) → Same workflow for any system at any scale (payoff)

**Key messages:**
1. Fragments are the source of truth — no config drift, no snowflake robots
2. Applying a fragment provisions a machine automatically — no SSH, no manual steps
3. One fragment update reaches the entire fleet in seconds

**Critical moment:**
Detection boxes appearing on keyboards, mice, and laptops across all three stations simultaneously after a single fragment edit. The visual change across multiple physical locations is the proof point.

**Tone:**
- Hook comes from genuine engineering experience — config drift and SSH-at-scale are problems every engineer has hit.
- Demo should feel calm and methodical — the contrast with the hook is the point.

---

## Research Backing for Hook Claims

### Fleet scaling pain points (validated 2020–2025):
- Manual fleet management becomes impossible past ~50 robots — "it quickly becomes impossible to manually keep track of everything happening with each robot" (Brain Corp, "5 Lessons Learned from Scaling the World's Largest AMR Fleet," August 2020)
- SSH-based workflows are "laborious, prone to operator error, not particularly secure, and lack traceability, reproducibility, and access controls" — they fall down as a fleet scales (Airbotics, "The Landscape of Software Deployment in Robotics," March 2023)
- Configuration drift: field engineers SSH in, edit YAML locally, edits don't sync back — every robot ends up with a unique config with no visibility into the gaps. Described as the "snowflake robot" problem. (Vedant Nair, Miru, "Why Server Automation Tools Fail at Robotics Configuration Management," May 2025)
- No standard solution exists — teams use 6+ incompatible toolchains; push-based tools (Ansible, Salt, Puppet) fail in robotics because robots can be offline, mid-task, or on restricted networks (Airbotics, March 2023; Miru, May 2025)

### How Viam addresses these:
- Fragments are the source of truth — no path for local edits to silently diverge from intended config
- No SSH needed — apply a fragment to a machine, it provisions automatically
- Pull-based updates — robots catch up when they reconnect, no coordinated deploy required
- Update a fragment once — every machine using it gets the change, fleet-wide, in seconds

---

## B-Roll Needed

- Wide shot of each QC station in its physical office location (Zone A, B, C)
- Close-up of each station's camera view with detection boxes on cups and bottles (v1)
- Each station's camera view after fragment update — detection boxes on keyboards, mice, laptops (v2)
- Fleet dashboard showing all three stations updating simultaneously

## Screen Recordings Needed

- Zone A station configuration in Viam app
- Saving Zone A config as the `qc-station` fragment
- Applying fragment to Zone B machine — provisions and starts detecting
- Applying fragment to Zone C machine — provisions and starts detecting
- Fragment editor — adding keyboard, mouse, laptop to `label_confidences`
- Saving fragment update
- Fleet dashboard showing all three stations pulling the change
- Detection boxes appearing on new object types across all three camera feeds

## Graphics/Overlays

- Zone labels (Zone A, Zone B, Zone C) visible during station shots
- Physical location callouts (e.g. "2nd floor", "lobby", "lab") to emphasize remoteness
- Highlight the fragment name (`qc-station`) in the Viam app during apply and update steps

## Technical Requirements

- 3x Raspberry Pi stations with USB cameras configured and running viam-server before filming
- Stations physically located in different parts of the office for visual impact
- ML model (`rdk:service:mlmodel`) and vision service (`rdk:service:vision`) configured on Zone A with `label_confidences` for cups and bottles
- `qc-station` fragment saved in Viam app before filming — covers camera, ML model, and vision service config
- Fragment applied to Zones B and C — confirm all three stations detecting cups and bottles before filming day
- Updated fragment (with keyboard, mouse, laptop added to `label_confidences`) prepared and tested before filming
- Fleet dashboard showing all three machines confirmed working before filming day

