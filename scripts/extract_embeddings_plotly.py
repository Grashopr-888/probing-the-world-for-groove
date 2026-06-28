#!/usr/bin/env python3
"""
Extract interactive t-SNE coordinates (7 perplexities) for each model from the
Plotly figures saved in the notebook outputs, into a compact JSON the site loads
on demand to rebuild interactive embedding plots.

Source cells (px.scatter coloured by primary style, perplexities 5/15/30/40/50/75/100):
  PaSST : PaSST_setup6_4.ipynb           cell 54 (outputs .0–.6)
  CNN   : GMD_CNN_prototype5_3_tSNE.ipynb cell 78 (outputs .0–.6)

Output (labels stored once; xy per perplexity per point):
  public/data/embeddings-passt.json, public/data/embeddings-cnn.json
"""
import nbformat, json, re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Sibling research repo by default; override with RESEARCH_DIR.
RESEARCH = Path(os.environ.get("RESEARCH_DIR", ROOT.parent / "research"))
OUT = ROOT / "public" / "data"
PERPS = [5, 15, 30, 40, 50, 75, 100]
SOURCES = {
    "passt": ("PaSST_setup6_4.ipynb", 54),
    "cnn": ("GMD_CNN_prototype5_3_tSNE.ipynb", 78),
}


def extract_data_array(html: str):
    """Pull the `data` array (2nd arg) out of Plotly.newPlot(...) via bracket matching."""
    i = html.find("Plotly.newPlot")
    if i < 0:
        return None
    # first '[' after the div-id string
    start = html.find("[", i)
    depth, in_str, esc = 0, False, False
    for j in range(start, len(html)):
        ch = html[j]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return json.loads(html[start:j + 1])
    return None


def perp_figure(nb, cell, out_index):
    o = nb.cells[cell]["outputs"][out_index]
    html = o["data"]["text/html"]
    html = "".join(html) if isinstance(html, list) else html
    return extract_data_array(html)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for model, (nbname, cell) in SOURCES.items():
        nb = nbformat.read(RESEARCH / nbname, as_version=4)
        color_map = {}
        # points keyed by (primary, index-within-primary) -> dict
        merged = {}
        order = []  # preserve first-seen order
        for k, perp in enumerate(PERPS):
            data = perp_figure(nb, cell, k)
            if data is None:
                raise SystemExit(f"{model}: could not parse perplexity {perp}")
            for tr in data:
                primary = tr.get("name", "?")
                col = (tr.get("marker", {}) or {}).get("color")
                if isinstance(col, str):
                    color_map.setdefault(primary, col)
                xs, ys = tr.get("x", []), tr.get("y", [])
                cd = tr.get("customdata", []) or []
                for idx in range(len(xs)):
                    key = (primary, idx)
                    if key not in merged:
                        sec = cd[idx][1] if idx < len(cd) and len(cd[idx]) > 1 else ""
                        full = cd[idx][2] if idx < len(cd) and len(cd[idx]) > 2 else primary
                        merged[key] = {"p": primary, "s": sec, "f": full, "xy": [None] * len(PERPS)}
                        order.append(key)
                    merged[key]["xy"][k] = [round(float(xs[idx]), 2), round(float(ys[idx]), 2)]
        points = [merged[k] for k in order]
        payload = {
            "model": model,
            "perplexities": PERPS,
            "colorMap": color_map,
            "count": len(points),
            "points": points,
        }
        fp = OUT / f"embeddings-{model}.json"
        fp.write_text(json.dumps(payload, separators=(",", ":")))
        print(f"✓ {model}: {len(points)} points × {len(PERPS)} perplexities, "
              f"{len(color_map)} classes → {fp.relative_to(ROOT)} ({fp.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
