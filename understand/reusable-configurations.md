# Reusable Configurations with Fragments

**Status:** Draft

When you have one robot, configuration is simple: you set it up, it works, you move on. When you have ten robots—or a hundred—configuration becomes a problem. How do you keep them consistent? How do you update them all? What happens when one machine needs slightly different settings?

Fragments solve these problems. A fragment is a reusable block of machine configuration that you define once and deploy to any number of machines. Update the fragment, and every machine using it receives the change. Need per-machine differences? Override specific values without duplicating the entire configuration.

This document explains what fragments enable and when to use them. For step-by-step instructions on creating and managing fragments, see the Build guides linked at the end.

---

## The Problem Fragments Solve

Robot configuration is more complex than typical software configuration. A machine's config includes hardware definitions (motors, cameras, sensors), service configurations (vision pipelines, data capture rules), network settings, calibration values, and more. This configuration determines how the machine behaves in the physical world.

At small scale, this complexity is manageable. You configure one machine, test it, and deploy it. But problems emerge as you scale:

**Configuration drift.** When you configure machines individually, small differences creep in over time. One machine gets a fix that others don't. Settings diverge. Debugging becomes harder because you can't assume machines are configured the same way.

**Update coordination.** Pushing a configuration change to fifty machines manually is tedious and error-prone. Miss one machine, and you have an inconsistent fleet. Make a typo on one, and that machine behaves differently.

**Hardware variance.** Real fleets have variation. Some machines have different camera models. Some are deployed in environments that require adjusted settings. Managing these differences while maintaining a shared baseline is difficult without the right abstractions.

**Provisioning at scale.** Setting up each new machine from scratch doesn't scale. You need a way to stamp out machines with known-good configurations quickly and reliably.

Fragments address all of these problems by establishing a single source of truth for machine configuration.

---

## Core Capabilities

### Define Once, Deploy Everywhere

A fragment captures a configuration that you want to reuse. This might be a complete machine setup (every component and service), or it might be a subset (just the camera and vision pipeline). You create the fragment once, then add it to any machine that needs that configuration.

When you add a fragment to a machine, the machine's configuration merges with the fragment's contents. The machine now has all the components, services, and settings defined in the fragment—without you copying and pasting JSON between machines.

Fragments can also include other fragments. This lets you compose configurations from smaller, reusable pieces. A "data capture" fragment might define capture rules; a "camera" fragment might define camera settings; a complete machine fragment might include both.

### Customize Without Forking

Fragments would be limited if every machine using them had to be identical. In practice, machines vary. One machine's camera is at a different IP address. Another machine needs a higher capture rate. A third machine is in a bright environment and needs adjusted exposure settings.

**Variables** let you parameterize a fragment. Instead of hardcoding a camera's IP address, you define a variable. When you add the fragment to a machine, you provide the value for that machine. Same fragment, different values per machine.

**Overwrites** let you modify specific parts of a fragment for a particular machine. If one machine in your fleet needs a different sensor threshold, you overwrite that value. The rest of the fragment stays intact. You're customizing, not forking.

This creates a spectrum of flexibility:

| Scenario | Approach |
|----------|----------|
| Machines are identical | Use fragment as-is |
| Machines differ by known parameters | Use fragment variables |
| One machine needs a specific tweak | Use fragment overwrites |
| Machines are fundamentally different | Use different fragments |

The goal is to keep shared configuration shared, while allowing necessary differences.

### Update Centrally, Propagate Automatically

When you update a fragment, machines using that fragment receive the update. You don't push changes to each machine individually—you change the source, and the change propagates.

This works even when machines are offline. Each machine caches its configuration locally. When connectivity returns, the machine checks for updates and applies them. If a machine reboots without network access, it runs from its cached configuration until it can sync.

For stability, you can pin a machine to a specific fragment version. Pinned machines don't automatically receive updates—they stay on the version you specified until you explicitly update them. This is useful for machines in production where you want to control exactly when changes take effect.

### Roll Out Safely

Updating configuration across a fleet carries risk. A bad configuration change can break machines. Fragments provide mechanisms to manage this risk:

**Version pinning.** Every change to a fragment creates a new version. You can pin machines to specific versions, ensuring they don't receive updates until you're ready.

**Tags.** You can tag fragment versions with names like "stable" or "beta." Some machines track the "stable" tag and only receive updates you've explicitly marked stable. Other machines track "beta" and receive updates earlier, serving as a test group.

**Staged rollouts.** Update a few machines first. Verify the change works. Then update the rest. Tags and version pinning make this workflow possible.

**Rollback.** If an update causes problems, pin affected machines back to the previous version. The fragment's version history gives you a known-good state to return to.

---

## Fragment Patterns

Different situations call for different fragment structures. Here are common patterns:

### The Golden Config

A complete machine template containing every component and service the machine needs. Add this fragment to a new machine, and it's fully configured.

**Example:** The Viam Rover fragments configure the board, motors, base, camera, and all other components for a standard rover. Add the fragment, and the rover is ready to drive.

**When to use:** Fleets of identical hardware where every machine should be configured the same way.

### The Component Library

Smaller fragments that each configure one piece of functionality. You compose these into complete configurations by adding multiple fragments to a machine.

