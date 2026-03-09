# Capability #4: Train and Deploy Models
## 60-Second Video Script

**Learning Outcome:** "ML deployment uses the same workflow as code deployment"

**Demo Setup:** Vino robot setup, Viam app open in browser, glass fullness detection model trained on data from Ep 3

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera, Vino setup in background

*Presenter:*
"You have images from your camera. Now you need a model that detects objects in those images — and it needs to run on the robot, not in the cloud."

---

### [00:08-00:18] Demo: Training (10 seconds)

*Visual:*
- Quick montage:
  - Captured glass fullness images in Viam app (from Ep 3)
  - Annotation interface — bounding boxes drawn around the glass
  - Click "Train Model"
  - Training job running in cloud

*Presenter (voiceover):*
"I take the images Vino captured, annotate them with bounding boxes, and kick off a training job. Viam handles the infrastructure — I don't need to set up a GPU or configure a pipeline."

---

### [00:18-00:52] Demo: Deploy and On-Device Inference (34 seconds)

*Visual:*
- Training completes, model appears in Viam Registry
- Add model to robot configuration in CONFIGURE tab → Save
- Robot pulls model
- CUT TO: camera feed with detection boxes appearing around the glass in real-time
- Move the glass, vary the fill level — detections update in real-time

*Presenter (voiceover):*
"When training completes, the model shows up in the registry. I add it to Vino's configuration, save, and the robot pulls it down automatically. Now inference is running on the device — the model is detecting the glass and its fill level in real-time, without any cloud round-trips."

---

### [00:52-01:00] Payoff (8 seconds)

*Visual:*
- Back to presenter on camera, Vino running inference in background

*Presenter:*
"From raw images to on-device inference — all within Viam, and all without managing any ML infrastructure yourself."
