
import pandas as pd

class Table:

    def __init__(self, name):
        self.name = name
        self.columns = []
        self.data = pd.DataFrame()

