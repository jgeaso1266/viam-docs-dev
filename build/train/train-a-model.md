# Train a Model

**Time:** ~25 minutes
**Prerequisites:** [Create a Dataset](create-a-dataset.md) (labeled dataset ready)
**Works with:** Simulation ✓ | Real Hardware ✓

## What You'll Learn

- The difference between TensorFlow Lite and TensorFlow models and when to use each
- The three task types: single label classification, multi label classification, and object detection
- How to start a training job from the web UI and CLI
- How to monitor training progress and read training logs
- How to test your trained model against images in the cloud
- How to deploy a model to a machine and configure the vision service

## What Problem This Solves

You have a labeled dataset with images tagged or annotated with bounding boxes.
Now you need to turn that data into a model that your machine can run. Training
is the process that takes your labeled examples and produces a model file -- a
compressed representation of the patterns in your data that can classify new
images or detect objects in real time.

Viam handles the compute for you. You do not need to provision GPUs, install
TensorFlow, or write training scripts. You select a dataset, pick a model type
and task, and start the job. When training completes, the model is available
to deploy to any machine in your organization. If the machine already has the
model configured, the new version deploys automatically.

This block covers the full cycle: starting a training job, monitoring it,
testing the result, deploying the model, and iterating to improve it.

## Concepts

### ML model types

Viam supports two model frameworks, each suited to different deployment
scenarios:

**TensorFlow Lite (TFLite)** produces compact models optimized for edge devices.
TFLite models run directly on single-board computers like the Raspberry Pi
without requiring a GPU. They use less memory and less CPU than full TensorFlow
models. Use TFLite when your model will run on the machine itself, which is the
most common case for robotics applications.

**TensorFlow (TF)** produces general-purpose models that require more compute
resources. TF models are larger and more expressive, which can improve accuracy
on complex tasks, but they need more powerful hardware to run at reasonable
speeds. Use TF when you are running on a machine with a capable CPU or GPU and
need the additional model capacity.

For most Viam use cases -- quality inspection, object detection on a camera
feed, simple classification -- TFLite is the right choice. Start with TFLite
and switch to TF only if you find that TFLite models cannot reach the accuracy
you need.

### Task types

The task type determines what the model learns to do. It must match how you
labeled your dataset.

**Single Label Classification** assigns exactly one label to each image. The
model outputs the most likely label or `UNKNOWN` if no label meets the
confidence threshold. Use this when each image belongs to exactly one category.
Example: classifying parts as "good" or "defective". Your dataset should use
tags with exactly one tag per image.

**Multi Label Classification** assigns one or more labels to each image. The
model outputs every label that meets the confidence threshold. Use this when
images can belong to multiple categories simultaneously. Example: an image of
a workspace might be tagged "person-present" and "safety-glasses-on". Your
dataset should use tags, and images may have multiple tags.

**Object Detection** finds objects in an image and draws bounding boxes around
them with labels. The model outputs a list of detected objects, each with a
label, a confidence score, and bounding box coordinates. Use this when you need
to know where objects are, not just whether they are present. Example: detecting
packages on a conveyor belt. Your dataset should use bounding box annotations.

### Training in the cloud

When you start a training job, Viam runs the training process on cloud
infrastructure. Your machine does not need to be online during training. The
job runs asynchronously -- you can close the browser and come back later.
Training times vary based on dataset size and model type, but typically range
from a few minutes to an hour.

Training logs are available for 7 days after the job completes. After that, the
logs expire, but the trained model remains available indefinitely.

### Automatic deployment

When training completes, the model is stored in your organization's registry.
If a machine is already configured to use that model, Viam automatically deploys
the new version. You do not need to manually download or transfer model files.
The machine pulls the latest version of the model the next time it checks for
updates, which happens at regular intervals.

## Components Needed

- A labeled dataset (from [Create a Dataset](create-a-dataset.md)) that meets
  the minimum requirements: at least 15 images, 80% labeled, 10+ examples per
  label
- A machine running `viam-server` (for the deployment step)

## Steps

### 1. Start a training job from the web UI

