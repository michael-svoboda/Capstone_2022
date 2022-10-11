import pandas as pd

'''
Area for testing the flash calculator. 
'''

test_init = {
    'Component' : ['CO2, N2, Methane, Ethane, Propane, i-Butane, n-Butane, i-Pentane, n-Pentane, Hexane, Heptane+'],
    'Mole Fraction %' : [0.22, 0.09, 63.35, 4.21, 2.09, 0.68, 1.08, 0.47, 0.38, 1.36, 26.07]
}

# convert to a dataframe
test_init_df = pd.DataFrame.from_dict(test_init)


