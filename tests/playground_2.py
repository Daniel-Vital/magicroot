

from config import *
import getpass
import re
import datetime as dt
from src.magicroot.databranch.directorymanager.folder import *

from src import magicroot as mr

"""
dm = DirectoriesManager(folder_database, folders)
df = dm.data
print(df)

dm.save()
"""

x = mr.databranch.validation_tools.dataframe_shape.transform_columns_to_eu_dates(db['insurance_contract_group_csm'], ['BEGIN_COV_DT', 'END_COV_DT'])
print(x)
print(x.dtypes)

x = x.assign(
    BEGIN_COV_DT=lambda x: pd.to_datetime(
                x['BEGIN_COV_DT'],
                errors='coerce',
                dayfirst=True)
)
print(x)

