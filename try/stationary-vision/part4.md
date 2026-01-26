# Part 4: Deploy as a Module (~20 min)

[← Back to Overview](./index.md) | [← Part 3: Build the Inspector](./part3.md)

---

**Goal:** Package your inspection logic as a module and deploy it to run on the machine.

**Skills:** Viam module structure, resource interfaces, module deployment.

## What You'll Do

In Part 3, you built inspection logic that runs from your laptop. That's great for development, but in production you need the code running on the machine itself—so it works even when your laptop is closed.

In this part, you'll:
1. Add the `DoCommand` interface so clients can call your inspector
2. Structure the code as a Viam resource
3. Register it as a module
4. Deploy it to the machine

---

## 4.1 Add the DoCommand Interface

Before turning this into a module, you need to expose your methods through Viam's **generic service** interface. Generic services use a single `DoCommand` method that accepts arbitrary commands as a map.

**Why DoCommand?** It provides flexibility without defining a custom API. Any client can send commands like `{"detect": true}` or `{"inspect": true}` without needing generated client code. This is ideal for application-specific logic like our inspector.

**Add the mapstructure import:**

```go
import (
	// ... existing imports ...
	"github.com/mitchellh/mapstructure"
)
```

Run `go get github.com/mitchellh/mapstructure` if needed.

**Add the Command struct and DoCommand method to `inspector.go`:**

```go
// Command represents the commands the inspector accepts via DoCommand.
// Using a struct with mapstructure tags lets us safely decode the
// map[string]interface{} that DoCommand receives.
type Command struct {
	Detect  bool `mapstructure:"detect"`
	Inspect bool `mapstructure:"inspect"`
}

// DoCommand handles incoming commands from clients.
// This is the generic service interface - all operations go through here.
// Using a single entry point with command maps is more flexible than
// defining separate RPC methods for each operation.
func (i *Inspector) DoCommand(ctx context.Context, req map[string]interface{}) (map[string]interface{}, error) {
	// Decode the request map into our typed Command struct.
	// mapstructure handles type coercion (e.g., JSON numbers to bools).
	var cmd Command
	if err := mapstructure.Decode(req, &cmd); err != nil {
		return nil, fmt.Errorf("failed to decode command: %w", err)
	}

	// Dispatch based on which command flag is set.
	// We use a switch on bools rather than a string command name
	// because it's more flexible - could support multiple flags at once.
	switch {
	case cmd.Detect:
		label, confidence, err := i.Detect(ctx)
		if err != nil {
			return nil, err
		}
		return map[string]interface{}{
			"label":      label,
			"confidence": confidence,
		}, nil

	case cmd.Inspect:
		label, confidence, rejected, err := i.Inspect(ctx)
		if err != nil {
			return nil, err
		}
		return map[string]interface{}{
			"label":      label,
			"confidence": confidence,
			"rejected":   rejected,
		}, nil

	default:
		return nil, fmt.Errorf("unknown command: %v", req)
	}
}
```

**Update the CLI to use DoCommand:**

This verifies the interface works the same way it will when called remotely. Replace the switch statement you added in section 3.5 with this version that calls through `DoCommand`:

```go
switch *cmd {
case "detect":
	// Call through DoCommand to verify the interface works
	result, err := insp.DoCommand(ctx, map[string]interface{}{"detect": true})
	if err != nil {
		return err
	}
	logger.Infof("Detection: %s (%.1f%%)",
		result["label"], result["confidence"].(float64)*100)

case "inspect":
	result, err := insp.DoCommand(ctx, map[string]interface{}{"inspect": true})
	if err != nil {
		return err
	}
	logger.Infof("Inspection: %s (%.1f%%), rejected=%v",
		result["label"], result["confidence"].(float64)*100, result["rejected"])

default:
	return fmt.Errorf("unknown command: %s", *cmd)
}
```

**Test it:**

```bash
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd inspect
```

