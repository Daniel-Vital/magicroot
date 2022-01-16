

from src import magicroot as mr
from logs import *

log = log.getLogger('Main')

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

