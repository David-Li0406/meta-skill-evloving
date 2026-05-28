# 08 - QC Preview (Optional)

If your pipeline can render annotated frames (bbox overlays), enable a display sink or an image sink in your DeepStream config for a handful of frames per video. Otherwise, sample raw frames and keep CSV side‑by‑side.

Sample command (raw frame extraction with ffmpeg for quick spot checks):
```bash
PEOPLENET_ROOT="/home/yousuf/PROJECTS/PeopleNet"
VCSV="$(ls -1 "$PEOPLENET_ROOT/Outputs/videos"/*.csv | head -n 1)"
VIDB="$(basename "$VCSV" .csv)"
PREV="$PEOPLENET_ROOT/Outputs/preview/$VIDB"
mkdir -p "$PREV"
# Extract 1 frame every 10 seconds from the original MP4 (ensure the MP4 exists in staging or source)
ORIG_MP4="/path/to/Park_F_or_Park_R/${VIDB}.mp4"
ffmpeg -y -i "$ORIG_MP4" -vf fps=1/10 "$PREV/frame_%04d.jpg"
ls -1 "$PREV" | head -n 5
```

Checkpoint (return):
- The preview directory path created
- 3 sample filenames listed from the preview folder


