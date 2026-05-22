# Playing Field Brainstorm — Orbit Odyssey CV Challenge

> Working document. No ideas are final — everything here is on the table for discussion.

---

## Established Constraints

| Constraint | Value |
|-----------|-------|
| Arena dimensions | 272.54 × 152.78 cm (~9 ft × 5 ft) |
| Walls | Low-profile pipe barriers on all four sides |
| Central partition | Removable. If used: wall at midpoint (X=136.27 cm), gap of 28.32 cm at one end |
| Camera | Mounted on robot (AIxBoard) — moves with robot |
| Robot width | <20 cm — fits easily through gap |
| main.py | Fully provided to students, will be adapted to final game design |
| Objects | 3D-printed tin cans, wheels, and rockets |
| Training data | Students photograph the actual competition objects |
| Classes | Rocket = contact, Tire = avoid, Tin can = avoid |
| Run length | 120 seconds |

---

## Part 1: Game Concepts (The Big Picture)

### Concept A: Open Arena (no partition)

Remove the partition entirely. The full 272 × 152 cm field is open. Objects are placed according to templates. The robot starts in a corner, spins, hunts, and engages objects across the entire field.

**Pros:**
- Simplest to implement and referee
- Maximum visibility for the robot camera — no blind spots
- Objects at varying distances test model detection range
- Current main.py logic (spin → detect → center → engage) works naturally
- Easy for spectators to follow the action

**Cons:**
- Might feel too easy — robot could find everything quickly by spinning
- Less "arena" feel, more like an empty room
- Doesn't use the unique feature of the existing field infrastructure
- Less dramatic than a two-room scenario

**Best for:** Maximizing the ML challenge (model quality is the differentiator). Simple, reliable, fair.

---

### Concept B: Half-Court (partition as boundary, one side only)

Keep the partition but only use one half (~136 × 152 cm). All objects in one half. The partition and outer walls form a contained arena.

**Pros:**
- Compact space creates more frequent object encounters
- No gap navigation needed
- Feels like a defined arena, not just "a room with stuff in it"
- Robot can't wander too far — easier to keep the action tight

**Cons:**
- Small space (~2 m²) — objects might be very close together
- Robot might detect multiple objects simultaneously, creating confusion
- Less room for strategic object placement
- Might feel cramped for spectators

**Best for:** Quick, action-packed runs with frequent detections. Good if we want short, intense games.

---

### Concept C: Two-Room Quest (full partition, gap navigation)

Embrace the partition. The avoid objects (tire, tin can) are in the start room. The rocket (contact target) is in the far room, accessible only through the 28 cm gap. The narrative comes alive: navigate the debris field to reach the rescue rocket.

**Pros:**
- Narratively perfect — debris blocks the path to the rescue rocket
- Most dramatic for spectators ("Will it make it through the gap?")
- Tests both detection AND navigation
- The gap creates a natural tension point
- Uses the arena's unique feature
- Creates a clear "quest" structure: clear debris room → navigate gap → find rocket

**Cons:**
- Requires gap navigation logic in main.py (extra development)
- Risk of robot getting stuck in the gap = boring dead time
- If ALL robots fail at the gap, the partition is just frustrating
- Since main.py is the same for everyone, gap navigation doesn't differentiate teams
- Camera (on robot) can't see through the wall — robot needs a strategy to FIND the gap

**Best for:** Maximum drama and narrative immersion. Best spectator experience IF the gap navigation works reliably.

---

### Concept D: Partition as Obstacle (objects on start side, wall blocks vision)

Keep the partition but place all objects on the start side. The partition wall creates natural vision-blocking: the camera can't see objects that are behind the wall from certain angles. The robot must physically move around the field to discover objects it couldn't see from the start position.

**Pros:**
- Adds exploration without requiring gap navigation
- Creates "discovery moments" as the robot rounds the wall
- The partition is a physical obstacle to drive around, not through
- Still simple for main.py — no gap logic needed, just spin-and-search
- Objects near the wall create interesting detection angles

