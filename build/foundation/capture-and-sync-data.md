# Capture and Sync Data

**Time:** ~15 minutes
**Prerequisites:** [Connect to Cloud](connect-to-cloud.md) (machine online) | [Add a Camera](add-a-camera.md) (at least one component configured)
**Works with:** Simulation ✓ | Real Hardware ✓

## What You'll Learn

- How to enable automatic data capture on any component
- How to configure capture methods and frequency
- How cloud sync works and where your data goes
- How to view and filter captured data in the Viam app
- How to set up machine health alerts for offline/online events
- How to query captured data programmatically with Python or Go

## What Problem This Solves

Your machine generates useful data -- camera images, sensor readings, detection
results -- but you need that data collected reliably and stored where you can
access it. Manual data collection is fragile and doesn't scale. Viam's data
management service runs in the background on your machine, capturing component
outputs at the frequency you specify and syncing them to the cloud automatically.
No code required. Once data is flowing, you can view it, filter it, query it,
and use it to train ML models.

## Concepts

### Data capture

Data capture is a built-in service that records the output of any component or
service on your machine. You configure it entirely through the Viam app --
select which components to capture from, which API methods to record, and how
often. `viam-server` handles the rest.

Captured data is written to the local filesystem first (in `~/.viam/capture` by
default), then synced to Viam's cloud storage. After successful sync, local
files are cleaned up automatically. This means your machine continues capturing
even if it temporarily loses network connectivity -- data syncs when the
connection is restored.

### What you can capture

Data capture works with any component or service that has capturable methods:

| Component/Service | Common methods | Data type |
|-------------------|---------------|-----------|
| Camera | `GetImages` | Images (JPEG, PNG, depth maps) |
| Movement sensor | `AngularVelocity`, `LinearAcceleration`, `Position` | Tabular (numbers) |
| Sensor | `GetReadings` | Tabular (numbers, strings) |
| Motor | `Position`, `IsPowered` | Tabular |
| Vision service | `GetClassifications`, `GetDetections` | Tabular |

You can capture from multiple components simultaneously, each with its own
method and frequency.

### Cloud sync

Cloud sync runs alongside data capture. It encrypts captured data and transmits
it to Viam's cloud via gRPC. You can configure the sync interval independently
from capture frequency. Sync and capture can also be enabled or disabled
independently -- you can pause sync while continuing to capture locally, or
stop capture while syncing any remaining backlog.

## Components Needed

- A machine running `viam-server` with at least one component configured (a
  camera from [Add a Camera](add-a-camera.md) works well, but any sensor or
  component will do)

## Steps

### 1. Open your machine in the Viam app

