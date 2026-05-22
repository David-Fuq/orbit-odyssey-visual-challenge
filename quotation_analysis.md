# Quotation Analysis: Orbit Odyssey — Viability Deep Dive

> **For:** David Alejandro Fuquen (internal decision-making)  
> **Date:** 2026-05-17  
> **Verdict:** Feasible but tight. The CETC integration is the make-or-break variable.

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Available hours (3 weeks × 10-15 hrs/wk) | **30–45 hours** |
| Estimated hours (base) | **43 hours** |
| Estimated hours (worst case) | **59 hours** |
| Quoted cost (base) | **$1,204** |
| Quoted cost (maximum) | **$1,428** |
| Risk of overrun | **Moderate-High** (driven by CETC unknown) |

**Bottom line:** If CETC integration goes smoothly (≤8 hrs), you'll finish within budget and timeline. If it's complex (12+ hrs), you'll need to either negotiate more time, work extra hours in weeks 2-3, or cut scope from Phase 3.

---

## Feasibility Assessment

### The Math

```
Available hours:  30 (pessimistic) – 45 (optimistic) hours
Estimated hours:  35 (optimistic)  – 59 (pessimistic) hours
```

**Best case:** You need 35 hours and have 45 → comfortable (10-hour buffer).  
**Expected case:** You need 43 hours and have 37 → slightly over (~1.5 extra hours/week needed).  
**Worst case:** You need 59 hours and have 30 → impossible without scope reduction.

### Probability Assessment

| Scenario | Probability | Hours Needed | Fits in 3 weeks? |
|----------|-------------|--------------|-------------------|
| Everything goes smoothly | 20% | 35 | Yes |
| CETC is moderate complexity | 50% | 43-48 | Barely (need 14-16 hrs/wk) |
| CETC is architecturally different | 25% | 50-59 | No (need scope cut or extension) |
| Showstopper discovered | 5% | N/A | Requires renegotiation |

**Most likely outcome (50%):** You'll need to push toward 15 hrs/week consistently, with one heavier week during GUI phase.

---

## Per-Phase Risk Analysis

### Phase 1: Competition Manual — LOW RISK

| Factor | Assessment |
|--------|-----------|
| Complexity | Low — documentation work, no code dependencies |
| Dependencies | None — can start immediately |
| Uncertainty | Minimal — scope is well-defined from next_steps.md |
| Estimated hours | 12-18 (quoted: 14) |

**Why it's safe:** This is writing work. You already have the full scoring system defined in `new_instructions_v2.tex`. The main new work is the playing field definition, scorecards, and anti-cheat documentation. No external dependencies.

**Tip:** Start here even if you get tempted to jump into code. The manual informs everything else (field dimensions affect XRP code, scoring rules affect what the receipt must capture).

---

### Phase 2: GUI Adaptation — HIGH RISK

