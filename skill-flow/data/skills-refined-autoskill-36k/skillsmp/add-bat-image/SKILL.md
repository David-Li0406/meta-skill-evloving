---
name: add-bat-image
description: Attach or upload bat images for BatDigest by generating a feature image from a long cutout, creating image variants, uploading to R2, and updating data/images.yaml. Use when asked to add/attach/upload bat images, generate bat image variants, or update images.yaml entries for a bat listing.
---

# Add Bat Image

## Overview

Generate BatDigest image variants from a provided long cutout, upload them to R2, and register the resulting static paths in `data/images.yaml` for the correct bat id.

## Workflow

1) Confirm the target bat and images
- Verify the bat id in `data/bats.yaml` and capture `year`, `brand`, `model`, and `league`.
- Require a long cutout image in `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/`.
- If a matching feature image is already present, use it; otherwise generate it.

2) Generate a feature image (if missing)
- Run `create_feature_bat.py` and save the output next to the long image.
- Naming rule: if the long filename contains `Long`, replace with `Feature`; otherwise append ` Feature` before the extension.

3) Generate variants and upload to R2
- Run `process_and_upload_bat_images_to_r2.py` using the bat metadata and the feature/long image paths.
- Capture the `static_paths` output from the script (do not hand-write URLs).

4) Update `data/images.yaml`
- Add a new entry under `images: <BAT_ID>:` if missing.
- Set `feature_large`, `feature_carousel`, `feature_thumb`, `long_large`, `long_400`, and `long_300` using the script output.
- Keep `feature_full` and `long_full` blank unless original source paths are provided.
- Do not overwrite existing image entries unless the user explicitly requests it.

## Paths and Commands

Repository defaults:
- Repo root: `~/Coding_Projects/batdigest-flask`
- Images staging: `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/`

Commands:
```bash
python AGENTS/Content_Creation/BAT_LISTINGS_Agent/create_feature_bat.py --input "<LONG_IMAGE_PATH>" --output "<FEATURE_IMAGE_PATH>"
```

```bash
python3 AGENTS/Content_Creation/BAT_LISTINGS_Agent/process_and_upload_bat_images_to_r2.py \
  --year <YEAR> \
  --brand "<BRAND>" \
  --model "<MODEL>" \
  --league <bbcor|usssa|usa|fastpitch> \
  --feature-image "<FEATURE_IMAGE_PATH>" \
  --long-image "<LONG_IMAGE_PATH>"
```

## References

For full details and edge cases, read `references/Bat_Image_Attach_Agent.md`.
