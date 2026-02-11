# Capability Videos Planning

**Date:** 2026-02-10
**Status:** Initial Planning
**Owner:** Jalen

## Overview

Creating eight 60-second videos to educate experienced software engineers (with limited-to-no robotics experience) about Viam's core capabilities.

## Target Audience

- Experienced software engineers
- Limited-to-no robotics experience
- High curiosity and interest in robotics
- Familiar with modern software engineering practices (version control, APIs, deployment pipelines)

## The 8 Capabilities

From `what-is-viam.md`:

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
- Lead with value and possibilities, not problems
- Focus on learning outcomes
- Use existing projects (Chess, Vino) where appropriate
- **Build purpose-built demos** for capabilities not well-covered by existing projects
- Keep it positive - avoid "the old way" comparisons (audience hasn't done robotics before)
- 60 seconds max per video

**Demo Strategy:**
- **Existing Projects:** Use Chess and Vino for capabilities they demonstrate well
- **Purpose-Built Demos:** Create focused, simple demos for complex capabilities
- **Connected Narrative:** Link related capabilities (e.g., data capture → ML training)

**Content Structure per Video:**
- Learning outcome (what viewer should understand)
- What to show (specific demos with timing)
- The value (why it matters)
- Critical moment (the "aha" for software engineers)

## Available Projects Analysis

From `~/viam/build-on-viam/projects/`:

### Existing Projects
- **Chess** - Robot chess player (existing code, module published)
- **Vino** - Wine service robot (existing code at ~/viam/vino, has web ordering interface)

### New Projects (Hackathon Feb 24-26)
- **Barista** - Espresso robot
- **Inventory Tracker** - Zero-tagging vision tracking
- **Greenhouse** - Automated growing environment
- **Smart Lighting** - Intelligent office lighting
- **Retro Roomba** - Custom driver for old Roomba
- **Salad Maker** - Dual-arm salad assembly
- **Applesauce** - Apple processing robot
- **Rod Hockey Robot**
- **Dog**

### Project Status
Most projects are "New" status - **hackathon is Feb 24-26, 2026**

## Demo Strategy by Capability

| Capability | Demo Approach | Requirements | Confidence |
|------------|---------------|--------------|------------|
| **1. Hardware Integration** | Use Chess (existing) | Chess robot | ✅ Very High |
| **2. Remote Operation** | Use Chess or Vino (existing) | Chess or Vino robot | ✅ Very High |
| **3. Data Capture** | **Purpose-built**: Pi + camera | Pi, camera, ethernet cable | ✅ High |
| **4. Train/Deploy Models** | **Purpose-built**: Object detection (uses data from #3) | Same as #3 + training service | ✅ High |
| **5. Remote Development** | Use Chess (existing) | Chess robot | ✅ Very High |
| **6. Software Deployment** | Use Chess module OR **purpose-built**: LED blinker | Chess or Pi + LED | ✅ High |
| **7. Scale Easily** | **Purpose-built**: 2-3 identical sensor stations | 2-3 Pis + cameras | ✅ High |
| **8. Productize Apps** | **Purpose-built**: TypeScript web app | Build simple app, connect to Chess/Vino | ⚠️ Medium |

### Confidence Levels Explained

✅ **Very High**: Exists today, ready to film
✅ **High**: Can build quickly, minimal dependencies
⚠️ **Medium**: Buildable but requires effort or coordination
❌ **Low**: Major blockers or unknowns

## Purpose-Built Demo Details

### Capabilities #3 + #4: Connected Data Pipeline Demo

**Setup: Object Detection Station**
- Hardware: Raspberry Pi + USB camera
- Two objects: Coffee mug and water bottle
- Goal: Build detector that identifies which object is in frame

**Capability #3: Capture Data from Edge to Cloud**
- Configure camera data capture (3 lines of JSON)
- Capture images of mug and bottle alternating
- Images sync to cloud in real-time
- **Resilience demo**: Unplug ethernet → keep capturing → reconnect → auto-sync
- Result: 30+ images ready for training

**Capability #4: Train and Deploy Models**
- Open Viam app, view captured images
- Annotate: tag mug/bottle
- Click "Train Model" → training in cloud
- Model appears in registry as v1.0
- Deploy to Pi → real-time detection
- Train v2 with more data → deploy update → improved accuracy

**Why connected:** Shows complete workflow: capture → label → train → deploy

---

### Capability #6: Manage Software Deployments

**Option A: Use Chess Module (Recommended)**
- Chess module already exists and is published
- Push module update to registry
- Show Chess robot pulling update
- Modify config parameter (e.g., Stockfish skill level)
- Robot adjusts behavior in seconds without restart

**Option B: Purpose-Built LED Blinker**
- Simple module: LED that changes blink pattern based on config
- Push v1.0 → robot updates
- Change pattern in config → live reconfiguration
- Simpler but less impressive than Chess

---

### Capability #7: Scale Easily

**Purpose-Built: Fleet of Sensor Stations**
- 2-3 identical Raspberry Pis with cameras
- Create fragment from one working station
- Apply fragment to others → watch them provision
- Update fragment (change capture frequency)
- All stations update simultaneously

**Hardware needed:** 2-3 Raspberry Pis, cameras, network

**Alternative:** Show fragments concept with existing projects (Chess + Vino), even though they're different

---

### Capability #8: Productize with Viam Apps

**Purpose-Built: Simple Web Dashboard**
- Build minimal TypeScript app: "Robot Monitor"
- 15-20 lines of SDK code
- Features: login, camera feed, trigger button
- Connect to Chess or Vino
- **Critical moment:** Show code side-by-side with working app

**Key Questions:**
- What customer delivery features exist? (white-label auth, billing)
- Should we focus only on SDK → app, or show full customer delivery stack?

### 4. Project Readiness Timeline
**Critical Question:** When are videos being produced?

**Option A: Pre-Hackathon (before Feb 24)**
- Only Chess is reliable
- Most demos would need staging/mocks
- Risk: Inauthentic demos

**Option B: Post-Hackathon (after Feb 26)**
- Multiple projects should have MVPs
- More authentic demos
- Risk: Still may not have ML, fleet, or apps working

**Option C: Post-Quarter (after Q1)**
- Projects mature with backlog items
- High confidence in all 8 capabilities
- Risk: Delays video launch significantly

## Critical Questions to Answer

1. **Timeline**: When must these videos be ready? What's the launch date?
2. **Project Dependencies**: Which projects will be in working state by video production?
3. **ML Capability**: Do we have ANY working ML pipeline example, or should we stage it?
4. **Fleet Capability**: Will we have 2+ instances of any project for fleet demo?
5. **Customer Apps**: Will any customer-facing app be built, or should we mock it?
6. **Authenticity vs Speed**: Is it acceptable to stage/mock demos, or must everything be real?

## Recommended Approach: Mix of Existing + Purpose-Built

### Ready Today (Can Film Immediately)
- **#1 Hardware Integration**: Chess (existing)
- **#2 Remote Operation**: Chess or Vino (existing)
- **#5 Remote Development**: Chess (existing)

### Build Purpose-Built Demos (Week 1)
- **#3 Data Capture**: Pi + camera setup
- **#4 Train/Deploy Models**: Use data from #3
- **#6 Software Deployment**: Chess module update (preferred) OR LED blinker

### Build Purpose-Built Demos (Week 2)
- **#7 Scale Easily**: 2-3 Pi sensor stations
- **#8 Productize Apps**: Simple TypeScript web app

**Hard Constraint: 2 weeks to production-ready**

## Next Steps

### Critical Questions (Need Answers ASAP)
1. **Customer Delivery Features**: What actually exists today for Capability #8? (white-label auth, billing, or just focus on SDKs?)

### 2-Week Execution Plan

**Week 1: Build Core Demos**
- Day 1-2: Set up Pi + camera for data capture demo (#3)
- Day 2-3: Capture data, test ML training workflow (#4)
- Day 3-4: Prepare Chess module update (#6)
- Day 4-5: Start TypeScript web app (#8)

**Week 2: Build Fleet Demo + Finalize**
- Day 1-3: Set up 2-3 Pi stations for fleet demo (#7)
- Day 3-4: Complete TypeScript web app (#8)
- Day 4-5: Test all demos, prepare for filming

**Production**: All demos ready for filming by end of Week 2

## Production Decisions

**Format:** ✅ Confirmed
- 60 seconds per video
- On-camera presenter: Shannon Bradshaw, Head of Education
- Mix of presenter talking head and screen recordings/B-roll
- No narration over demos - presenter provides context

**Timeline:** ✅ Confirmed
- 2 weeks to production-ready

**Budget:** ✅ Confirmed
- No budget constraints

## Open Questions

- Who is producing these videos? (Internal team, agency, contractor?)
- What's the distribution channel? (Website, YouTube, social, sales deck?)

---

## Appendix: Detailed Capability Outlines

### 1. Get Hardware Running in Minutes

**Status:** ✅ Script complete - see `capability-1-script.md`

**Learning outcome:** "I can add hardware without writing drivers or dealing with dependencies"

**Demo approach:** Presenter-led with Chess robot

**What to show:**
- Presenter introduces challenge (driver hunting, SDK installation)
- Fast-paced montage: Plug in camera → add config → camera works
- Continue pattern: Arm and gripper, same process
- Robot playing chess (proof it all works)
- Presenter emphasizes: "Same pattern you use for databases and APIs"

**The value:** Hardware setup feels like software config you already know - no special tooling required

**Key message:** Config-driven architecture that software engineers already trust works for hardware too

**Critical moment:** Robot working after just adding config - no driver installation, no compilation, just configuration

**Format:** 60 seconds, presenter on camera with robot demonstrations

---

### 2. Operate from Anywhere

**Learning outcome:** "I can access and control my robot remotely without networking configuration"

**What to show:**
- Developer on laptop connects to robot across networks
- Live camera feed streaming from remote robot
- Real-time log viewing and filtering
- Control robot from browser or run commands remotely

**The value:** Debug and operate as easily as using localhost

**Critical moment:** Control physical hardware from laptop on different network as naturally as opening a website

---

### 3. Capture Data from Edge to Cloud

**Learning outcome:** "Data collection is configuration, not code I have to write"

**What to show:**
- Configure data capture in 3 lines - component, frequency, filters
- Data flowing to cloud automatically
- Survives network interruptions (disconnect/reconnect demo)
- Query across entire fleet by time, location, tags

**The value:** Resilient data pipeline with zero custom code

**Critical moment:** Network disconnects and reconnects - data sync continues seamlessly

---

### 4. Train and Deploy Models

**Learning outcome:** "ML deployment uses the same workflow as code deployment"

**What to show:**
- Select data → annotate → train with one click
- Training happens in cloud (no GPU setup)
- Model appears as versioned registry asset
- Deploy to robots instantly
- Inference runs on-device in real-time
- Pin versions or allow auto-updates

**The value:** ML models managed like npm packages

**Critical moment:** Deploy model update to fleet, rollback version with one click

---

### 5. Develop Code Remotely

**Learning outcome:** "I can develop against robot hardware like it's a cloud API"

**What to show:**
- Write code on laptop that controls remote robot
- Edit script in local IDE
- Run script - robot moves immediately
- Access live camera feeds in code
- Iterate instantly with no deployment

**The value:** Development feels like building a web app

**Critical moment:** Code change → run → robot responds in <1 second

---

### 6. Manage Software Deployments

**Learning outcome:** "Code deployment has version control and lifecycle management built-in"

**What to show:**
- Package code as module, push to registry
- Robots auto-update to new versions
- Lifecycle managed: starts on boot, restarts on failure
- Live reconfiguration - change parameters, app adjusts instantly
- Version pinning and semantic versioning

**The value:** Production-grade deployment from day one

**Critical moment:** Adjust config parameter in UI, robot behavior changes in 2 seconds with no restart

---

### 7. Scale Easily

**Learning outcome:** "One robot's config becomes 100 robots' config with zero scripting"

**What to show:**
- Working robot → export as fragment → reusable template
- Apply to multiple robots simultaneously
- All provision automatically
- Update fragment, all robots pull changes
- Per-robot overrides for site-specific differences
- Incremental rollout and instant rollback

**The value:** Fleet management that scales linearly

**Critical moment:** Update one fragment, watch it propagate to dozens of robots in real-time

---

### 8. Productize with Viam Apps

**Learning outcome:** "Customer-facing infrastructure is provided, I just build the product"

**What to show:**
- Build customer apps with provided SDKs and infrastructure
- Custom-branded authentication
- TypeScript/Flutter SDKs for web/mobile
- 10 lines of code → full customer dashboard
- Built-in billing and invoicing
- Customer fleet management UI

**The value:** Ship product features, not infrastructure

**Critical moment:** Full-featured customer dashboard running from minimal SDK code - "this 10 lines = this entire interface"
