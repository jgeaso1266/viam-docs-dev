# Viam Essentials — Technical Validation Summary

This document records the validation of all code, configs, and narrative
claims across the 8-episode video series against authoritative source code.

## Validation methodology

Adapted from `~/viam/code-map/playbooks.md`:
- API method names and signatures verified against proto definitions
  (`~/viam/api/proto/viam/`) and SDK source code
- Config field names, types, and defaults verified against
  `~/viam/code-map/config-xref.md` and RDK source
- Behavioral claims verified against `~/viam/code-map/flows.md` and
  RDK implementation
- UI references verified against `~/viam/app/ui/src/` route structure
  (per Playbook 5)
- CLI commands verified against `~/viam/code-map/cli-xref.md`
- TypeScript SDK verified against docs.viam.com and npm package

## Source versions

- RDK: `~/viam/rdk` (code-map built against commit `568a4eb2`)
- API protos: `~/viam/api` (commit `f2838ed1`)
- App: `~/viam/app` (commit `30d1d4aa`)
- Python SDK: installed in `~/viam/shannonutils/.venv/`
- TypeScript SDK: `@viamrobotics/sdk` (verified against docs)

---

## Python SDK — Verified Method Signatures

| Class | Method | Signature | Source |
|-------|--------|-----------|--------|
| `RobotClient` | `at_address` | `async at_address(cls, address: str, options: Options) -> Self` | `robot/client.py:175` |
| `RobotClient.Options` | `with_api_key` | `with_api_key(cls, api_key: str, api_key_id: str, **kwargs) -> Self` | `robot/client.py:142` |
| `Arm` | `from_robot` | `from_robot(cls, robot: "RobotClient", name: str) -> Self` | `component_base.py:33` |
| `Arm` | `get_end_position` | `async get_end_position(self, *, extra=None, timeout=None, **kwargs) -> Pose` | `arm.py:32` |
| `Arm` | `move_to_position` | `async move_to_position(self, pose: Pose, *, extra=None, timeout=None, **kwargs)` | `arm.py:60` |
| `Arm` | `get_joint_positions` | `async get_joint_positions(self, *, extra=None, timeout=None, **kwargs) -> JointPositions` | `arm.py:125` |
| `Arm` | `move_to_joint_positions` | `async move_to_joint_positions(self, positions: JointPositions, *, extra=None, timeout=None, **kwargs)` | `arm.py:92` |
| `Arm` | `stop` | `async stop(self, *, extra=None, timeout=None, **kwargs)` | `arm.py:152` |
| `Camera` | `from_robot` | `from_robot(cls, robot: "RobotClient", name: str) -> Self` | `component_base.py:33` |
| `Camera` | `get_image` | `async get_image(self, mime_type: str = "", *, extra=None, timeout=None, **kwargs) -> ViamImage` | `camera.py:40` |
| `Camera` | `get_images` | `async get_images(self, *, filter_source_names=None, extra=None, timeout=None, **kwargs) -> Tuple[Sequence[NamedImage], ResponseMetadata]` | `camera.py:66` |
| `VisionClient` | `from_robot` | `from_robot(cls, robot: "RobotClient", name: str) -> Self` | `service_base.py:28` |
| `VisionClient` | `get_detections_from_camera` | `async get_detections_from_camera(self, camera_name: str, *, extra=None, timeout=None, **kwargs) -> List[Detection]` | `client.py:87` |
| `VisionClient` | `get_classifications_from_camera` | `async get_classifications_from_camera(self, camera_name: str, count: int, *, extra=None, timeout=None, **kwargs) -> List[Classification]` | `client.py:125` |
| `VisionClient` | `get_detections` | `async get_detections(self, image: ViamImage, *, extra=None, timeout=None, **kwargs) -> List[Detection]` | `client.py:100` |
| `VisionClient` | `capture_all_from_camera` | `async capture_all_from_camera(self, camera_name: str, return_image=False, return_classifications=False, return_detections=False, return_object_point_clouds=False, *, extra=None, timeout=None, **kwargs) -> CaptureAllResult` | `client.py:46` |

