# Part 3: Control Logic (~30 min)

[← Back to Overview](./index.md) | [← Part 2: Data Capture](./part2.md)

---

**Goal:** Write inspection logic that detects dented cans and rejects them, then deploy it as a module.

**Skills:** Module-first development, Viam SDK, adding actuators, module deployment.

Your vision pipeline detects dented cans and records the results. Now you'll write code to act on those detections—rejecting defective cans automatically.

You'll use the **module-first development pattern**: code that runs on your laptop during development, connecting to remote hardware over the network. When it works, you package it as a module and deploy it to the machine. Same code, different context.

## 3.1 Set Up Your Project

Create a project with two files: your service logic and a CLI to test it.

{{< tabs >}}
{{% tab name="Go" %}}

```bash
mkdir inspection-module && cd inspection-module
go mod init inspection-module
go get go.viam.com/rdk
go get github.com/erh/vmodutils
mkdir -p cmd/cli cmd/module
```

Create this structure:

```
inspection-module/
├── cmd/
│   ├── cli/main.go        # Development CLI
│   └── module/main.go     # Production entry point (added later)
├── inspector.go           # Your service logic
└── go.mod
```

{{% /tab %}}
{{% tab name="Python" %}}

```bash
mkdir inspection-module && cd inspection-module
python3 -m venv venv && source venv/bin/activate
pip install viam-sdk Pillow
```

Create two files:

```
inspection-module/
├── inspector.py    # Your service logic
└── cli.py          # CLI for testing
```

{{% /tab %}}
{{< /tabs >}}

Your service logic lives in one file; the CLI imports it. During development, the CLI runs on your laptop and connects to the remote machine. You iterate locally without deploying anything.

## 3.2 Build the Inspector

Create the inspector service with detection and rejection logic.

{{< tabs >}}
{{% tab name="Go" %}}

Create `inspector.go`:

```go
package inspector

import (
	"context"
	"fmt"

	"github.com/mitchellh/mapstructure"
	"go.viam.com/rdk/components/motor"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/vision"
)

// Config declares which dependencies the inspector needs.
type Config struct {
	Camera        string `json:"camera"`
	VisionService string `json:"vision_service"`
	Rejector      string `json:"rejector"`
}

// Validate checks the config and returns dependency names.
func (cfg *Config) Validate(path string) ([]string, []string, error) {
	if cfg.Camera == "" {
		return nil, nil, fmt.Errorf("camera is required")
	}
	if cfg.VisionService == "" {
		return nil, nil, fmt.Errorf("vision_service is required")
	}
	if cfg.Rejector == "" {
		return nil, nil, fmt.Errorf("rejector is required")
	}
	return []string{cfg.Camera, cfg.VisionService, cfg.Rejector}, nil, nil
}

// Inspector implements resource.Resource.
type Inspector struct {
	// AlwaysRebuild tells Viam to recreate this service when config changes,
	// rather than trying to update it in place.
	resource.AlwaysRebuild

	name   resource.Name
	conf   *Config
	logger logging.Logger

	detector vision.Service
	rejector motor.Motor
}

// NewInspector is the exported constructor called by both CLI and module.
func NewInspector(
	ctx context.Context,
	deps resource.Dependencies,
	name resource.Name,
	conf *Config,
	logger logging.Logger,
) (resource.Resource, error) {
	detector, err := vision.FromDependencies(deps, conf.VisionService)
	if err != nil {
		return nil, err
	}
	rejector, err := motor.FromDependencies(deps, conf.Rejector)
	if err != nil {
		return nil, err
	}

	return &Inspector{
		name:     name,
		conf:     conf,
		logger:   logger,
		detector: detector,
		rejector: rejector,
	}, nil
}

func (i *Inspector) Name() resource.Name {
	return i.name
}

// Command struct for DoCommand parsing.
type inspectorCmd struct {
	Detect  bool
	Inspect bool
}

func (i *Inspector) DoCommand(ctx context.Context, cmdMap map[string]interface{}) (map[string]interface{}, error) {
	var cmd inspectorCmd
	if err := mapstructure.Decode(cmdMap, &cmd); err != nil {
		return nil, err
	}

	if cmd.Detect {
		label, confidence, err := i.detect(ctx)
		if err != nil {
			return nil, err
		}
		return map[string]interface{}{"label": label, "confidence": confidence}, nil
	}

	if cmd.Inspect {
		label, confidence, rejected, err := i.inspect(ctx)
		if err != nil {
			return nil, err
		}
		return map[string]interface{}{
			"label":      label,
			"confidence": confidence,
			"rejected":   rejected,
		}, nil
	}

	return nil, fmt.Errorf("unknown command: %v", cmdMap)
}

func (i *Inspector) Close(ctx context.Context) error {
	return nil
}

func (i *Inspector) detect(ctx context.Context) (string, float64, error) {
	// Pass camera name to tell the vision service which camera to use.
	// This allows one vision service to work with multiple cameras.
	detections, err := i.detector.DetectionsFromCamera(ctx, i.conf.Camera, nil)
	if err != nil {
		return "", 0, err
	}

	if len(detections) == 0 {
		return "NO_DETECTION", 0, nil
	}

	best := detections[0]
	for _, d := range detections[1:] {
		if d.Score() > best.Score() {
			best = d
		}
	}

	return best.Label(), best.Score(), nil
}

func (i *Inspector) inspect(ctx context.Context) (string, float64, bool, error) {
	label, confidence, err := i.detect(ctx)
	if err != nil {
		return "", 0, false, err
	}

	shouldReject := label == "FAIL" && confidence > 0.7

	if shouldReject {
		if err := i.reject(ctx); err != nil {
			i.logger.Errorw("Failed to reject part", "error", err)
		}
	}

	return label, confidence, shouldReject, nil
}

func (i *Inspector) reject(ctx context.Context) error {
	if err := i.rejector.GoFor(ctx, 100, 1, nil); err != nil {
		return err
	}
	i.logger.Info("Part rejected")
	return nil
}
```

