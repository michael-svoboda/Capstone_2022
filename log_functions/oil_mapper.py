import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pykrige.kriging_tools as kt
from pykrige.ok import OrdinaryKriging

# Going to import a 

data = pd.read_csv('log_functions/Log_Duvernay_Tops.csv')
dev_sur = pd.read_csv('log_functions/Well_Deviation_Survey_5_11_pad.csv')

fig = go.Figure()
porosity_maps = make_subplots(rows=1, cols=4, subplot_titles= ['Phi_eff_80-82', 'Phi_eff_82-84', 'Phi_eff_84-87', 'Phi_eff_87-90', 'k_80-82', 'k_82-84', 'k_84-87', 'k_87-90'])
permeability_maps = make_subplots(rows=1, cols=4, subplot_titles= ['k_80-82', 'k_82-84', 'k_84-87', 'k_87-90'])
contour_plot = go.Figure()

def kriging_interpolate(figure, df, z_col, position, parameters, contour_params, var_type, wells_added):
    data = df.dropna()
    OK = OrdinaryKriging(
        x=data['Long'],
        y=data['Lat'],
        z = data[z_col],
        variogram_model= var_type,
        variogram_parameters = parameters,
        verbose=True,
        #enable_plotting= True
    )
    gridx = np.arange(116.52444, 116.81692, 0.00146239999999992, dtype='float64')
    gridy = np.arange(54.26932, 54.39836, 0.000645200000000017, dtype='float64')
    zstar, ss = OK.execute("grid", gridx, gridy)

    figure.add_trace(go.Contour(
        z=zstar,
        x=gridx, # horizontal axis
        y=gridy, # vertical axis
        contours=contour_params
    ),

    row=position[0], col=position[1])

    figure.add_trace(go.Scatter(
        x=data['Long'], y=data['Lat'],
        #name='Wells',
        mode='markers',
        marker_color= 'red',
        marker_size = 10,
    ),
    row=position[0], col=position[1])

    if wells_added:
        for well in dev_sur['UWI']:
            survey = dev_sur[dev_sur['UWI'] == well]
            figure.add_trace(go.Scatter(
                x=survey['Long'], y=survey['Lat'],
                #name = well,
                mode='lines',
                marker_color= '#00CC96',
                #marker_size = 10,
            ),
        row=position[0], col=position[1])

porosity_parameters = [20, 0.5, 7.799400370621302e-12]
permeabilty_parameters = [2, 0.15, 7.799400370621302e-11]

porosity_contour_params = dict(
                start=1.9,
                end=20,
                size=1.75)

perm_contour_params = dict(
                start=300,
                end=600,
                size=25)

perm_type = 'spherical'

# adding traces to porosity map
kriging_interpolate(porosity_maps, data, 'Phi_eff_80-82', [1, 1], porosity_parameters, porosity_contour_params, 'exponential', True)
kriging_interpolate(porosity_maps, data, 'Phi_eff_82-84', [1, 2], porosity_parameters, porosity_contour_params,'exponential', True)
kriging_interpolate(porosity_maps, data, 'Phi_eff_84-87', [1, 3], porosity_parameters, porosity_contour_params,'exponential', True)
kriging_interpolate(porosity_maps, data, 'Phi_eff_87-90', [1, 4], porosity_parameters, porosity_contour_params,'exponential', True)

kriging_interpolate(permeability_maps, data, 'k_80-82', [1, 1], permeabilty_parameters, perm_contour_params, perm_type, True)
kriging_interpolate(permeability_maps, data, 'k_82-84', [1, 2], permeabilty_parameters, perm_contour_params, perm_type, True)
kriging_interpolate(permeability_maps, data, 'k_84-87', [1, 3], permeabilty_parameters, perm_contour_params, perm_type, True)
kriging_interpolate(permeability_maps, data, 'k_87-90', [1, 4], permeabilty_parameters, perm_contour_params, perm_type, True)

OK = OrdinaryKriging(
    x=data['Long'],
    y=data['Lat'],
    z = data['top_TVD'],
    variogram_model= 'exponential',
    verbose=True,
    #enable_plotting= True
)

