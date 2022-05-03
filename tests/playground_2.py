

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
print(db)
print(db['insurance_contract_group_csm'])

db.save_analysis(
    df=db['insurance_contract_group_csm'],
    table_name='Analises SAS',
    analysis_name='insurance_contract_group_csm',
    cap_rows=100000
)


path = r'C:\Users\daalcantara\Lusitania\IFRS17 - IFRS17-Implementação - Programa\Outputs\12. Implementação do protótipo de IFRS 17 e monitorização – abordagem partilhada\99 Ficheiros motor de calculo\02 Grouping\02 run\02 Outputs'

mr.pysas.copy_to_csv(path, sep=';')




