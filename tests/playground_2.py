

from config import *
import getpass
import re
import datetime as dt
from src.magicroot.databranch.directorymanager.folder import *

dm = DirectoriesManager(folder_database, folders)
df = dm.data
print(df)

dm.save()



