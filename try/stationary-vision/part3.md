# Part 3: Build the Inspector (~20 min)

[← Back to Overview](./index.md) | [← Part 2: Data Capture](./part2.md)

---

**Goal:** Write inspection logic that detects dented cans and rejects them from your laptop.

**Skills:** Viam SDK, module-first development, CLI-based testing.

## What You'll Build

Your vision pipeline detects dented cans and records the results. Now you'll write code that **acts** on those detections—rejecting defective cans automatically.

This completes the **sense-think-act** cycle that defines robotic systems:

1. **Sense** — Camera captures images
2. **Think** — Vision service classifies cans as PASS/FAIL
3. **Act** — Rejector pushes defective cans off the belt

You'll use the **module-first development pattern**: write code on your laptop, test it against remote hardware over the network. This workflow lets you iterate quickly—edit code, run it, see results—without redeploying after every change.

---

## Prerequisites

Before starting, verify you have the required tools installed.

**Check Go version:**

```bash
go version
```

You need Go 1.21 or later. If Go isn't installed or is outdated, download it from [go.dev/dl](https://go.dev/dl/).

**Install the Viam CLI:**

The Viam CLI is used for authentication and module deployment. Install it:

```bash
# macOS (Homebrew)
brew tap viamrobotics/brews
brew install viam

# Linux (binary)
sudo curl -o /usr/local/bin/viam https://storage.googleapis.com/packages.viam.com/apps/viam-cli/viam-cli-stable-linux-amd64
sudo chmod +x /usr/local/bin/viam
```

Verify it's installed:

```bash
viam version
```

> **Note:** The Viam CLI (`viam`) is different from `viam-server`. The CLI runs on your development machine; `viam-server` runs on your robot/machine.

---

## 3.1 Set Up Your Project

Create a Go project with a CLI for testing.

```bash
mkdir inspection-module && cd inspection-module
go mod init inspection-module
go get go.viam.com/rdk
go get github.com/erh/vmodutils
mkdir -p cmd/cli
```

You'll end up with this structure:

```
inspection-module/
├── cmd/
│   └── cli/main.go        # CLI for testing against remote machine
├── inspector.go           # Your service logic
└── go.mod
```

The `vmodutils` package provides helpers for connecting to remote machines using your Viam CLI credentials. This lets your local code talk to hardware running elsewhere.

---

## 3.2 Connect to Your Machine

Before writing inspection logic, verify you can connect to your machine from Go code.

**Get your machine address:**

1. In the Viam app, go to your machine's page
2. Click **Code sample** in the top right
3. Copy the machine address (looks like `your-machine-main.abc123.viam.cloud`)

[SCREENSHOT: Code sample tab showing machine address]

**Authenticate the CLI:**

The CLI uses your Viam CLI token for authentication. Make sure you're logged in:

```bash
viam login
```

This stores a token that `vmodutils` uses automatically.

**Create the CLI:**

Create `cmd/cli/main.go`:

```go
package main

import (
	"context"
	"flag"
	"fmt"

	"github.com/erh/vmodutils"
	"go.viam.com/rdk/logging"
)

// main wraps realMain so we can use error returns instead of log.Fatal.
// This pattern makes deferred cleanup (like machine.Close) work properly on errors.
func main() {
	if err := realMain(); err != nil {
		panic(err)
	}
}

func realMain() error {
	// Context carries cancellation signals and deadlines through the call chain
	ctx := context.Background()
	// Logger provides structured logging with levels (Info, Error, Debug)
	logger := logging.NewLogger("cli")

	// Parse command-line flags
	host := flag.String("host", "", "Machine address")
	flag.Parse()

	if *host == "" {
		return fmt.Errorf("need -host flag")
	}

	// Connect to the remote machine using credentials from `viam login`
	machine, err := vmodutils.ConnectToHostFromCLIToken(ctx, *host, logger)
	if err != nil {
		return fmt.Errorf("failed to connect: %w", err)
	}
	defer machine.Close(ctx) // Always close the connection when done

	// List available resources to verify connection works
	logger.Info("Connected! Available resources:")
	for _, name := range machine.ResourceNames() {
		logger.Infof("  %s", name)
	}

	return nil
}
```

**Test the connection:**

```bash
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud
```

You should see output listing your machine's resources:

```
Connected! Available resources:
  rdk:component:camera/inspection-cam
  rdk:service:vision/can-detector
  ...
```

> **What just happened:** Your laptop connected to the machine running in Docker (or on physical hardware) over the network. The `vmodutils.ConnectToHostFromCLIToken` function reads your Viam CLI credentials and establishes a secure connection. You now have a `machine` object that can access any component or service on that machine.

**Checkpoint:** If you see your resources listed, you're ready to write inspection logic.

<details>
<summary><strong>Troubleshooting: Connection failures</strong></summary>

