# Playing Field Proposals — Version 1

> Four concrete field layouts with exact coordinates. Positions are fixed; class assignments rotate between rounds.

---

## Common Rules (All Layouts)

| Rule | Detail |
|------|--------|
| **Start position** | Any of the 4 corner zones (12×12 in / 30.48×30.48 cm) |
| **Start heading** | Team selects freely |
| **Corner selection** | Fixed per heat (referee draws before heat begins) |
| **Run length** | 120 seconds |
| **Object radius** | ~6 cm (for clearance calculations) |
| **Robot chassis** | 24.2 × 15.3 cm |
| **Contact (Rocket)** | Approach → nudge ≥3 cm → 180° turn |
| **Avoid (Tire)** | Approach to ~20 cm → pause → turn RIGHT |
| **Avoid (Tin Can)** | Approach to ~20 cm → pause → turn LEFT |
| **Wall detection** | Rangefinder <10 cm + no object → back up + turn |
| **Search pattern** | Spin → if nothing → drive forward ~10 cm → spin again |
| **Rescue** | Team may pick up robot → must place in a corner → penalty applied |

### Coordinate System

- Origin (0, 0) at the **bottom-left** corner of the field
- X-axis: runs left→right (0 to 254 cm / 100 in)
- Y-axis: runs bottom→top (0 to 142.24 cm / 56 in)

### Corner Zones (robot start areas — no objects allowed)

| Corner | X range (cm) | Y range (cm) |
|--------|-------------|-------------|
| Bottom-Left (BL) | 0 – 30.48 | 0 – 30.48 |
| Bottom-Right (BR) | 223.52 – 254 | 0 – 30.48 |
| Top-Left (TL) | 0 – 30.48 | 111.76 – 142.24 |
| Top-Right (TR) | 223.52 – 254 | 111.76 – 142.24 |

### Clearance Minimums

| Clearance | Minimum |
|-----------|---------|
| Object center → wall | 20 cm |
| Object center → object center | 35 cm |
| Object center → partition (if present) | 20 cm |
| Object center → corner zone edge | outside zone entirely |

---

## Layout 1: No Partition — 5 Objects

**Class breakdown:** 1 Rocket (contact) + 2 Tires (avoid) + 2 Tin Cans (avoid)

### Positions

| ID | X (in) | Y (in) | X (cm) | Y (cm) | Location |
|----|--------|--------|--------|--------|----------|
| P1 | 25 | 14 | 63.50 | 35.56 | Bottom-left quadrant |
| P2 | 75 | 14 | 190.50 | 35.56 | Bottom-right quadrant |
| P3 | 50 | 28 | 127.00 | 71.12 | Dead center |
| P4 | 25 | 42 | 63.50 | 106.68 | Top-left quadrant |
| P5 | 75 | 42 | 190.50 | 106.68 | Top-right quadrant |

### Diagram

```
  0       25       50       75      100 (in)
  |________|________|________|________|
  |                                    |  56
  | [TL]            P4      P5  [TR]  |
  |          ●               ●        |  42
  |                                    |
  |                                    |
  |                 P3                 |
  |                  ●                 |  28
  |                                    |
  |                                    |
  | [BL]    P1               P2  [BR] |
  |          ●               ●        |  14
  |____________________________________|  0
```

### Inter-Object Distance Matrix (cm)

|    | P1 | P2 | P3 | P4 | P5 |
|----|----|----|----|----|-----|
| P1 | — | 127.0 | 72.8 | 71.1 | 145.6 |
| P2 | 127.0 | — | 72.8 | 145.6 | 71.1 |
| P3 | 72.8 | 72.8 | — | 72.8 | 72.8 |
| P4 | 71.1 | 145.6 | 72.8 | — | 127.0 |
| P5 | 145.6 | 71.1 | 72.8 | 127.0 | — |

**Minimum inter-object distance: 71.1 cm** (P1↔P4 and P2↔P5) ✓

### Distance from Each Corner (cm)

| Corner | P1 | P2 | P3 | P4 | P5 |
|--------|----|----|----|----|-----|
| BL | **52** | 176 | 125 | 103 | 198 |
| BR | 176 | **52** | 125 | 198 | 103 |
| TL | 103 | 198 | 125 | **52** | 176 |
| TR | 198 | 103 | 125 | 176 | **52** |

