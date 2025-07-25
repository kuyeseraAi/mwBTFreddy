import csv
import json
import os
import uuid

# This script reads a CSV file of polygon data and converts it to a structured JSON format.

def convert_csv_to_json(input_csv_path):
    # Read the CSV file
    polygons = {}
    with open(input_csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            polygon_id = int(row['polygon_id'])
            if polygon_id not in polygons:
                polygons[polygon_id] = {
                    "xy": [],
                    "lng_lat": [],
                    "status":[]
                }

            map_x = float(row['map_x'])
            map_y = float(row['map_y'])
            pixel_x = float(row['pixel_x'])
            pixel_y = float(row['pixel_y'])
            status = str(row['status'])

            polygons[polygon_id]["xy"].append((pixel_x, pixel_y))
            polygons[polygon_id]["lng_lat"].append((map_x, map_y))
            polygons[polygon_id]["status"].append(status)

    # Creating the output JSON structure
    output_json = {
        "features": {
            "lng_lat": [],
            "xy": []
        },
        "metadata": {
            "disaster": "malawi-cyclone",
            "disaster_type": "cyclone",
            "catalog_id": "10300100841CB50012",
            "original_width": 1024,
            "original_height": 1024,
            "width": 1024,
            "height": 1024,
            "id": str(uuid.uuid4()),
            "img_name": os.path.basename(input_csv_path).replace('.csv', '.png')
        }
    }

    # Converting polygons to WKT format for both lng_lat and xy
    for polygon_id, coordinates in polygons.items():
        uid = str(uuid.uuid4())

        # For lng_lat
        lng_lat_coordinates = ", ".join(f"{x} {y}" for x, y in coordinates["lng_lat"])
        lng_lat_wkt_polygon = f"POLYGON (({lng_lat_coordinates}))"
        status = coordinates["status"][0]
        lng_lat_feature = {
            "properties": {
                "feature_type": "building",
                "subtype": status,
                "uid": uid
            },
            "wkt": lng_lat_wkt_polygon
        }
        output_json["features"]["lng_lat"].append(lng_lat_feature)

        # For xy
        xy_coordinates = ", ".join(f"{x} {y}" for x, y in coordinates["xy"])
        xy_wkt_polygon = f"POLYGON (({xy_coordinates}))"
        
        xy_feature = {
            "properties": {
                "feature_type": "building",
                "subtype": status,
                "uid": uid
            },
            "wkt": xy_wkt_polygon
        }
        output_json["features"]["xy"].append(xy_feature)

    return output_json

# Processing all CSV files in a folder and converting each to a JSON file.
def process_csv_folder(input_folder_path, output_folder_path):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(input_folder_path):
        if filename.endswith('.csv'):
            input_csv_path = os.path.join(input_folder_path, filename)
            print(input_csv_path)
            output_json = convert_csv_to_json(input_csv_path)
            output_file_path = os.path.join(output_folder_path, filename.replace('.csv', '.json'))
            with open(output_file_path, 'w') as output_file:
                json.dump(output_json, output_file, indent=2)


# Specify the input folder containing CSV files
timeline = 'post'
input_folder_path = f'/path/to/your/csv/folder'  # <-- Set your own input folder path here

# Specify the output folder to save converted JSON files
output_folder_path = f'/path/to/save/json/files'  # <-- Set your own output folder path here

# Call the processing function
process_csv_folder(input_folder_path, output_folder_path)
print(f"JSON files saved to {output_folder_path}")