**Cons:**
- If objects are far from the wall, the partition barely matters
- Might not feel purposeful — "why is there a wall?"
- Less dramatic than the two-room concept

**Best for:** A middle ground — adds physical complexity without the risk of gap navigation failure.

---

### Concept E: Progressive Difficulty (multiple rounds)

Offer 2-3 rounds with increasing difficulty. Each team runs the same main.py but faces different layouts:
- **Round 1:** Open half, all objects visible from start (easy)
- **Round 2:** Objects partially hidden by partition (medium)
- **Round 3:** Rocket in far room, requires gap navigation (hard)

Higher difficulty rounds have a score multiplier (e.g., ×1.0, ×1.2, ×1.5). Teams can choose which round(s) to attempt.

**Pros:**
- Teams pick their comfort level
- Creates natural escalation and excitement
- Tests model robustness across different scenarios
- Rewards bold teams without punishing cautious ones

**Cons:**
- Complex to manage (referee must reset field between rounds)
- More time per team = fewer teams can compete
- main.py might need mode selection logic
- Might dilute the "one decisive run" drama

**Best for:** Longer events with fewer teams where you want to maximize the experience per team.

---

## Part 2: Answering the Open Questions

For each question, ideas are given for **both** partition scenarios.

---

### Q1: Where should the robot start?

#### Without partition (Open Arena):
| Idea | Description | Trade-off |
|------|------------|-----------|
| **Random corner** | Referee draws one of four corners before each run | Adds variety; robot must search in all directions |
| **Fixed corner** | Same corner for all teams in a heat | Most fair — identical conditions |
| **Short-wall center** | Center of one 152 cm wall, facing down the length | Best initial camera view — longest sight line |
| **"Launch pad" zone** | Marked rectangle (e.g., 30×30 cm) near a corner | Gives team some freedom within a zone |

#### With partition (Two-Room):
| Idea | Description | Trade-off |
|------|------------|-----------|
| **Far corner from gap** | Corner diagonally opposite the gap | Maximum challenge — robot must traverse entire start room + find gap |
| **Near the gap** | Start near the transit lane opening | Easier gap navigation; robot can go either way quickly |
| **Center of start half** | Middle of the start room | Balanced: equal distance to objects and to gap |
| **Against the partition wall** | Facing into the start room | Robot naturally searches start room first |

**My lean:** Fixed corner for all teams in a heat (fairest). Without partition, any corner works. With partition, the far corner from the gap creates the most interesting journey.

---

### Q2: How should the robot be positioned at the starting point?

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Team selects heading** | Team places robot facing any direction they choose | Small strategic element, zero implementation cost |
| **Fixed heading (facing center)** | All robots face the center of the field | Standardized, no strategic variance |
| **Fixed heading (facing nearest wall)** | Robot faces a wall, must turn around first | Adds ~2-3 seconds to find first object — unnecessary penalty |
| **Random heading** | Referee spins a pointer | Adds chaos, feels unfair |

**My lean:** Team selects heading. It's the only decision students make on game day (since they don't write main.py), and it gives them a moment of agency. A smart team that thinks about where objects will likely be can gain a small edge.

---

### Q3: How many objects will we place?

| Idea | Objects | Rationale |
|------|---------|-----------|
| **3 total** (one per class) | 1 rocket + 1 tire + 1 can | Clean, simple, each detection matters. No confusion. |
| **3 + 1-2 decoys** | 3 real + blank/different cubes | Tests false positive resistance. Model must distinguish real objects from similar-looking decoys. |
| **5 total** (duplicates) | 1 rocket + 2 tires + 2 cans | More interactions. Robot has more chances to score/lose points. More action for spectators. |
| **6 total** (2 per class) | 2 rockets + 2 tires + 2 cans | Symmetric. Every class appears twice. Higher scoring ceiling. |

**My lean:** **3 objects (one per class)**, no decoys. Here's why:
- Students are photographing 3D-printed objects they've handled. Their models should be accurate on these specific objects.
- Decoys require extra 3D prints and add logistics overhead.
- With only 120 seconds and 3 objects, each detection is meaningful. 
- "Find and correctly engage all 3 in 120 seconds" is a clean, understandable objective.
- If we add more later, we can always scale up. Harder to scale down.

