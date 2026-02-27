# Connect to Cloud

**Time:** ~15 minutes
**Prerequisites:** None — this is the starting point.
**Works with:** Simulation ✓ | Real Hardware ✓

## What You'll Learn

- What `viam-server` is and what it does on your device
- How to create a machine in the Viam app
- How to install `viam-server` on real hardware (or set up simulation)
- How to verify your machine is online
- How to connect to your machine programmatically from Python or Go

## What Problem This Solves

Before you can configure hardware, capture data, or run any logic on a device,
the device needs to connect to the Viam platform. `viam-server` is the agent
that makes this happen. This block gets your first machine connected and
reachable — both from the Viam app and from your own code.

## Components Needed

- **Real hardware path:** A single-board computer (Raspberry Pi 4/5, Jetson,
  etc.) or any Linux machine. Must have network access.
- **Simulation path:** A laptop or desktop running macOS or Linux. No physical
  hardware required.

## Concepts

### What is viam-server?

`viam-server` is a binary that runs on every Viam-managed device. It:

- **Connects to the Viam cloud** — registers the device, syncs configuration,
  reports status.
- **Manages hardware** — talks to cameras, motors, sensors, and other
  components through a unified interface.
- **Exposes APIs** — provides gRPC and WebRTC endpoints so your code (running
  anywhere) can control the device.
- **Runs modules** — loads and manages additional capabilities (ML models,
  custom drivers, business logic).

You don't write `viam-server` or modify it. You configure it through the Viam
app, and it applies that configuration on the device.

## Steps

### 1. Create a machine in the Viam app

1. Go to [app.viam.com](https://app.viam.com) and log in (or create an
   account).
2. Create or select an organization, then create or select a location.
3. Click **New machine**.
4. Give your machine a name (e.g., `my-first-machine`). Click **Save**.

The app creates a machine entry and shows a setup page. Don't close this page —
you'll need the install command in the next step.

### 2. Install viam-server

#### Real hardware

On the machine's setup page, the Viam app displays a `curl` command tailored to
your machine. It looks like this:

```bash
curl -fsSL https://storage.googleapis.com/packages.viam.com/apps/viam-server/install.sh | sudo bash -s -- --aarch64 --config <YOUR_CONFIG>
```

SSH into your device and run the command. It installs `viam-server`, writes the
machine credentials to `/etc/viam.json`, and starts the service.

> **Tip:** The exact command varies by architecture. Always copy the command from
> the Viam app's setup page rather than manually editing a command.

#### Simulation

If you don't have physical hardware, you can run `viam-server` locally:

1. On the machine's setup page, select your OS and architecture.
2. Copy and run the install command on your laptop/desktop.

`viam-server` works the same way in simulation as on real hardware. The only
difference is that some components (e.g., GPIO pins) won't be available without
physical hardware. Simulated cameras and other virtual components work normally.

### 3. Verify your machine is online

Go back to the Viam app and navigate to your machine's page.

- **Green dot** next to the machine name means it's online and connected.
- **Red or gray dot** means the machine is offline.

If the indicator shows online, `viam-server` is running and connected to the
cloud. You're ready to configure components and connect programmatically.

### 4. Connect programmatically

Every subsequent block builds on programmatic access to your machine. Set this
up now.

#### Get your API credentials

1. In the Viam app, go to your machine's page.
2. Click the **CONNECT** tab.
3. Select the **API keys** section.
4. Copy the **API key** and **API key ID**. You'll also need your **machine
   address** (shown on the same page).

> **Keep credentials secure.** Don't commit API keys to version control. Use
> environment variables or a `.env` file.

#### Python

Install the Viam Python SDK:

```bash
pip install viam-sdk
```

Create a file called `connect.py`:

