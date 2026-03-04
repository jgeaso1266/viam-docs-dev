# Content Guidelines

**Status:** Updated to reflect actual editorial standards from viam-docs migration.

Guidelines for authors implementing content from this documentation plan.

---

## Terminology

- Use **"how-to"** (not "block") in all user-facing content. "Block" is an internal planning term only.
- Use **"machine"** (not "device") throughout.
- Do not reference simulation or fake components. All instructions should target real hardware.
- Avoid marketing language. Be direct and factual.

---

## How-to Page Structure

Each how-to page uses the following structure:

### YAML Frontmatter

```yaml
---
linkTitle: "Short Nav Title"
title: "Full Page Title"
weight: 10
layout: "docs"
type: "docs"
description: "One-sentence description of what this page covers."
date: "2025-01-01"
---
```

### Page Body

| Section | Description |
|---------|-------------|
| **## What Problem This Solves** | 2-3 concise sentences. State the problem directly, no marketing. |
| **Step-by-step content** | Use `##` headers for each major step. Provide clear instructions with complete, copy-paste-able code. |
| **## Try It** | Verification section. Include a complete test script the reader can run to confirm everything works. |
| **## Troubleshooting** | Collapsible sections using `{{</* expand */>}}` shortcodes. Cover common failures with "If you see X, check Y" patterns. |
| **## Next Steps** | Links to related how-to pages and reference material. |

### Shortcodes

| Shortcode | Use |
|-----------|-----|
| `{{</* tabs */>}}` | Wrap Python/Go code alternatives |
| `{{</* alert */>}}` | Tips, notes, and warnings |
| `{{</* expand */>}}` | Collapsible troubleshooting items |

---

## How-to Pages Are Top-Level Sections

How-to pages live as top-level sections in the docs navigation, not nested under a "Build/" parent. Structure the `weight` values in frontmatter to control ordering within the section.

---

## Self-Containment

Each how-to should be completable by a reader who arrives directly at that page. This means providing everything they need within the page itself.

### What "Everything They Need" Includes

| Element | Description |
|---------|-------------|
| **Conceptual context** | Why this matters, what problem it solves |
| **Prerequisites state** | The configuration and code state needed to begin |
| **Step-by-step instructions** | The actual content |
| **Working code samples** | Complete, copy-paste-able code |
| **Verification** | How to confirm it worked (the "Try It" section) |
| **Troubleshooting** | Common failures and how to resolve them |

### Challenges and Solutions

| Challenge | Problem | Solution |
|-----------|---------|----------|
| **Configuration state** | A how-to assumes a camera and vision service exist. Do we repeat camera setup? | Provide a "start here" fragment. Reader applies the fragment and has the prerequisite configuration. |
| **Code state** | How-to B extends code from how-to A. Do we repeat A's code? | Provide starter code or a GitHub repo with checkpoints. Each page links to its starting point. |
| **Conceptual dependencies** | Can you explain "Track Objects Across Frames" without the reader understanding detections? | Brief recap, not re-teaching. One paragraph: "This page assumes you can get detections--a list of bounding boxes with labels and confidence scores." |
| **Length vs. self-containment** | Fully self-contained pages might be long. | Use fragments and starter code to handle setup. The page itself focuses on the new material. |

---

## Troubleshooting Deserves Special Attention

A reader who worked through prior how-tos has context: "I just configured the camera, so if detections aren't working, maybe the camera config is wrong."

A reader who arrived directly has no such context. They applied a fragment and starter code--if something doesn't work, they don't know where to look.

**Each how-to needs independent troubleshooting guidance.** Don't assume the reader knows what might be broken. Use collapsible `{{</* expand */>}}` sections for each troubleshooting item. Common patterns:

- "If you see X, check Y"
- "Verify the camera is streaming by..."
- "Confirm the model loaded by..."

---

## Diataxis Alignment

Our content maps to the [Diataxis framework](https://diataxis.fr/):

| Diataxis Type | Purpose | Our Content |
|---------------|---------|-------------|
| **Tutorial** | Learning-oriented, guided journey | Guided walkthroughs |
| **How-to Guide** | Task-oriented, solve specific problem | How-to pages, Deploy/Scale/Maintain |
| **Explanation** | Understanding-oriented, the "why" | Understand section |
| **Reference** | Information-oriented, lookup | Reference section |

Our how-to pages are closer to how-to guides than tutorials. They assume the reader chose that page for a reason and wants to accomplish a specific task.

---

## Writing Style

- Be direct and concise. No marketing language.
- Use second person ("you") for instructions.
- State what something does, not how exciting it is.

---

## Links

Internal links use absolute Hugo paths with trailing slashes:

```markdown
[Configure a camera](/operate/reference/components/camera/)
```

Do not use relative paths or omit trailing slashes.

---

## Code Samples

### Language Requirements

All control logic code must be provided in both **Python** and **Go**.

- Use `{{</* tabs */>}}` shortcodes so readers can switch between languages
- Both versions should be functionally equivalent
- Both must be tested and complete (copy-paste-able)

### What Counts as "Control Logic"

Code that interacts with Viam APIs to control or read from components:

- Getting camera images
- Running detections
- Moving arms/bases
- Reading sensor data
- Sending commands

### What Doesn't Need Both Languages

- Shell commands (e.g., `viam module upload`)
- Configuration snippets (JSON)
- One-off debugging scripts

---

## Content Checklist

Before considering a how-to complete, verify:

- [ ] Can be completed without prior how-tos (using provided fragment + starter code)
- [ ] "What Problem This Solves" explains why this matters in 2-3 sentences
- [ ] All control logic code provided in both Python and Go using `{{</* tabs */>}}`
- [ ] All code samples are complete and tested
- [ ] "Try It" section includes a complete verification script
- [ ] Troubleshooting covers common failures in collapsible `{{</* expand */>}}` sections
- [ ] No references to simulation or fake components
- [ ] Uses "machine" not "device"
- [ ] No marketing language
- [ ] Internal links use absolute Hugo paths with trailing slashes
- [ ] Links to logical next steps
