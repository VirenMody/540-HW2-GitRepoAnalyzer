
import urllib.request
from unidiff import PatchSet
import understand
import subprocess
import os
import pandas as pd
import numpy as np
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

# Test Java Repository: guillermokrh/simple-java-changes

def my_func():
    return 1

# Understand Helper Functions
def understand_entity_info(ent):
    print("---------------------")
    print("Entity Name: ", ent.name())
    print("Annotations: ", str(ent.annotations()))
    print("Comments: ", str(ent.comments()))
    print("Contents: ", ent.contents())
    print("Depends: ", ent.depends())
    print("Depends By: ", ent.dependsby())
    print("Entities: ", str(ent.ents("")))
    print("Filerefs: ", str(ent.filerefs()))
    print("ID: ", str(ent.id()))
    print("Kind: ", ent.kind())
    print("Kindname: ", ent.kindname())
    print("Language: " + ent.language())
    print("Library: " + ent.library())
    print("Longname: " + ent.longname())
    print("Metrics: ", str(ent.metrics()))
    print("Metric: ", ent.metric(ent.metrics()))
    print("Name: ", ent.name())
    print("Parameters: ", ent.parameters())
    print("Parent: ", ent.parent())
    print("Ref: ", ent.ref())
    print("Refs: ", ent.refs())
    print("Type: ", ent.type())
    print("Uniquename: ", ent.uniquename())
    print("Value: ", ent.value())
    print("---------------------")


def create_und_db(path):
    # subprocess.call('/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/understand_files/create_und.sh')
    # subprocess.Popen('ls -la', shell=True)

    # test = subprocess.Popen('und create -db project.udb -languages java')
    cmd = 'ls -la'
    os.system('und create -db project.udb -languages java')
    # subprocess.Popen("und add -db project.udb \"/home/guillermo/cs540/guillermo_rojas_hernandez_viren_mody_hw2/old_db\"", shell=True)
    #subprocess.Popen('und -db project.udb analyze', shell=True)
    #subprocess.Popen('und -db project.udb report', shell=True)


# Patch File Helper Functions
def patch_info(url):
    diff = urllib.request.urlopen(url)
    # Assume encoding is utf-8
    patch = PatchSet(diff, encoding='utf-8')
    print("Additions: " + str(patch.added))
    print("Deletions: " + str(patch.removed))
    added_files = patch.added_files
    modified_files = patch.modified_files
    removed_files = patch.deleted_files
    print("Added Files: " + str(added_files))
    print("Modified Files: " + str(modified_files))
    print("Removed Files: " + str(removed_files))


# Stores files in file struct, 0: added, 1: deleted, 2: modified
def patch_files(url):
    files = []
    diff = urllib.request.urlopen(url)
    # Assume encoding is utf-8
    patch = PatchSet(diff, encoding='utf-8')

    files.append(patch.added_files)
    files.append(patch.modified_files)
    files.append(patch.removed_files)

    return files


def patch_file_paths(file_lists):
    file_paths = []
    for file_list in file_lists:
        for file in file_list:
            file_paths.append(file.path)

    return file_paths

def create_pandas_db():

    df = pd.DataFrame({'Method': 'm1',
                       'ChangeType': pd.Categorical(["parameter", "if_statement", "return_type", "return_value"]),
                       'ChangeValue': pd.Series(1, index=list(range(4)), dtype='int32'),
                       'F': ['foo', 'bar', 'fizz', 'buzz']})
    print(df)

'''
output of create_xml_output(): 
<output>
    <method>m1
        <frequency> 20 </frequency>
        <file> f.java </file>
        <change>
            <parameter> salary
                <oldtype>int</oldtype>
                <newtype>double</newtype>
            </parameter>
        </change>
        <change>
            <ifstatement> salary
                <addcondition>if salary \gt 0 return true<addcondition>
            </ifstatement>
        </change>
    </method>
</output>
'''
# method: 'm1',
# frequency: '20',
# file: 'f.java',
### first tuple is tag name, text, remaining tuples are the children for that change
# change list: [
#                  [('parameter', 'salary'), ('oldtype','int'), ('newtype','int')],
#                  [('ifstatement', 'salary'), ('addcondition', 'if salary \gt 0 return true')]
#              ]
def create_xml_output():
    output = Element('output')
    title = Comment('Output of Changes for CS540 HMW2')

    output.append(title)
    method = SubElement(output, 'method')
    method.text = 'ml'

    frequency = SubElement(method, 'frequency')
    frequency.text = '20'
    
    file = SubElement(method, 'file')
    file.text = 'f.java'

    # First Change
    change = SubElement(method, 'change')

    parameter = SubElement(change, 'parameter')
    parameter.text = 'salary'

    old_type = SubElement(parameter, 'oldtype')
    old_type.text = 'int'
    new_type = SubElement(parameter, 'newtype')
    new_type.text = 'double'

    # Second change
    change2 = SubElement(method, 'change')
    ifstatement = SubElement(change2, 'ifstatement')
    ifstatement.text = 'salary'
    addcondition = SubElement(ifstatement, 'addcondition')
    addcondition.text = 'if salary \gt 0 return true'

    print(tostring(output))


# Check if script is running as main
if __name__=="__main__":
    # file_lists = []
    # url = 'https://github.com/guillermokrh/simple-java-changes/commit/ca33cf8c7f89766cae41a5100bad711043f37b44.patch'
    # file_lists = patch_files(url)
    # file_paths = patch_file_paths(file_lists)
    # create_und_db("path")
    # print(file_lists)
    # print(file_paths)
    create_pandas_db()
    # create_xml_output()
