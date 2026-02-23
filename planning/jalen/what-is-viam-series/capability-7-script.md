# Capability #7: Scale Easily
## 60-Second Video Script

**Learning Outcome:** "One robot's config becomes 100 robots' config with zero scripting"

**Demo Setup:** 2-3 identical sensor stations (Raspberry Pis with cameras) framed as "Quality Control Stations" monitoring different production zones. Each station views a desk/area with multiple objects (cups, bottles, keyboards, mice, laptops). Initially detecting only cups and bottles. Viam app showing fragment management and fleet dashboard.

---

## Script

### [00:00-00:08] Hook (8 seconds)

*Visual:*
- Presenter on camera
- Multiple QC stations visible in background with labels ("Zone A", "Zone B", "Zone C")

*Presenter:*
"Deploy one quality control station. Scale to dozens across your facility without writing deployment scripts. Let me show you."

---

### [00:08-00:18] Explain Fragments (10 seconds)

*Visual:*
- Show one working QC station (camera viewing desk with objects)
- ML detection boxes visible on screen around cups and bottles only
- Screen showing its configuration in Viam app
- Station labeled "Zone A - Quality Control"

*Presenter (voiceover):*
"Configure one station. Detects cups and bottles. That config becomes a fragment—a reusable template for your entire fleet."

---

### [00:18-00:32] Demo: Create and Apply Fragment (14 seconds)

*Visual:*
- Quick montage:
  - Create fragment from Zone A station (export/save)
  - Fragment appears in registry
  - Apply fragment to Zones B and C with location overrides
  - Show override: Each keeps unique zone label
  - All stations provision and start working
  - All three stations now detecting cups and bottles (same detection boxes visible)

*Presenter (voiceover):*
"Create fragment from Zone A. Apply to Zones B and C. All provision automatically. Same inspection logic, different locations."

---

### [00:32-00:50] Demo: Update Propagation (The "Wow") (18 seconds)

*Visual:*
- Focus on Viam app showing fragment configuration
- Edit fragment: Change detected object classes from ["cup", "bottle"] to ["cup", "bottle", "keyboard", "mouse", "laptop"]
- Save fragment update
- Show fleet dashboard with all 3 stations:
  - Status indicators: "Updating..." on all stations
  - All stations pull new config simultaneously
  - **Visual change:** Detection boxes suddenly appear on keyboards, mice, and laptops across ALL stations
  - Each station keeps its zone label (A, B, C)
  - Dramatic and obvious - new object types now detected everywhere
- Timestamp showing update takes seconds

*Presenter (voiceover):*
"Update fragment to detect more object types. All stations pull the change. Detection boxes appear on new objects across the fleet. In seconds."

---

### [00:50-00:60] Payoff (10 seconds)

*Visual:*
- Back to presenter on camera
- All three QC stations visible, running with updated config
- Optional: Show fleet dashboard indicating all stations in sync

*Presenter:*
"One station becomes dozens. Update once, update everywhere. Production-scale fleet management with zero scripting."

*Final beat:*
"That's Viam."

---

## Production Notes

**Total time:** 60 seconds

**Pacing:**
- Hook establishes production context (QC stations, facility scale)
- Fragment explanation is brief and clear
- Fragment creation/application is fast-paced
- Update propagation is the centerpiece with clear visual proof
- Payoff reinforces production scale and ease

**The narrative arc:**
Production deployment challenge → Fragments make config reusable → Deploy to multiple zones with overrides → Update fragment, entire fleet synchronizes → This is production-scale fleet management

**Key message:**
Production-scale deployment without scripting. One configuration becomes many, updates propagate instantly, per-site customization without forking.

**Critical moment:**
Fragment update propagating to all stations in real-time, with visual proof that all stations update while maintaining their zone-specific settings.

---

## Production Framing - Critical

**This is NOT a hobby demo.** Frame everything as production/industrial:
- Call them "Quality Control Stations" not "sensor stations"
- Use "Zone A/B/C" or "Station 1/2/3" labels
- Mention "facility", "fleet", "production"
- Show professional dashboard/UI
- Narration emphasizes "dozens of stations" even though we show 3
- Visual design should feel industrial/professional, not hobbyist

**The stations are performing real work:**
- ML-based quality inspection
- Monitoring different zones of a facility
- Running production inspection logic
- This could scale to 100 stations doing the same thing

---

## B-Roll Needed

- All 3 QC stations visible in frame with zone labels clear
- Close-ups of individual stations with ML detection visible
- All three camera feeds/detection results visible simultaneously
- Professional labels/overlays: "Zone A - Quality Control" etc.
- Fleet dashboard showing all stations
- Visual indication of update happening (status, progress bars, etc.)
- Before/after showing detection or behavior change across all stations

## Screen Recordings Needed

- Working QC station configuration in Viam app
- Camera feed with ML detection/classification visible
- Creating/exporting fragment from Zone A
- Fragment in registry/library
- Applying fragment to multiple stations with zone overrides visible
- Override configuration showing zone-specific parameters
- Fleet dashboard showing all stations
- Fragment editor showing shared configuration
- Editing fragment (updating ML model version, detection parameters, or similar)
- Saving fragment update
- Fleet view showing all stations updating simultaneously
- Station status indicators during update ("Updating...", "Synced", etc.)
- Updated behavior visible on all stations (new detection, different parameters, etc.)

## Graphics/Overlays

- Professional zone labels: "Zone A - Quality Control", "Zone B - Quality Control", "Zone C - Quality Control"
- "1 Fragment → 3 Zones" or "1 Update → Entire Fleet" text overlay
- Fleet status dashboard (professional looking)
- Timestamp showing update speed (< 10 seconds)
- Status indicators: "Synced", "Updating", "Running"
- Optional: Facility map showing station locations
- Optional: "Scales to 100+ stations" text overlay
- Clean, industrial aesthetic - NOT hobbyist

## Technical Considerations

**Making It Feel Production-Scale:**
- Use professional terminology (QC, facility, fleet, zones)
- Visual design matters: clean overlays, professional labels
- Narrator mentions "dozens" or "hundreds" to imply scale beyond what's shown
- Frame it as a real use case: quality control in manufacturing

**Fragment Update Must Be Visually Clear:**
- Update changes detected object classes from ["cup", "bottle"] to ["cup", "bottle", "keyboard", "mouse", "laptop"]
- **Before:** Only cups and bottles have detection boxes
- **After:** Keyboards, mice, and laptops suddenly get detection boxes too
- Very obvious visual change - new boxes appear on new object types
- All stations show the change simultaneously
- Use split screen or fleet dashboard to show simultaneity across all 3 stations

**Per-Station Overrides:**
- Zone labels must be clearly visible and persistent
- Show that overrides are preserved after fragment update
- Emphasize: shared logic updated, local settings preserved

**Hardware Setup:**
- 2-3 Raspberry Pis with cameras
- Each views a desk/area with objects: cups, water bottles, keyboards, mice, laptops
- Same types of objects in each zone (for consistency)
- Objects should be clearly visible and well-lit
- ML model: Object detection (COCO model or similar pre-trained model)
- Clear visual output on screens/displays showing detection boxes
- Professional mounting/setup (not breadboards on desks)

**Detection Setup:**
- Initial fragment configures model to detect only: ["cup", "bottle"]
- Desks have cups, bottles, keyboards, mice, laptops visible
- Only cups and bottles get detection boxes initially
- Fragment update adds: ["keyboard", "mouse", "laptop"] to detection list
- After update: Detection boxes appear on all object types
- Visual change is dramatic and immediate across all stations
