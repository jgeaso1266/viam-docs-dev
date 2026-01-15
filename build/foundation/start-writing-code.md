# Start Writing Code

**Status:** 🟡 Draft

**Time:** ~30 minutes
**Prerequisites:** Connect to Cloud, Add a Camera
**Works with:** Simulation | Real Hardware

---

## What You'll Learn

- Initialize a Viam module from scratch
- Structure your code for both local testing and deployment
- Test against remote hardware from your laptop
- Deploy when ready for autonomous operation

## The Pattern: Module-First Development

Start with a module, not a script. A module is code that:
- Defines a service with configuration and commands
- Can run locally (for testing) or on the machine (for production)
- Uses the same code in both cases

```
Development:                          Production:
┌─────────────────┐                   ┌─────────────────┐
│   Your Laptop   │                   │    Machine      │
│                 │                   │                 │
│  Module code    │    WebRTC         │  viam-server    │
│  runs here      │◄──────────►       │  + module       │
│                 │   (components)    │  runs here      │
│  CLI sends      │                   │                 │
│  commands       │                   │  Commands via   │
└─────────────────┘                   │  app or API     │
         │                            └─────────────────┘
         │ uses remote
         ▼ components
┌─────────────────┐
│    Machine      │
│  viam-server    │
│  + components   │
└─────────────────┘
```

---

## Step 1: Initialize Your Module

Create the module structure:

```bash
mkdir my-inspection-module
cd my-inspection-module
```

**Python:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate
pip install viam-sdk
```

**Go:**
```bash
go mod init my-inspection-module
go get go.viam.com/rdk
```

---

## Step 2: Define Your Service

Create the service with configuration and command handling.

**Python** (`inspection.py`):
```python
from typing import ClassVar, Mapping, Any, Optional
from viam.module.types import Reconfigurable
from viam.resource.types import Model, ModelFamily
from viam.services.generic import Generic
from viam.components.camera import Camera
from viam.services.vision import VisionClient
from viam.proto.app.robot import ServiceConfig
from viam.resource.base import ResourceBase
from viam.utils import struct_to_dict

