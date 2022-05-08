from config import *
from logs import *
import logging
import inspect

log = logging.getLogger('Playground.4')

# from src.magicroot.databranch.directorymanager.folder import *
from src.magicroot.databranch.directorymanager.folder import *


if __name__ == '__main__':
    print(home['Deloitte\\Lusitania'])
    print(Navigator('Deloitte\\Lusitania'))


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