## Python SDK — Verified Types

| Type | Properties/Fields | Source |
|------|-------------------|--------|
| `ViamImage` | `.data: bytes`, `.mime_type: CameraMimeType`, `.width: Optional[int]`, `.height: Optional[int]` | `media/video.py:120-154` |
| `NamedImage` | Extends `ViamImage` + `.name: str` | `media/video.py:178-185` |
| `Detection` (proto) | `.x_min`, `.y_min`, `.x_max`, `.y_max` (int), `.confidence` (float), `.class_name` (str) | `vision_pb2.pyi:108-122` |
| `Classification` (proto) | `.class_name` (str), `.confidence` (float) | proto `Classification` message |
| `JointPositions` (proto) | `.values` (repeated double) | `arm_pb2.pyi`, import: `viam.proto.component.arm` |
| `Pose` | `.x`, `.y`, `.z`, `.o_x`, `.o_y`, `.o_z`, `.theta` | common proto |

## Go SDK — Verified Interfaces

| Interface | Methods (key ones) | Import |
|-----------|-------------------|--------|
| `arm.Arm` | `EndPosition`, `MoveToPosition`, `MoveToJointPositions`, `JointPositions`, `Stop` | `go.viam.com/rdk/components/arm` |
| `camera.Camera` | `Image`, `Images`, `NextPointCloud`, `Properties` | `go.viam.com/rdk/components/camera` |
| `vision.Service` | `DetectionsFromCamera`, `Detections`, `ClassificationsFromCamera`, `Classifications`, `CaptureAllFromCamera` | `go.viam.com/rdk/services/vision` |
| Detection | `BoundingBox() *image.Rectangle`, `Score() float64`, `Label() string` | `go.viam.com/rdk/vision/objectdetection` |
| Classification | `Score() float64`, `Label() string` | `go.viam.com/rdk/vision/classification` |
| Robot client | `client.New(ctx, address, logger, ...opts)` | `go.viam.com/rdk/robot/client` |

**NOTE:** Go method names differ from proto:
- `EndPosition` not `GetEndPosition`
- `JointPositions` not `GetJointPositions`
- `DetectionsFromCamera` not `GetDetectionsFromCamera`
- `ClassificationsFromCamera` not `GetClassificationsFromCamera`
- `Image` not `GetImage`

## TypeScript SDK — Verified Patterns

```typescript
// Connection
import * as VIAM from "@viamrobotics/sdk";
const machine = await VIAM.createRobotClient({
  host: "...",
  credentials: { type: "api-key", payload: "...", authEntity: "..." },
  signalingAddress: "https://app.viam.com:443",
});

// Camera stream
const stream = new StreamClient(machine);
const mediaStream = await stream.getStream("camera-name");

// Component client
const camera = new CameraClient(machine, "camera-name");

// Cleanup
machine.disconnect();
```

Source: docs.viam.com/operate/control/web-app/

---

## Config Fields — Verified

### Model triplets
| Resource | Triplet | Confirmed from |
|----------|---------|----------------|
| xArm 6 arm | `viam:ufactory:xArm6` | `tutorials/projects/claw-game.md:237` |
| RealSense camera | `viam:camera:realsense` | `reference/module-configuration.md:229` |
| TFLite ML model | `tflite_cpu` (short form) | `vision/configure.md:155` |
| ML vision service | `rdk:vision:mlmodel` | `config-xref.md:331-333` |
| Data manager | `rdk:builtin:builtin` | docs, multiple references |
| Filtered camera | `viam:filtered-camera` (module) | `alert-on-detections.md` |

### ML Vision config
| Field | Type | Required | Source |
|-------|------|----------|--------|
| `mlmodel_name` | string | yes | `config-xref.md:337` |
| `default_minimum_confidence` | float64 | no | `config-xref.md:344` |
| `label_confidences` | map | no | `config-xref.md:345` |