| Factor | Assessment |
|--------|-----------|
| Complexity | High — unknown codebase integration + crypto implementation |
| Dependencies | CETC code (you have it, but haven't assessed it) |
| Uncertainty | **Very high** — CETC integration could be 5 hours or 12+ |
| Estimated hours | 14-26 (quoted: 18) |

**Why it's risky:**

1. **CETC Integration (the wildcard):** You're quoting 8 hours for something you haven't assessed. Scenarios:
   - *Best:* CETC code follows similar patterns to `gui_train_model.py`, uses the same Ultralytics YOLO API, just needs wrapper adjustments. → 5 hours.
   - *Moderate:* Different data pipeline, different folder structure, different training call. Needs adapter layer. → 8-10 hours.
   - *Worst:* Completely different framework, different model architecture, incompatible assumptions. Requires partial rewrite of either CETC code or the GUI. → 12-15 hours.

2. **Fernet Encryption:** Well-scoped and predictable (4-6 hours). The `cryptography` library makes this straightforward. Key management is the design decision, not the code.

3. **mAP Extraction:** Low risk. The data is already in `results.csv` from Ultralytics. Just needs programmatic reading (2 hours).

**Mitigation strategy:**
- **Day 1 of Week 2:** Spend 2-3 hours ONLY assessing CETC code. Don't start coding.
- **Go/no-go decision:** If CETC integration looks like 12+ hours, immediately communicate to the team that either (a) the timeline extends by 1 week, or (b) CETC integration is descoped and you work with the existing GUI structure.

---

### Phase 3: XRP Robot Code — MEDIUM RISK

| Factor | Assessment |
|--------|-----------|
| Complexity | Medium — MicroPython on hardware, needs physical testing |
| Dependencies | Phase 1 (field definition), hardware availability |
| Uncertainty | Medium — code changes are clear, but hardware testing is unpredictable |
| Estimated hours | 9-15 (quoted: 11) |

**Why it's medium risk:**

1. **Hardware dependency:** You can write and review code on your laptop, but you CANNOT verify it works without the physical XRP, a webcam, and serial connection. If hardware isn't available until mid-week-3, you lose testing time.

2. **Known code issues:** The current `main.py` has clear problems (5s hardcoded sleep, avoid drives toward object, no timeouts). Fixing these is straightforward in isolation, but testing each fix requires a full pipeline run.

3. **Scope pressure:** Phase 3 shares Week 3 with the tail end of Phase 2. If GUI work overruns, XRP testing gets compressed.

**Mitigation:**
- Write all code changes in Week 2 (evenings, if possible) so Week 3 is pure testing.
- Define a "minimum viable XRP" — what's the least you must change for the competition to work?

---

## Encryption Implementation: Recommended Approach

### Architecture: Fernet Symmetric Encryption

```
[GUI trains model] → collects hyperparams + results → JSON payload
                   → encrypt with Fernet(SECRET_KEY) → .receipt file
                   → student submits .receipt + best.pt

[Moderator] → loads .receipt → decrypt with same SECRET_KEY
            → reads hyperparams, mAP, model size → applies scoring formula
```

### Why Fernet?

| Criterion | Fernet | RSA | HMAC-only |
|-----------|--------|-----|-----------|
| Complexity | Low | High | Low |
| Student can forge? | No (needs key) | No (needs private key) | No (needs key) |
| Student can read? | No (encrypted) | Yes (only signed) | Yes (only signed) |
| Library | `cryptography` (pip) | `cryptography` (pip) | `hashlib` (stdlib) |
| Key management | 1 shared key | Key pair | 1 shared key |

**Fernet wins** because students cannot even READ their own receipt contents (it's encrypted, not just signed). This prevents them from knowing what mAP was recorded and adjusting their strategy to claim a different one.

### Security Considerations

- The secret key will exist in the GUI source code (or a config file). Determined students COULD extract it.
- **Mitigation:** Obfuscate the key (don't store as plaintext constant). Not bulletproof, but raises the bar significantly.
- **Better mitigation:** Load key from an environment variable or a file that moderators place on competition machines. Students never see the key.
- **Best mitigation (if time allows):** Compile the GUI to an executable (PyInstaller). Key embedded in binary is much harder to extract.

### Receipt Payload Structure

```json
{
  "version": 1,
  "run_id": "uuid-v4",
  "timestamp": "2026-06-01T14:30:00Z",
  "hyperparameters": {
    "epochs": 20,
    "learning_rate": 0.01,
    "model_size": "n",
    "train_split": 0.8,
    "classes": ["Rocket", "Tire", "Tin can"]
  },
  "results": {
    "mAP_per_class": [0.92, 0.87, 0.85],
    "mAP_average": 0.88,
    "precision": 0.91,
    "recall": 0.86,
    "model_file_size_bytes": 12345678
  },
  "machine_fingerprint": "sha256-of-hostname+mac"
}
```

---

## Timeline Visualization

```
Week 1 (10-15 hrs)          Week 2 (10-15 hrs)          Week 3 (10-15 hrs)
========================    ========================    ========================
[  Phase 1: MANUAL    ]     [   Phase 2: GUI       ]    [Phase 2 tail][Phase 3 ]
                                                         [  GUI wrap ] [ XRP    ]
├─ Field definition         ├─ CETC assessment (2-3h)   ├─ UI polish
├─ Scoring + scorecards     ├─ CETC integration         ├─ State machine fixes
├─ Student guide            ├─ Receipt system           ├─ Hardware testing
├─ Moderator guide          ├─ mAP extraction           ├─ Integration test
└─ Anti-cheat docs          └─ Testing begins           └─ Final validation

DELIVERABLE: Manual PDF     DELIVERABLE: GUI + Receipt  DELIVERABLE: XRP code
```

---

## What to Prioritize If Time Runs Short

If you hit Week 3 and Phase 2 isn't done, here's the triage order:

### Must-have (competition cannot run without these)
1. Competition manual (Phase 1) — defines what the competition IS
2. Working GUI that trains a model (even without CETC changes)
3. XRP code that can search/center/contact/avoid (already works today)

### Should-have (competition quality suffers without these)
4. Signed receipt system (anti-cheating)
5. XRP timeout protection and parameterization
6. mAP extraction into receipt

### Nice-to-have (can defer to post-competition patch)
7. Full CETC integration (could ship with current GUI if CETC proves too complex)
8. GUI executable compilation (PyInstaller)
9. Boundary-aware robot behavior (robots won't fall off a table, but may wander)

### Recommended scope cut if over budget:
**Cut CETC integration depth.** If their code doesn't mesh cleanly with the GUI in ≤8 hours, stop. Ship the existing `gui_train_model.py` with the receipt system added. Integrate CETC in a future iteration.

---

## Cost Comparison

| Scenario | Hours | Total Cost | Fits 3 weeks? |
|----------|-------|-----------|---------------|
| Optimistic (everything smooth) | 35 | $980 | Yes, with buffer |
| **Quoted (expected)** | **43** | **$1,204** | **Yes, at 14-15 hrs/wk** |
| With contingency | 51 | $1,428 | Tight, needs 17 hrs/wk |
| Worst case | 59 | $1,652 | No — needs 4th week |

---

## Recommendations

1. **Assess CETC code IMMEDIATELY** (before submitting the quotation if possible). Even 1-2 hours of reading their code would dramatically reduce your risk. You said you have it — spend 2 hours on it this week. This single action could save you from over-promising.

2. **Quote the base (43 hrs / $1,204) with a written contingency clause.** Something like: "CETC integration complexity may add up to 8 additional hours ($224). Final hours will be reported weekly."

3. **Front-load the manual.** It has zero dependencies and zero risk. Getting Phase 1 done in Week 1 gives you maximum runway for the risky Phase 2.

4. **Set a hard go/no-go on CETC by end of Day 1, Week 2.** If integration looks like 12+ hours, communicate immediately. Don't burn a week trying to force-fit incompatible code.

5. **Write XRP code changes during Week 2** (on paper or in a branch). Don't wait until Week 3 to start thinking about it. The hardware testing in Week 3 should be validation, not development.

6. **Negotiate a 4th week as buffer** if the team is open to it. Frame it as: "3 weeks for delivery, 4th week for testing and polish." This gives you breathing room at zero additional commitment if things go smoothly.

---

## Final Verdict

**The project is feasible at the quoted scope and timeline, with one major caveat:** the CETC integration is a black box. Your quoted 43 hours is achievable at 14-15 hours/week — slightly above your stated 10-15 range but not unreasonable for a 3-week sprint.

**Risk of failure:** Low for Phases 1 and 3. Moderate-High for Phase 2 (CETC).

**My recommendation:** Submit the quotation as-is ($1,204 base, $1,428 max), but internally plan for 15 hrs/week and assess the CETC code this week before committing.
