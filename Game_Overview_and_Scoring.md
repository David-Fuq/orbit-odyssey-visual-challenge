# IntelXRP Object Detection Game

## Orbit Odyssey: Autonomous Lunar Detection

### Overview

- **Run length:** 120 seconds
- **Objects:** Exactly 3 classes total. Before each run, teams declare which classes are CONTACT and which are AVOID (e.g., 2 contact + 1 avoid).
- **Robot design variables (team-controlled):**
  - Camera height/tilt
  - Onboard lighting additions
- **Perception pipeline:**
  - Train model using the GUI and pre-provided datasets.
  - The AIxBoard script streams detections to XRP.
  - Students write the MicroPython code for robot behavior in the game.

---

# Game Field Setup

## What changes each match (announced at staging, set by refs)

### 1. Start Zone Corner
- Randomly chosen among the four corners.
- Robot must start fully inside.
- Heading is team-selected at set-down.

### 2. Placement Template (A/B/C)
One of three pre-published templates is drawn.

Each template defines:
- Three non-overlapping target zones (60 cm radius)
- Two hazard zones (50 cm radius)

Refs place:
- One cube from each of the 3 classes into its assigned target zone center
- Hazard cube(s) into hazard zones

Additional rule:
- At least one hazard is positioned to interfere with the straight-line path from start to a target ≥50% of the time.

### 3. Cube Facing
- For every cube, its image orientation is rotated by a random multiple of 90°.

### 4. Decoys (0–2 Blank Cubes or Different Images)
- At ref discretion
- Placed at least 30 cm from any zone center
- Never inside a target/hazard zone

### 5. Clearance Rules
- Minimum 30 cm cube-to-cube distance
- Minimum 20 cm cube-to-boundary distance

---

# Scoring

## Total Score Formula

```text
Total = (Field Score × Model-Size Multiplier) + mAP Bonus − Penalties
```

---

## A) Field Score (max 120)

- Contact a declared CONTACT class (unique cube per declared class): **+30 each**
- All declared CONTACT classes completed: **+15 bonus**
- No contact with any declared AVOID class for entire run: **+15 bonus**

### Contact Definition
- A contact is a clear nudge moving the cube ≥3 cm.
- Re-contacting the same cube does not add points.

---

## B) Model-Size Multiplier (applied once to Field Score)

- **Small:** × 1.05
- **Medium:** × 1.00
- **Large:** × 0.95

---

## C) mAP Bonus (max +15)

- Average mAP across the 3 classes × 15
- Rounded
- Cap at +15

---

# Penalties

- False contact (nudging a declared AVOID class or a decoy): **−15 each**
- Out of bounds (any part of robot crosses field edge):
  - First occurrence: **−10**
  - Subsequent occurrences: **−20 each**

---

# Tiebreakers (in order)

1. Fewer penalties
2. Higher average mAP
3. Smaller model family