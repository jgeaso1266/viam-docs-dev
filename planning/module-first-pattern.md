# Module-First Development Pattern

**Status:** 🟢 Reference

A comprehensive guide to the module-first development pattern for building Viam services. This pattern enables rapid iteration during development while producing production-ready deployable modules.

---

## Overview

The module-first pattern separates **where your code runs** from **what your code does**. During development, your code runs on your laptop while talking to remote hardware. For production, the same code runs on the machine itself as a module.

```
Development (CLI):
┌─────────────┐         ┌─────────────────┐
│ Your Laptop │ ──────► │ Remote Machine  │
│ (runs code) │   API   │ (has hardware)  │
└─────────────┘         └─────────────────┘

Production (Module):
┌─────────────────────────────────────────┐
│            Machine                      │
│  ┌─────────────┐    ┌───────────────┐  │
│  │ Your Module │───►│ Hardware      │  │
│  │ (runs code) │    │ (same machine)│  │
│  └─────────────┘    └───────────────┘  │
└─────────────────────────────────────────┘
```

**The key insight:** Your service constructor and logic are identical in both contexts. Only the entry point differs.

---

## Why This Pattern?

### Problems with Traditional Module Development

| Problem | Impact |
|---------|--------|
| **Slow iteration** | Change code → rebuild → upload → restart viam-server → test |
| **Remote debugging** | Logs are on the machine, not your terminal |
| **No breakpoints** | Can't attach a debugger to a running module |
| **Environment mismatch** | Development happens in a different context than production |
| **Deployment friction** | Every test requires a deployment cycle |

### How Module-First Solves These

| Solution | Benefit |
|----------|---------|
| **Local execution** | Change code → rebuild → run locally → see results immediately |
| **Local logs** | Output in your terminal, add print statements freely |
| **Debugger support** | Attach debuggers, set breakpoints, inspect state |
| **Same code path** | CLI and module use identical constructors and logic |
| **Deploy when ready** | Only deploy after the code works |

---

## Directory Structure

A typical module-first project:

```
your-module/
├── cmd/
│   ├── module/main.go     # Production: module entry point
│   └── cli/main.go        # Development: CLI entry point
├── service.go             # Your service implementation
├── common.go              # Shared definitions (optional)
├── meta.json              # Module metadata for registry
├── Makefile               # Build automation
├── go.mod
└── go.sum
```

**Why this structure?**

- `cmd/` separates entry points from library code
- Service logic in the root is importable by both entry points
- `common.go` is useful when you have multiple services sharing definitions
- `meta.json` is required for registry upload

**Variations are fine.** Some modules put everything in one file. Some have deep package hierarchies. The key is that your service logic is importable by both CLI and module entry points.

