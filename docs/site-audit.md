# Site Audit — *Probing the World for Groove*

> Factual inventory of all research material backing the GitHub Pages site.
> Generated during Phase 1 (audit before building). Read-only inspection — no notebooks were executed.

- **Research repo:** `Grashopr-888/A-comparative-study-of-Transfer-Learning-for-Drum-audio-Style-Classification-` (PUBLIC, default branch `main`)
- **Local clone:** `../research` @ HEAD `ddd4415` (pushed 2025-08-03)
- **User source staging:** `../context_docs/` (poster, LBD paper, thesis PDF, workbook, slides)
- **Audit scripts:** `scripts/audit_notebooks.py`, `scripts/dump_xlsx.py` (currently in session scratchpad; to be moved into repo)

---

## 1. Notebook inventory

34 notebooks in the repo. **31 valid, 3 corrupt (2-byte placeholders).** All valid notebooks carry rich saved outputs (no re-execution needed). Feature flags below come from scanning cell sources + saved outputs for keywords.

Legend: `conf`=confusion matrix · `tsne`=t-SNE/embedding · `curve`=training/val curves · `rpt`=classification report · `aug`=augmentation code · `pad`=padding code.

### CNN family (`GMD_CNN_*`)

| Notebook | Exp | Cells | Outputs | conf | tsne | curve | rpt | Status |
|---|---|---|---|---|---|---|---|---|
| GMD_CNN_prototype3 | 1.1 | 48 | 122 | ✓ | | ✓ | ✓ | valid |
| GMD_CNN_prototype4 | 3.1 | 50 | 124 | ✓ | | ✓ | ✓ | valid |
| GMD_CNN_prototype5 | 4.1 | 51 | 125 | ✓ | | ✓ | ✓ | valid |
| GMD_CNN_prototype5_2 | 5.3 | 52 | 125 | ✓ | | ✓ | ✓ | valid |
| GMD_CNN_prototype5_3 | 5.4 | 52 | 123 | ✓ | | ✓ | ✓ | valid |
| GMD_CNN_prototype6 | 9.1 | 82 | 149 | ✓ | ✓ | ✓ | ✓ | valid |
| **GMD_CNN_prototype6_2** | **9.2** | — | — | | | | | **CORRUPT (2 B)** |
| GMD_CNN_prototype6_3 | 9.3 | 82 | 139 | ✓ | ✓ | ✓ | ✓ | valid |
| GMD_CNN_prototype6_4 | 10.1 | 84 | 150 | ✓ | ✓ | ✓ | ✓ | valid — **headline CNN** |
| GMD_CNN_prototype6_5 | 10.4 | 84 | 152 | ✓ | ✓ | ✓ | ✓ | valid |
| GMD_CNN_prototype6_6 | 11.3 | 84 | 130 | ✓ | ✓ | ✓ | ✓ | valid |
| GMD_CNN_prototype6_7 | 11.4 | 83 | 151 | ✓ | ✓ | ✓ | ✓ | valid |
| GMD_CNN_prototype6_8 | 11.5 | 83 | 149 | ✓ | ✓ | ✓ | ✓ | valid |

### PaSST family (`PaSST_setup*`)

| Notebook | Exp | Cells | Outputs | conf | tsne | curve | rpt | Status |
|---|---|---|---|---|---|---|---|---|
| PaSST_setup2 | 1.2 | 29 | 124 | ✓ | | ✓ | ✓ | valid |
| PaSST_setup3 | 2.1 | 30 | 193 | ✓ | | ✓ | ✓ | valid |
| PaSST_setup4 | 2.2 | 30 | 198 | ✓ | | ✓ | ✓ | valid |
| PaSST_setup5 | 3.2 | 53 | 214 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup5_2 | 6.2 | 53 | 206 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6 | 4.2 | 34 | 202 | ✓ | | ✓ | ✓ | valid |
| PaSST_setup6_2 | 5.1 | 36 | 211 | ✓ | | ✓ | ✓ | valid |
| PaSST_setup6_3 | 5.2 | 35 | 206 | ✓ | | ✓ | ✓ | valid |
| PaSST_setup6_4 | 6.1 | 55 | 235 | ✓ | ✓ | ✓ | ✓ | valid |
| **PaSST_setup6_5** | **7.1** | — | — | | | | | **CORRUPT (2 B)** |
| PaSST_setup6_6 | 8.1 | 57 | 224 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_7 | 8.2 | 57 | 224 | ✓ | ✓ | ✓ | ✓ | valid |
| **PaSST_setup6_8** | **8.3** | — | — | | | | | **CORRUPT (2 B)** — best PaSST head |
| PaSST_setup6_9 | 8.4 | 57 | 227 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_10 | 8.5 | 58 | 191 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_11 | 8.6 | 57 | 236 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_12 | 8.7 | 57 | 220 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_13 | 10.2 | 58 | 234 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_14 | 10.3 | 58 | 192 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_15 | 11.1 | 57 | 208 | ✓ | ✓ | ✓ | ✓ | valid |
| PaSST_setup6_16 | 11.2 | 57 | 212 | ✓ | ✓ | ✓ | ✓ | valid — **headline PaSST** |

