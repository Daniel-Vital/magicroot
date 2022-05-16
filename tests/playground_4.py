import logging

log = logging.getLogger('Playground.4')

# from src.magicroot.databranch.os.folder import *
from src.magicroot.os.folder import *
import src.magicroot as mr


if __name__ == '__main__':


    df_insurance_cashflow = dm_ifrs17.get('insurance_cashflow')
    df = group_out_folder.get('insurance_contract_disc.csv', index_col=0)

    query = 'ALLOC_INSURANCE_CONTRACT_GROUP_ID == "D02100C2020" & CASHFLOW_TYPE_CD == "EXR"'
    # print(df_insurance_cashflow.sample(100))

    df = df.query(query).sample(10)

    # print(df)

    # df = mr.df.format.as_date(df, ['CASHFLOW_DT'])
    # df = mr.df.format.as_date(df, ['CASHFLOW_DT', 'REPORTING_DT'])
    # df = mr.df.format.as_date(df, ['REPORTING_DT', 'CASHFLOW_DT'])
    # df = mr.df.compute.duration(df, 'BEGIN_COV_DT', 'END_COV_DT', computed_column='Cohort_dur', errors='coerce')
    # df = mr.df.compute.duration(df, 'BEGIN_COV_DT', 'REPORTING_DT', computed_column='COhort_passed', errors='coerce')
    # df['x'] = df['Cohort_dur'] / df['COhort_passed']
    # print(mr.df.compute.duration(df, 'BEGIN_COV_DT', 'REPORTING_DT', computed_column='COhort_passed', errors='coerce'))
    # df['x'] = mr.df.compute.duration(df, 'BEGIN_COV_DT', 'REPORTING_DT', computed_column='COhort_passed', errors='coerce') / mr.df.compute.duration(df, 'BEGIN_COV_DT', 'END_COV_DT', computed_column='Cohort_dur', errors='coerce')
    df = mr.df.compute.date_perc(df, 'BEGIN_COV_DT', 'END_COV_DT', 'REPORTING_DT')

    print(df)


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
