import shutil
import os
import xml.sax
import xml.dom.minidom

from .. import fileleaf as fl


def extract_sas_guide_project(path, output_folder='01 SAS project files', aux_files='02 Other files'):
    """
    Extracts the program files from a SAS Guide Project (.egp)
    :param path: directory containing the .egp file
    :param output_folder: directory to be created containing programs files within the sas project
    :param aux_files: directory to be created containing other files within the sas project
    :return: None
    """

    dirs = os.listdir(path)

    # 0 - Checks if the program can run
    number_sas_projects_in_folder = 0
    sas_file = ''

    for file in dirs:
        if file == output_folder:
            raise FileExistsError(f'Cannot create {output_folder} folder since it already exists, will not overwrite')
        if file == aux_files:
            raise FileExistsError(f'Cannot create {aux_files} folder since it already exists, will not overwrite')
        if file[-4:] == '.egp':
            number_sas_projects_in_folder += 1
            sas_file = file

    if number_sas_projects_in_folder != 1:
        raise FileExistsError(f'No SAS project found, or more than one SAS project found, needs exactly one')

    sas_path = os.path.join(path, sas_file)

    # 1 - Create Destination and aux folder
    # targetPath = path + "00 Output\\"
    targetPath = os.path.join(path, output_folder)
    os.mkdir(targetPath)

    # auxPath = path + "01 aux\\"
    auxPath = os.path.join(path, aux_files)
    os.mkdir(auxPath)

    # 2 - Change file extension from .egp to .zip
    fl.change_file_extension(sas_path, '.zip')

    # 3 - Unzip file
    fl.unzip_file(sas_path)

    # 4 - get code
    # parse an xml file by name

    domtree = xml.dom.minidom.parse(auxPath + 'project.xml')
    group = domtree.documentElement

    Elements = group.getElementsByTagName('Elements')[0].getElementsByTagName('Element')

    codesFound = 0

    for elem in Elements:  # elements of project
        if elem.hasAttribute('Type'):
            if elem.getAttribute('Type') == "SAS.EG.ProjectElements.CodeTask":  # if it is code

                codesFound += 1
                print("\n     {}      Element found with code Type: {}".format(codesFound, elem.getAttribute('Type')))

                name = elem.getElementsByTagName('Label')[0].childNodes[0].data
                folder = elem.getElementsByTagName('ID')[0].childNodes[0].data

                print("                  Name:    " + name)
                print("                  Folder:  " + folder)

                # handle multiple files with same name
                reps = 0
                originalName = name
                while os.path.exists(targetPath + name + ".sas"):
                    reps += 1
                    name = originalName + " ({})".format(reps)

                if reps > 0:
                    print(
                        "WARNING:          file with name {} already exists changing name to {}".format(originalName,
                                                                                                        name))

                # copy file
                try:
                    shutil.copy2(auxPath + folder + "\\code.sas", targetPath + name + ".sas")
                    print("                  Success coping")
                    print("                         From: " + auxPath)
                    print("                         To:   " + targetPath + name + ".sas")

                except:
                    print("WARNING:         " + auxPath + " is empty")