1. Go to [app.viam.com](https://app.viam.com).
2. Click the **DATA** tab in the top navigation.
3. Click the **DATASETS** subtab.
4. Click the dataset you want to train on.
5. Click **Train model**.
6. Select the model framework:
   - **TFLite** for edge devices (recommended for most use cases)
   - **TF** for general-purpose models requiring more compute
7. Enter a name for your model. Use a descriptive name like
   `part-inspector-v1` or `package-detector-v1`. This name identifies the model
   in your organization's registry.
8. Select the task type:
   - **Single Label Classification** if each image has one tag
   - **Multi Label Classification** if images have multiple tags
   - **Object Detection** if you used bounding box annotations
9. Select which labels to include in training. You can exclude labels that have
   too few examples or that you do not want the model to learn.
10. Click **Train model**.

The training job starts. You will see a confirmation message with the job ID.

### 2. Start a training job from the CLI

If you prefer the command line, use the Viam CLI:

```bash
viam train submit managed \
  --dataset-id=YOUR-DATASET-ID \
  --model-name=part-inspector-v1 \
  --model-type=tflite_classifier \
  --org-id=YOUR-ORG-ID
```

Available model types:

| Flag value | Framework | Task |
|------------|-----------|------|
| `tflite_classifier` | TFLite | Single or Multi Label Classification |
| `tflite_detector` | TFLite | Object Detection |
| `tf_classifier` | TensorFlow | Single or Multi Label Classification |
| `tf_detector` | TensorFlow | Object Detection |

The command returns a training job ID that you can use to check status.

To list labels in your dataset before training:

```bash
viam dataset data list --dataset-id=YOUR-DATASET-ID
```

### 3. Monitor training progress

**Web UI:**

1. In the Viam app, click the **DATA** tab.
2. Click the **TRAINING** subtab.
3. You will see a list of training jobs with their status:
   - **Pending** -- the job is queued
   - **Running** -- training is in progress
   - **Completed** -- the model is ready
   - **Failed** -- something went wrong
4. Click a job ID to view detailed logs. Logs show training progress, including
   loss metrics and accuracy at each epoch.

**CLI:**

Check the status of a training job:

```bash
viam train get --job-id=YOUR-JOB-ID
```

View training logs:

```bash
viam train logs --job-id=YOUR-JOB-ID
```

Training logs expire after 7 days. If you need to retain logs for longer,
copy them before they expire.

**Python:**

```python
async def main():
    viam_client = await connect()
    ml_training_client = viam_client.ml_training_client

    # Get the status of a training job
    job = await ml_training_client.get_training_job(
        id="YOUR-TRAINING-JOB-ID",
    )
    print(f"Status: {job.status}")
    print(f"Model name: {job.model_name}")
    print(f"Created: {job.created_on}")

    viam_client.close()
```

**Go:**

```go
job, err := mlTrainingClient.GetTrainingJob(ctx, "YOUR-TRAINING-JOB-ID")
if err != nil {
	logger.Fatal(err)
}
fmt.Printf("Status: %s\n", job.Status)
fmt.Printf("Model name: %s\n", job.ModelName)
fmt.Printf("Created: %s\n", job.CreatedOn)
```

### 4. Test your model

After training completes, test the model against images before deploying it to
a machine.

1. In the Viam app, click the **DATA** tab.
2. Click an image to open the detail view. Choose images the model has not seen
   during training for a more realistic test.
3. Click **Actions** in the image toolbar.
4. Click **Run model**.
5. Select your trained model from the dropdown.
6. Set a **confidence threshold**. This is the minimum confidence score (0.0 to
   1.0) an output must have to be shown. Start with 0.5 and adjust:
   - Lower the threshold to see more predictions (including less certain ones)
   - Raise the threshold to see only high-confidence predictions
7. Click **Run model**.

For classification models, the result shows the predicted label and its
confidence score. A score of 0.95 means the model is 95% confident in that
label. A score of 0.55 means the model is barely confident -- the image may be
ambiguous or unlike anything in the training data.

For object detection models, the result shows bounding boxes drawn on the image,
each with a label and confidence score. Compare these boxes to the ground truth
annotations you drew during dataset creation.

Test with a variety of images:

- Images that clearly belong to each class (should get high confidence)
- Ambiguous images (helps you understand the model's decision boundary)
- Images from conditions not in the training set (reveals generalization gaps)

### 5. Deploy the model to a machine

Deploying a model requires two service configurations on your machine: an ML
model service that loads the model file, and a vision service that uses the ML
model to process camera frames.

**Configure the ML model service:**

In your machine's configuration, add an ML model service. This service loads
the trained model and makes it available to other services.

```json
{
  "name": "my-ml-model",
  "api": "rdk:service:mlmodel",
  "model": "tflite_cpu",
  "attributes": {
    "model_path": "${packages.my-model}/model.tflite",
    "label_path": "${packages.my-model}/labels.txt"
  }
}
```

- `name`: A name for this service instance. You will reference it from the
  vision service.
- `model`: Use `tflite_cpu` for TFLite models. This runs inference on the CPU,
  which works on all hardware including Raspberry Pi.
- `model_path`: The path to the model file. The `${packages.my-model}` syntax
  references a model package from your organization's registry. Replace
  `my-model` with your model's package name.
- `label_path`: The path to the labels file, which maps numeric model outputs
  to human-readable label names.

**Configure the vision service:**

Add a vision service that uses the ML model to process images:

```json
{
  "name": "my-detector",
  "api": "rdk:service:vision",
  "model": "mlmodel",
  "attributes": {
    "mlmodel_name": "my-ml-model"
  }
}
```

- `name`: A name for this vision service. Your code will use this name to get
  classifications or detections.
- `model`: Use `mlmodel` to indicate this vision service is backed by an ML
  model.
- `mlmodel_name`: Must match the `name` of the ML model service you configured
  above.

**Verify in the web UI:**

1. Save your configuration.
2. Navigate to the **CONTROL** tab.
3. Find your vision service and click **Test**.
4. Select a camera to run the model against.
5. You should see live classifications or detections overlaid on the camera
   feed.

**Use the model in code:**

Once the services are configured, you can call the vision service from your
application code.

**Python:**

```python
from viam.services.vision import VisionClient

# Get the vision service (assumes you have a robot connection)
vision = VisionClient.from_robot(robot, "my-detector")

# For classification
classifications = await vision.get_classifications(
    image=my_image,
    count=5,
)
for c in classifications:
    print(f"  {c.class_name}: {c.confidence:.2f}")

# For object detection
detections = await vision.get_detections(image=my_image)
for d in detections:
    print(f"  {d.class_name}: {d.confidence:.2f} "
          f"at ({d.x_min}, {d.y_min}) to ({d.x_max}, {d.y_max})")
```

**Go:**

```go
import "go.viam.com/rdk/services/vision"

// Get the vision service (assumes you have a robot connection)
visionSvc, err := vision.FromRobot(robot, "my-detector")
if err != nil {
	logger.Fatal(err)
}

// For classification
classifications, err := visionSvc.Classifications(ctx, myImage, 5, nil)
if err != nil {
	logger.Fatal(err)
}
for _, c := range classifications {
	fmt.Printf("  %s: %.2f\n", c.Label(), c.Score())
}

// For object detection
detections, err := visionSvc.Detections(ctx, myImage, nil)
if err != nil {
	logger.Fatal(err)
}
for _, d := range detections {
	box := d.BoundingBox()
	fmt.Printf("  %s: %.2f at (%d, %d) to (%d, %d)\n",
		d.Label(), d.Score(),
		box.Min.X, box.Min.Y, box.Max.X, box.Max.Y)
}
```

### 6. Iterate on the model

Your first model is a baseline. Improving it is an ongoing process.

**Add more data.** The single most effective way to improve a model is to give
it more diverse training examples. Focus on:

- **Edge cases:** Images where the model got it wrong or gave low confidence.
  These are the most valuable additions to your dataset.
- **Counterexamples:** If the model falsely detects objects in empty scenes, add
  images of empty scenes labeled appropriately.
- **Varied conditions:** Capture images under different lighting, angles,
  distances, and backgrounds. A model trained on images from one camera position
  may fail when the camera moves.

**Ensure label balance.** If one label has significantly more examples than
others, the model will be biased toward predicting that label. Add more
examples of underrepresented classes or reduce overrepresented ones.

**Match training to production.** Your training images should look like what the
camera sees in actual operation. If the production environment has different
lighting, clutter, or camera angles than your training images, the model will
underperform.

**Retrain.** After updating your dataset, start a new training job. Each
training job produces a new model version. If your machine is configured to use
the model, the new version deploys automatically -- you do not need to update
the machine configuration.

**Python:**

```python
async def main():
    viam_client = await connect()
    ml_training_client = viam_client.ml_training_client

    # List all training jobs to see versions
    jobs = await ml_training_client.list_training_jobs(
        organization_id=ORG_ID,
    )
    for job in jobs:
        print(f"Job: {job.id}, Status: {job.status}, "
              f"Model: {job.model_name}, Created: {job.created_on}")

    viam_client.close()
```

**Go:**

```go
jobs, err := mlTrainingClient.ListTrainingJobs(ctx, orgID)
if err != nil {
	logger.Fatal(err)
}
for _, job := range jobs {
	fmt.Printf("Job: %s, Status: %s, Model: %s, Created: %s\n",
		job.ID, job.Status, job.ModelName, job.CreatedOn)
}
```

## Try It

1. Start a training job from the web UI using your labeled dataset.
2. Wait for the training job to complete. Monitor it in the **TRAINING** tab.
3. When training finishes, go to the **DATA** tab and test the model on
   several images:
   - Test with clear, obvious examples. Expect high confidence scores (above
     0.8).
   - Test with ambiguous or edge-case images. Note where confidence drops.
   - Test with images from a different environment than your training set.
     Note any accuracy degradation.
4. Configure the ML model service and vision service on your machine.
5. Open the **CONTROL** tab and test the vision service with a live camera
   feed.
6. If results are not satisfactory, add more images to your dataset (especially
   the cases where the model struggled) and retrain.

## Troubleshooting

### Training job fails

- **Check the training logs.** In the **TRAINING** tab, click the failed job ID
  to view logs. The error message usually indicates the problem.
- **Dataset too small.** Training requires at least 15 images with at least 80%
  labeled. Check your dataset in the **DATASETS** tab and verify it meets the
  requirements.
- **No labels selected.** When starting a training job, you must select at least
  two labels. A model cannot learn to classify if there is only one category.
- **Bounding box format issue.** For object detection, verify that your bounding
  boxes are correctly formed -- coordinates should be normalized between 0.0 and
  1.0, and `x_min` must be less than `x_max`.

### Low confidence scores

- **Add more training data.** Low confidence usually means the model has not seen
  enough examples to be certain. More diverse images of each class will help.
- **Check label balance.** If one label dominates the dataset, the model may
  assign low confidence to minority labels. Balance the dataset and retrain.
- **Verify image quality.** Blurry, dark, or low-resolution images make it
  harder for the model to learn distinctive features. Ensure your training images
  are clear and well-lit.
- **Lower the confidence threshold.** If the model is correct but with scores
  around 0.4-0.6, your threshold may be set too high. Lowering it to 0.3 will
  show more results, though with higher false-positive risk.

### Model not appearing on the machine

- **Check the ML model service configuration.** Verify that `model_path` uses
  the correct `${packages.<name>}` syntax and that the package name matches your
  model's name in the registry.
- **Check the model version.** If you renamed the model or it was retrained
  under a different name, the package reference may be stale. Update the
  configuration to point to the correct model name.
- **Restart viam-server.** In some cases, the machine may need to restart to
  pick up a new model version. Restart `viam-server` and check the logs for
  model loading messages.
- **Check machine connectivity.** The machine must be online and connected to
  the cloud to download model updates. Verify the machine shows as **Live** in
  the Viam app.

### Vision service returns no results

- **Verify the mlmodel_name.** The `mlmodel_name` in the vision service
  configuration must exactly match the `name` of the ML model service. A
  mismatch means the vision service cannot find the model.
- **Check the camera.** The vision service needs images to process. Verify that
  the camera is working in the **CONTROL** tab before testing the vision
  service.
- **Check the confidence threshold.** If no results appear, try lowering the
  confidence threshold. The model may be producing results below your current
  threshold.

### Training takes too long

- **Large datasets take longer.** Training time scales with the number of images.
  A dataset with thousands of images may take an hour or more. This is normal.
- **TF models take longer than TFLite.** If training time is a concern and you
  do not need the extra capacity, switch to TFLite.
- **Training is queued.** If the status stays at "Pending" for a long time, the
  training infrastructure may be busy. Jobs are processed in order.

## What's Next

- [Add Computer Vision](../vision-detection/add-computer-vision.md) -- build
  applications that use your trained model to process live camera feeds.
- [Detect Objects (2D)](../vision-detection/detect-objects-2d.md) -- use your
  object detection model to find and locate objects in camera images.
- [Classify Objects](../stationary-vision/classify-objects.md) -- use your
  classification model to categorize images from your machine's camera.
