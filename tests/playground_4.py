from config import *
from logs import *
import logging
import inspect
import os

log = logging.getLogger('Playground.4')

# from src.magicroot.databranch.directorymanager.folder import *
from src.magicroot.databranch.directorymanager.folder import *
from src import magicroot as mr

if __name__ == '__main__':
    d = {'A': 1, 'B': 2}
    # print(home['documents\\lus\\Scripts'].new_file('settings.json', d))
    settings = {'read': {'delimiter': ';', 'decimal': ',', 'encoding': 'latin-1', 'quotechar': '"'}}
    default_configs = {
        '.csv': {'delimiter': ';', 'decimal': ',', 'encoding': 'latin-1', 'quotechar': '"'},
        '.sas7bdat': {'encoding': 'latin-1'}
    }
    # mr.databranch.directorymanager.CSV.set_default_settings(settings)
    folder = home['Lus\\IFRS 17\\Motor de calculo\\data model tables\\output\\groping\\pre-performing']

    excel = folder.get(
        file='grouping validation',
        sheet_name='02 | Benchmark Justification',
        usecols='B:AF',
        skiprows=10
    )
    print(excel.head())
    # folder.new_file('LUS - IFRS17 - Grouping_Validation_v2.00.xlsx', excel, sheet_name='03 | Code', startcol='AF', startrow=10)


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