Also corrupt in repo: `LUMT_Thesis_Presentation.pptx` (2 B placeholder).

### Recovery — the 3 corrupt notebooks + 2 missing notebooks all exist locally

`~/Downloads/` holds valid copies of every corrupt file, plus two notebooks absent from the repo:

| Repo gap | Recovery file (Downloads) | Cells | Notes |
|---|---|---|---|
| GMD_CNN_prototype6_2 (exp 9.2) | `GMD_CNN_prototype6_2 (2).ipynb` (Aug 3 2025) | 82 | full outputs, t-SNE, conf, report |
| PaSST_setup6_5 (exp 7.1) | `PaSST_setup6_5 (1).ipynb` (Aug 3 2025) | 56 | full outputs |
| PaSST_setup6_8 (exp 8.3) | `PaSST_setup6_8 (1).ipynb` (Aug 3 2025) | 57 | full outputs |
| *(missing from repo)* | `GMD_CNN_prototype5_3_tSNE.ipynb` | 79 | dedicated CNN t-SNE — LBD Fig. 2 source |
| *(missing from repo)* | `GMD_prototype_preprocessing.ipynb` | 72 | dataset/preprocessing pipeline — Method-page source (0 saved outputs, code only) |

**Recommended action (needs go-ahead — touches the research repo):** replace the 3 corrupt notebooks with the recovered copies and add the 2 missing notebooks, in a single clearly-labelled "restore corrupt/missing notebooks" commit, before reorganizing anything.

---

## 2. Experiment workbook — the experiment source of truth

Two copies exist and differ slightly (different md5):
- `research/Thesis Experiment results.xlsx` (repo, 379 939 B) — **canonical** (referenced by the handoff).
- `context_docs/ISMIRLBD2025_Experiment_results.xlsx` (380 282 B, newer file date) — to diff before final extraction.

**17 sheets:**

| Sheet | Rows | Purpose |
|---|---|---|
| `Overall` | 34 exp | All 34 experiments × 11 rounds — drives the experiments explorer |
| `Configuration Exploration` | rounds 1–2 | Category 1 |
| `Dataset Exploration` | rounds 3–5 | Category 2 (incl. GMD-mini low-data) |
| `Model depth and Patchout` | rounds 6–9 | Category 3 |
| `Augmentations and Padding` | rounds 10–11 | Category 4 |
| `PaSST_top20shift_embeddings` etc. (12 sheets) | per-class | Centroid-shift + embedding-comparison data → Representations page |

Columns (results sheets): `Experiment Round · Experiment ID · Model · F1 · Notebook · Description`.
Columns (embedding sheets): `Experiment A · Experiment B · Mean Centroid Shift · Class Rank · Class Label · Class Index · Class Shift`.

Data hygiene notes (record corrections in `editorial-decisions.md`, never overwrite source):
- `Notebook` column is inconsistent — rows 1–8 lack the `.ipynb` extension, rows 9+ include it. Normalize for linking.
- F1 values stored as floats (e.g. `0.908`, `0.9204`); render consistently to 4 dp.

---

## 3. Verified headline claims

Every central claim from the handoff was checked against the workbook + LBD paper. **All verified.** (Full mapping in `content-provenance.md`.)

| Claim | Value | Confirmed in |
|---|---|---|
| Processed clips | 18,264 | LBD §2 |
| Style classes | 74 | LBD §2; workbook |
| Experiments / rounds | 34 / 11 | workbook `Overall`; LBD §3 |
| Experiment categories | 4 | LBD §3; workbook sheets |
| **Final CNN macro-F1** | **0.9080** (exp 10.1, 7-conv + GaussianNoise + RoomSimulator) | workbook; LBD Table 1 |
| **Final PaSST macro-F1** | **0.8752** (exp 11.2, 4-layer MLP + reflection padding) | workbook; LBD Table 1 |
| Low-data GMD-mini | CNN 0.3267 / PaSST 0.3911 | workbook exp 3.1/3.2; LBD §3 |
| Best CNN depth | 7-conv = 0.8944 (exp 9.2) | workbook; LBD §3 |
| Best PaSST head | 4-layer MLP = 0.8659 (exp 8.3) | workbook; LBD §3 |
| Early rock-only CNN (NOT headline) | 0.9204 (exp 1.1) | workbook; LBD Table 1 |
| Centroid shift (cross-model — DO NOT compare raw) | PaSST 8.32 vs CNN 94.66 (primary style, reflection padding) | LBD §3; embedding sheets |

