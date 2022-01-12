import sys
import os

from src import magicroot as mr
from localdata.folders import *

import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# some public data

db = mr.Database(
    path=folder_database,
    folders={'extractions': folder_extractions},
    default_configs={'.csv': {'delimiter': ';', 'decimal': ',', 'encoding': 'latin-1'}},
    column_types={'COBERTURA': str}
)


