"""
Run in a Google Colab cell (signed into the account holding your thesis notebooks).

Downloads, for each thesis notebook, ONE real snapshot per edit-day from Google
Drive revision history (the latest revision on each day), plus a manifest of all
revision timestamps. These real snapshots + dates are used to rebuild an honest
git history (author date = when you actually saved that notebook).

It prints the total size first so we can scope down before building if it's large.
Nothing is invented — only Drive's own revisions are used.
"""
import io, os, json, zipfile, collections
from google.colab import auth, files
auth.authenticate_user()
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

drive = build("drive", "v3")
NAME_PREFIXES = ("GMD_", "PaSST_")          # thesis notebooks
FOLDER_ID = ""                               # optional: restrict to one Drive folder
OUT = "nb_snapshots"; os.makedirs(OUT, exist_ok=True)

def list_files():
    q = "name contains '.ipynb' and trashed = false"
    if FOLDER_ID:
        q = f"'{FOLDER_ID}' in parents and trashed = false"
    out, tok = [], None
    while True:
        r = drive.files().list(q=q, pageSize=200, pageToken=tok,
              fields="nextPageToken, files(id,name,createdTime,modifiedTime)").execute()
        out += r.get("files", []); tok = r.get("nextPageToken")
        if not tok: return out

def list_revs(fid):
    out, tok = [], None
    while True:
        try:
            r = drive.revisions().list(fileId=fid, pageSize=200, pageToken=tok,
                  fields="nextPageToken, revisions(id,modifiedTime)").execute()
        except Exception:
            return out
        out += r.get("revisions", []); tok = r.get("nextPageToken")
        if not tok: return out

def fetch(fid, rid):
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, drive.revisions().get_media(fileId=fid, revisionId=rid))
    done = False
    while not done:
        _, done = dl.next_chunk()
    return buf.getvalue()

manifest, total = [], 0
for f in list_files():
    if not FOLDER_ID and not f["name"].startswith(NAME_PREFIXES):
        continue
    revs = list_revs(f["id"])
    by_day = {}                                   # latest revision per calendar day
    for rv in revs:
        day = rv["modifiedTime"][:10]
        by_day[day] = rv                          # later ones overwrite -> last of the day
    stem = f["name"].replace(".ipynb", "").replace("/", "_")
    os.makedirs(f"{OUT}/{stem}", exist_ok=True)
    saved = []
    for day, rv in sorted(by_day.items()):
        try:
            data = fetch(f["id"], rv["id"])
        except Exception:
            continue
        # Strip saved cell outputs to keep the zip tiny (we only need code + dates;
        # full-output notebooks already exist locally for the final versions).
        try:
            nbj = json.loads(data)
            for c in nbj.get("cells", []):
                if c.get("cell_type") == "code":
                    c["outputs"] = []
                    c["execution_count"] = None
            data = json.dumps(nbj).encode()
        except Exception:
            pass
        path = f"{OUT}/{stem}/{rv['modifiedTime'].replace(':','-')}.ipynb"
        open(path, "wb").write(data); total += len(data)
        saved.append(rv["modifiedTime"])
    manifest.append({"name": f["name"], "created": f.get("createdTime"),
                     "modified": f.get("modifiedTime"), "snapshot_days": saved})
    print(f"  {f['name']}: {len(saved)} daily snapshots")

json.dump(manifest, open(f"{OUT}/manifest.json", "w"), indent=2)
print(f"\nTOTAL: {len(manifest)} notebooks, {sum(len(m['snapshot_days']) for m in manifest)} snapshots, {total/1e6:.0f} MB")
zf = "notebook_history_snapshots.zip"
with zipfile.ZipFile(zf, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, fns in os.walk(OUT):
        for fn in fns:
            p = os.path.join(root, fn); z.write(p, os.path.relpath(p, OUT))
print(f"zipped -> {zf}")
files.download(zf)     # lands in your ~/Downloads
