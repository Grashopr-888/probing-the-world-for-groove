# Content Provenance

> Every headline claim, metric, and figure on the site maps to a verified source here.
> Purpose: prevent the condensed site from mixing non-comparable rounds or presenting a preliminary result as final.
> Status legend: ✅ verified against primary source · ⏳ to verify at build time.

## Primary sources

- **WB** = `Thesis Experiment results.xlsx`, sheet `Overall` (repo copy, canonical).
- **LBD** = `context_docs/456_lbd (2).pdf` (ISMIR 2025 Late-Breaking Demo, 3 pp).
- **TH** = `Trent_Eriksen_s3746887_LUMT_Thesis_Final_v2.pdf` (57 pp).
- **NB** = source notebook (saved outputs).

## Headline metrics

| # | Claim | Value | Source | Exact location | Status |
|---|---|---|---|---|---|
| 1 | Processed two-bar clips | 18,264 | LBD | §2 Method | ✅ |
| 2 | Style classes (primary⊕secondary) | 74 | LBD; WB | §2; class labels across embedding sheets | ✅ |
| 3 | Experiments | 34 | WB; LBD | `Overall` rows 1–34; §3 "34 experiments" | ✅ |
| 4 | Experiment rounds | 11 | WB; LBD | `Overall` rounds 1.0–11.0; §3 | ✅ |
| 5 | Experiment categories | 4 | LBD; WB | §3; 4 results sheets | ✅ |
| 6 | **Final CNN macro-F1** | **0.9080** | WB; LBD | exp 10.1; Table 1 (10.1) | ✅ |
| 7 | Final CNN config | 7-conv + GaussianNoise + RoomSimulator | WB; LBD | exp 10.1 desc; §3 | ✅ |
| 8 | **Final PaSST macro-F1** | **0.8752** | WB; LBD | exp 11.2; Table 1 (11.2) | ✅ |
| 9 | Final PaSST config | frozen PaSST + 4-layer MLP + reflection padding | WB; LBD | exp 11.2 desc; §3 | ✅ |
| 10 | Low-data CNN (GMD-mini) | 0.3267 | WB; LBD | exp 3.1; §3 | ✅ |
| 11 | Low-data PaSST (GMD-mini) | 0.3911 | WB; LBD | exp 3.2; §3 / Table 1 | ✅ |
| 12 | Best plain CNN depth | 7-conv = 0.8944 | WB; LBD | exp 9.2; Table 1 (9.2) | ✅ |
| 13 | Best PaSST head depth | 4-layer MLP = 0.8659 | WB; LBD | exp 8.3; Table 1 (8.3) | ✅ |
| 14 | Early rock-only CNN (**not** headline) | 0.9204 | WB; LBD | exp 1.1; Table 1 (1.1) | ✅ |
| 15 | Early rock-only PaSST | 0.8544 | WB | exp 1.2 | ✅ |

## Interpretation claims

| # | Claim | Value / wording | Source | Status |
|---|---|---|---|---|
| 16 | Cross-model centroid shift NOT comparable (different spaces/scales) | PaSST primary-style shift **8.32** vs CNN **94.66** under reflection padding | LBD §3; embedding sheets | ✅ |
| 17 | PaSST = tighter primary-style clustering / lower mean centroid shift → more hierarchical embedding | qualitative | LBD §3 + Conclusion | ✅ |
| 18 | CNN = more local feature adherence; more impacted by class imbalance | qualitative | LBD §3 + Conclusion | ✅ |
| 19 | Augmentations (RoomSimulator, GaussianNoise) slightly help CNN, degrade PaSST; TimeStretch hurts both | qualitative + WB (10.x) | LBD §3; WB | ✅ |
| 20 | Reflection padding = PaSST's best (0.8752); adding it on top of CNN augmentation lowers CNN (10.1 0.9080 → 11.3 0.8747) | WB | exp 10.1 vs 11.3 | ✅ |
| 21 | Time patchout gave no benefit | qualitative + WB | LBD §3; WB round 6 | ✅ |
| 22 | Class imbalance: rock ≈ two-thirds of GMD | LBD §3 | ✅ |
| 23 | 'misfits' cluster ≈ drum fills (291 files labeled 'fill' vs 'beat') | LBD §3 | ✅ |
| 24 | Commonly confused: jazz-fast ↔ dance-breakbeat / jazz-mediumfast; funk ↔ hip-hop | LBD §3 | ✅ |

## Method facts

| # | Claim | Value | Source | Status |
|---|---|---|---|---|
| 25 | CNN input | 16 kHz mono, log-mel | LBD §2 | ✅ |
| 26 | PaSST input | resampled 32 kHz mono, padded to 10 s (AudioSet match) | LBD §2 | ✅ |
| 27 | Split | ~80 / 10 / 10, proportional class balancing | LBD §2 | ✅ |
| 28 | Training | Adam, lr 1e-4, batch 16, 50 epochs, early-stop patience 10 | LBD §2 | ✅ |
| 29 | CNN architecture basis | VGG-inspired, adapted from Hiner / khiner DrumClassification | LBD §1–2 | ✅ |
| 30 | PaSST | frozen AudioSet embeddings, no fine-tuning (Patchout AST) | LBD §1–2 | ✅ |
| 31 | Augmentation library | audiomentations (GaussianNoise, RoomSimulator, TimeStretch) | LBD §2 | ✅ |
| 32 | Padding modes | zeros, reflection, circular | LBD §2 | ✅ |
| 33 | Primary metric | macro-F1 | LBD §2 | ✅ |
| 34 | Research question (core) | effect of pretrained general-audio embeddings (PaSST) vs baseline CNN for drum audio style classification | LBD §1; TH | ✅ (exact thesis RQ wording ⏳ to lift at build) |
| 35 | GMD metadata available | BPM, beat/fill type, time signature | TH p3 | ✅ |

## Comparability guardrails (enforce in the experiments explorer)

- ⚠️ **Never** headline exp 1.1 (0.9204, rock-only) as the final result — different, narrower label set than the 74-class benchmark (claim #14).
- ⚠️ **Never** plot raw CNN vs PaSST centroid-shift magnitudes side by side (claim #16). Use within-model ranks / normalized shifts / shift÷baseline dispersion.
- ✅ Final CNN (10.1, 0.9080) vs final PaSST (11.2, 0.8752) **are** comparable — both GMD-full, 74 classes.
- ✅ Low-data reversal (3.1 vs 3.2) is comparable within the GMD-mini condition.

## To verify at build time (⏳)

- Exact thesis research-question wording (TH Introduction) and dataset-split section numbers.
- Diff `ISMIRLBD2025_Experiment_results.xlsx` vs canonical workbook before final JSON extraction.
- Per-figure provenance (notebook + cell index + git SHA) recorded in the figure manifest as figures are extracted.
- Confirm `2024-2025-EriksenTTrent (1).pdf` is identical thesis content before using either PDF as the download.
