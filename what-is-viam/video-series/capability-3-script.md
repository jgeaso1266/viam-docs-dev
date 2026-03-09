# Capability #3: Capture Data from Edge to Cloud
## 65-Second Video Script

**Learning Outcome:** "Data collection is configuration, not code I have to write"

**Demo Setup:** Vino robot setup (table camera pointed at empty glass being filled with water), laptop with Viam app open in browser

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera, Vino setup in background

*Presenter:*
"Your robot is running. Now you want to capture what it sees — images, sensor readings, whatever you need for training or analysis. With Viam, that's just a config change."

---

### [00:08-00:20] Vino Intro (12 seconds)

*Visual:*
- Wide shot of Vino setup — two arms, table camera pointed at empty glass

*Presenter (voiceover):*
"This is Vino — a robot that pours drinks. During the pouring step, the camera on the table watches the glass as it's being filled to ensure it's not getting the perfect pour. We want to train a model to detect fullness levels."

---

### [00:20-00:37] Demo: Configure Data Capture (17 seconds)

*Visual:*
- Screen capture — CONFIGURE tab
- Add data management service → Save
- Camera component: data capture enabled, method `GetImages`, frequency 1Hz, Save

*Presenter (voiceover):*
"First, I add a data management service — that's what handles syncing captured data to the cloud. Then I go to the camera, enable data capture, and set the method and frequency. One image per second. Save."

---

### [00:37-00:49] Demo: Data Flowing (12 seconds)

*Visual:*
- CUT TO: Vino pouring water into the empty glass
- CUT TO: Screen — Data tab in Viam app, images from the table camera appearing as thumbnails

*Presenter (voiceover):*
"Viam starts capturing immediately. Images flow from the camera into the cloud — no sync code, no pipeline to build."

---

### [00:49-00:59] Demo: Resilience (10 seconds)

*Visual:*
- Screen — Data tab, images still flowing in
- Hand unplugs ethernet cable
- Screen — data stops appearing, machine shows offline
- Beat — a few seconds pass
- Hand plugs ethernet back in
- Screen — batch of images suddenly appears in the Data tab

*Presenter (voiceover):*
"Even when my machine is offline, data is still capturing locally, and the moment it reconnects — everything syncs automatically."

---

### [00:59-01:07] Payoff (8 seconds)

*Visual:*
- Back to presenter on camera, Vino in background

*Presenter:*
"That's all it takes. One camera, a data management service, and Viam handles everything else — capturing, syncing, and recovering from network interruptions automatically."