{{% /tab %}}
{{% tab name="Python" %}}

Create `inspector.py`:

```python
from dataclasses import dataclass
from typing import Any, Mapping
from viam.components.motor import Motor
from viam.services.vision import VisionClient

@dataclass
class Config:
    camera: str
    vision_service: str
    rejector: str

    def validate(self) -> list[str]:
        """Check config and return dependency names."""
        if not self.camera:
            raise ValueError("camera is required")
        if not self.vision_service:
            raise ValueError("vision_service is required")
        if not self.rejector:
            raise ValueError("rejector is required")
        return [self.camera, self.vision_service, self.rejector]

class Inspector:
    """Inspector implements the generic service interface."""

    def __init__(self, name: str, conf: Config, detector: VisionClient, rejector: Motor):
        self.name = name
        self.conf = conf
        self.detector = detector
        self.rejector = rejector

    @classmethod
    async def new(cls, deps: dict, cfg: Config) -> "Inspector":
        """Create an inspector by extracting dependencies from the map."""
        detector = next((v for k, v in deps.items() if k.name == cfg.vision_service), None)
        rejector = next((v for k, v in deps.items() if k.name == cfg.rejector), None)
        return cls("inspector", cfg, detector, rejector)

    async def do_command(self, command: Mapping[str, Any]) -> Mapping[str, Any]:
        """Generic service interface. All commands go through here."""
        if command.get("detect"):
            label, confidence = await self._detect()
            return {"label": label, "confidence": confidence}

        if command.get("inspect"):
            label, confidence, rejected = await self._inspect()
            return {"label": label, "confidence": confidence, "rejected": rejected}

        raise ValueError(f"unknown command: {command}")

    async def close(self) -> None:
        pass

    async def _detect(self) -> tuple[str, float]:
        detections = await self.detector.get_detections_from_camera(self.conf.camera)

        if not detections:
            return "NO_DETECTION", 0.0

        best = max(detections, key=lambda d: d.confidence)
        return best.class_name, best.confidence

    async def _inspect(self) -> tuple[str, float, bool]:
        label, confidence = await self._detect()
        should_reject = label == "FAIL" and confidence > 0.7

        if should_reject:
            try:
                await self._reject()
            except Exception as e:
                print(f"Failed to reject part: {e}")

        return label, confidence, should_reject

    async def _reject(self) -> None:
        await self.rejector.go_for(rpm=100, revolutions=1)
        print("Part rejected")
```

{{% /tab %}}
{{< /tabs >}}

**Fetch dependencies:**

```bash
go mod tidy
```

## 3.3 Write the Development CLI

Now create the CLI that imports and tests your inspector. The CLI connects to your remote machine and converts its resources to a Dependencies map—the same format the module system uses in production.

{{< tabs >}}
{{% tab name="Go" %}}

Create `cmd/cli/main.go`:

