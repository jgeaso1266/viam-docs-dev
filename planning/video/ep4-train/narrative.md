# Viam Essentials: Train and Deploy Models

**Duration target:** 90 seconds

---

## Pre-shoot checklist

- [ ] Machine running with camera configured and capturing data (from Ep 3)
- [ ] At least 50-100 images in the DATA tab (captured in Ep 3 with objects
      on workbench). Pre-capture these before the shoot — don't wait for
      real-time capture during filming.
- [ ] Some images pre-labeled with bounding boxes (wrench, bolt). Label
      most beforehand, leave 2-3 unlabeled for live demo.
- [ ] Training job pre-completed. Have a trained model version ready in the
      Registry. During filming, show the "training complete" state, not the
      actual wait.
- [ ] Objects (wrench, bolt) available on workbench for live detection demo.
- [ ] `test_detection.py` ready on laptop.

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> You have images from your camera. Now you need a model that detects
> objects on those images — and it needs to run on the robot, not in the
> cloud.

SHOT: Presenter at workbench. Wrench and bolt visible.

---

### DEMO — screen [0:10–1:15]

**Label data [0:10–0:30]**

> In the DATA tab, I select a batch of images and start labeling. I draw
> bounding boxes around each object and assign a class name — wrench, bolt.

SHOT: Screen capture — DATA tab. Select images. Draw a bounding box
around a wrench, label it "wrench". Draw a box around a bolt, label it
"bolt". Show 2-3 labels being drawn live. (The rest are pre-labeled.)

> I've labeled about 80 images. That's enough for a basic detector.

SHOT: Brief view of the labeled dataset — many images with colored
bounding boxes.

**Train [0:30–0:45]**

> I create a training job. I select this dataset, choose object detection
> as the model type, and start training. Viam handles the GPU provisioning
> and training pipeline.

SHOT: Screen — navigate to training. Create a training job. Select
dataset, select model type (object detection). Click train.

> (cut) Training's done. Here's the model with a version number in the
> Registry.

SHOT: Screen — model listed in the Registry or ML models section, with
version number visible.

**Deploy and test [0:45–1:15]**

> Now I deploy it to the machine. I add an ML model service that points
> to this model, and a vision service that uses it as a detector.

SHOT: Screen — CONFIGURE tab. Add ML model service. Search for
"tflite_cpu", add it, name it "wrench-detector-model". Set the
`model_path` to the deployed model package. Save.

Add a vision service. Select `mlmodel`, name it "my-detector". Set
`mlmodel_name` to "wrench-detector-model". Save.

> Let me test it. I hold up a wrench in front of the camera —

SHOT: Presenter holds up wrench in front of the RealSense camera.

> — and there it is. Bounding box, label, confidence score.

SHOT: Screen — CONTROL tab, vision service TEST panel. Live detection
overlay showing "wrench: 0.92" with bounding box.

CUT TO: Run `test_detection.py` in terminal:
```
wrench: 0.92 at (120, 80, 340, 290)
```

---

### PAYOFF — face to camera [1:15–1:30]

> From raw images to on-device inference. No GPU provisioning, no export
> pipeline, no deploy scripts. Label, train, deploy, detect.

SHOT: Presenter, wrench in hand.

---

## Validation notes

### Config accuracy (machine-config.json)
- ML model service `"model": "tflite_cpu"` — confirmed from
  `vision/configure.md:155` (short form resolved by app)
- `model_path` using `${packages.wrench-detector}/model.tflite` — confirmed
  package variable pattern from `vision/configure.md:157`
- `label_path` — confirmed attribute from config-xref.md:346
- Vision service `"model": "rdk:vision:mlmodel"` — confirmed from
  config-xref.md:331-333
- `mlmodel_name` attribute — confirmed from config-xref.md:337
  (Required field, points to the ML model service name)

### Code accuracy (test_detection.py)
- `VisionClient.from_robot(robot, name)` — confirmed from SDK
  (`service_base.py:28`)
- `detector.get_detections_from_camera(camera_name)` — confirmed from
  SDK (`client.py:87`): takes `camera_name: str` positional
- Detection object attributes: `class_name`, `confidence`, `x_min`,
  `y_min`, `x_max`, `y_max` — confirmed from proto (`vision.proto`
  Detection message) and SDK pyi stubs

### Behavioral claims
- "runs on the robot, not in the cloud" — confirmed: ML model service
  loads model locally on the machine (`rdk/services/vision/mlvision/`)
- "Viam handles GPU provisioning" for training — this refers to the
  cloud training infrastructure, not on-device. Accurate for cloud-based
  training jobs.
- Package deployment: model files downloaded via the packages system
  to the machine — confirmed from config-xref.md (packages config)

### UI references
- **DATA tab** — confirmed route `/data`
- Bounding box labeling tool — exists in DATA tab
- Training job creation — exists in training routes
- ML model service and vision service add flow — standard CONFIGURE tab
  component/service add flow
- Vision service TEST panel — rendered on CONTROL tab