**Example:** A "camera-and-capture" fragment that configures a camera and data capture rules. Add it to any machine that needs camera-based data collection, regardless of what else that machine does.

**When to use:** Mix-and-match scenarios where different machines need different combinations of capabilities.

### The Hardware Variant

A base fragment with overwrites for hardware differences. The fragment defines the standard configuration; machines with different hardware override the relevant parts.

**Example:** A fleet of inspection robots where most have Camera Model A, but some have Camera Model B. The fragment configures Model A. Machines with Model B override the camera configuration while keeping everything else from the fragment.

**When to use:** Fleets with hardware variation that can be expressed as parameter differences.

### The Provisioning Template

A fragment designed for zero-touch device setup. Combined with Viam's provisioning tools, new devices automatically configure themselves when they first connect.

**Example:** An air quality monitoring company creates a fragment with their sensor configuration and data pipeline. They flash SD cards with the provisioning agent and fragment ID. When a device boots and connects to WiFi, it automatically applies the fragment—no manual configuration needed.

**When to use:** Shipping pre-configured devices to customers or remote sites.

---

## When to Use Fragments

### Good Fit

Fragments make sense when:

- **You have two or more machines with shared configuration.** Even at small scale, fragments prevent drift and simplify updates.

- **You need to update multiple machines simultaneously.** Changing a fragment is faster and safer than updating machines individually.

- **Your hardware varies in ways that can be expressed as parameters.** Fragment variables and overwrites handle this cleanly.

- **You're shipping devices to customers or remote sites.** Provisioning templates make setup reliable and repeatable.

### Not a Fit

Fragments may not be the right tool when:

- **You have a single prototype machine.** Just configure it directly. You can extract a fragment later if you need to replicate it.

- **Your machines have fundamentally different architectures.** If machines share little configuration, separate fragments (or direct configuration) may be clearer than heavily overwritten fragments.

- **Configuration changes more often than it's shared.** If every machine needs constant, unique adjustments, the overhead of fragment management may not pay off.

### The "When Does One Become Many?" Question

A common question: when should you create your first fragment?

The practical answer: when you're about to configure a second machine that resembles the first. Before you copy-paste configuration, extract it into a fragment. This takes minutes and immediately prevents the drift that copy-paste introduces.

You don't need to plan for fragments from the start. Configure your first machine directly. Get it working. When you need a second machine, that's when you create the fragment from the working configuration.

---

## Fragments in Your Workflow

Fragments sit between your application code and individual machine configurations. Your code defines behavior; fragments define the hardware that behavior runs on.

### Fragments vs. Modules

Both fragments and modules are reusable, but they serve different purposes:

| Aspect | Fragments | Modules |
|--------|-----------|---------|
| **What it is** | Reusable configuration (JSON) | Reusable code (Go/Python) |
| **Contains** | Component definitions, service configs, parameters | Custom logic, drivers, algorithms |
| **Answers** | "What hardware do I have and how is it configured?" | "What can my hardware do beyond built-in capabilities?" |
| **Changes require** | Config update in Viam app (no rebuild) | Code changes, rebuild, republish |

A chess-playing robot illustrates the distinction. The **module** contains the chess logic: analyzing the board, calculating moves, coordinating the arm and gripper. The **fragment** contains the hardware specifics: the arm's IP address, the camera's serial number, the gripper's offset values.

This separation means the same module can work with different fragments. Deploy the chess module to a new robot arm by providing a new fragment with that arm's settings—no code changes needed.

**Decision framework:**
- Hardware settings that vary per deployment → fragment variables
- Custom behavior or new capabilities → module

### Team Patterns

As your team grows, consider:

- **Who owns the fragment?** Typically, the team responsible for that hardware or deployment pattern.
- **How do changes get reviewed?** Treat fragment changes like code changes when they affect production machines.
- **How do you test changes?** Use version pinning to test fragment updates on a subset of machines before fleet-wide rollout.

---

## Limitations and Boundaries

Fragments are powerful but not unlimited:

**Some resources can't be in fragments.** Triggers (event-based automations) must be configured directly on machines, not in fragments.

**Overwrites are all-or-nothing.** When you overwrite a fragment value on a machine, the overwrite either applies completely or fails entirely. There's no partial application. This prevents machines from ending up in inconsistent states.

**Complexity has limits.** If a machine's overwrites become extensive—overriding most of the fragment's values—consider whether a separate fragment would be clearer. Heavy overwrites can make configuration harder to understand and debug.

---

## What's Next

This document explained what fragments enable and when to use them. To start working with fragments:

- **Create your first fragment:** [Build: Create a Fragment](../build/foundation/create-fragment.md) — Extract configuration from a working machine into a reusable fragment.

- **Customize for different machines:** [Build: Customize a Fragment](../build/foundation/customize-fragment.md) — Use variables and overwrites to handle per-machine differences.

- **Manage versions and rollouts:** [Build: Fragment Versioning](../build/foundation/fragment-versioning.md) — Use tags and version pinning for safe fleet updates.

- **Look up syntax details:** [Reference: Fragment Configuration](../reference/fragments.md) — Complete reference for fragment JSON structure and options.
