from unicodedata import name
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.interpolate import interp1d
import numpy as np
import math

# Basically we want to 
data = pd.read_csv('log_functions/Digitized_Logs.csv')
las_data = pd.read_csv('C:/Users/micha/Documents/PetroleumProgramming/data/databases_verticals/curves_values.csv')
#data.dropna()

print(data.head())
print(data['Log'].unique())
print(data['Well'].unique())

log_names = [x for x in data['Log'].unique() if str(x) != 'nan']



digitized_logs = make_subplots(rows=3, cols=4, subplot_titles= ['GR', 'Deep_RES', 'Shallow_RES', 'SP',  'Phi_D', 'Phi_N', 'Ats', 'AC', 'Vsh', 'Phi_eff', 'TOC'])
digitized_logs.update_layout(height=4000)

log_track = {
        'GR': (1,1),
        'Deep_RES': (1,2),
        'Shallow_RES': (1,3),
        'SP': (1,4),
        'Phi_D': (2,1),
        'Phi_N': (2,2),
        'Ats': (2,3),
        'AC': (2,4),
        'Vsh': (3,1),
        'Phi_eff': (3,2),
        'TOC': (3,3)
    }

well_colors = {
        '100021806218W500': '#636EFA',
        '100060206219W500': '#EF553B',
        '100062906118W500': '#00CC96',
        '103162506119W500': '#AB63FA',
        '100100906218W500': '#FFA15A',
        '100111306219W500': '#19D3F3',
        '100070706218W500': '#FF6692',
        '100123506118W500': '#B6E880',
        '100082806118W500': '#FF97FF',
    }

def generate_heatmap_matrix():

    heatmap_matrix = []

    for well in data['Well'].unique():

        vector = []
        data_filtered = data[data['Well'] == well]

        for log in ['Deep_RES', 'Shallow_RES', 'SP', 'GR', 'Phi_D', 'Phi_N', 'Ats']:
            if log in data_filtered['Log'].unique():
                vector.append(1)
            else:
                vector.append(0)

        heatmap_matrix.append(vector)
    
    return heatmap_matrix



calculation_input_logs = {
    'TOC': ['Deep_RES', 'AC'],
    'Phi_eff': ['Phi_', 'Phi_N'],
    'Vsh': ['GR']
}

# Lets start with Vsh calculation, then porosity, finally TOC

def interpolate(x_list, y_list, max, min):

    f = interp1d(x_list, y_list)
    #print(max)
    #print(min)
    #print('--------')
    x_new = np.linspace(min, max, num = (max - min)*100, endpoint=True)
    y_new = f(x_new)

    return x_new, y_new

def calculate_Vsh(GR, GR_clean, GR_shale):

    V_sh = [(value-GR_clean)/(GR_shale - GR_clean) for value in GR]
    
    return V_sh

def init_Vsh_calcs():

    Vsh_calcs = {}

    for well in data['Well'].unique():

        data_filtered = data[data['Well'] == well]

        if set(['GR']) <= set(data_filtered['Log'].unique()):

            #print(well)

            GR_df = data_filtered[data_filtered['Log'] == 'GR']

            Vsh_calcs[well] = (calculate_Vsh(GR_df['Value'], 10, 150) , GR_df['Depth'])
    
    return Vsh_calcs


def calculate_Phi_eff(phi_D_df, phi_N_df):
    # First we need to find the max and min depth of each one and then determine the maximum overlap

    max_depth_phi_D = max(phi_D_df['Depth'].tolist())
    min_depth_phi_D = min(phi_D_df['Depth'].tolist())
    #print('max_D =' , max_depth_phi_D)
    #print('min_D =' , min_depth_phi_D)

    max_depth_phi_N = max(phi_N_df['Depth'].tolist())
    min_depth_phi_N = min(phi_N_df['Depth'].tolist())
    #print('max_N =' , max_depth_phi_N)
    #print('min_N =' , min_depth_phi_N)

    depth_max = lambda D, N: D if (D > N) else N
    depth_min = lambda D, N: D if (D < N) else N

    D_depths, phi_D_interpltd = interpolate(phi_D_df['Depth'], phi_D_df['Value'], math.floor(depth_min(max_depth_phi_D, max_depth_phi_N)), math.ceil(depth_max(min_depth_phi_D, min_depth_phi_N)))
    N_depths, phi_N_interpltd = interpolate(phi_N_df['Depth'], phi_N_df['Value'], math.floor(depth_min(max_depth_phi_D, max_depth_phi_N)), math.ceil(depth_max(min_depth_phi_D, min_depth_phi_N)))

    phi_df = pd.DataFrame.from_dict({'depth':D_depths, 'phi_D':phi_D_interpltd, 'phi_N':phi_N_interpltd})
    phi_df['phi_eff'] = 0.5*(phi_df['phi_D'] + phi_df['phi_N'])

    return phi_df['phi_eff'].to_list(), phi_df['depth'].to_list()

def init_phi_calcs():

    phi_calcs = {}

    for well in data['Well'].unique():

        data_filtered = data[data['Well'] == well]

        if set(['Phi_D', 'Phi_N' ]) <= set(data_filtered['Log'].unique()):

            #print(well)

            phi_D_df = data_filtered[data_filtered['Log'] == 'Phi_D']
            phi_N_df = data_filtered[data_filtered['Log'] == 'Phi_N']

            phi_calcs[well] = calculate_Phi_eff(phi_D_df, phi_N_df)
    
    return phi_calcs

#print(init_phi_calcs().keys())

