import logging

log = logging.getLogger('Playground.4')

# from src.magicroot.databranch.os.folder import *
from src.magicroot.os.folder import *
import src.magicroot as mr


if __name__ == '__main__':
    group_out_folder = mr.os.home['lus\\ifrs 17\\motor de calculo\\data model tables\\outputs\\grouping\\reperforming']
    dm_ifrs17 = mr.os.home['LUS\\IFRS 17\\Motor de calculo\\tables\\input\\name change']

    # print(dm_ifrs17)

    df_icg_x_curve = dm_ifrs17.get('group_x_curve')
    df_rf_x_rf_curve = dm_ifrs17.get('factor_x_risk', encoding='UTF-8')
    df_quotes = dm_ifrs17.get('quotes', encoding='UTF-8')

    df_icg_x_curve = df_icg_x_curve.rename(columns={'CURRENT_CURVE_ID': 'CURVE_ID'})
    df_rf_x_rf_curve = df_rf_x_rf_curve.rename(columns={'RISK_FACTOR_ID': 'QUOTE_ID'})

    print(df_quotes.head())
    print(df_rf_x_rf_curve.head())
    print(df_icg_x_curve.head())
    # print('----------------')
    # print(mr.df.sample.columns_in_list(df_icg_x_curve, columns=['CURVE_ID']))
    print('----------------')
    print(*mr.df.sample.join(df_icg_x_curve, df_rf_x_rf_curve, df_quotes, on=['INSURANCE_CONTRACT_GROUP_ID', 'QUOTE_ID', 'CURVE_ID'], n=1), sep='\n\n')



    # print(df_insurance_cashflow)

# print(os.path.expanduser('~'))

"""

/etc
├── acpi
│   ├── asus-keyboard-backlight.sh
│   ├── asus-wireless.sh
│   ├── events
│   │   ├── asus-keyboard-backlight-down
│   │   ├── asus-keyboard-backlight-up
│   │   ├── asus-wireless-off
│   │   ├── asus-wireless-on
│   │   ├── ibm-wireless
│   │   ├── lenovo-undock
│   │   ├── thinkpad-cmos

"""