**Observation:** Perfectly symmetric diamond. Every corner has the same profile: one object at ~52 cm (nearest), one at ~103 cm, one at ~125 cm (center), one at ~176 cm, one at ~198 cm (farthest). No corner has an advantage. Start corner doesn't affect fairness.

### Wall Clearances (cm)

| ID | Left wall | Right wall | Bottom wall | Top wall | Min |
|----|-----------|------------|-------------|----------|-----|
| P1 | 63.5 | 190.5 | 35.6 | 106.7 | 35.6 ✓ |
| P2 | 190.5 | 63.5 | 35.6 | 106.7 | 35.6 ✓ |
| P3 | 127.0 | 127.0 | 71.1 | 71.1 | 71.1 ✓ |
| P4 | 63.5 | 190.5 | 106.7 | 35.6 | 35.6 ✓ |
| P5 | 190.5 | 63.5 | 106.7 | 35.6 | 35.6 ✓ |

### Suggested Class Assignments (Rotation Templates)

| Template | P1 | P2 | P3 | P4 | P5 |
|----------|----|----|----|----|-----|
| A | Rocket | Tire | Tin Can | Tire | Tin Can |
| B | Tin Can | Rocket | Tire | Tin Can | Tire |
| C | Tire | Tin Can | Rocket | Tin Can | Tire |
| D | Tire | Tin Can | Tin Can | Rocket | Tire |

---

## Layout 2: No Partition — 6 Objects

**Class breakdown:** 2 Rockets (contact) + 2 Tires (avoid) + 2 Tin Cans (avoid)

### Positions

| ID | X (in) | Y (in) | X (cm) | Y (cm) | Location |
|----|--------|--------|--------|--------|----------|
| P1 | 22 | 16 | 55.88 | 40.64 | Bottom-left |
| P2 | 50 | 14 | 127.00 | 35.56 | Bottom-center |
| P3 | 78 | 16 | 198.12 | 40.64 | Bottom-right |
| P4 | 22 | 40 | 55.88 | 101.60 | Top-left |
| P5 | 50 | 42 | 127.00 | 106.68 | Top-center |
| P6 | 78 | 40 | 198.12 | 101.60 | Top-right |

### Diagram

```
  0       22       50       78      100 (in)
  |________|________|________|________|
  |                                    |  56
  | [TL]                        [TR]  |
  |        P4       P5       P6       |  40-42
  |         ●        ●        ●       |
  |                                    |
  |                                    |
  |        P1       P2       P3       |  14-16
  |         ●        ●        ●       |
  | [BL]                        [BR]  |
  |____________________________________|  0
```

### Inter-Object Distance Matrix (cm)

|    | P1 | P2 | P3 | P4 | P5 | P6 |
|----|----|----|----|----|----|----|
| P1 | — | 71.3 | 142.2 | 61.0 | 98.4 | 156.8 |
| P2 | 71.3 | — | 71.3 | 98.4 | 71.1 | 98.4 |
| P3 | 142.2 | 71.3 | — | 156.8 | 98.4 | 61.0 |
| P4 | 61.0 | 98.4 | 156.8 | — | 71.3 | 142.2 |
| P5 | 98.4 | 71.1 | 98.4 | 71.3 | — | 71.3 |
| P6 | 156.8 | 98.4 | 61.0 | 142.2 | 71.3 | — |

**Minimum inter-object distance: 61.0 cm** (P1↔P4 and P3↔P6) ✓

### Distance from Each Corner (cm)

| Corner | P1 | P2 | P3 | P4 | P5 | P6 |
|--------|----|----|----|----|----|----|
| BL | **47** | 113 | 184 | 95 | 140 | 201 |
| BR | 184 | 113 | **47** | 201 | 140 | 95 |
| TL | 95 | 140 | 201 | **47** | 113 | 184 |
| TR | 201 | 140 | 95 | 184 | 113 | **47** |

**Observation:** Symmetric. Each corner has: 1 object at ~47 cm, 1 at ~95 cm, 2 at ~113-140 cm, 1 at ~184 cm, 1 at ~201 cm. The staggered rows create a slight hexagonal pattern. Good spread.

### Wall Clearances (cm)

