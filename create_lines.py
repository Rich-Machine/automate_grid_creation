import geopandas as gpd
import geoplot
import pandas as pd
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import LineString
import numpy as np

#######################################
## Now let's do the same for the lines 
#######################################
region = "ghana"
data_lines = gpd.read_file(
    f"files/export_{region}_lines.geojson"
)

data_buses = pd.read_csv(f'matpower_{region}_buses.csv')
bus_coords = data_buses.coordinates
bus_coords = [np.array(eval(coord)) for coord in bus_coords]

one_line = data_lines.geometry[1]
coords = list(one_line.coords)
closest_index = np.argmin([Point(coord).distance(Point(coords[0])) for coord in bus_coords])
print(closest_index)

f_buses = []
t_buses = []
for index, row in data_lines.iterrows():
    line_coords = list(row.geometry.coords)
    f_bus_index = np.argmin([Point(coord).distance(Point(line_coords[0])) for coord in bus_coords])
    f_buses.append(f_bus_index)
    t_bus_index = np.argmin([Point(coord).distance(Point(line_coords[-1])) for coord in bus_coords])
    t_buses.append(t_bus_index)
    print(f"Line {index}: From bus {f_bus_index} to bus {t_bus_index}")



matpower_lines = gpd.GeoDataFrame({
    'f_bus': f_buses,
    't_bus': t_buses,
    'r': 0,  
    'x': 0,  
    'b': 0,
    'rateA': 1000,
    'rateB': 1,
    'rateC': 1,
    'ratio': 0,
    'angle': 0,  # Convert voltage to kV
    'status': 1.1,
    'angmin': 0.9
})

matpower_lines.to_csv(f'matpower_{region}_lines.csv', index=False)


mapping = data_lines.geometry
# ax = geoplot.polyplot(
#     mapping,
#     projection=gcrs.Mercator(),
#     figsize=(12, 8),
#     facecolor='red',
#     linewidth=0.5,
#     alpha=0.3 # Adjust transparency for better visualization
# )

# Plot bus coordinates
for coord in bus_coords:
    plt.plot(coord[0], coord[1], 'b*', markersize=10)  # 'b*' for large blue asterisks
    # Plot lines
    for line in mapping:
        x, y = line.xy
        plt.plot(x, y, color='red', linewidth=1)  # Plot each line in red
plt.show()

bus_coords = data_buses.coordinates