---

### Q4: Where should we place the objects?

#### Without partition (Open Arena):

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Template zones** (A/B/C) | 3 pre-published templates, each defining 3 zones. Referee draws one per heat. | Predictable, fair, teams can study templates beforehand. |
| **Distance tiers** | One near start (~50 cm), one mid-field (~130 cm), one far (~220 cm) | Tests detection at varying ranges — directly rewards better models |
| **Triangular spread** | Objects form an equilateral triangle across the field | No object is "closest" — robot must commit to a direction |
| **Clustered** | All objects within ~80 cm of each other | Tests differentiation — can the model tell them apart when close together? |
| **Wall-hugging** | Objects placed near walls (20-30 cm from edge) | Tests detection at tight angles, robot must approach carefully |

#### With partition (Two-Room):

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Debris + Rescue** | Avoid objects in start room, rocket in far room | Narrative-perfect. Forces gap navigation to win. |
| **Gatekeeper** | One avoid object placed near the gap entrance | Robot must detect and avoid it before navigating the gap |
| **All start-side** | 3 objects in start room only, partition is just a boundary | Simple, uses the arena shape without requiring gap navigation |
| **Split** | 1 object in start room, 2 in far room (or vice versa) | Forces exploration of both rooms |

**My lean:** 
- Without partition: **Distance tiers**. Places objects at near/mid/far ranges, directly testing model detection quality at different distances. Simple to set up, clear rationale.
- With partition: **Debris + Rescue** (avoid objects in start room, rocket through gap). Narratively compelling and creates a natural game arc.

---

### Q5: Do we want to change the position of the objects between each round?

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Same layout for all teams in a heat** | Referee sets layout once per heat, all teams run it | Most fair — identical conditions. Teams can't gain advantage by watching earlier runs (if they don't see them). |
| **Different template per heat** | 3 templates, rotated across heats | Variety across heats, fairness within a heat. |
| **Randomized each run** | Referee rolls dice for placement | Maximum unpredictability, but harder to compare teams fairly |
| **Fixed for entire event** | One layout, all day | Simplest for referees. Risk: later teams might gain intel from spectating. |

**My lean:** **Same layout within a heat, different template between heats.** Fair comparison within each group. Variety across the event. Referee draws template before each heat begins.

**Important consideration:** If teams are watching each other's runs, they could learn object positions. Options to prevent this:
- Teams wait in a separate area and only enter the field for their run
- Or: accept it — knowing where objects are doesn't help if main.py is provided and identical

Actually, since main.py is provided and identical for all teams, knowing object positions gives zero advantage. The robot behaves the same regardless. So this concern is moot — we can let teams watch.

---

### Q6: What should the robot do if it encounters a wall?

| Idea | Description | Implementation complexity |
|------|------------|--------------------------|
| **Nothing special — walls are physical barriers** | Robot bumps, wheels spin against the wall, eventually turns away | Zero. Current behavior. Might look stuck. |
| **Rangefinder wall detection** | If rangefinder reads <10 cm but camera sees no object → it's a wall. Back up + turn. | Low. Few lines in main.py. |
| **Motor stall detection** | If wheels are spinning but robot isn't moving (encoders show no progress) → back up + turn | Medium. Requires encoder monitoring. |
| **Timed wall escape** | If no new object detected for X seconds while driving → back up + random turn | Low. Simple timer in main.py. |
| **Penalty for being stuck** | -5 pts if robot is in contact with a wall for >5 consecutive seconds | Medium (referee judgment). Discourages bad code. BUT main.py is provided, so students can't fix it — unfair to penalize. |

**My lean:** **Rangefinder wall detection** — the rangefinder is already on the robot and already used in the contact logic. Add a simple check: "if very close to something but camera sees nothing recognizable, it's a wall — reverse and turn." Clean, elegant, and prevents the robot from looking stuck.

