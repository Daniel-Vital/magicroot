import os

sep = os.path.sep

full_path = os.path.realpath(__name__).replace('.', sep)

components = full_path.split(sep)[:-1]

settings_path = sep.join(components)
