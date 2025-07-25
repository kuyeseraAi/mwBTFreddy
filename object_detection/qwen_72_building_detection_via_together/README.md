## Building Count from Satellite Images using Together QWEN_72 VLM

This script processes satellite `.jpg` images using Qwen_72 VLM hosted on **Together.ai**, and estimates the **number of buildings** visible in each image.

---

### What This Script Does

- Loads images from a specified input directory.
- Converts each image to base64 format.
- Sends the image to Together's Qwen_72 model with a prompt asking for the **number of distinct buildings**.
- Extracts the from the model's response.
- Saves the predicted number as a `.txt` file named after the image, in an output directory.

---

## How To Use

### 1. Get Together API Key
- Register for an account on [https://www.together.ai/](https://www.together.ai/) and generate an API key.
- Assign your key to the `os.environ['TOGETHER_API_KEY']` variable in the notebook.
- **NOTE:** This project is for research and educational purposes only. Be sure to comply with the Together.ai terms of use when using their API.

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
pip install Together
```

### 4. Run The Script
Run the `qwen_72_building_detection_via_together.ipynb` notebook

### 5. Output
For each input image, a .txt file is saved in: `sample_output/qwen_72_outputs/`