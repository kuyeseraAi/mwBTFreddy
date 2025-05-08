import simplekml
from shapely.geometry import Polygon, Point

def create_grid_without_labels(kml_file, polygon_coords, lat_spacing, lon_spacing):
    kml = simplekml.Kml()

    # Create the polygon
    polygon = Polygon(polygon_coords)

    # Get the bounding box of the polygon
    minx, miny, maxx, maxy = polygon.bounds

    # Create horizontal and vertical lines as polygons
    lat = miny
    while lat <= maxy:
        lon = minx
        while lon <= maxx:
            if polygon.contains(Point(lon, lat)):
                box_coords = [
                    (lon, lat),
                    (lon + lon_spacing, lat),
                    (lon + lon_spacing, lat + lat_spacing),
                    (lon, lat + lat_spacing),
                    (lon, lat)
                ]
                if polygon.intersects(Polygon(box_coords)):
                    grid_polygon = kml.newpolygon()
                    grid_polygon.outerboundaryis = box_coords
                    grid_polygon.style.polystyle.color = simplekml.Color.changealphaint(0, simplekml.Color.red)  # Fully transparent fill
                    grid_polygon.style.polystyle.fill = 0  # No fill
                    grid_polygon.style.linestyle.color = simplekml.Color.red
                    grid_polygon.style.linestyle.width = 2  # Line width

            lon += lon_spacing
        lat += lat_spacing

    kml.save(kml_file)
    print(f"KML file saved as: {kml_file}")

# Replace "output.kml" with your desired output file name
kml_filename = "output.kml"

# Replace with your own coordinates
polygon_coords = [
    (35.00004428168152, -15.82503923829606),
    (35.04009739154355, -15.82507457317074),
    (35.04012666318832, -15.85010734237624),
    (35.00015291121928, -15.85003454786558),
]

# Call the function with desired spacings
create_grid_without_labels(kml_filename, polygon_coords, 0.001, 0.002)
