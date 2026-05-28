# 05 - Run PeopleNet on One Video (Produce CSV)

Pick one staged MP4:
```bash
PEOPLENET_ROOT="/home/yousuf/PROJECTS/PeopleNet"
STAGE="$PEOPLENET_ROOT/staging/videos"
VID="$(ls -1 "$STAGE"/*.mp4 | head -n 1)"
echo "$VID"
```

Option A) Using deepstream-app (if your config emits structured output):
```bash
CONF="$PEOPLENET_ROOT/configs/peoplenet_ds_config.txt"
deepstream-app -c "$CONF" > "$PEOPLENET_ROOT/logs/ds_one_video.log" 2>&1
# If your config writes per-frame detections to a JSON/CSV file, note the output path(s) and proceed.
```

Option B) Using an existing runner script (if present in your repo), for example:
```bash
# Example placeholder; replace with your runner if you have one:
python3 run_peoplenet_ds.py --video "$VID" --config "$PEOPLENET_ROOT/configs/peoplenet_ds_config.txt" \
  --output-csv "$PEOPLENET_ROOT/Outputs/videos/$(basename "${VID%.mp4}").csv"
```

Expected per-video CSV columns:
```
video_path,frame_ts,obj_id,class,conf,bbox_x,bbox_y,bbox_w,bbox_h
```

Checkpoint (return):
- The per-video CSV path you produced
- `head -n 5` of that CSV
- Count of rows: `wc -l < the_csv`


