# 07 - Consolidate Detections and Update Central Log

Merge all per-video CSVs into a consolidated CSV (dedupe on video_path, frame_ts, obj_id):

```bash
python3 - <<'PY'
import os, glob, pandas as pd
root="/home/yousuf/PROJECTS/PeopleNet"
vdir=os.path.join(root,"Outputs","videos")
cons=os.path.join(root,"Outputs","peoplenet_consolidated.csv")
files=sorted(glob.glob(os.path.join(vdir,"*.csv")))
dfs=[]
for f in files:
    try: dfs.append(pd.read_csv(f))
    except Exception: pass
if not dfs:
    print("no_csvs"); raise SystemExit(0)
big=pd.concat(dfs, ignore_index=True, sort=False)
subset=[c for c in ["video_path","frame_ts","obj_id"] if c in big.columns]
if subset:
    big.drop_duplicates(subset=subset, inplace=True)
big.to_csv(cons, index=False)
print("consolidated_rows", len(big))
PY
```

Update central log:
```bash
python3 - <<'PY'
import os, glob, pandas as pd, datetime as dt
root="/home/yousuf/PROJECTS/PeopleNet"
vdir=os.path.join(root,"Outputs","videos")
log=os.path.join(root,"Outputs","central_log.xlsx")
rows=[]
for f in sorted(glob.glob(os.path.join(vdir,"*.csv"))):
    try:
        df=pd.read_csv(f)
        persons=int((df["class"]=="person").sum()) if "class" in df.columns else None
        rows.append({
          "video_filename": os.path.basename(f).replace(".csv",".mp4"),
          "processed_date": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
          "frames_scanned": len(df),
          "persons_detected": persons
        })
    except Exception:
        pass
if rows:
    pd.DataFrame(rows).to_excel(log, index=False)
    print("central_log_rows", len(rows))
else:
    print("central_log_rows", 0)
PY
```

Checkpoint (return):
- consolidated_rows count
- central_log_rows count
- `head -n 5` of `peoplenet_consolidated.csv`


