# Capability #4: Train and Deploy Models
## 60-Second Video Script

**Learning Outcome:** "ML deployment uses the same workflow as code deployment"

**Demo Setup:** Robot with camera and trained ML model (object detection or classification), Viam app showing registry and model deployment, demo objects for inference

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera with robot in background
- Robot with camera, objects visible for detection demo

*Presenter:*
"If you've deployed code with version control and package managers, you already know how to deploy ML models to robots. Let me show you."

---

### [00:08-00:18] Demo: Training (Brief) (10 seconds)

*Visual:*
- Quick montage showing:
  - Captured data in Viam app
  - Annotation interface (bounding boxes or labels)
  - Click "Train Model"
  - Training job running in cloud

*Presenter (voiceover):*
"Select your data. Annotate. Train. Viam handles the infrastructure—no GPU setup, no pipeline configuration."

---

### [00:18-00:28] Demo: Model in Registry (10 seconds)

*Visual:*
- Training completes
- Model appears in Viam Registry
- Show it as versioned asset (v1.0)
- Looks like a code module in registry (semantic versioning visible)

*Presenter (voiceover):*
"Model appears in the registry as v1.0. Versioned like code. Ready to deploy."

---

### [00:28-00:43] Demo: Deploy and On-Device Inference (15 seconds)

*Visual:*
- Add model to robot configuration (quick config change)
- Robot pulls model
- **Show inference running in real-time:**
  - Camera feed with detection boxes or labels appearing
  - Objects being detected in real-time
  - Emphasize it's happening on-device (low latency, instant response)

*Presenter (voiceover):*
"Deploy to the robot. Inference runs on-device. Real-time detection. No cloud round-trips."

---

### [00:43-00:53] Demo: Update Deployment (10 seconds)

*Visual:*
- Deploy v2.0 of model to registry
- Robot automatically pulls update
- Show improved inference (better accuracy, new detections, or faster)
- Maybe side-by-side comparison or before/after

*Presenter (voiceover):*
"Train v2 with more data. Deploy the update. Robot pulls it automatically. Improved performance."

---

### [00:53-00:60] Payoff (7 seconds)

*Visual:*
- Back to presenter on camera
- Robot still running inference in background

*Presenter:*
"ML models managed like npm packages. Version control, instant deployment, on-device inference."

*Final beat:*
"That's Viam."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Hook establishes typical ML deployment complexity
- Training section is brief - just prove it's simple, not the focus
- Registry section shows familiar software workflow (versioning)
- On-device inference is a key moment - needs to show real-time performance
- Update deployment shows the lifecycle management (deploy, update, improve)
- Payoff reinforces the "like code modules" message

**The narrative arc:**
ML deployment is complex → Training is simple (quick mention) → Model as versioned asset → Deploy and run inference on-device → Update deployed seamlessly → ML models managed like code

**Key message:**
ML models are deployed and managed using the same workflow as code modules. On-device inference, semantic versioning, instant updates.

**Critical moments:**
1. On-device inference running in real-time (proves local execution, low latency)
2. Deploying v2 and seeing automatic update (proves familiar deployment workflow)

---

## B-Roll Needed

- Robot with camera performing object detection
- Close-ups of objects being detected
- Detection boxes/labels appearing in real-time on camera feed
- Multiple angles of inference running
- Robot performing action based on detection (optional, if relevant)

## Screen Recordings Needed

- Captured data in Viam app
- Annotation interface (bounding boxes or classification labels)
- Training job starting/running
- Model appearing in Registry with version number
- Registry interface showing model details (version, description)
- Robot configuration showing model being added
- Live inference view (camera feed with detections)
- Deploying v2.0 to registry
- Robot pulling update (status change or notification)
- Improved inference performance with v2

## Graphics/Overlays

- Version labels (v1.0, v2.0) when showing model updates
- "On-device" or "Local inference" indicator during inference demo
- Comparison indicators if showing v1 vs v2 performance
- Optional: Simple diagram showing model in registry → deployed to robot
- Clean, minimal aesthetic