**"failed to connect" or timeout errors:**
- Verify your machine is online in the Viam app (green dot next to machine name)
- Check that you've run `viam login` and authenticated successfully
- Confirm the host address is correct (copy it fresh from the Code sample tab)

**"unauthorized" or "invalid credentials" errors:**
- Run `viam logout` then `viam login` to refresh your credentials
- Ensure you're logged into the correct Viam organization

**No resources listed:**
- The machine is connected but may not have components configured yet
- Go back to Part 1 and verify the camera and vision service are configured

</details>

---

## 3.3 Build the Inspector

Now write code that calls the vision service to detect cans.

We'll call this `Inspector` from the start—even though it only does detection for now. By the end of Part 3, it will also reject defective cans. Naming it `Inspector` now avoids renaming later and reflects what we're building toward.

**Create the config:**

Create `inspector.go` and start with a configuration struct:

```go
package inspector

import (
	"context"
	"fmt"

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/vision"
)

// Config declares which dependencies the inspector needs.
// Each field names a resource that must exist on the machine.
// When deployed as a module, these come from the JSON config.
// When testing via CLI, we set them directly in code.
type Config struct {
	Camera        string `json:"camera"`         // Name of the camera component
	VisionService string `json:"vision_service"` // Name of the vision service
}

// Validate checks that required fields are present and returns dependency names.
// Viam calls this during configuration to:
// 1. Catch config errors early (before trying to start the service)
// 2. Know which resources to inject into the constructor
func (cfg *Config) Validate(path string) ([]string, error) {
	if cfg.Camera == "" {
		return nil, fmt.Errorf("camera is required")
	}
	if cfg.VisionService == "" {
		return nil, fmt.Errorf("vision_service is required")
	}
	// Return dependency names so Viam's dependency injection provides them
	return []string{cfg.Camera, cfg.VisionService}, nil
}
```

**Add the Inspector struct and constructor:**

```go
// Inspector handles detection and (eventually) rejection of defective cans.
// For now it only does detection; we'll add rejection in section 3.5.
type Inspector struct {
	conf     *Config
	logger   logging.Logger
	detector vision.Service
}

// NewInspector creates an inspector from a dependencies map.
// This same constructor works whether called from CLI or module.
func NewInspector(deps resource.Dependencies, conf *Config, logger logging.Logger) (*Inspector, error) {
	// Extract the vision service from dependencies by name.
	// FromDependencies looks up the resource and returns it as the correct type.
	// If the resource doesn't exist or isn't a vision service, it returns an error.
	detector, err := vision.FromDependencies(deps, conf.VisionService)
	if err != nil {
		return nil, fmt.Errorf("failed to get vision service %q: %w", conf.VisionService, err)
	}

	return &Inspector{
		conf:     conf,
		logger:   logger,
		detector: detector,
	}, nil
}
```

**Add the Detect method:**

```go
// Detect runs the vision service and returns the best detection.
// Returns: label (e.g., "PASS" or "FAIL"), confidence (0.0-1.0), error
func (i *Inspector) Detect(ctx context.Context) (string, float64, error) {
	// Call vision service, passing camera name so it knows which camera to use.
	// One vision service can work with multiple cameras.
	// The third argument (nil) is for extra parameters we don't need.
	detections, err := i.detector.DetectionsFromCamera(ctx, i.conf.Camera, nil)
	if err != nil {
		return "", 0, err
	}

	// Handle case where nothing was detected
	if len(detections) == 0 {
		return "NO_DETECTION", 0, nil
	}

	// Find the detection with highest confidence score.
	// When multiple objects are detected, we care about the most confident one.
	best := detections[0]
	for _, det := range detections[1:] {
		if det.Score() > best.Score() {
			best = det
		}
	}

	return best.Label(), best.Score(), nil
}
```

**Update the CLI to test detection:**

Replace the contents of `cmd/cli/main.go`:

```go
package main

import (
	"context"
	"flag"
	"fmt"

	"github.com/erh/vmodutils"
	"go.viam.com/rdk/logging"

	inspector "inspection-module"
)

func main() {
	if err := realMain(); err != nil {
		panic(err)
	}
}

func realMain() error {
	ctx := context.Background()
	logger := logging.NewLogger("cli")

	host := flag.String("host", "", "Machine address")
	flag.Parse()

	if *host == "" {
		return fmt.Errorf("need -host flag")
	}

	// Configuration specifying which resources to use.
	// These names must match what you configured in the Viam app.
	conf := &inspector.Config{
		Camera:        "inspection-cam",
		VisionService: "can-detector",
	}

	if _, err := conf.Validate(""); err != nil {
		return err
	}

	machine, err := vmodutils.ConnectToHostFromCLIToken(ctx, *host, logger)
	if err != nil {
		return fmt.Errorf("failed to connect: %w", err)
	}
	defer machine.Close(ctx)

	// Convert machine resources to a Dependencies map.
	// This gives us the same format the module system uses,
	// so our constructor works identically in both contexts.
	deps, err := vmodutils.MachineToDependencies(machine)
	if err != nil {
		return fmt.Errorf("failed to get dependencies: %w", err)
	}

	// Create the inspector using the same constructor the module will use
	insp, err := inspector.NewInspector(deps, conf, logger)
	if err != nil {
		return err
	}

	// Run detection
	label, confidence, err := insp.Detect(ctx)
	if err != nil {
		return fmt.Errorf("detection failed: %w", err)
	}

	logger.Infof("Detection: %s (%.1f%% confidence)", label, confidence*100)
	return nil
}
```

