# Playing Field Brainstorm — Orbit Odyssey CV Challenge

> Working document. No ideas are final — everything here is on the table for discussion.

---

## Established Constraints

| Constraint | Value |
|-----------|-------|
| Arena dimensions | 254 × 142.24 cm (100 × 56 in) |
| Walls | Low-profile PVC pipe barriers on all four sides |
| Corner zones | 12 × 12 in (30.48 × 30.48 cm) at each corner |
| Central partition | 127 cm (50 in) long, runs horizontally, centered on both axes |
| Partition height | Same as perimeter walls — low PVC pipe. **Camera can see over it.** |
| Gaps | Two symmetric 63.5 cm (25 in) openings, one at each end of the partition |
| Camera | Mounted on robot (AIxBoard) — sits above pipe height, can see the entire field |
| Robot width | <20 cm — fits through gaps very easily |
| main.py | Fully provided to students, will be adapted to final game design |
| Objects | 3D-printed tin cans, wheels, and rockets |
| Training data | Students photograph the actual competition objects |
| Classes | Rocket = contact, Tire = avoid, Tin can = avoid |
| Run length | 120 seconds |

### Arena Layout (top-down)

```
 ← ————————————— 100 in ————————————— →

 ┌──────────────────────────────────────────────┐  ↑
 │  [corner]                        [corner]    │  |
 │                                              │  |
 │         ┌──────────────────┐                 │  28 in
 │  25 in  │  PARTITION 50 in │   25 in         │  TOP HALF
 │  GAP    │  (low PVC pipe)  │   GAP           │  |
 │         └──────────────────┘                 │  |
 │                                              │  28 in
 │  [corner]                        [corner]    │  BOTTOM HALF
 │                                              │  |
 └──────────────────────────────────────────────┘  ↓
                    56 in
```

### Key Facts About the Partition

The partition is a low PVC pipe — same height as the perimeter walls. This means:
- **Does NOT block the camera's view** — the camera sits above pipe height and can see the entire field from any position
- **Does NOT restrict the robot to one half** — 63.5 cm gaps on both sides allow free traversal
- **DOES block the robot from driving straight through the center** — it must go around via one of the gaps
- **Net effect:** a physical detour of ~5-10 seconds when the robot needs to reach the other half. Does not change the detection problem at all.

The partition's impact is **navigational, not visual**. Since main.py is provided to all teams, the navigation is identical for everyone. The partition affects all teams equally and does not differentiate based on model quality.

---

## Part 1: Game Concepts

### Concept A: Open Arena (partition removed)

Remove the partition. Full 254 × 142 cm field is open.

**Pros:**
- Simplest to implement and referee
- Full visibility — robot can detect and drive to any object directly
- No wasted time on detours — 120 seconds is spent entirely on detection and engagement
- The challenge is purely about ML model quality
- Easy for spectators to follow
- Easy for referees to judge

**Cons:**
- Doesn't use the partition (team may want to keep it)
- Might feel too simple as an arena
- Robot could potentially find everything with one spin from the start position

**Best for:** A clean, pure CV challenge where model quality is the sole differentiator.

---

### Concept B: Low Partition (kept as-is)

Keep the partition. The robot sees everything but must drive around it to reach objects on the other half.

**Pros:**
- Uses existing infrastructure — no need to ask the team to remove it
- Adds a minor navigation element (driving around the partition)
- Objects behind the partition require the robot to commit to a gap (left or right)
- The arena looks more interesting than an empty rectangle
- The partition creates a natural reference point for placement templates

**Cons:**
- The partition doesn't affect the detection problem — camera sees over it
- The navigation detour is identical for all teams (main.py is provided)
- If the robot bumps into the partition, it triggers wall-avoidance and wastes time — but this isn't skill-based since students don't write the navigation code
- Could confuse spectators who expect the wall to block vision

**Best for:** Keeping the team happy with the existing field setup while accepting that the partition's impact is minor.

---

### How to make the partition matter more (within Concept B):

Since the partition can't block vision, we need other ways to make it relevant:

| Idea | Description | Does it work? |
|------|------------|---------------|
| **Objects placed directly behind partition** | Robot sees the object but must drive around to reach it | Yes — adds time pressure. Robot must choose left or right gap. |
| **Objects placed IN the gaps** | Object blocks a transit path, forcing robot to use the other gap or approach carefully | Yes — creates decision points. But gap is 63.5 cm, object is ~8 cm. Doesn't really block the gap. |
| **Start on one side, contact target on the other** | Robot must cross at least once | Yes — guarantees the partition creates a detour. But the detour is the same for all teams. |
| **Time bonus for efficiency** | Extra points for finishing fast — rewards teams whose models detect quickly, reducing time lost to detours | Yes — indirectly makes the partition meaningful because wasted navigation time costs points. |