| ID | Left wall | Right wall | Bottom wall | Top wall | Min |
|----|-----------|------------|-------------|----------|-----|
| P1 | 55.9 | 198.1 | 40.6 | 101.6 | 40.6 ✓ |
| P2 | 127.0 | 127.0 | 35.6 | 106.7 | 35.6 ✓ |
| P3 | 198.1 | 55.9 | 40.6 | 101.6 | 40.6 ✓ |
| P4 | 55.9 | 198.1 | 101.6 | 40.6 | 40.6 ✓ |
| P5 | 127.0 | 127.0 | 106.7 | 35.6 | 35.6 ✓ |
| P6 | 198.1 | 55.9 | 101.6 | 40.6 | 40.6 ✓ |

### Suggested Class Assignments (Rotation Templates)

| Template | P1 | P2 | P3 | P4 | P5 | P6 |
|----------|----|----|----|----|----|----|
| A | Tire | Rocket | Tin Can | Tin Can | Rocket | Tire |
| B | Rocket | Tin Can | Tire | Rocket | Tire | Tin Can |
| C | Tin Can | Tire | Rocket | Tire | Tin Can | Rocket |

---

## Layout 3: With Partition — 5 Objects

**Class breakdown:** 1 Rocket (contact) + 2 Tires (avoid) + 2 Tin Cans (avoid)

### Partition Details

| Property | Value |
|----------|-------|
| Position | Horizontal at Y = 71.12 cm (28 in), centered on X |
| Span | X = 63.50 to X = 190.50 cm (25 to 75 in) |
| Left gap | X = 0 to 63.50 cm (25 in wide) |
| Right gap | X = 190.50 to 254 cm (25 in wide) |
| Height | Low PVC pipe — camera sees over it |

**Split: 3 objects on bottom half (zigzag), 2 objects on top half.**

### Positions

Objects are staggered in a **high-low-high zigzag** pattern: side objects sit closer to the partition, center objects sit closer to the outer wall. This prevents the robot from getting boxed in by a horizontal line of objects.

| ID | X (in) | Y (in) | X (cm) | Y (cm) | Location | Half |
|----|--------|--------|--------|--------|----------|------|
| P1 | 18 | 18 | 45.72 | 45.72 | Left gap lane, near partition | Bottom |
| P2 | 50 | 10 | 127.00 | 25.40 | Center, near bottom wall | Bottom |
| P3 | 82 | 18 | 208.28 | 45.72 | Right gap lane, near partition | Bottom |
| P4 | 33 | 38 | 83.82 | 96.52 | Behind partition, left | Top |
| P5 | 67 | 46 | 170.18 | 116.84 | Near top wall, right | Top |

### Diagram

```
  0    18   33       50    67   82   100 (in)
  |_____|____|________|_____|____|_____|
  |                                    |  56
  | [TL]                        [TR]  |
  |                        P5         |  46
  |                         ●         |
  |             P4                    |  38
  |              ●                    |
  |  gap  ┌──────────────────┐  gap   |  28  ← partition
  |       └──────────────────┘        |
  |     P1                     P3     |  18
  |      ●                      ●     |
  |                                    |
  | [BL]          P2            [BR]  |
  |                ●                   |  10
  |____________________________________|  0
```

### Inter-Object Distance Matrix (cm)

|    | P1 | P2 | P3 | P4 | P5 |
|----|----|----|----|----|-----|
| P1 | — | 84 | 163 | 64 | 143 |
| P2 | 84 | — | 84 | 83 | 101 |
| P3 | 163 | 84 | — | 134 | 81 |
| P4 | 64 | 83 | 134 | — | 89 |
| P5 | 143 | 101 | 81 | 89 | — |

**Minimum inter-object distance: 64 cm** (P1↔P4) ✓

### Distance from Each Corner (cm)

| Corner | P1 | P2 | P3 | P4 | P5 |
|--------|----|----|----|----|-----|
| BL | **43** | 112 | 195 | 106 | 185 |
| BR | 195 | 112 | **43** | 175 | 123 |
| TL | 87 | 151 | 210 | **75** | 155 |
| TR | 210 | 151 | 87 | **158** | 69 |

### Partition Clearances (cm)

| ID | Dist. to partition (Y) | Dist. to nearest wall | In gap lane? |
|----|------------------------|----------------------|--------------|
| P1 | 25.4 ✓ | 45.7 (left) ✓ | Yes (X < 63.5) |
| P2 | 45.7 ✓ | 25.4 (bottom) ✓ | N/A (under partition) |
| P3 | 25.4 ✓ | 45.7 (right) ✓ | Yes (X > 190.5) |
| P4 | 25.4 ✓ | 83.8 (left) ✓ | No (behind partition) |
| P5 | 45.7 ✓ | 25.4 (top) ✓ | No (behind partition) |