**Fetch dependencies and test:**

```bash
go mod tidy
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud
```

You should see output like:

```
Detection: PASS (94.2% confidence)
```

or

```
Detection: FAIL (87.3% confidence)
```

Run it several times—you'll see different results as different cans pass under the camera.

> **What just happened:** Your laptop called the vision service running on the remote machine. The vision service grabbed an image from the camera, ran it through the ML model, and returned detection results. You're running ML inference on remote hardware from local code.

<details>
<summary><strong>Troubleshooting: Detection failures</strong></summary>

**"failed to get vision service" error:**
- Verify `can-detector` exists in your machine config (Part 1, section 1.6)
- Check the exact name matches—it's case-sensitive

**"NO_DETECTION" result:**
- This is normal if no can is in view—wait for one to appear
- Check the camera is working in the Viam app's Test panel

**Import errors or "package not found":**
- Run `go mod tidy` to fetch missing dependencies
- Ensure you're in the `inspection-module` directory

</details>

---

### Milestone 1: Detection Working

You can now detect cans from your laptop. Run the CLI a few times and watch the results change as different cans pass under the camera.

**What you have:** A working detector that calls remote ML inference from local code.

**What's next:** Add the ability to reject defective cans.

---

## 3.4 Configure the Rejector

Before writing rejection code, add the rejector hardware to your machine.

**Add the motor component:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine in the left sidebar
3. Select **Component**, then **motor**
4. For **Model**, select `fake` (this creates a simulated motor for testing)
5. Name it `rejector`
6. Click **Create**
7. Click **Save** in the top right

> **Note:** In a real deployment, you'd use an actual motor model (like `gpio`) with pin configuration. The `fake` model lets us test the control logic without physical hardware.

**Test it in the Viam app:**

1. Find the `rejector` motor in your config
2. Click **Test** at the bottom of its card
3. Try the **Run** controls to verify it responds

[SCREENSHOT: Motor test panel showing rejector controls]

---

## 3.5 Add Rejection Logic

Now extend the inspector to trigger the rejector when a defective can is detected.

**Update the imports in `inspector.go`:**

Add the motor import:

```go
import (
	"context"
	"fmt"

	"go.viam.com/rdk/components/motor" // Add this
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/vision"
)
```

**Add the Rejector field to Config:**

```go
type Config struct {
	Camera        string `json:"camera"`
	VisionService string `json:"vision_service"`
	Rejector      string `json:"rejector"` // Add this
}
```

**Update Validate to include the rejector:**

Add the rejector validation check and include `cfg.Rejector` in the returned dependencies:

```go
func (cfg *Config) Validate(path string) ([]string, error) {
	if cfg.Camera == "" {
		return nil, fmt.Errorf("camera is required")
	}
	if cfg.VisionService == "" {
		return nil, fmt.Errorf("vision_service is required")
	}
	if cfg.Rejector == "" {                                          // NEW
		return nil, fmt.Errorf("rejector is required")               // NEW
	}                                                                // NEW
	return []string{cfg.Camera, cfg.VisionService, cfg.Rejector}, nil  // CHANGED: added cfg.Rejector
}
```

**Add the rejector field to Inspector:**

```go
type Inspector struct {
	conf     *Config
	logger   logging.Logger
	detector vision.Service
	rejector motor.Motor // Add this
}
```

**Update NewInspector to get the rejector:**

Add the rejector lookup after getting the detector, and include it in the returned struct:

```go
func NewInspector(deps resource.Dependencies, conf *Config, logger logging.Logger) (*Inspector, error) {
	detector, err := vision.FromDependencies(deps, conf.VisionService)
	if err != nil {
		return nil, fmt.Errorf("failed to get vision service %q: %w", conf.VisionService, err)
	}

	rejector, err := motor.FromDependencies(deps, conf.Rejector)  // NEW
	if err != nil {                                                // NEW
		return nil, fmt.Errorf("failed to get rejector %q: %w", conf.Rejector, err)  // NEW
	}                                                              // NEW

	return &Inspector{
		conf:     conf,
		logger:   logger,
		detector: detector,
		rejector: rejector,  // NEW
	}, nil
}
```

