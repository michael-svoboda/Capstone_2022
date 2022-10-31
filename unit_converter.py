import pandas as pd

'''
Script for converting units of logs. Will turn into a module and call in app later.
'''

# Reading in the .csv data

curves_df = pd.read_csv('C:/Users/micha/Documents/PetroleumProgramming/data/databases_verticals/Curves.csv')

curves_values_df = pd.read_csv('C:/Users/micha/Documents/PetroleumProgramming/data/databases_verticals/curves_values.csv')

#print(curves_df.head())
#print(curves_values_df.head())

# Need to grab the depth column and compare the units for each well
# First filter curves_df on mnemonic == DEPT

curves_df = curves_df[curves_df['mnemonic'] == 'DEPT']

#print(curves_df)

# Get a unique list of the uwi's
vertical_well_list = curves_df['UWI'].unique().tolist()

metric_depths = []

'''# Filter the curves_values_df and if the units are not 'M' then apply unit conversion
for uwi in vertical_well_list:

    print(curves_df[curves_df['UWI'].str.contains(uwi)]['unit'])

    for well in curves_df[curves_df['UWI'].str.contains(uwi)]['unit'].to_list():

        pass_num = curves_df[curves_df['UWI'].str.contains(uwi)]['unit'].to_list().index(well) + 1

        filtered_df = curves_values_df[curves_values_df['UWI'] == uwi]
        filtered_df = filtered_df[filtered_df['pass_#'] == pass_num]
        #print("Filtered DF: ", filtered_df)

        if well == 'F':
            filtered_df['DEPT'] = filtered_df['DEPT'] * 0.3048
            metric_depths.extend(filtered_df['DEPT'].tolist())
            print("Units, converted")
        else:
            metric_depths.extend(filtered_df['DEPT'].tolist())

        #print("LENGTH: ", filtered_df['DEPT'].tolist())
    print("LENGTH: ", len(metric_depths))

curves_values_df['DEPT_m'] = metric_depths

print(curves_values_df.head())'''


# Do this a different way, we will append a new column with the units for the depths and then
# apply the unit conversion on rows only if they have feet.

# First filter down to only depths
curves_df = curves_df[curves_df['mnemonic'] == 'DEPT']

# Generate a list of units

curves_sub = curves_df[['UWI', 'unit']]

curves_dict = curves_sub.set_index('UWI').to_dict()

print(curves_dict)
print(curves_dict['unit']['100021806218W500'])

# Now we can use the dictionary as a check up to find out which wells have what units

print("CONVERTED: ", curves_values_df['DEPT'].head())

'''for well in list(curves_dict.keys()):
    curves_values_df['DEPT'] = curves_values_df.apply(lambda x: x['DEPT']*0.3048 if x['UWI'] == well else x['DEPT'], axis=1)
'''
curves_values_df['DEPT'] = curves_values_df.apply(lambda x: x['DEPT']*0.3048 if curves_dict['unit'][x['UWI']] == 'F' else x['DEPT'], axis=1)

curves_values_df.to_csv('curves_values_metric.csv', index = False)

print("CONVERTED: ", curves_values_df['DEPT'].head())
