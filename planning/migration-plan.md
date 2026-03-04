# Migration Plan: docs-dev → viam-docs

**Status:** Phases 1-4 Complete, Restructured
**Date:** 2026-03-03 (updated 2026-03-04)

Migrate the 23 completed blocks (and future blocks) from `docs-dev/build/` into the
Hugo-based `viam-docs/docs/` site. All 23 blocks have been ported and the site has
been restructured: block categories promoted from `build/` subsections to top-level
sections, and Foundation split into "Get Started", "Hardware", and "Data".

---

## Decisions

| # | Issue | Decision |
|---|-------|---------|
| 1 | Structure | **Categorized** — adopt the docs-dev category structure (`build/data/`, `build/train/`, etc.) in viam-docs. Move the 3 misplaced stubs out of `build/foundation/`. |
| 2 | Content scope | **Port now, trim later** — convert blocks to Hugo format with full content intact. Editorial trimming to match Diataxis howto style happens in a separate pass. |
| 3 | Missing stubs | **Write stop-data-capture only** — draft `stop-data-capture.md` for `build/foundation/`. Delete the `start-writing-code.md` stub; the three development blocks replace it. |
| 4 | Conversion approach | **Manual** — convert each block by hand during the port. No automation script. |
| 5 | Source page cleanup | **Separate follow-up PRs** — land the blocks first, then clean up source pages section-by-section in follow-up PRs per the IA-REORG-PLAN. |
| 6 | Top-level promotion | **Promoted** — block categories promoted from `build/` subsections to top-level sections (e.g., `docs/build/data/` → `docs/data/`). Eliminates the extra `build/` nesting level. |
| 7 | Foundation split | **Split** — Foundation renamed to "Get Started" (single page overview), "Add a Camera" moved to new "Hardware" section, data-related pages moved to "Data" section. |

---

## Format Conversion Reference

Each docs-dev block needs these manual conversions when porting to viam-docs:

### Frontmatter

Replace the title line and bold metadata with YAML frontmatter:

**docs-dev:**
```markdown
# Configure Data Pipelines

**Time:** ~25 minutes
**Prerequisites:** [Capture and Sync Data](../foundation/capture-and-sync-data.md)
**Works with:** Simulation ✓ | Real Hardware ✓
```

**viam-docs:**
```yaml
---
linkTitle: "Configure Data Pipelines"
title: "Configure Data Pipelines"
weight: 40
layout: "docs"
type: "docs"
description: "Create scheduled pipelines that automatically aggregate and summarize captured data."
date: "2026-03-03"
---
```

The Time, Prerequisites, and Works-with metadata from docs-dev should be preserved
as a short intro paragraph below the frontmatter, not in frontmatter fields (Hugo
has no standard fields for these).

### Code Tabs

Replace `**Python:**` / `**Go:**` labels with Hugo tab shortcodes:

**docs-dev:**
````markdown
**Python:**

```python
result = await data_client.tabular_data_by_mql(...)
```

**Go:**

```go
result, err := dataClient.TabularDataByMQL(ctx, ...)
```
````

**viam-docs:**
````markdown
{{< tabs >}}
{{% tab name="Python" %}}

```python
result = await data_client.tabular_data_by_mql(...)
```

{{% /tab %}}
{{% tab name="Go" %}}

```go
result, err := dataClient.TabularDataByMQL(ctx, ...)
```

{{% /tab %}}
{{< /tabs >}}
````

### Alerts

Convert bold-text warnings or important notes to alert shortcodes:

**docs-dev:**
```markdown
**Important:** Translations are in millimeters, not centimeters or meters.
```

**viam-docs:**
```markdown
{{< alert title="Important" color="note" >}}
Translations are in millimeters, not centimeters or meters.
{{< /alert >}}
```

Use `color="note"` for informational, `color="caution"` for warnings,
`color="tip"` for helpful hints.

### Internal Links

Update relative markdown links to Hugo absolute paths:

**docs-dev:**
```markdown
[Capture and Sync Data](../foundation/capture-and-sync-data.md)
```

**viam-docs:**
```markdown
[Capture and Sync Data](/data/capture-and-sync-data/)
```

### Section Index Pages

Each new category directory needs an `_index.md` with cards:

```yaml
---
linkTitle: "Data"
title: "Data"
weight: 20
layout: "docs"
type: "docs"
no_list: true
description: "Work with captured data."
---

Work with captured data.

{{< cards >}}
{{% card link="/data/query-data/" %}}
{{% card link="/data/filter-at-the-edge/" %}}
{{% card link="/data/visualize-data/" %}}
{{% card link="/data/configure-data-pipelines/" %}}
{{% card link="/data/sync-data-to-your-database/" %}}
{{< /cards >}}
```

---

## Content Mapping

### Files to port (23 blocks)

