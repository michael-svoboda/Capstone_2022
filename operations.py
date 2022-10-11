import pandas as pd

# need to write a function that will take in a table, and a new list of columns and cross check them together
# columns will potentially need to be hard coded idk how to get around that

class Table_Check:

    operations = {
        'Well' : [],
        'Curves' : [],
        'Parameter' : [],
        'Core_Definition' : [],
        'Core | Core_Definition' : [],
        'TEST_Definition' : [],
        'TEST | TEST_Definition' : [],
        'TOPS_Definition' : []

    }

    def __init__(self, table, file_columns):
        self.table = table
        self.file_columns = file_columns
    
    def check_columns(self):
        
        # Identify which table we are working in.
        self.table.name