```go
package main

import (
	"context"
	"flag"
	"fmt"

	"github.com/erh/vmodutils"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/services/generic"

	inspector "inspection-module"
)

func main() {
	err := realMain()
	if err != nil {
		panic(err)
	}
}

func realMain() error {
	ctx := context.Background()
	logger := logging.NewLogger("cli")

	host := flag.String("host", "", "Machine address")
	cmd := flag.String("cmd", "", "Command: detect, inspect")
	flag.Parse()

	if *host == "" {
		return fmt.Errorf("need -host flag")
	}
	if *cmd == "" {
		return fmt.Errorf("need -cmd flag")
	}

	// 1. Config with hardcoded dependency names
	cfg := inspector.Config{
		Camera:        "inspection-cam",
		VisionService: "can-detector",
		Rejector:      "rejector",
	}

	// 2. Validate the config
	_, _, err := cfg.Validate("")
	if err != nil {
		return err
	}

	// 3. Connect using vmodutils
	machine, err := vmodutils.ConnectToHostFromCLIToken(ctx, *host, logger)
	if err != nil {
		return err
	}
	defer machine.Close(ctx)

	// 4. Get dependencies using vmodutils
	deps, err := vmodutils.MachineToDependencies(machine)
	if err != nil {
		return err
	}

	// 5. Create service using exported constructor
	svc, err := inspector.NewInspector(ctx, deps, generic.Named("inspector"), &cfg, logger)
	if err != nil {
		return err
	}
	defer svc.Close(ctx)

	// 6. Call DoCommand with the command from -cmd flag
	result, err := svc.DoCommand(ctx, map[string]interface{}{*cmd: true})
	if err != nil {
		return err
	}
	logger.Infof("Result: %v", result)
	return nil
}
```

{{% /tab %}}
{{% tab name="Python" %}}

Create `cli.py`:

```python
import asyncio
import sys
from viam.robot.client import RobotClient

from inspector import Inspector, Config

async def main():
    if len(sys.argv) < 3:
        print("Usage: python cli.py HOST COMMAND")
        print("Commands: detect, inspect")
        return

    host = sys.argv[1]
    cmd = sys.argv[2]

    # 1. Config with hardcoded dependency names
    cfg = Config(
        camera="inspection-cam",
        vision_service="can-detector",
        rejector="rejector"
    )

    # 2. Validate the config
    cfg.validate()

    # 3. Connect to the remote machine
    robot = await RobotClient.at_address(host)

    # 4. Get dependencies
    deps = {}
    for name in robot.resource_names:
        try:
            deps[name] = robot.get_component(name)
        except:
            try:
                deps[name] = robot.get_service(name)
            except:
                pass

    # 5. Create service using exported constructor
    inspector = await Inspector.new(deps, cfg)

    # 6. Call do_command with the command from CLI args
    result = await inspector.do_command({cmd: True})
    print(f"Result: {result}")

    await inspector.close()
    await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

{{% /tab %}}
{{< /tabs >}}

The CLI uses `{*cmd: true}` to pass whatever command you specify via `-cmd` flag. This means the same CLI works for both `detect` and `inspect` commands.

**Authenticate the CLI:**

The Go CLI uses your Viam CLI token for authentication. Make sure you're logged in:

```bash
viam login
```

This stores a token that `vmodutils.ConnectToHostFromCLIToken` uses automatically.

**Get your machine address:**

1. In the Viam app, go to your machine's page
2. Click the **Code sample** tab
3. Copy the machine address (looks like `your-machine-main.abc123.viam.cloud`)

[SCREENSHOT: Code sample tab showing machine address]

## 3.4 Configure the Rejector

Your code depends on a rejector motor. Add that hardware to your work cell.

**Add the reject mechanism to your simulation:**

Click the button below to add a can rejector:

[BUTTON: Add Reject Mechanism]

The simulation now shows a pneumatic pusher mounted beside the conveyor. When activated, it pushes defective cans into a reject bin.

[SCREENSHOT: Work cell with reject mechanism visible]

**Configure it in Viam:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine in the left sidebar
3. Select **Component**, then **motor**
4. For **Model**, select `gpio` (or the appropriate model for your simulation)
5. Name it `rejector`
6. Click **Create**

**Configure the motor:**

Set the board and pin that controls the rejector:

```json
{
  "board": "local",
  "pins": {
    "pwm": "32"
  }
}
```

[SCREENSHOT: Rejector motor configuration]

**Test it in the Viam app:**

1. Find the `rejector` motor in your config
2. Click **Test** at the bottom of its configuration card
3. Click **Run** to activate it briefly
4. Watch the simulation—the pusher should extend and retract

[SCREENSHOT: Motor test panel with Run button]

## 3.5 Test the Inspector

Now test your inspector against the remote machine.

**Test detection:**

```bash
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd detect
# or: python cli.py your-machine-main.abc123.viam.cloud detect
```

```
Result: map[confidence:0.942 label:PASS]
```

You're running ML inference on the remote machine from your laptop.

**Test the full inspection loop:**

```bash
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd inspect
# or: python cli.py your-machine-main.abc123.viam.cloud inspect
```

With a good can:
```
Result: map[confidence:0.942 label:PASS rejected:false]
```

With a dented can:
```
Result: map[confidence:0.873 label:FAIL rejected:true]
```

Watch the simulation—when a FAIL is detected, the rejector activates and pushes the dented can into the reject bin.

[SCREENSHOT: Simulation showing can being rejected]

**You've closed the control loop:**
1. **Sees** — Camera captures the can
2. **Thinks** — Vision service classifies it
3. **Acts** — Rejector removes defective cans

This is the sense-think-act cycle that defines robotic systems.

## 3.6 Deploy as a Module

Your code works. Now package it as a module so it runs on the machine itself, not your laptop.

**Why deploy as a module?**

During development, your laptop runs the logic and talks to the machine over the network. This is great for iteration—edit, run, see results. But for production:
- The machine should run autonomously
- Network latency adds delay to the control loop
- Your laptop shouldn't need to be connected

Modules run directly on the machine as part of viam-server.

**Create the module entry point:**

{{< tabs >}}
{{% tab name="Go" %}}

Create `cmd/module/main.go`:

```go
package main

