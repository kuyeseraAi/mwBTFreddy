# TIFF to JPEG Conversion and Black Region Cropping

This script processes multi-band satellite TIFF images by:
- Converting them to 8-bit RGB JPEGs
- Applying percentile-based contrast stretching
- Cropping out large black or no-data regions

---

## What This Script Does

- Reads selected bands (e.g. R, G, B) from multi-band `.tif` satellite images
- Scales pixel values based on specified percentile thresholds
- Crops out low-brightness areas (e.g. black/no-data margins)
- Saves clean `.jpg` outputs suitable for visualization or downstream tasks

---

## How to Use

### 1. Prepare Your TIFF Images
Place your input `.tif` or `.tiff` files in a folder, e.g. `sample_tiff_input/`.

### 2. Run the Script

```bash
python convert_and_crop.py