| docs-dev path | viam-docs target path (final) | Replaces stub? |
|---|---|---|
| `build/foundation/connect-to-cloud.md` | `docs/get-started/initialize-a-viam-machine.md` | Yes (renamed) |
| `build/foundation/add-a-camera.md` | `docs/hardware/add-a-camera.md` | Yes (moved to Hardware) |
| `build/foundation/capture-and-sync-data.md` | `docs/data/capture-and-sync-data.md` | Yes (moved to Data) |
| `build/data/query-data.md` | `docs/data/query-data.md` | No (new) |
| `build/data/filter-at-the-edge.md` | `docs/data/filter-at-the-edge.md` | No (new) |
| `build/data/visualize-data.md` | `docs/data/visualize-data.md` | No (new) |
| `build/data/configure-data-pipelines.md` | `docs/data/configure-data-pipelines.md` | No (new) |
| `build/data/sync-data-to-your-database.md` | `docs/data/sync-data-to-your-database.md` | No (new) |
| `build/train/create-a-dataset.md` | `docs/train/create-a-dataset.md` | No (new) |
| `build/train/train-a-model.md` | `docs/train/train-a-model.md` | No (new) |
| `build/development/write-an-inline-module.md` | `docs/development/write-an-inline-module.md` | No (new) |
| `build/development/write-a-module.md` | `docs/development/write-a-module.md` | No (new) |
| `build/development/deploy-a-module.md` | `docs/development/deploy-a-module.md` | No (new) |
| `build/work-cell-layout/define-your-frame-system.md` | `docs/work-cell-layout/define-your-frame-system.md` | No (new) |
| `build/work-cell-layout/configure-robot-kinematics.md` | `docs/work-cell-layout/configure-robot-kinematics.md` | No (new) |
| `build/work-cell-layout/calibrate-camera-to-robot.md` | `docs/work-cell-layout/calibrate-camera-to-robot.md` | No (new) |
| `build/work-cell-layout/define-obstacles.md` | `docs/work-cell-layout/define-obstacles.md` | No (new) |
| `build/vision-detection/add-computer-vision.md` | `docs/vision-detection/add-computer-vision.md` | No (new) |
| `build/vision-detection/detect-objects-2d.md` | `docs/vision-detection/detect-objects-2d.md` | No (new) |
| `build/vision-detection/classify-objects.md` | `docs/vision-detection/classify-objects.md` | No (new) |
| `build/vision-detection/track-objects-across-frames.md` | `docs/vision-detection/track-objects-across-frames.md` | No (new) |
| `build/vision-detection/measure-depth.md` | `docs/vision-detection/measure-depth.md` | No (new) |
| `build/vision-detection/localize-objects-in-3d.md` | `docs/vision-detection/localize-objects-in-3d.md` | No (new) |

### Stubs to handle in viam-docs

| Existing stub | Action |
|---|---|
| `build/foundation/connect-to-cloud.md` | Replace with ported block |
| `build/foundation/add-a-camera.md` | Replace with ported block |
| `build/foundation/capture-and-sync-data.md` | Replace with ported block |
| `build/foundation/filter-data.md` | Delete (replaced by `build/data/filter-at-the-edge.md`) |
| `build/foundation/configure-data-pipelines.md` | Delete (replaced by `build/data/configure-data-pipelines.md`) |
| `build/foundation/sync-to-your-database.md` | Delete (replaced by `build/data/sync-data-to-your-database.md`) |
| `build/foundation/start-writing-code.md` | Delete (replaced by `build/development/` blocks) |
| `build/foundation/stop-data-capture.md` | Keep stub; write content for it |

### New files to create

| File | Purpose |
|---|---|
| `docs/get-started/_index.md` | Get Started section (single page, formerly Foundation) |
| `docs/hardware/_index.md` | Hardware category landing page |
| `docs/data/_index.md` | Data category landing page |
| `docs/train/_index.md` | Train category landing page |
| `docs/development/_index.md` | Development category landing page |
| `docs/work-cell-layout/_index.md` | Work Cell Layout category landing page |
| `docs/vision-detection/_index.md` | Vision & Detection category landing page |
| `docs/data/stop-data-capture.md` | New block (formerly in foundation) |

---

## Execution Phases

### Phase 1: Foundation -- COMPLETE (committed)

**Scope:** 3 blocks + 1 new block + structural cleanup

1. Convert and replace the 3 foundation stubs:
   - `connect-to-cloud.md`
   - `add-a-camera.md`
   - `capture-and-sync-data.md`
2. Write `stop-data-capture.md` content (small -- 3 toggle procedures).
3. Update `build/foundation/_index.md`:
   - Remove cards for pages moving to other categories.
   - Keep cards for the 4 foundation pages.
4. Update `build/_index.md` to reference foundation only (other categories come later).
5. Verify Hugo build succeeds, sidebar renders correctly.

**Files touched:** 6 (3 replaced, 1 written, 2 index files updated)

### Phase 2: Data -- COMPLETE (committed)