**With partition:** Same logic applies at the partition wall. If the robot reaches the partition, it detects "close obstacle, no object" and turns away. For gap navigation (if we use the two-room concept), we'd need additional logic to FIND the gap — perhaps driving along the wall until the rangefinder reading suddenly jumps (indicating the opening).

---

### Q7: What should the robot do for each type of object?

#### Contact behavior (Rocket):

| Idea | Description | Spectacle factor |
|------|------------|-----------------|
| **Drive + nudge + reverse** | Drive to rocket, push it ≥3 cm, back up | Standard. Clear. Easy to judge. |
| **Drive + orbit** | Drive to rocket, circle around it, then nudge | Flashy but complex. Overkill. |
| **Drive + stop + honk** | Drive to rocket, stop within 5 cm, play a sound/flash LED | Non-contact alternative. Harder to judge "close enough." |

#### Avoid behavior (Tire and Tin can):

| Idea | Description | Pro/Con |
|------|------------|---------|
| **Turn away immediately** | Detect avoid-class → DON'T approach → turn 90° away → resume search | Logical. Safe. But boring — spectators see robot turning away from objects for no visible reason. |
| **Approach + stop + turn away** | Drive to ~20 cm of object, pause, then turn 90° and resume search | More dramatic — robot "sees" the danger, hesitates, retreats. Visually clearer to spectators. |
| **Approach + turn LEFT (tin can) / RIGHT (tire)** | Different avoid direction per class | Proves the model actually distinguished the two avoid classes, not just "avoid vs. contact." More educational. |
| **Scan and skip** | Detect, acknowledge (brief pause), continue spinning without approaching | Fastest. Robot wastes no time. But hard for spectators to see what happened. |
| **Drive to safe distance + scan around it** | Drive to ~30 cm, slow down, drive around the object, continue | Looks like the robot is "inspecting" the debris. Cool but complex to implement. |

**My lean:** **Approach to ~20cm, pause briefly, then turn away.** Here's the reasoning:
- Spectators can SEE the robot reacting to the object (it drove close, then retreated)
- The pause makes it visually clear the robot "decided" this was an avoid object
- Driving toward it uses the rangefinder naturally (confirms distance)
- The retreat direction doesn't need to differ per class (keeps code simple)

**Alternative strong idea:** Different avoid directions (left for can, right for tire). This proves the model distinguished between the two avoid classes. It's more educational and testable — if the robot turns the wrong way, it means the model confused the classes.

---

### Q8: How should we handle when a robot gets lost?

| Idea | Description | Trade-off |
|------|------------|-----------|
| **Search timeout** | If no object detected after X seconds of spinning, drive forward ~30 cm and spin again | Prevents infinite loops. Robot self-recovers. Low spectator drama. |
| **Progressive spiral** | Spin → drive forward → spin → drive further → repeat with increasing radius | Covers more ground each cycle. Could drive off into a wall. |
| **One free rescue** | Referee picks up robot, places it back at start. First rescue is free, subsequent rescues incur -15 pts each. | Keeps runs alive. Feels fair — one "oops" is forgiven. |
| **Hard time limit per object** | Robot has 40 seconds per object. If not found, it's skipped and the run moves on. | Prevents entire runs from being wasted on one missing object. But requires tracking per-object time. |
| **Emergency recall** | After 90 seconds, if <2 objects engaged, robot enters "desperation mode" — faster spin, lower detection threshold | Creates late-game drama. Complex to implement. |
| **Run just ends** | No rescue. 120 seconds is 120 seconds. If the robot finds nothing, the team scores 0 on field performance. | Simplest. Harsh but fair — the model either works or it doesn't. |

**My lean:** **Search timeout + one free rescue.**
- The search timeout (built into main.py) handles the common case: robot just hasn't found anything yet, needs to reposition.
- The one free rescue handles the rare case: robot is physically stuck against a wall or in a corner. Referee can quickly reposition it.
- Subsequent rescues cost -15 pts — incentivizes reliability without destroying a team's run on a fluke.

---

## Part 3: Physical Object Considerations

