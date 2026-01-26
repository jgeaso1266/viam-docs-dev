# Stationary Vision Tutorial - Planning Notes

Internal planning and authoring notes for the [Stationary Vision Tutorial](../try/stationary-vision/index.md).

---

## Blocks Used

From [block-definitions.md](./block-definitions.md):

**Foundation:**
- Connect to Cloud
- Add a Camera
- Capture and Sync Data
- Start Writing Code

**Perception:**
- Add Computer Vision
- Detect Objects (2D)

**Stationary Vision:**
- Trigger on Detection
- Inspect for Defects

**Fleet/Deployment:**
- Configure Multiple Machines

**Productize:**
- Build a Customer Dashboard (TypeScript SDK)
- Set Up White-Label Auth
- Configure Billing

---

## Author Guidance

### UI Rough Edges to Address

Document and provide explicit guidance for:

- [ ] Account creation flow
- [ ] Finding the camera panel in the app
- [ ] Vision service configuration steps
- [ ] Data capture configuration UI
- [ ] Trigger configuration UI
- [ ] Fragment creation UI
- [ ] Fleet view navigation

### Key Teaching Moments

At each step, explicitly connect to transferable skills:

- "This is how you configure *any* component"
- "This pattern works for *any* sensor"
- "You'd do the same thing with a robot arm"

### Anti-Patterns to Avoid

- Don't let users think Viam is "just for cameras"
- Don't let steps feel like magic—explain what's happening
- Don't assume users will read linked docs—include essential context inline

---

## Open Questions

1. **Part appearance:** Timer vs. manual trigger? Timer feels realistic; manual gives control.

2. **ML model:** Pre-trained (provided) vs. walk through training? Pre-trained keeps focus on platform skills.

3. ~~**Alert mechanism:** What works without user setup?~~ **Resolved:** Using machine health trigger (offline alert) with email notification. Detection-based alerts deferred to Part 5.

4. **Second station:** Identical or slightly different? Identical is simpler; different shows fragment flexibility.

5. **Dashboard complexity:** How much web dev do we include? Keep minimal—point is Viam APIs, not teaching React.

6. **Mobile app control:** Consider introducing mobile SDK / remote control from phone somewhere in the tutorials. Could demonstrate controlling machines from anywhere.