> **Example:** [viam-chess](https://github.com/erh/viam-chess) uses this structure with `chess.go` and `piece_finder.go` as two services in the root, plus `common.go` for the shared model family definition.

---

## The Pattern: Step by Step

### 1. Define Your Config

The config struct declares what dependencies your service needs. Users specify these in their machine configuration.

```go
type Config struct {
    Camera        string `json:"camera"`
    VisionService string `json:"vision_service"`
    // Add fields for each dependency your service needs
}
```

**Why JSON tags?** These must match the keys users write in their machine config JSON. Without tags, Go uses the field name directly, which may not match user expectations.

### 2. Implement Validate

The `Validate` method checks the config and returns dependency names. The module system uses these to ensure dependencies exist before constructing your service.

```go
func (cfg *Config) Validate(path string) ([]string, []string, error) {
    // Check required fields
    if cfg.Camera == "" {
        return nil, nil, fmt.Errorf("camera is required")
    }
    if cfg.VisionService == "" {
        return nil, nil, fmt.Errorf("vision_service is required")
    }

    // Return: (required deps, optional deps, error)
    return []string{cfg.Camera, cfg.VisionService}, nil, nil
}
```

**Why return dependency names?** The module system builds a dependency graph. By declaring dependencies, you ensure they're initialized before your service and that configuration errors are caught early.

**The signature:** `([]string, []string, error)` - first slice is required dependencies, second is optional. If an optional dependency doesn't exist, your constructor still gets called.

### 3. Define Your Service Struct

The struct holds everything your service needs at runtime.

```go
type MyService struct {
    resource.AlwaysRebuild   // How to handle config changes

    name   resource.Name     // This instance's resource name
    conf   *Config           // The validated config
    logger logging.Logger    // For logging

    // Dependencies (extracted in constructor)
    cam      camera.Camera
    detector vision.Service
}
```

**Why `resource.AlwaysRebuild`?** When config changes, Viam can either rebuild your service from scratch or call a `Reconfigure` method. `AlwaysRebuild` chooses rebuild, which is simpler. For services with expensive initialization, implement `Reconfigure` instead.

**Why store `conf`?** Methods often need config values. For example, `conf.Camera` gives you the camera name for calling `DetectionsFromCamera`.

### 4. Create the Module Constructor

The module constructor is called by the module system. It extracts the typed config and delegates to your exported constructor.

```go
func newMyService(
    ctx context.Context,
    deps resource.Dependencies,
    rawConf resource.Config,
    logger logging.Logger,
) (resource.Resource, error) {
    // Extract your typed config
    conf, err := resource.NativeConfig[*Config](rawConf)
    if err != nil {
        return nil, err
    }

    // Delegate to exported constructor
    return NewMyService(ctx, deps, rawConf.ResourceName(), conf, logger)
}
```

**Why a separate function?** The module system passes `resource.Config` (generic). Your exported constructor takes `*Config` (typed). This wrapper does the conversion. It's a thin layer that exists only to bridge the module system's interface to your typed interface.

### 5. Create the Exported Constructor

This is the constructor both CLI and module use. It extracts dependencies and initializes the service.

```go
func NewMyService(
    ctx context.Context,
    deps resource.Dependencies,
    name resource.Name,
    conf *Config,
    logger logging.Logger,
) (resource.Resource, error) {
    // Extract typed dependencies
    cam, err := camera.FromDependencies(deps, conf.Camera)
    if err != nil {
        return nil, err
    }

    detector, err := vision.FromDependencies(deps, conf.VisionService)
    if err != nil {
        return nil, err
    }

    return &MyService{
        name:     name,
        conf:     conf,
        logger:   logger,
        cam:      cam,
        detector: detector,
    }, nil
}
```

**Why `FromDependencies`?** The `deps` map contains `resource.Resource` interfaces. `camera.FromDependencies` extracts a `camera.Camera` specifically, with proper type checking and error messages.

**This is the key to module-first development.** The same constructor works whether deps come from a remote machine (CLI) or local viam-server (module).

### 6. Implement Required Methods

Every service must implement these methods:

```go
func (s *MyService) Name() resource.Name {
    return s.name
}

func (s *MyService) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
    // Parse and dispatch commands
}

func (s *MyService) Close(ctx context.Context) error {
    // Cleanup: cancel goroutines, close connections, etc.
    return nil
}
```

**If Close() does nothing**, you can embed `resource.TriviallyCloseable` instead of implementing it:

```go
type MyService struct {
    resource.AlwaysRebuild
    resource.TriviallyCloseable  // Provides no-op Close()
    // ...
}
```

### 7. Implement DoCommand

`DoCommand` is the generic service interface. All operations go through it.

```go
// Define a struct for parsing commands
type myCmd struct {
    Capture bool
    Detect  bool
    Process struct {
        Input  string
        Rounds int
    }
}

func (s *MyService) DoCommand(ctx context.Context, cmdMap map[string]interface{}) (map[string]interface{}, error) {
    var cmd myCmd
    if err := mapstructure.Decode(cmdMap, &cmd); err != nil {
        return nil, err
    }

    if cmd.Capture {
        // Handle capture command
        return s.handleCapture(ctx)
    }

    if cmd.Detect {
        // Handle detect command
        return s.handleDetect(ctx)
    }

    if cmd.Process.Input != "" {
        // Handle process command with parameters
        return s.handleProcess(ctx, cmd.Process.Input, cmd.Process.Rounds)
    }

    return nil, fmt.Errorf("unknown command: %v", cmdMap)
}
```

**Why mapstructure?** It converts `map[string]interface{}` to typed structs, handling nested structures and type conversions. This is cleaner than manual map access and provides better error messages.

**Why a command struct?** Type safety, IDE support, and cleaner dispatch logic. The struct documents what commands your service accepts.

### 8. Register the Service

Registration tells the module system about your service.

```go
// Define your model identifier
var Model = resource.NewModel("your-org", "your-family", "your-model")

func init() {
    resource.RegisterService(generic.API, Model,
        resource.Registration[resource.Resource, *Config]{
            Constructor: newMyService,
        },
    )
}
```

**Model naming:** `your-org:your-family:your-model` becomes the identifier users put in their config. Choose meaningful names.

**Which API?** Most custom services use `generic.API`. If you're implementing a specific interface (vision, motion, etc.), use that API instead.

> **Example:** viam-chess registers two models - one with `generic.API` for the chess service, one with `vision.API` for the piece finder.

### 9. Create the Module Entry Point

The module entry point starts viam-server's module system with your models.

```go
// cmd/module/main.go
package main

import (
    "go.viam.com/rdk/module"
    "go.viam.com/rdk/resource"
    "go.viam.com/rdk/services/generic"

    mymodule "your-module"  // Import your package
)

func main() {
    module.ModularMain(
        resource.APIModel{generic.API, mymodule.Model},
        // Add more models if your module provides multiple services
    )
}
```

**Multiple services?** Pass multiple `resource.APIModel` entries to `ModularMain`.

### 10. Create the CLI Entry Point

The CLI connects to a remote machine and creates your service locally.

```go
// cmd/cli/main.go
package main

import (
    "context"
    "flag"
    "fmt"

    "github.com/erh/vmodutils"
    "go.viam.com/rdk/logging"
    "go.viam.com/rdk/services/generic"

    mymodule "your-module"
)

func main() {
    if err := run(); err != nil {
        panic(err)
    }
}

func run() error {
    ctx := context.Background()
    logger := logging.NewLogger("cli")

    host := flag.String("host", "", "Machine address")
    cmd := flag.String("cmd", "", "Command to execute")
    flag.Parse()

    if *host == "" {
        return fmt.Errorf("need -host")
    }
    if *cmd == "" {
        return fmt.Errorf("need -cmd")
    }

    // Config with dependency names matching your machine's config
    cfg := mymodule.Config{
        Camera:        "my-camera",
        VisionService: "my-detector",
    }

    // Validate before connecting
    if _, _, err := cfg.Validate(""); err != nil {
        return err
    }

    // Connect to remote machine
    machine, err := vmodutils.ConnectToHostFromCLIToken(ctx, *host, logger)
    if err != nil {
        return err
    }
    defer machine.Close(ctx)

    // Convert machine resources to Dependencies
    deps, err := vmodutils.MachineToDependencies(machine)
    if err != nil {
        return err
    }

    // Create service with SAME constructor module uses
    svc, err := mymodule.NewMyService(ctx, deps, generic.Named("cli-instance"), &cfg, logger)
    if err != nil {
        return err
    }
    defer svc.Close(ctx)

    // Call DoCommand
    result, err := svc.DoCommand(ctx, map[string]interface{}{*cmd: true})
    if err != nil {
        return err
    }

    logger.Infof("Result: %v", result)
    return nil
}
```

**Why vmodutils?**
- `ConnectToHostFromCLIToken` uses your `viam login` credentials
- `MachineToDependencies` converts machine resources to the `resource.Dependencies` format your constructor expects

**The magic:** Your service runs on your laptop, but `cam.Image()` fetches from the remote camera. The Viam SDK handles the RPC transparently.

---

## Build System

A typical Makefile:

```makefile
MODULE_NAME := your-module
CLI_BINARY := bin/cli
MODULE_BINARY := bin/$(MODULE_NAME)

.PHONY: all cli module clean test

all: cli module

cli: cmd/cli/main.go *.go
	go build -o $(CLI_BINARY) ./cmd/cli/

module: cmd/module/main.go *.go
	go build -o $(MODULE_BINARY) ./cmd/module/

module.tar.gz: module meta.json
	tar czf $@ $(MODULE_BINARY) meta.json

test:
	go test ./...

clean:
	rm -rf bin/ module.tar.gz
```

---

## Module Metadata

`meta.json` describes your module for the registry:

```json
{
  "$schema": "https://dl.viam.dev/module.schema.json",
  "module_id": "your-org:your-module",
  "visibility": "public",
  "description": "What your module does",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "your-org:your-family:your-model"
    }
  ],
  "entrypoint": "bin/your-module",
  "build": {
    "build": "make module.tar.gz",
    "path": "module.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  }
}
```

---

## Development Workflow

### Initial Setup

```bash
mkdir your-module && cd your-module
go mod init your-module
go get go.viam.com/rdk
go get github.com/erh/vmodutils
go get github.com/mitchellh/mapstructure

# Authenticate for CLI usage
viam login
```

### Development Loop

```bash
# Build CLI
make cli

# Run against remote machine
./bin/cli -host your-machine.viam.cloud -cmd detect

# See results immediately
# Edit code, rebuild, run again - no deployment needed
```

### Deploy When Ready

```bash
# Build and package
make module.tar.gz

# Upload to registry
viam module upload --version 1.0.0 --platform linux/amd64
```

---

## Common Patterns

### Commands with Parameters

```go
type myCmd struct {
    Move struct {
        From string
        To   string
    }
}

// CLI invocation:
result, err := svc.DoCommand(ctx, map[string]interface{}{
    "move": map[string]interface{}{
        "from": "a1",
        "to":   "b2",
    },
})
```

### Background Operations

For services that run continuously:

```go
type MyService struct {
    // ...
    cancelCtx  context.Context
    cancelFunc context.CancelFunc
}

func NewMyService(...) (resource.Resource, error) {
    cancelCtx, cancelFunc := context.WithCancel(context.Background())

    s := &MyService{
        cancelCtx:  cancelCtx,
        cancelFunc: cancelFunc,
        // ...
    }

    go s.backgroundLoop()

    return s, nil
}

func (s *MyService) backgroundLoop() {
    ticker := time.NewTicker(time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-s.cancelCtx.Done():
            return
        case <-ticker.C:
            // Periodic work
        }
    }
}

func (s *MyService) Close(ctx context.Context) error {
    s.cancelFunc()
    return nil
}
```

### Thread-Safe DoCommand

If commands shouldn't run concurrently:

```go
type MyService struct {
    // ...
    mu sync.Mutex
}

func (s *MyService) DoCommand(ctx context.Context, cmd map[string]interface{}) (map[string]interface{}, error) {
    s.mu.Lock()
    defer s.mu.Unlock()

    // ... handle command
}
```

### Multiple Services Per Module

Define each service in its own file with its own model:

```go
// common.go
var family = resource.ModelNamespace("your-org").WithFamily("your-family")

// service_a.go
var ModelA = family.WithModel("service-a")

func init() {
    resource.RegisterService(generic.API, ModelA, ...)
}

// service_b.go
var ModelB = family.WithModel("service-b")

func init() {
    resource.RegisterService(vision.API, ModelB, ...)
}

// cmd/module/main.go
func main() {
    module.ModularMain(
        resource.APIModel{generic.API, mymodule.ModelA},
        resource.APIModel{vision.API, mymodule.ModelB},
    )
}
```

---

## Reference Implementation

The [viam-chess](https://github.com/erh/viam-chess) project demonstrates this pattern with:

- Two services: chess game logic (`generic.API`) and piece detection (`vision.API`)
- Shared family definition in `common.go`
- CLI for development testing
- Full Makefile with build targets

Study it as a working example of these patterns in production use.

---

## Checklist

Before deploying your module:

**Config:**
- [ ] All fields have JSON tags matching expected config keys
- [ ] `Validate()` returns `([]string, []string, error)`
- [ ] `Validate()` checks all required fields
- [ ] `Validate()` returns all dependency names

**Service struct:**
- [ ] Embeds `resource.AlwaysRebuild` (or implements `Reconfigure`)
- [ ] Embeds `resource.TriviallyCloseable` or implements `Close()`
- [ ] Stores `name`, `conf`, `logger`
- [ ] Stores all dependencies as typed fields

**Constructors:**
- [ ] Module constructor extracts config with `resource.NativeConfig`
- [ ] Module constructor calls exported constructor
- [ ] Exported constructor signature: `(ctx, deps, name, conf, logger) -> (resource.Resource, error)`
- [ ] Exported constructor extracts deps with `FromDependencies`

**Methods:**
- [ ] `Name()` returns stored name
- [ ] `DoCommand()` uses `mapstructure.Decode`
- [ ] `Close()` cancels goroutines and cleans up

**Registration:**
- [ ] Model defined with appropriate namespace/family/model
- [ ] `init()` calls `resource.RegisterService`
- [ ] Module main calls `module.ModularMain` with all models

**CLI:**
- [ ] Validates config before connecting
- [ ] Uses `vmodutils.ConnectToHostFromCLIToken`
- [ ] Uses `vmodutils.MachineToDependencies`
- [ ] Calls same constructor as module
- [ ] Calls `DoCommand`, not internal methods directly

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "need a host" | Missing `-host` flag | Get machine address from Viam app Code Sample tab |
| "failed to connect" | Auth or network issue | Run `viam login`, verify machine is online |
| "resource not found" | Dependency name mismatch | Check config names match machine component names |
| "unknown command" | Command not in DoCommand | Check command struct field names and dispatch logic |
| "cannot unmarshal" | mapstructure type mismatch | Verify command map structure matches command struct |
