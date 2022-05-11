from config import *
import logging


log = logging.getLogger('Datamodel.Montantes_por_Cobertura')


def trata_tabelas():
    log.debug('Initializing Step 1 - Formatting and checking inputs')
    log.debug('Removing prefix \'HRECRES\' from the columns of the reinsurance table')
    tabela_resseguro.columns = [column.replace('HRECRES', '') for column in tabela_resseguro.columns]
    log.debug('Reformatting premiums from \'.3\' to 0.3 in reinsurance table')
    tabela_resseguro = tabela_resseguro.assign(
        PREMIO=lambda x: x['PREMIO'].map(lambda p: float('0' + p if p[0] == '.' else p))
    )
    log.debug('Defining dictionary with all columns expected by the process, and their respective types')
    colunas_utilizadas = {
        'BRAND': 'string',
        'RAMO': 'string',
        'CODIGO': 'string',
        'TRATADO': 'string',
        'APOLICE': 'string',
        'DATAPROC': 'string',
        'CODMOV': 'string',
        'CODSIT': 'string',
        'MODALIDADE': 'string',
        'SUBMODALIDADE': 'string',

        'PREMIO': 'float64',
        'COMISSAO_COBRANCA': 'float64',
        'COMISSAO_MEDIACAO': 'float64',
        'COMISSAO_CORRETAGEM': 'float64',
        'COMISSAO_PROTOCOLO': 'float64',
        'PREMIO_COMISSAO': 'float64',
    }


    def formata_tabela_por_tipos(tabela, colunas, table_name):
        log.debug(f'Selecting the appropriate columns from the {table_name} table')
        df = tabela.astype({col: colunas_utilizadas[col] for col in colunas_utilizadas.keys() if col in colunas})
        log.debug(f'The {table_name} table contains {len(df)} lines and {len(df.columns)} columns')
        return df


    tabela_premios = formata_tabela_por_tipos(tabela_premios, [
        'BRAND', 'DATAPROC', 'CODIGO', 'CODMOV', 'CODSIT', 'RAMO', 'APOLICE', 'PREMIO'
    ], table_name='premiums')

    tabela_resseguro = formata_tabela_por_tipos(tabela_resseguro, [
        'BRAND', 'DATAPROC', 'CODMOV', 'CODSIT', 'RAMO', 'APOLICE', 'TRATADO', 'PREMIO'
    ], table_name='reinsurance')

    tabela_comissoes = formata_tabela_por_tipos(tabela_comissoes, [
        'BRAND', 'DATAPROC', 'CODIGO', 'CODMOV', 'CODSIT', 'RAMO', 'APOLICE',
        'COMISSAO_COBRANCA', 'COMISSAO_MEDIACAO', 'COMISSAO_CORRETAGEM', 'COMISSAO_PROTOCOLO', 'PREMIO_COMISSAO'
    ], table_name='commissions')

    config_coberturas = formata_tabela_por_tipos(config_coberturas, [
        'RAMO', 'MODALIDADE', 'SUBMODALIDADE', 'CODIGO', 'TRATADO', 'PRODUTO', 'MARGEM', 'RAMO_ALLOC',
        'COMISSAO_COBRANCA_ALLOC', 'COMISSAO_MEDIACAO_ALLOC', 'COMISSAO_CORRETAGEM_ALLOC', 'COMISSAO_PROTOCOLO_ALLOC'
    ], table_name='config')

    log.debug('Checking that the config table has the appropriate zeros on columns MODALIDADE, SUBMODALIDADE e CODIGO')
    if config_coberturas['MODALIDADE'].str.len().max() < 2 or config_coberturas['SUBMODALIDADE'].str.len().max() < 2 \
            or config_coberturas['CODIGO'].str.len().max() < 3:
        mensg = 'The config table does not have the appropriate format:' \
                '(ex: found 2 instead of 002) probably was open in Excel and saved'
        log.warning(mensg)
        raise Warning(mensg)
    else:
        log.debug('The config table has the appropriate format')
    """
    log.debug(
        'Adding the columns MODALIDADE e SUBMODALIDADE to the premiums table to permit the join with the config table'
    )
    tabela_premios = adiciona_modalidade(tabela_premios, dicionario_de_modalidades)
    log.debug(f'The premiums table contains {len(tabela_premios)} lines and {len(tabela_premios.columns)} columns')
    """


if __name__ == '__main__':
    df_premiums = db['FM_HRECICOBERTURASANO', {'nrows': 10}]
    df_reinsurance = db['FM_HRECRESSEGUROANO', {'nrows': 10}]
    df_commissions = db['FM_HRECICOBERTURASANO_COMISSAO', {'nrows': 10}]
    df_config = db['CONFIG_MARGENS_COBERTURAS', {'nrows': 10}]

    print(df_premiums)
    """
    group = df_premiums.groupby('APOLICE')
    print(group.groups)

    for i, df in group:
        print(i)
        print(df)

    regrouped = group.apply(lambda x: x)
    print(regrouped)
    
    """
    print(df_reinsurance)
    print(df_commissions)
    print(df_config)


