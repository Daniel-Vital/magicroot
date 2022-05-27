

import src.magicroot as mr
import pandas as pd
import re
import warnings
import logging
log = logging.getLogger(__name__)


if __name__ == '__main__':
    folder_input = mr.os.home['Lus\\IFRS 17\\outputs\\Implementacao motor\\integracao\\inputs']

    # 01 creates folder for auxiliary files
    folder_aux = folder_input.new(folder='01 aux files')

    # 02 unzips files to specifically created folder
    folder_unziped = folder_aux.new(folder='01 unziped')
    # folder_input.unzip(to=folder_unziped)

    # 03 changes extension of unziped files to specifically created folder
    folder_txt = folder_aux.new(folder='02 txts')
    folder_unziped.copy(to=folder_txt, with_new_extension='.txt')
    folder_txt.remove('LSP_010_20220225.txt')

    # 04 creates dataframe from txt files
    lines_per_file = 10000000
    dic = {}
    for file in folder_txt.files:
        n_file = int(re.findall('_\d+\.', file)[-1][1:-1])
        threw_warning = False
        for n_line, line in enumerate(folder_txt.get(file, mode='r', encoding='latin-1')):
            if n_line < lines_per_file:
                row = line[:103].split() + [line[103:-2]]

                def split_columns(on):
                    row.insert(1, row[0][-on:])
                    row[0] = row[0][:-on]

                for split in [3, 10, 1, 10, 4, 4]:
                    split_columns(split)

                del row[7:9]
                row.append(n_file)
                dic[n_line + n_file * lines_per_file] = row
            elif not threw_warning:
                msg = f'Did not read all lines form {file}'
                warnings.warn(msg)

    df = pd.DataFrame.from_dict(
        dic, orient='index',
        columns=['ledger', 'chart_of_accounts', 'year', 'source', 'movement', 'account', 'currency', 'amount',
                 'Description', 'file']
    ).assign(
        amount=lambda x: x['amount'].mask(
            x['amount'].str.endswith('-'), '-' + x['amount'].str.slice(stop=-1)
        ).astype(float)
    )
    folder_input.new_file('treated_data.csv', df)





    # folder_treated_2.get('LSP_010_20220225_ACDOCA_1.txt', mode='w', encoding='utf-8').write(line)

    # folder_treated.open()

