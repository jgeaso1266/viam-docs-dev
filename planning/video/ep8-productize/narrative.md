# Viam Essentials: Productize with Apps

**Duration target:** 75 seconds

---

## Pre-shoot checklist

- [ ] At least one machine running with camera and detections working
- [ ] Web dashboard built and deployed (see `web-dashboard/README.md`)
  - Custom branding: fictional company logo and colors (e.g., "Wrench Watch")
  - Login page with custom branding via Viam OAuth
  - Fleet overview page showing machine status
  - Machine detail page with live camera feed
- [ ] Flutter mobile app built and running on a real phone
  - Same fleet overview and camera feed capability
  - Same fictional branding
- [ ] Billing configuration set up in Viam app (or use a test org with
      billing enabled)
- [ ] Laptop and phone available for filming

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> You've built a robotics product. Your customers need dashboards,
> authentication, maybe billing. You could spend months building all that.
> Or you could use what Viam already provides.

SHOT: Presenter at laptop.

---

### DEMO — screen [0:10–0:55]

**Web dashboard [0:10–0:30]**

> Here's a customer-facing dashboard I built with the TypeScript SDK.
> Notice the branding — this is my company's logo, not Viam's.

SHOT: Screen — web browser showing the "Wrench Watch" (or similar)
login page. Custom logo, custom colors. Clean, professional.

> I log in, and I see my fleet. Two machines, both online. I can click
> into one and see the live camera feed with detection overlays.

SHOT: Screen — log in. Fleet overview: two machines listed with green
"online" indicators. Click into Machine 1. Camera feed appears with
live detections ("wrench: 0.92").

**Mobile app [0:30–0:45]**

> Same thing on mobile. Here's a Flutter app with the same data.

SHOT: Phone screen — Flutter app showing the fleet overview. Same
branding. Tap into a machine. Camera feed streaming on the phone.

NOTE: Film the phone screen with the film camera for clean footage.
Don't rely on screen recording — the physical phone in someone's hand
is more compelling.

**Billing [0:45–0:55]**

> And Viam handles the billing infrastructure too. I set up pricing
> tiers — per-machine fees, data costs — and Viam handles invoicing.

SHOT: Screen — Viam app, billing configuration page. Show pricing tier
setup briefly. Don't dwell — just enough to establish the capability
(5-8 seconds).

---

### PAYOFF — face to camera [0:55–1:15]

> Auth, dashboards, mobile apps, billing. All built in. Ship your product,
> not your infrastructure.

SHOT: Presenter. Laptop and phone both visible.

---

## Validation notes

### Code accuracy (web-dashboard/src/app.ts)
- `createRobotClient` with `credentials: { type: "api-key", payload,
  authEntity }` — confirmed from docs.viam.com/operate/control/web-app/
- `signalingAddress: "https://app.viam.com:443"` — confirmed from docs
- `StreamClient` and `getStream(cameraName)` — confirmed from docs
- `machine.resourceNames()` — confirmed (returns resource name list)
- `machine.disconnect()` — confirmed cleanup method
- `CameraClient` constructor takes `(machine, name)` — confirmed from docs
- Package: `@viamrobotics/sdk` — confirmed from npm

### Behavioral claims
- "customer-facing dashboard with TypeScript SDK" — confirmed: the SDK
  supports web browser environments for building custom UIs
- "white-label authentication" — Viam supports custom OAuth branding.
  Needs verification of exact configuration steps for the demo.
- "Flutter SDK for iOS and Android" — Viam provides a Flutter SDK.
  The demo app needs to use the Flutter SDK, not just embed a web view.
- "billing infrastructure" — Viam app includes billing configuration.
  Confirmed from app route structure (`/billing`).

### Pre-production build items
1. **Web dashboard** (TypeScript + React or Svelte):
   - Login page with Viam OAuth, custom branding
   - Fleet page: list machines, show online/offline (poll `machineStatus`)
   - Machine detail: `StreamClient` for camera feed
   - Estimated effort: 2-3 days for a video-ready demo

2. **Flutter mobile app**:
   - Same fleet overview + camera stream
   - Uses Viam Flutter SDK
   - Estimated effort: 2-3 days for a video-ready demo

3. **Fictional company branding**:
   - Logo, color scheme, app name
   - Applied to both web and mobile apps
   - Estimated effort: half day with a designer

### UI references
- Billing configuration — confirmed route `/billing` in app
- OAuth/auth configuration — exists in organization settings
