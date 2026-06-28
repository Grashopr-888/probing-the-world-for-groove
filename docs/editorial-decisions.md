# Editorial decisions

Normalizations and judgment calls made while turning the research material into the site.
Source values are never silently overwritten; deviations are recorded here.

## Naming & framing

- **Public hero title** is editorial — "Can a model trained on general audio understand drum style?" The full thesis title is preserved verbatim on the Method and Publication pages and in metadata.
- **Repository / site name** `probing-the-world-for-groove` chosen for a clean URL (the research repo's name is very long). Decided with the author.
- **Round titles & research questions** in the Experiments progression are editorial synthesis (the workbook has no per-round titles). The 4 categories match the workbook's own sheet grouping and the LBD paper.

## Data normalization (scripts/extract_experiments.py)

- **Notebook column**: workbook rows 1–8 omit the `.ipynb` extension; normalized to always include it.
- **Derived fields** parsed from the workbook's own `Description` column: `datasetScope` (rock-only / GMD-mini / GMD-full), `convDepth`, `headDepth` (MLP), `augmentation`, `padding` (defaults to "zero" where unstated, per the LBD method), `patchout`, `bottleneck`.
- **F1** rendered to 4 decimal places consistently.

## Comparability guardrails

- The early **rock-only** CNN result (exp 1.1, 0.9204) is shown only in experiment history — never as the headline — because it uses a narrower, easier label set than the final 74-class task.
- **Cross-model centroid shifts are never plotted on a shared axis.** CNN (~94.66) and PaSST (~8.07) primary-style shifts live in different coordinate systems; the Representations page uses separate within-model axes and states the ≈11.7× scale gap is an artifact.
- The Experiments "compare" tool warns when two selected runs differ in dataset scope.

## Known discrepancies (flagged, not fixed)

- **exp 8.3 (`PaSST_setup6_8`, PaSST 4-layer MLP):** the workbook records macro-F1 **0.8659**; the saved notebook's classification report shows macro avg ≈ **0.861**. Both local copies (May & Aug 2025) agree on ≈0.861. The site uses the **workbook value** (declared source of truth). Likely a re-run or a different F1 averaging between the logged result and the saved notebook — flagged for the author to reconcile.
- Audio sample rate: the LBD/handoff "16 kHz mono" is the **CNN** input; PaSST resamples to **32 kHz** and pads to 10 s. Both stated precisely on the Method page.

## Notebook restoration (research repo, local commit — not pushed)

Three notebooks were 2-byte placeholders on GitHub; valid copies from `~/Downloads` (Aug 2025 variants) were restored, plus two notebooks missing from the repo entirely:

| Restored | = experiment | Verified macro-F1 in outputs |
| --- | --- | --- |
| `GMD_CNN_prototype6_2.ipynb` | 9.2 (best CNN depth) | 0.894 ✓ |
| `PaSST_setup6_5.ipynb` | 7.1 | 0.858 ✓ |
| `PaSST_setup6_8.ipynb` | 8.3 (best PaSST head) | ≈0.861 (see discrepancy above) |
| `GMD_CNN_prototype5_3_tSNE.ipynb` | CNN t-SNE analysis | (new file) |
| `GMD_prototype_preprocessing.ipynb` | data pipeline | (new file) |
