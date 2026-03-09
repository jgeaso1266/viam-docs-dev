# Viam Essentials: Manage Deployments

**Duration target:** 90 seconds

---

## Pre-shoot checklist

- [ ] Machine running with arm + camera + detector from previous episodes
- [ ] Module code (`src/main.py`, `meta.json`, `run.sh`, `requirements.txt`)
      ready and tested locally
- [ ] Viam CLI installed and authenticated on presenter's laptop
- [ ] First version of the module already uploaded to Registry (for showing
      the update flow, upload v0.1.0 beforehand)
- [ ] `test_module.py` ready on laptop
- [ ] Wrench on workbench

---

## Script

### COLD OPEN — face to camera [0:00–0:10]

> Your detection script works. But it only runs when you run it. You need
> it to start on boot, restart on failure, and update without SSH. That's
> what modules are for.

SHOT: Presenter at laptop.

---

### DEMO — screen [0:10–1:15]

**Package as a module [0:10–0:30]**

> I take the same detection logic from the previous episode and wrap it
> as a Viam module. The key changes: it implements the Generic service API,
> declares its dependencies, and handles reconfiguration.

SHOT: Screen — VS Code showing `src/main.py`. Briefly highlight:
1. `class DetectAndMove(Generic, EasyResource)` — the service type
2. `validate_config` returning dependency names
3. `reconfigure` getting arm and detector from dependencies

> I have a `meta.json` that describes the module — its name, model, and
> entrypoint.

SHOT: Screen — show `meta.json` briefly.

**Upload to the Registry [0:30–0:45]**

> I upload it with one command.

SHOT: Terminal —
```
$ viam module upload --version 0.1.0 --platform linux/arm64
```

Output showing successful upload.

> It's in the Registry now, versioned and ready to deploy.

SHOT: Screen — Viam app Registry page showing the module with version
0.1.0.

**Deploy to the machine [0:45–0:55]**

> On the machine's CONFIGURE tab, I add the module from the Registry and
> configure it with the names of the arm, camera, and detector.

SHOT: Screen — CONFIGURE tab. Add service. Search for the module. Add
it. Set attributes: `arm_name`, `camera_name`, `detector_name`. Save.

> viam-server downloads the module, starts it, and it's running.

SHOT: Screen — LOGS tab showing the module starting, the "Configured:"
log line appearing.

**Push an update [0:55–1:15]**

> Now I make a change — bump the move scale from 10 to 20 — and upload
> a new version.

SHOT: Screen — change `move_scale` default from `10.0` to `20.0` in the
code. Terminal:
```
$ viam module upload --version 0.2.0 --platform linux/arm64
```

> The machine pulls the update automatically.

SHOT: Screen — LOGS tab. Show the module restarting with the new version.
Log line shows the new configuration.

---

### PAYOFF — face to camera [1:15–1:30]

> Version control. OTA updates. Managed lifecycle. Your code runs on the
> robot like a production service — because it is one.

SHOT: Presenter, confident.

---

## Validation notes

### Code accuracy (src/main.py)
- `Generic` base class — confirmed from SDK
  (`viam/services/generic/__init__.py`)
- `EasyResource` mixin — confirmed from SDK
  (`viam/resource/easy_resource.py:77`). Provides `new()` (calls
  `reconfigure`), default `validate_config`, and auto-registration.
- `MODEL = "YOUR-ORG-ID:wrench-finder:detect-and-move"` — string format
  confirmed: `_parse_model()` parses `"namespace:family:name"` strings
  (`easy_resource.py:105`)
- `validate_config` return type `Tuple[Sequence[str], Sequence[str]]` —
  confirmed (`easy_resource.py:125`)
- `Arm.get_resource_name(name)` — returns `ResourceName` for dependency
  lookup. Inherited from `ResourceBase`.
- `VisionClient.get_resource_name(name)` — same pattern.
- `Module.run_from_registry()` — confirmed entrypoint
  (`module/module.py:125-132`)
- `ComponentConfig` import from `viam.proto.app.robot` — confirmed
- `getLogger` from `viam.logging` — confirmed

### CLI accuracy
- `viam module upload --version 0.1.0 --platform linux/arm64` — verified
  against CLI xref. The `upload` subcommand takes `--version` and
  `--platform` flags.
- Note: actual upload may also require `--module` flag or be run from
  the directory containing `meta.json`. Confirm exact flags before shoot.

### Config accuracy (machine-config-addition.json)
- Service config with `api: "rdk:service:generic"` — correct for a
  Generic service
- `depends_on` list — correct; ensures arm and detector are ready before
  the module starts
- Attributes match what `validate_config` and `reconfigure` expect

### Behavioral claims
- "starts on boot" — confirmed from Flow 3 (Module Lifecycle): viam-server
  starts all configured modules on startup
- "restarts on failure" — confirmed: module manager monitors module
  processes and restarts them
- "update without SSH" — confirmed: OTA updates via Registry; machine
  pulls new version based on update policy
- "viam-server downloads the module, starts it" — confirmed from Flow 3:
  module download, extraction, and process start are managed by
  viam-server's module manager
