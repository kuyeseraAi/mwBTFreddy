import os
import shutil
import re

# Used to sort filenames in a "natural" order (e.g., file2 comes before file10)
def natural_key(string):
    return [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', string)]

# Copy the TIFF file to the new output path and log the mapping
def rename_tiff(image_path, output_path, mapping_summary):
    shutil.copy(image_path, output_path)
    print(f"Copied {image_path} => {output_path}")
    mapping_summary.write(f"{os.path.basename(image_path)},{os.path.basename(output_path)}\n")

# Process all subfolders and rename paired TIFF files (pre and post disaster)
def process_folder(input_folder, output_folder, mapping_summary):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_pairs = {}

    for root, _, files in os.walk(input_folder):
        files.sort(key=natural_key)
        for filename in files:
            if filename.lower().endswith(('.tif', '.tiff')):
                try:
                    base_name, timeline = os.path.splitext(filename)[0].rsplit('_', 1)
                except ValueError:
                    print(f"Skipped (unexpected format): {filename}")
                    continue

                if base_name not in image_pairs:
                    image_pairs[base_name] = {}

                image_pairs[base_name][timeline] = os.path.join(root, filename)
            else:
                print(f"Skipped (unsupported format): {filename}")

    counter = 0
    for base_name, images in image_pairs.items():
        if 'pre' in images and 'post' in images:
            pre_output_filename = f"malawi-cyclone_{counter:08d}_pre_disaster.tif"
            post_output_filename = f"malawi-cyclone_{counter:08d}_post_disaster.tif"
            
            pre_output_path = os.path.join(output_folder, pre_output_filename)
            post_output_path = os.path.join(output_folder, post_output_filename)

            rename_tiff(images['pre'], pre_output_path, mapping_summary)
            rename_tiff(images['post'], post_output_path, mapping_summary)
            
            counter += 1 
        else:
            print(f"Missing pair for: {base_name}")

# === Edit below with your actual paths ===
input_folder = '/path/to/your/tiff/folder'      # Folder containing original TIFFs
output_folder = '/path/to/save/renamed/files'   # Destination folder for renamed files
print(f"Saving renamed TIFFs to: {output_folder}")

mapping_summary = open("mapping_summary.txt", "a")
mapping_summary.write("from,to\n")

process_folder(input_folder, output_folder, mapping_summary)

mapping_summary.close()

print("Processing complete.")