### Data capture config (per-component)
| Field | Type | Source |
|-------|------|--------|
| `method` | string | `flows.md:17` |
| `capture_frequency_hz` | float | `flows.md:18` |
| `capture_queue_size` | int (default 250) | `flows.md:19` |
| `additional_params` | map | `flows.md:20` |

### Data manager service config
| Field | Default | Source |
|-------|---------|--------|
| `sync_interval_mins` | 0.1 (6 sec) | `flows.md:28` |
| `capture_disabled` | false | `config-xref.md:270` |
| `sync_disabled` | false | `config-xref.md:279` |

---

## CLI Commands — Verified

| Command | Required flags | Source |
|---------|---------------|--------|
| `viam module upload` | `--version`, `--platform` | `cli-xref.md:217` |
| `viam module create` | `--name` | `cli-xref.md:213` |
| `viam module generate` | (all optional) | `cli-xref.md:214` |

---

## Behavioral Claims — Verified

| Claim | Episode | Verified against |
|-------|---------|-----------------|
| viam-server pulls modules from Registry on config change | 1, 6 | Flow 3 (Module Lifecycle) |
| All arms/cameras share the same API interface | 1 | Proto definitions + RDK interfaces |
| NAT traversal without VPN | 2 | SDK uses WebRTC via `viam.rpc.dial` |
| Data capture writes locally, syncs when connected | 3 | Flow 1 (Data Capture & Sync) |
| ML model service runs inference locally | 4 | `rdk/services/vision/mlvision/` |
| SDK connects remotely, same API | 5 | `robot/client.py` uses gRPC/WebRTC |
| Module manager starts on boot, restarts on failure | 6 | Flow 3 (Module Lifecycle) |
| Fragment config merges into machine config | 7 | `flows.md`, config system |
| Fragment updates propagate to all machines | 7 | Config polling (~15 sec interval) |
| `viam module upload` pushes to Registry | 6 | `cli-xref.md:217` |

---

## UI Route Verification

| Reference | Route | Confirmed |
|-----------|-------|-----------|
| CONFIGURE tab | `/machine/{id}/configure` | Yes |
| CONTROL tab | `/machine/{id}/control` | Yes |
| LOGS tab | `/machine/{id}/logs` | Yes |
| DATA tab | `/data` | Yes |
| FLEET view | `/fleet` | Yes |
| Billing | `/billing` | Yes |
| Training | `/training` | Yes |
| Registry | `/registry` | Yes |

---

## Issues Found and Resolved

1. **xArm model triplet**: Initial config used `viam:xarm:xArm6` — corrected
   to `viam:ufactory:xArm6` (confirmed from claw-game tutorial).

2. **NamedImage attribute**: Initial test script used `img.source_name` —
   corrected to `img.name` (confirmed from SDK `video.py:178-185`).

3. **TypeScript SDK credentials**: Initial code used `credential: { type,
   payload }` with separate `authEntity` — corrected to `credentials: {
   type, payload, authEntity }` (confirmed from docs).

4. **Module code**: Simplified to use `EasyResource` mixin which provides
   `new()` and default `validate_config`, avoiding boilerplate.

## Open Items for Pre-Production

1. **xArm attribute verification**: The `speed_degs_per_sec` and
   `acceleration_degs_per_sec2` attributes in the xArm config should be
   verified against the actual xArm module's config schema. These are
   plausible but not confirmed from an authoritative source.

2. **RealSense attributes**: The `sensors`, `width_px`, `height_px`, `fps`
   attributes should be verified against the RealSense module README.

3. **TypeScript `RobotClient` type**: The code uses `VIAM.RobotClient` as
   a type annotation — verify this is the correct exported type name.

4. **Flutter SDK**: The mobile app in Ep 8 uses the Flutter SDK, which
   was not verified in this pass. Need to check the Flutter SDK API
   before building the demo app.

5. **White-label OAuth setup**: The exact configuration steps for custom
   branding on the OAuth login page need to be researched and tested.
