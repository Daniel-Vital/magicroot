import src.magicroot as mr
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


if __name__ == '__main__':
    folder_dir = mr.os.home['Lus\\IFRS 17\\outputs\\dados\\exec plano\\dados manuais\\tab prep\\dw']
    folder_ress = mr.os.home['Deloitte\\IFRS 17\\outputs\\dados\\prep dados manuais\\inputs tabelas python']
    dm_ifrs17 = mr.os.home['LUS\\IFRS 17\\Motor de calculo\\tables\\input\\name change']
    datawarehouse = mr.os.home['Lus\\IFRS 17\\motor de calculo\\data model tables\\input\\aux tables']
    extractions = mr.os.home['LUS\\IFRS 17\\outputs\\dados\\fontes\\extracoes']
    dm_atuariado = mr.os.home[
        'LUS\\IFRS 17\\outputs\\dados\\execucao plano' \
        '\\8.05 - Identificação de Requisitos de Atuariado\\8.5.10 - Atu - Testes de aceitação de neg - DM\\datawarehouse'
    ]
    analises_AT = mr.os.home['Deloitte\\LUS IFRS 17\\Projeto AT e RA\\analises']
    contab_input = mr.os.home['Lus\\IFRS 17\\outputs\\Implementacao motor\\integracao\\inputs']
    dm_contabilidade = mr.os.home['Lus\\IFRS 17\\outputs\\Implementacao motor\\integracao\\suporte']
    amort_csm = mr.os.home[
        'Lus\\IFRS 17\\outputs\\dados\\exec plano\\Id. map. req. SAS' \
        '\\Implem. proc. automático\\Amortização CSM\\Ident Regra\\Materialidade'
    ]

    x = pd.DataFrame(data=[[1, 2, 3], [1, 2, 3], [1, 2, 3]], columns=['a', 'b', 'c'])

    print(x)

    print(mr.df.create.const_col(x, 5))
