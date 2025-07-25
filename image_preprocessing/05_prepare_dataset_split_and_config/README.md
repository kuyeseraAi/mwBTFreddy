## Building Count from Satellite Images using Fireworks LLaMA VLM

This script processes satellite `.jpg` images using a Visual Language Model (VLM) hosted on **Fireworks.ai**, and estimates the **number of buildings** visible in each image.

---

### What This Script Does

- Loads images from a specified input directory.
- Converts each image to base64 format.
- Sends the image to Fireworks' LLaMA model with a prompt asking for the **number of distinct buildings**.
- Extracts the **first number** from the model's response (assuming it represents the count).
- Saves the predicted number as a `.txt` file named after the image, in an output directory.

---

## How To Use

### 1. Get Fireworks API Key

- Register for an account on [https://fireworks.ai](https://fireworks.ai) and generate an API key.
- Assign your key to the `fireworks.client.api_key` variable in the script or notebook.
- **NOTE:** This project is for research and educational purposes only. Be sure to comply with the Fireworks.ai terms of use when using their API.

---

### 2. Organize Your Input Data

- Use the provided folder structure included in this repository:  
  `sample_input/jpg_images/`
- Place all your `.jpg` satellite images inside that folder.  
- **OR** update the `image_dir` variable in the script to point to your own image directory.

---

### 3. Install Dependencies

Install the required Python package:

```bash
pip install fireworks-ai
```

### 4. Run The Script
Run the `llama_building_detection_via_fireworks.ipynb` notebook

### 5. Output
For each input image, a .txt file is saved in: `sample_output/fireworks_llama11b_outputs/`