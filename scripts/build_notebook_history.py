#!/usr/bin/env python3
"""
Build a backdated git history from real Drive snapshots produced by
colab_extract_drive_history.py.

Each snapshot becomes one commit whose author + committer date is the notebook's
real Drive revision time. Commits are applied in chronological order, so the
repo's history (and your GitHub contribution graph, once pushed) mirrors when you
actually worked. Author identity matches your existing contributions.

Usage:
  python3 scripts/build_notebook_history.py <snapshots_dir> <output_repo_dir> [strip]
  # <snapshots_dir> = the unzipped nb_snapshots/ folder (must contain manifest.json)
  # add "strip" to remove saved cell outputs from each snapshot (keeps the repo
  #   lean; the code + dates stay authentic; full-output notebooks live in the
  #   research repo).

Does NOT create a GitHub repo or push — that stays gated on your approval.
"""
import json, os, sys, shutil, subprocess, datetime, collections
from pathlib import Path

def write_snapshot(src: Path, dest: Path, strip: bool):
    if not strip:
        shutil.copyfile(src, dest); return
    import nbformat
    nb = nbformat.read(src, as_version=4)
    nb.metadata.pop("widgets", None)          # ipywidgets state is the real bulk
    for c in nb.cells:
        if c.get("cell_type") == "code":
            c["outputs"] = []
            c["execution_count"] = None
        if "metadata" in c:
            c["metadata"].pop("widgets", None)
    nbformat.write(nb, dest)

AUTHOR_NAME = "Trent Eriksen"
AUTHOR_EMAIL = "124685398+Grashopr-888@users.noreply.github.com"

def git(args, cwd, env=None):
    subprocess.run(["git", *args], cwd=cwd, env=env, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    snap = Path(sys.argv[1]); repo = Path(sys.argv[2])
    strip = len(sys.argv) > 3 and sys.argv[3] == "strip"
    manifest = json.load(open(snap / "manifest.json"))
    events = []
    for m in manifest:
        stem = m["name"].replace(".ipynb", "").replace("/", "_")
        for mt in m.get("snapshot_days", []):
            fn = snap / stem / (mt.replace(":", "-") + ".ipynb")
            if fn.exists():
                dt = datetime.datetime.fromisoformat(mt.replace("Z", "+00:00"))
                events.append((dt, m["name"], stem, fn))
    if not events:
        sys.exit("No snapshots found (check the unzipped folder + manifest.json).")
    events.sort(key=lambda e: e[0])

    if repo.exists():
        shutil.rmtree(repo)
    repo.mkdir(parents=True)
    git(["init", "-q", "-b", "main"], repo)
    (repo / "notebooks").mkdir()

    seen = set(); months = collections.Counter()
    for dt, name, stem, fn in events:
        write_snapshot(fn, repo / "notebooks" / f"{stem}.ipynb", strip)
        git(["add", f"notebooks/{stem}.ipynb"], repo)
        verb = "Add" if stem not in seen else "Update"; seen.add(stem)
        epoch = int(dt.timestamp()); gdate = f"@{epoch} +0000"
        env = {**os.environ,
               "GIT_AUTHOR_DATE": gdate, "GIT_COMMITTER_DATE": gdate,
               "GIT_AUTHOR_NAME": AUTHOR_NAME, "GIT_AUTHOR_EMAIL": AUTHOR_EMAIL,
               "GIT_COMMITTER_NAME": AUTHOR_NAME, "GIT_COMMITTER_EMAIL": AUTHOR_EMAIL}
        git(["commit", "-q", "-m", f"{verb} {name}"], repo, env)
        months[dt.strftime("%Y-%m")] += 1

    print(f"✓ {len(events)} commits across {len(seen)} notebooks")
    print(f"  range: {events[0][0].date()} → {events[-1][0].date()}")
    print("  commits by month:")
    for k in sorted(months):
        print(f"    {k}: {months[k]}")

if __name__ == "__main__":
    main()
