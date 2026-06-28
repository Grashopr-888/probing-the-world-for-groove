#!/usr/bin/env python3
"""
Normalize the experiment workbook into structured JSON for the site.

Source of truth : public/data/thesis-experiment-results.xlsx  (sheet "Overall")
Outputs         : src/data/experiments.json
                  src/data/experiment-rounds.json
                  src/data/key-results.json

Never executes notebooks. Derivations (datasetScope, depth, augmentation, padding)
are parsed from the workbook's own Description column; round titles/questions are
editorial synthesis recorded in docs/content-provenance.md. Run from repo root:

    python3 scripts/extract_experiments.py
"""
import json, re, sys
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parent.parent
SRC_XLSX = ROOT / "public" / "data" / "thesis-experiment-results.xlsx"
OUT_DIR = ROOT / "src" / "data"

# Round → (title, category, research question). Editorial synthesis; see provenance doc.
ROUND_META = {
    1:  ("Initial configuration", "Configuration", "Do a baseline CNN and PaSST work on a narrow rock-style subset?"),
    2:  ("PaSST configuration", "Configuration", "How should PaSST be configured before scaling up?"),
    3:  ("Low-data comparison", "Dataset", "Which model wins when training data is scarce (GMD-mini)?"),
    4:  ("Full-dataset comparison", "Dataset", "How do the models compare on the full 74-class task?"),
    5:  ("Repeatability", "Dataset", "Are the full-data results stable across repeated runs?"),
    6:  ("t-SNE & time patchout", "Model depth & patchout", "Does time patchout help, and how are embeddings structured?"),
    7:  ("PaSST head depth I", "Model depth & patchout", "Does a deeper MLP head help PaSST?"),
    8:  ("PaSST head depth & bottlenecks", "Model depth & patchout", "What head depth and bottleneck shape is best for PaSST?"),
    9:  ("CNN convolutional depth", "Model depth & patchout", "How many convolutional layers does the CNN need?"),
    10: ("Augmentation", "Augmentation & padding", "Do audio augmentations improve either model?"),
    11: ("Padding", "Augmentation & padding", "Does the padding mode affect performance and representation?"),
}

AUG_MAP = {"GaussianNoise": "gaussian-noise", "RoomSimulator": "room-simulation", "TimeStretch": "time-stretch"}
SCOPE_LABEL = {"rock-only": "Rock-only (narrow)", "gmd-mini": "GMD-mini (low-data)", "gmd-full": "GMD-full (74-class)"}

HEADLINE = {("cnn", "10.1"), ("passt", "11.2")}


def norm_notebook(s: str) -> str:
    s = (s or "").strip()
    if s and not s.endswith(".ipynb"):
        s += ".ipynb"
    return s


def derive(desc: str, model: str):
    d = desc or ""
    low = d.lower()
    if "rock" in low:
        scope = "rock-only"
    elif "mini" in low:
        scope = "gmd-mini"
    else:
        scope = "gmd-full"

    conv = re.search(r"(\d+)\s*Conv", d)
    head = re.search(r"MLP\s*(\d+)\s*Layer", d)
    aug = [AUG_MAP[k] for k in AUG_MAP if k in d]
    if "Reflection" in d:
        padding = "reflection"
    elif "Circular" in d:
        padding = "circular"
    else:
        padding = "zero"
    bottleneck = "symmetric" if "Symmetric" in d else "progressive" if "Progressive" in d else None
    return {
        "datasetScope": scope,
        "datasetScopeLabel": SCOPE_LABEL[scope],
        "convDepth": int(conv.group(1)) if conv else None,
        "headDepth": int(head.group(1)) if head else None,
        "augmentation": aug,
        "padding": padding,
        "patchout": "patchout" in low,
        "bottleneck": bottleneck,
    }


def main():
    if not SRC_XLSX.exists():
        sys.exit(f"ERROR: workbook not found at {SRC_XLSX}")
    wb = openpyxl.load_workbook(SRC_XLSX, data_only=True)
    ws = wb["Overall"]
    rows = list(ws.iter_rows(values_only=True))
    header = rows[0]
    assert [h for h in header][:6] == [
        "Experiment Round", "Experiment ID", "Model", "F1", "Notebook", "Description",
    ], f"Unexpected header: {header}"

    experiments = []
    for r in rows[1:]:
        if r is None or r[1] is None:
            continue
        rnd = int(float(r[0]))
        exp_id = str(r[1]).strip()
        model = "cnn" if str(r[2]).strip().upper() == "CNN" else "passt"
        f1 = round(float(r[3]), 4)
        notebook = norm_notebook(str(r[4]))
        desc = str(r[5]).strip()
        d = derive(desc, model)
        title, category, _q = ROUND_META[rnd]
        experiments.append({
            "round": rnd,
            "experimentId": exp_id,
            "model": model,
            "f1": f1,
            "notebook": notebook,
            "description": desc,
            "category": category,
            "roundTitle": title,
            **d,
            "isHeadline": (model, exp_id) in HEADLINE,
            "comparableWithFinal": d["datasetScope"] == "gmd-full",
        })

    # rounds
    rounds = []
    for rnd, (title, category, q) in ROUND_META.items():
        members = [e for e in experiments if e["round"] == rnd]
        rounds.append({
            "round": rnd,
            "title": title,
            "category": category,
            "question": q,
            "experimentIds": [e["experimentId"] for e in members],
            "models": sorted({e["model"] for e in members}),
            "bestF1": max((e["f1"] for e in members), default=None),
        })

    def find(model, exp_id):
        return next(e["f1"] for e in experiments if e["model"] == model and e["experimentId"] == exp_id)

    key = {
        "finalCnn": find("cnn", "10.1"),
        "finalPasst": find("passt", "11.2"),
        "lowdataCnn": find("cnn", "3.1"),
        "lowdataPasst": find("passt", "3.2"),
        "bestCnnDepth": find("cnn", "9.2"),
        "bestPasstHead": find("passt", "8.3"),
        "rockOnlyCnn": find("cnn", "1.1"),
        "counts": {
            "experiments": len(experiments),
            "rounds": len(rounds),
            "categories": len({e["category"] for e in experiments}),
        },
    }

    # --- validation (fail loudly so the site never ships wrong numbers) ---
    assert key["counts"]["experiments"] == 34, key["counts"]
    assert key["counts"]["rounds"] == 11, key["counts"]
    assert key["counts"]["categories"] == 4, key["counts"]
    assert key["finalCnn"] == 0.908 and key["finalPasst"] == 0.8752, key
    assert key["lowdataCnn"] == 0.3267 and key["lowdataPasst"] == 0.3911, key
    assert key["bestCnnDepth"] == 0.8944 and key["bestPasstHead"] == 0.8659, key
    assert sum(1 for e in experiments if e["isHeadline"]) == 2

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "experiments.json").write_text(json.dumps(experiments, indent=2))
    (OUT_DIR / "experiment-rounds.json").write_text(json.dumps(rounds, indent=2))
    (OUT_DIR / "key-results.json").write_text(json.dumps(key, indent=2))

    print(f"✓ {len(experiments)} experiments, {len(rounds)} rounds → {OUT_DIR.relative_to(ROOT)}/")
    print(f"  final: CNN {key['finalCnn']} · PaSST {key['finalPasst']}  |  low-data: CNN {key['lowdataCnn']} · PaSST {key['lowdataPasst']}")


if __name__ == "__main__":
    main()
