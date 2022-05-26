

import src.magicroot as mr
import pandas as pd
import logs
import os
import logging
log = logging.getLogger(__name__)


if __name__ == '__main__':
    path = r'C:\Users\daalcantara\Lusitania\IFRS17 - IFRS17-Implementação - Programa\Outputs\08. Dados\03. Execução do Plano\8.05 - Identificação de Requisitos de Atuariado\8.5.10 - Atuariado - Testes de aceitação de negócio - DM\8.5.10.1 Datawarehouse\DAT_SINISTROS_GRAVES.csv'
    x = os.path.exists(path)
    print(x)
    x = os.path.isfile(path)
    print(x)

    folder_contab = mr.os.home['Lus\\IFRS 17\\outputs\\Implementacao motor\\integracao\\inputs\\extracted']
    # folder_treated = mr.os.home['Lus\\IFRS 17\\outputs\\Implementacao motor\\integracao\\treated']

    # folder_dir = mr.os.home['Lus\\IFRS 17\\outputs\\Implementacao\\integracao\\inputs\\extracted']
    print(folder_contab.get('LSP_010_20220225_ACDOCA_1.fil').tail)
    # folder_contab.copy(to=folder_treated, objs='LSP_010_20220225_ACDOCA_1.fil')

    log.debug('-----------------------------------------------------------')
    dm_atuariado = mr.os.home['LUS\\IFRS 17\\outputs\\dados\\execucao plano\\8.05 - Identificação de Requisitos de Atuariado\\8.5.10 - Atu - Testes de aceitação de neg - DM\\datawarehouse']

    print(dm_atuariado)

    df_sinistros_graves = dm_atuariado.get('DAT_SINISTROS_GRAVES.csv', nrows=100)
    df_pagamentos_at = dm_atuariado.get('DAT_PAGAMENTOS_AT.csv', nrows=100)

    print(df_sinistros_graves)

    """

    
    
    """


    # print(folder_dir)



