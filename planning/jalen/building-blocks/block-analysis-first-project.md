# Block Analysis: First Project Tutorial

**Date:** 2026-02-11
**Analyzed Tutorial:** `/viam-docs/docs/operate/hello-world/first-project/`
**Compared Against:** `/viam-docs-dev/planning/block-definitions.md`

## Recommended Block Additions

Based on analysis of the "Your First Project" stationary vision tutorial, the following blocks should be added to fill gaps between what the tutorial teaches and what the current block definitions cover:

| Block Name | Category | Time | Components | What You Learn | Problems Addressed |
|------------|----------|------|------------|----------------|-------------------|
| **Write a Module** | Foundation | ~15 min | CLI + laptop + remote machine | Generate module scaffolding, dependency injection pattern, DoCommand interface, remote testing against hardware | 1.3, 1.21 |
| **Deploy a Module** | Foundation | ~10 min | CLI + registry | Cross-compile for target platform, package modules, upload to registry, version management, add to machine config | 1.21, 4.8 |
| **Query Tabular Data** | Foundation | ~10 min | Data service + captured data | Configure DoCommand data capture, SQL vs MQL queries, navigate nested JSON, filter and aggregate results | 2.13, 3.10 |
| **Build a Teleop Dashboard** | Productize | ~10 min | Teleop + MQL | Create workspaces, configure widgets, write MQL aggregation pipelines, time series visualization | 4.9 |
| **Build a Web App** | Productize | ~15 min | TypeScript SDK | Custom web applications, real-time data access, customer-facing interfaces, branding | 4.9 |

---

## Rationale

### 1. Write a Module

**What the tutorial teaches (Part 3):**
- Generate module scaffolding with `viam module generate`
- Declare dependencies in Config struct and Validate() method
- Extract dependencies using `FromProvider()` pattern
- Implement business logic (e.g., `detect()` method)
- Expose functionality through DoCommand interface
- Test locally on laptop against remote hardware using `vmodutils.ConnectToHostFromCLIToken()`
- Rapid iteration: edit → run → see results on real hardware

**Current block coverage:**
- "Start Writing Code" (Foundation) - only says "Run code remotely against hardware"
- Doesn't capture module-specific patterns, dependency injection, or development workflow

**Why this needs a separate block:**
- Module development is fundamentally different from writing standalone scripts
- Dependency injection is a core Viam pattern that needs explicit teaching
- Remote testing workflow is a critical productivity multiplier
- DoCommand pattern for generic services is not obvious
- This is ~15 minutes of distinct, teachable content

---

### 2. Deploy a Module

**What the tutorial teaches (Part 4.1-4.3):**
- Review generated module structure (cmd/module/main.go, meta.json)
- Cross-compile for target platform (GOOS, GOARCH, CGO_ENABLED flags)
- Package module with metadata (tar.gz with meta.json + binary)
- Upload to registry with platform-specific flags
- Version management (0.0.1, etc.)
- Add registry modules to machine configuration

**Current block coverage:**
- Not covered in any existing block
- "Start Writing Code" stops at running code, not deploying it

**Why this needs a separate block:**
- Deployment is distinct from development
- Cross-compilation is non-obvious (especially CGO_ENABLED=0 and no_cgo tag)
- Registry workflow is production-critical
- Platform matching is error-prone
- Could be combined with "Write a Module" as one ~25 min block if needed

---

### 3. Query Tabular Data

**What the tutorial teaches (Part 4.4):**
- Configure data capture on DoCommand with additional parameters
- Set up service dependencies using `depends_on` in JSON config
- Query captured data with SQL (SELECT with WHERE, ORDER BY, LIMIT)
- Query with MQL aggregation pipelines ($match, $group, etc.)
- Navigate nested JSON structure (`data.docommand_output.label`)
- Understand difference between binary data (images) and tabular data (JSON)

**Current block coverage:**
- "Capture and Sync Data" covers images only
- "Configure Data Pipelines" mentions "windowed roll-ups, aggregations" but unclear if it covers DoCommand capture
- No block explicitly teaches SQL/MQL querying

**Why this needs a separate block:**
- Different data type (tabular/JSON vs binary/images)
- Different configuration pattern (method + parameters vs component-level)
- Different use case (analytics/queries vs visual review)
- SQL and MQL are different skills with different syntax
- This enables all downstream analytics work

---

### 4. Build a Teleop Dashboard