# define a grid for x and y ranges that we are interested in

gridx = np.arange(116.52444, 116.81692, 0.00146239999999992, dtype='float64')
gridy = np.arange(54.26932, 54.39836, 0.000645200000000017, dtype='float64')
zstar, ss = OK.execute("grid", gridx, gridy)

print(zstar.shape)
print(ss.shape)

contour_plot.add_trace(go.Contour(
        z=zstar,
        x=gridx, # horizontal axis
        y=gridy, # vertical axis
        contours=dict(
                start=2950,
                end=3100,
                size=5)
    ))

contour_plot.add_trace(go.Scatter(
    x=data['Long'], y=data['Lat'],
    name='Wells',
    mode='markers',
    marker_color= 'red',
    marker_size = data['Thickness'],
))


#_--------------------------------------------------------

# 3D plot

OK2 = OrdinaryKriging(
    x=data['Long'],
    y=data['Lat'],
    z = data['top_TVD'],
    variogram_model= 'exponential',
    verbose=True,
    #enable_plotting= True
)

# define a grid for x and y ranges that we are interested in

gridx = np.arange(116.52444, 116.81692, 0.00146239999999992, dtype='float64')
gridy = np.arange(54.26932, 54.39836, 0.000645200000000017, dtype='float64')
zstar, ss = OK2.execute("grid", gridx, gridy)

fig.add_trace(go.Surface(
        z=zstar,
        x=gridx, # horizontal axis
        y=gridy, # vertical axis
        contours = {
        "z": {"show" : True, "start": 2800, "end": 3300, "size": 10, "color": "white"}
    },
    ))

OK3 = OrdinaryKriging(
    x=data['Long'],
    y=data['Lat'],
    z = data['bottom_TVD'],
    variogram_model= 'exponential',
    verbose=True,
    #enable_plotting= True
)

# define a grid for x and y ranges that we are interested in

gridx = np.arange(116.52444, 116.81692, 0.00146239999999992, dtype='float64')
gridy = np.arange(54.26932, 54.39836, 0.000645200000000017, dtype='float64')
zstar, ss = OK3.execute("grid", gridx, gridy)

fig.add_trace(go.Surface(
        z=zstar,
        x=gridx, # horizontal axis
        y=gridy, # vertical axis
        contours = {
        "z": {"show" : True, "start": 2800, "end": 3300, "size": 10, "color": "white"}
    },
    ))

for well in dev_sur['UWI']:
    surv = dev_sur[dev_sur['UWI'] == well]
    survey = surv[surv['TVD'] > 2500]
    fig.add_trace(go.Scatter3d(
                z = survey['TVD'],
                x=survey['Long'], 
                y=survey['Lat'],
                #name = well,
                marker=dict(
                    size=4,
                    color=survey['TVD'],
                    colorscale='Sunsetdark',
                ),
                line=dict(
                    color='darkblue',
                    width=2
                )
                #marker_size = 10,
            ))
# adding the pad wells onto the maps

for well in dev_sur['UWI']:
    survey = dev_sur[dev_sur['UWI'] == well]
    contour_plot.add_trace(go.Scatter(
                x=survey['Long'], y=survey['Lat'],
                #name = well,
                mode='lines',
                marker_color= '#00CC96',
                #marker_size = 10,
            ))

fig.update_layout(yaxis_range=[2500,3300])
fig.update_xaxes(autorange="reversed")
fig.update_layout(
    scene={
        'zaxis': {'autorange': 'reversed'}, # reverse automatically
    }
)
#porosity_maps.update_xaxes(autorange="reversed")
#permeability_maps.update_xaxes(autorange="reversed")
#porosity_maps.write_html('log_functions/porosity_map.html')
#permeability_maps.write_html('log_functions/perm_map.html')

contour_plot.update_xaxes(autorange="reversed")
contour_plot.show()
#fig.write_html('log_functions/3D_map.html')

#fig.write_html('log_functions/test_surface.html')

#print(data.head())