Output should be identical to before. The behavior hasn't changed—you've just formalized the interface.

---

## 4.2 Structure as a Viam Resource

To run as a module, your inspector must implement Viam's `resource.Resource` interface. This requires a few additions.

**Update the Inspector struct:**

Add the embedded `AlwaysRebuild` struct and a `name` field:

```go
// Inspector implements resource.Resource for the generic service API.
type Inspector struct {
	// AlwaysRebuild is an embedded struct that tells Viam to destroy and
	// recreate this service when config changes, rather than trying to
	// update it in place. This is simpler than implementing Reconfigure().
	resource.AlwaysRebuild  // NEW

	name     resource.Name  // NEW
	conf     *Config
	logger   logging.Logger
	detector vision.Service
	rejector motor.Motor
}
```

**Update the constructor to accept a resource name:**

Add a `name` parameter and include it in the returned struct:

```go
// NewInspector creates an inspector. This constructor is used by both CLI and module.
func NewInspector(
	deps resource.Dependencies,
	name resource.Name,  // NEW parameter
	conf *Config,
	logger logging.Logger,
) (*Inspector, error) {
	detector, err := vision.FromDependencies(deps, conf.VisionService)
	if err != nil {
		return nil, fmt.Errorf("failed to get vision service %q: %w", conf.VisionService, err)
	}

	rejector, err := motor.FromDependencies(deps, conf.Rejector)
	if err != nil {
		return nil, fmt.Errorf("failed to get rejector %q: %w", conf.Rejector, err)
	}

	return &Inspector{
		name:     name,  // NEW
		conf:     conf,
		logger:   logger,
		detector: detector,
		rejector: rejector,
	}, nil
}
```

**Add required interface methods:**

```go
// Name returns the resource name. Required by resource.Resource.
func (i *Inspector) Name() resource.Name {
	return i.name
}

// Close cleans up the resource. Required by resource.Resource.
// Our inspector doesn't hold any resources that need cleanup -
// the vision service and motor are managed by Viam.
func (i *Inspector) Close(ctx context.Context) error {
	return nil
}
```

**Update the CLI for the new constructor signature:**

Add the import:

```go
import (
	// ... existing imports ...
	"go.viam.com/rdk/services/generic"
)
```

Update the `NewInspector` call to pass a resource name as the second argument:

```go
// generic.Named creates a resource name for the generic service API.
// The string "inspector" is just a local name for logging/debugging.
insp, err := inspector.NewInspector(deps, generic.Named("inspector"), conf, logger)
//                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^ NEW argument
```

**Test it:**

```bash
go run ./cmd/cli -host your-machine-main.abc123.viam.cloud -cmd inspect
```

Still works. You've restructured the code without changing behavior.

---

## 4.3 Add Module Registration

Now add the code that lets viam-server discover and instantiate your inspector.

**Add the generic import to `inspector.go`:**

```go
import (
	// ... existing imports ...
	"go.viam.com/rdk/services/generic"
)
```

**Add the Model variable and init function:**

```go
// Model is the full model triplet that identifies this service type.
// Format: namespace:family:model
// - "acme" is your organization namespace (replace with yours from Viam app)
// - "inspection" is the model family (groups related models)
// - "inspector" is the specific model name
var Model = resource.NewModel("acme", "inspection", "inspector")

func init() {
	// Register this model with Viam's resource registry.
	// This runs automatically when the module binary starts (due to Go's init semantics).
	// The registration tells viam-server how to create instances of this service.
	resource.RegisterService(generic.API, Model,
		// Registration is a generic type parameterized by:
		// - resource.Resource: the interface our service implements
		// - *Config: the config type for type-safe config parsing
		resource.Registration[resource.Resource, *Config]{
			Constructor: createInspector,
		},
	)
}

// createInspector is the constructor that viam-server calls.
// It receives raw config (from JSON) and must extract our typed Config.
func createInspector(
	ctx context.Context,
	deps resource.Dependencies,
	rawConf resource.Config,
	logger logging.Logger,
) (resource.Resource, error) {
	// NativeConfig extracts our typed *Config from the raw config.
	// This uses the JSON tags we defined on Config fields.
	conf, err := resource.NativeConfig[*Config](rawConf)
	if err != nil {
		return nil, fmt.Errorf("failed to parse config: %w", err)
	}
	// Delegate to our shared constructor
	return NewInspector(deps, rawConf.ResourceName(), conf, logger)
}
```

