from qgis.core import QgsProject, QgsCoordinateTransform, QgsPointXY, QgsGeometry
import csv
import geopandas as gpd
from pyproj import Proj, transform
#from geopy.distance import distance


# Function to convert map coordinates to pixel coordinates with floating point precision
def map_to_pixel(point, geotransform, width, height):
    x, y = point
    px = (x - geotransform[0]) / geotransform[1]
    py = (y - geotransform[3]) / geotransform[5]
    
    px = min(max(px, 0), width - 1)
    py = min(max(py, 0), height - 1)
    return px, py
def map_distance_to_pixel(point, distance_transform, width, height):
    x, y = point
    px = (x - distance_transform[0]) / distance_transform[1]
    py = (y - distance_transform[3]) / distance_transform[5]
    # Ensure pixel coordinates are within image bounds
    px = min(max(px, 0), width - 1)
    py = min(max(py, 0), height - 1)
    return px, py
def measure_distance(lat1, lon1, lat2, lon2):
    dist_in_meters = ((lat2 - lat1)**2 + (lon2 - lon1)**2)**0.5
    return dist_in_meters
    
timeline = 'post'
layer_name = f'malawi-cyclone_00000005_{timeline}_disaster'
output_path = f'/path/to/save/csv/files/{layer_name}.csv'  # <-- Set your own output CSV path here


# Load the georeferenced raster layer
raster_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
raster_extent = raster_layer.extent()
raster_transform = raster_layer.transformContext()
raster_crs = raster_layer.crs()

# Load the vector layer (labeled polygons)
vector_layer = QgsProject.instance().mapLayersByName(f'{layer_name}_labels')[0]

# Define the projected CRS (e.g., UTM zone appropriate for your location)
projected_crs = QgsCoordinateReferenceSystem("EPSG:32737")  # Replace with appropriate UTM zone

# Coordinate transformation from vector CRS to projected CRS
vector_crs = vector_layer.crs()
transform_to_projected = QgsCoordinateTransform(vector_crs, projected_crs, QgsProject.instance())

# Coordinate transformation from projected CRS to raster CRS
transform_to_raster = QgsCoordinateTransform(projected_crs, raster_crs, QgsProject.instance())


provider = raster_layer.dataProvider()
extent = provider.extent()

# Get the raster geotransform
# Transform the four corners of the extent
bottom_left = QgsPointXY(extent.xMinimum(), extent.yMinimum())
bottom_right = QgsPointXY(extent.xMaximum(), extent.yMinimum())
top_left = QgsPointXY(extent.xMinimum(), extent.yMaximum())
top_right = QgsPointXY(extent.xMaximum(), extent.yMaximum())

bottom_left_proj = transform_to_projected.transform(bottom_left)
bottom_right_proj = transform_to_projected.transform(bottom_right)
top_left_proj = transform_to_projected.transform(top_left)
top_right_proj = transform_to_projected.transform(top_right)

# Calculate the geotransform using projected coordinates
width = provider.xSize()
height = provider.ySize()

geotransform = (
    bottom_left_proj.x(), (bottom_right_proj.x() - bottom_left_proj.x()) / width, 0,
    top_left_proj.y(), 0, (bottom_left_proj.y() - top_left_proj.y()) / height
)

x_distance = measure_distance(top_left.x(), top_left.y(), top_right.x(),top_right.y())
y_distance = measure_distance(top_left.x(), top_left.y(), bottom_left.x(),bottom_left.y())
distance_transform = (
    0, (x_distance) / width, 0,
    0, 0, (y_distance) / height
)


with open(output_path, 'w', newline='') as csvfile:
    fieldnames = ['polygon_id', 'point_index', 'point_map_x', 'point_map_y', 'point_pixel_x', 'point_pixel_y']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for feature in vector_layer.getFeatures():
        geometry = feature.geometry()
        print(feature.id())
        polygon_id = feature.id()
        
        if geometry.isMultipart():
            polygons = geometry.asMultiPolygon()
        else:
            polygons = [geometry.asPolygon()]
        print("within")
        for polygon in polygons:
            for ring in polygon:
                for point_index, point in enumerate(ring):
                    
                    map_point = QgsPointXY(point)
                    projected_point = transform_to_projected.transform(map_point)
                    x_dist = measure_distance(top_left.x(),0,map_point.x(),0)
                    y_dist = measure_distance(0,top_left.y(),0,map_point.y())
                    
                    raster_point = transform_to_raster.transform(projected_point)
                    
                    pixel_coords = map_to_pixel((projected_point.x(), projected_point.y()), geotransform, width, height)
                    
                    pixel_coords = map_distance_to_pixel((x_dist,y_dist), distance_transform, width, height)
                    
                    writer.writerow({
                        'polygon_id': polygon_id,
                        'point_index': point_index,
                        'point_map_x': raster_point.x(),
                        'point_map_y': raster_point.y(),
                        'point_pixel_x': pixel_coords[0],
                        'point_pixel_y': pixel_coords[1]
                    })

print(f"Polygon point pixel coordinates with decimal places have been saved to '{layer_name}.csv'")
