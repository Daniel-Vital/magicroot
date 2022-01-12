import pandas as pd

from config import *


# print(db.tables.list)



print(db['FM_RAMOS'].analyse.nulls())

print(db['FM_RAMOS'].analyse.all_duplicated())


# db['some_table'].analyse.nulls()


