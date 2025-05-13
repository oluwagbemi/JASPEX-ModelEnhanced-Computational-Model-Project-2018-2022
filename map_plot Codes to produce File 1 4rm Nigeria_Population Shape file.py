import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


nigeria_shapefile_path = "../../../../../Downloads/Shapefiles/NGA_population_v2_0_admin/NGA_population_v2_0_admin_level1_boundaries.shp"
nigeria = gpd.read_file(nigeria_shapefile_path)
southwestern_states = ['Lagos', 'Ogun', 'Oyo', 'Ondo', 'Ekiti', 'Osun']

sw_states = nigeria[nigeria['statename'].isin(southwestern_states)]  
fig, ax = plt.subplots(figsize=(13, 13))

nigeria.boundary.plot(ax=ax, color='black', linewidth=0.8)
rest_of_nigeria = nigeria[~nigeria['statename'].isin(southwestern_states)]
rest_of_nigeria.plot(ax=ax, color='white', edgecolor='black', linewidth=0.8, label='Other Nigerian States')

colors = list(mcolors.TABLEAU_COLORS.values())  # Use Tableau colors (a set of visually distinct colors)
for i, state in enumerate(southwestern_states):
    state_geo = sw_states[sw_states['statename'] == state]
    state_geo.plot(ax=ax, color=colors[i % len(colors)], edgecolor='black', linewidth=0.8, label=state)
for x, y, label in zip(sw_states.geometry.centroid.x, sw_states.geometry.centroid.y, sw_states['statename']):
    ax.text(x, y, label, fontsize=13, ha='center')

plt.xlabel("Longitude (°E)", fontsize=15)
plt.ylabel("Latitude (°N)", fontsize=15)
plt.savefig('./Nigeria_map3', dpi=300, bbox_inches='tight')
plt.show()