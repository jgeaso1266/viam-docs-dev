# Capability Videos Planning

**Date:** 2026-02-10
**Status:** Script Fine-tuning in Progress
**Owner:** Jalen

## Overview

Creating eight short videos to educate experienced software engineers (with limited-to-no robotics experience) about Viam's core capabilities.

## Target Audience

- Experienced software engineers
- Limited-to-no robotics experience
- High curiosity and interest in robotics
- Familiar with modern software engineering practices (version control, APIs, deployment pipelines)

## The 8 Capabilities

1. Get hardware running in minutes
2. Operate from anywhere
3. Capture data from edge to cloud
4. Train and deploy models
5. Develop code remotely
6. Manage software deployments
7. Scale easily
8. Productize with Viam apps

## Content Approach

**Key Principles:**
- Lead with value and familiarity, not problems
- Focus on learning outcomes
- Avoid "the old way" comparisons (audience hasn't done robotics before)
- Each video stands alone

**Content Structure per Video:**
- Hook (leads with value or familiar context)
- Demo (specific, timed sections)
- Payoff (generalizes the capability)

## Production Decisions

**Format:** ✅ Confirmed
- On-camera presenter: Shannon Bradshaw, Head of Education
- Mix of presenter talking head, screen recordings, and hardware shots
- Voiceover narration during demos — full natural sentences

**Duration:** Varies by capability (60–90 seconds)

---

## Demo Strategy by Capability

| Capability | Demo Approach | Hardware | Status |
|------------|---------------|----------|--------|
| **1. Hardware Integration** | xArm 6 + cameras + gripper on RPi | xArm 6, EMEET SmartCam, RealSense D435, gripper, Raspberry Pi | ✅ Script done |
| **2. Remote Operation** | Reuse Cap 1 machine | Same as Cap 1 | ✅ Script done |
| **3. Data Capture** | Vino robot, table camera, empty glass | Vino robot, table camera | ✅ Script done |
| **4. Train/Deploy Models** | Vino robot, glass fullness detection (uses data from #3) | Same as Cap 3 | ✅ Script done |
| **5. Remote Development** | Hand-eye calibration script (`hand-eye-test`) | Robot arm, depth camera, gripper | ✅ Script done |
| **6. Software Deployment** | Beanjamin barista robot, v1.0 → v1.1 | Beanjamin robot | 🔄 Pending engineer input |
| **7. Scale Easily** | 3 QC sensor stations in different office locations | 3x Raspberry Pi + cameras | ✅ Script done |
| **8. Productize Apps** | Greenhouse Viam app | TBD | 🔄 Pending details |

---

## Hardware Needed by Capability

### Cap 1 — Get Hardware Running in Minutes
- xArm 6 (ethernet connected to network)
- EMEET SmartCam (external, USB)
- Intel RealSense D435 (arm-mounted)
- Gripper (compatible with xArm 6)
- Raspberry Pi (viam-server pre-installed)

### Cap 2 — Operate from Anywhere
- Same machine as Cap 1 (no additional hardware)
- Laptop with browser and terminal (presenter's machine)

### Cap 3 — Capture Data from Edge to Cloud
- Vino robot (two arms)
- Table camera (pointed at glass during pour)
- Empty glass
- Ethernet cable (for resilience demo — unplugged and reconnected)
- Laptop with Viam app open

### Cap 4 — Train and Deploy Models
- Same Vino setup as Cap 3 (reuse)

### Cap 5 — Develop Code Remotely
- Robot arm with depth camera and gripper (hand-eye-test compatible setup)
- Object on workbench for pick test
- Laptop with terminal open, `hand-eye-test` binary ready

### Cap 6 — Manage Software Deployments
- Beanjamin barista robot
- Two versions of beanjamin module (v1.0 and v1.1 with visibly different behavior)
- *(Details TBD pending engineer conversation)*

### Cap 7 — Scale Easily
- 3x Raspberry Pi (viam-server pre-installed)
- 3x USB cameras
- Objects on each desk: cups, bottles, keyboards, mice, laptops
- Stations physically located in different parts of the office
- Laptop with Viam app open

### Cap 8 — Productize with Viam Apps
- Greenhouse project hardware *(TBD)*
- Laptop with demo app open

---

## Capability Outlines

### 1. Get Hardware Running in Minutes

**Status:** ✅ Script done — see `capability-1-script.md`
**Duration:** 90 seconds
**Learning outcome:** "I can add hardware without writing drivers or dealing with dependencies"
**Demo:** Add xArm 6, EMEET SmartCam, RealSense D435, and gripper via CONFIGURE tab. Test each in CONTROL tab. Payoff: hardware abstraction means swapping hardware doesn't change code.

---

### 2. Operate from Anywhere

**Status:** ✅ Script done — see `capability-2-script.md`
**Duration:** 75 seconds
**Learning outcome:** "I can access and control my robot remotely without networking configuration"
**Demo:** Open Viam app from a different room, view live camera feed, jog arm from CONTROL tab, run `demo_remote_connect.py` from laptop, stream logs filtered by component.

---

### 3. Capture Data from Edge to Cloud

**Status:** ✅ Script done — see `capability-3-script.md`
**Duration:** 65 seconds
**Learning outcome:** "Data collection is configuration, not code I have to write"
**Demo:** Add data management service, enable `GetImages` capture on Vino's table camera at 1Hz. Show images flowing into Data tab. Resilience demo: unplug ethernet → data keeps capturing locally → reconnect → batch syncs.

---

### 4. Train and Deploy Models

**Status:** ✅ Script done — see `capability-4-script.md`
**Duration:** 60 seconds
**Learning outcome:** "ML deployment uses the same workflow as code deployment"
**Demo:** Annotate glass fullness images from Cap 3, train model, deploy to Vino via CONFIGURE tab, show on-device inference detecting fill level in real-time.

---

### 5. Develop Code Remotely

**Status:** ✅ Script done — see `capability-5-script.md`
**Duration:** 60 seconds
**Learning outcome:** "I can develop against robot hardware like it's a cloud API"
**Demo:** Run `hand-eye-test pick` from laptop — robot detects object via point cloud, moves arm, closes gripper, lifts. Adjust `--approach-offset` flag and run again. Iterating on hardware in seconds, not hours.

---

### 6. Manage Software Deployments

**Status:** 🔄 Pending engineer input — see `capability-6-script.md`
**Duration:** 60 seconds
**Learning outcome:** "Code deployment has version control and lifecycle management built-in"
**Demo:** Beanjamin barista v1.0 running, develop v1.1 with visibly different behavior, push to registry, robot pulls update automatically.

---

### 7. Scale Easily

**Status:** ✅ Script done — see `capability-7-script.md`
**Duration:** 60 seconds
**Learning outcome:** "One robot's config becomes 100 robots' config with zero scripting"
**Demo:** Zone A station detecting cups and bottles. Save config as fragment, apply to Zones B and C in different office locations — both provision automatically. Update fragment to detect more object types — all three stations pull the change within seconds.

---

### 8. Productize with Viam Apps

**Status:** 🔄 Pending details — see `capability-8-script.md`
**Duration:** TBD
**Learning outcome:** "Customer-facing infrastructure is provided, I just build the product"
**Demo:** Greenhouse Viam app *(details TBD)*