class InspectionService(Generic, Reconfigurable):
    MODEL: ClassVar[Model] = Model(
        ModelFamily("my-org", "inspection"),
        "inspector"
    )

    def __init__(self, name: str):
        super().__init__(name)
        self.camera: Optional[Camera] = None
        self.detector: Optional[VisionClient] = None

    @classmethod
    def new(cls, config: ServiceConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        service = cls(config.name)
        service.reconfigure(config, dependencies)
        return service

    def reconfigure(self, config: ServiceConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        attrs = struct_to_dict(config.attributes)

        # Get dependencies by name from config
        camera_name = attrs.get("camera", "inspection-cam")
        detector_name = attrs.get("detector", "part-detector")

        self.camera = dependencies[Camera.get_resource_name(camera_name)]
        self.detector = dependencies[VisionClient.get_resource_name(detector_name)]

    async def do_command(
        self,
        command: Mapping[str, Any],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, Any]:

        if "inspect" in command:
            return await self._do_inspect()

        if "capture" in command:
            path = command.get("path", "capture.png")
            return await self._do_capture(path)

        raise ValueError(f"Unknown command: {command}")

    async def _do_inspect(self) -> Mapping[str, Any]:
        """Run inspection and return results."""
        image = await self.camera.get_image()
        detections = await self.detector.get_detections(image)

        results = []
        for d in detections:
            results.append({
                "class": d.class_name,
                "confidence": d.confidence,
            })

        return {"detections": results}

    async def _do_capture(self, path: str) -> Mapping[str, Any]:
        """Capture and save an image."""
        image = await self.camera.get_image()
        image.save(path)
        return {"saved": path}
```

**Go** (`inspection.go`):
```go
package inspection

import (
    "context"
    "go.viam.com/rdk/components/camera"
    "go.viam.com/rdk/resource"
    "go.viam.com/rdk/services/generic"
    "go.viam.com/rdk/services/vision"
)

var Model = resource.NewModel("my-org", "inspection", "inspector")

type Config struct {
    Camera   string `json:"camera"`
    Detector string `json:"detector"`
}

func (cfg *Config) Validate(path string) ([]string, error) {
    // Return dependencies so Viam knows what this service needs
    deps := []string{cfg.Camera, cfg.Detector}
    return deps, nil
}

type inspectionService struct {
    resource.Named
    camera   camera.Camera
    detector vision.Service
}

func NewInspectionService(
    ctx context.Context,
    deps resource.Dependencies,
    conf resource.Config,
    logger logging.Logger,
) (resource.Resource, error) {
    svc := &inspectionService{
        Named: conf.ResourceName().AsNamed(),
    }

    cfg, err := resource.NativeConfig[*Config](conf)
    if err != nil {
        return nil, err
    }

    // Get dependencies by name
    svc.camera, err = camera.FromDependencies(deps, cfg.Camera)
    if err != nil {
        return nil, err
    }

    svc.detector, err = vision.FromDependencies(deps, cfg.Detector)
    if err != nil {
        return nil, err
    }

    return svc, nil
}

func (s *inspectionService) DoCommand(
    ctx context.Context,
    cmd map[string]interface{},
) (map[string]interface{}, error) {

    if _, ok := cmd["inspect"]; ok {
        return s.doInspect(ctx)
    }

    if path, ok := cmd["capture"].(string); ok {
        return s.doCapture(ctx, path)
    }

    return nil, fmt.Errorf("unknown command: %v", cmd)
}

func (s *inspectionService) doInspect(ctx context.Context) (map[string]interface{}, error) {
    img, err := s.camera.Image(ctx, nil, nil)
    if err != nil {
        return nil, err
    }

    detections, err := s.detector.Detections(ctx, img, nil)
    if err != nil {
        return nil, err
    }

    results := make([]map[string]interface{}, len(detections))
    for i, d := range detections {
        results[i] = map[string]interface{}{
            "class":      d.Label(),
            "confidence": d.Score(),
        }
    }

    return map[string]interface{}{"detections": results}, nil
}
```

---

## Step 3: Create a CLI for Testing

The CLI instantiates your service locally but uses remote components:

**Python** (`cli.py`):
```python
import asyncio
import argparse
from viam.robot.client import RobotClient
from inspection import InspectionService

async def connect():
    # Get these from your machine's CONNECT tab
    opts = RobotClient.Options.with_api_key(
        api_key='your-api-key',
        api_key_id='your-api-key-id'
    )
    return await RobotClient.at_address('your-machine.viam.cloud', opts)

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["inspect", "capture"])
    parser.add_argument("--path", default="capture.png")
    args = parser.parse_args()

    robot = await connect()

    try:
        # Create service instance with remote dependencies
        # The service runs here, but camera/detector are on the machine
        deps = {
            Camera.get_resource_name("inspection-cam"):
                Camera.from_robot(robot, "inspection-cam"),
            VisionClient.get_resource_name("part-detector"):
                VisionClient.from_robot(robot, "part-detector"),
        }

        service = InspectionService("test-inspector")
        service.reconfigure(mock_config(), deps)

        # Execute command
        if args.command == "inspect":
            result = await service.do_command({"inspect": True})
            for d in result["detections"]:
                print(f"{d['class']}: {d['confidence']:.2f}")

        elif args.command == "capture":
            result = await service.do_command({"capture": args.path})
            print(f"Saved to {result['saved']}")

    finally:
        await robot.close()

if __name__ == "__main__":
    asyncio.run(main())
```

**Go** (`cmd/cli/main.go`):
```go
package main

import (
    "context"
    "flag"
    "fmt"

    "go.viam.com/rdk/logging"
    "github.com/erh/vmodutils"

    "my-inspection-module/inspection"
)

func main() {
    ctx := context.Background()
    logger := logging.NewLogger("cli")

    host := flag.String("host", "", "machine address")
    cmd := flag.String("cmd", "", "command: inspect, capture")
    path := flag.String("path", "capture.png", "output path for capture")
    flag.Parse()

    // Connect to remote machine
    machine, err := vmodutils.ConnectToHostFromCLIToken(ctx, *host, logger)
    if err != nil {
        panic(err)
    }
    defer machine.Close(ctx)

    // Get remote components as dependencies
    deps, err := vmodutils.MachineToDependencies(machine)
    if err != nil {
        panic(err)
    }

    // Create service locally with remote dependencies
    cfg := &inspection.Config{
        Camera:   "inspection-cam",
        Detector: "part-detector",
    }

    svc, err := inspection.NewInspectionService(ctx, deps, mockConfig(cfg), logger)
    if err != nil {
        panic(err)
    }

    // Execute command
    switch *cmd {
    case "inspect":
        result, err := svc.DoCommand(ctx, map[string]interface{}{"inspect": true})
        if err != nil {
            panic(err)
        }
        fmt.Printf("Results: %v\n", result)

    case "capture":
        result, err := svc.DoCommand(ctx, map[string]interface{}{"capture": *path})
        if err != nil {
            panic(err)
        }
        fmt.Printf("Saved: %v\n", result)
    }
}
```

---

## Step 4: Test Locally

Run your CLI against the remote machine:

```bash
# Python
python cli.py inspect
python cli.py capture --path test.png

# Go
go run cmd/cli/main.go -host your-machine.viam.cloud -cmd inspect
go run cmd/cli/main.go -host your-machine.viam.cloud -cmd capture -path test.png
```

Your service code runs on your laptop. Camera and detector calls go to the machine. Iterate on the service logic without deploying.

---

## Step 5: Deploy When Ready

When you need autonomous operation, package and deploy the module:

1. Create `meta.json`:
```json
{
  "module_id": "my-org:my-inspection-module",
  "visibility": "private",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "my-org:inspection:inspector"
    }
  ]
}
```

2. Build and upload:
```bash
viam module build
viam module upload
```

3. Add to your machine config in the Viam app

Now the service runs on the machine. Commands come via the Viam app, API, or triggers—not your laptop.

---

## Why Module-First?

| Approach | Problem |
|----------|---------|
| Script first, module later | Rewrite when you need deployment |
| Module first | Same code for testing and production |

The module structure forces you to:
- Define configuration explicitly
- Declare dependencies
- Use the DoCommand pattern for operations

These are the same requirements for deployment. No rewrite needed.

---

## Try It

1. Initialize a module with the structure above
2. Define a simple service that captures an image
3. Create a CLI that tests it against your machine
4. Run the CLI and verify it works

---

## What's Next

- [Add Computer Vision](../perception/add-computer-vision.md) — Add detection to your service
- [Building Modules](../../reference/modules.md) — Full module packaging guide
- [Trigger on Detection](../stationary-vision/trigger-on-detection.md) — Automate responses

---

## Key Takeaway

**Start with a module, not a script. The same service code runs locally for testing (via CLI) or deployed for production. Structure it right from the beginning.**
