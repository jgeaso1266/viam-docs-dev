# Capability #8: Productize with Viam Apps
## 60-Second Video Script

**Learning Outcome:** "Customer-facing infrastructure is provided, I just build the product"

**Demo Setup:** Custom-built customer-facing web app with fictional company branding, connected to Chess or Vino robot, demonstrating white-label auth, fleet management, robot control, and billing features

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera
- Screen showing infrastructure checklist: Auth systems, Billing, Customer portals, API access

*Presenter:*
"Building a robotics product means building customer infrastructure: auth, billing, dashboards, APIs. Or you can skip all that. Let me show you."

---

### [00:08-00:18] Demo: Customer Login (10 seconds)

*Visual:*
- Customer-facing app opens
- Branded login screen with fictional company logo and colors (e.g., "RoboClean" or "FleetBot")
- **Overlay/badge: "Example Customer App" or "Demo Company"**
- NOT Viam branding - clearly white-label
- Customer enters credentials and logs in
- Smooth transition to dashboard

*Presenter (voiceover):*
"Customer logs into your branded app. White-label authentication. Your brand, not Viam's."

---

### [00:18-00:30] Demo: Fleet Dashboard (12 seconds)

*Visual:*
- Customer dashboard showing robot fleet
- 2-3 robots visible with status (online, battery, location)
- Professional UI with company branding throughout
- Customer clicks on one robot to view details

*Presenter (voiceover):*
"Customer sees their robot fleet. Status, location, diagnostics. Fleet management UI provided. You didn't build this infrastructure."

---

### [00:30-00:44] Demo: Robot Control (14 seconds)

*Visual:*
- Robot detail view opens
- Live camera feed from robot (Chess or Vino)
- Control interface visible
- Customer sends command or interacts with robot
- Robot responds (arm moves, action executes)
- Clean, professional interface

*Presenter (voiceover):*
"Live camera feed. Control interface. API access to the robot. All provided. You built the robot features, Viam provides the connection."

---

### [00:44-00:52] Demo: Billing & Account (8 seconds)

*Visual:*
- Navigate to account/billing section
- Show subscription tier, usage metrics, payment information
- Professional billing interface

*Presenter (voiceover):*
"Billing, invoicing, payment processing. Built-in. You define pricing, Viam handles the rest."

---

### [00:52-00:60] Payoff (8 seconds)

*Visual:*
- Quick montage of all sections: Login → Dashboard → Control → Billing
- Overlay text showing: "✓ Auth", "✓ Billing", "✓ Fleet Management", "✓ API Access"
- Back to presenter

*Presenter:*
"Customer-facing infrastructure provided. You build product features, not infrastructure."

*Final beat:*
"That's Viam."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Hook establishes the infrastructure challenge
- Each section is fast but clear - showing what's provided
- Login → Dashboard → Control → Billing flow feels like real customer experience
- Payoff emphasizes "provided vs built" distinction

**The narrative arc:**
Building infrastructure is complex → Customer logs in (auth provided) → Views fleet (management provided) → Controls robot (API access provided) → Manages billing (payments provided) → You focus on product, not infrastructure

**Key message:**
Viam provides customer-facing infrastructure (auth, billing, fleet management, API access) so you can focus on building product features, not rebuilding infrastructure.

**Critical moment:**
The full customer experience showing all the infrastructure features working together - login, fleet management, robot control, billing - all provided, not built by you.

---

## Demo App Requirements

**Must Build:**
A customer-facing web application with the following features:

### 1. Branding
- Fictional company name and logo (e.g., "RoboClean", "FleetBot", "AutoServe")
- Consistent color scheme and branding throughout
- Professional UI/UX design (not prototype-looking)
- NO Viam branding visible in customer-facing app

### 2. Authentication
- Login screen with company branding
- Uses Viam authentication backend (white-label)
- Clean, professional login flow
- Username/password or similar

### 3. Fleet Dashboard
- Shows list/grid of robots with:
  - Robot names/IDs
  - Online/offline status
  - Location or zone (can be labels)
  - Optional: Battery, last active time
- 1 real robot (Chess or Vino)
- 1-2 additional mocked robots for fleet visualization
- Click on robot to view details

### 4. Robot Control Interface
- Live camera feed from robot
- Control interface (buttons, sliders, or similar)
- Ability to send commands to robot
- Robot responds visibly (arm moves, action executes)
- Real-time connection to actual robot

### 5. Billing/Account Section
- Displays subscription/pricing tier
- Usage metrics (can be static/mocked)
- Payment information display (can be mocked)
- Professional billing UI
- Does NOT need real payment processing - just UI

### 6. Technical Implementation
- Built with TypeScript + React or similar web framework
- Uses Viam SDK to connect to robot
- Responsive design (works on laptop screen for demo)
- Smooth navigation between sections
- Professional polish - this represents a customer product

---

## B-Roll Needed

- Clean shots of robot (Chess or Vino) that customer will control
- Close-ups of robot responding to commands from app
- Multiple angles of the web app on screen
- Professional-looking workspace with laptop running app

## Screen Recordings Needed

- Full customer login flow (start to finish)
- Fleet dashboard with robots visible
- Clicking on robot to view details
- Live camera feed from robot
- Sending control command and robot responding
- Navigation to billing/account section
- Billing interface display
- Smooth transitions between all sections
- Professional UI throughout - this is a product demo

## Graphics/Overlays

- **"Example Customer App" or "Demo Company" badge/overlay** - Make it clear this is fictional
- Fictional company logo and branding visible throughout
- Text overlays highlighting infrastructure: "✓ White-label Auth", "✓ Fleet Management", "✓ API Access", "✓ Billing"
- Clean, professional aesthetic
- Optional: Split screen showing app + robot simultaneously
- Emphasize: "Provided by Viam" vs "You built" distinction

## Technical Considerations

**App Development:**
- Timeline: Needs to be built before filming
- Scope: Full-featured enough to demonstrate all infrastructure
- Polish: Must look like a real product, not a prototype
- Real vs Mock: Robot connection and control must be real; other robots in fleet and billing can be mocked

**Infrastructure to Demonstrate:**
1. **White-label Auth** - Login screen with custom branding, no Viam branding
2. **Fleet Management** - Dashboard showing multiple robots with status
3. **API Access** - Live connection to robot, camera feed, control commands
4. **Billing** - Account/billing interface (can be mocked/static)

**Customer Experience Focus:**
- Frame everything from customer perspective
- Professional, polished UI - this is what end customers see
- Emphasize what you DIDN'T have to build (auth backend, billing system, fleet management infrastructure)
- Show it works like any professional SaaS product

**Robot Choice:**
- Chess or Vino (whichever is more reliable/photogenic)
- Must respond to commands from the app
- Live camera feed must work smoothly
- Consider: Chess might be more impressive (arm movement more visible than pouring)

**Realistic Complexity:**
- This is the most complex demo to build
- Requires web development expertise
- Plan adequate time for development and testing
- Focus on polish - this represents what customers would build
