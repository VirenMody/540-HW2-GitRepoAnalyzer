import urllib.request
from unidiff import PatchSet
import subprocess
import pandas as pd

df_headers = ['ChangeCategory', 'BeforeValue', 'AfterValue', 'filename', 'scope', 'occurrence', 'prTitle']


# Understand Helper Functions
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


def create_und_db(db_name, dir_to_analyze):
    """
    Function to create Understand database for repo for commit [hash]
    :param db_name: [repo database name].udb
    :param dir_to_analyze: path to repo to be analyzed
    :return: return code returned from execute_command function call
    """
    und_cmd = ['und', '-db', db_name, 'create', '-languages', 'java', 'add', dir_to_analyze, 'analyze']
    return execute_command(und_cmd)


# TODO Remove console logging
def execute_command(command, dir=None):
    """
    Function executes given command on CLI (i.e. create udb files, checkout specific commits, etc.)
    :param command: to be executed on CLI
    :param dir: path to directory
    :return: return code from subprocess call
    """

    if dir is None:
        p = subprocess.Popen(command, shell=True)
    else:
        p = subprocess.Popen(command, shell=True, cwd=dir)
    p.wait()

    # Return Code: 0 (no error), 128 (possible: 'fatal: reference is not a tree: [commit]')
    return p.returncode


def get_files_from_patch(url):
    """
    Function parses patch file/url for affected files and returns a dictionary of files
    :param url: patch URL from pull request
    :return: files: dictionary of added, modified, and deleted files
    """
    diff = urllib.request.urlopen(url)
    # Assume encoding is utf-8
    patch = PatchSet(diff, encoding='utf-8')

    files = {'added_files': patch.added_files, 'modified_files': patch.modified_files, 'removed_files': patch.removed_files}

    return files


def create_df():
    """
    Function creates Python Pandas DataFrame used to store changes found in pull requests
    :return: data_frame: DataFrame
    """
    data_frame = pd.DataFrame(columns=df_headers)
    return data_frame


def add_row_to_df(df, new_row):
    """
    Function inserts each new change found when analyzing commits into DataFrame
    :param df: old Python Pandas DataFrame of change
    :param new_row: list of new change categorized
    :return: df: updated
    """
    new_df = pd.DataFrame(new_row, columns=df_headers)
    df = df.append(new_df, ignore_index=True)
    return df


# Check if script is running as main
if __name__ == "__main__":
    df = create_df()