```python
import asyncio
from viam.robot.client import RobotClient


async def connect():
    opts = RobotClient.Options.with_api_key(
        api_key="YOUR_API_KEY",
        api_key_id="YOUR_API_KEY_ID",
    )
    robot = await RobotClient.at_address(
        "YOUR_MACHINE_ADDRESS",
        opts,
    )

    print("Connected!")
    print("Resources:")
    print(robot.resource_names)

    await robot.close()


if __name__ == "__main__":
    asyncio.run(connect())
```

Replace `YOUR_API_KEY`, `YOUR_API_KEY_ID`, and `YOUR_MACHINE_ADDRESS` with the
values from the **CONNECT** tab. Then run:

```bash
python connect.py
```

You should see `Connected!` followed by a list of available resources (empty for
now, since you haven't configured any components yet).

#### Go

Initialize a Go module and install the Viam Go SDK:

```bash
mkdir viam-connect && cd viam-connect
go mod init viam-connect
go get go.viam.com/rdk/robot/client
```

Create a file called `main.go`:

```go
package main

import (
	"context"
	"fmt"

	"go.viam.com/rdk/logging"
	"go.viam.com/rdk/robot/client"
	"go.viam.com/rdk/utils"
)

func main() {
	logger := logging.NewLogger("client")

	robot, err := client.New(
		context.Background(),
		"YOUR_MACHINE_ADDRESS",
		logger,
		client.WithCredentials(
			utils.Credentials{
				Type:    utils.CredentialsTypeAPIKey,
				Payload: "YOUR_API_KEY",
			},
		),
		client.WithAPIKeyID("YOUR_API_KEY_ID"),
	)
	if err != nil {
		logger.Fatal(err)
	}
	defer robot.Close(context.Background())

	fmt.Println("Connected!")
	fmt.Println("Resources:")
	fmt.Println(robot.ResourceNames())
}
```

Replace `YOUR_API_KEY`, `YOUR_API_KEY_ID`, and `YOUR_MACHINE_ADDRESS` with the
values from the **CONNECT** tab. Then run:

```bash
go run main.go
```

You should see `Connected!` followed by a list of available resources.

## Try It

Run your connection script (Python or Go). Confirm that:

1. The script prints `Connected!` without errors.
2. The resource list appears (it will be empty or minimal at this stage).
3. In the Viam app, your machine's status indicator stays green while the script
   runs.

If all three checks pass, your machine is connected and ready for the next
block.

## Troubleshooting

### Machine shows offline in the Viam app

- **Is `viam-server` running?** On Linux, check with
  `sudo systemctl status viam-server`. If it's not running, start it with
  `sudo systemctl start viam-server`.
- **Does the device have network access?** Verify with `ping google.com`.
- **Is the config correct?** Inspect `/etc/viam.json` and confirm it contains
  valid credentials. If in doubt, re-run the install command from the Viam app.

### Connection script fails with "context deadline exceeded"

- Confirm your machine is online (green dot in the Viam app).
- Verify the machine address is correct — it should look like
  `my-first-machine-main.1234abcd.viam.cloud`.
- Check that your laptop/desktop has internet access.

### Connection script fails with "authentication failed"

- Double-check that you copied the API key, API key ID, and machine address
  correctly from the **CONNECT** tab.
- Make sure there are no trailing spaces or newlines in the credentials.
- Verify the API key hasn't been revoked — you can check this in the Viam app
  under your organization's settings.

### "Permission denied" during install

- The install script requires `sudo`. Run the `curl` command exactly as shown on
  the setup page.
- On some systems, your user may not be in the `sudo` group. Consult your
  device's documentation for how to grant sudo access.

### viam-server starts but immediately exits

- Check the logs: `sudo journalctl -u viam-server -n 50`.
- Common causes: invalid JSON in `/etc/viam.json`, port conflicts (another
  service on port 8080), or missing system libraries.

## What's Next

- [Add a Camera](add-a-camera.md) — Configure your first hardware component and
  see a live feed.
- [Capture and Sync Data](capture-and-sync-data.md) — Start recording data from
  your machine to the cloud.