### Navigation Notes

The camera sees all 5 objects from any corner (low partition doesn't block vision). The partition only affects the driving path:

- **From bottom corners:** P1, P2, P3 are directly reachable. P4 and P5 require going around the partition via the left gap (X<63.5) or right gap (X>190.5).
- **From top corners:** P4 and P5 are directly reachable. P1, P2, P3 require going around.
- **Zigzag prevents trapping:** The robot always has a clear lane between the staggered objects — it won't get boxed against the partition or a wall.
- **Estimated detour per crossing:** ~5-10 seconds depending on robot's position relative to nearest gap.

### Suggested Class Assignments

#### Option A: "Dodge First" (robot starts on bottom half)

| Template | P1 | P2 | P3 | P4 | P5 |
|----------|----|----|----|----|-----|
| A1 | Tire | Tin Can | Tire | **Rocket** | Tin Can |
| A2 | Tin Can | Tire | Tin Can | **Rocket** | Tire |

*Bottom half = 3 avoid objects. Robot dodges them, then crosses partition to find the rocket.*

#### Option B: Balanced (any corner works equally)

| Template | P1 | P2 | P3 | P4 | P5 |
|----------|----|----|----|----|-----|
| B1 | **Rocket** | Tire | Tin Can | Tire | Tin Can |
| B2 | Tire | **Rocket** | Tin Can | Tire | Tin Can |

*Contact target on the start side. Robot engages the rocket early, then avoids the rest.*

#### Note on corner selection

Since positions are fixed and classes rotate, the referee can create a "dodge first" experience regardless of corner by assigning avoid objects to the start side and the rocket to the far side.

---

## Layout 4: With Partition — 6 Objects

**Class breakdown:** 2 Rockets (contact) + 2 Tires (avoid) + 2 Tin Cans (avoid)

### Positions

Same **high-low-high zigzag** as Layout 3, applied to both halves. Side objects near the partition, center objects near the outer walls.

| ID | X (in) | Y (in) | X (cm) | Y (cm) | Location | Half |
|----|--------|--------|--------|--------|----------|------|
| P1 | 18 | 18 | 45.72 | 45.72 | Left gap lane, near partition | Bottom |
| P2 | 50 | 10 | 127.00 | 25.40 | Center, near bottom wall | Bottom |
| P3 | 82 | 18 | 208.28 | 45.72 | Right gap lane, near partition | Bottom |
| P4 | 18 | 38 | 45.72 | 96.52 | Left gap lane, near partition | Top |
| P5 | 50 | 46 | 127.00 | 116.84 | Center, near top wall | Top |
| P6 | 82 | 38 | 208.28 | 96.52 | Right gap lane, near partition | Top |

### Diagram

```
  0    18           50           82   100 (in)
  |_____|____________|____________|_____|
  |                                    |  56
  | [TL]                        [TR]  |
  |                P5                  |  46
  |                 ●                  |
  |     P4                      P6    |  38
  |      ●                       ●    |
  |  gap  ┌──────────────────┐  gap   |  28  ← partition
  |       └──────────────────┘        |
  |     P1                      P3    |  18
  |      ●                       ●    |
  |                P2                  |  10
  |                 ●                  |
  | [BL]                        [BR]  |
  |____________________________________|  0
```

### Inter-Object Distance Matrix (cm)

|    | P1 | P2 | P3 | P4 | P5 | P6 |
|----|----|----|----|----|----|----|
| P1 | — | 84 | 163 | 51 | 108 | 170 |
| P2 | 84 | — | 84 | 108 | 91 | 108 |
| P3 | 163 | 84 | — | 170 | 108 | 51 |
| P4 | 51 | 108 | 170 | — | 84 | 163 |
| P5 | 108 | 91 | 108 | 84 | — | 84 |
| P6 | 170 | 108 | 51 | 163 | 84 | — |

**Minimum inter-object distance: 51 cm** (P1↔P4 and P3↔P6 — vertically paired in the gap lanes) ✓

### Distance from Each Corner (cm)

| Corner | P1 | P2 | P3 | P4 | P5 | P6 |
|--------|----|----|----|----|----|----|
| BL | **43** | 112 | 195 | 87 | 151 | 210 |
| BR | 195 | 112 | **43** | 210 | 151 | 87 |
| TL | 87 | 151 | 210 | **43** | 112 | 195 |
| TR | 210 | 151 | 87 | 195 | 112 | **43** |

**Observation:** Symmetric across all four corners. Each corner has: 1 object at ~43 cm, 1 at ~87 cm, 2 at ~112-151 cm, 1 at ~195 cm, 1 at ~210 cm.

### Partition Clearances (cm)

| ID | Dist. to partition (Y) | Dist. to nearest wall | In gap lane? |
|----|------------------------|----------------------|--------------|
| P1 | 25.4 ✓ | 45.7 (left) ✓ | Yes (X < 63.5) |
| P2 | 45.7 ✓ | 25.4 (bottom) ✓ | N/A (under partition) |
| P3 | 25.4 ✓ | 45.7 (right) ✓ | Yes (X > 190.5) |
| P4 | 25.4 ✓ | 45.7 (left) ✓ | Yes (X < 63.5) |
| P5 | 45.7 ✓ | 25.4 (top) ✓ | N/A (above partition) |
| P6 | 25.4 ✓ | 45.7 (right) ✓ | Yes (X > 190.5) |

### Navigation Notes

- **Zigzag prevents trapping:** On each half, the side objects are near the partition (Y=18/38) while the center object is near the outer wall (Y=10/46). The robot always has a clear path between them.
- **Gap lane pairs:** P1↔P4 (left gap) and P3↔P6 (right gap) are vertically paired at 51 cm apart — a robot crossing through a gap naturally encounters both.
- **Center objects** (P2, P5) are tucked near the outer walls, reachable by driving along the wall without crossing the partition.

### Suggested Class Assignments

#### Option A: "Dodge First" (robot starts on bottom half)

| Template | P1 | P2 | P3 | P4 | P5 | P6 |
|----------|----|----|----|----|----|----|
| A1 | Tire | Tin Can | Tin Can | **Rocket** | Tire | **Rocket** |
| A2 | Tin Can | Tire | Tire | **Rocket** | Tin Can | **Rocket** |

*Bottom = all avoid. Top = both rockets + 1 avoid. Robot must cross to score contact points.*

#### Option B: Balanced (1 of each type per half)

| Template | P1 | P2 | P3 | P4 | P5 | P6 |
|----------|----|----|----|----|----|----|
| B1 | **Rocket** | Tire | Tin Can | Tin Can | **Rocket** | Tire |
| B2 | Tire | **Rocket** | Tin Can | Tin Can | Tire | **Rocket** |
| B3 | Tin Can | Tire | **Rocket** | **Rocket** | Tin Can | Tire |

*Each half has 1 rocket + 1 tire + 1 can. Robot can score on either side without crossing.*

---

## Class Rotation Between Rounds

Positions (P1–P5 or P1–P6) are **physically fixed** for the entire event. Between heats, the referee changes which class goes on which position by selecting a different template from the tables above.

### How it works:

1. Before each heat, the referee selects a template (A1, B2, etc.)
2. The referee places the correct 3D-printed object on each position
3. All teams in that heat face the same template
4. Between heats, the referee swaps to a different template

This ensures:
- Positions are deterministic and consistent within a heat
- Different heats see different arrangements, adding variety
- No team gains an advantage from knowing positions (since main.py is provided and identical)

---

## Summary Comparison

| Property | Layout 1 | Layout 2 | Layout 3 | Layout 4 |
|----------|----------|----------|----------|----------|
| Partition | No | No | Yes | Yes |
| Objects | 5 | 6 | 5 | 6 |
| Classes | 1R+2T+2C | 2R+2T+2C | 1R+2T+2C | 2R+2T+2C |
| Pattern | Diamond+center | Staggered 2×3 | Zigzag 3+2 | Zigzag 3+3 |
| Min object spacing | 71.1 cm | 61.0 cm | 64 cm | 51 cm |
| Min wall clearance | 35.6 cm | 35.6 cm | 25.4 cm | 25.4 cm |
| Min partition clearance | N/A | N/A | 25.4 cm | 25.4 cm |
| Symmetry | All corners equal | All corners equal | Bottom-heavy | All corners equal |
| Corner advantage | None | None | Minor (bottom has 3 objects) | None |
