#!/usr/bin/env python3
"""
Extract saved PNG image outputs from notebooks (no execution) into a staging dir,
tagging each by keywords found in its source cell so the right figure can be picked.

Usage: python3 scripts/extract_notebook_outputs.py
Outputs: scratchpad staging PNGs + a printed manifest of (notebook, cell, tags).
Curated figures are then copied to public/figures/ with a manifest by figures_manifest.
"""
import nbformat, base64, sys, os
from pathlib import Path

# Sibling research repo by default; override with RESEARCH_DIR / STAGE_DIR.
RESEARCH = Path(os.environ.get("RESEARCH_DIR", Path(__file__).resolve().parents[2] / "research"))
STAGE = Path(os.environ.get("STAGE_DIR", "/tmp/nb_figures"))
STAGE.mkdir(parents=True, exist_ok=True)

TARGETS = [
    "GMD_CNN_prototype5_3_tSNE.ipynb",
    "PaSST_setup6_4.ipynb",
    "GMD_CNN_prototype6_4.ipynb",
    "PaSST_setup6_16.ipynb",
]
KW = ["tsne", "t-sne", "confusion", "history", "val_loss", "accuracy", "loss", "centroid", "primary"]


def main():
    for name in TARGETS:
        p = RESEARCH / name
        if not p.exists():
            print("MISSING", name); continue
        nb = nbformat.read(p, as_version=4)
        stem = p.stem.replace(" ", "_")
        print("=" * 80); print(name)
        for i, c in enumerate(nb.cells):
            if c.cell_type != "code":
                continue
            src = (c.get("source", "") or "").lower()
            for j, o in enumerate(c.get("outputs", []) or []):
                png = (o.get("data", {}) or {}).get("image/png")
                if not png:
                    continue
                tags = [k for k in KW if k in src]
                fn = STAGE / f"{stem}__c{i:03d}_{j}.png"
                fn.write_bytes(base64.b64decode(png))
                tagstr = ",".join(tags) if tags else "-"
                snippet = " ".join((c.get("source", "") or "").split())[:90]
                print(f"  c{i:03d}.{j}  [{tagstr:24}] {fn.name}  | {snippet}")


if __name__ == "__main__":
    main()