**The honest assessment:** With a low partition that the camera sees over, the difference between "partition in" and "partition out" is about 5-10 seconds of robot travel time per crossing. In a 120-second run, this is noticeable but not game-changing. Both scenarios work. The real challenge — training a model that accurately detects and classifies 3D-printed objects — is identical in both.

---

## Part 2: Answering the Open Questions

Answers apply to **both** scenarios unless noted.

---

### Q1: Where should the robot start?

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Corner zone** | Use the existing 12 × 12 in corner markings | Natural fit. Consistent. |
| **Random corner** | Referee draws one of four corners per run | Adds variety. Robot must search in all directions. |
| **Fixed corner per heat** | Same corner for all teams in a heat | Most fair — identical starting conditions. |
| **Short-wall center** | Center of one 142 cm wall | Longest initial sight line. But no existing marking. |

**With partition note:** All four corners work equally. The robot can see the whole field regardless of which corner it starts in. The corner choice only affects which gap is closer if the robot needs to cross.

**My lean:** **Fixed corner per heat**, using the existing 12 × 12 in corner zone markings. Fairest option, zero setup needed.

---

### Q2: How should the robot be positioned at the starting point?

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Team selects heading** | Team places robot facing any direction | Small strategic element, zero cost |
| **Fixed heading (facing center)** | All robots face center | Standardized |
| **Random heading** | Referee decides | Feels unfair |

**My lean:** **Team selects heading.** Only decision students make on game day. A team that thinks about object placement can gain a small edge by pointing the camera toward the most likely object location.

---

### Q3: How many objects will we place?

| Idea | Objects | Rationale |
|------|---------|-----------|
| **3 total** (one per class) | 1 rocket + 1 tire + 1 can | Clean. Each detection is decisive. |
| **3 + decoys** | 3 real + 1-2 blank objects | Tests false positive resistance. |
| **5 total** (duplicates) | 1 rocket + 2 tires + 2 cans | More action. More scoring opportunities. |
| **6 total** (2 per class) | 2 of each | Symmetric. Highest scoring ceiling. |

**My lean:** **3 objects, one per class.** Simple objective: find and correctly engage all 3 in 120 seconds. Every detection matters. Can scale up later.

---

### Q4: Where should we place the objects?

#### Without partition:

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Distance tiers** | Near (~50 cm), mid (~130 cm), far (~220 cm) from start | Tests model at varying ranges |
| **Triangular spread** | Objects form a wide triangle | No object is "closest" — robot must commit |
| **Template zones** (A/B/C) | Pre-published templates, referee draws one | Predictable, fair, studyable |
| **Wall-adjacent** | Objects 20-30 cm from walls | Tests detection at tight angles |

#### With partition:

All of the above, plus:

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Split across halves** | At least 1 object on each side of the partition | Guarantees robot must cross at least once |
| **Contact target on far side** | Rocket across the partition from start | Creates a journey — dodge avoid objects first, then cross for the target |
| **All on start side** | Everything on one half | Partition becomes irrelevant — might as well remove it |
| **One in each gap lane** | Objects placed in the 63.5 cm gap areas | Robot encounters them while crossing |

**My lean:**
- Without partition: **Distance tiers** — directly tests detection quality at range.
- With partition: **Split across halves** with the rocket on the far side. Guarantees the partition matters (robot must cross at least once). Creates a natural game arc.

---

### Q5: Do we want to change the position of the objects between each round?

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Same layout within a heat** | All teams in a heat face the same layout | Most fair comparison |
| **Different template per heat** | 3 templates, rotated | Variety across event, fairness within heats |
| **Randomized each run** | Referee randomizes per team | Unpredictable, harder to compare |
| **Fixed all day** | One layout, entire event | Simplest. No risk of unfairness. |

**My lean:** **Same layout within a heat, different template between heats.** Since main.py is provided and identical for all teams, knowing object positions gives zero advantage. Teams can watch each other's runs.

---

### Q6: What should the robot do if it encounters a wall or the partition?

| Idea | Description | Complexity |
|------|------------|------------|
| **Rangefinder wall detection** | Rangefinder reads <10 cm but camera sees no recognized object → wall. Back up + turn. | Low |
| **Motor stall detection** | Wheels spinning, no encoder progress → back up + turn | Medium |
| **Timed escape** | No new detection for X seconds while driving → back up + random turn | Low |

**With partition:** Same logic. Robot approaches partition, rangefinder triggers, robot backs up and turns. Through normal search behavior, it will eventually head toward a gap. The 63.5 cm gaps are wide enough that the robot will find them without special logic.

**My lean:** **Rangefinder wall detection.** The rangefinder is already on the robot. Simple, elegant, works on both perimeter walls and the partition.

---

### Q7: What should the robot do for each type of object?

