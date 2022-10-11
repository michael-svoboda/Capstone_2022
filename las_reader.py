import lasio
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
from pyparsing import col
from operations import *

from sqlalchemy import false

from structures import *

fig = go.Figure()

# assign directory
directory = '.\data\LAS_Batch_Export'

#-------------------------------------------------------------------------------
# Creating the first file name
#-------------------------------------------------------------------------------

las = lasio.read("./data/LAS_Batch_Export/100053606118W500_g1_MainPass.las")

unique_table_list = list(las.sections.keys())

# deleting the 'Other' section because its defaulted to an empty string resulting in errors
del unique_table_list[4]
del unique_table_list[0]

las_dict = {
    "name": unique_table_list
    }

las_df = pd.DataFrame.from_dict(las_dict)

# list of Table objects, every time the list of tables gets a new table then extend 'tables' 

tables = {}

# creating a list of all of the tables for the initial file.
for table in unique_table_list:
    tables[table] = Table(table)

global_tables = {}

# now we will want to populate the data for each table
# iterate over files in directory
for filename in os.listdir(directory):

    f = os.path.join(directory, filename)

    # checking if it is a file
    if os.path.isfile(f):
        print(f)
    
    las_loop = lasio.read(f)

    file_unique_table_list = list(las_loop.sections.keys())

    #-------------------------------------------------------------
    # GOAL is to generate a list of all the damn tables and keys
    global_tables_set = set(list(global_tables.keys()))
    file_unique_set = set(file_unique_table_list)


    if not(global_tables_set >= file_unique_set):
        new_columns = list(set(file_unique_set).difference(set(global_tables_set)))
        
        for column in new_columns:
            global_tables[column] = file_unique_table_list


    '''# check for new tables being introduced to add and populate
    for table in global_tables.keys:

        if not(set(global_tables[table]) == set(las_loop.sections[table])):
            # get the columns missing from the global table
            missing_columns = list(set(global_tables[table]).difference(set(las_loop.sections[table])))

            # populate with null later


            pass'''
        


    
    #------------------------------------------------------------

    '''las_dict_loop = {
    "name": list(las.sections.keys())
    }

    las_df_loop = pd.DataFrame.from_dict(las_dict)

    dfs_to_merge = [las_df, las_df_loop]

    las_df = pd.concat(dfs_to_merge)'''

    # here we will check the unique list of tablenames, and append any new names to the list above
    # we need to cut down the new list only to values that don't exist in the old list
    # if the values are not inside the existing list, then extend

    #print(unique_table_list)

    #print(file_unique_table_list, unique_table_list)
    #print(type(file_unique_table_list), type(unique_table_list))

    '''# check if the file_unique_table_list is a subset of the master table list
    if not(set(file_unique_table_list) <= set(unique_table_list)):
        # for every new table in the new list, append a Table object to 'tables'
        for new_table in list(set(unique_table_list).difference(set(file_unique_table_list))):
            tables.append(Table(new_table))
            # set the columns of the new table equal to the 'keys' of the las file'''

    # we also need to check old tables for keys. Lets make 'tables' a dictionary for easier check
    for table_name in [list(tables.keys())[0]]:

        # creating the master unique columns list, and the file unique keys list
        if not tables[table_name].columns:
            tables[table_name].columns = list(las_loop.sections[table])
        else:
            # check if there are new columns to add
            unique_columns_list = tables[table_name].columns

            # This probably needs to be done for only the last table.
            # checking if there are any new keys to add to the table.
            if not(set(file_unique_table_list) <= set(unique_columns_list)):
                # adding any new columns into the master columns set
                columns_set = set(tables[table_name].columns).update(set(file_unique_keys_list).difference(set(unique_columns_list)))
                # setting the columns of that table to the updated list
                
                if not(columns_set is None):
                    tables[table_name].columns = list(columns_set)

        print(table_name)
        print(list(tables.keys()))
        #print(tables[table_name].columns)
        
        print(table.name)
        file_unique_keys_list = list(las_loop.sections[table.name].keys())
        items = [i for i in las_loop.sections[table.name].items()]

        #print(table.name)

        if table.name == "Version":

            version_dict = {
                'item_#' : list(range(0, len(las_loop.sections[table.name].items()))),
                'mnemonic' : [],
                'unit' : [],
                'value' : [],
                'descr' : []
            }

            # The Version table has got the information buried in a wierd format so we will unwrap it into a dict
            for item in las_loop.sections[table.name].items():
                version_dict['mnemonic'].append(item[1].mnemonic)
                version_dict['unit'].append(item[1].unit)
                version_dict['value'].append(item[1].value)
                version_dict['descr'].append(item[1].descr)

            #print(version_dict)

            #exit()

            data = pd.DataFrame.from_dict(version_dict)

            
            if table.data.empty:
                table.data = data
        
            else:
                table.data = pd.concat([table.data, data])

            print(table.data)

            #exit()

        # This probably needs to be done for only the last table.
        # checking if there are any new keys to add to the table.
        if not(set(file_unique_table_list) <= set(unique_columns_list)):
            # adding any new columns into the master columns set
            columns_set = set(table.columns).update(set(file_unique_keys_list).difference(set(unique_columns_list)))
            # setting the columns of that table to the updated list
            
            if not(columns_set is None):
                table.columns = list(columns_set)

