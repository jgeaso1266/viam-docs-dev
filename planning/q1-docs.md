# Docs Punch List

Running punch list of documentation deliverables.
Updated: 2026-03-04

---

## How-To Pages (ported to viam-docs, IA-reorg branch)

### Complete

All 23 how-to pages ported from docs-dev and restructured as top-level sections:

- **Get Started:** Initialize a Viam Machine
- **Hardware:** Add a Camera
- **Data:** Capture and Sync Data, Stop Data Capture, Query Data, Filter at the Edge, Configure Data Pipelines, Sync Data to Your Database, Visualize Data
- **Train:** Create a Dataset, Train a Model
- **Development:** Write an Inline Module, Write a Module, Deploy a Module
- **Work Cell Layout:** Define Your Frame System, Configure Robot Kinematics, Calibrate Camera to Robot, Define Obstacles
- **Vision & Detection:** Add Computer Vision, Detect Objects (2D), Classify Objects, Track Objects Across Frames, Measure Depth, Localize Objects in 3D

### Still to write (future how-to sections)

**Stationary Vision:**
- [ ] Trigger on Detection
- [ ] Count Objects
- [ ] Inspect for Defects
- [ ] Monitor Over Time

**Mobile Base:**
- [ ] Drive the Base
- [ ] Estimate Position
- [ ] Build a Map
- [ ] Navigate to Waypoint
- [ ] Avoid Obstacles
- [ ] Follow a Patrol Route
- [ ] Detect While Moving
- [ ] Navigate to Detected Object
- [ ] Mobile Pick-and-Place

**Arm + Manipulation:**
- [ ] Move the Arm
- [ ] Control Gripper
- [ ] Move to Pose
- [ ] Pick an Object
- [ ] Place an Object
- [ ] Pick from Bin
- [ ] Visual Servoing

**Productize:**
- [ ] Build a Teleop Dashboard
- [ ] Build a Customer-Facing Web App
- [ ] Branded Customer Login
- [ ] Configure Billing

---

## Phase 5: Source Page Cleanup

Remove procedural content from existing reference/operate pages that duplicates
the new how-to pages. Replace with cross-links. One PR per source section.

### data-ai/capture-data/ → overlaps Data section
- [ ] capture-sync.md — deduplicate with data/capture-and-sync-data.md
- [ ] filter-before-sync.md — deduplicate with data/filter-at-the-edge.md
- [ ] conditional-sync.md — deduplicate with data/filter-at-the-edge.md
- [ ] upload-other-data.md — review, may stay as reference
- [ ] lorawan.md — review, specialized content may stay

### data-ai/data/ → overlaps Data section
- [ ] query.md — deduplicate with data/query-data.md
- [ ] visualize.md — deduplicate with data/visualize-data.md
- [ ] data-pipelines.md — deduplicate with data/configure-data-pipelines.md
- [ ] hot-data-store.md — deduplicate with data/sync-data-to-your-database.md
- [ ] export.md — review, may stay as reference
- [ ] alert-data.md — review, may stay or move to future Stationary Vision

### data-ai/train/ → overlaps Train section
- [ ] create-dataset.md — deduplicate with train/create-a-dataset.md
- [ ] annotate-images.md — deduplicate with train/create-a-dataset.md
- [ ] train-tf-tflite.md — deduplicate with train/train-a-model.md
- [ ] train.md — deduplicate with train/train-a-model.md

### data-ai/ai/ → overlaps Vision & Detection section
- [ ] deploy.md — deduplicate with vision-detection/add-computer-vision.md
- [ ] run-inference.md — deduplicate with vision-detection/add-computer-vision.md
- [ ] alert.md — review, may move to future Stationary Vision
- [ ] act.md — review, may move to future Stationary Vision

### operate/modules/ → overlaps Development section
- [ ] configure-modules.md — deduplicate with development/write-a-module.md
- [ ] deploy-module.md — deduplicate with development/deploy-a-module.md
- [ ] control-logic.md — deduplicate with development/write-an-inline-module.md
- [ ] lifecycle-module.md — review, may stay as reference

### operate/mobility/ → overlaps Work Cell Layout section
- [ ] motion-concepts.md — review, conceptual content may move to Understand
- [ ] define-dynamic-obstacles.md — deduplicate with work-cell-layout/define-obstacles.md (currently draft)
- [ ] move-base.md — review, may move to future Mobile Base section
- [ ] move-gantry.md — review, may stay as reference
- [ ] orientation-vector.md — review, may stay as reference
- [ ] use-input-to-act.md — review, may stay as reference

### reference/components/camera/ → overlaps Hardware section
- [ ] webcam.md — deduplicate procedural content with hardware/add-a-camera.md, keep config reference
- [ ] calibrate.md — deduplicate with work-cell-layout/calibrate-camera-to-robot.md
- [ ] transform.md — review, may stay as reference
- [ ] fake.md, ffmpeg.md, image-file.md, esp32-camera.md — keep as reference

### reference/services/vision/ → overlaps Vision & Detection section
- [ ] mlmodel.md — deduplicate with vision-detection/add-computer-vision.md, keep config reference
- [ ] color_detector.md — deduplicate with vision-detection/detect-objects-2d.md, keep config reference
- [ ] detector_3d_segmenter.md — deduplicate with vision-detection/localize-objects-in-3d.md, keep config reference

### reference/services/frame-system/ → overlaps Work Cell Layout section
- [ ] _index.md — deduplicate with work-cell-layout/define-your-frame-system.md, keep API reference

---

## Conceptual (Understand section)

- [x] What is Viam? (exists in viam-docs)
- [x] Problems Viam Solves (exists in viam-docs)
- [x] Reusable Configurations (exists in viam-docs)
- [ ] How Viam Works (planned in docs-dev, not yet written)

---

## Tutorials (Browser-Based Simulations)

Each tutorial needs:
- Simulation implementation (Gazebo world + Viam modules)
- Step-by-step tutorial content
- Supporting how-to pages

### Stationary Vision
- [ ] Simulation: camera + compute work cell
- [ ] Tutorial: object detection, defect inspection, alerts

### Mobile Base
- [ ] Simulation: wheeled robot + camera + lidar work cell
- [ ] Tutorial: autonomous navigation, object detection, patrol

### Arm + Vision
- [x] Simulation: xArm 6 + RGBD cameras work cell
- [ ] Tutorial: visual detection, pick-and-place, bin picking

---

## Reference/Explanation

- [ ] Fragments explanation (update reusable-configurations.md or write new reference)

---

## Notes

- How-to pages are top-level sections in viam-docs (not under Build/)
- Tutorials walk users through all lifecycle stages
- Each tutorial ~1-1.5 hours
- Zero installation (browser-based)
- Phase 5 cleanup should preserve reference-quality content while removing procedural duplication