Go to [app.viam.com](https://app.viam.com) and navigate to your machine.
Confirm it shows as **Live** in the upper left.

### 2. Enable data capture on a component

1. Find your component (e.g., `my-camera`) in the machine configuration.
2. Scroll to the **Data capture** section in the component's configuration
   panel.
3. Click **+ Add method**.
4. If this is your first time configuring data capture, Viam will prompt you to
   enable the **data management service**. Click to enable it. This adds the
   service to your machine configuration and enables both capture and cloud
   sync.
5. Select the method to capture:
   - For a camera, select **GetImages**. This captures a frame from the camera
     each time it fires.
   - For a sensor, select **GetReadings**. This records the sensor's current
     values.
6. Set the **capture frequency**. This is specified in hertz (captures per
   second):
   - `0.5` = one capture every 2 seconds
   - `0.2` = one capture every 5 seconds
   - `1` = one capture per second
   - Start low. For cameras, `0.5` Hz is a reasonable starting point. You can
     always increase it later.
7. Click **Save** in the upper right.

After saving, `viam-server` begins capturing immediately. You do not need to
restart anything.

> **Tip:** You can add multiple capture methods to a single component (e.g.,
> capture both `GetImages` and `NextPointCloud` from the same camera), each
> with its own frequency.

### 3. Capture from additional components (optional)

Repeat step 2 for any other components you want to capture from. Each
component's data capture is independent -- you can have a camera capturing
images every 2 seconds and a sensor capturing readings every 10 seconds at the
same time.

### 4. Verify data is being captured

Wait 30 seconds to a minute for data to accumulate and sync, then:

1. In the Viam app, click the **DATA** tab in the top navigation.
2. You should see captured data appearing. For camera captures, you will see
   image thumbnails. For sensor data, you will see tabular entries.
3. Use the filters on the left to narrow by:
   - **Machine** -- select your specific machine
   - **Component** -- select the component you configured
   - **Time range** -- pick a recent window
   - **Data type** -- Images or Tabular

If you see data flowing in, capture and sync are working correctly.

### 5. Configure machine health alerts

Viam can notify you when your machine goes offline or comes back online.
This is useful for catching connectivity problems, power failures, or crashes.

1. In the Viam app, navigate to your machine's page.
2. Go to the **CONFIGURE** tab.
3. Click the **+** button and select **Trigger**.
4. Select the trigger type **Machine online/offline**.
5. Choose the event you want to be notified about:
   - **Offline** -- the machine disconnects from the cloud
   - **Online** -- the machine reconnects
   - Or configure both.
6. Under **Notifications**, add your email address.
7. Click **Save**.

No code is required. Viam monitors your machine's connection status and sends
email alerts based on the events you configured.

### 6. Explore the Data tab

With data flowing, familiarize yourself with the Data tab's query capabilities:

1. **Filtering:** Use the sidebar filters to narrow data by machine, component,
   location, time range, or tags. This is useful when you have multiple machines
   or components capturing data.
2. **SQL queries:** Click **Query** in the Data tab to open the query editor.
   Write SQL queries to analyze your tabular data:
   ```sql
   SELECT * FROM readings
   WHERE component_name = 'my-sensor'
   ORDER BY time_received DESC
   LIMIT 10
   ```
3. **MQL queries:** Switch to MQL mode for MongoDB-style queries:
   ```json
   [
     {"$match": {"component_name": "my-sensor"}},
     {"$sort": {"time_received": -1}},
     {"$limit": 10}
   ]
   ```

## Try It

### Verify capture is running

1. Check the **DATA** tab and confirm new entries are appearing at roughly the
   frequency you configured.
2. For camera data, click an image thumbnail to view the full captured image.
3. For sensor data, inspect the tabular values and confirm they match what you
   expect from your sensor.

### Query captured data programmatically

Beyond the Viam app UI, you can query your captured data from your own code
using the Viam app client. This is useful for building dashboards, running
analysis, or integrating captured data into your applications.

#### Python

Install the SDK if you haven't already:

```bash
pip install viam-sdk
```

Save this as `query_data.py`:

```python
import asyncio
from viam.rpc.dial import DialOptions, Credentials
from viam.app.viam_client import ViamClient


API_KEY = "YOUR-API-KEY"
API_KEY_ID = "YOUR-API-KEY-ID"
ORG_ID = "YOUR-ORGANIZATION-ID"


async def connect() -> ViamClient:
    dial_options = DialOptions(
        credentials=Credentials(
            type="api-key",
            payload=API_KEY,
        ),
        auth_entity=API_KEY_ID,
    )
    return await ViamClient.create_from_dial_options(dial_options)


async def main():
    viam_client = await connect()
    data_client = viam_client.data_client

    # Query with SQL -- get recent readings from a specific component
    sql_results = await data_client.tabular_data_by_sql(
        organization_id=ORG_ID,
        sql_query=(
            "SELECT * FROM readings "
            "WHERE component_name = 'my-camera' "
            "ORDER BY time_received DESC "
            "LIMIT 5"
        ),
    )
    print("SQL results:")
    for row in sql_results:
        print(f"  {row}")

    # Query with MQL -- count entries by component
    mql_results = await data_client.tabular_data_by_mql(
        organization_id=ORG_ID,
        mql_binary=[
            {"$group": {"_id": "$component_name", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
        ],
    )
    print("\nCapture counts by component:")
    for entry in mql_results:
        print(f"  {entry}")

    viam_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

Replace `YOUR-API-KEY`, `YOUR-API-KEY-ID`, and `YOUR-ORGANIZATION-ID` with your
values. Find your organization ID in the Viam app under **Settings** in the left
navigation.

Run it:

```bash
python query_data.py
```

You should see your captured data printed to the console.

#### Go

Initialize a Go module and install the SDK:

```bash
mkdir query-data && cd query-data
go mod init query-data
go get go.viam.com/rdk
```

Save this as `main.go`:

```go
package main

import (
	"context"
	"fmt"

	"go.viam.com/rdk/app"
	"go.viam.com/rdk/logging"
)

func main() {
	apiKey := "YOUR-API-KEY"
	apiKeyID := "YOUR-API-KEY-ID"
	orgID := "YOUR-ORGANIZATION-ID"

	ctx := context.Background()
	logger := logging.NewDebugLogger("query-data")

	viamClient, err := app.CreateViamClientWithAPIKey(
		ctx, app.Options{}, apiKey, apiKeyID, logger)
	if err != nil {
		logger.Fatal(err)
	}
	defer viamClient.Close()

	dataClient := viamClient.DataClient()

	// Query with SQL -- get recent readings
	sqlResults, err := dataClient.TabularDataBySQL(ctx, orgID,
		"SELECT * FROM readings WHERE component_name = 'my-camera' ORDER BY time_received DESC LIMIT 5")
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Println("SQL results:")
	for _, row := range sqlResults {
		fmt.Printf("  %v\n", row)
	}

	// Query with MQL -- count entries by component
	mqlStages := []map[string]interface{}{
		{"$group": map[string]interface{}{
			"_id":   "$component_name",
			"count": map[string]interface{}{"$sum": 1},
		}},
		{"$sort": map[string]interface{}{"count": -1}},
	}

	mqlResults, err := dataClient.TabularDataByMQL(ctx, orgID, mqlStages, nil)
	if err != nil {
		logger.Fatal(err)
	}
	fmt.Println("\nCapture counts by component:")
	for _, entry := range mqlResults {
		fmt.Printf("  %v\n", entry)
	}
}
```

Replace the placeholder values with your API key, API key ID, and organization
ID. Then run:

```bash
go run main.go
```

## Troubleshooting

### No data appears in the Data tab

- **Wait a minute.** Data must be captured locally and then synced to the cloud.
  The first entries can take 30-60 seconds to appear.
- **Is the data management service enabled?** Go to your machine's
  **CONFIGURE** tab and check that the data management service exists and both
  **Capturing** and **Syncing** are toggled on.
- **Is capture configured on the component?** Verify that the component's Data
  capture section shows at least one method with a non-zero frequency.
- **Is the machine online?** Data syncs only when the machine has a network
  connection. Check the machine's status indicator in the Viam app.

### Data appears but images are missing or blank

- Verify the camera works in the test panel first. If the test panel shows
  nothing, the issue is with the camera configuration, not data capture.
- Check that the capture method is **GetImages**, not another method.

### Data capture frequency seems wrong

- The frequency is in hertz (captures per second), not seconds between captures.
  `0.5` Hz means once every 2 seconds, not twice per second.
- High-frequency capture (above 1 Hz for cameras) generates large amounts of
  data. Start with `0.5` Hz or lower unless you need high-frequency capture.

### Local disk filling up

- By default, captured data is stored in `~/.viam/capture` before syncing. If
  sync is disabled or the machine is offline for an extended period, this
  directory can grow large.
- Re-enable sync or manually clear the capture directory if needed.
- Check that the **Syncing** toggle is on in the data management service
  configuration.

### Machine health alert not received

- Check that you entered your email address correctly in the trigger
  configuration.
- Look in your spam/junk folder.
- Alerts fire when the machine's connection status changes. If the machine was
  already offline when you configured the trigger, the alert won't fire
  retroactively -- it fires on the next status change.

### Programmatic query returns empty results

- Verify your organization ID is correct. Find it in the Viam app under
  **Settings**.
- Make sure you're querying the right component name. Component names are
  case-sensitive and must match exactly.
- Confirm that data has actually synced to the cloud (visible in the Data tab)
  before querying.

## What's Next

- [Query Data](../data/query-data.md) -- write more advanced queries, set up
  data pipelines, and export data.
- [Add Computer Vision](../vision-detection/add-computer-vision.md) -- run ML
  models on your camera feed and capture detection results.
- [Create a Dataset](../train/create-a-dataset.md) -- organize captured images
  into training datasets for machine learning.