#### Contact (Rocket):
**Drive to it, nudge it ≥3 cm, reverse.** Standard. Clear. Easy to judge.

#### Avoid (Tire and Tin can):

| Idea | Description | Trade-off |
|------|------------|---------|
| **Turn away immediately** | Detect → turn 90° → resume search | Safe but boring for spectators |
| **Approach + stop + turn away** | Drive to ~20 cm, pause, turn away | Dramatic — robot "sees" danger and retreats |
| **Different direction per class** | Left for can, right for tire | Proves model distinguished both avoid classes |
| **Scan and skip** | Detect, brief pause, continue spinning | Fast but invisible to spectators |

**My lean:** **Approach to ~20 cm, pause briefly, then turn away.** Visually clear to spectators. The pause makes the "decision" visible.

**Strong alternative:** Different avoid directions per class. Educational — proves the model can tell tin can from tire. If the robot turns the wrong way, spectators see the misclassification in real time.

---

### Q8: How should we handle when a robot gets lost?

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Search timeout** | No detection after X seconds → drive forward + spin again | Self-recovery. Built into main.py. |
| **One free rescue** | Referee repositions robot. First is free, subsequent = -15 pts. | Keeps runs alive. |
| **Run just ends** | 120 seconds is 120 seconds. No rescue. | Simplest. Harsh. |

**My lean:** **Search timeout + one free rescue.** The timeout handles "robot hasn't found anything yet." The rescue handles "robot is physically stuck." Subsequent rescues cost -15 pts.

---

## Part 3: Physical Object Considerations

### Size
- Must be detectable from across the field (~250 cm away)
- Suggested minimum: **8-10 cm tall, 6-8 cm wide**
- All three should have similar footprints (fairness)
- Heavy enough for a ≥3 cm nudge, not so light they fly across the field
- Consider weighted base or sand filling

### Printing and Appearance
- Color that contrasts with the field surface
- Visually distinct to a human from 2+ meters
- Consider painting for realism

### Orientation
- Fix orientation for consistency (rocket upright, tire flat, can standing)
- A rocket lying on its side is a setup problem, not a model quality problem

### Training Data
- Students photograph the actual competition objects
- Suggest a protocol: turntable, multiple heights, various backgrounds and lighting
- Photo quantity/quality is the primary student-controlled variable alongside hyperparameters

---

## Part 4: Scoring Considerations

### Current system (from Game_Overview_and_Scoring.md):
```
Total = (Field Score × Model-Size Multiplier) + mAP Bonus − Penalties
```

This system works for both scenarios with minor adjustments.

### Possible additions:

| Bonus/Penalty | Open Arena | With Partition |
|--------------|------------|----------------|
| Time bonus (finish under 60s) | Worth considering — rewards fast, accurate models | Less fair — partition adds unavoidable travel time |
| All-contact bonus (+15) | Keep | Keep |
| Clean-avoid bonus (+15) | Keep | Keep |
| False contact penalty (-15) | Keep | Keep |
| Out-of-bounds penalty | Keep | Keep |
| Rescue penalty (-15 after first) | Add | Add |

### Partition-specific consideration:
No special "crossing bonus" needed. The partition only adds a few seconds of travel time. It doesn't warrant its own scoring category.

---

## Part 5: Recommendations (for discussion)

### If partition is removed (Open Arena):

1. 3 objects, one per class
2. Distance-tier placement (near/mid/far from start)
3. Start in corner zone, team picks heading
4. Rangefinder wall detection
5. Approach-then-retreat avoidance
6. Search timeout + one free rescue
7. Same layout per heat

**Character:** Clean, fair, purely about model quality. The simplest possible game that still creates drama.

### If partition stays (Low Partition):

Same as above, plus:
1. Split objects across both halves (rocket on far side)
2. Rangefinder handles partition collisions naturally
3. No special crossing or gap bonuses

**Character:** Nearly identical to open arena, with a minor navigation element. The partition adds ~5-10 seconds of travel time per crossing but doesn't change the detection challenge.

### Bottom line:

The challenge is fundamentally the same with or without the low partition. The real differentiator between teams is **model quality** — can their trained YOLOv11 accurately detect and classify the 3D-printed objects at various distances and angles? Everything else (navigation, wall avoidance, object engagement) is handled by the provided main.py and is identical for all teams.

The partition decision is more about aesthetics and team preference than gameplay impact.

---

## Open Items Still To Decide
- [ ] Partition: keep or remove? (Low impact either way — team preference)
- [ ] Physical object format: size, weight, color, orientation rules
- [ ] Placement templates: how many, exact coordinates
- [ ] Exact scoring adjustments
- [ ] Field surface: color/material (affects 3D-print color choice)
- [ ] Do we need field markings (start zone, object zones)?