**Create the module entry point:**

Create the directory and file:

```bash
mkdir -p cmd/module
```

Create `cmd/module/main.go`:

```go
package main

import (
	"go.viam.com/rdk/module"
	"go.viam.com/rdk/resource"
	"go.viam.com/rdk/services/generic"

	// This blank import runs the inspector package's init() function,
	// which registers our model with Viam's resource registry.
	// Without this import, viam-server wouldn't know our model exists.
	inspector "inspection-module"
)

func main() {
	// ModularMain starts the module and handles communication with viam-server.
	// We pass our API and Model so the module knows what it provides.
	module.ModularMain(
		resource.APIModel{API: generic.API, Model: inspector.Model},
	)
}
```

**Build the module:**

```bash
mkdir -p bin
go build -o bin/inspection-module ./cmd/module
```

---

## 4.4 Deploy to the Machine

Package your module and upload it to the Viam registry.

**Create `meta.json`:**

```json
{
  "module_id": "acme:inspection-module",
  "visibility": "private",
  "url": "",
  "description": "Can inspection with automatic rejection of defects",
  "models": [
    {
      "api": "rdk:service:generic",
      "model": "acme:inspection:inspector"
    }
  ],
  "entrypoint": "bin/inspection-module"
}
```

Replace `acme` with your Viam organization namespace (find it in the Viam app under **Organization → Settings**).

**Package the module:**

```bash
tar czf module.tar.gz meta.json bin/
```

**Upload to the registry:**

```bash
viam module upload --version 1.0.0 --platform linux/amd64 module.tar.gz
```

> **Note:** Use `linux/arm64` if your machine runs on ARM (like Raspberry Pi).

**Add the module to your machine:**

1. In the Viam app, go to your machine's **Configure** tab
2. Click **+** next to your machine
3. Select **Local module**, then **Local module**
4. Search for your module name (e.g., `acme:inspection-module`)
5. Click **Add module**

**Add the inspector service:**

1. Click **+** next to your machine
2. Select **Service**, then **generic**
3. For **Model**, select your model (e.g., `acme:inspection:inspector`)
4. Name it `inspector`
5. Click **Create**

**Configure the service:**

In the inspector's configuration panel, set the attributes:

```json
{
  "camera": "inspection-cam",
  "vision_service": "can-detector",
  "rejector": "rejector"
}
```

Click **Save**.

**Verify it's running:**

1. Go to the **Logs** tab for your machine
2. Look for log messages from the inspector module
3. You should see it starting up and connecting to its dependencies

The inspector now runs on the machine itself, not your laptop. It will continuously inspect cans and reject defective ones—even when you're not connected.

---

## 4.5 Summary

You packaged your inspection logic as a Viam module:

1. **Added DoCommand** — exposed operations via the generic service interface
2. **Structured as a resource** — implemented Viam's resource interface
3. **Registered as a module** — made it discoverable by viam-server
4. **Deployed** — packaged and uploaded to the registry

**The key pattern:** One constructor (`NewInspector`) used by both CLI and module. During development, the CLI connects to remote hardware and calls your constructor directly. In production, viam-server loads your module and calls the same constructor. Same code, different context.

**Your inspection system now runs autonomously.** The machine sees, thinks, and acts on its own—the complete control loop, running 24/7.

---

**[Continue to Part 5: Scale →](./part5.md)**