import (
	"go.viam.com/rdk/module"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/generic"

	inspector "inspection-module"
)

func main() {
	module.ModularMain(
		resource.APIModel{generic.API, inspector.Model},
	)
}
```

Now update `inspector.go` to add module registration. Here's the complete updated file—the new parts are the `Model` variable, `init()` function, and `newInspector` constructor:

```go
package inspector

import (
	"context"
	"fmt"

	"github.com/mitchellh/mapstructure"
	"go.viam.com/rdk/components/motor"
	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/generic"
	"go.viam.com/rdk/services/vision"
)

// Model is the full model triplet for this service.
var Model = resource.NewModel("your-org", "inspection", "inspector")

func init() {
	// Register this model so viam-server can instantiate it from config.
	resource.RegisterService(generic.API, Model,
		resource.Registration[resource.Resource, *Config]{
			Constructor: newInspector,
		},
	)
}

// newInspector is the module constructor called by viam-server.
// It extracts the typed config and calls the exported constructor.
func newInspector(
	ctx context.Context,
	deps resource.Dependencies,
	rawConf resource.Config,
	logger logging.Logger,
) (resource.Resource, error) {
	// Convert the raw JSON config to our typed Config struct.
	conf, err := resource.NativeConfig[*Config](rawConf)
	if err != nil {
		return nil, err
	}
	return NewInspector(ctx, deps, rawConf.ResourceName(), conf, logger)
}

// Config declares which dependencies the inspector needs.
type Config struct {
	Camera        string `json:"camera"`
	VisionService string `json:"vision_service"`
	Rejector      string `json:"rejector"`
}

// Validate checks the config and returns dependency names.
func (cfg *Config) Validate(path string) ([]string, []string, error) {
	if cfg.Camera == "" {
		return nil, nil, fmt.Errorf("camera is required")
	}
	if cfg.VisionService == "" {
		return nil, nil, fmt.Errorf("vision_service is required")
	}
	if cfg.Rejector == "" {
		return nil, nil, fmt.Errorf("rejector is required")
	}
	return []string{cfg.Camera, cfg.VisionService, cfg.Rejector}, nil, nil
}

// Inspector implements resource.Resource.
type Inspector struct {
	resource.AlwaysRebuild

	name   resource.Name
	conf   *Config
	logger logging.Logger

	detector vision.Service
	rejector motor.Motor
}

// NewInspector is the exported constructor called by both CLI and module.
func NewInspector(
	ctx context.Context,
	deps resource.Dependencies,
	name resource.Name,
	conf *Config,
	logger logging.Logger,
) (resource.Resource, error) {
	detector, err := vision.FromDependencies(deps, conf.VisionService)
	if err != nil {
		return nil, err
	}
	rejector, err := motor.FromDependencies(deps, conf.Rejector)
	if err != nil {
		return nil, err
	}

	return &Inspector{
		name:     name,
		conf:     conf,
		logger:   logger,
		detector: detector,
		rejector: rejector,
	}, nil
}

// The rest of the file (Name, DoCommand, Close, detect, inspect, reject)
// stays exactly the same as before.
```

This matches the viam-chess pattern:
- `init()` registers with a module constructor
- Module constructor (`newInspector`) extracts the config and calls the exported constructor
- Exported constructor (`NewInspector`) is used by both CLI and module

{{% /tab %}}
{{% tab name="Python" %}}

Create `main.py`:

```python
import asyncio
from viam.module.module import Module
from viam.services.generic import Generic

