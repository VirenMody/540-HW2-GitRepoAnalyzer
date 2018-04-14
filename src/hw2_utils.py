import urllib.request
from unidiff import PatchSet
import subprocess
import os
import pandas as pd
import numpy as np
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

# Test Java Repository: guillermokrh/simple-java-changes


# Understand Helper Functions

df_headers = ['ChangeCategory', 'BeforeValue', 'AfterValue', 'filename', 'scope', 'occurrence', 'prTitle']


def understand_lexeme_info(lexeme):
    print("----------LEXEME INFO START-----------")
    print("Lexeme Text: ", lexeme.text())
    print("Token: ", lexeme.token())
    print("Entity: ", lexeme.ent())
    print("Column Begin:End: ", lexeme.column_begin(), ':', lexeme.column_end())
    print("Line Begin:End: ", lexeme.line_begin(), ':', lexeme.line_end())
    print("Reference: ", lexeme.ref())
    print("---------LEXEME INFO END------------")


def understand_entity_info(ent):
    print("----------ENTITY INFO START-----------")
    print("Entity Name: ", ent.name())
    # print("Annotations: ", str(ent.annotations()))
    # print("Comments: ", str(ent.comments()))
    print("Contents: ", ent.contents())
    # print("Lexer: ", ent.lexer())
    # print("Depends: ", ent.depends())
    # print("Depends By: ", ent.dependsby())
    # print("Entities: ", str(ent.ents("")))
    # print("Filerefs: ", str(ent.filerefs()))
    # print("ID: ", str(ent.id()))
    print("Kind: ", ent.kind())
    print("Kindname: ", ent.kindname())
    print("Language: " + ent.language())
    print("Library: " + ent.library())
    print("Longname: " + ent.longname())
    print("Metrics: ", str(ent.metrics()))
    print("Metric: ", ent.metric(ent.metrics()))
    # print("Name: ", ent.name())
    print("Parameters: ", ent.parameters())
    print("Parent: ", ent.parent())
    print("Ref: ", ent.ref())
    print("Refs: ", ent.refs())
    print("Type: ", ent.type())
    print("Uniquename: ", ent.uniquename())
    print("Value: ", ent.value())
    print("Info Browser: ", ent.ib())

    print("---------ENTITY INFO END------------")


def print_entities(db):
    current_ents = db.ents('~unresolved ~volatile')
    for ent in current_ents:
        understand_entity_info(ent)


def is_entity_match(ent1, ent2):
    if len(ent1.refs()) == len(ent2.refs()) and \
            len(ent1.ents("")) == len(ent2.ents("")):
        return True
    else:
        return False


# TODO Update parameters
def create_und_db(db_name, dir_to_analyze):
    """
    Function to create Understand database repo
    :param db_name: repo database name
    :param dir_to_analyze: repo to be analyzed
    :return: return code from execute_command
    """
    und_cmd = ['und', '-db', db_name, 'create', '-languages', 'java', 'add', dir_to_analyze, 'analyze']
    g_und_cmd = 'und -db ' + db_name + ' create -languages java add ' + dir_to_analyze + ' analyze'
    return execute_command(g_und_cmd)


# TODO remove extra print line stuff
# TODO Remove console logging+
def execute_command(command, dir=None):
    """
    Function executes given command on CLI
    :param command: to be executed on CLI
    :param dir: path to directory
    :return: return code from subprocess call
    """

    if dir is None:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(command, shell=True, cwd=dir, stdout=subprocess.PIPE)

    for line in p.stdout:
        print('LINE: ', line)
    p.wait()
    print('RETURN CODE: ', p.returncode)

    # Return Code: 128: 'fatal: reference is not a tree: [commit]'
    return p.returncode

# Stores files in file struct, 0: added, 1: modified, 2: deleted
def patch_files(url):
    files = []
    diff = urllib.request.urlopen(url)
    # Assume encoding is utf-8
    patch = PatchSet(diff, encoding='utf-8')

    files.append(patch.added_files)
    files.append(patch.modified_files)
    files.append(patch.removed_files)

    return files


def create_df():
    df = pd.DataFrame(columns=df_headers)
    print(df)
    return df


def add_row_to_df(df, new_row):
    new_df = pd.DataFrame(new_row, columns=df_headers)
    df = df.append(new_df, ignore_index=True)
    # print(df)
    return df

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

    df = create_df()
    new_changes = [['test', 'test', 'test', 'test', 'test', 9]]
    df = add_row_to_df(df, new_changes)
