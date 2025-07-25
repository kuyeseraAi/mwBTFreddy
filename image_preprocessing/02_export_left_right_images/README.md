# TIFF Splitter: Vertical Halving and Black Region Cropping

This script processes splits tiff images into left and right halves:  
- Detecting the top boundary of a black (no-data) region  
- Cropping out everything below that black section  
- Splitting the remaining image vertically into left and right halves  
- Saving each half as a separate PNG

---

## What This Script Does

- Reads `.tif` files that end with `_pre_disaster.tif` from a folder
- Scans each image top-down to detect the first full black row
- Crops the image at that black boundary
- Splits the upper portion into left and right halves
- Saves the results as `.png` images in an output directory

---

## How to Use

### 1. Prepare Your TIFF Images
- Use the provided folder already included in this repository (`sample_tiff_input/`) and put it in the same folder as the notebook
- **OR** update the `tif_image_location` variable to point to your own directories

### 2. Run the Script

Run the `export_left_right_images.ipynb` notebook
