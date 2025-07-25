# Satellite TIFF to JPEG Conversion with Bounding Box Extraction and Visualization

This script processes satellite `.tif` images and their associated `.json` annotations by:  
- Converting TIFFs to RGB JPEGs with contrast stretching  
- Extracting bounding boxes from polygon WKT in JSON files and saving them to CSV  
- Displaying images with bounding boxes for visual verification  

---

## What This Script Does

- Converts multi-band satellite TIFF images to 8-bit RGB JPEGs
- Applies percentile-based contrast stretching for better visibility
- Supports custom band selection (e.g., RGB, BGR, etc.)
- Parses polygon annotations from JSON files to extract bounding boxes
- Saves bounding boxes to CSV files (per image)
- Displays annotated images with bounding boxes using `matplotlib`

---

## How to Use

### 1. Organize Your Input Data

- Use the provided folders already included in this repository (`sample_input/xview_images/` and `sample_input/buildings_labels/`) and put them in the same folder as the notebook
- **OR** update the `input_images_path` and `input_labels_path` variables to point to your own directories

### 2. Organize Your Ouput Locations

- Use the provided folders already included in this repository (`sample_output/jpeg_images/` and `sample_output/bbox_csv`)
- **OR** update the `output_images_path` and `output_labels_path` variables to point to your own directories
  
### 3. Install dependency

```bash
pip install numpy pillow rasterio matplotlib shapely
```
### 4. Run the notebook

- Run the notebook `tiff_to_jpeg_bbox_export_viewer.ipynb`
- You can change the name of the jpg image to visualize by changing the name in the notebook