**What the tutorial teaches (Part 5):**
- Create Teleop workspaces for specific locations/machines
- Add and configure widgets (camera stream, time series)
- Write custom MQL aggregation pipelines:
  - `$match` - filter documents
  - `$group` - aggregate with $sum, $avg, $dateTrunc for time buckets
  - `$project` - shape output for visualization
- Configure widget parameters (refresh rates, time ranges, axis bounds)
- Arrange dashboard layout

**Current block coverage:**
- "Build a Customer Dashboard" says "TypeScript SDK, web apps, real-time data display"
- Completely different approach - no mention of Teleop or MQL

**Why this needs a separate block:**
- Teleop is for **internal monitoring** (operators, engineers)
- Web apps are for **customer-facing** applications
- Different tools, different audiences, different use cases
- MQL pipelines are a distinct skill
- No-code/low-code approach vs full programming
- This is the fastest path to operational dashboards

---

### 5. Build a Web App

**What should be taught (not in tutorial):**
- Set up TypeScript SDK project
- Authenticate and connect to Viam
- Access machine resources through SDK
- Query data with `tabularDataBySQL()` and `tabularDataByMQL()`
- Build custom UI with any framework (React, Vue, etc.)
- Deploy customer-facing applications
- Apply custom branding

**Current block coverage:**
- "Build a Customer Dashboard" exists but title is too specific
- Should be renamed to "Build a Web App"

**Why this is distinct from Teleop:**
- **Teleop**: Built-in Viam UI, internal monitoring, quick setup
- **Web App**: Custom development, customer-facing, full control over UX
- Different skill set (programming vs configuration)
- Different deployment model (hosted separately vs Viam-hosted)
- Use cases: customer portals, branded monitoring, embedded controls, custom workflows

---

## Comparison: Tutorial vs Stationary Vision Work Cell Path

### What the Tutorial Covers

**Foundation:**
- ✅ Connect to Cloud (Part 1.1-1.2)
- ✅ Add a Camera (Part 1.3-1.4)
- ✅ Capture and Sync Data (Part 2)
- ✅ Start Writing Code (Part 3) - *but much deeper than block suggests*

**Vision & Detection:**
- ✅ Add Computer Vision (Part 1.5)
- ✅ Classify Objects (Part 1.6 - PASS/FAIL classification)

**Productize:**
- ✅ Build a Dashboard (Part 5 - Teleop version)

### What the Tutorial Does NOT Cover

**Foundation:**
- ❌ Basic Filtering (time-based sampling, sensor thresholds)
- ❌ Configure Data Pipelines (mentioned but not taught as standalone block)
- ❌ Sync Data to Your Database (external MongoDB egress)

**Stationary Vision:**
- ❌ Trigger on Detection (event-driven actions, alerts)
- ❌ Count Objects (accumulation, logging to dashboard)
- ❌ Inspect for Defects (covered implicitly but not as separate block)
- ❌ Monitor Over Time (baseline establishment, anomaly detection)

**Productize:**
- ❌ Branded Customer Login
- ❌ Configure Billing

### What the Tutorial Teaches That Blocks Don't Cover

- ✅ Module development workflow (generate, develop, test remotely)
- ✅ Module deployment (cross-compile, package, upload)
- ✅ Tabular data capture and querying (DoCommand + SQL/MQL)
- ✅ Teleop dashboard building with MQL

---

## Implementation Notes

### Block Self-Containment Challenge

The tutorial is a **linear path** where state accumulates across parts. This violates the block principle that "each block should be completable by a reader who arrives directly at that block."

For the recommended blocks to work as standalone modules:

1. **Write a Module**
   - Provide starter: machine config with camera + vision service already configured
   - Provide fragment: pre-configured `inspection-cam` and `vision-service`

2. **Deploy a Module**
   - Provide starter: complete module code ready to build
   - Could be continuation of "Write a Module" or standalone with provided code

3. **Query Tabular Data**
   - Provide starter: machine already capturing DoCommand data
   - Provide sample queries and expected data structure

4. **Build a Teleop Dashboard**
   - Provide starter: machine with data already captured
   - Provide example MQL pipelines to adapt

5. **Build a Web App**
   - Provide starter: authentication credentials and sample data
   - Provide TypeScript SDK boilerplate

### Suggested Block Ordering

Within the Foundation category:
1. Connect to Cloud
2. Add a Camera
3. Capture and Sync Data
4. **Start Writing Code** (rename to "Write Control Code" - simple scripts)
5. **Write a Module** (new - structured development)
6. **Deploy a Module** (new - production deployment)
7. **Query Tabular Data** (new - analytics foundation)

This progression goes from simple (run code) → structured (module pattern) → production (deploy) → analytics (query).