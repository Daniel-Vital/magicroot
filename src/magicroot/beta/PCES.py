import shutil
import zipfile
import os, sys
import xml.sax
import xml.dom.minidom

# Folder where sas project is (the folder should only contain the .egp file)
path = 'C:\\Users\\daalcantara\\Documents\\00_Macros\\02_Python\\'


def insert_separator(string):
    """
    Inserts the apropriate separator before the first encontered non-digit non-space caracter (letter)
    """
    insert_at = 0
    for i in range(0, len(string)):
        c = string[i]
        if not (c.isdigit() or c == " ") and insert_at == 0:
            insert_at = i
    return string[:insert_at] + "\t" + string[insert_at:]


def asf_pces(line):
    """
    Used for ASF PCES translation
    """
    if line[0].isdigit() and line[1].isdigit() and line[2] == " ":
        return insert_separator(str(line))
    return None


def sts_pces(line):
    """
    Used for Plano de Contas do Santader Seguros translation
    """
    relevant_line = line[:90].strip()
    if len(relevant_line) > 0:
        if relevant_line[0].isdigit():
            return insert_separator(str(relevant_line))
    return None


selected_function = asf_pces

with open(path + 'PCES.txt', 'r', encoding='utf-8') as file_input:
    with open(path + 'PCES_output.txt', 'w', encoding='utf-8') as file_output:
        for line in file_input:
            treated_line = selected_function(line)
            if treated_line is not None:
                file_output.write(treated_line + '\n')

print('I ran something')