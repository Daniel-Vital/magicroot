

from config import *

print(db.tables.get_references('extractions'))
print('----------------------------------------------------')
print(db['SAS_Risk_Factor_v2.00'].analyse)
print('----------------------------------------------------')
db['SAS_Risk_Factor_v2.00'].analyse.nulls()
print('----------------------------------------------------')


def some_test(df):
    return df


db['SAS_Risk_Factor_v2.00'].analyse(func=some_test)

