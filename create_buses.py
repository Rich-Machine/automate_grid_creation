import geopandas as gpd
import geoplot
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
from shapely.geometry import Point

region = "ghana_buses"
per_capita_consumption = 1000  # Example value, adjust as needed
country_population = 31072940  # Example value for Ghana, adjust as needed
slack_bus = 1 # Example slack bus, adjust as needed



data_buses = gpd.read_file(
    f"files/export_{region}.geojson"
)

# Add a new column 'centroid' to store the centroid of each geometry
data_buses['centroid'] = data_buses.geometry.centroid.apply(lambda geom: (geom.x, geom.y))

matpower_buses = gpd.GeoDataFrame({
    'bus_i': range(1, len(data_buses) + 1),
    'type': 1,
    'Pd': per_capita_consumption * country_population / len(data_buses.geometry),  # Distribute load evenly
    'Qd': 0,  # Assuming no reactive power demand for simplicity
    'Gs': 0,
    'Bs': 0,
    'area': 1,
    'Vm': 1,
    'Va': 0,
    'base_kV': data_buses.voltage,  # Convert voltage to kV
    'Vmax': 1.1,
    'Vmin': 0.9,
    'coordinates': data_buses['centroid']  # Use the centroid of each row
})

matpower_buses.to_csv(f'matpower_{region}.csv', index=False)
data_buses.to_csv(f'full_overpass_{region}_transmission.csv', index=False)
