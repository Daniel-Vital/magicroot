import pandas as pd

from config import *


print(db.tables.list)


# print(db['FM_RAMOS'])

db.save_analysis(
    table_name='FM_RAMOS',
    analysis_name='TESTE',
    df=db['FM_RAMOS'].nulls
)


print(db['FM_RAMOS'].analyse.nulls)


def all_duplicated(df):
    """
    Creates Dataframe with all lines which are repeated in all rows
    :return: DataFrame with all lines with all repeated rows
    """
    return df[df.duplicated(keep=False)]


db.define_analysis(all_duplicated)

print(db['FM_RAMOS'].analyse.all_duplicated())



# db['some_table'].analyse.nulls()