#-----------------------------------------------------------------------------------
# Code for fixing the last table
#----------------------------------------------------------------------------------

        '''# creating a list of all the curves 
        curves = [las_loop.sections[table.name][column] for column in file_unique_keys_list]
        # packing the curves into a dataframe
        data = pd.DataFrame(np.column_stack(curves), 
                               columns=[file_unique_keys_list])
        
        # get the columns from the master list that are missing in the dataframe
        missing_columns = list(set(unique_columns_list).difference(set(file_unique_keys_list)))
        
        # adding the missing columns to the dataframe
        for column in missing_columns:
            data[column] = np.nan'''

        

            



        # now we need to edit the existing data to make sure that we can append in the new table
        # 1. Add to file dataframe the new missing columns, and then append.
        # 2. Check if a new column has been added from new file. If so, add to master df, populate with null above new values.

#  ATTEMPT TO EXPORT THE DATA FROM THE FRIST TABLE INTO A CSV FILE

tables[0].data.to_csv('test_batch_output.csv', index = false)

# we have an option. we can loop through once and dynamically add data to each table changing the dimensions each tim
# or we can loop through files twice, to first get a unique list of all columns. and then simply add the data.
# I think that looping through twice is better.

# then we want to check if there is a new name in this

#las_df_group = las_df.groupby(['name']).size()
#las_df_grouped = las_df_group.to_frame(name = 'size').reset_index()

# Printing out the grouped dataframe
#print("GROUP:" , las_df_grouped)
#las_df_grouped.to_csv('las_table_names.csv', index=False)

# Lets append the new keys into a list, and then aggregate by this list
# For each unique table name: 
#       get the list(keys) for that file, and append to the master list for table name
#
# After every key has been added to each list, then we will aggregate occurances




# create a unique list of tables now. Now lets add the columns from each of the keys




#---------------------------------------------------------------------------
# Printing out the number of files in the directory
#---------------------------------------------------------------------------

print('Number of files in dir: ' +  str(len([name for name in os.listdir(directory) if os.path.isfile(name)])))
    



#print(las.sections.keys())

#print(las.keys())
#print(las['PGGR'])

# create a list equal to the length of keys

'''for key in las.keys():
    print(len(las[key]))


las.to_csv('las_ouput.csv')

for key in las.keys(): 

    fig.add_trace(go.Scatter(x=las[key], y=las['DEPT'],
                            mode='lines',
                            name=key))


fig.write_html("output_graphs/test_1.html")'''

# Code to extract the various tables, create a large list of all of the various table names
# and which files they came from

# read through every file, save the names into a column. If the name exists, then increase count by one








#print(las_df)

# Step 1: append all of the keys into the name column