from inspector import Inspector

async def main():
    module = Module.from_args()
    module.add_model_from_registry(Generic.SUBTYPE, Inspector.MODEL)
    await module.start()

if __name__ == "__main__":
    asyncio.run(main())
```

Now update `inspector.py` to add module registration. The key changes are: import `Generic` and `Model`/`ModelFamily`, make `Inspector` extend `Generic`, and add the `MODEL` class attribute:

```python
from dataclasses import dataclass
from typing import Any, Mapping
from viam.components.motor import Motor
from viam.services.generic import Generic
from viam.services.vision import VisionClient
from viam.resource.types import Model, ModelFamily

@dataclass
class Config:
    camera: str
    vision_service: str
    rejector: str

    def validate(self) -> list[str]:
        """Check config and return dependency names."""
        if not self.camera:
            raise ValueError("camera is required")
        if not self.vision_service:
            raise ValueError("vision_service is required")
        if not self.rejector:
            raise ValueError("rejector is required")
        return [self.camera, self.vision_service, self.rejector]

class Inspector(Generic):
    """Inspector implements the generic service interface."""

    # Model triplet for module registration.
    MODEL = Model(ModelFamily("your-org", "inspection"), "inspector")

    def __init__(self, name: str, conf: Config, detector: VisionClient, rejector: Motor):
        self.name = name
        self.conf = conf
        self.detector = detector
        self.rejector = rejector

    @classmethod
    async def new(cls, deps: dict, cfg: Config) -> "Inspector":
        """Create an inspector by extracting dependencies from the map.
        Called by both CLI and module system."""
        detector = next((v for k, v in deps.items() if k.name == cfg.vision_service), None)
        rejector = next((v for k, v in deps.items() if k.name == cfg.rejector), None)
        return cls("inspector", cfg, detector, rejector)

    # The rest of the methods (do_command, close, _detect, _inspect, _reject)
    # stay exactly the same as before.
```

{{% /tab %}}
{{< /tabs >}}

**Create `meta.json`:**

```json
{
  "module_id": "your-org:inspection-module",
  "visibility": "private",
  "url": "",
  "description": "Can inspection with automatic rejection of defects",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "your-org:inspection:inspector"
    }
  ],
  "entrypoint": "bin/inspection-module"
}
```

**Build and package the module:**

```bash
# Build the binary
mkdir -p bin
go build -o bin/inspection-module cmd/module/main.go

# Create the upload tarball
tar czf module.tar.gz meta.json bin/
```

**Upload to the registry:**

```bash
viam module upload --version 1.0.0 --platform linux/amd64 module.tar.gz
```

> **Note:** Replace `your-org` in meta.json with your actual Viam organization namespace. You can find this in the Viam app under **Organization settings**.

**Add the module to your machine:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine
3. Select **Service** and search for `inspection-module`
4. Select your module from the results (it will show as `your-org:inspection-module`)
5. Click **Add module**

This adds both the module and creates a service configuration card.

**Configure the inspector service:**

In the service card that was created:

1. Name it `inspector`
2. Expand the **Attributes** section and add the dependencies:

```json
{
  "camera": "inspection-cam",
  "vision_service": "can-detector",
  "rejector": "rejector"
}
```

3. Click **Save** in the top right

**Verify it's running:**

1. Check the **Logs** tab for your machine
2. You should see the inspector module starting up
3. Watch the simulation—when a dented can passes under the camera, the rejector should activate

The machine now runs your inspection logic autonomously. The same code that ran on your laptop now runs on the machine as part of viam-server.

## 3.7 Summary

You built a working inspection system:

1. **Detect** — ML inference via the vision service
2. **Inspect** — Decision-making based on detection results
3. **Reject** — Actuation to remove defective cans

Your code ran on your laptop while the hardware ran on the remote machine. Then you packaged and deployed the same code as a module. **Same constructor, same `DoCommand`, different context.** That's module-first development.

**The module-first pattern:**
- **Config** — One field per dependency (declares what you need)
- **Constructor** — Extract dependencies using `FromDependencies`, return `resource.Resource`
- **DoCommand** — The generic service interface; all operations go through here
- **CLI** — Creates your service locally, calls `DoCommand`, just like the module system does

When you need to add another sensor or actuator, it's the same pattern: add to config, extract in constructor, add a command to `DoCommand`.

**Checkpoint:** Your inspection system runs autonomously on the machine. It sees, thinks, and acts—the complete control loop.

---

**[Continue to Part 4: Scale →](./part4.md)**
