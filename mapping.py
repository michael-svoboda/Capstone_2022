import geopandas as gpd
import plotly.express as px

print('starting program')

'''shp_file = gpd.read_file('Pipelines_SHP/Pipelines_GCS_NAD83.shp')
shp_file.to_file('Pipelines_SHP/Pipelines_GCS_NAD83.geojson', driver='GeoJSON')'''

data = gpd.read_file('Pipelines_SHP/Pipelines_GCS_NAD83.geojson')
print(data["features"][0])

print("made it here")

'''fig = px.choropleth_mapbox(data, geojson=data, color="OUT_DIAMET",
                           locations="geometry", featureidkey="properties.geometry",
                           center={"lat": 45.5517, "lon": -73.7073},
                           mapbox_style="carto-positron", zoom=9)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
'''
