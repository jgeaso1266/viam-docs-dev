# Capability #4a: Train and Deploy Models (Glass Detection)
## 90-Second Video Script

**Learning Outcome:** "ML deployment uses the same workflow as code deployment — and if I bring my own model, there's no conversion step."

**Demo Setup:** Vino wine-pouring robot. Uses images captured in Capability 3a (two-camera glass detection dataset). Training a glass detection model (object detection with bounding boxes). Viam app open in browser.

---

## Script

### [00:00-00:18] Hook (18 seconds)

*Visual:*
- Presenter on camera, Vino robot visible in background

*Presenter:*
"Training a model is one project. Getting it running on your robot is a completely different one. You need to provision GPUs, set up a training pipeline, then figure out how to package the model, get it onto the device, wire it to the camera, and do it all again every time you retrain.

Viam collapses this into configuration."

*Presenter guidance:*
- "Training a model is one project" — most teams can get a model trained using cloud GPUs, Roboflow, Ultralytics, etc. That part is increasingly commoditized.
- "Getting it running on your robot is a completely different one" — this is the infrastructure gap. Training tools don't handle deployment. Deployment tools don't handle training. Teams stitch together 3-5 separate tools (annotation tool, training environment, model registry, deployment pipeline, inference runtime) with custom glue code.
- "Provision GPUs" — training object detection or classification models requires GPU compute. This means setting up cloud GPU instances (AWS, GCP), managing CUDA/PyTorch/TensorFlow version compatibility, and paying $2-13/hour per GPU. Viam runs training on Vertex AI behind the scenes — the user never sees any of this.
- "Wire it to the camera" — even after the model is on the device, you need code to: grab frames from the camera, resize/normalize them to match the model's expected input, run inference, parse the output tensors into usable detections or classifications. In Viam, the vision service does all of this automatically through the mlvision bridge — you just point it at an ML model service by name.
- "Do it all again every time you retrain" — model improvement is iterative. Each retrain cycle means re-running the full pipeline. If any step is manual, it's a tax you pay repeatedly.

---

### [00:18-00:28] Establish Setup (10 seconds)

*Visual:*
- Presenter gestures to Vino robot

*Presenter:*
"In the last video, we captured images of glasses from two cameras on this robot. Now we need a model that detects where the glass is in the frame."

*Presenter guidance:*
- "Detects where the glass is in the frame" — this is object detection, not classification. The model outputs bounding boxes (rectangles around detected objects) with labels and confidence scores. This is what Vino needs to locate the glass before pouring.
- The connection to capability 3a should feel natural — same robot, same data, next step in the workflow.

---

### [00:28-00:45] Demo: Training (17 seconds)

*Visual:*
- Viam app: captured images from cap 3 in the DATA tab
- Create dataset, add images
- Draw bounding boxes around glasses, label "glass"
- Click "Train model"
- Training job running indicator

*Presenter (voiceover):*
"These are the images we captured. I create a dataset, draw bounding boxes around the glasses, and submit a training job. Viam handles the GPU, the framework, the training pipeline. I just label and click train."

*Presenter guidance:*
- "Create a dataset" — datasets in Viam are named collections of images drawn from your captured cloud data. You can pull images from any machine in your organization. The dataset is snapshotted when you train, so adding new images later doesn't affect an in-progress training job.
- "Draw bounding boxes" — in the Viam web UI, Cmd/Ctrl+click-drag draws a rectangle around an object. You assign a label to each box. The coordinates are stored as normalized values (0.0 to 1.0), so they work regardless of image resolution. Minimum requirement: 10+ examples per label, at least 80% of images labeled, at least 15 images total.
- "Viam handles the GPU, the framework, the training pipeline" — behind the scenes, Viam provisions an n1-standard-16 machine with 2 NVIDIA T4 GPUs on Google Vertex AI. It exports your dataset as JSONLines, runs a Keras/TensorFlow training script using MobileNet-based transfer learning, and produces a TFLite model optimized for edge devices. The user sees none of this — they see a progress indicator and get an email when training completes.
- "I just label and click train" — this is the key message. The ML infrastructure is invisible. The user's job is domain expertise (knowing what a glass looks like). Viam handles everything else.

---

### [00:45-01:05] Demo: Deploy + Inference (20 seconds)

*Visual:*
- Training complete notification
- Model `pour-glass-locate-on-top-model` visible in Registry
- CONFIGURE tab: add ML model service `glass-finder-first-model` using `tflite_cpu` module, pointing at the model package
- Add vision service `glass-finder-first-service` referencing the ML model service
- Save config
- `left-cam` feed with bounding boxes appearing around the glass in real-time

*Presenter (voiceover):*
"Training's done. The model is in the registry — `pour-glass-locate-on-top-model`. I add two services to the robot's config: an ML model service called `glass-finder-first-model` that loads it with the TFLite runtime, and a vision service called `glass-finder-first-service` that connects it to the left camera. Save. The robot pulls the model and starts detecting. Bounding boxes around the glass, running on the device, no cloud round-trips."

