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

db = mr.databranch.Database(
    path=folder_database,
    folders={
        'extractions': folder_extractions,
        'aux_to_gl_account': folder_aux_tables_gl_account,
        'datawarehouse': folder_dw_tables,
        'icg_table': folder_icg,
        'ins_cash_flow': folder_ins_cash_flow,
        'sas_input': folder_sas_input,
        'sas_ouput': folder_sas_output,
        # 'sas_grouping_output': folder_sas_grouping_output,
    },
    default_configs={
        '.csv': {
            'delimiter': ';', 'decimal': ',', 'encoding': 'latin-1', 'on_bad_lines': 'warn', 'dayfirst': True
        },
        '.sas7bdat': {
            'encoding': 'latin-1'
        }
    },
    column_types={
        'BRAND': str,
        'Tx_MARCA': str,
        'RAMO': str,
        'Id_RAMO': str,
        'MODALIDADE': str,
        'Id_MODALIDADE': str,
        'SUBMODALIDADE': str,
        'Id_SUBMODALIDE': str,
        'PRODUTO': str,
        'Id_PRODUTO': str,
        'APOLICE': str,
        'RECIBO': str,
        'COBERTURA': str,
        'CODMOV': str,
        'RUBRICA_CONTABILISTICA': str,
        'PMES': str,
        'SEQUENCIA': str,
        'PROC_GRAVE': str
    }
)

