import lasio
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
from pyparsing import col
from operations import *
from sqlalchemy import false

from structures import *

# function for creating a dictionary for each table
# get a list of the mnemonics, units, values, descriptions
# add them
def create_new_table_df(wellname, pass_num, table):

    table_dict = {
                'UWI': wellname,
                "pass_#": pass_num,
                'item_#' : list(range(0, len(las_loop.sections[table].items()))),
                'mnemonic' : [],
                'unit' : [],
                'value' : [],
                'descr' : []
            }

    for item in las_loop.sections[table].items():
                table_dict['mnemonic'].append(item[1].mnemonic)
                table_dict['unit'].append(item[1].unit)
                table_dict['value'].append(item[1].value)
                table_dict['descr'].append(item[1].descr)

    new_table_df = pd.DataFrame.from_dict(table_dict)

    return new_table_df

# assign directory
directory = '.\data\LAS_Batch_Export'

las = lasio.read("./data/LAS_Batch_Export/100053606118W500_g1_MainPass.las")

unique_table_list = list(las.sections.keys())

# deleting the 'Other' section because its defaulted to an empty string resulting in errors
del unique_table_list[4]
del unique_table_list[0]

global_tables = {}
curves_table = None

# now we will want to populate the data for each table
# iterate over files in directory

print('started reading')

for filename in os.listdir(directory):

    # Getting the pass number
    first_ = filename.index("_")
    second_ = filename.index("_", first_ + 1)
    pass_num = filename[first_+2:second_]

    f = os.path.join(directory, filename)

    # checking if it is a file
    if os.path.isfile(f):
        print(f)
    
    las_loop = lasio.read(f)

    
    '''for item in las_loop.sections['Well'].items():
        print(item)'''
        

    wellname = None

    # first iteration we will just hard code the fifth element of the list. Otherwise we can loop through each one
    # and find the best one
    for item in las_loop.sections['Well'].items():

        value = item[0]

        if value == 'UWI':
            wellname = item[1].value
            break

    file_unique_table_list = list(las_loop.sections.keys())
    del file_unique_table_list[4]
    del file_unique_table_list[0]

    global_tables_set = set(list(global_tables.keys()))
    file_unique_set = set(file_unique_table_list)

    new_tables = list(set(file_unique_set).difference(set(global_tables_set)))
    existing_tables = list(set(global_tables_set).intersection(set(file_unique_set)))

    if not(global_tables_set >= file_unique_set):

        for table in new_tables:

            global_tables[table] = create_new_table_df(wellname, pass_num, table)
            # take all of the lists from the global table and merge them all together.
        
    for table in existing_tables:

            # merge the dataframes together
            global_tables[table] = pd.concat([global_tables[table], create_new_table_df(wellname, pass_num, table)])
            #print(table, str(global_tables[table].shape))

    # Creating the curves dataframe
    curves_df = las_loop.df().reset_index()
    curves_df['UWI'] = wellname
    curves_df['pass_#'] = pass_num
    
    if curves_table is None:
        curves_table = curves_df
    else:
        dfs = [curves_table, curves_df]
        curves_table = pd.concat(dfs, axis=0, ignore_index=True)

print('done reading')

for table_number in range(len(global_tables.keys())):

    table_name = list(global_tables.keys())[table_number]
    table_name = table_name.replace(" ","")
    table_name = table_name.replace("|","_")

    global_tables[list(global_tables.keys())[table_number]].to_csv('data/databases/' + str(table_name) + '.csv', index = False)

# code for getting the curve values

curves_table.to_csv('data/databases/' + 'curves_values' + '.csv', index = False)


