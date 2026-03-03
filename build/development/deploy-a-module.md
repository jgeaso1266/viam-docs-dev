# Deploy a Module

**Time:** ~20 minutes
**Prerequisites:** [Write a Module](write-a-module.md) (a working module to deploy)
**Works with:** Simulation ✓ | Real Hardware ✓

## What You'll Learn

- What the Viam module registry is and how it distributes modules
- How to configure `meta.json` for your module
- How to set up automated cloud builds with GitHub Actions
- How to upload a module manually from the command line
- How to configure a deployed module on a machine
- How to manage versions and control updates

## What Problem This Solves

A module that only runs locally on your development machine is useful for testing
but does not scale. If you have ten machines that need your custom sensor driver,
you do not want to SSH into each one and copy files. You need a way to package,
distribute, and update your module across your fleet.

The Viam module registry solves this. You upload your module once, and any
machine in your organization (or the public, if you choose) can install it
through the Viam app. When you release a new version, machines update
automatically. The registry handles packaging, platform-specific builds,
versioning, and delivery.

This block takes you from a working local module to a deployed, versioned module
in the registry that any machine can use.

## Concepts

### The module registry

The Viam module registry is a package manager for modules. It stores versioned
module packages and serves them to machines on demand. When you configure a
module on a machine, `viam-server` downloads the correct version for the
machine's platform (OS and architecture) from the registry.

Modules in the registry can be:

- **Private** -- visible only to your organization. Use this for internal tools,
  proprietary hardware drivers, and modules under development.
- **Public** -- visible to all Viam users. Use this for open-source modules and
  community contributions.

### meta.json

Every module has a `meta.json` file that describes it to the registry. This file
is created by `viam module generate` and updated as your module evolves. It
contains:

- **module_id** -- a unique identifier in the format `namespace:module-name`.
- **visibility** -- `private` or `public`.
- **description** -- a human-readable summary shown in the registry.
- **models** -- the list of resource models this module provides, each with an
  API and model triplet.
- **entrypoint** -- the command that starts the module.
- **build** -- configuration for cloud builds (setup script, build script,
  output path, target architectures).

### Cloud build

Cloud build uses GitHub Actions to compile your module for multiple platforms
automatically. When you push a version tag (e.g., `v0.1.0`) to your GitHub
repository, a workflow builds your module for each target architecture, packages
it, and uploads it to the Viam registry.

This is the recommended approach for modules that need to run on different
hardware (e.g., both amd64 desktops and arm64 Raspberry Pis). You write code
once, and the build system produces platform-specific packages.

### Versioning

The registry uses semantic versioning (semver). Each upload is tagged with a
version like `0.1.0`, `0.2.0`, or `1.0.0`. Machines can be configured to:

- **Track the latest version** -- automatically update when a new version is
  uploaded. This is the default and recommended for most deployments.
- **Pin to a specific version** -- stay on a fixed version regardless of new
  releases. Use this when you need stability and want to control when updates
  happen.

## Components Needed

- A working module (from [Write a Module](write-a-module.md))
- The Viam CLI installed (`brew tap viamrobotics/brews && brew install viam`)
- A Viam API key with organization-level access
- A GitHub repository for the module (required for cloud build, optional for
  manual upload)

## Steps

### 1. Prepare meta.json

Open the `meta.json` file in your module directory. If you used
`viam module generate`, this file already exists with sensible defaults. Review
and update each field:

```json
{
  "module_id": "my-org:my-sensor-module",
  "visibility": "private",
  "url": "https://github.com/my-org/my-sensor-module",
  "description": "A custom sensor module that reads temperature and humidity from an HTTP endpoint.",
  "models": [
    {
      "api": "rdk:component:sensor",
      "model": "my-org:my-sensor-module:my-sensor"
    }
  ],
  "entrypoint": "run.sh",
  "build": {
    "setup": "./setup.sh",
    "build": "./build.sh",
    "path": "dist/archive.tar.gz",
    "arch": ["linux/amd64", "linux/arm64"]
  }
}
```

Here is what each field does:

| Field | Purpose | Example |
|-------|---------|---------|
| `module_id` | Unique ID in the registry. Format: `namespace:name`. | `my-org:my-sensor-module` |
| `visibility` | Who can see and install the module. | `private` or `public` |
| `url` | Link to the source code repository. | `https://github.com/my-org/my-sensor-module` |
| `description` | Shown in the registry UI and search results. | A sentence describing what the module does. |
| `models` | List of resource models the module provides. | Each has an `api` and `model` triplet. |
| `entrypoint` | The command that starts the module. | `run.sh` for Python, the binary name for Go. |
| `build.setup` | Script that installs build dependencies. | `./setup.sh` |
| `build.build` | Script that compiles and packages the module. | `./build.sh` |
| `build.path` | Path to the packaged output archive. | `dist/archive.tar.gz` |
| `build.arch` | Target platforms to build for. | `["linux/amd64", "linux/arm64"]` |

The `api` field in each model entry must match the Viam resource API your module
implements. Common values:

