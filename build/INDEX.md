# Build

*Task-oriented blocks — modular tutorials you compose.*

---

## Overview

Blocks are self-contained tutorials (~15-30 minutes each) that teach a specific capability. They're designed to be composed—complete the ones relevant to your project, skip the ones that aren't.

Each block can be completed standalone. Prerequisites list what you should know or have configured, but each block provides the starting state you need so you can jump in directly.

All blocks work in both simulation and real hardware.

---

## Block Categories

### [Foundation](foundation/) ✓
*Start here. Every project needs these basics.*
- [Connect to Cloud](foundation/connect-to-cloud.md)
- [Add a Camera](foundation/add-a-camera.md)
- [Capture and Sync Data](foundation/capture-and-sync-data.md)

### [Data](data/)
*Work with captured data.*
- [Query Data](data/query-data.md)
- [Filter at the Edge](data/filter-at-the-edge.md)
- Visualize Data
- Configure Data Pipelines
- Sync Data to Your Database

### [Train](train/)
*Go from raw data to trained models.*
- Create a Dataset
- Train a Model

### [Development](development/)
*Write and ship code.*
- Write an Inline Module
- Write a Module
- Deploy a Module

### [Work Cell Layout](work-cell-layout/)
*Configure the 3D space your robot operates in.*
- Define Your Frame System
- Configure Robot Kinematics
- Calibrate Camera to Robot
- Define Obstacles

### [Vision & Detection](vision-detection/)
*Build understanding of the environment.*
- Add Computer Vision
- Detect Objects (2D)
- Classify Objects
- Track Objects Across Frames
- Measure Depth
- Localize Objects in 3D

### [Stationary Vision](stationary-vision/)
*Vision systems that don't move.*
- Trigger on Detection
- Count Objects
- Inspect for Defects
- Monitor Over Time

### [Mobile Base](mobile-base/)
*Robots that move.*
- Drive the Base
- Estimate Position
- Build a Map
- Navigate to Waypoint
- Avoid Obstacles
- Follow a Patrol Route
- Detect While Moving
- Navigate to Detected Object
- Mobile Pick-and-Place

### [Arm + Manipulation](arm-manipulation/)
*Robots that grab things.*
- Move the Arm
- Control Gripper
- Move to Pose
- Pick an Object
- Place an Object
- Pick from Bin
- Visual Servoing

### [Productize](productize/)
*Ship a product to your customers.*
- Build a Teleop Dashboard
- Build a Customer-Facing Web App
- Branded Customer Login
- Configure Billing

---

## How to Use Blocks

**If you know what you need:** Jump directly to the relevant block.

**If you're following a work cell guide:** The guide tells you which blocks to complete in order.

**If you're exploring:** Start with Foundation, then pick a track (Stationary Vision, Mobile Base, or Arm + Manipulation) based on your hardware.

---

## Prerequisites

Each block lists its prerequisites. Some blocks can be done in any order; others build on previous blocks. Every block provides a starting state (configuration fragment, starter code, or sample data) so you can begin without completing all prior blocks.

---

## After Building

Once you've built your application, continue to:
- [Deploy](../deploy/INDEX.md) — Get it running in the real world
- [Scale](../scale/INDEX.md) — Go from one robot to many
- [Maintain](../maintain/INDEX.md) — Keep it running over time
