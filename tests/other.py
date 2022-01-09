db = mr.Database(
    path=r'C:\Users\daalcantara\Deloitte (O365D)\PT DL FS RA Lusitania IFRS 17 - General\04. Outputs\08. Dados\14. Preparacao dos dados manuais\00 Python DataBase',
    csv=['some_path.csv', 'other_path.csv'],
    ftr=['C:\Users\daalcantara\Desktop\Gl_account_RAMO.ftr', 'other_path.ftr'],
    dirs=[
        r'C:\Users\daalcantara\Deloitte (O365D)\PT DL FS RA Lusitania IFRS 17 - General\04. Outputs\08. Dados\14. Preparacao dos dados manuais\00 Python DataBase\01 Tabelas',
        r'C:\Users\daalcantara\Lusitania\IFRS17 - IFRS17-Implementação - Programa\Outputs\08. Dados\03. Execução do Plano\8.14 - Prep. dos dados manualmente SAS\03 Tabelas manuais preparadas\SAS_Insurance_Contract',
        r'C:\Users\daalcantara\Lusitania\IFRS17 - IFRS17-Implementação - Programa\Outputs\08. Dados\01. Fontes recebidas\01 Extrações'
    ],
    input_csv_config={'encoding': 'latin-1', 'delimiter': ';'},
    input_ftr_config={}
)