*Presenter guidance:*
- "The model is in the registry — `pour-glass-locate-on-top-model`" — when training completes, Viam automatically packages the model files as a versioned .tar.gz and publishes it to your organization's section of the Viam Registry. This is the same Registry that hosts code modules. The model gets a name and version string, and it's immediately available for deployment. In the Vino1 config, this model is declared as a package with `"type": "ml_model"` and `"version": "latest"`.
- "An ML model service called `glass-finder-first-model`" — this is a service you add in the CONFIGURE tab. It uses the `viam:mlmodel-tflite:tflite_cpu` module as its inference runtime. The config points to the model package with path syntax like `${packages.ml_model.pour-glass-locate-on-top-model}/pour-glass-locate-on-top-model.tflite` — the `${packages...}` syntax automatically resolves to wherever the package manager downloaded and extracted the model on disk. There's also a labels file at the same path (`labels.txt`) that maps output tensor indices to class names like "glass."
- "A vision service called `glass-finder-first-service`" — the vision service is the bridge between the ML model and the camera. Its config has one key field: `mlmodel_name: "glass-finder-first-model"`, which points to the ML model service. It also specifies `camera_name: "left-cam"` and a `default_minimum_confidence: 0.5` to filter low-confidence detections. The vision service automatically detects whether your model is a detector or classifier by testing it with a small dummy image at startup. It handles all the image preprocessing — resizing, normalizing, tensor layout conversion — so your application code just calls `GetDetections()`.
- "Save. The robot pulls the model" — saving the config triggers a config sync to the robot. The package manager sees the `pour-glass-locate-on-top-model` package in the config, downloads the .tar.gz from the Registry, extracts it, and creates a symlink. Then the `glass-finder-first-model` ML model service starts, loads the .tflite file, and the `glass-finder-first-service` vision service connects to it. This all happens automatically within seconds of saving.
- "Running on the device, no cloud round-trips" — inference happens entirely on the robot's CPU using the `tflite_cpu` module. Each frame from `left-cam` is processed locally. This matters for latency (real-time detections) and for robots that may lose connectivity. The model works whether the robot is online or offline.

---

### [01:05-01:15] Bring Your Own Model (10 seconds)

*Visual:*
- Stay on camera feed with detection boxes running
- Optional: brief flash of Registry showing model formats

*Presenter (voiceover):*
"And if you trained your own model in PyTorch or ONNX, you bring it as-is. Upload to the registry, pick the matching runtime module. No conversion step."

*Presenter guidance:*
- "Trained your own model in PyTorch or ONNX" — this speaks directly to ML-experienced viewers. Many teams already have models trained in their preferred framework. The built-in training path produces TFLite, but that's not the only option.
- "Bring it as-is" — this is the key point. Viam doesn't require you to convert your model to a specific format. The module system provides inference runtimes for TFLite, ONNX, TensorFlow, and PyTorch. You upload your model in whatever format it's already in.
- "Pick the matching runtime module" — instead of converting PyTorch → ONNX → TFLite (the conversion gauntlet), you just select the module that runs your format natively. torch-cpu for PyTorch, onnx-cpu for ONNX, tensorflow-cpu for TensorFlow. On Jetson hardware with a GPU, triton runs all three with GPU acceleration.
- "No conversion step" — this is architecturally different from most edge ML platforms. Typically the model has to adapt to the device. In Viam, the runtime adapts to the model. This works because the vision service talks to a framework-agnostic tensor interface (the MLModel service API is just Infer(tensors) → tensors). Your application code is identical regardless of what framework is behind it.
- This line serves double duty: it tells ML experts "you're not locked in," and it tells everyone else "there's a deeper capability here when you need it."

---

### [01:15-01:30] Payoff (15 seconds)

*Visual:*
- Back to presenter on camera
- Robot with detections still running in background

*Presenter:*
"Built-in training when you need it. Bring your own model when you don't. Same deployment, same APIs, no conversion. ML deployment is configuration in Viam."

*Presenter guidance:*
- "Built-in training when you need it" — the simple path. Annotate, click train, deploy. For teams without ML expertise, or for common tasks (object detection, classification) where a MobileNet-based model is sufficient.
- "Bring your own model when you don't" — "when you don't" means "when you don't need built-in training" — i.e., you already have a model or need a custom architecture. This isn't lesser — it's the power-user path. Same deployment mechanism either way.
- "Same deployment, same APIs" — whether you used built-in training or brought your own PyTorch model, deployment is the same: model goes to Registry, add to config, robot pulls it. And the vision service API your application calls (GetDetections, GetClassifications) is identical regardless of framework. This is the hardware abstraction story from capability 1, applied to ML.
- "No conversion" — reinforces the bring-your-own-model point from the previous section. Pick the runtime, don't convert the model.
- "ML deployment is configuration in Viam" — mirrors the payoff pattern from previous videos ("Data capture is configuration in Viam"). Configuration, not code. Not infrastructure. Not a pipeline you build and maintain.

