import logging as log

log_file = 'tests/logs/tests.log'

log.basicConfig(level=log.DEBUG,
                filename=log_file,
                filemode='w',
                format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'
                )
