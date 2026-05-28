# Bat Image Variant Creation Instructions

You will create, upload, and document **bat variant images**.

All image processing and uploads must follow the steps below.

---

## Source Images

The user will place source images in:

```
AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/
```

The goal is: the user can provide **only the long image**, and you generate everything else from it.
If a feature-image generator is not available, request a feature image or the script location before continuing.

- Required input: a **long** bat cutout image (wide horizontal bat, ideally with transparency).
- Derived input (you generate if missing): a **feature** composite PNG (1080x1080) made from the long image.

Do not source images from elsewhere.

---

## 1) Find The Long Image

Look in `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/` for the bat’s **long** image.

Typical filenames include `Long` (human naming) or end with `_long.webp` / `_long.png`.

---

## 2) Generate The Feature Image (From Long)

If there is not already a matching **Feature** image in the same folder, generate it from the long image using:

```
python AGENTS/Content_Creation/BAT_LISTINGS_Agent/create_feature_bat.py --input "<LONG_IMAGE_PATH>" --output "<FEATURE_IMAGE_PATH>"
```

Notes:
- `create_feature_bat.py` expects the long image to have transparency (best results come from a cutout with alpha).
- If `create_feature_bat.py` is not present, ask the user for a feature image or the script location before proceeding.
- Save the output **next to the long image** in `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/`.
- Naming: if the long filename contains `Long`, create the feature filename by replacing `Long` → `Feature` (same base name). Otherwise append ` Feature` before the extension.

Example:
- Long: `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/2026 Marucci CATX Rckless Composite USSSA Long 10.webp`
- Feature (generated): `AGENTS/Content_Creation/BAT_LISTINGS_Agent/Image_Processing/2026 Marucci CATX Rckless Composite USSSA Feature 10.png`

---

## 3) Generate Variants + Upload To R2

To generate all image variants and upload them to R2, use:

```
python3 AGENTS/Content_Creation/BAT_LISTINGS_Agent/process_and_upload_bat_images_to_r2.py \
  --year <YEAR> \
  --brand "<BRAND>" \
  --model "<MODEL>" \
  --league <bbcor|usssa|usa|fastpitch> \
  --feature-image "<FEATURE_IMAGE_PATH>" \
  --long-image "<LONG_IMAGE_PATH>"
```

Fill in `<YEAR>`, `<BRAND>`, `<MODEL>`, and `<LEAGUE>` from the matching bat entry in `data/bats.yaml`.

This script:
- Generates all required image sizes (`feature`, `carousel`, `thumb`, `long`, `mobile-long`, `box-long`)
- Uploads each image to R2
- Prints JSON including `static_paths` and `cdn_urls`

Do not manually construct URLs; use the script output.

---

## Image Metadata Storage

Update:

```
data/images.yaml
```

---

## Bat ID Association

Each image set must be associated with the correct bat entry.

To find the correct bat ID, reference:

```
data/bats.yaml
```

Use the existing bat ID as the key in `images.yaml`.

---

## images.yaml Structure

`data/images.yaml` is nested under `images:`. Add/update entries under the correct bat id.

Each bat entry should include these keys:

```yaml
images:
  [BAT_ID]:
    # Optional originals (if provided elsewhere)
    feature_full:
    long_full:

    feature_thumb:
    feature_large:
    feature_carousel:
    long_large:
    long_400:
    long_300:
```

---

## URL Requirements

For generated variants (the `.webp` files), store the `static_paths` values from the script output:

- Must begin with `/static/img/bats/`
- Must end with `.webp`

---

## Constraints and Notes

* Do not overwrite existing image entries unless explicitly instructed
* Do not add image records without a valid bat ID
* All variants must be generated for each bat unless the user specifies otherwise
* Maintain consistent formatting and indentation in `images.yaml`
