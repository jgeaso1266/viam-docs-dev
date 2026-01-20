# Part 4: Scale (~10 min)

[← Back to Overview](./index.md) | [← Part 3: Control Logic](./part3.md)

---

**Goal:** Add a second inspection station.

**Skills:** Configuration reuse with fragments, fleet basics.

## 4.1 Create a Fragment

You have one working inspection station. Now imagine you need 10 more—or 100. Manually copying configuration to each machine would be tedious and error-prone.

Viam solves this with *fragments*: reusable configuration blocks that can be applied to any machine. Think of a fragment as a template. Define your camera, vision service, data capture, and triggers once, then apply that template to as many machines as you need.

**Export your machine configuration:**

1. Go to your `inspection-station-1` machine
2. Click the **Configure** tab, then click **JSON** (top right) to see the raw configuration
3. Copy the entire JSON configuration to your clipboard

[SCREENSHOT: JSON config view with copy button]

**Create the fragment:**

1. In the Viam app, click **Fragments** in the left sidebar
2. Click **+ Create fragment**
3. Name it `inspection-station`
4. Paste your configuration into the fragment editor
5. Click **Save**

[SCREENSHOT: Fragment editor with pasted configuration]

## 4.2 Parameterize Machine-Specific Values

Your fragment now contains everything—but some values are specific to each machine. The camera's `video_path` might be `/dev/video0` on one machine and `/dev/video1` on another. Hardcoding these values would break the fragment's reusability.

Viam fragments support *variables* for exactly this purpose.

**Find the camera configuration in your fragment:**

Look for the camera component in the JSON. It will look something like:

```json
{
  "name": "inspection-cam",
  "type": "camera",
  "model": "webcam",
  "attributes": {
    "video_path": "/dev/video0"
  }
}
```

**Replace the hardcoded value with a variable:**

Change `video_path` to use the `$variable` syntax:

```json
{
  "name": "inspection-cam",
  "type": "camera",
  "model": "webcam",
  "attributes": {
    "video_path": {
      "$variable": {
        "name": "camera_path"
      }
    }
  }
}
```

Click **Save** to update the fragment.

Now when you apply this fragment to a machine, you'll provide the actual `camera_path` value for that specific machine.

> **What to parameterize:** Device paths (`/dev/video0`, `/dev/ttyUSB0`), IP addresses, serial numbers—anything that varies between physical machines. Configuration like detection thresholds, capture frequency, and module versions should stay in the fragment so they're consistent across your fleet.

**Apply the fragment to your first machine:**

Now that the fragment exists, update `inspection-station-1` to use it instead of inline configuration:

1. Go to `inspection-station-1`'s **Configure** tab
2. Switch to **JSON** view
3. Delete all the component and service configurations (keep only the machine metadata)
4. Switch back to **Builder** view
5. Click **+** and select **Insert fragment**
6. Select `inspection-station` and click **Add**
7. Set the variable: `{"camera_path": "/dev/video0"}`
8. Click **Save**

The machine reloads with the same configuration, but now it's sourced from the fragment. Any future changes to the fragment will automatically apply to this machine.

## 4.3 Add a Second Machine

Let's spin up a second inspection station and apply the fragment.

**Launch a second simulation:**

Click the button below to launch a second work cell:

[BUTTON: Launch Second Station]

This opens another browser tab with an identical simulation environment—conveyor, camera, the works. But this machine doesn't have any Viam configuration yet.

[SCREENSHOT: Second simulation tab]

**Create the machine and install viam-server:**

Follow the same steps from [Part 1](./part1.md):

1. In the Viam app, click **+ Add machine**
2. Name it `inspection-station-2`
3. Copy the install command from the **Setup** tab
4. Paste and run it in the second simulation's terminal
5. Wait for the machine to come online

**Apply the fragment with variable values:**

1. On `inspection-station-2`, go to the **Configure** tab
2. Click **+** and select **Insert fragment**
3. Search for and select `inspection-station`
4. Click **Add**

The fragment appears in your configuration. Notice the **Variables** section—this is where you provide machine-specific values.

**Set the camera path for this machine:**

1. In the fragment's **Variables** section, add:

```json
{
  "camera_path": "/dev/video0"
}
```

2. Click **Save** in the top right

[SCREENSHOT: Fragment with variables configured]

Within seconds, the machine reloads its configuration. It now has the camera (with the correct device path), vision service, inspector module, data capture, and alerting—all from the fragment, customized for this specific machine.

**Verify it works:**

1. Go to the **Control** tab
2. Check the camera feed
3. Run a detection

Both stations are now running identical inspection logic.

[SCREENSHOT: Fleet view showing both machines online]

## 4.4 Fleet Management Capabilities

With fragments in place, you have the foundation for managing fleets at any scale. Here's what's possible:

**Push updates across your fleet:**
- **Configuration changes** — Edit the fragment, and all machines using it receive the update automatically within seconds
- **ML model updates** — Change which model the vision service uses; all machines switch to the new version
- **Module updates** — Deploy new versions of your inspection logic across the fleet
- **Capture settings** — Adjust data capture frequency, enable/disable components fleet-wide

**Monitor and maintain remotely:**
- **Fleet dashboard** — View all machines' status, last seen, and health from one screen
- **Aggregated data** — Query inspection results across all stations ("How many FAILs across all machines this week?")
- **Remote diagnostics** — View live camera feeds, check logs, and test components without physical access
- **Alerts** — Get notified when any machine goes offline or exhibits anomalies

**Handle machine-specific variations:**
- **Fragment variables** — Parameterize device paths, IP addresses, serial numbers—anything that differs between physical machines
- **Per-machine overrides** — Add machine-specific configuration on top of fragments when needed
- **Hardware flexibility** — Same inspection logic works whether a station uses USB cameras, CSI cameras, or IP cameras

This same pattern scales from 2 machines to 2,000. The fragment is your single source of truth; Viam handles the distribution.

**Checkpoint:** Two stations running identical inspection logic from a shared fragment. Update the fragment once, and all machines receive the change automatically.

---

**[Continue to Part 5: Productize →](./part5.md)**
