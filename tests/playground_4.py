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
    mr.databranch.directorymanager.CSV.set_default_settings(settings)
    print(home['documents\\lus\\Scripts'].get('PORTFOLIO_DICTIONARY'))


    file_path = os.path.realpath(__name__)
    print(file_path)


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