---

## Production Notes

**Total time:** 90 seconds

**Pacing:**
- Hook lands the infrastructure gap — not "ML is hard" but the specific things you have to build between training and running on a robot.
- Setup connects directly to capability 3a — same robot, same data, next step.
- Training demo should feel fast — the labeling and clicking is the point, not the waiting.
- Deploy + inference demo should breathe — let the viewer see bounding boxes appearing in real-time on the camera feed. This is the proof.
- Bring-your-own-model is a quick, confident aside — it opens a door for ML-experienced viewers without derailing the main narrative.
- Payoff is short and direct. No taglines.

**The narrative arc:**
ML infrastructure is the real project, not the model (hook) → We captured glass images, now we need a detector (setup) → Annotate in the UI, train with a click (training) → Model deploys via config, detections running on device (deploy + inference) → Bring your own model if you prefer, no conversion (BYOM) → Same deployment as code, all configuration (payoff)

**Key messages:**
1. The gap between "I have a trained model" and "it's running on my robot" is where teams lose months
2. Viam's built-in training handles the full path from labeled images to on-device inference — no GPU provisioning, no pipeline setup
3. Bring your own model in any framework — the runtime adapts to the model, not the other way around
4. ML deployment uses the same versioning and config mechanism as code modules

**Tone:**
- The hook should feel like a catalog of work you've watched teams do — authoritative, not dramatic.
- The training demo should feel effortless — label, click, done.
- The deploy demo should feel like the capability 1 pattern — configuration, not engineering.
- The BYOM mention should feel like a confident aside, not a sales pitch.

**Connection to Capability 3a:**
This video picks up exactly where capability 3a left off. The glass images captured from two arm-mounted cameras become the training dataset.

**Connection to Capability 5:**
The deployed model enables the code development story — writing application logic that uses detections/classifications from the vision service.

---

## Research Backing for Hook Claims

### ML infrastructure tax (validated March 2025 - March 2026):
- GPU compute consumes 40-60% of technical budgets for AI startups in first two years (GMI Cloud, 2025)
- CUDA/PyTorch version mismatches cause hard-to-debug training failures across team members and CI/CD
- YOLO-to-TFLite conversion produces models that always predict class 0 (Ultralytics #21922, 2025)
- INT8 TFLite export fails entirely for YOLOv10/11/12 (Ultralytics #23131, 2025-2026)
- TensorRT engines must be rebuilt per device variant — non-portable across Jetson JetPack versions (NVIDIA Forums, 2025)
- Google Coral TPU: "Brilliant Hardware, Broken Toolchain" — toolchain abandoned, kernel driver broken on Linux >= 6.4 (GitHub edgetpu #896)
- AWS SageMaker Edge Manager shut down April 2024, replaced with "build it yourself" guidance
- YOLO26 (Jan 2026) redesigned architecture specifically to fix edge export problems — tacit admission of how broken the conversion path was
- No standard toolchain exists for edge ML deployment, versioning, or rollback (ACM Computing Surveys, 2025)

### How Viam solves it:
- Built-in training: annotate in web UI, submit training job, Viam provisions Vertex AI GPUs and runs Keras/TF pipeline
- Model auto-published to Registry as versioned package on training completion
- Deploy via config: add ML model service + vision service, save, robot pulls model automatically
- Framework-agnostic inference: tflite_cpu, onnx-cpu, tensorflow-cpu, torch-cpu, triton (Jetson GPU) — pick the runtime that matches your model
- Vision service bridge (mlvision): framework-agnostic tensor interface, auto-detects detector vs classifier, handles all image preprocessing
- Same deployment mechanism as code modules — versioned, fragment-deployable, rollback by version change
- On-device inference — no cloud round-trips, works offline

---

## B-Roll Needed

- Vino robot on bench (same setup as capability 3a)
- Presenter with robot in background
- Camera feed showing glass with bounding boxes appearing

## Screen Recordings Needed

- Viam app: DATA tab showing captured glass images from two cameras
- Viam app: creating a dataset, adding images
- Viam app: drawing bounding boxes around glasses, labeling "glass"
- Viam app: submitting training job, progress indicator
- Viam app: training complete, model in Registry
- Viam app: CONFIGURE tab — adding ML model service, adding vision service
- Viam app: saving config
- Camera feed with live bounding box detections on glasses
- Clean, readable config

## Graphics/Overlays

- Minimal aesthetic — let the annotation and detection demo speak for itself
- Bounding boxes should be clearly visible on camera feed
- Optional: brief label showing model framework when mentioning BYOM
