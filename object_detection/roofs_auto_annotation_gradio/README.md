## Roof Detection and Auto-Annotation using Gradio Client

This script uses a hosted **Gradio demo** (via `gradio_client`) to automatically detect rooftops in satellite `.jpg` images and generate both **annotations** and **annotated images** using the model from:  
[Yifeng-Liu/satellite-image-roofs-auto-annotation](https://huggingface.co/spaces/Yifeng-Liu/satellite-image-roofs-auto-annotation)

---

### What This Script Does

- Loads each image from a specified input directory
- Sends the image to the Gradio API via `gradio_client`
- Retrieves:
  - A `.json` annotation file containing building polygons
  - A `.webp` image with rooftops overlaid (visual output)
- Saves both results into an output directory with filenames based on the original image

---

### 1. Install Dependencies

Install the required package using pip:

```bash
pip install gradio_client
```

### 2. Organize Your Input Data
- Place all .jpg satellite images in the `sample_input/jpg_images/` folder (relative to script): 
- OR edit the `img_dir` variable in the script to point to your custom folder:

### 3. Run the Script

Run `roofs_auto_annotation_yifeng_liu_api.ipynb` notebook

### 4. Output

The script creates a `sample_output` directory containing an image with rooftop overlays and a corresponding .json file with annotations for each processed input image.