Since objects will be **3D-printed representations**, some practical considerations:

### Size
- Objects should be large enough to detect from across the field (~2.5 m away)
- Suggested minimum: **8-10 cm tall, 6-8 cm wide**
- All three objects should be approximately the same footprint (fairness — one class shouldn't be easier to detect just because it's bigger)
- Need to be heavy enough that the robot's nudge moves them exactly ≥3 cm, not sends them flying across the field
- Consider adding a weighted base or filling with sand

### Printing
- Print in a color that contrasts with the field surface (if the field is light-colored, print dark, and vice versa)
- Consider painting for more realistic appearance — helps models generalize and looks better for spectators
- Each object should be visually distinct even to a human from 2+ meters

### Orientation
- 3D objects don't have "faces" like cubes — they look different from every angle
- This is GOOD for the ML challenge: models must generalize across viewing angles
- Consider: should we fix object orientation (e.g., rocket always points up) or randomize it (rocket could be on its side)?
- **Recommendation:** Fix orientation for consistency. A rocket lying on its side looks nothing like a standing rocket, and that's a detection failure caused by the setup, not the model.

### Training Data Collection
- Students photograph the actual competition objects from many angles
- Suggest providing a photo-taking protocol: turntable, multiple heights, various backgrounds, various lighting
- The number and quality of training photos will directly affect model performance — this IS the student-controlled variable (along with hyperparameters)

---

## Part 4: Scoring Considerations (implications of field design)

The existing scoring system (from Game_Overview_and_Scoring.md) was designed for an open field with zones and decoys. Depending on which concept we choose, some adjustments may be needed:

### If Open Arena (no partition):
- Current scoring works almost as-is
- May want to simplify: remove hazard zones and decoys for the first iteration
- Consider adding a **time bonus**: completing all objectives in under 60 seconds earns extra points (rewards model speed)

### If Two-Room Quest (with partition):
- Consider a **room-clearing bonus**: +10 pts if robot correctly handles all objects in the start room before navigating to the far room
- **Gap navigation bonus**: +10 pts for successfully passing through the gap (rewards the hardest part)
- Rocket contact is worth MORE here because it requires gap navigation (+40 instead of +30?)

### Regardless of concept:
- **mAP bonus and model-size multiplier remain** — these reward model quality directly
- **False contact penalty remains** — nudging an avoid object = -15 pts
- Consider: should we penalize "no action"? If the robot detects an avoid object but does nothing (no approach, no turn), is that okay or should it demonstrate avoidance?

---

## Part 5: What I'd Recommend (for discussion)

**If forced to pick today, I'd go with Open Arena (Concept A)** with these specifics:

1. **No partition** — simpler, more reliable, spectators can see everything
2. **3 objects, one per class** — clean and decisive
3. **Distance-tier placement** — near/mid/far from start, testing model range
4. **Corner start, team picks heading** — fair with a dash of strategy
5. **Rangefinder wall detection** — prevents stuck robots
6. **Approach-then-retreat avoidance** — visually clear to spectators
7. **Search timeout + one free rescue** — keeps runs alive
8. **Same layout per heat** — fair comparison

**BUT — if the team wants to use the partition** (and I could see why — it's a cool piece of infrastructure), I'd go with the Two-Room Quest (Concept C):

1. **Partition with gap** — debris room + rescue room
2. **Avoid objects in start room, rocket through the gap**
3. **Start at far corner from gap** — maximum journey
4. **Gap navigation via wall-following + rangefinder gap detection**
5. **Room-clearing bonus + gap navigation bonus** in scoring
6. **Two free rescues** (because more things can go wrong)

Both are viable. The partition version is more dramatic but riskier. The open version is more reliable but less spectacular.

---

## Open Items Still To Decide
- [ ] Partition: use it or not?
- [ ] Physical object format: size, weight, color, orientation rules
- [ ] Placement templates: how many, exact coordinates
- [ ] Exact scoring adjustments based on field design
- [ ] Field surface: color/material (affects 3D-print color choice)
- [ ] Do we need field markings (start zone, object zones)?
