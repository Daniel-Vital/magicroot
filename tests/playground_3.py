import src.magicroot as mr
import logging


log = logging.getLogger('Datamodel.Montantes_por_Cobertura')


if __name__ == '__main__':
    mr.os.parcers.CSV.set_default_settings({
        'read': {'delimiter': ';', 'decimal': ',', 'encoding': 'latin-1', 'quotechar': '"'},
        'save': {'sep': ';', 'decimal': ',', 'encoding': 'latin-1', 'quotechar': '"'},
    })
    extract_folder = mr.os.home['Lus\\IFRS 17\\output\\dados\\fontes\\extracoes']
    outputs_pre_cob = mr.os.home['Lus\\IFRS 17\\outputs\\dados\\premios por cobertura\\ouputs']
    df_premiums = extract_folder.get('FM_HRECICOBERTURASANO', nrows=10)
    df_reinsurance = extract_folder.get('FM_HRECRESSEGUROANO', nrows=100000)
    df_commissions = extract_folder.get('FM_HRECICOBERTURASANO_COMISSAO', nrows=10)
    df_config = outputs_pre_cob.get('CONFIG_MARGENS_COBERTURAS.csv', nrows=10)

    dic_cod = {
        'RAMO': 2, 'TRATADO': 3, 'APOLICE': 7, 'MODALIDADE': 2, 'SUBMODALIDADE': 3, 'CODIGO': 3, 'CODMOV': 2
    }

    df_reinsurance = mr.df.remove.column_name_sequence(df_reinsurance, 'HRECRES')
    df_reinsurance = mr.df.format.as_set_len_code(df_reinsurance, dic_cod)
    df_reinsurance = df_reinsurance.assign(
        PREMIO=lambda x: x['PREMIO'].map(lambda p: float('0' + p if p[0] == '.' else p))
    )

    df_config = mr.df.format.as_set_len_code(df_config, dic_cod)
    """
    print(df_premiums)
    print(df_reinsurance)
    print(df_commissions)
    print(df_config)
    """
    def get_reinsurance_premiumns(df_reinsurance, df_config):
        id_reinsurance = ['BRAND', 'RAMO', 'APOLICE', 'RECIBO', 'TRATADO']

        df_config = df_config[['BRAND', 'RAMO', 'CODIGO', 'TRATADO', 'MARGEM']].drop_duplicates().groupby(
            ['BRAND', 'RAMO', 'TRATADO']
        ).mean().reset_index()
        print(df_reinsurance.query('APOLICE == "9961967"'))
        df_reinsurance = df_reinsurance.query('CODMOV == "01"')[id_reinsurance + ['PREMIO']].groupby(id_reinsurance, dropna=False).sum().reset_index()
        df_reinsurance_test = mr.df.count.unique(df_reinsurance, ['PREMIO'], id_reinsurance)

        df_reinsurance = df_reinsurance.merge(df_config, how='left', validate='many_to_one')[
            lambda x: x['MARGEM'].notnull()
        ].assign(
            PREMIO_RESS=lambda x: x['MARGEM'] * x['PREMIO']
        )[['BRAND', 'RAMO', 'APOLICE', 'RECIBO', 'TRATADO', 'PREMIO_RESS']]
        return df_reinsurance, df_config


    df_reinsurance, df_config = get_reinsurance_premiumns(df_reinsurance, df_config)

    print(df_config)
    print(df_reinsurance.sample(100))