**Add the reject and Inspect methods:**

```go
// reject activates the rejector motor to push a defective can off the belt.
func (i *Inspector) reject(ctx context.Context) error {
	// GoFor runs the motor at a given speed for a given number of revolutions.
	// Arguments: rpm (speed), revolutions (distance), extra (nil = no extra params)
	// Tune these values based on your actuator - a pneumatic pusher might use
	// different parameters than a servo arm.
	if err := i.rejector.GoFor(ctx, 100, 1, nil); err != nil {
		return err
	}
	i.logger.Info("Defective can rejected")
	return nil
}

// Inspect runs detection and rejects defective cans.
// Returns: label, confidence, whether the can was rejected, error
func (i *Inspector) Inspect(ctx context.Context) (string, float64, bool, error) {
	label, confidence, err := i.Detect(ctx)
	if err != nil {
		return "", 0, false, err
	}

	// Decide whether to reject based on label and confidence.
	// The 0.7 threshold avoids rejecting on uncertain detections.
	// Lower values: catch more defects, risk more false positives
	// Higher values: fewer false positives, might miss some defects
	// Tune based on cost of each error type in your application.
	shouldReject := label == "FAIL" && confidence > 0.7

	if shouldReject {
		if err := i.reject(ctx); err != nil {
			// Log but don't fail - we still want to return the detection result
			i.logger.Errorw("Failed to reject", "error", err)
		}
	}

	return label, confidence, shouldReject, nil
}
```

**Update the CLI to support both commands:**

Add the `-cmd` flag and update the config and command handling. In `cmd/cli/main.go`:

Add the flag after the `host` flag:

```go
host := flag.String("host", "", "Machine address")
cmd := flag.String("cmd", "detect", "Command: detect or inspect") // Add this
flag.Parse()
```

Add `Rejector` to the config:

```go
conf := &inspector.Config{
	Camera:        "inspection-cam",
	VisionService: "can-detector",
	Rejector:      "rejector", // Add this
}
```

Replace the detection code at the end of `realMain()` (the four lines from `label, confidence, err := insp.Detect(ctx)` through `logger.Infof(...)`) with this switch:

```go
// Handle the requested command
switch *cmd {
case "detect":
	label, confidence, err := insp.Detect(ctx)
	if err != nil {
		return err
	}
	logger.Infof("Detection: %s (%.1f%%)", label, confidence*100)

case "inspect":
	label, confidence, rejected, err := insp.Inspect(ctx)
	if err != nil {
		return err
	}
	logger.Infof("Inspection: %s (%.1f%%), rejected=%v", label, confidence*100, rejected)

default:
	return fmt.Errorf("unknown command: %s (use 'detect' or 'inspect')", *cmd)
}

return nil
```

**Test both commands:**

```bash
# Detection only
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd detect

# Full inspection with rejection
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd inspect
```

With a good can:
```
Inspection: PASS (94.2%), rejected=false
```

With a dented can:
```
Inspection: FAIL (87.3%), rejected=true
Defective can rejected
```

> **What just happened:** You closed the control loop. Your code detects a defect, decides to reject based on confidence threshold, and actuates the motor. This is the sense-think-act cycle running from your laptop against remote hardware.

<details>
<summary><strong>Troubleshooting: Rejection failures</strong></summary>

**"failed to get rejector" error:**
- Verify the `rejector` motor exists in your machine config (section 3.4)
- Check the name matches exactly—it's case-sensitive

**Motor doesn't respond:**
- Test the motor in the Viam app's Test panel first
- For real hardware: check wiring and motor driver configuration
- For `fake` motor: this is expected—it simulates motion without physical output

**"rejected=true" but no physical action:**
- If using the `fake` motor model, this is expected behavior
- The fake motor accepts commands but doesn't control real hardware

</details>

---

### Milestone 2: Full Inspection Loop Working

You now have a complete inspect-and-reject system running from your laptop. The CLI connects to your remote machine, runs ML inference, makes a decision, and triggers actuation—all over the network.

**What you have:** Working inspection logic that you can iterate on quickly (edit code, run CLI, see results).

**What's next:** Package this as a module so it runs on the machine itself, not your laptop.

---

## 3.6 Summary

You built inspection logic using the module-first development pattern:

1. **Connected** to the remote machine from local code
2. **Built detection** — called vision service, processed results
3. **Added rejection** — triggered motor based on detection confidence

**The key insight:** You can develop and test against real (or simulated) hardware without deploying anything. Edit code locally, run the CLI, see results immediately. This is much faster than the traditional deploy-test-debug cycle.

**Your code is ready.** In Part 4, you'll package it as a module and deploy it to the machine so it runs autonomously.

---

**[Continue to Part 4: Deploy as a Module →](./part4.md)**
