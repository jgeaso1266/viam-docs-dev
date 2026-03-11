# Capability #8: Productize with Viam Apps
## ~75-Second Video Script

**Learning Outcome:** "Customer-facing infrastructure is provided, I just build the product"

**Demo Setup:** Greenhouse Dashboard (`viam:greenhouse-dashboard`) — a real customer-facing Viam app with live sensor monitoring, light control, and camera feed connected to a greenhouse robot

---

## Script

### [00:00-00:15] Hook (15 seconds)

*Visual:*
- Presenter on camera

*Presenter:*
"Shipping a robotics product means building the robot — and then building all the infrastructure your customers expect from any software product: authentication, dashboards, connectivity. Getting all of that right takes months before a customer can even log in. Here's what it looks like when Viam handles it instead."

---

### [00:15-00:27] Show the App (12 seconds)

*Visual:*
- Screen — Greenhouse Dashboard running
- Sensors updating in real time (temperature, humidity, CO2, soil moisture)
- Live camera feed visible
- Presenter toggles the light on and off

*Presenter (voiceover):*
"This is the Greenhouse Dashboard — a customer-facing app built on Viam. Live sensor readings, a camera feed, and control over the greenhouse lighting. This is what the customer sees."

---

### [00:27-00:47] Codebase Reveal (20 seconds)

*Visual:*
- Code editor open on `main.ts` — full file visible (~410 lines)
- Scroll to lines 36–50: `THRESHOLDS` object and `healthClass` function
- Scroll to lines 262–273: light toggle click handler
- Scroll to lines 295–316: `pollSensors` reading env sensor, updating charts

*Presenter (voiceover):*
"This is the entire application — about 410 lines of TypeScript. Here are the health thresholds for temperature, humidity, CO2, and soil moisture. Here's the light toggle. Here's the sensor polling — reading live data and pushing it to the charts. No auth code, no connection management, no distribution logic. Just the product."

---

### [00:47-01:05] What Viam Provided (18 seconds)

*Visual:*
- Screen — Viam app showing machine picker UI
- Customer selects a greenhouse from the picker
- Screen — browser dev tools or Viam app settings showing credential injection via cookie
- Screen — Viam Registry showing `viam:greenhouse-dashboard` published

*Presenter (voiceover):*
"The machine picker — the UI that lets a customer select which greenhouse to connect to — is provided by Viam. Authentication is handled by Viam's proxy; the app reads credentials from a cookie, it never manages auth directly. And the app is published to the Viam registry and installed like any other module."

---

### [01:05-01:15] Payoff (10 seconds)

*Visual:*
- Back to presenter on camera

*Presenter:*
"You define what your customers need to see and build exactly that. Authentication, connectivity, distribution — all provided. The infrastructure between your robot and your customer is handled. You build the product."

---

## Production Notes

**Pacing:**
- Hook is on camera — deliver with conviction. The infrastructure tax is real and immediately recognizable to any engineer who has shipped a product.
- Show the App should feel like a customer using it — unhurried, natural. Let the live data speak.
- Codebase Reveal is deliberate — scroll slowly enough that viewers can read the section headers. The absence of auth/connection code is the point, not the presence of product code.
- What Viam Provided moves quickly through three beats — machine picker, auth, registry. Each should feel like a reveal, not a list.
- Payoff is short and direct. No taglines.

**The narrative arc:**
Shipping a robotics product requires building customer infrastructure too (hook) → Here's the finished product (show the app) → Here's everything the developer wrote — just product logic (codebase reveal) → Here's what Viam handled (what Viam provided) → You build what's differentiated (payoff)

**Key messages:**
1. The developer only wrote product logic — health thresholds, sensor polling, light control
2. Auth, machine picker, and distribution are provided by Viam — zero lines written for them
3. A Viam app is published and installed exactly like a module — same workflow, same registry

**Critical moment:**
The codebase reveal — scrolling through ~410 lines with no auth code, no connection management code, no distribution logic. The contrast between what the app does and how little infrastructure code it contains is the proof point.

**Tone:**
- Hook comes from genuine engineering experience — every engineer has rebuilt auth at least once.
- Demo should feel like a product, not a prototype. The greenhouse dashboard is real.

---

---

## Research Backing for Hook Claims

### Productization pain points (validated 2019–2025):
- Every robotics company rebuilds the same customer-facing infrastructure — auth, dashboards, connectivity — none of which is what customers pay for. "Each robotics startup independently recreates these capabilities in-house, reinventing the wheel over and over again. Very few of these capabilities provide differentiation." (Christian Fritz, Transitive Robotics founder, Medium)
- Building just the fleet management layer takes over a year and six engineers (Robotics 24/7; Logistics Business, citing Meili Robots industry report, 2023)
- Tennibot CEO: auth infrastructure "could only be done through a complex integration of platforms that weren't designed to work with machines — it progressively took time away from working on the machines themselves" (Viam customer story, 2024)
- IoT auth is two-tier — platform users AND customer app users — requiring multi-tenant identity management across both layers, plus device-level security for cameras and actuators in customer facilities (FusionAuth/Viam case study)
- Industry consensus: "Every robotics company builds substantially the same infrastructure" (Hacker News, August 2022)

### How Viam addresses these:
- Auth is handled by Viam's proxy — credentials are injected via cookie, the app never touches authentication logic
- Machine picker UI is provided by Viam — customers select their machine without the developer building fleet selection UI
- Distribution uses the same registry and module system as robot code — no separate deployment pipeline to build
- The developer writes only product logic — the Greenhouse Dashboard is ~410 lines of TypeScript with zero auth, connection, or distribution code

---

## B-Roll Needed

- Greenhouse hardware setup — sensors, smart plug, camera in place
- Close-up of plant with soil sensors visible
- Close-up of light toggling on and off

## Screen Recordings Needed

- Greenhouse Dashboard running — sensors updating in real time
- Live camera feed from greenhouse
- Light toggle — turning on and off, status updating
- Code editor showing `main.ts` full file (~410 lines)
- Scroll through: lines 36–50 (`THRESHOLDS`), lines 262–273 (light toggle), lines 295–316 (`pollSensors`)
- Viam app showing machine picker UI — customer selecting a greenhouse
- Browser dev tools or Viam app settings showing credential cookie injection
- Viam Registry showing `viam:greenhouse-dashboard` published

## Graphics/Overlays

- Callout annotations on code sections during codebase reveal (e.g. "health thresholds", "light toggle", "sensor polling")
- Highlight absence of auth/connection code — e.g. subtle overlay: "no auth code", "no connection management"
- Clean aesthetic — let the contrast between app complexity and codebase simplicity speak for itself

## Technical Requirements

- Greenhouse robot with all components configured and running before filming: `temp-moisture-sensor`, `soil-sensor-2/3/4`, `light-smart-plug`, `tent-camera`
- `viam:greenhouse-dashboard` published to Viam Registry before filming
- App installed on greenhouse machine and confirmed working end-to-end before filming day
- Machine picker confirmed working in Viam app UI
- Live sensor data and camera feed confirmed stable before filming day
