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

print(folder_extractions)

db = mr.Database(
    path=folder_database,
    folders={'extractions': folder_extractions},
    default_configs={'.csv': {'delimiter': ';', 'decimal': ',', 'encoding': 'latin-1'}},
    column_types={'COBERTURA': str}
)

print(db.tables.list)

df_cob = db['FM_COBERTURAS']

df = df_cob.loc[df_cob['RAMO'] == 34, ['COBERTURA', 'DESCRITIVO']].drop_duplicates().sort_values('COBERTURA')

# 17.0                                CHOQUE OU IMPACTO DE VEÍCULOS TERRESTRES

df_cob = db['FM_RAMOS']

print(db)

print(len(db))

print('---------------------------------------')

print(db.peak('extractions/FM_RAMOS'))

