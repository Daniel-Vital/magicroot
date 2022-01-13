import pandas as pd

from config import *
from src.magicroot.databranch.database_structures.__analysis_book import AnalysisBook

# print(db.tables.list)


def get_methods_not_dunder(cls):
    return [
        method
        for method in dir(cls) if method.startswith('__') is False
    ]


x = AnalysisBook()

y = AnalysisBook()

x.__setattr__('hello', 5)

print(get_methods_not_dunder(AnalysisBook))
print(get_methods_not_dunder(x))
print(get_methods_not_dunder(y))

print('----------------------------------------------')

