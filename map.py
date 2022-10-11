import pandas as pd
import geopandas as gpd
import json
import plotly.express as px

print('Starting program')

geodf = gpd.read_file('Pipelines_SHP/Pipelines_GCS_NAD83.shp')

df = gpd.read_file('Pipelines_SHP/Pipelines_GCS_NAD83.shp')
#df.head()

print(list(df.columns))
# This part is very slow also... :(
geodf.to_file("Pipelines_SHP/Pipelines_GCS_NAD83.geojson", driver = "GeoJSON")
with open("Pipelines_SHP/Pipelines_GCS_NAD83.geojson") as geofile:
    j_file = json.load(geofile)

print('Loaded geojson file.')
print('Creating features')


# This part is very very slow
'''i=1
for feature in j_file["features"]:
    feature ['id'] = str(i).zfill(2)
    i += 1'''

print('Beginning chart creation.')
fig = px.choropleth(df, geojson=j_file, locations='geometry',
                        color='OUT_DIAMET',
                        color_continuous_scale="Viridis",
                        range_color=(0, 12)
                          )

fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#fig.update_geos(fitbounds="locations", visible=True)
fig.show()
print('Done')

