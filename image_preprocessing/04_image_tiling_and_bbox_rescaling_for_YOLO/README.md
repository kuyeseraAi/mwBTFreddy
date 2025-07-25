# Image Upscaling, Tiling, and Bounding Box Conversion (CSV + YOLO)

This script processes `.jpg` images and their associated `.csv` bounding boxes by:  
- Upscaling images and bounding boxes by a given factor  
- Tiling the upscaled images into smaller fixed-size patches  
- Clipping and shifting bounding boxes to fit within each tile  
- Saving each tile with bounding boxes in both **CSV** and **YOLO** formats  
- Optionally displaying tiles with bounding boxes for visual verification

---

## What This Script Does

- Upscales RGB JPEG images using bicubic interpolation
- Multiplies bounding box coordinates by the same upscaling factor
- Splits upscaled images into non-overlapping tiles (e.g., 1024×512)
- Clips and shifts bounding boxes into tile-local coordinates
- Saves:
  - Tiled images (`.jpg`)
  - Tiled bounding boxes as `.csv` (all feature types)
  - Tiled bounding boxes in YOLO format (`.txt`) for `"building"` only
- Optionally skips tiles that contain no `"building"` boxes
- Includes a visual inspection tool using `matplotlib`

---

## How to Use

### 1. Organize Your Input Data

- Use the provided folders already included in this repository (`sample_input/images/` and `sample_input/labels/`) and put them in the same folder as the script  
- **OR** update the `input_images_dir` and `input_csv_dir` variables to point to your own directories

### 2. Organize Your Output Locations

- Use the provided folders already included in this repository (`sample_output/images/`, `sample_output/labels_csvs/`, and `sample_output/labels_yolo/`)  
- **OR** update the `output_images_dir`, `output_csv_dir`, and `output_yolo_dir` variables to point to your own directories

### 3. Install Dependencies

```bash
pip install numpy pillow rasterio matplotlib shapely
```
### 4. Run the notebook

- Run the notebook `image_tiling_and_bbox_rescaling_for_YOLO.ipynb`
- You can change the name of the jpg image to visualize by changing the name in the notebook
