# Building Damage Detection and Classification

This repository contains code for detecting buildings in satellite imagery and classifying their damage levels after disasters.

## Overview

The pipeline consists of two main stages:

1. **Object Detection**: Detects buildings in pre-disaster and post-disaster satellite images using YOLO models
2. **Damage Classification**: Classifies detected buildings into damage categories using a siamese network architecture

## Features

- Dual-model detection with Weighted Boxes Fusion (WBF) for improved building detection
- Damage classification using:
  - Visual differences between pre/post-disaster images
  - NDVI (Normalized Difference Vegetation Index) data
- Annotated output generation showing damage classification
- Submission file generation for evaluation

## Requirements

- Python 3.7+
- PyTorch
- Ultralytics YOLO
- Albumentations
- OpenCV
- Pandas
- ensemble-boxes

## Installation

```bash
pip install ultralytics torch albumentations opencv-python pandas ensemble-boxes
```

## Usage

1. Prepare your input data:
   - Place pre-disaster images in `data/sample_jpg_images/` with `_pre_disaster.jpg` suffix
   - Place post-disaster images in same directory with `_post_disaster.jpg` suffix
   - Prepare NDVI data in CSV format at `data/test_ndvi.csv`
   - Prepare model weights:
        - YOLO model for building detection (default path: `data/yolo_weights/best.pt`)
        - EfficientViT-based siamese classifier (default path: `data/classifier_weights/efficientvit_b0.r224_in1k_3_patch_model_fold_0.pth`)

    The input data should mirror the following folder structure

   ```
    data/
        ├── sample_jpg_images/              # Input satellite images
        │   ├── [image_id]_pre_disaster.jpg
        │   ├── [image_id]_post_disaster.jpg
        │   └── ...
        ├── yolo_weights/                   # YOLO model weights
        │   └── best.pt
        ├── classifier_weights/             # Damage classifier weights
        │   └── efficientvit_b0.r224_in1k_3_patch_model_fold_0.pth
        ├── test_ndvi.csv                   # NDVI data for classification
    ```

3. Run the notebook `detection_classification_inference.ipynb`

## Outputs

The script generates:
- Cropped building images in `data/cropped_images/`
- Annotated images showing damage classification in `data/annotated_images/`
- A submission CSV file at `data/sample_inference_output.csv`
- Intermediate data pickle at `data/data_pkl_path.pkl`

## Configuration

Key parameters you can adjust:
- `THRESH`: Confidence threshold for detection (default: 0.5)
- `IOU_THRESH`: IoU threshold for WBF (default: 0.2)
- `CONF`: YOLO confidence threshold (default: 0.5)
- `AUGMENT`: Whether to use test-time augmentation (default: True)
- `CLASSIFIER_SZ`: Input size for classifier (default: 128)


## Damage Categories

Buildings are classified into:
- No damage (green in output images)
- Destroyed (red in output images)

Note: This implementation focuses on binary classification (no damage vs destroyed) but can be extended to multi-class.

## Troubleshooting

- Ensure all input paths are correct
- Verify all required packages are installed
- Check that input images follow the required naming convention
- If NDVI data is missing for some images, those images will be skipped