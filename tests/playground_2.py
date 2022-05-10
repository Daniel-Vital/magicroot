import pandas as pd

from config import *
import getpass
import re
import datetime as dt
from src.magicroot.databranch.directorymanager.old_folder import *

from src.magicroot.diamondpinky.tools.allocate import *

from src import magicroot as mr

"""
dm = DirectoriesManager(folder_database, folders)
df = dm.data
print(df)

dm.save()
"""


def create_error_category(df):
    """
    """
    df_allocation_matrix.loc['OverAllocated'] = df.sum() - 1
    df_allocation_matrix['OverAllocated'] = df.sum(axis=1) - 1


def allocation_matrix(df):
    """
    Checks that a matrix can be used to allocate
    Checks if all lines sum to
    :param df:
    :return: Assertion error if cannot be allocated
    """
    # assert len(df) + 1 == len(df.columns)
    assert pd.DataFrame({'Observed': df.sum()}).assign(
        Expected=1.0,
        Result=lambda x: (x['Observed'] - x['Expected']).abs()
    )['Result'].sum() == 0.0


def set_allocation_index(df, alloc_matrix):
    alloc_matrix.index = df.index
    alloc_matrix.columns = df.index


def allocate(df, alloc_matrix):
    # allocation_matrix(alloc_matrix)
    df['Allocated'] = alloc_matrix @ df['Value']


print('------------------ Tabela inicial')
df_cashflows = pd.DataFrame({
    'CAT': ['A', 'B', 'C', 'D'],
    'Value': [1.232, 3.212, 2.314, 5.165]
})
df_cashflows = df_cashflows.set_index('CAT')
print(df_cashflows)
print('------------------ Criação de buckects adicionais')


print('------------------ Calculos de allocacoes')
df_allocation_matrix = pd.DataFrame([
    [0.5, 0.4, 0, 0],
    [0.33, 0.37, 0.34, 0],
    [1, 0, 0, 0],
    [0, 1, 0, 0]]).astype(float)
df_allocation_matrix.index = df_cashflows.index
df_allocation_matrix.columns = df_cashflows.index
df_cashflows = pd.concat([df_cashflows, df_allocation_matrix], axis=1)
print(df_cashflows)


print('------------------ OverAllocation')
df_cashflows['UnAllocated'] = 1 - df_cashflows[df_cashflows.index.to_list()].sum(axis=1)
print(df_cashflows)

print('------------------ Matrix de allocacoes')
df_allocation_matrix = df_cashflows[df_cashflows.index.to_list() + ['UnAllocated']].T
# set_allocation_index(df_cashflows, df_allocation_matrix)
print(df_allocation_matrix)

print('------------------ Allocacao')
allocate(df_cashflows, df_allocation_matrix)

print(df_cashflows)


# df_allocation_matrix.loc[len(df_allocation_matrix)] = 0