**Audio / preprocessing facts (LBD §2):** CNN = 16 kHz mono; PaSST = resampled to **32 kHz** mono, padded to fixed **10 s** to match AudioSet; mel spectrograms; ~80/10/10 split with proportional class balancing; Adam, lr 1e-4, batch 16, 50 epochs, early-stop patience 10. (Note: the handoff's "16 kHz mono" applies to the CNN; PaSST differs.)

---

## 4. Publication & media assets

| Asset | Location | Notes |
|---|---|---|
| **Final thesis PDF** (57 pp) | `Desktop/Thesis/Final Thesis files/Trent_Eriksen_s3746887_LUMT_Thesis_Final_v2.pdf` + repo copy | canonical |
| Thesis (library deposit, 57 pp) | `context_docs/2024-2025-EriksenTTrent (1).pdf` | same content, alt cover — confirm before use |
| **ISMIR LBD paper** (3 pp) | `context_docs/456_lbd (2).pdf` | publication-page primary |
| **Poster** (1 p) | `context_docs/456_poster (3).pdf` | |
| **Defense slides** | `context_docs/LUMT_Thesis_Presentation (5).pptx` (repo copy is a 2 B placeholder) | optional asset |
| **Presentation video** | `Desktop/ISMIR2025LBD_take1.mov` (422 MB), `take5.mov` (341 MB) | ⚠️ too large for Pages — **need a public embed URL (YouTube/Vimeo)** |
| ISMIR thumbnail | `Desktop/ISMIR_LBD_Thumbnail_456_Trent_Eriksen.png` | video poster candidate |
| Audio examples | GMD (CC BY 4.0); LBD references a Google Drive folder | curate ~6–10 clips; attribute, don't bundle full dataset |

**External links (from LBD paper):**
- GMD dataset — https://www.tensorflow.org/datasets/catalog/groove#groove2bar-16000hz
- PaSST — https://github.com/kkoutini/passt_hear21
- DrumClassification (CNN basis, khiner) — https://github.com/khiner/DrumClassification
- audiomentations — https://github.com/iver56/audiomentations
- Audio-examples Drive folder — https://drive.google.com/drive/folders/1taQUOIU8z7aKlKEZvoMsV9u3fP7IBS_C
- Official ISMIR LBD page — https://ismir2025program.ismir.net/lbd_456.html (paper/poster/video links are JS-rendered, not in static HTML)

---

## 5. Identity / citation facts (verified)

- **Title:** *Probing the World for Groove: A comparative study of Transfer Learning for Drum audio Style Classification*
- **Author:** Trent Eriksen (s3746887) · **Supervisors:** Edwin van der Heide (1st), Dr. Robert Saunders (2nd)
- **Degree:** MSc Media Technology, Leiden Institute of Advanced Computer Science (LIACS), Leiden University · **Date:** 30/06/2025
- **Keywords:** Machine Learning, Deep Learning, Music Information Retrieval, Transfer Learning, Supervised Learning
- **Thesis TOC:** Introduction · Related Work · Methodology · Experiments · Analysis · Discussion · Conclusion · References · Appendices
- **Origin hook:** project began as an attempt to detect the *motorik* groove (1970s krautrock 4/4); to avoid custom dataset creation, GMD was adopted and scope broadened from rock-only to all 74 styles.
- **ISMIR LBD:** "A Comparative Study Of Transfer Learning For Drum Audio Style Classification", Eriksen, van der Heide, Saunders — Extended Abstracts, Late-Breaking Demo Session, 26th ISMIR, Daejeon, South Korea, 2025. License CC BY 4.0.
- **Grants (post-thesis, publication page only):** ISMIR First-time Authors Grant (Aug 2025); Creative Intelligence and Technology Grant, Leiden University (Sep 2025); Leiden University Fund Research Grant (Oct 2025).

---

## 6. Tooling

node v22.14.0 · npm 10.9.2 · python 3.12.7 (nbformat 5.10.4, openpyxl 3.1.5; **no pypdf** — use built-in PDF reader or `pip install pypdf`) · git 2.47.1 · gh 2.94.0 (authed as `Grashopr-888`, scopes `repo, workflow, gist, read:org`). No conda. Jupyter present.

---

## 7. Open items needing user input

1. **Deployment target** — site in existing (long-named) repo under `/site` vs. a new dedicated repo vs. custom domain. Affects Astro `base`/`site` config.
2. **Public video URL** — YouTube/Vimeo link for the presentation (local `.mov` files are too large for Pages).
3. **Go-ahead to restore** the 3 corrupt + 2 missing notebooks in the research repo (separate commit).
4. **Defense slides** — include as a downloadable asset? (repo copy is a placeholder; real `.pptx` in `context_docs`.)
5. **Conference photos** — none located yet; include if available.
6. **Content license** for the site/text (code vs. thesis content vs. GMD attribution) — to be set in `LICENSES.md`, not chosen unilaterally.
