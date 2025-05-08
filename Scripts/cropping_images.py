import os
import tifffile as tiff
from osgeo import gdal, osr
import numpy as np
import pandas as pd
from skimage.util import crop
from skimage.draw import polygon

# Constants for cropping and padding
BLEED = 10
PAD = True
CENTER = False
BOTTOM = 4.5  # Adjust this based on your image characteristics

# Returns the second smallest number in a list
def second_min(numbers):
    unique_numbers = list(numbers)
    if len(unique_numbers) < 2:
        return min(numbers)
    unique_numbers.sort()
    return unique_numbers[1]
    
# Returns the second largest number in a list
def second_max(numbers):
    unique_numbers = list(numbers)
    if len(unique_numbers) < 2:
        return max(numbers)
    unique_numbers.sort(reverse=True)
    return unique_numbers[1]

# Crops the image using the coordinates from a points file and pads to 1024x1024 if needed
def crop_image(image, points):
    x_coords, y_coords = points[:, 0], np.abs(points[:, 1])
    
    coords = np.array([x_coords, y_coords]).T
    coords = coords[np.argsort(coords[:, 0])]
    
    x_coords, y_coords = coords.T
    height, width = image.shape[1], image.shape[2]
    x_coords = np.clip(x_coords, 0, width - 1)
    y_coords = np.clip(y_coords, 0, height - 1)
    
    mask = np.zeros((height, width), dtype=np.uint8)
    rr, cc = polygon(y_coords, x_coords, mask.shape)
    mask[rr, cc] = 1
    
    start_lon = points[:, 2][0]
    start_lat = points[:, 3][0]
    residual_x = np.ceil(np.max(points[:, 4])/10).astype(int)
    if residual_x < 1:
        residual_x = 2
        
    residual_y = np.ceil(np.max(points[:, 5])/10).astype(int)  
    if residual_y < 1:
        residual_y = 1
    
    polygon_image = np.zeros((image.shape[0], mask.shape[0], mask.shape[1]), dtype=image.dtype)
    for band in range(image.shape[0]):
        polygon_image[band][mask == 1] = image[band][mask == 1]
    
    x_min, y_min = second_min(x_coords), second_min(y_coords)
    x_max, y_max = second_max(x_coords), second_max(y_coords)
    
    y_min = np.floor(y_min).astype(int) + (BLEED * 1)
    y_max = (np.ceil(y_max).astype(int) - (BLEED * (1 * BOTTOM))).astype(int)
    x_min = np.floor(x_min).astype(int) + (BLEED * 1)
    x_max = np.ceil(x_max).astype(int) - (BLEED * 1)
    
    cropped_image = image[:, y_min:y_max, x_min:x_max]
    
    if PAD == False:
        return cropped_image, start_lat, start_lon, 0, 0
    
    new_image = np.zeros((image.shape[0], 1024, 1024), dtype=image.dtype)
    
    cropped_height, cropped_width = cropped_image.shape[1], cropped_image.shape[2]
    if CENTER:
        y_offset = (1024 - cropped_height) // 2
        x_offset = (1024 - cropped_width) // 2
    else:
        y_offset = 0
        x_offset = 0
    
    new_image[:, y_offset:y_offset + cropped_height, x_offset:x_offset + cropped_width] = cropped_image
    
    return new_image, start_lat, start_lon, x_offset, y_offset

# Saves a cropped image as a GeoTIFF with updated georeferencing info
def save_geotiff(image_file, image, geotransform, projection, start_lat, start_lon, output_folder, x_offset=0, y_offset=0):
    driver = gdal.GetDriverByName('GTiff')
    bands, height, width = image.shape
    output_path = os.path.join(output_folder, os.path.basename(image_file))
    dataset = driver.Create(output_path, width, height, bands, gdal.GDT_Byte)
    if dataset is None:
        print(f"Failed to create file: {output_path}")
        return

    pixel_width = geotransform[1]
    pixel_height = geotransform[5]

    new_geotransform = list(geotransform)
    print(list(new_geotransform))
    new_geotransform[0] = start_lon - (x_offset * pixel_width) + (BLEED * pixel_width)
    new_geotransform[3] = start_lat - (y_offset * pixel_height) - (BLEED * pixel_width)
    print(y_offset)
    print(list(new_geotransform))
    dataset.SetGeoTransform(new_geotransform)
    dataset.SetProjection(projection)

    for i in range(bands):
        dataset.GetRasterBand(i + 1).WriteArray(image[i])

    dataset.FlushCache()
    dataset = None

# Reads a GeoTIFF and returns its image array, geotransform, and projection
def read_geotiff(image_file):
    dataset = gdal.Open(image_file)
    geotransform = dataset.GetGeoTransform()
    projection = dataset.GetProjection()
    image = dataset.ReadAsArray()
    return dataset, image, geotransform, projection

# Reads the .points file containing cropping coordinates
def read_points_file(points_file):
    df = pd.read_csv(points_file, skiprows=1)
    points = df.head(4)
    return points[['sourceX', 'sourceY','mapX','mapY','dX','dY']].values

# Reading, cropping, and saving a single image
def process_image(image_file, points_file, output_folder):
    with tiff.TiffFile(image_file) as tif:
        image = tif.asarray()
        tags = {tag.name: tag.value for tag in tif.pages[0].tags.values()}
    
    dataset, image, geotransform, projection = read_geotiff(image_file)
    points = read_points_file(points_file)
    cropped_image, start_lat, start_lon, x_offset, y_offset = crop_image(image, points)
    
    if 'ModelTiepointTag' in tags:
        tiepoints = np.array(tags['ModelTiepointTag'])
        tags['ModelTiepointTag'] = tuple(tiepoints)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    save_geotiff(image_file, cropped_image, geotransform, projection, start_lat, start_lon, output_folder, x_offset, y_offset)
    print(f"Cropped image saved to {output_folder}")

# Processes all images in a folder by matching them with .points files
def main(folder, output_folder):
    for file in os.listdir(folder):
        if (file.endswith(".tif") or file.endswith(".tiff")) and "_cropped" not in file:
            image_file = os.path.join(folder, file)
            points_file = os.path.splitext(image_file)[0] + '.points'
            alt_points_file = os.path.splitext(image_file)[0] + '.jpg.points'
            if os.path.exists(points_file):
                process_image(image_file, points_file, output_folder)
            elif os.path.exists(alt_points_file):
                process_image(image_file, alt_points_file, output_folder)
            else:
                print(f"Error: Points file {points_file} does not exist")

# Set your input and output folders here
input_folder = 'C:/path/to/your/georeferencing_images'   # Folder with GeoTIFF images
output_folder = 'C:/path/to/your/cropped_images'         # Folder to save cropped GeoTIFFs

main(input_folder, output_folder)
print(f"Cropped images saved to {output_folder}")