- `rdk:component:sensor` for sensors
- `rdk:component:camera` for cameras
- `rdk:component:motor` for motors
- `rdk:component:generic` for generic components
- `rdk:service:vision` for vision services

The `model` field is a triplet in the format `namespace:module-name:model-name`.
It must be unique within the registry.

### 2. Create build and setup scripts

The cloud build system runs your `setup.sh` and `build.sh` scripts to produce
the module package. Create these scripts in your module directory.

**Python module -- `setup.sh`:**

```bash
#!/bin/bash
set -e
pip install -r requirements.txt
```

**Python module -- `build.sh`:**

```bash
#!/bin/bash
set -e

# Create the output directory.
mkdir -p dist

# Package the module into a tarball.
tar -czf dist/archive.tar.gz \
    src/ \
    requirements.txt \
    meta.json \
    run.sh
```

**Python module -- `run.sh`** (the entrypoint):

```bash
#!/bin/bash
cd "$(dirname "$0")"
exec python3 -m src.main "$@"
```

**Go module -- `setup.sh`:**

```bash
#!/bin/bash
set -e
# Go modules are self-contained; no setup needed.
```

**Go module -- `build.sh`:**

```bash
#!/bin/bash
set -e

mkdir -p dist

# Build the binary.
GOOS=linux GOARCH=$TARGET_ARCH go build -o dist/module cmd/module/main.go

# Package it.
tar -czf dist/archive.tar.gz -C dist module
```

Make all scripts executable:

```bash
chmod +x setup.sh build.sh run.sh
```

### 3. Set up cloud build

Cloud build automates the build-and-upload process using GitHub Actions. Every
time you push a version tag, the workflow builds your module for all target
platforms and uploads it to the registry.

#### Create a GitHub repository

If your module is not already in a GitHub repository, create one:

```bash
cd my-sensor-module
git init
git add .
git commit -m "Initial module code"
git remote add origin https://github.com/my-org/my-sensor-module.git
git push -u origin main
```

#### Add Viam credentials as GitHub secrets

The build action needs credentials to upload to the Viam registry.

