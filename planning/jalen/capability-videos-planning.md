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
- Show actual working systems from Build on Viam projects
- Keep it positive - avoid "the old way" comparisons (audience hasn't done robotics before)
- 60 seconds max per video

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

## Capability-to-Project Mapping

| Capability | Best Project(s) | Project Status | Confidence |
|------------|----------------|----------------|------------|
| **1. Hardware Integration** | Chess, Inventory Tracker | Chess: existing<br>Inventory: new | ✅ High - Chess works |
| **2. Remote Operation** | Chess, Greenhouse | Chess: existing<br>Greenhouse: new | ✅ High - Chess works |
| **3. Data Capture** | Inventory Tracker, Greenhouse | Both new | ⚠️ Medium - Need Phase 1 working |
| **4. Train/Deploy Models** | Inventory Tracker | New, ML is Phase 2 | ❌ Low - ML may not be ready |
| **5. Remote Development** | Chess, Barista | Chess: existing<br>Barista: new | ✅ High - Chess works |
| **6. Software Deployment** | Chess, Retro Roomba | Chess: existing<br>Roomba: unknown | ⚠️ Medium - Need module updates |
| **7. Scale Easily** | Inventory Tracker, Greenhouse | Both new, fleet is core concept | ❌ Low - Need multiple stations built |
| **8. Productize Apps** | Vino, Barista | Vino: existing (app is backlog)<br>Barista: new | ❌ Low - Apps not implemented |

### Confidence Levels Explained

✅ **High**: Project exists and works, can film today
⚠️ **Medium**: Project planned, may be ready post-hackathon
❌ **Low**: Depends on features that may not be implemented

## Key Gaps & Risks

### 1. ML Pipeline (Capability #4)
**Problem:** Most ML features are backlog items across projects
- Inventory Tracker: Item recognition is Phase 2 (Phase 1 is capture-only)
- Barista: ML is for quality assessment (backlog)
- Chess: Piece recognition (backlog)
- Greenhouse: Ripeness detection (backlog)

**Options:**
- Wait for Inventory Tracker Phase 2 to be implemented
- Use a different existing Viam example with ML
- Film with placeholder/staged ML demo
- Skip this capability video for initial release

### 2. Fleet Management (Capability #7)
**Problem:** Requires multiple instances of the same project
- Inventory Tracker: Designed for multiple stations but need physical hardware
- Greenhouse: Multiple grow stations concept but need hardware

**Options:**
- Wait for multiple stations to be built
- Film with 2+ stations if available post-hackathon
- Use simulated/virtualized fleet demo
- Use fragments without showing actual fleet deployment

### 3. Customer Apps (Capability #8)
**Problem:** Requires customer-facing app to be built
- Vino: Has Streamdeck physical controls (existing), but TypeScript web app is backlog
- Barista: Tablet interface concept, not yet built
- All projects: Most are internal demos, not customer products

**Options:**
- Wait for Vino or Barista customer app to be implemented
- Build minimal example app specifically for video
- Use mock-ups/wireframes with SDK code examples
- Find existing Viam customer app example outside Build on Viam projects
- Skip for initial release

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

## Recommendations (Pending Answers)

### Conservative Approach (High Confidence)
Use only what exists and works today:
- **1-2, 5-6**: Use Chess (existing, working)
- **3**: Use any project with sensors/cameras (even if new)
- **4, 7-8**: Stage demos or use external examples
- **Timeline**: Can film immediately

### Moderate Approach (Post-Hackathon)
Wait for hackathon MVPs:
- **1-2, 5**: Chess or Barista
- **3**: Inventory Tracker or Greenhouse
- **4**: Inventory Tracker if Phase 2 ready, else stage
- **6**: Chess module updates
- **7-8**: Mock/stage or wait for implementation
- **Timeline**: March 2026

### Aggressive Approach (Wait for Features)
Wait for backlog items to be implemented:
- All 8 capabilities shown with real, working projects
- High production value, authentic demos
- **Timeline**: April-May 2026 or later

## Next Steps

1. **Clarify Timeline**: When are videos needed? What's the deadline?
2. **Assess Project Status**: After hackathon, which projects are demo-ready?
3. **Identify Gaps**: For capabilities we can't demo, decide: stage, mock, skip, or wait?
4. **Create Detailed Scripts**: Once projects are selected, write shot-by-shot scripts
5. **Production Planning**: Filming locations, equipment, who's filming

## Open Questions

- Who is producing these videos? (Internal team, agency, contractor?)
- What's the distribution channel? (Website, YouTube, social, sales deck?)
- Are we doing live-action filming or screen recordings?
- Do we need voice-over or on-camera presenters?
- What's the budget and production timeline?

---

## Appendix: Detailed Capability Outlines

### 1. Get Hardware Running in Minutes

**Learning outcome:** "I can add hardware without writing drivers or dealing with dependencies"

**What to show:**
- Add hardware in JSON config (3 lines: model, connection)
- Hardware appears in interface immediately
- Swap to different hardware brand - change model name, everything still works
- Show code accessing hardware - same API works with any brand

**The value:** Write once, work with any hardware

**Critical moment:** Swap camera brands mid-demo, code keeps running without changes

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
