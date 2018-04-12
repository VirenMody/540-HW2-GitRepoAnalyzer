import urllib.request
from unidiff import PatchSet
import subprocess

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


# TODO Update parameters
def create_und_db(db_name, dir_to_analyze):
    """
    Function to create Understand database for given repo
    :param db_name: repo database name
    :param dir_to_analyze: repo to be analyzed
    :return:
    """
    und_cmd = ['und', '-db', db_name, 'create', '-languages', 'java', 'add', dir_to_analyze, 'analyze']
    execute_command(und_cmd)


# TODO remove extra print line stuff
def execute_command(command, dir=None):
    """
    Function executes given command on CLI
    :param command: to be executed on CLI
    :param dir: path to directory
    :return:
    """
    if dir is None:
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    else:
        p = subprocess.Popen(command, shell=True, cwd=dir, stdout=subprocess.PIPE)

    for line in p.stdout:
        print('LINE: ', line)
    p.wait()
    print('RETURN CODE: ', p.returncode)


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


# Check if script is running as main
if __name__=="__main__":
    # file_lists = []
    # url = 'https://github.com/guillermokrh/simple-java-changes/commit/ca33cf8c7f89766cae41a5100bad711043f37b44.patch'
    # file_lists = patch_files(url)
    # file_paths = patch_file_paths(file_lists)

    db_name = 'old.udb'
    dir_to_analyze = 'C:/Users/Viren/Google Drive/1.UIC/540/hw2/guillermo_rojas_hernandez_viren_mody_hw2/old_db'
    create_und_db(db_name, dir_to_analyze)

    # print(file_lists)
    # print(file_paths)