1. In the [Viam app](https://app.viam.com), go to your organization's settings.
2. Create an API key with organization-level access (or use an existing one).
3. In your GitHub repository, go to **Settings > Secrets and variables >
   Actions**.
4. Add two secrets:
   - `VIAM_KEY_ID` -- your API key ID
   - `VIAM_KEY_VALUE` -- your API key

#### Create the workflow file

Create `.github/workflows/deploy.yml` in your repository:

```yaml
on:
  push:
    tags:
      - 'v*'

jobs:
  build:
    uses: viamrobotics/build-action/.github/workflows/deploy.yml@v1
    with:
      ref: ${{ github.ref }}
    secrets:
      viam_key_id: ${{ secrets.VIAM_KEY_ID }}
      viam_key_value: ${{ secrets.VIAM_KEY_VALUE }}
```

This workflow triggers on any tag that starts with `v` (e.g., `v0.1.0`,
`v1.0.0`). It uses Viam's official `build-action` to run your `setup.sh` and
`build.sh` scripts, then uploads the resulting archive to the registry.

#### Trigger a build

Commit and push the workflow file, then create a version tag:

```bash
git add .github/workflows/deploy.yml
git commit -m "Add cloud build workflow"
git push origin main

git tag v0.1.0
git push origin v0.1.0
```

The GitHub Action runs automatically. Monitor its progress in the **Actions**
tab of your GitHub repository. When it completes, your module is available in the
Viam registry.

### 4. Upload manually (alternative)

If you do not want to use cloud build, you can build and upload your module from
the command line. This is useful for quick iterations or modules that only target
one platform.

#### Build the module locally

**Python:**

```bash
cd my-sensor-module
bash build.sh
```

**Go:**

```bash
cd my-sensor-module
go build -o dist/module cmd/module/main.go
tar -czf dist/archive.tar.gz -C dist module
```

#### Upload to the registry

```bash
viam module upload \
    --version=0.1.0 \
    --platform=linux/amd64 \
    dist/archive.tar.gz
```

To upload for multiple platforms, run the command once per platform:

```bash
viam module upload \
    --version=0.1.0 \
    --platform=linux/arm64 \
    dist/archive.tar.gz
```

Each upload adds a platform-specific package to the same version. Machines
download the package that matches their architecture.

### 5. Configure the module on a machine

Once your module is in the registry, any machine in your organization can use it.

1. In the [Viam app](https://app.viam.com), navigate to your machine's
   **CONFIGURE** tab.
2. Click **+** and select **Component** (or **Service**, depending on what your
   module provides).
3. Search for your module by name or browse the registry.
4. Click **Add module** to add the module to the machine.
5. Click **Add component** (or **Add service**) to create an instance of the
   model.
6. Name the component (e.g., `my-sensor`).
7. Configure the attributes your module expects:

```json
{
  "source_url": "https://api.example.com/sensor/data"
}
```

8. Click **Save**.

`viam-server` downloads the module from the registry, starts it, and makes the
component available. You can test it immediately from the **CONTROL** tab.

### 6. Manage versions

#### Release a new version

Update your code, commit the changes, and create a new tag:

```bash
git add .
git commit -m "Add humidity calibration offset"
git tag v0.2.0
git push origin main v0.2.0
```

If you are using cloud build, the workflow runs automatically and uploads the
new version. If you are uploading manually, build and upload with the new version
number:

```bash
viam module upload --version=0.2.0 --platform=linux/amd64 dist/archive.tar.gz
```

#### Automatic updates

By default, machines track the latest version of each module. When you upload
`v0.2.0`, all machines using your module update automatically the next time they
check for updates (typically within a few minutes).

This is the recommended behavior for most deployments. It ensures all machines
run the same version and receive bug fixes promptly.

#### Pin to a specific version

If you need a machine to stay on a specific version (e.g., a production machine
that should not update until you have tested the new version):

1. In the Viam app, go to the machine's **CONFIGURE** tab.
2. Find the module in the configuration.
3. Set the **Version** field to the specific version (e.g., `0.1.0`).
4. Click **Save**.

The machine stays on that version until you change the pin or remove it.

#### View available versions

To see all published versions of your module:

```bash
viam module list --module-id my-org:my-sensor-module
```

This shows each version, its upload date, and the supported platforms.

## Try It

1. Prepare your `meta.json` with the correct module ID, models, and build
   configuration.
2. Upload your module to the registry (either through cloud build or manually).
3. Navigate to a machine in the Viam app and add your module from the registry.
4. Configure a component using your module and set the required attributes.
5. Open the **CONTROL** tab and verify the component works:
   - For a sensor: click **Get readings** and confirm values appear.
   - For a camera: toggle the stream and confirm an image appears.
   - For a generic component: send a DoCommand and confirm a response.
6. Upload a new version (e.g., `v0.2.0`) and verify the machine picks it up
   automatically within a few minutes.

If all checks pass, your module is deployed and ready for fleet-wide use.

## Troubleshooting

### Upload fails with "not authenticated"

- Log in to the Viam CLI: `viam login`. Follow the prompts to authenticate.
- If using an API key, verify it has organization-level access. Keys scoped to a
  single machine cannot upload modules.
- Check that `VIAM_KEY_ID` and `VIAM_KEY_VALUE` are set correctly in your GitHub
  secrets (for cloud build).

### Upload fails with "invalid meta.json"

- Verify `meta.json` is valid JSON. Run `python -m json.tool meta.json` or
  `jq . meta.json` to check for syntax errors.
- Confirm the `module_id` matches the format `namespace:module-name`. The
  namespace must match your organization's namespace in the Viam app.
- Ensure all model entries have both `api` and `model` fields, and the `api`
  value is a valid Viam resource API.

### Module not appearing in the registry

- Check the module's visibility. If it is `private`, it only appears for users
  in your organization. Make sure you are logged in to the correct organization
  in the Viam app.
- Verify the upload completed successfully. Check the CLI output or the GitHub
  Actions log for errors.
- The module may take a minute to propagate after upload. Refresh the page and
  try searching again.

### Machine cannot find the module

- Verify the module version supports the machine's platform. If your machine
  runs `linux/arm64` (e.g., a Raspberry Pi) but you only uploaded for
  `linux/amd64`, the machine cannot use the module. Upload for the correct
  platform or add it to your `build.arch` list.
- Check the module version. If the machine is pinned to a version that does not
  exist, it will fail. Run `viam module list --module-id my-org:my-sensor-module`
  to see available versions.
- Confirm the machine is online and connected to the cloud. The module download
  requires network access.

### Cloud build fails in GitHub Actions

- Check the Actions tab in your GitHub repository for the build log. The most
  common issues are missing dependencies in `setup.sh` or build errors in
  `build.sh`.
- Verify your `setup.sh` and `build.sh` scripts work locally before pushing.
  Run them on your development machine to confirm they produce the expected
  output in `dist/`.
- Confirm the `build.path` in `meta.json` matches the actual output location of
  your build script.
- Ensure the GitHub secrets (`VIAM_KEY_ID` and `VIAM_KEY_VALUE`) are set and
  not expired.

### Module works locally but fails after deployment

- The deployed module runs in a different environment than your development
  machine. Check for hard-coded paths, missing environment variables, or
  dependencies that are installed on your machine but not in the build
  environment.
- For Python modules, verify all dependencies are in `requirements.txt`. A
  package that is globally installed on your development machine may not be
  available on the target machine.
- For Go modules, verify the binary is compiled for the correct target
  architecture. A binary compiled for `amd64` does not run on `arm64`.
- Check the module logs in the Viam app (**LOGS** tab) for error messages from
  the deployed environment.

## What's Next

- [Write an Inline Module](write-an-inline-module.md) -- prototype quickly with
  an inline module before building a full deployable module.
- [Filter at the Edge](../data/filter-at-the-edge.md) -- deploy filtering
  modules across your fleet to reduce data costs.
- [Add Computer Vision](../vision-detection/add-computer-vision.md) -- deploy
  vision service modules that run ML models on your machines.