def calculate_TOC(R_df, AC_df):
    # First we need to find the max and min depth of each one and then determine the maximum overlap

    max_depth_R = max(R_df['Depth'].tolist())
    min_depth_R = min(R_df['Depth'].tolist())
    #print('max_D =' , max_depth_R)
    #print('min_D =' , min_depth_R)

    max_depth_AC = max(AC_df['DEPT'].tolist())
    min_depth_AC = min(AC_df['DEPT'].tolist())
    #print('max_N =' , max_depth_AC)
    #print('min_N =' , min_depth_AC)

    depth_max = lambda R, AC: R if (R > AC) else AC
    depth_min = lambda R, AC: R if (R < AC) else AC

    R_depths, R_interpltd = interpolate(R_df['Depth'], R_df['Value'], math.floor(depth_min(max_depth_R, max_depth_AC)), math.ceil(depth_max(min_depth_R, min_depth_AC)))
    AC_depths, AC_interpltd = interpolate(AC_df['DEPT'], AC_df['AC'], math.floor(depth_min(max_depth_R, max_depth_AC)), math.ceil(depth_max(min_depth_R, min_depth_AC)))

    TOC_df = pd.DataFrame.from_dict({'depth':R_depths, 'R':R_interpltd, 'AC':AC_interpltd})

    TOC_df['TOC'] = np.log10(TOC_df['R']/7) + 0.02*(TOC_df['R'] - 220)*(10**((0.297 - (0.1688*11.5))))

    return TOC_df['TOC'].to_list(), TOC_df['depth'].to_list()

def init_TOC_calcs():
    
    # we could try to manually define these... I wont referring to AER TOC report for Duvernay

    R_base = 7 # ohm*m
    dt_base = 220 # usec/m

    AC_well_list = las_data[las_data['AC'].notna()]['UWI'].unique()

    R_baseline_dict = {
        '100060206219W500': 0,
        '100062906118W500' : 0,
        '100100906218W500' : 0,
        '100111306219W500' : 0,
        '100123506118W500' : 0
    }

    dt_baseline_dict = {
        '100060206219W500': 0,
        '100062906118W500' : 0,
        '100100906218W500' : 0,
        '100111306219W500' : 0,
        '100123506118W500' : 0
    }

    TOC_calcs = {}

    for well in AC_well_list:

        RES_data_filtered = data[data['Well'] == well]
        AC_data_filtered = las_data[las_data['UWI'] == well]


        if set(['Deep_RES']) <= set(RES_data_filtered['Log'].unique()):

            print(well)

            deep_RES_df = RES_data_filtered[RES_data_filtered['Log'] == 'Deep_RES']
            AC_df = AC_data_filtered[['DEPT', 'AC', 'UWI']]

            TOC_calcs[well] = calculate_TOC(deep_RES_df, AC_df)
    
    return TOC_calcs






logs_heatmap = go.Figure(data=go.Heatmap(
                    z=generate_heatmap_matrix(),
                    x=['Deep_RES', 'Shallow_RES', 'SP', 'GR', 'Phi_D', 'Phi_N', 'Ats'],
                    y=data['Well'].unique(),
                    xgap= 2, 
                    ygap= 2,
                    colorscale = 'RdYlGn'))

#logs_heatmap.show()

def add_logs(fig, log_name):

    for well in data['Well'].unique():
        data_filtered = data[(data['Log'] == log_name) & (data['Well'] == well)]
        data_sorted = data_filtered.sort_values(by=['Depth'])

        #print(data_filtered['Log'])
        # Now we should have one trace and we can plot it to the figure
        fig.add_trace(
            go.Scatter(
                x=data_sorted['Value'], 
                y=data_sorted['Depth'],  
                name = log_name + ': ' + str(well), 
                marker=dict(
                    color = well_colors[well],
                    #line_width=1
                )),
            row=log_track[log_name][0], col=log_track[log_name][1],
           
        )
    
        '''for well in las_data['UWI'].unique():
        data_filtered = las_data[las_data['UWI'] == well]
        data_sorted = data_filtered.sort_values(by=['DEPT'])

        #print(data_filtered['Log'])
        # Now we should have one trace and we can plot it to the figure
        fig.add_trace(
            go.Scatter(
                x=data_sorted['AC'], 
                y=data_sorted['DEPT'],  
                name = 'AC: ' + str(well), 
                marker=dict(
                    color = well_colors[well],
                    #line_width=1
                )),
            row=log_track['AC'][0], col=log_track['AC'][1],
           
        )'''

    
def add_TOC(fig):
        # add the TOC values
    TOC_values = init_TOC_calcs()
    add_calculated_traces(fig, init_TOC_calcs().keys(), TOC_values, 'TOC', well_colors, log_track, 'TOC')
    print('Added TOC')        

def add_Vsh(fig):
        # add the TOC values
    Vsh_values = init_Vsh_calcs()
    add_calculated_traces(fig, Vsh_values.keys(), Vsh_values, 'Vsh', well_colors, log_track, 'Vsh')
    print('Added VSH')

def add_Phi_eff(fig):
        # add the TOC values
    phi_values = init_phi_calcs()
    add_calculated_traces(fig, phi_values.keys(), phi_values, 'Phi_eff', well_colors, log_track, 'Phi_eff')
    print('Added Phi_eff')    


def add_calculated_traces(fig, well_list, values, name, well_colors, log_track, loc_name):
    for well in well_list:

            # Now we should have one trace and we can plot it to the figure
            fig.add_trace(
                go.Scatter(
                    x = values[well][0], 
                    y = values[well][1],  
                    name = name + ': ' + str(well), 
                    marker=dict(
                        color = well_colors[well],
                        #line_width=1
                    )),
                
                row=log_track[loc_name][0], col=log_track[loc_name][1],
            )

# Plotting all our logs
for log_name in log_names:
    add_logs(digitized_logs, log_name)

# Plotting calculated values
add_TOC(digitized_logs)
add_Vsh(digitized_logs)
add_Phi_eff(digitized_logs)


digitized_logs.show()

