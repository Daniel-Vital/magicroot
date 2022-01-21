

from logs import *
from config import *




log = log.getLogger('Main')

df = db['FM_SINISTROS', {'on_bad_lines': 'skip'}]
# df = db.tables.get_dataframe('FM_SINISTROS', overwrite_configs={'on_bad_lines': 'skip'})




log.debug('01. Preprocesses the input data and transforms it into readable csv')
df = mr.EventsDataFrame()

accounts = {
    # level 1
    ('Balance', None),
    ('Profit_Loss', None),
    # level 2
    ('Asset', 'Balance'),
    ('Liability', 'Balance'),
    ('Profit', 'Profit_Loss'),
    ('Loss', 'Profit_Loss'),
    # level 3
    ('Cash', 'Asset'),
    ('Stock', 'Asset'),
    ('Option', 'Asset'),
    ('Margin', 'Liability'),
    ('Stock_Gains_Realized', 'Profit')

}

po = mr.PartiallyOrderedSet(accounts)
print(po)