**Scope:** 5 blocks + directory setup + stub cleanup

1. Create `docs/build/data/_index.md`.
2. Convert and add the 5 data blocks:
   - `query-data.md`
   - `filter-at-the-edge.md`
   - `visualize-data.md`
   - `configure-data-pipelines.md`
   - `sync-data-to-your-database.md`
3. Delete the 3 misplaced stubs from `build/foundation/`:
   - `filter-data.md`
   - `configure-data-pipelines.md`
   - `sync-to-your-database.md`
4. Delete `build/foundation/start-writing-code.md` (replaced by development blocks in Phase 3).
5. Update `build/foundation/_index.md` to remove deleted cards.
6. Update `build/_index.md` to add Data category card.
7. Add aliases from old stub paths to new locations so any existing links don't break.

**Files touched:** 12 (5 new blocks, 1 new index, 4 deleted, 2 indexes updated)

### Phase 3: Train + Development -- COMPLETE (committed)

**Scope:** 5 blocks + 2 directory setups

1. Create `docs/build/train/_index.md`.
2. Convert and add 2 train blocks:
   - `create-a-dataset.md`
   - `train-a-model.md`
3. Create `docs/build/development/_index.md`.
4. Convert and add 3 development blocks:
   - `write-an-inline-module.md`
   - `write-a-module.md`
   - `deploy-a-module.md`
5. Update `build/_index.md` to add Train and Development category cards.

**Files touched:** 8 (5 new blocks, 2 new indexes, 1 index updated)

### Phase 4: Work Cell Layout + Vision & Detection -- COMPLETE (committed)

**Scope:** 10 blocks + 2 directory setups

1. Create `docs/build/work-cell-layout/_index.md`.
2. Convert and add 4 work cell layout blocks:
   - `define-your-frame-system.md`
   - `configure-robot-kinematics.md`
   - `calibrate-camera-to-robot.md`
   - `define-obstacles.md`
3. Create `docs/build/vision-detection/_index.md`.
4. Convert and add 6 vision & detection blocks:
   - `add-computer-vision.md`
   - `detect-objects-2d.md`
   - `classify-objects.md`
   - `track-objects-across-frames.md`
   - `measure-depth.md`
   - `localize-objects-in-3d.md`
5. Update `build/_index.md` to add both category cards.

**Files touched:** 13 (10 new blocks, 2 new indexes, 1 index updated)

### Post-Phase Restructure -- COMPLETE (committed)

**Scope:** Promote categories to top-level, split Foundation

1. Promoted all block categories from `docs/build/<category>/` to `docs/<category>/`.
2. Split Foundation:
   - Renamed to "Get Started" (single overview page).
   - Moved `add-a-camera.md` to new `docs/hardware/` section.
   - Moved `capture-and-sync-data.md` and `stop-data-capture.md` to `docs/data/`.
3. Updated all internal links and card references to use new top-level paths.
4. Updated `_index.md` files and weight assignments for new structure.

### Phase 5: Source Page Cleanup (1 PR per section)

Follow the `IA-REORG-PLAN.md` for each source page affected by the new blocks.
Each PR removes procedural content from the existing reference page and adds a
cross-link to the new block.

Separate PRs by source section:
- `data-ai/capture-data/` pages
- `data-ai/data/` pages
- `data-ai/train/` pages
- `operate/modules/` pages
- `operate/install/` pages
- `reference/components/camera/` pages
- `reference/services/vision/` pages
- `reference/services/frame-system/` pages

---

## Weight Assignments

Top-level section weights for sidebar ordering (post-restructure):

| Section | Weight | Rationale |
|---|---|---|
| Get Started | 30 | Everyone starts here |
| Hardware | 35 | Configure physical components |
| Data | 40 | Capture, sync, query, visualize |
| Train | 50 | Uses captured data |
| Development | 60 | Write custom code |
| Work Cell Layout | 70 | Spatial setup for manipulation |
| Vision & Detection | 80 | Perception pipeline |
| Stationary Vision | 90 | (future) |
| Mobile Base | 100 | (future) |
| Arm + Manipulation | 110 | (future) |
| Productize | 120 | (future) |

Within each section, blocks are weighted in the order listed in `docs-dev/build/INDEX.md`,
starting at 10 and incrementing by 10.

---

## Open Items

- [x] Write `stop-data-capture.md` content before Phase 1
- [x] Determine whether moved stubs need `aliases` for SEO (the stubs have no
  inbound links yet since they say "Content to be written", but check before deleting)
- [x] Verify Hugo build after each phase before merging
- [x] Port all 23 blocks (Phases 1-4)
- [x] Restructure: promote categories to top-level, split Foundation
- [ ] Phase 5: Source page cleanup (1 PR per section) -- not yet started
- [ ] Remaining 27 blocks (Stationary Vision, Mobile Base, Arm + Manipulation,
  Productize) -- draft in docs-dev, then port using the same process
